
from django.shortcuts import render
from .models import Category, Course, Student, Instructor
from django.shortcuts import get_object_or_404

# Create your views here.

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
