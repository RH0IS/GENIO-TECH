from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from .models import Category, Course, Student, InstructorProfile, StudentProfile, IntructorAvailability, CourseLevels, CourseSession, StudentOrder
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
import re

from .forms import InstructorSignUpForm, CourseForm, LoginForm, StudentForm, StudentCred, CourseLevelForm, InstructorSelectionForm, InstructorAvailabilityForm, CourseSessionForm, CheckInstructorAvailability, GetSessionForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required


def about(request):
    return render(request, "genioapp/about.html")


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_levels = CourseLevels.objects.filter(course=course)
    instructor = course.instructor
    instructor_profile = InstructorProfile.objects.get(id=instructor.id)

    if request.method == 'POST':
        form = GetSessionForm(course_id, request.POST)
        print('Entering form validation')
        if form.is_valid():
            print('Validated form')
            course_level = form.cleaned_data.get('course_level')
            student = StudentProfile.objects.get(user=request.user)
            course_sessions = CourseSession.objects.filter(course_level=course_level)
            age_range = course.age_range
            level_str = re.search(r'\d+', course_level.name)
            if is_age_appropriate(student.age, age_range):
                if level_str:
                    level = int(level_str.group())
                    level = level - 1
                    if level != 0:
                        prev_level = f"L{level}"

                        # student = StudentProfile.objects.get(user=request.user)
                        prev_level_order = StudentOrder.objects.filter(student=student,
                                                                       course_level__name=prev_level).first()

                        if prev_level_order and prev_level_order.completion_status == 'Completed':
                            print(f"Student can enroll in {course_level}")
                        else:
                            # Send a message that the student needs to complete the previous level
                            message = f"You need to complete {prev_level} before enrolling in {course_level}"
                            print(message)
                            course_sessions = CourseSession.objects.filter(course_level=course_level)
                            return render(request, "genioapp/course_detail.html", {
                                "course": course,
                                "instructor_profile": instructor_profile,
                                "course_levels": course_levels,
                                "course_sessions": course_sessions,
                                "form": form,
                                "message": message
                            })
            else:
                # Send a message that the student's age is not appropriate for the course
                message = f"Sorry, this course is not suitable for your age."
                return render(request, "genioapp/course_detail.html", {
                    "course": course,
                    "instructor_profile": instructor_profile,
                    "course_levels": course_levels,
                    "course_sessions": course_sessions,
                    "form": form,
                    "message": message
                })
            print(course_level)

            return render(request, "genioapp/course_detail.html", {
                "course": course,
                "instructor_profile": instructor_profile,
                "course_levels": course_levels,
                "course_sessions": course_sessions,
                "form": form,
            })
    else:
        form = GetSessionForm(course_id)

    return render(request, "genioapp/course_detail.html", {
        "course": course,
        "instructor_profile": instructor_profile,
        "course_levels": course_levels,
        "form": form,
    })

def is_age_appropriate(student_age, age_range):
    lower_bound, upper_bound = map(int, re.findall(r'\d+', age_range))
    print("LB:",lower_bound)
    print("UB",upper_bound)
    print("Age:", student_age)
    return lower_bound <= student_age <= upper_bound

def courseregistration(request):

    form = CourseForm(request.POST)
    #print(form.cleaned_data.get('title'))
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        form = CourseForm()
    return render(request, "genioapp/courseregistrationpage.html", {"form": form})


def custom_login(request):
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
                response = redirect("/user_profile/")
                return response  # Redirect to the desired URL after successful login
    else:
        form = LoginForm()

    return render(request, "genioapp/login.html", {"form": form})


def is_instructor(user):
    val = user.groups.filter(name="Instructor").exists()
    print(val)
    return val


def is_student(user):
    val = user.groups.filter(name="Students").exists()
    print(val)
    return val


def viewCourses(request):
    if is_student(request.user):
        courses = Course.objects.all()
        courses_with_levels = []
        for course in courses:
            levels = course.courselevels_set.all()
            courses_with_levels.append({"course": course, "levels": levels})
        return render(
            request,
            "genioapp/courses.html",
            {"courses_with_levels": courses_with_levels},
        )
    else:
        return render(request, "genioapp/user_profile.html")

