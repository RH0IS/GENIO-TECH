from django.shortcuts import render, redirect
from .models import Category, Course, Student, InstructorProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import InstructorSignUpForm, CourseForm, LoginForm, CourseLevelForm
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
def courseregistration(request):
    form = CourseForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        form = CourseForm()

    return render(request, "genioapp/courseregistrationpage.html", {"form": form})


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
                response = redirect("/instructor_profile/")
                return response  # Redirect to the desired URL after successful login

    else:
        form = LoginForm()

    return render(request, "genioapp/login.html", {"form": form})


@login_required(login_url="/login")
def viewCourses(request):
    courses = Course.objects.all()
    courses_with_levels = []
    for course in courses:
        levels = course.courselevels_set.all()
        courses_with_levels.append({"course": course, "levels": levels})

    print(courses_with_levels)
    return render(
        request, "genioapp/courses.html", {"courses_with_levels": courses_with_levels}
    )


def addcourselevels(request):
    form = CourseLevelForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        form = CourseLevelForm()

    return render(request, "genioapp/courseregistrationpage.html", {"form": form})


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
            return render(request, "genioapp/index.html")  # Redirect to a success page
    else:
        form = InstructorSignUpForm()

    return render(request, "genioapp/InstructorSignup.html", {"form": form})


def index(request):
    # Retrieve the list of categories from the database and order them by ID
    # category_list = Category.objects.all().order_by('id')[:10]
    # return render(request, 'genioapp/index0.html', {'category_list': category_list})
    return render(request, "genioapp/index.html")


@login_required
def about(request):
    heading = "This is a Distance Education Website! Search our Categories to find all available Courses."
    return render(request, "genioapp/about.html", {"heading": heading})


def detail(request, category_no):
    category = get_object_or_404(Category, id=category_no)
    courses = Course.objects.filter(categories=category)

    return render(
        request,
        "genioapp/detail.html",
        {"courses": courses, "category": category, "student": Student},
    )


def courses(request):
    courlist = Course.objects.all().order_by("id")
    return render(request, "genioapp/courses.html", {"courlist": courlist})


def custom_logout(request):
    logout(request)
    return redirect("/login/")


@login_required(login_url="/login/")
def instructor_profile(request):
    return render(request, "genioapp/instructor_profile.html")
