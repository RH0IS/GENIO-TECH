# pylint: disable=unused-wildcard-import
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Student

from genioapp.models import Course, CourseLevels

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CourseLevelForm(forms.ModelForm):
    class Meta:
        model=CourseLevels
        fields='__all__'

class InstructorSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    name=forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'age', 'gender', 'phone', 'country' ]


class StudentCred(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

