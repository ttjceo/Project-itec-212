from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UploadedFile(models.Model):
   user = models.ForeignKey(User,
        on_delete=models.CASCADE
                             )
   file = models.FileField(upload_to='uploaded_files/')
   uploaded_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return self.file.name

   class UserQQuery(models.Model):
       user = models.ForeignKey(
           User,
            on_delete=models.CASCADE
        )

question = models.TextField()
response = models.TextField()
created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return self.question[:50]