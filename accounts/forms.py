from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import UserProfile


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "First name"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Last name"}
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-input", "placeholder": "your.email@example.org"}
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input pr-12",
                "placeholder": "Minimum 8 characters",
                "autocomplete": "new-password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input pr-12",
                "placeholder": "Confirm your password",
                "autocomplete": "new-password",
            }
        )
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "The two password fields did not match.")
        if password1:
            try:
                validate_password(password1)
            except ValidationError as exc:
                self.add_error("password1", exc)
        return cleaned_data

    def _generate_username(self, email):
        base = email.split("@", 1)[0][:24] or "user"
        candidate = base
        counter = 1
        while User.objects.filter(username__iexact=candidate).exists():
            suffix = str(counter)
            candidate = f"{base[: max(1, 30 - len(suffix) - 1)]}_{suffix}"
            counter += 1
        return candidate

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]
        user.email = email
        user.username = self._generate_username(email)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-input", "placeholder": "your.email@example.org"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input pr-12",
                "placeholder": "Your password",
                "autocomplete": "current-password",
            }
        )
    )


class PasswordResetRequestForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-input", "placeholder": "your.email@example.org"}
        )
    )


class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-input pr-12",
                "autocomplete": "new-password",
            }
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-input pr-12",
                "autocomplete": "new-password",
            }
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["department", "bio"]
        widgets = {
            "department": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Your department"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 3,
                    "placeholder": "Brief bio about yourself",
                }
            ),
        }
