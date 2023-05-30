from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Documents(models.Model):
    image = models.ImageField()
    result_image = models.ImageField()
    image_text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    
    

    