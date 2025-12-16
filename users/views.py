from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from waste.models import WasteRecord, Pickup
from django.contrib import messages
from django.shortcuts import get_object_or_404
from waste.models import Pickup
from django.utils import timezone


@login_required
def dashboard(request):
    waste = WasteRecord.objects.filter(user=request.user).order_by('-created_at')
    pickups = Pickup.objects.filter(waste_record__user=request.user).order_by('-status')
    return render(request, 'users/dashboard.html', {'waste': waste, 'pickups': pickups})


@login_required
def report_waste(request):
    if request.method == 'POST':
        wt = request.POST.get('waste_type')
        weight = request.POST.get('weight')
        image = request.FILES.get('image')
        if wt and weight:
            try:
                w = WasteRecord.objects.create(user=request.user, waste_type=wt, entered_weight=float(weight), image=image)
                messages.success(request, 'Waste reported, pickup requested')
                return redirect('users:dashboard')
            except Exception as e:
                messages.error(request, 'Could not save waste report')
    return render(request, 'users/report_waste.html')


@login_required
def request_reschedule(request, pickup_id):
    pickup = get_object_or_404(Pickup, id=pickup_id, waste_record__user=request.user)
    if request.method == 'POST':
        date = request.POST.get('scheduled_date')
        if date:
            try:
                dt = timezone.datetime.fromisoformat(date)
                pickup.scheduled_date = dt.date()
                pickup.status = 'requested'
                pickup.save()
                messages.success(request, 'Reschedule requested')
                return redirect('users:dashboard')
            except Exception:
                messages.error(request, 'Invalid date format. Use YYYY-MM-DD')
    return render(request, 'users/reschedule.html', {'pickup': pickup})
