from django.db import models
from .utils import ImageCompressionClass

# Create your models here.
class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs) 
        for field in self._meta.get_fields():
            if isinstance(field, models.ImageField):
                image_field = getattr(self, field.name)
                if image_field and image_field.path:
                    try:
                        ImageCompressionClass.reduce_image_size(image_field.path)
                    except FileNotFoundError:
                        print(f"File {image_field.path} not found. Skipping resize.")

    class Meta:
        abstract = True
        ordering = ["id"]