from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, ObjectList, TabbedInterface
from wagtail.models import Orderable
from wagtail.search import index


class CaseStudyTag(TaggedItemBase):
    content_object = ParentalKey(
        "casebook.CaseStudy",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class CaseStudy(index.Indexed, ClusterableModel):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHABLE = "publishable"
    STATUS_SENSITIVE = "sensitive"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PUBLISHABLE, "Publishable"),
        (STATUS_SENSITIVE, "Sensitive"),
    ]

    CONFIDENTIALITY_PUBLIC = "public"
    CONFIDENTIALITY_ANONYMISED = "anonymised"
    CONFIDENTIALITY_PRIVATE = "private"
    CONFIDENTIALITY_CHOICES = [
        (CONFIDENTIALITY_PUBLIC, "Public"),
        (CONFIDENTIALITY_ANONYMISED, "Anonymised"),
        (CONFIDENTIALITY_PRIVATE, "Private"),
    ]

    CURRENCY_GBP = "GBP"
    CURRENCY_USD = "USD"
    CURRENCY_EUR = "EUR"
    CURRENCY_OTHER = "Other"
    CURRENCY_CHOICES = [
        (CURRENCY_GBP, "GBP"),
        (CURRENCY_USD, "USD"),
        (CURRENCY_EUR, "EUR"),
        (CURRENCY_OTHER, "Other"),
    ]

    title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Campaign title. Optional for early drafts.",
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="Optional; auto-generated from title if left blank.",
    )
    client_or_org = models.CharField(
        max_length=255,
        blank=True,
        help_text="Client, organization, or stakeholder this work was for.",
    )
    brand_or_campaign = models.CharField(
        max_length=255,
        blank=True,
        help_text="Brand, product, campaign, or initiative name.",
    )
    date_start = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Flexible start date text (e.g. "2024", "January 2024", "Q1 2024").',
    )
    date_end = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Flexible end date text (e.g. "2024", "March 2024", "Q2 2024").',
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text='Geographic scope (e.g. "UK / US / Global").',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        blank=True,
        help_text="Workflow status for inclusion readiness.",
    )
    confidentiality = models.CharField(
        max_length=20,
        choices=CONFIDENTIALITY_CHOICES,
        default=CONFIDENTIALITY_PUBLIC,
        blank=True,
        help_text="Content sensitivity and privacy level.",
    )
    one_liner = models.TextField(blank=True, help_text="One or two sentence summary of the case.")
    objective = models.TextField(blank=True, help_text="What success meant for this case.")
    audience = models.TextField(blank=True, help_text="Who this was for and why they mattered.")
    constraints = models.TextField(
        blank=True,
        help_text="Known restrictions: time, budget, legal, platform, etc.",
    )
    strategy = models.TextField(blank=True, help_text="The strategy used to solve the objective.")
    creative_direction = models.TextField(
        blank=True,
        help_text="Narrative/visual direction and creative rationale.",
    )
    production_and_tooling = models.TextField(
        blank=True,
        help_text="Production process and tools/workflows used.",
    )
    delivery_and_distribution = models.TextField(
        blank=True,
        help_text="How work was shipped and distributed.",
    )
    my_contribution = models.TextField(
        blank=True,
        help_text="Your explicit ownership and decision-making responsibilities.",
    )
    team_and_partners = models.TextField(
        blank=True,
        help_text="Internal team, partners, agencies, and collaborators.",
    )
    results_summary = models.TextField(
        blank=True,
        help_text="Narrative summary of impact and outcomes.",
    )
    what_worked = models.TextField(blank=True, help_text="What proved effective and why.")
    what_id_do_differently = models.TextField(
        blank=True,
        help_text="Retrospective improvements you would make next time.",
    )

    spend_currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default=CURRENCY_GBP,
        help_text="Currency used for spend estimates.",
    )
    spend_amount_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum spend estimate.",
    )
    spend_amount_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum spend estimate.",
    )
    spend_notes = models.TextField(
        blank=True,
        help_text='Assumptions (e.g. "approx, excludes production").',
    )

    proof_links = models.TextField(
        blank=True,
        help_text="One URL per line that supports this case.",
    )
    press_mentions = models.TextField(blank=True, help_text="One citation or link per line.")
    notes = models.TextField(
        blank=True,
        help_text="Public portfolio notes and context.",
    )

    tags = ClusterTaggableManager(through=CaseStudyTag, blank=True)
    sort_date = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Optional sortable date label (e.g. "January 2024", "2024"). Defaults to end/start text.',
    )

    search_fields = [
        index.SearchField("title", partial_match=True),
        index.SearchField("client_or_org", partial_match=True),
        index.SearchField("brand_or_campaign", partial_match=True),
        index.SearchField("one_liner", partial_match=True),
    ]

    overview_panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("client_or_org"),
        FieldPanel("brand_or_campaign"),
        FieldPanel("date_start"),
        FieldPanel("date_end"),
        FieldPanel("sort_date"),
        FieldPanel("location"),
        FieldPanel("status"),
        FieldPanel("confidentiality"),
        FieldPanel("tags"),
        FieldPanel("one_liner"),
    ]
    narrative_panels = [
        FieldPanel("objective"),
        FieldPanel("audience"),
        FieldPanel("constraints"),
        FieldPanel("strategy"),
        FieldPanel("creative_direction"),
        FieldPanel("my_contribution"),
        FieldPanel("team_and_partners"),
        FieldPanel("what_worked"),
        FieldPanel("what_id_do_differently"),
    ]
    delivery_panels = [
        FieldPanel("production_and_tooling"),
        FieldPanel("delivery_and_distribution"),
    ]
    results_panels = [
        FieldPanel("results_summary"),
        FieldPanel("spend_currency"),
        FieldPanel("spend_amount_min"),
        FieldPanel("spend_amount_max"),
        FieldPanel("spend_notes"),
        FieldPanel("proof_links"),
        FieldPanel("press_mentions"),
        InlinePanel("metrics", label="Metrics"),
        InlinePanel("channel_spend", label="Channel spend"),
    ]
    assets_panels = [InlinePanel("assets", label="Assets")]
    private_panels = [FieldPanel("notes")]

    edit_handler = TabbedInterface(
        [
            ObjectList(overview_panels, heading="Overview"),
            ObjectList(narrative_panels, heading="Narrative"),
            ObjectList(delivery_panels, heading="Delivery & Production"),
            ObjectList(results_panels, heading="Results"),
            ObjectList(assets_panels, heading="Assets"),
            ObjectList(private_panels, heading="Private"),
        ]
    )

    class Meta:
        ordering = ["-sort_date", "-date_end", "-date_start", "title"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if (
            self.spend_amount_min is not None
            and self.spend_amount_max is not None
            and self.spend_amount_min > self.spend_amount_max
        ):
            raise ValidationError(
                {"spend_amount_max": "Maximum spend must be greater than or equal to minimum spend."}
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            source = self.title or self.brand_or_campaign or self.client_or_org or f"campaign-{uuid4().hex[:8]}"
            base_slug = slugify(source) or f"campaign-{uuid4().hex[:8]}"
            slug_candidate = base_slug
            counter = 2
            while CaseStudy.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        if not self.sort_date:
            self.sort_date = self.date_end or self.date_start
        super().save(*args, **kwargs)


class CaseAsset(Orderable):
    TYPE_AD_SCREENSHOT = "ad_screenshot"
    TYPE_CREATIVE = "creative"
    TYPE_DASHBOARD = "dashboard"
    TYPE_PRESS = "press"
    TYPE_VIDEO = "video"
    TYPE_OTHER = "other"
    TYPE_CHOICES = [
        (TYPE_AD_SCREENSHOT, "Ad Screenshot"),
        (TYPE_CREATIVE, "Creative"),
        (TYPE_DASHBOARD, "Dashboard"),
        (TYPE_PRESS, "Press"),
        (TYPE_VIDEO, "Video"),
        (TYPE_OTHER, "Other"),
    ]

    case_study = ParentalKey("casebook.CaseStudy", on_delete=models.CASCADE, related_name="assets")
    asset_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default=TYPE_OTHER,
        help_text="Asset category for filtering and export context.",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )
    video = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
        help_text="Optional uploaded video document.",
    )
    caption = models.TextField(blank=True, help_text="Context or explanation for this asset.")
    platform = models.CharField(
        max_length=100,
        blank=True,
        help_text='Source platform (e.g. "Meta", "Google", "TikTok").',
    )
    format = models.CharField(
        max_length=100,
        blank=True,
        help_text='Media format (e.g. "1:1", "9:16", "16:9", "carousel").',
    )
    date = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Flexible date text for this asset (e.g. "January 2024").',
    )
    is_hero = models.BooleanField(
        default=False,
        help_text="Mark as the primary visual for this case (single hero only).",
    )
    alt_text = models.CharField(max_length=255, blank=True, help_text="Accessibility description for the image.")

    panels = [
        FieldPanel("asset_type"),
        FieldPanel("image"),
        FieldPanel("video"),
        FieldPanel("caption"),
        FieldPanel("platform"),
        FieldPanel("format"),
        FieldPanel("date"),
        FieldPanel("is_hero"),
        FieldPanel("alt_text"),
    ]

    def __str__(self):
        return f"{self.case_study.title} - {self.asset_type}"

    def clean(self):
        super().clean()
        if not self.image and not self.video:
            raise ValidationError("Provide either an image or a video document.")
        if self.image and self.video:
            raise ValidationError("Attach only one media type per asset: image or video.")
        if self.is_hero and self.case_study_id:
            queryset = self.case_study.assets.filter(is_hero=True)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            if queryset.exists():
                raise ValidationError({"is_hero": "Only one hero asset is allowed per case study."})


