from django.contrib import admin
from .models import Paper


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "department",
        "document_type",
        "status",
        "year",
        "submission_date",
    )
    list_filter = ("status", "department", "document_type", "year")
    search_fields = (
        "title",
        "abstract",
        "keywords",
        "author__username",
        "author__first_name",
        "author__last_name",
    )
    actions = ["approve_papers", "reject_papers"]
    readonly_fields = ("slug", "submission_date")

    @admin.action(description="Approve selected papers")
    def approve_papers(self, request, queryset):
        from django.utils import timezone

        queryset.update(status="approved", reviewed_at=timezone.now())

    @admin.action(description="Reject selected papers")
    def reject_papers(self, request, queryset):
        from django.utils import timezone

        queryset.update(status="rejected", reviewed_at=timezone.now())
