from accounts.decorators import admin_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import *
from django.contrib import messages

@admin_required
def admin_dashboard(request):
    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect("login_page")
    return render(request, "admin_panel/admin_dashboard.html")


@admin_required
def admin_student_management(request):
    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect("login_page")
    return render(request, "admin_panel/admin_student_management.html")


@admin_required
def admin_teacher_management(request):
    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect("login_page")
    return render(request, "admin_panel/admin_teacher_management.html")

@admin_required
def admin_examinations(request):
    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect("login_page")
    return render(request, "admin_panel/admin_examinations.html")

@admin_required
def admin_questionbank(request):
    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect("login_page")
    return render(request, "admin_panel/admin_questionbank.html")