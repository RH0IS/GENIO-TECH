from decimal import Decimal
from django.db import models
from django.utils import timezone
import random

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    name = models.CharField(max_length=200, default='user')
    uid = models.CharField(max_length=1000, default='0')
    room_name = models.CharField(max_length=200, default='classroom')
    user_role = models.CharField(max_length=200, default='Student', null=True)
    insession = models.BooleanField(default=False)
    def __str__(self):
        return self.name+" "+self.room_name

class InstructorProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='first_name', null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, unique=True, default=None, null=True)
    bio = models.TextField(null=True)
    language = models.CharField(max_length=100, default="none", null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, null=True)
    start_date = models.TextField(null=True)
    end_date = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    interested = models.PositiveIntegerField(default=0,null=True)
    AGE_RANGE_CHOICES = [
        ('(7-11)', '(7-11)'),
        ('(12-14)', '(12-14)'),
        ('(15-17)', '(15-17)'),
        ('(17+)', '(17+)'),
    ]
    age_range = models.CharField(max_length=10, choices=AGE_RANGE_CHOICES, default='1')

    def __str__(self):
        return self.title


class CourseLevels(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, default=25)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True,default="w@example.com")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    # student = models.OneToOneField(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, default="w@example.com")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class IntructorAvailability(models.Model):
     instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, null=True)
     day = models.DateField(default=timezone.now)
     start_time=models.TimeField(default='08:00')
     end_time=models.TimeField(default='09:00')
     available = models.BooleanField(default=False)
     def __str__(self):
        return f"{self.instructor.first_name} {self.instructor.last_name}"


class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status = models.IntegerField(
        choices=((0, "Order Confirmed"), (1, "Order Cancelled")), default=1
    )
    order_date = models.DateField()
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    levels = models.PositiveIntegerField()

    def discount(self):
        discount_amount = Decimal(0.10) * self.course.price
        self.order_price = self.course.price - discount_amount

    def __str__(self):
        return f"Order for {self.course} by {self.student}"
    
class CourseSession(models.Model):
    course_level = models.ForeignKey(CourseLevels, on_delete=models.CASCADE)
    YOUR_CHOICES = [
        (1, 'Session 1'),
        (2, 'Session 2'),
        (3, 'Session 3'),
        (4, 'Session 4'),
    ]
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True)
    session = models.IntegerField(choices=YOUR_CHOICES)
    start_datetime = models.CharField(max_length=50, blank=True)#models.DateTimeField(default = timezone.now)
    end_datetime = models.CharField(max_length=50, blank=True)#models.DateTimeField(default = timezone.now)
    def __str__(self):
        return self.course_level.course.title+" "+self.course_level.name+" Session-"+str(self.session)

class StudentOrder(models.Model):
    COMPLETION_CHOICES = [
        (0, 'On-going'),
        (1, 'Completed'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course_level = models.ForeignKey(CourseLevels, on_delete=models.CASCADE)
    completion_status = models.CharField(max_length=10, choices=COMPLETION_CHOICES, default=0)
    payment_id=models.CharField(max_length=100, null=True, default="id")
    class Meta:
        unique_together = ('student', 'course_level')

    def __str__(self):
        return f"{self.student.user.username} - {self.course_level} - {self.completion_status}"


