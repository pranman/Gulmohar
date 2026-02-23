from django import forms
from django.forms import inlineformset_factory

from .models import CaseAsset, CaseChannelSpend, CaseMetric, CaseStudy


class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = CaseStudy
        fields = [
            "title",
            "slug",
            "client_or_org",
            "brand_or_campaign",
            "date_start",
            "date_end",
            "sort_date",
            "location",
            "status",
            "confidentiality",
            "tags",
            "one_liner",
            "objective",
            "audience",
            "constraints",
            "strategy",
            "creative_direction",
            "production_and_tooling",
            "delivery_and_distribution",
            "my_contribution",
            "team_and_partners",
            "results_summary",
            "what_worked",
            "what_id_do_differently",
            "spend_currency",
            "spend_amount_min",
            "spend_amount_max",
            "spend_notes",
            "proof_links",
            "press_mentions",
            "notes_private",
        ]
        widgets = {
            "date_start": forms.DateInput(attrs={"type": "date"}),
            "date_end": forms.DateInput(attrs={"type": "date"}),
            "sort_date": forms.DateInput(attrs={"type": "date"}),
        }


CaseAssetFormSet = inlineformset_factory(
    CaseStudy,
    CaseAsset,
    fields=[
        "asset_type",
        "image",
        "caption",
        "platform",
        "format",
        "date",
        "is_hero",
        "alt_text",
    ],
    widgets={"date": forms.DateInput(attrs={"type": "date"})},
    extra=1,
    can_delete=True,
)

CaseMetricFormSet = inlineformset_factory(
    CaseStudy,
    CaseMetric,
    fields=["metric_name", "value", "timeframe", "source", "notes"],
    extra=1,
    can_delete=True,
)

CaseChannelSpendFormSet = inlineformset_factory(
    CaseStudy,
    CaseChannelSpend,
    fields=["channel", "spend_currency", "spend_amount", "dates", "notes"],
    extra=1,
    can_delete=True,
)
