from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegistrationForm, WorkerRegistrationForm
from django.contrib import messages
from django.conf import settings
from workers.models import WorkerProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # role-based redirect
            if hasattr(user, 'workerprofile'):
                return redirect('workers:dashboard')
            return redirect('users:dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def register_user_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.full_name = form.cleaned_data['full_name']
            user.user_type = form.cleaned_data['user_type']
            user.local_body_type = form.cleaned_data['local_body_type']
            user.local_body = form.cleaned_data['local_body']
            user.ward = form.cleaned_data['ward']
            user.address = form.cleaned_data['address']
            user.phone = form.cleaned_data['phone']
            user.save()
            login(request, user)
            return redirect('users:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_user.html', {'form': form})


def register_worker_view(request):
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_worker = True
            user.save()
            worker = WorkerProfile.objects.create(
                user=user,
                worker_id=form.cleaned_data['worker_id'],
                local_body=form.cleaned_data['local_body'],
                phone=form.cleaned_data['phone'],
            )
            if form.cleaned_data['assigned_wards']:
                worker.assigned_wards.set(form.cleaned_data['assigned_wards'])
            if form.files.get('id_proof'):
                worker.id_proof = form.files['id_proof']
                worker.save()
            messages.success(request, 'Worker registration submitted for approval')
            return redirect('/')
    else:
        form = WorkerRegistrationForm()
    return render(request, 'accounts/register_worker.html', {'form': form})
