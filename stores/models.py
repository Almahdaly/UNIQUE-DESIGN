from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Store(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='store')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='store_images/', blank=True, null=True)
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    cover = models.ImageField(upload_to='store_covers/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, blank=True, default='#2563eb')  # لون افتراضي أزرق
    slug = models.SlugField(unique=True, blank=True, max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
