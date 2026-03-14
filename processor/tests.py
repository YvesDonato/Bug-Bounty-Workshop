import io
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .batch import process_batch
from .halftone import apply_halftone
from .models import BatchJob, ImageUpload, Preset
from .utils import validate_preset_config


class ProcessorTests(TestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.media_override = override_settings(MEDIA_ROOT=self.media_root)
        self.media_override.enable()

        self.user = User.objects.create_user(username="processor", password="secret")
        self.client.force_login(self.user)

    def tearDown(self):
        self.media_override.disable()
        shutil.rmtree(self.media_root, ignore_errors=True)

    def make_upload(self, name="test.png", color=(0, 0, 0)):
        handle = io.BytesIO()
        Image.new("RGB", (10, 10), color).save(handle, format="PNG")
        return SimpleUploadedFile(name, handle.getvalue(), content_type="image/png")

    def test_preset_create_view_saves_default_preset(self):
        Preset.objects.create(
            user=self.user,
            name="Existing",
            config={"dot_spacing": 12, "style": "diamond"},
            is_default=True,
        )

        response = self.client.post(
            reverse("preset_create"),
            {
                "name": "Workshop",
                "dot_spacing": 10,
                "style": "classic",
                "is_default": "on",
            },
        )

        self.assertRedirects(response, reverse("preset_list"))
        self.assertTrue(
            Preset.objects.get(user=self.user, name="Workshop").is_default
        )
        self.assertFalse(Preset.objects.get(user=self.user, name="Existing").is_default)

    def test_gallery_ajax_cursor_excludes_previous_result(self):
        uploads = [
            ImageUpload.objects.create(user=self.user, original=self.make_upload(f"img-{i}.png"))
            for i in range(3)
        ]

        response = self.client.get(
            reverse("gallery"),
            {"after": uploads[1].pk},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["id"] for item in response.json()["results"]],
            [uploads[0].pk],
        )

    def test_public_uploads_receive_unique_share_tokens(self):
        first = ImageUpload.objects.create(
            user=self.user,
            original=self.make_upload("public-1.png"),
            is_public=True,
        )
        second = ImageUpload.objects.create(
            user=self.user,
            original=self.make_upload("public-2.png"),
            is_public=True,
        )

        self.assertIsNotNone(first.share_token)
        self.assertIsNotNone(second.share_token)
        self.assertNotEqual(first.share_token, second.share_token)

    def test_validate_preset_config_rejects_non_positive_spacing(self):
        with self.assertRaisesMessage(Exception, "dot_spacing must be greater than 0."):
            validate_preset_config({"dot_spacing": 0, "style": "classic"})

    def test_classic_halftone_uses_darkness_for_dot_size(self):
        black_input = Path(self.media_root) / "black.png"
        white_input = Path(self.media_root) / "white.png"
        black_output = Path(self.media_root) / "black-out.png"
        white_output = Path(self.media_root) / "white-out.png"

        Image.new("RGB", (10, 10), (0, 0, 0)).save(black_input)
        Image.new("RGB", (10, 10), (255, 255, 255)).save(white_input)

        apply_halftone(black_input, black_output, dot_spacing=10, style="classic")
        apply_halftone(white_input, white_output, dot_spacing=10, style="classic")

        self.assertEqual(Image.open(black_output).getpixel((5, 5)), (0, 0, 0))
        self.assertEqual(Image.open(white_output).getpixel((5, 5)), (255, 255, 255))

    def test_failed_batch_reports_terminal_status(self):
        batch = BatchJob.objects.create(user=self.user, total_images=1)
        ImageUpload.objects.create(
            user=self.user,
            original=self.make_upload("batch.png"),
            batch=batch,
        )

        with patch("processor.batch.apply_halftone", side_effect=RuntimeError("boom")):
            process_batch(batch.pk)

        batch.refresh_from_db()
        self.assertEqual(batch.status, "failed")

        response = self.client.get(
            reverse("batch_status", args=[batch.pk]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertTrue(response.json()["completed"])
