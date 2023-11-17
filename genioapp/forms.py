# pylint: disable=unused-wildcard-import
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from genioapp.models import Course

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