class CaseMetric(Orderable):
    case_study = ParentalKey("casebook.CaseStudy", on_delete=models.CASCADE, related_name="metrics")
    metric_name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Metric label (e.g. "ROAS", "Reach", "Revenue/day").',
    )
    value = models.CharField(
        max_length=255,
        blank=True,
        help_text='Metric value, allowing flexible units (e.g. "ROAS 3.2", "4.5m users").',
    )
    timeframe = models.CharField(
        max_length=255,
        blank=True,
        help_text='Measurement period (e.g. "6 weeks", "Q1 2025").',
    )
    source = models.CharField(
        max_length=255,
        blank=True,
        help_text='Evidence source (e.g. "GA4", "Meta Ads", "Press").',
    )
    notes = models.CharField(max_length=255, blank=True, help_text="Extra metric context or caveats.")

    panels = [
        FieldPanel("metric_name"),
        FieldPanel("value"),
        FieldPanel("timeframe"),
        FieldPanel("source"),
        FieldPanel("notes"),
    ]

    def __str__(self):
        return f"{self.metric_name}: {self.value}"


class CaseChannelSpend(Orderable):
    CHANNEL_META = "Meta"
    CHANNEL_GOOGLE = "Google"
    CHANNEL_TIKTOK = "TikTok"
    CHANNEL_X = "X"
    CHANNEL_LINKEDIN = "LinkedIn"
    CHANNEL_EMAIL = "Email"
    CHANNEL_ORGANIC_SOCIAL = "Organic Social"
    CHANNEL_OTHER = "Other"
    CHANNEL_CHOICES = [
        (CHANNEL_META, "Meta"),
        (CHANNEL_GOOGLE, "Google"),
        (CHANNEL_TIKTOK, "TikTok"),
        (CHANNEL_X, "X"),
        (CHANNEL_LINKEDIN, "LinkedIn"),
        (CHANNEL_EMAIL, "Email"),
        (CHANNEL_ORGANIC_SOCIAL, "Organic Social"),
        (CHANNEL_OTHER, "Other"),
    ]

    case_study = ParentalKey("casebook.CaseStudy", on_delete=models.CASCADE, related_name="channel_spend")
    channel = models.CharField(
        max_length=30,
        choices=CHANNEL_CHOICES,
        default=CHANNEL_OTHER,
        help_text="Channel where spend occurred.",
    )
    spend_currency = models.CharField(
        max_length=10,
        choices=CaseStudy.CURRENCY_CHOICES,
        default=CaseStudy.CURRENCY_GBP,
        help_text="Currency for this channel spend amount.",
    )
    spend_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Spend amount for this channel segment.",
    )
    dates = models.CharField(max_length=255, blank=True, help_text='Date label (e.g. "Jan-Mar 2025").')
    notes = models.CharField(max_length=255, blank=True, help_text="Extra context for this spend item.")

    panels = [
        FieldPanel("channel"),
        FieldPanel("spend_currency"),
        FieldPanel("spend_amount"),
        FieldPanel("dates"),
        FieldPanel("notes"),
    ]

    def __str__(self):
        return f"{self.channel} - {self.spend_amount or 'N/A'}"
