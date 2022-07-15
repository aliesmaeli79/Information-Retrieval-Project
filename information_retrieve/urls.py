from django.urls import path
from . import views
from .forms import KeywordSearchForm


app_name = 'information_retrieve'
urlpatterns = [
    path('', views.ReadDocument.as_view()),
    path('search/', views.FormView.as_view(),name="search"),
    path('upload/', views.FormTwo.as_view(),name="upload"),
]
