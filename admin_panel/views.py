from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN" and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect("login_page")
    return render(request, "admin_panel/admin_dashboard.html")
