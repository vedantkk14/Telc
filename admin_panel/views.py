from django.shortcuts import render

def admin_dashboard(request):
    return render(request, "admin_panel/admin_dashboard.html")
