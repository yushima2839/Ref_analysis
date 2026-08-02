from django.urls import path
from . import views

urlpatterns = [
    path('matches/', views.match_list),
    path('search/', views.search_form, name='search_form'),
    path('result/', views.search_result, name='search_result')
]