from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import redirect
from django.shortcuts import render
from django.views.generic import TemplateView

