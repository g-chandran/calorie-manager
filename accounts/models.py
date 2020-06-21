from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  name = models.OneToOneField(to=User, on_delete=models.CASCADE)
  age = models.IntegerField()
  gender = models.CharField(default='Male', max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])
  height = models.FloatField()
  weight = models.FloatField()
  typeSelection = [
      ('Very Light', 'Very Light'),
      ('Light', 'Light'),
      ('Moderate', 'Moderate'),
      ('Heavy', 'Heavy'),
      ('Very Heavy', 'Very Heavy'),
    ]
  type = models.CharField(default='Very Light', max_length=10, choices=typeSelection)
  calorie = models.FloatField(default=0)

  def __str__(self):
      return self.name.username
  
class Image(models.Model):
  image = models.ImageField(upload_to='images/')
