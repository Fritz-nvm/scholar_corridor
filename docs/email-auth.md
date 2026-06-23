# Email verification and login flow

Scholar Corridor now uses email verification at signup and email/password login for regular users.

## How it works

1. A user submits the signup form with username, email, and password.
2. The account is created with `is_active = False`.
3. The app generates a signed verification token and emails a link to the user.
4. The user opens the verification link, which activates the account.
5. The login form accepts email and password and authenticates through the custom backend.

## Files involved

- `repository/views.py` contains the signup, login, and verification views.
- `repository/forms.py` contains the email login form and email uniqueness validation.
- `repository/auth_backends.py` authenticates by email or username.
- `scholara/urls.py` routes the login and verification URLs before Django’s built-in auth URLs.
- `scholara/settings.py` configures the authentication backend and local console email backend.
- `repository/templates/registration/login.html` uses email/password fields.
- `repository/templates/repository/verification_sent.html` confirms that the verification email was sent.
- `repository/templates/repository/emails/verification_email.txt` is the email body.

## Local development

The project uses Django’s console email backend by default, so verification emails print to the terminal instead of being sent through SMTP.

If you want real email delivery, replace these settings in `scholara/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@your-domain.com'
```

Then add your SMTP host, username, password, and port.

## Notes

- Existing inactive accounts must verify their email before they can sign in.
- Admin login still works because the custom backend accepts both email and username.
- The verification link expires according to Django’s default token rules.
