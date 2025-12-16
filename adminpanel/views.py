from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from waste.models import Pickup
from workers.models import WorkerProfile
from django.contrib import messages


@staff_member_required
def pickups_list(request):
    pickups = Pickup.objects.filter(assigned_worker__isnull=True).order_by('scheduled_date', 'waste_record__created_at')
    workers = WorkerProfile.objects.filter(approved=True)
    return render(request, 'adminpanel/pickups_list.html', {'pickups': pickups, 'workers': workers})


@staff_member_required
def assign_pickup(request, pickup_id):
    pickup = get_object_or_404(Pickup, id=pickup_id)
    if request.method == 'POST':
        worker_id = request.POST.get('worker')
        worker = get_object_or_404(WorkerProfile, id=worker_id)
        pickup.assigned_worker = worker
        pickup.status = 'assigned'
        pickup.save()
        messages.success(request, f'Pickup {pickup.id} assigned to {worker}')
        return redirect('adminpanel:pickups_list')
    workers = WorkerProfile.objects.filter(approved=True)
    return render(request, 'adminpanel/assign_pickup.html', {'pickup': pickup, 'workers': workers})
