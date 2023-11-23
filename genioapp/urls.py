from django.urls import path
from . import views

app_name = "genioapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name = 'courses'),
    path('category/<int:category_no>/', views.course_by_id, name='category_detail'),
    path('instructorsignup/',views.instructorsignup, name='instructorsignup'),
    path('courseregistration/',views.courseregistration, name='courseregistration'),
    path('login/',views.login, name='login'),
    path('addcourselevels/',views.addcourselevels, name='addcourselevels'),
    path('viewCourses/',views.viewCourses, name='viewCourses'),
    path('login/redirect/',views.instructorsignup, name='login/redirect/'),
    path('logout/', views.custom_logout, name='logout'),
    path('user_profile/', views.user_profile, name = 'user_profile'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('student_form/', views.student_form, name='student_form'),
    path('admin_students_list/', views.admin_students_list, name='admin_students_list'),
    path('create_credentials/<int:student_id>/', views.create_credentials, name='create_credentials'),
    path('viewinsavailability/',views.view_ins_availability, name='viewinsavailability'),
    path('create_course_session/', views.create_course_session, name='create_course_session'),
    path('get_course_levels/', views.get_course_levels, name='get_course_levels'),
    path('get_instructor/', views.get_instructor, name='get_instructor'),
    path('add_availability/', views.add_availability, name='add_availability'),
    path('createorder/<int:course_level_id>',views.createorder,name='createorder'),

]
