from django.urls import path
from . import views

urlpatterns = [
    path('view_r/', views.view_star_rating, name="viewRatings"),
]
