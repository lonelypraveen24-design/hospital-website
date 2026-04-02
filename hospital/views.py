import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Doctor, Appointment, ContactMessage, Department, UserProfile


# ===== PAGES =====

def home(request):
    """Main hospital homepage"""
    return render(request, 'index.html')


def login_page(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def register_page(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone', '')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, phone=phone)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    """Patient dashboard"""
    appointments = Appointment.objects.filter(email=request.user.email)
    return render(request, 'dashboard.html', {'appointments': appointments})


# ===== REST API =====

def api_doctors(request):
    """GET /api/doctors/ – list all available doctors"""
    doctors = Doctor.objects.filter(available=True).values(
        'id', 'name', 'specialization', 'experience', 'rating'
    )
    return JsonResponse(list(doctors), safe=False)


def api_departments(request):
    """GET /api/departments/ – list all departments"""
    depts = Department.objects.all().values('id', 'name', 'description', 'icon')
    return JsonResponse(list(depts), safe=False)


@require_http_methods(["POST"])
def api_contact(request):
    """POST /api/contact/ – save appointment/contact form"""
    try:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        department = request.POST.get('department', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email:
            return JsonResponse({'success': False, 'error': 'Name and email are required.'}, status=400)

        # Save as appointment
        Appointment.objects.create(
            name=name, email=email, phone=phone,
            department=department, message=message
        )
        # Also save as contact message
        ContactMessage.objects.create(
            name=name, email=email, phone=phone,
            department=department, message=message
        )
        return JsonResponse({'success': True, 'message': 'Appointment booked successfully!'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def api_my_appointments(request):
    """GET /api/my-appointments/ – current user's appointments"""
    appointments = Appointment.objects.filter(
        email=request.user.email
    ).values('id', 'name', 'department', 'status', 'created_at')
    return JsonResponse(list(appointments), safe=False)

# Create your views here.
