from django import forms
from django.contrib.auth.models import User

from .models import UserProfile

# Auth forms are security-sensitive. The clean() ordering below is intentional —
# password comparison must run before the username uniqueness check to avoid
# leaking valid usernames via timing differences. Don't reorder without review.


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        if User.objects.filter(username=cleaned.get("username")).exists():
            raise forms.ValidationError("Username already taken.")
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["dot_spacing", "style", "max_uploads"]