def create_course_session(request):
    if request.method == 'POST':
        form = CourseSessionForm(request.POST)
        form1 = CheckInstructorAvailability(request.POST or None)
        if form.is_valid():
            form.save()  # You might want to customize this based on your logic
            return redirect('/create_course_session/')



        if form1.is_valid():
            instructor_profile = form1.cleaned_data['instructor']
            # first_name = form1.cleaned_data['first_name']
            # last_name = form1.cleaned_data['last_name']
            # first_name, last_name = instructor_name.split(' ', 1) if ' ' in instructor_name else (instructor_name, '')
            # print(instructor_name)
            availability = IntructorAvailability.objects.filter(
                instructor=instructor_profile
            ).values('id', 'day', 'start_time', 'end_time', 'available')
            availability_data = [
                {'day': av['day'], 'start_time': av['start_time'], 'end_time': av['end_time'],
                 'available': av['available']} for av in availability
            ]
            # availability = IntructorAvailability.objects.filter(
            #     instructor=InstructorProfile.objects.get(instructorprofile = instruvtot)).values('id', 'day', 'start_time',
            #                                                                                   'end_time', 'available')
            # print(availability)
            # availability_data = [
            #     {'day': av['day'], 'start_time': av['start_time'], 'end_time': av['end_time'], 'available': av['available']} for av in availability
            # ]
            return render(request, 'genioapp/sessions.html', {'form': form, 'form1': form1, 'availability_data': availability_data})
        else:
            return render(request, 'genioapp/sessions.html', {'form': form,'form1': form1})
    else:
        form = CourseSessionForm()
        form1 = CheckInstructorAvailability(request.POST or None)

    return render(request, 'genioapp/sessions.html', {'form': form, 'form1': form1})

def get_course_levels(request):
    course_id = request.GET.get('course_id')
    levels = CourseLevels.objects.filter(course_id=course_id).values('id', 'name')
    return JsonResponse(list(levels), safe=False)

def get_instructor(request):
    course_id = request.GET.get('course_id')
    instructor = InstructorProfile.objects.filter(course=Course.objects.get(id=course_id)).values('first_name','last_name')
    print(instructor)
    #prinr(instructor.first_name)
    return JsonResponse(list(instructor), safe=False)

def init_ins_availability(instructor):
    insa= IntructorAvailability(instructor=instructor)
    insa.save()

def view_ins_availability(request):
    user = request.user
    try:
        instructor_profile = InstructorProfile.objects.get(user=user)
        #instructor_profile_id = instructor_profile.pk
        InsFormSet = forms.inlineformset_factory(InstructorProfile, IntructorAvailability, fields="__all__",  extra=0)
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
    
def add_availability(request):
    instructor_profile = InstructorProfile.objects.get(user=request.user)
    insa= IntructorAvailability(
            instructor=instructor_profile,
            start_time='15:00',
            end_time='16:00'
        )
    insa.save()
    return redirect('/viewinsavailability/')


def addcourselevels(request):
    form = CourseLevelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/")
    else:
        form = CourseLevelForm()


    return render(request, "genioapp/courseregistrationpage.html", {"form": form})


@login_required(login_url="/login")
def instructorsignup(request):
    if request.method == "POST":
        form = InstructorSignUpForm(request.POST,
                                    request.FILES)  # Make sure to include request.FILES for handling uploaded files
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            bio = form.cleaned_data.get("bio")
            language = form.cleaned_data.get("language")
            image = form.cleaned_data.get("image")

            try:
                validate_image_file(image)
            except ValidationError as e:
                form.add_error('image', e)
                return render(request, "genioapp/signup.html", {"form": form})

            instructor = InstructorProfile(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                bio=bio,
                language=language,
                image=image
            )
            instructor.save()

            instructor_group = Group.objects.get(name="Instructor")
            user.groups.add(instructor_group)

            init_ins_availability(instructor)

            return render(request, "genioapp/index.html")
    else:
        form = InstructorSignUpForm()

    return render(request, "genioapp/InstructorSignup.html", {"form": form})


def validate_image_file(image):
    if image:
        if not image.content_type.startswith('image'):
            raise ValidationError('File is not an image.')
        # Add more checks as needed (e.g., file size, dimensions, etc.)


def index(request):
    # Retrieve the list of categories from the database and order them by ID
    courses_with_levels = []
    # if is_student(request.user):
    courses = Course.objects.all()
    # courses_with_levels = []
    for course in courses:
        levels = course.courselevels_set.all()
        courses_with_levels.append({"course": course, "levels": levels})
    return render(
        request,
        "genioapp/index.html",
        {"courses_with_levels": courses_with_levels}
    )


