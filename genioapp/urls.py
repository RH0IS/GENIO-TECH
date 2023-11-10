from django.urls import path
from . import views

app_name = 'genioapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name = 'courses'),
    path('category/<int:category_no>/', views.detail, name='category_detail'),

]