from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("search/", views.search, name="search"),
    path("papers/<slug:slug>/", views.paper_detail, name="paper_detail"),
    path("papers/<slug:slug>/download/", views.download_paper, name="download_paper"),
    path("author/<int:pk>/", views.author_profile, name="author_profile"),
    path("submit/", views.submit_paper, name="submit_paper"),
    path("my-papers/", views.submission_status, name="submission_status"),
]
