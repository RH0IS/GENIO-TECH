# pylint: disable=unused-wildcard-import
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Student, IntructorAvailability, CourseLevels, Course, CourseSession, InstructorProfile, ClassRoom



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
    #username = forms.CharField(max_length=100)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    bio = forms.CharField()
    language = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'language','password1', 'password2']
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class StudentForm(UserCreationForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = forms.CharField()
    email = forms.EmailField()
    age = forms.IntegerField()
    phone = forms.CharField()
    country = forms.CharField()

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ['username','password1', 'password2', 'name', 'age', 'email', 'phone','gender', 'country']



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
        fields = ['id','first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CheckInstructorAvailability, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

class GetSessionForm(forms.ModelForm):
    course_level = forms.ModelChoiceField(queryset=CourseLevels.objects.all(), label='Course Level')

    class Meta:
        model=CourseLevels
        fields=['course_level']
    def __init__(self, course_id, *args, **kwargs):
        super(GetSessionForm, self).__init__(*args, **kwargs)
        course=Course.objects.get(id=course_id)
        #print('Course:',course)
        #course=CourseLevels.objects.get(course_id=course_id)

        self.fields['course_level'].queryset = CourseLevels.objects.filter(course=course)