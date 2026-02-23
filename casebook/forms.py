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
            "notes",
        ]
        widgets = {
            "date_start": forms.TextInput(attrs={"placeholder": "2024 or January 2024"}),
            "date_end": forms.TextInput(attrs={"placeholder": "2024 or March 2024"}),
            "sort_date": forms.TextInput(attrs={"placeholder": "Optional sort label, e.g. 2024"}),
        }


CaseAssetFormSet = inlineformset_factory(
    CaseStudy,
    CaseAsset,
    fields=[
        "asset_type",
        "image",
        "video",
        "caption",
        "platform",
        "format",
        "date",
        "is_hero",
        "alt_text",
    ],
    widgets={"date": forms.TextInput(attrs={"placeholder": "January 2024"})},
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
