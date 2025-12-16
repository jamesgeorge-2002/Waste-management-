from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import io
try:
    from xhtml2pdf import pisa
    has_pdf = True
except Exception:
    has_pdf = False


def render_invoice_pdf(payment):
    html = render_to_string('payments/invoice.html', {'payment': payment})
    if not has_pdf:
        return None
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=result)
    if pisa_status.err:
        return None
    return result.getvalue()


def send_invoice_email(payment, to_email=None):
    to_email = to_email or payment.user.email
    subject = f"Invoice {payment.invoice_number} - Ward Waste Management"
    body = render_to_string('payments/invoice.html', {'payment': payment})
    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email])
    pdf = render_invoice_pdf(payment)
    if pdf:
        email.attach(f'invoice_{payment.invoice_number}.pdf', pdf, 'application/pdf')
    email.content_subtype = 'html'
    email.send()
    return True
