from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db.models.functions import Lower, Trim
import re

from repository.models import Paper, PaperStatus

from .forms import EmailLoginForm, SignUpForm, UserProfileForm
from .models import UserProfile


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


def _send_verification_email(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_link = request.build_absolute_uri(
        reverse("verify_email", kwargs={"uidb64": uidb64, "token": token})
    )
    email_body = render_to_string(
        "registration/verification_email.txt",
        {
            "user": user,
            "verification_link": verification_link,
        },
    )
    send_mail(
        subject="Verify your Scholar Corridor account",
        message=email_body,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )


def login_view(request):
    form = EmailLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        password = form.cleaned_data["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("landing")

        pending_user = User.objects.filter(email__iexact=email).first()
        if pending_user and not pending_user.is_active:
            form.add_error(None, "Verify your email before signing in.")
        else:
            form.add_error(None, "Please enter a valid email and password.")

    return render(request, "registration/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect(request, "landing")


@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    department_suggestions = _department_suggestions_for_user(request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile_obj)
        form.fields["department"].widget.attrs["list"] = "department-suggestions"
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile_obj)
        form.fields["department"].widget.attrs["list"] = "department-suggestions"
    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "department_suggestions": department_suggestions,
        },
    )


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.is_active = False
            user.save()
            UserProfile.objects.create(user=user)
            _send_verification_email(request, user)
            return render(
                request,
                "accounts/verification_sent.html",
                {"email": user.email},
            )
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
        UserProfile.objects.get_or_create(user=user)
        messages.success(request, "Your email has been verified. You can sign in now.")
        return redirect("login")

    messages.error(request, "The verification link is invalid or has expired.")
    return redirect("signup")
