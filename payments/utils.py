from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import io
try:
    from xhtml2pdf import pisa
    has_pdf = True
except Exception:
    has_pdf = False


def send_invoice_email(payment, to_email=None, as_pdf=True, from_email=None):
    subject = f"Invoice {payment.invoice_number} - {payment.month:%B %Y}"
    to_email = to_email or payment.user.email
    from_email = from_email or 'no-reply@wardwaste.local'
    html = render_to_string('payments/invoice.html', {'payment': payment})
    email = EmailMessage(subject, html, from_email, [to_email])
    email.content_subtype = 'html'
    if as_pdf and has_pdf:
        result = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=result)
        if not pisa_status.err:
            email.attach(f'invoice_{payment.invoice_number}.pdf', result.getvalue(), 'application/pdf')
    email.send(fail_silently=False)
    return True
