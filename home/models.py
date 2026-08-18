from django.db import models


class HeroSlider(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    label = models.CharField(
        max_length=150,
        blank=True,
    )

    title = models.CharField(
        max_length=200,
    )

    highlight_text = models.CharField(
        max_length=200,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    button1_text = models.CharField(
        max_length=100,
        blank=True,
    )

    button1_url = models.CharField(
        max_length=255,
        blank=True,
    )

    button2_text = models.CharField(
        max_length=100,
        blank=True,
    )

    button2_url = models.CharField(
        max_length=255,
        blank=True,
    )

    image = models.ImageField(
        upload_to="hero_sliders/",
    )

    mobile_image = models.ImageField(
        upload_to="hero_sliders/mobile/",
        blank=True,
        null=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "Hero Slider"
        verbose_name_plural = "Hero Sliders"

    def __str__(self):
        return self.title