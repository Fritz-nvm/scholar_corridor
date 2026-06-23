# Django App Structure

This project is now split by responsibility:

- `accounts` owns user-facing account features:
  - login
  - registration
  - email verification
  - password reset
  - profile editing
  - account-related forms, views, URLs, admin, and templates
- `repository` owns paper features:
  - paper submission
  - paper search and listing
  - paper detail pages
  - download handling
  - paper models, forms, views, URLs, admin, and templates

## Why this split exists

The goal is to keep each app focused on one domain so future changes are easier to place, test, and maintain. Account logic no longer sits inside the paper app, which makes it simpler to add new apps later without mixing concerns.

## Current routing pattern

- Project-level URLs live in `scholara/urls.py`.
- `accounts` is mounted under `/accounts/`.
- `repository` is mounted at the site root for paper pages.

## How to add a new app later

1. Create a new app with `python manage.py startapp <app_name>`.
2. Move one feature area into that app only.
3. Add the app to `INSTALLED_APPS` in `scholara/settings.py`.
4. Give the app its own `urls.py` and include it from `scholara/urls.py`.
5. Put app-specific templates inside `<app_name>/templates/<app_name>/`.
6. Keep shared layout files at the project level only when multiple apps need them.
7. Update imports so models, forms, views, and admin code live in the app that owns the feature.

## Practical rule of thumb

If a feature is about users, authentication, or profile state, it belongs in `accounts`.
If a feature is about papers, submissions, departments attached to papers, or search over papers, it belongs in `repository`.

## Notes from this refactor

- `UserProfile` now lives in `accounts.models`.
- Account forms and views now live in `accounts.forms` and `accounts.views`.
- Paper forms and views stay in `repository`.
- Existing paper templates continue to use the shared `base.html` layout.
