
from django.shortcuts import render
from .models import Category, Course, Student, InstructorProfile
from django.shortcuts import get_object_or_404
from .forms import InstructorSignUpForm, CourseForm
from django.contrib.auth import authenticate, login

# Create your views here.
def courseregistration(request):
    form= CourseForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        form = CourseForm()
    
    return render(request, 'genioapp/courseregistrationpage.html', {'form': form})

def instructorsignup(request):
    if request.method == 'POST':
        form = InstructorSignUpForm(request.POST)
        if form.is_valid():
            # Save only required fields
            user=form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            instructor= InstructorProfile(
                user=user,
                name=name,
                email=email
            )
            instructor.save()
            return render(request,'genioapp/index.html')  # Redirect to a success page
    else:
        form = InstructorSignUpForm()
    
    return render(request, 'genioapp/InstructorSignup.html', {'form': form})

def index(request):
    # Retrieve the list of categories from the database and order them by ID
    category_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'genioapp/index.html', {'category_list': category_list})

def about(request):

    heading = 'This is a Distance Education Website! Search our Categories to find all available Courses.'
    return render(request, 'genioapp/about.html', {'heading': heading})

def detail(request, category_no):
    category = get_object_or_404(Category,id=category_no)
    courses = Course.objects.filter(categories= category)

    return render(request, 'genioapp/detail.html',
                  {'courses': courses,'category': category, 'student':Student})
def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'genioapp/courses.html',
                  {'courlist': courlist})
