from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.models import User
from accounts.forms import UserCreateForm

# Create your views here.
class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name= 'accounts/signup.html'
