from django import forms
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Paper


class PaperSubmissionForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = [
            "title",
            "abstract",
            "department",
            "supervisor",
            "year",
            "document_type",
            "keywords",
            "pdf_file",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Full title of the paper"}
            ),
            "abstract": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 6,
                    "placeholder": "Brief summary of the paper content and contributions",
                }
            ),
            "department": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Department"}
            ),
            "supervisor": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Name of supervisor (if applicable)",
                }
            ),
            "year": forms.NumberInput(
                attrs={"class": "form-input", "min": 2000, "max": 2026}
            ),
            "document_type": forms.Select(attrs={"class": "form-input"}),
            "keywords": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Comma-separated keywords"}
            ),
            "pdf_file": forms.FileInput(
                attrs={"class": "form-input", "accept": ".pdf"}
            ),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        base_slug = slugify(instance.title)[:80]
        slug = base_slug
        counter = 1
        while Paper.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug
        if commit:
            instance.save()
        return instance
