from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/<int:pk>/', views.results, name='results'),
    path('generate-poster/', views.poster_generator, name='generate_poster'),
]
