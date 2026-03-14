from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile


class AccountFlowTests(TestCase):
    def test_user_profile_is_only_created_once(self):
        user = User.objects.create_user(username="alice", password="secret")

        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

        user.first_name = "Alice"
        user.save()

        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

    def test_profile_page_heading_is_readable(self):
        user = User.objects.create_user(username="bob", password="secret")

        self.client.force_login(user)
        response = self.client.get(reverse("profile"))

        self.assertContains(response, "Your Profile")
