import json
from datetime import datetime, timezone
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from casebook.models import CaseStudy


def _split_lines(value):
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]


def _serialize_asset(asset):
    image_urls = {"original": asset.image.file.url}
    for key, spec in [("fill_1600x900", "fill-1600x900"), ("max_1200x1200", "max-1200x1200")]:
        try:
            image_urls[key] = asset.image.get_rendition(spec).url
        except Exception:
            image_urls[key] = None

    return {
        "type": asset.asset_type,
        "caption": asset.caption,
        "platform": asset.platform,
        "format": asset.format,
        "date": asset.date.isoformat() if asset.date else None,
        "is_hero": asset.is_hero,
        "alt_text": asset.alt_text,
        "image_urls": image_urls,
    }


def _serialize_case(case, include_private_notes=False):
    payload = {
        "title": case.title,
        "slug": case.slug,
        "client_or_org": case.client_or_org,
        "brand_or_campaign": case.brand_or_campaign,
        "date_start": case.date_start.isoformat() if case.date_start else None,
        "date_end": case.date_end.isoformat() if case.date_end else None,
        "sort_date": case.sort_date.isoformat() if case.sort_date else None,
        "location": case.location,
        "status": case.status,
        "confidentiality": case.confidentiality,
        "one_liner": case.one_liner,
        "objective": case.objective,
        "audience": case.audience,
        "constraints": case.constraints,
        "strategy": case.strategy,
        "creative_direction": case.creative_direction,
        "production_and_tooling": case.production_and_tooling,
        "delivery_and_distribution": case.delivery_and_distribution,
        "my_contribution": case.my_contribution,
        "team_and_partners": case.team_and_partners,
        "results_summary": case.results_summary,
        "what_worked": case.what_worked,
        "what_id_do_differently": case.what_id_do_differently,
        "spend_currency": case.spend_currency,
        "spend_amount_min": str(case.spend_amount_min) if case.spend_amount_min is not None else None,
        "spend_amount_max": str(case.spend_amount_max) if case.spend_amount_max is not None else None,
        "spend_notes": case.spend_notes,
        "proof_links": _split_lines(case.proof_links),
        "press_mentions": _split_lines(case.press_mentions),
        "tags": [tag.name for tag in case.tags.all()],
        "metrics": [
            {
                "metric_name": metric.metric_name,
                "value": metric.value,
                "timeframe": metric.timeframe,
                "source": metric.source,
                "notes": metric.notes,
            }
            for metric in case.metrics.all()
        ],
        "channel_spend": [
            {
                "channel": spend.channel,
                "spend_currency": spend.spend_currency,
                "spend_amount": str(spend.spend_amount) if spend.spend_amount is not None else None,
                "dates": spend.dates,
                "notes": spend.notes,
            }
            for spend in case.channel_spend.all()
        ],
        "assets": [_serialize_asset(asset) for asset in case.assets.select_related("image").all()],
    }
    if include_private_notes:
        payload["notes_private"] = case.notes_private
    return payload


class Command(BaseCommand):
    help = "Export casebook content to clean JSON."

    def add_arguments(self, parser):
        parser.add_argument("--output", required=True, help="Path to output JSON file.")
        parser.add_argument(
            "--include-sensitive",
            action="store_true",
            help="Include case studies marked as status=sensitive.",
        )
        parser.add_argument(
            "--include-private",
            action="store_true",
            help="Include case studies with confidentiality=private.",
        )
        parser.add_argument(
            "--include-private-notes",
            action="store_true",
            help="Include notes_private in exported payload.",
        )

    def handle(self, *args, **options):
        output = Path(options["output"])
        include_sensitive = options["include_sensitive"]
        include_private = options["include_private"]
        include_private_notes = options["include_private_notes"]

        queryset = CaseStudy.objects.prefetch_related(
            "tags",
            "metrics",
            "channel_spend",
            "assets__image",
        ).order_by("-sort_date", "-date_end", "-date_start", "title")

        if not include_sensitive:
            queryset = queryset.exclude(status=CaseStudy.STATUS_SENSITIVE)
        if not include_private:
            queryset = queryset.exclude(confidentiality=CaseStudy.CONFIDENTIALITY_PRIVATE)

        cases = [_serialize_case(case, include_private_notes=include_private_notes) for case in queryset]

        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "count": len(cases),
            "cases": cases,
        }

        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
        except OSError as exc:
            raise CommandError(f"Unable to write export file: {exc}") from exc

        self.stdout.write(self.style.SUCCESS(f"Exported {len(cases)} case studies to {output}"))
