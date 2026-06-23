from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    department = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=200, blank=False)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = "repository_userprofile"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
