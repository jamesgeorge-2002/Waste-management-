from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
import io
try:
    from xhtml2pdf import pisa
    has_pdf = True
except Exception:
    has_pdf = False


@login_required
def payments_dashboard(request):
    payments = Payment.objects.filter(user=request.user).order_by('-month')
    return render(request, 'payments/dashboard.html', {'payments': payments})


@login_required
def pay_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    if request.method == 'POST':
        payment.paid = True
        payment.save()
        return redirect('payments:dashboard')
    return render(request, 'payments/pay.html', {'payment': payment})


@login_required
def invoice_view(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    # allow only owner or staff
    if payment.user != request.user and not request.user.is_staff:
        return HttpResponse('Forbidden', status=403)
    html = render_to_string('payments/invoice.html', {'payment': payment})
    if request.GET.get('pdf') and has_pdf:
        result = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=result)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{payment.invoice_number}.pdf"'
        return response
    return HttpResponse(html)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from django.utils import timezone
from datetime import date


@login_required
def payments_dashboard(request):
    payments = Payment.objects.filter(user=request.user).order_by('-month')
    return render(request, 'payments/dashboard.html', {'payments': payments})


@login_required
def pay_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    if request.method == 'POST':
        payment.paid = True
        payment.save()
        return redirect('payments:dashboard')
    return render(request, 'payments/pay.html', {'payment': payment})
