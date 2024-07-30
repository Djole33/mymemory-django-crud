from django.db import models
from django.urls import reverse

# Create your models here.

class Word(models.Model):
    word = models.CharField(max_length=100)
    
    def __str__(self):
	    return self.word

class Guess(models.Model):
    guess = models.CharField(max_length=100)
    
    def __str__(self):
	    return self.guess
    
    def get_absolute_url(self):
        return reverse('recall')
    
class Level(models.Model):
    level = models.IntegerField()

    def __str__(self):
        return str(self.level)
    