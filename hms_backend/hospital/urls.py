from django.urls import path
from . import views

urlpatterns = [

    path('', views.user_login, name="login"),
    path('signup/', views.signup, name="signup"),

    path('doctor/dashboard/', views.doctor_dashboard, name="doctor_dashboard"),
    path('patient/dashboard/', views.patient_dashboard, name="patient_dashboard"),
    path('book/<int:slot_id>/', views.book_slot, name="book_slot"),

]