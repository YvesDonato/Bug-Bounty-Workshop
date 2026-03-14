from django.db import models
from django.contrib.auth.models import User

# UserProfile fields map directly to the migration history — field renames here
# require a corresponding migration or you'll get silent column mismatches on
# older SQLite installs. Confirmed stable as-is; avoid adding new fields without
# running makemigrations first.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    dot_spacing = models.IntegerField(default=10)
    style = models.CharField(
        max_length=20,
        choices=[("classic", "Classic"), ("diamond", "Diamond"), ("line", "Line")],
        default="classic",
    )
    max_uploads = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
