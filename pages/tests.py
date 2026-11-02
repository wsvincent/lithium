from django.test import SimpleTestCase, override_settings
from django.urls import reverse


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)
class PageTests(SimpleTestCase):
    def test_pages(self):
        for name, template in (
            ("home", "pages/home.html"),
            ("about", "pages/about.html"),
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)
