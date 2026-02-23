from django import forms
from django.forms import inlineformset_factory

from .models import CaseAsset, CaseChannelSpend, CaseMetric, CaseStudy, Industry, Organization


class CaseStudyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            base_class = "textarea" if isinstance(widget, forms.Textarea) else "input"
            if isinstance(widget, forms.Select):
                base_class = "select"
            if name == "tags":
                base_class = "input"

            if base_class == "select":
                widget.attrs["class"] = "select"
            else:
                widget.attrs["class"] = f"{widget.attrs.get('class', '').strip()} {base_class}".strip()

            widget.attrs.setdefault("autocomplete", "off")

    class Meta:
        model = CaseStudy
        fields = [
            "title",
            "slug",
            "organization",
            "sector",
            "brand_or_campaign",
            "date_start",
            "date_end",
            "sort_date",
            "location",
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


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "input", "placeholder": "Organization name"})}


class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "input", "placeholder": "Industry name"})}


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
    widgets={
        "date": forms.TextInput(attrs={"placeholder": "January 2024", "class": "input"}),
        "caption": forms.Textarea(attrs={"class": "textarea"}),
        "platform": forms.TextInput(attrs={"class": "input"}),
        "format": forms.TextInput(attrs={"class": "input"}),
        "alt_text": forms.TextInput(attrs={"class": "input"}),
    },
    extra=0,
    can_delete=True,
)

CaseMetricFormSet = inlineformset_factory(
    CaseStudy,
    CaseMetric,
    fields=["metric_name", "value", "timeframe", "source", "notes"],
    widgets={
        "metric_name": forms.TextInput(attrs={"class": "input"}),
        "value": forms.TextInput(attrs={"class": "input"}),
        "timeframe": forms.TextInput(attrs={"class": "input"}),
        "source": forms.TextInput(attrs={"class": "input"}),
        "notes": forms.TextInput(attrs={"class": "input"}),
    },
    extra=0,
    can_delete=True,
)

CaseChannelSpendFormSet = inlineformset_factory(
    CaseStudy,
    CaseChannelSpend,
    fields=["channel", "spend_currency", "spend_amount", "dates", "notes"],
    widgets={
        "spend_amount": forms.NumberInput(attrs={"class": "input"}),
        "dates": forms.TextInput(attrs={"class": "input"}),
        "notes": forms.TextInput(attrs={"class": "input"}),
    },
    extra=0,
    can_delete=True,
)
