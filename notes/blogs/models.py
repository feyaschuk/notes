from django.db import models
import datetime as dt

from django.contrib.auth.models import AbstractUser

USER_CITY_CHOICES =['Moscow', 'SPB', 'Khabarovsk']

class User(AbstractUser):
    city = models.CharField(
        max_length=150,
        choices=USER_CITY_CHOICES,        
        verbose_name="Город пользователя",
    )    

    def __str__(self):
        return self.username

class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = (models.ForeignKey(User, on_delete=models.CASCADE,
              related_name="posts"))    
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ["-pub_date"]