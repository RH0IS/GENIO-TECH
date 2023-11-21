from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from .models import Category, Course, Student, InstructorProfile, StudentProfile, IntructorAvailability

from django.shortcuts import get_object_or_404
from .forms import InstructorSignUpForm, CourseForm, LoginForm, StudentForm, StudentCred, CourseLevelForm, InstructorSelectionForm, InstructorAvailabilityForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'genioapp/course_detail.html', {'course': course})



# Create your views here.
def courseregistration(request):
    form = CourseForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        form = CourseForm()

    return render(request, 'genioapp/courseregistrationpage.html', {'form': form})


def ins_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or any desired page after login
                # Example: return redirect('home')
                print(username)
                print(password)

                response = redirect('/instructor_profile/')
                return response  # Redirect to the desired URL after successful login
    else:
        form = LoginForm()

    return render(request, "genioapp/login.html", {"form": form})



# def viewCourses(request):
#     courses=Course.objects.all()
#     courselevels=CourseLevels.objects.get(course=co)
    
#     return render (request,'genioapp/courses.html', {'courses': courses})

def is_instructor(user):
    val=user.groups.filter(name='Instructor').exists()
    print(val)
    return val

def is_student(user):
    val=user.groups.filter(name='Students').exists()
    print(val)
    return val

def viewCourses(request):
    if is_student(request.user):
        courses = Course.objects.all()
        courses_with_levels = []
        for course in courses:
            levels = course.courselevels_set.all()
            courses_with_levels.append({'course': course, 'levels': levels})
        return render(request, 'genioapp/courses.html', {'courses_with_levels': courses_with_levels})
    else:
        return render(request, 'genioapp/instructor_profile.html')

def init_ins_availability(instructor):
    i=1
    while i<=20:
        insa= IntructorAvailability(
            instructor=instructor
        )
        insa.save()
        i+=1

def view_ins_availability(request):

    user = request.user
    try:
        instructor_profile = InstructorProfile.objects.get(user=user)
        #instructor_profile_id = instructor_profile.pk
        InsFormSet = forms.inlineformset_factory(InstructorProfile, IntructorAvailability, fields="__all__")
        if request.method == "POST":
            formset = InsFormSet(request.POST, request.FILES, instance=instructor_profile)
            if formset.is_valid():
                formset.save()
                return redirect('/viewinsavailability/')
        else:
            formset = InsFormSet(instance=instructor_profile)
            return render(request, 'genioapp/insavailability.html', {
                                                             'form':formset})
    except InstructorProfile.DoesNotExist:
        #instructor_profile_id = None
        return render(request, 'genioapp/index.html')
    



def addcourselevels(request):
    form= CourseLevelForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        form = CourseLevelForm()
    
    return render(request, 'genioapp/courseregistrationpage.html', {'form': form})

@login_required(login_url="/login")
def instructorsignup(request):
    if request.method == "POST":
        form = InstructorSignUpForm(request.POST)
        if form.is_valid():
            # Save only required fields
            user = form.save()
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            instructor = InstructorProfile(user=user, name=name, email=email)
            instructor.save()
            instructor_group = Group.objects.get(name="Instructor")
            user.groups.add(instructor_group)
            init_ins_availability(instructor)
            
            return render(request, "genioapp/index.html")  # Redirect to a success page
    else:
        form = InstructorSignUpForm()

    return render(request, 'genioapp/InstructorSignup.html', {'form': form})



def index(request):
    # Retrieve the list of categories from the database and order them by ID

    # category_list = Category.objects.all().order_by('id')[:10]
    # return render(request, 'genioapp/index0.html', {'category_list': category_list})
    return render(request, "genioapp/index.html")


@login_required
def about(request):
    heading = 'This is a Distance Education Website! Search our Categories to find all available Courses.'
    return render(request, 'genioapp/about.html', {'heading': heading})


def course_by_id(request, course_id):
    
    courses = Course.objects.get(id=course_id)

    return render(
        request,
        "genioapp/course_detail.html",
        {"course": courses},
    )


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'genioapp/courses.html',
                  {'courlist': courlist})

def custom_logout(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url = '/login/')
def instructor_profile(request):
    return render(request, 'genioapp/instructor_profile.html')

def student_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin_students_list/')  # Redirect to the admin view
    else:
        form = StudentForm()

    return render(request, 'genioapp/student_form.html', {'form': form})

def admin_students_list(request):
    students = Student.objects.all()
    return render(request, 'genioapp/admin_students_list.html', {'students': students})

def create_credentials(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    name = student.name
    email = student.email
    age = student.age
    gender = student.gender
    phone = student.phone
    country = student.country

    if request.method == "POST":
        form = StudentCred(request.POST)
        if form.is_valid():
            user = form.save()
            studentProfile = StudentProfile(user=user, name=name, email=email,age = age, gender = gender, phone = phone, country =country)
            studentProfile.save()
            student.delete()
            student_group = Group.objects.get(name ="Students")
            user.groups.add(student_group)
            return redirect('/admin_students_list/')
    else:
        form = StudentCred(request.POST)

    return render(request,'genioapp/create_credentials.html',{'form': form, 'student_id': student_id})  # Redirect back to the admin view