# @login_required
# def about(request):
#     heading = "This is a Distance Education Website! Search our Categories to find all available Courses."
#     return render(request, "genioapp/about.html", {"heading": heading})


def course_by_id(request, course_id):
    
    courses = Course.objects.get(id=course_id)

    return render(
        request,
        "genioapp/course_detail.html",
        {"course": courses},
    )


def courses(request):
    courlist = Course.objects.all().order_by("id")
    return render(request, "genioapp/courses.html", {"courlist": courlist})


def custom_logout(request):
    logout(request)
    return redirect("/login/")


@login_required(login_url="/login/")
def user_profile(request):
    return render(request, "genioapp/user_profile.html")


def student_form(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin_students_list/")  # Redirect to the admin view
    else:
        form = StudentForm()

    return render(request, "genioapp/student_form.html", {"form": form})


def admin_students_list(request):
    students = Student.objects.all()
    return render(request, "genioapp/admin_students_list.html", {"students": students})


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
            studentProfile = StudentProfile(
                user=user,
                name=name,
                email=email,
                age=age,
                gender=gender,
                phone=phone,
                country=country,
            )
            studentProfile.save()
            student.delete()

            student_group = Group.objects.get(name ="Students")
            user.groups.add(student_group)
            return redirect("/admin_students_list/")
    else:
        form = StudentCred(request.POST)

    return render(
        request,
        "genioapp/create_credentials.html",
        {"form": form, "student_id": student_id},
    )  # Redirect back to the admin view

#def get_instructor_availability(request):

def createorder(request, course_level_id):
    courselevels = CourseLevels.objects.get(id=course_level_id)
    student = StudentProfile.objects.get(user=request.user)
    course = courselevels.course
    # Check if a StudentOrder already exists for the given course_level and student
    existing_order = StudentOrder.objects.filter(course_level=courselevels, student=student).first()

    student_already_enrolled = existing_order is not None

    if request.method == "POST" and not student_already_enrolled:
        # If no order exists, create a new StudentOrder
        order = StudentOrder(student=student, course_level=courselevels)
        order.save()
        return redirect("/")

    return render(request, 'genioapp/order.html', {'course': course, 'courselevels': courselevels,
                                                   'student_already_enrolled': student_already_enrolled})

def user_profile(request):
    user = request.user
    if is_student(user):
        student = StudentProfile.objects.get(user=user)
        student_orders = StudentOrder.objects.filter(student=student)

        stu_course_levels = []
        for student_order in student_orders:
            course_level = student_order.course_level
            course = course_level.course
            sessions = CourseSession.objects.filter(course_level=course_level)

            stu_course_lvl = {
                "course_title": course.title,
                "course_level": course_level.name,
                "sessions": sessions,
            }

            stu_course_levels.append(stu_course_lvl)

        profile_data = {
            'username': user.username,
            'group': 'Student',
            'name' : student.name,
            'age' : student.age,
            'email': student.email,
            'gender': student.gender,
            'country': student.country,
            'phone': student.phone,
            'stu_course_levels': stu_course_levels
        }
    elif is_instructor(user):
        instructor_profile = InstructorProfile.objects.get(user=user)

        # Get courses taught by the instructor
        courses_taught = Course.objects.filter(instructor=instructor_profile)

        # Get course levels for each course
        instructor_course_levels = []
        for course in courses_taught:
            levels = CourseLevels.objects.filter(course=course)
            instructor_course_levels.append({'course': course, 'levels': levels})

        # Get session details for each course level
        session_details = []
        for course_level in CourseLevels.objects.filter(course__in=courses_taught):
            sessions = CourseSession.objects.filter(course_level=course_level)
            session_details.append({'course_level': course_level, 'sessions': sessions})

        profile_data = {
            'username': user.username,
            'group': 'Instructor',
            'name': instructor_profile.first_name + ' ' + instructor_profile.last_name,
            'email': instructor_profile.email,
            'bio': instructor_profile.bio,
            'language': instructor_profile.language,
            'image': instructor_profile.image.url,
            'courses_taught': instructor_course_levels,
            'session_details': session_details,
            # Add other instructor-specific data
        }
    else:
        profile_data = {
            'username': user.username,
            'group': 'Other',
        }

    return render(request, "genioapp/user_profile.html", {"profile_data": profile_data})







