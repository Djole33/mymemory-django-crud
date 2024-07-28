from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('words-list/', views.words_list, name="words-list"),
    path('recall/', views.recall, name="recall"),
]
