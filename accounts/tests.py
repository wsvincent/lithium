import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)
class AccountTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "Example-password-429!"
        cls.user = get_user_model().objects.create_user(
            username="learner", email="learner@example.com", password=cls.password
        )

    def test_account_pages(self):
        for name, template in (
            ("account_login", "account/login.html"),
            ("account_signup", "account/signup.html"),
            ("account_reset_password", "account/password_reset.html"),
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)
                self.assertContains(response, 'type="email"')

    def test_signup_with_email(self):
        response = self.client.post(
            reverse("account_signup"),
            {"email": "new@example.com", "password1": self.password},
        )
        self.assertRedirects(response, reverse("home"))
        user = get_user_model().objects.get(email="new@example.com")
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_login_with_email(self):
        response = self.client.post(
            reverse("account_login"),
            {"login": self.user.email, "password": self.password},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("account_logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_password_reset(self):
        response = self.client.post(
            reverse("account_reset_password"), {"email": self.user.email}
        )
        self.assertRedirects(response, reverse("account_reset_password_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        reset_url = re.search(r"https?://[^\s]+", mail.outbox[0].body).group()
        response = self.client.get(reset_url, follow=True)
        self.assertTemplateUsed(response, "account/password_reset_from_key.html")

        new_password = "Updated-password-853!"
        response = self.client.post(
            response.request["PATH_INFO"],
            {"password1": new_password, "password2": new_password},
        )
        self.assertRedirects(response, reverse("account_reset_password_from_key_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_admin_user_forms(self):
        admin = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password=self.password
        )
        self.client.force_login(admin)
        for name, args in (
            ("admin:accounts_customuser_add", []),
            ("admin:accounts_customuser_change", [self.user.pk]),
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'name="username"')
