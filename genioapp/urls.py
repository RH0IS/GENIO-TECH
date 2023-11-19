from django.urls import path
from . import views

app_name = 'genioapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name = 'courses'),
    path('category/<int:category_no>/', views.detail, name='category_detail'),
    path('instructorsignup/',views.instructorsignup, name='instructorsignup'),
    path('courseregistration/',views.courseregistration, name='courseregistration'),
    path('login/',views.ins_login, name='ins_login'),
    path('addcourselevels/',views.addcourselevels, name='addcourselevels'),
    path('viewCourses/',views.viewCourses, name='viewCourses'),
    path('login/redirect/',views.instructorsignup, name='login/redirect/'),
    path('logout/', views.custom_logout, name='logout'),
    path('instructor_profile/', views.instructor_profile, name = 'instructor_profile'),
    path('student_form/', views.student_form, name='student_form'),
    path('admin_students_list/', views.admin_students_list, name='admin_students_list'),
    path('create_credentials/<int:student_id>/', views.create_credentials, name='create_credentials'),


]
