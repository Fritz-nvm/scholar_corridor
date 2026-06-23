from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.functions import Lower, Trim
from django.http import FileResponse, HttpResponse
import re
from accounts.models import UserProfile
from .models import Paper, DocumentType, PaperStatus
from .forms import PaperSubmissionForm


def _clean_department_label(name):
    return re.sub(r"\s+", " ", (name or "").strip())


def _normalize_department_key(name):
    return _clean_department_label(name).casefold()


def _canonical_departments(names):
    canonical_by_key = {}
    for name in names:
        clean_name = _clean_department_label(name)
        if not clean_name:
            continue
        key = clean_name.casefold()
        if key not in canonical_by_key:
            canonical_by_key[key] = clean_name
    return canonical_by_key


def _department_suggestions_for_user(user):
    # Prefer departments from the same institution when that metadata is available.
    profile = getattr(user, "profile", None)
    institution = ""
    if profile and profile.institution:
        institution = profile.institution.strip()

    profile_departments_qs = UserProfile.objects.exclude(department="")
    if institution:
        profile_departments_qs = profile_departments_qs.filter(institution=institution)

    profile_departments = profile_departments_qs.values_list("department", flat=True)
    paper_departments = Paper.objects.exclude(department="").values_list(
        "department", flat=True
    )
    canonical = _canonical_departments(
        list(profile_departments) + list(paper_departments)
    )
    return sorted(canonical.values(), key=str.casefold)


def landing(request):
    recent_papers = Paper.objects.filter(status=PaperStatus.APPROVED).select_related(
        "author"
    )[:8]
    approved_departments = Paper.objects.filter(
        status=PaperStatus.APPROVED
    ).values_list("department", flat=True)
    canonical = _canonical_departments(approved_departments)
    department_totals = {key: 0 for key in canonical.keys()}
    for name in approved_departments:
        key = _normalize_department_key(name)
        if key in department_totals:
            department_totals[key] += 1

    ordered_department_counts = sorted(
        ((canonical[key], total) for key, total in department_totals.items() if total),
        key=lambda item: (-item[1], item[0].casefold()),
    )
    department_counts = dict(ordered_department_counts)
    total_papers = Paper.objects.filter(status=PaperStatus.APPROVED).count()
    return render(
        request,
        "repository/landing.html",
        {
            "recent_papers": recent_papers,
            "department_counts": department_counts,
            "total_departments": len(department_counts),
            "total_papers": total_papers,
        },
    )


def search(request):
    papers = Paper.objects.filter(status=PaperStatus.APPROVED).select_related("author")

    q = request.GET.get("q", "")
    department = _clean_department_label(request.GET.get("department", ""))
    document_type = request.GET.get("document_type", "")
    year = request.GET.get("year", "")

    if q:
        papers = papers.filter(
            Q(title__icontains=q)
            | Q(abstract__icontains=q)
            | Q(keywords__icontains=q)
            | Q(author__first_name__icontains=q)
            | Q(author__last_name__icontains=q)
            | Q(author__username__icontains=q)
        )

    if department:
        papers = papers.annotate(department_norm=Lower(Trim("department"))).filter(
            department_norm=department.casefold()
        )

    if document_type:
        papers = papers.filter(document_type=document_type)

    if year:
        try:
            papers = papers.filter(year=int(year))
        except ValueError:
            pass

    papers = papers.order_by("-submission_date")

    years = (
        Paper.objects.filter(status=PaperStatus.APPROVED)
        .values_list("year", flat=True)
        .distinct()
        .order_by("-year")
    )
    department_values = Paper.objects.filter(status=PaperStatus.APPROVED).values_list(
        "department", flat=True
    )
    canonical_departments = _canonical_departments(department_values)
    departments = sorted(canonical_departments.values(), key=str.casefold)

    selected_department = department
    selected_key = _normalize_department_key(department)
    if selected_key and selected_key in canonical_departments:
        selected_department = canonical_departments[selected_key]

    return render(
        request,
        "repository/search.html",
        {
            "papers": papers,
            "q": q,
            "selected_department": selected_department,
            "selected_document_type": document_type,
            "selected_year": year,
            "departments": departments,
            "document_types": DocumentType.choices,
            "years": years,
        },
    )


def paper_detail(request, slug):
    paper = get_object_or_404(Paper, slug=slug, status=PaperStatus.APPROVED)
    return render(request, "repository/paper_detail.html", {"paper": paper})


def author_profile(request, pk):
    from django.contrib.auth.models import User

    author = get_object_or_404(User, pk=pk)
    papers = Paper.objects.filter(author=author, status=PaperStatus.APPROVED).order_by(
        "-submission_date"
    )
    return render(
        request, "repository/author_profile.html", {"author": author, "papers": papers}
    )


@login_required
def download_paper(request, slug):
    paper = get_object_or_404(Paper, slug=slug, status=PaperStatus.APPROVED)
    if not paper.pdf_file:
        messages.error(request, "No PDF file available for this paper.")
        return redirect(paper.get_absolute_url())
    response = FileResponse(
        paper.pdf_file.open("rb"), as_attachment=True, filename=f"{paper.slug}.pdf"
    )
    return response


@login_required
def submit_paper(request):
    department_suggestions = _department_suggestions_for_user(request.user)
    if request.method == "POST":
        form = PaperSubmissionForm(request.POST, request.FILES)
        form.fields["department"].widget.attrs["list"] = "department-suggestions"
        if form.is_valid():
            paper = form.save(commit=False)
            paper.author = request.user
            paper.status = PaperStatus.PENDING
            paper.save()
            messages.success(request, "Your paper has been submitted for review.")
            return redirect("submission_status")
    else:
        form = PaperSubmissionForm()
        form.fields["department"].widget.attrs["list"] = "department-suggestions"
    return render(
        request,
        "repository/submit_paper.html",
        {
            "form": form,
            "department_suggestions": department_suggestions,
        },
    )


@login_required
def submission_status(request):
    papers = Paper.objects.filter(author=request.user).order_by("-submission_date")
    return render(request, "repository/submission_status.html", {"papers": papers})
