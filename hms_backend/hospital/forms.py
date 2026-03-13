from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):

    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username','email','role','password1','password2']
from django import forms
from .models import Availability

class AvailabilityForm(forms.ModelForm):

    class Meta:
        model = Availability
        fields = ['date','start_time','end_time']