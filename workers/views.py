from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WorkerProfile
from waste.models import Pickup
from django.contrib import messages
from django.utils import timezone


@login_required
def dashboard(request):
    try:
        wp = request.user.workerprofile
    except WorkerProfile.DoesNotExist:
        return redirect('/')
    pickups = Pickup.objects.filter(assigned_worker=wp).order_by('status')
    return render(request, 'workers/dashboard.html', {'pickups': pickups, 'worker': wp})


@login_required
def update_pickup_status(request, pickup_id):
    pickup = get_object_or_404(Pickup, id=pickup_id)

    # Ensure only assigned worker can update
    try:
        wp = request.user.workerprofile
    except WorkerProfile.DoesNotExist:
        messages.error(request, 'Only workers can update pickups')
        return redirect('/')

    if pickup.assigned_worker != wp:
        messages.error(request, 'You are not assigned to this pickup')
        return redirect('workers:dashboard')

    if request.method == 'POST':
        status = request.POST.get('status')
        verified_weight = request.POST.get('verified_weight')
        worker_proof = request.FILES.get('worker_proof')
        if status in dict(Pickup._meta.get_field('status').choices):
            pickup.status = status
            if worker_proof:
                pickup.worker_proof_image = worker_proof
            if status == 'completed':
                pickup.completed_at = timezone.now()
                # set verified weight if provided
                try:
                    vw = float(verified_weight) if verified_weight else None
                    if vw:
                        wr = pickup.waste_record
                        wr.verified_weight = vw
                        wr.save()
                except ValueError:
                    pass
            pickup.save()
            messages.success(request, 'Pickup updated')
        return redirect('workers:dashboard')
    return render(request, 'workers/update_pickup.html', {'pickup': pickup})
