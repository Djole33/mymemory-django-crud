from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('words-list/', WordsView.as_view(), name="words-list"),
    path('recall/', views.guess_view, name="recall"),
    path('delete/', views.delete_guess, name='delete-guess'),
    path('results/', views.results, name='results'),
]
