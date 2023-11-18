from django.contrib import admin
from .models import Category,Course,Student,Instructor,Order,InstructorProfile

# Register your models here.

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Order)
admin.site.register(InstructorProfile)
