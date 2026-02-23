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
        fields = ["organization", "sector", "tag"]


class CaseStudyViewSet(SnippetViewSet):
    model = CaseStudy
    icon = "folder-open-inverse"
    menu_label = "Case Studies"
    menu_name = "case_studies"
    list_display = ["title", "organization", "sector", "sort_date"]
    search_fields = ["title", "organization__name", "sector__name", "brand_or_campaign", "one_liner"]
    filterset_class = CaseStudyFilterSet


register_snippet(CaseStudyViewSet)
