from accounts.decorators import admin_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .decorators import *

User = get_user_model()

def login_page(request):

    # We do not redirect authenticated users on GET requests so that the login page is always accessible when opening the URL.

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        if not email or not password:
            messages.error(request, "Please fill all the required fields")
            return redirect('login_page')
        
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid login Credentials!")
            return redirect('login_page')
        else:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60*60*24*7)

            if user.role == "ADMIN" or user.is_superuser:
                redirect_url = reverse('admin_dashboard')
            elif user.role == "TEACHER":
                redirect_url = reverse('teacher_dashboard')
            else:
                redirect_url = reverse('login_page')

            welcome_msg = f"Welcome {user.full_name}. Redirecting to dashboard..."

            return render(request, 'auth/login_page.html', {
                'login_success': True,
                'redirect_url': redirect_url,
                'welcome_message': welcome_msg
            })

    return render(request, 'auth/login_page.html')


from django.http import JsonResponse

@admin_required
def create_admin(request):

    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permisson to access this page')
        return redirect("login_page")

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        department = request.POST.get("department")
        designation = request.POST.get("designation")
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if not all([ full_name, email, password, confirm_password ]): 
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["All compulsory fields are required."]})
            messages.error( request, "All compulsory fields are required." ) 
            return redirect("create_admin")

        if password != confirm_password: 
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Passwords do not match."]})
            messages.error( request, "Passwords do not match." ) 
            return redirect("create_admin")

        if User.objects.filter(email=email).exists():
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Email already exists"]})
            messages.error(request, "Email already exists")
            return redirect("create_admin")
        
        # Use email as the username
        username = email

        if User.objects.filter(username=username).exists():
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Username already exists"]})
            messages.error(request, "Username already exists")
            return redirect("create_admin")

        from django.db import transaction
        try:
            with transaction.atomic():
                # Create the admin user
                new_admin = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role='ADMIN',
                    full_name=full_name
                )
                new_admin.is_staff = True
                new_admin.save()

                # Create the admin profile
                from accounts.models import AdminProfile
                AdminProfile.objects.create(
                    user=new_admin,
                    department=department if department else None,
                    designation=designation if designation else None
                )
        except Exception as e:
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Database error: " + str(e)]})
            messages.error(request, "Database error: " + str(e))
            return redirect("create_admin")

        if is_ajax:
            return JsonResponse({"status": "success", "messages": ["Admin created successfully!"]})

        messages.success(request, "Admin created successfully!")
        return redirect("admin_dashboard")

    return render(request, 'admin_panel/create_admin.html')


@admin_required
def create_teacher(request):

    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect("login_page")

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        specialization = request.POST.get("specialization")
        experience_years = request.POST.get("experience_years")
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if not all([ full_name, email, password, confirm_password, specialization ]): 
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["All compulsory fields are required."]})
            messages.error(request, "All compulsory fields are required.") 
            return redirect("create_teacher")

        if password != confirm_password: 
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Passwords do not match."]})
            messages.error(request, "Passwords do not match.") 
            return redirect("create_teacher")

        if User.objects.filter(email=email).exists():
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Email already exists"]})
            messages.error(request, "Email already exists")
            return redirect("create_teacher")
        
        # Use email as the username
        username = email

        if User.objects.filter(username=username).exists():
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Username already exists"]})
            messages.error(request, "Username already exists")
            return redirect("create_teacher")

        from django.db import transaction
        try:
            with transaction.atomic():
                # Create the teacher user
                new_teacher = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role='TEACHER',
                    full_name=full_name
                )
                new_teacher.save()

                # Parse experience years if provided
                exp_years = None
                if experience_years and experience_years.strip():
                    exp_years = int(experience_years.strip())

                # Create the teacher profile
                from accounts.models import TeacherProfile
                TeacherProfile.objects.create(
                    user=new_teacher,
                    specialization=specialization,
                    experience_years=exp_years
                )
        except Exception as e:
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Database error: " + str(e)]})
            messages.error(request, "Database error: " + str(e))
            return redirect("create_teacher")

        if is_ajax:
            return JsonResponse({"status": "success", "messages": ["Teacher created successfully!"]})

        messages.success(request, "Teacher created successfully!")
        return redirect("teacher_dashboard")

    return render(request, 'teachers/create_teacher.html')
        

@admin_required
def create_student(request):

    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect("login_page")

    if request.method == "POST":
        student_id = request.POST.get('student_id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        exam_batch = request.POST.get('exam_batch')
        dob = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if not all([student_id, full_name, email, phone_number, exam_batch]):
            if is_ajax:
                return JsonResponse({"status":"error", "messages":["All compulsory fields are required."]})
            messages.error(request, "All compulsory fields are required.")
            return redirect("create_student")

        from accounts.models import Student
        if Student.objects.filter(email=email).exists():
            if is_ajax:
                return JsonResponse({"status":"error", "messages":["Email already exists."]})
            messages.error(request, "Email already exists.")
            return redirect("create_student")
        
        if Student.objects.filter(student_id=student_id).exists():
            if is_ajax:
                return JsonResponse({"status":"error", "messages":["Student ID already exists."]})
            messages.error(request, "Student ID already exists.")
            return redirect("create_student")

        from django.db import transaction
        try:
            with transaction.atomic():
                Student.objects.create(
                    student_id=student_id,
                    full_name=full_name,
                    email=email,
                    phone_number=phone_number,
                    exam_batch=exam_batch,
                    date_of_birth=dob if dob else None,
                    gender=gender if gender else None
                )
        except Exception as e:
            if is_ajax:
                return JsonResponse({"status":"error", "messages":["Database error: " + str(e)]})
            messages.error(request, "Database error: " + str(e))
            return redirect("create_student")

        if is_ajax:
            return JsonResponse({"status": "success", "messages": ["Student registered successfully!"]})

        messages.success(request, "Student registered successfully!")
        return redirect("admin_dashboard")

    return render(request, 'students/create_student.html')


def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login_page")