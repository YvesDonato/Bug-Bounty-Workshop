import os
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image

from accounts.models import UserProfile
from processor.models import BatchJob, ImageUpload, Preset


class Command(BaseCommand):
    help = "Seed the database with sample data for the bug bounty workshop"

    def handle(self, *args, **options):
        self.stdout.write("Seeding workshop data...")

        # Create test users
        users = []
        for i, name in enumerate(["alice", "bob", "charlie"], 1):
            user, created = User.objects.get_or_create(
                username=name,
                defaults={"email": f"{name}@example.com"},
            )
            if created:
                user.set_password("workshop2024")
                user.save()
                self.stdout.write(f"  Created user: {name}")
            else:
                self.stdout.write(f"  User exists: {name}")

            # Create profile manually (since signal is buggy)
            UserProfile.objects.get_or_create(user=user)
            users.append(user)

        # Create sample images (simple colored squares)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "uploads"), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "processed"), exist_ok=True)

        colors = [
            ("red_square", (255, 0, 0)),
            ("green_square", (0, 255, 0)),
            ("blue_square", (0, 0, 255)),
            ("gradient", None),
        ]

        for user in users:
            for name, color in colors:
                img = Image.new("RGB", (200, 200))
                if color:
                    for x in range(200):
                        for y in range(200):
                            img.putpixel((x, y), color)
                else:
                    # Create a gradient
                    for x in range(200):
                        for y in range(200):
                            val = int(255 * x / 200)
                            img.putpixel((x, y), (val, val, val))

                # Save to a temp buffer
                from io import BytesIO

                buf = BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)

                upload, created = ImageUpload.objects.get_or_create(
                    user=user,
                    title=f"{name} by {user.username}",
                    defaults={"original": ContentFile(buf.read(), name=f"{name}_{user.username}.png")},
                )
                if created:
                    self.stdout.write(f"  Created image: {upload.title}")

        # Create sample presets
        preset_configs = [
            ("Fine Detail", {"dot_spacing": 5, "style": "classic"}),
            ("Bold Dots", {"dot_spacing": 20, "style": "classic"}),
            ("Diamond Art", {"dot_spacing": 15, "style": "diamond"}),
            ("Line Sketch", {"dot_spacing": 8, "style": "line"}),
        ]

        for user in users[:2]:  # Only alice and bob get presets
            for name, config in preset_configs:
                Preset.objects.get_or_create(
                    user=user,
                    name=name,
                    defaults={"config": config},
                )

        # Create a sample batch job for alice
        batch, created = BatchJob.objects.get_or_create(
            user=users[0],
            defaults={
                "total_images": 3,
                "processed_count": 2,
                "status": "completed",
            },
        )
        if created:
            self.stdout.write("  Created sample batch job")

        self.stdout.write(self.style.SUCCESS("\nWorkshop data seeded successfully!"))
        self.stdout.write(f"  Users: {', '.join(u.username for u in users)}")
        self.stdout.write("  Password for all: workshop2024")
        self.stdout.write(f"  Images: {ImageUpload.objects.count()}")
        self.stdout.write(f"  Presets: {Preset.objects.count()}")
