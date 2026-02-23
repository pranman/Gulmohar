import json
from datetime import date
from pathlib import Path
from uuid import uuid4

from django.core.files.images import ImageFile
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Collection

from casebook.models import CaseAsset, CaseChannelSpend, CaseMetric, CaseStudy


def _build_test_assets(test_dir):
    from PIL import Image

    test_dir.mkdir(parents=True, exist_ok=True)
    files = []
    presets = [
        ("creative_red.png", (1800, 1000), (186, 34, 57)),
        ("creative_green.png", (1200, 1200), (26, 121, 93)),
        ("creative_blue.png", (1080, 1920), (39, 82, 163)),
    ]

    for name, size, color in presets:
        path = test_dir / name
        if not path.exists():
            image = Image.new("RGB", size, color)
            image.save(path)
        files.append(path)
    return files


class Command(BaseCommand):
    help = "Create lorem test data, attach generated images, export casebook JSON, and validate output."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="exports/final_casebook_export.json",
            help="Output file for final export JSON.",
        )
        parser.add_argument(
            "--assets-dir",
            default="test_assets",
            help="Folder for generated test images.",
        )

    def handle(self, *args, **options):
        output = Path(options["output"])
        assets_dir = Path(options["assets_dir"])
        image_paths = _build_test_assets(assets_dir)

        case = CaseStudy.objects.create(
            title=f"Lorem Ipsum Campaign {uuid4().hex[:8]}",
            client_or_org="Lorem Org",
            brand_or_campaign="Ipsum Launch",
            date_start=date(2025, 1, 1),
            date_end=date(2025, 3, 31),
            location="UK / US / Global",
            status=CaseStudy.STATUS_PUBLISHABLE,
            confidentiality=CaseStudy.CONFIDENTIALITY_PUBLIC,
            one_liner="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            objective="Grow qualified reach and improve conversion quality.",
            audience="Primary audience: growth-stage founders and operators.",
            constraints="Tight timeline, capped media budget, compliance review.",
            strategy="Test-and-learn creative matrix with channel-specific messaging.",
            creative_direction="Bold color blocks and direct value-led language.",
            production_and_tooling="Built with Python pipelines, Figma, and ad managers.",
            delivery_and_distribution="Weekly creative drops across paid and owned surfaces.",
            my_contribution="Owned strategy, experimentation design, and performance synthesis.",
            team_and_partners="Worked with internal growth, design, and media buying teams.",
            results_summary="Performance improved across efficiency and conversion signals.",
            what_worked="Short-cycle iteration and audience-segmented creative.",
            what_id_do_differently="Increase instrumentation depth from week one.",
            spend_currency=CaseStudy.CURRENCY_GBP,
            spend_amount_min="12000.00",
            spend_amount_max="18000.00",
            spend_notes="Approximate range excluding production.",
            proof_links="https://example.com/report\nhttps://example.com/dashboard",
            press_mentions="https://example.com/press-mention",
            notes_private="Private retrospective note for internal reference.",
        )
        case.tags.add("lorem", "ipsum", "casebook")

        CaseMetric.objects.create(
            case_study=case,
            metric_name="ROAS",
            value="3.2",
            timeframe="Q1 2025",
            source="Meta Ads",
            notes="Sustained after week 4.",
        )
        CaseMetric.objects.create(
            case_study=case,
            metric_name="Reach",
            value="4.5m users",
            timeframe="6 weeks",
            source="GA4",
            notes="Deduplicated estimate.",
        )

        CaseChannelSpend.objects.create(
            case_study=case,
            channel="Meta",
            spend_currency=CaseStudy.CURRENCY_GBP,
            spend_amount="9000.00",
            dates="Jan-Feb 2025",
            notes="Primary spend lane.",
        )
        CaseChannelSpend.objects.create(
            case_study=case,
            channel="Google",
            spend_currency=CaseStudy.CURRENCY_GBP,
            spend_amount="6000.00",
            dates="Feb-Mar 2025",
            notes="Intent capture support.",
        )

        image_model = CaseAsset._meta.get_field("image").remote_field.model
        root_collection = Collection.get_first_root_node()

        for idx, image_path in enumerate(image_paths):
            with image_path.open("rb") as file_handle:
                wagtail_image = image_model(
                    title=f"Test asset {idx + 1} {uuid4().hex[:6]}",
                    collection=root_collection,
                    file=ImageFile(file_handle, name=image_path.name),
                )
                wagtail_image.full_clean()
                wagtail_image.save()

            CaseAsset.objects.create(
                case_study=case,
                asset_type=CaseAsset.TYPE_CREATIVE,
                image=wagtail_image,
                caption=f"Lorem caption {idx + 1}",
                platform="Meta",
                format="1:1" if idx == 0 else "9:16",
                date=date(2025, 1, 15 + idx),
                is_hero=idx == 0,
                alt_text=f"Lorem alt text {idx + 1}",
            )

        call_command("export_casebook", output=str(output))

        payload = json.loads(output.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise CommandError("Export payload must be a JSON object.")
        for key in ["generated_at", "count", "cases"]:
            if key not in payload:
                raise CommandError(f"Export payload missing top-level key: {key}")
        if not payload["cases"]:
            raise CommandError("Export payload contains no cases.")

        first_case = payload["cases"][0]
        required_case_keys = [
            "title",
            "slug",
            "objective",
            "strategy",
            "my_contribution",
            "tags",
            "metrics",
            "channel_spend",
            "assets",
        ]
        missing = [key for key in required_case_keys if key not in first_case]
        if missing:
            raise CommandError(f"Case payload missing required keys: {', '.join(missing)}")
        if "notes_private" in first_case:
            raise CommandError("notes_private should not be exported by default.")

        self.stdout.write(self.style.SUCCESS(f"Final casebook test completed successfully: {output}"))
