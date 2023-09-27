from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
class ServicesList(models.Model):
    STATUS_CHOICES = (
        ('Sale Planning', 'Sale Planning'),
        ('SEO', 'SEO'),
        ('Web-Site Design', 'Web-Site Design'),
    )
    service_name=models.CharField(max_length=20,
        choices=STATUS_CHOICES,
        default='SEO') # Optional: Set a default value
    description=models.TextField(max_length=250,null=False,blank=False)
    picture= ProcessedImageField(upload_to='albums', processors=[ResizeToFit(300)], format='JPEG',
                                options={'quality': 90})

