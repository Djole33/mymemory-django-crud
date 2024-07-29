from django.contrib import admin
from .models import Guess, Word

# Register your models here.

admin.site.register(Word)
admin.site.register(Guess)
