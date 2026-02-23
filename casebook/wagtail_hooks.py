import django_filters
from taggit.models import Tag
from wagtail.admin.filters import WagtailFilterSet
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import CaseStudy


class CaseStudyFilterSet(WagtailFilterSet):
    tag = django_filters.ModelChoiceFilter(
        field_name="tags",
        queryset=Tag.objects.all(),
        label="Tag",
    )

    class Meta:
        model = CaseStudy
        fields = ["status", "confidentiality", "tag"]


class CaseStudyViewSet(SnippetViewSet):
    model = CaseStudy
    icon = "folder-open-inverse"
    menu_label = "Case Studies"
    menu_name = "case_studies"
    list_display = ["title", "client_or_org", "status", "confidentiality", "sort_date"]
    search_fields = ["title", "client_or_org", "brand_or_campaign", "one_liner"]
    filterset_class = CaseStudyFilterSet


register_snippet(CaseStudyViewSet)
