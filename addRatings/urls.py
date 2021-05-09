from django.urls import path
from . import views

urlpatterns = [
    path('add_r/', views.star_rating_form, name="add_r"),
    path('confirm_r/', views.confirm_star_rating, name="confirm_r"),
    path('page/', views.page, name="page"),
]
