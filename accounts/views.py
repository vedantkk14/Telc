from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

def login_page(request):

    # if request.user.is_authenticated:

    #     if request.user.role == "ADMIN":
    #         return redirect("/admin_panel/admin_dashboard")

    #     elif request.user.role == "TEACHER":
    #         return redirect("/teachers/dashboard")

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

            return render(request, 'auth/login_page.html', {
                'login_success': True,
                'redirect_url': reverse('admin_dashboard')
            })

        # if user.role == "ADMIN":
        #     return redirect('admin_dashboard')

        # elif user.role == "TEACHER":
        #     return redirect('teachers_dashboard')

    return render(request, 'auth/login_page.html')


from django.http import JsonResponse

@login_required
def create_admin(request):

    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permisson to access this page')
        return redirect("login_page")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if not all([ username, email, password, confirm_password ]): 
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["All fields are required."]})
            messages.error( request, "All fields are required." ) 
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
        
        if User.objects.filter(username=username).exists():
            if is_ajax:
                return JsonResponse({"status": "error", "messages": ["Username already exists"]})
            messages.error(request, "Username already exists")
            return redirect("create_admin")

        # Create the admin user
        new_admin = User.objects.create_user(username=username, email=email, password=password, role='ADMIN')
        new_admin.is_staff = True
        new_admin.save()

        if is_ajax:
            return JsonResponse({"status": "success", "messages": ["Admin created successfully!"]})

        messages.success(request, "Admin created successfully!")
        return redirect("create_admin")

    return render(request, 'admin_panel/create_admin.html')   
        