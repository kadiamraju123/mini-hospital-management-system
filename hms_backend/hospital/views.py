from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import datetime

from .utils import create_calendar_event
from .forms import SignupForm, AvailabilityForm
from .models import Availability, Appointment


# Signup
def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")

    else:
        form = SignupForm()

    return render(request, "auth/signup.html", {"form": form})


# Login
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == "doctor":
                return redirect("doctor_dashboard")
            else:
                return redirect("patient_dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "auth/login.html")


# Doctor Dashboard
@login_required
def doctor_dashboard(request):

    if request.user.role != "doctor":
        return redirect("login")

    form = AvailabilityForm()

    if request.method == "POST":
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()

    slots = Availability.objects.filter(doctor=request.user)
    appointments = Appointment.objects.filter(doctor=request.user)

    return render(request, "doctor/dashboard.html", {
        "form": form,
        "slots": slots,
        "appointments": appointments
    })


# Patient Dashboard
@login_required
def patient_dashboard(request):

    slots = Availability.objects.filter(is_booked=False)

    return render(request, "patient/dashboard.html", {
        "slots": slots
    })


# Book Slot
@login_required
def book_slot(request, slot_id):

    slot = Availability.objects.get(id=slot_id)

    if slot.is_booked:
        return redirect("patient_dashboard")

    # Create appointment
    Appointment.objects.create(
        doctor=slot.doctor,
        patient=request.user,
        slot=slot
    )

    # Mark slot as booked
    slot.is_booked = True
    slot.save()

    # Create Google Calendar Event
    start = datetime.datetime.combine(slot.date, slot.start_time).isoformat()
    end = datetime.datetime.combine(slot.date, slot.end_time).isoformat()

    create_calendar_event(
        f"Appointment with Dr {slot.doctor.username}",
        start,
        end
    )

    # Send email using serverless service
    try:
        requests.post(
            "http://localhost:3000/dev/send-email",
            json={
                "action": "BOOKING_CONFIRMATION",
                "email": request.user.email
            }
        )
    except:
        print("Email service not running")

    return redirect("patient_dashboard")