from django.contrib import admin

from .models import Category,Course,Student,Instructor,Order,InstructorProfile, StudentProfile, CourseLevels, IntructorAvailability, CourseSession


# Register your models here.

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Order)
admin.site.register(InstructorProfile)
admin.site.register(StudentProfile)
admin.site.register(CourseLevels)
admin.site.register(IntructorAvailability)
admin.site.register(CourseSession)

