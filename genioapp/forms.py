# pylint: disable=unused-wildcard-import
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Student, IntructorAvailability

from genioapp.models import Course, CourseLevels

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

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
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-input'}))
    class Meta:
        model = Student
        fields = ['name', 'email', 'age', 'gender', 'phone', 'country']



    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            # self.fields[field_name].label_classes = 'custom-label-class'

class StudentCred(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class InstructorSelectionForm(forms.ModelForm):
    class Meta:
        model = IntructorAvailability
        fields = ['instructor']
        
class InstructorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = IntructorAvailability
        fields = ['day', 'start_time', 'end_time', 'available']