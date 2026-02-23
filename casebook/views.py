from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CaseAssetFormSet,
    CaseChannelSpendFormSet,
    CaseMetricFormSet,
    CaseStudyForm,
)
from .models import CaseStudy


def casebook_index(request):
    query = request.GET.get("q", "").strip()
    confidentiality = request.GET.get("confidentiality", "").strip()
    status = request.GET.get("status", "").strip()
    tag = request.GET.get("tag", "").strip()

    cases = CaseStudy.objects.all().prefetch_related("tags")

    if query:
        cases = cases.filter(
            Q(title__icontains=query)
            | Q(client_or_org__icontains=query)
            | Q(brand_or_campaign__icontains=query)
            | Q(one_liner__icontains=query)
        )
    if confidentiality:
        cases = cases.filter(confidentiality=confidentiality)
    if status:
        cases = cases.filter(status=status)
    if tag:
        cases = cases.filter(tags__name__iexact=tag)

    cases = cases.distinct().order_by("-sort_date", "-date_end", "-date_start", "title")
    return render(
        request,
        "casebook/index.html",
        {
            "cases": cases,
            "query": query,
            "status": status,
            "confidentiality": confidentiality,
            "tag": tag,
            "status_choices": CaseStudy.STATUS_CHOICES,
            "confidentiality_choices": CaseStudy.CONFIDENTIALITY_CHOICES,
        },
    )


def casebook_detail(request, slug):
    case = get_object_or_404(
        CaseStudy.objects.prefetch_related("assets__image", "assets__video", "metrics", "channel_spend", "tags"),
        slug=slug,
    )
    return render(request, "casebook/detail.html", {"case": case})


def _build_case_form_bundle(request, instance=None):
    case_form = CaseStudyForm(request.POST or None, instance=instance)
    asset_formset = CaseAssetFormSet(request.POST or None, request.FILES or None, instance=instance, prefix="assets")
    metric_formset = CaseMetricFormSet(request.POST or None, instance=instance, prefix="metrics")
    channel_spend_formset = CaseChannelSpendFormSet(
        request.POST or None,
        instance=instance,
        prefix="channel_spend",
    )
    return case_form, asset_formset, metric_formset, channel_spend_formset


def casebook_create(request):
    case_form, asset_formset, metric_formset, channel_spend_formset = _build_case_form_bundle(request)

    if request.method == "POST":
        if (
            case_form.is_valid()
            and asset_formset.is_valid()
            and metric_formset.is_valid()
            and channel_spend_formset.is_valid()
        ):
            case = case_form.save()
            asset_formset.instance = case
            metric_formset.instance = case
            channel_spend_formset.instance = case
            asset_formset.save()
            metric_formset.save()
            channel_spend_formset.save()
            return redirect("casebook_detail", slug=case.slug)

    return render(
        request,
        "casebook/form.html",
        {
            "mode": "create",
            "case_form": case_form,
            "asset_formset": asset_formset,
            "metric_formset": metric_formset,
            "channel_spend_formset": channel_spend_formset,
        },
    )


def casebook_edit(request, slug):
    case = get_object_or_404(CaseStudy, slug=slug)
    case_form, asset_formset, metric_formset, channel_spend_formset = _build_case_form_bundle(
        request,
        instance=case,
    )

    if request.method == "POST":
        if (
            case_form.is_valid()
            and asset_formset.is_valid()
            and metric_formset.is_valid()
            and channel_spend_formset.is_valid()
        ):
            case = case_form.save()
            asset_formset.save()
            metric_formset.save()
            channel_spend_formset.save()
            return redirect("casebook_detail", slug=case.slug)

    return render(
        request,
        "casebook/form.html",
        {
            "mode": "edit",
            "case": case,
            "case_form": case_form,
            "asset_formset": asset_formset,
            "metric_formset": metric_formset,
            "channel_spend_formset": channel_spend_formset,
        },
    )
