from decimal import Decimal
from django.db import models

# Create your models here.
class Student(models.Model):
    STUDENT_STATUS_CHOICES = [
        ('ER', 'Enrolled'),
        ('SP', 'Suspended'),
        ('GD', 'Graduated')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES, default='ER')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class InstructorProfile(models.Model):
    
    user= models.OneToOneField('auth.User',on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)  # Optional field
    email = models.EmailField(unique=True)
    # Additional fields
    field2 = models.CharField(max_length=50, blank=True)  # Optional field
    def __str__(self):
        return self.name 
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.SET_NULL, null=True, related_name='courses_teaching')
    image = models.ImageField(upload_to='images/',default='default_image.jpg')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    interested = models.PositiveIntegerField(default=0)
    video = models.FileField(upload_to='videos/',default='default_image.jpg')
    # level choices in Course

    def __str__(self):
        return self.title

class CourseLevels(models.Model):
    name= models.CharField(max_length=100)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    description=models.CharField(max_length=100)
    def __str__(self):
        return self.name  
    

    

class Instructor(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True, default=None)
    bio = models.TextField()
    language = models.CharField(max_length=100, default='none')
    image = models.ImageField(upload_to='images/',default='default_image.jpg')
    students = models.ManyToManyField(Student, blank=True, related_name='instructors')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status= models.IntegerField(
        choices=((0, 'Order Confirmed'), (1, 'Order Cancelled')),
        default=1
    )
    order_date = models.DateField()
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    levels = models.PositiveIntegerField()

    def discount(self):
        discount_amount = Decimal(0.10)* self.course.price
        self.order_price = self.course.price - discount_amount

    def __str__(self):
        return f"Order for {self.course} by {self.student}"