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
    image_urls = None
    video_url = None
    if asset.image:
        image_urls = {"original": asset.image.file.url}
        for key, spec in [("fill_1600x900", "fill-1600x900"), ("max_1200x1200", "max-1200x1200")]:
            try:
                image_urls[key] = asset.image.get_rendition(spec).url
            except Exception:
                image_urls[key] = None
    if asset.video:
        video_url = asset.video.file.url

    return {
        "type": asset.asset_type,
        "caption": asset.caption,
        "platform": asset.platform,
        "format": asset.format,
        "date": asset.date,
        "is_hero": asset.is_hero,
        "alt_text": asset.alt_text,
        "image_urls": image_urls,
        "video": {
            "title": asset.video.title if asset.video else None,
            "url": video_url,
            "filename": asset.video.file.name if asset.video else None,
        },
    }


def _serialize_case(case, include_notes=False):
    payload = {
        "title": case.title,
        "slug": case.slug,
        "organization": case.organization.name if case.organization else None,
        "sector": case.sector.name if case.sector else None,
        "brand_or_campaign": case.brand_or_campaign,
        "date_start": case.date_start,
        "date_end": case.date_end,
        "sort_date": case.sort_date,
        "location": case.location,
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
        "assets": [_serialize_asset(asset) for asset in case.assets.select_related("image", "video").all()],
    }
    if include_notes:
        payload["notes"] = case.notes
    return payload


class Command(BaseCommand):
    help = "Export casebook content to clean JSON."

    def add_arguments(self, parser):
        parser.add_argument("--output", required=True, help="Path to output JSON file.")
        parser.add_argument(
            "--include-notes",
            action="store_true",
            help="Include campaign notes in exported payload.",
        )

    def handle(self, *args, **options):
        output = Path(options["output"])
        include_notes = options["include_notes"]

        queryset = CaseStudy.objects.prefetch_related(
            "tags",
            "metrics",
            "channel_spend",
            "assets__image",
            "assets__video",
        ).order_by("-sort_date", "-date_end", "-date_start", "title")

        cases = [_serialize_case(case, include_notes=include_notes) for case in queryset]

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
