from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class DocumentType(models.TextChoices):
    THESIS = "thesis", "Thesis"
    DISSERTATION = "dissertation", "Dissertation"
    RESEARCH_PAPER = "research_paper", "Research Paper"


class PaperStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class Paper(models.Model):
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="papers")
    department = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=200, blank=True)
    year = models.IntegerField()
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    keywords = models.CharField(
        max_length=500, blank=True, help_text="Comma-separated keywords"
    )
    pdf_file = models.FileField(upload_to="papers/", blank=True)
    status = models.CharField(
        max_length=20, choices=PaperStatus.choices, default=PaperStatus.PENDING
    )
    slug = models.SlugField(max_length=500, unique=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-submission_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("paper_detail", kwargs={"slug": self.slug})

    def keyword_list(self):
        if not self.keywords:
            return []
        return [k.strip() for k in self.keywords.split(",") if k.strip()]

    @property
    def citation_publication_date(self):
        return f"{self.year}/01/01"

    @property
    def citation_online_date(self):
        return self.submission_date.strftime("%Y/%m/%d")

    @property
    def citation_pdf_url(self):
        if self.pdf_file:
            return self.pdf_file.url
        return ""

    @property
    def institution_name(self):
        return "Scholar Corridor"

    @property
    def department_display(self):
        return self.department
