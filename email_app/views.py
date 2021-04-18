from django.shortcuts import render, redirect, get_object_or_404
from django.http import StreamingHttpResponse
from django.shortcuts import render
import json
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.admin import AdminSite
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta
from django.db.models import Sum
from .models import *
from .forms import *
from django.db.models import Q
from django.core import serializers
# Create your views here.

def index(request):
    request.session.flush()
    if request.method == "POST":
        data = request.POST.copy()
        if data['password1'] != data['password2']:
            return render(request, 'index.html', {'errors': 'Both passwords field did not match. Try again!'})
        data['password1'] = make_password(data['password1'])
        data['password2'] = make_password(data['password2'])

        form =userForm(data)

        if form.is_valid():
            instance = form.save(commit=True)
            request.session['logged_in'] = {'username': request.POST['username'], 'email': request.POST['email']}
            return redirect('inbox')
        else:
            print(form.errors)
            return render(request, 'index.html', {'errors': form.errors})
    return render(request, 'index.html', {'start': 'start'})



def signin(request):
    request.session.flush()
    if request.method == "POST":
        form = User.objects.filter(username=request.POST['username']).exists()
        if form:
            user = User.objects.filter(username=request.POST['username'])[0]

            if check_password(request.POST['password'], user.password1):
                request.session['logged_in'] = {'username': request.POST['username'], 'email': user.email}
                return redirect('inbox')

        return render(request, 'signin.html', {'errors': 'Invalid username or password'})
    return render(request, 'signin.html', {'start': 'start'})

def inbox(request):
    if True: #'logged_in' in request.session:
        request.session['logged_in'] = {'username': 'alex' ,'email': 'felokemboi10@gmail.com'}
        messages = Message.objects.filter(To=request.session['logged_in']['email']).order_by('-id')
        return render(request, 'inbox.html', {'messages':messages})
    else:
        return redirect('index')

def logout(request):
    if 'logged_in' in request.session:
        request.session.flush()
    return redirect('signin')

def message_view(request, id):
    if 'logged_in' in request.session:
        message = Message.objects.get(id=id)

        if request.method == "POST":
            form = messageForm({'To':message.From, 'From':message.To, 'subject':message.subject,
                                'body':request.POST['body']})
            if form.is_valid():
                instance = form.save(commit=True)
                return render(request, 'message_view.html', {'message': message, 'success': 'Reply sent successfully!'})
            else:
                return render(request, 'message_view.html', {'message': message, 'errors': form.errors})

        return render(request, 'message_view.html', {'message': message, 'start':'start'})
    else:
        return redirect('index')


def message_view2(request, id):
    if 'logged_in' in request.session:
        message = Message.objects.get(id=id)
        if request.method == "POST":
            form = messageForm({'To':message.To, 'From':message.From, 'subject':message.subject,
                                'body':request.POST['body']})
            if form.is_valid():
                instance = form.save(commit=True)
                return render(request, 'message_view.html', {'message': message, 'success': 'Reply sent successfully!'})
            else:
                return render(request, 'message_view.html', {'message': message, 'errors': form.errors})

        return render(request, 'message_view2.html', {'message': message, 'start':'start'})
    else:
        return redirect('index')


def sent(request):
    if 'logged_in' in request.session:
        messages = Message.objects.filter(From=request.session['logged_in']['email']).order_by('-id')
        return render(request, 'sent.html',{'messages':messages})
    else:
        return redirect('index')

def compose(request):
    if 'logged_in' in request.session:
        if request.method == "POST":
            form = messageForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=True)
                return render(request, 'compose.html', {'message':' Email sent successfully!'})
            else:
                return render(request, 'compose.html', {'errors': form.errors})

        return render(request, 'compose.html', {'start': 'start'})
    else:
        return redirect('index')
