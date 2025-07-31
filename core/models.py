from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')  # Stores uploaded file in MEDIA_ROOT/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically adds upload timestamp
    labels = models.TextField(blank=True, null=True)  # Stores comma-separated labels from Google Vision
    dominant_colors = models.JSONField(blank=True, null=True)  # Stores RGB values as JSON (list of dicts)

    def __str__(self):
        return f"Image {self.pk} uploaded at {self.uploaded_at}"
