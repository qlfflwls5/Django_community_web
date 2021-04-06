from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    image = ProcessedImageField(
        upload_to='profile_images/%Y/%m/%d/',
        processors=[ResizeToFill(20,20)],
        format='JPEG',
        options={'quality': 100}
        )