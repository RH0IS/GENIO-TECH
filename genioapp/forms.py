# pylint: disable=unused-wildcard-import
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Student, IntructorAvailability, CourseLevels, Course, CourseSession, InstructorProfile

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
        
class CourseSessionForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True, label='Course Title')
    course_level = forms.ModelChoiceField(queryset=CourseLevels.objects.none(), required=True, label='Course Level')
    instructor = forms.ModelChoiceField(queryset=InstructorProfile.objects.none(), required=True, label='Instructor')

    class Meta:
        model = CourseSession
        fields = ['course', 'course_level', 'instructor', 'session', 'start_datetime', 'end_datetime']

    def __init__(self, *args, **kwargs):
        super(CourseSessionForm, self).__init__(*args, **kwargs)
        self.fields['course_level'].queryset = CourseLevels.objects.none()
        self.fields['instructor'].queryset = InstructorProfile.objects.none()

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['course_level'].queryset = CourseLevels.objects.filter(course_id=course_id)
                self.fields['instructor'].queryset = InstructorProfile.objects.filter(course=Course.objects.get(id=course_id))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['course_level'].queryset = self.instance.course_level.course.course_levels_set
            self.fields['instructor'].queryset = self.instance.instructor.course.instructor_set

    widgets = {
        'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }

class CheckInstructorAvailability(forms.ModelForm):
    instructor = forms.ModelChoiceField(queryset=InstructorProfile.objects.all(), required=True, label='Instructor')
    class Meta:
        model = InstructorProfile
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CheckInstructorAvailability, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'