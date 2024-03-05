from django.contrib import admin

from .models import ClassRoom,Category,Course,Student,Order,InstructorProfile, StudentProfile, CourseLevels, IntructorAvailability, CourseSession, StudentOrder


# Register your models here.

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Order)
admin.site.register(InstructorProfile)
admin.site.register(StudentProfile)
admin.site.register(CourseLevels)
admin.site.register(IntructorAvailability)
admin.site.register(CourseSession)
admin.site.register(StudentOrder)
admin.site.register(ClassRoom)


