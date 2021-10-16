from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()



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