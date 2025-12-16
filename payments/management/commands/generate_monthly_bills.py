from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from payments.models import Payment
from waste.models import Pickup
from django.db.models import Count
import calendar


class Command(BaseCommand):
    help = 'Generate monthly bills for all users' 

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, help='Year for billing (default: current year)')
        parser.add_argument('--month', type=int, help='Month number for billing (1-12, default: current month)')

    def handle(self, *args, **options):
        year = options.get('year') or timezone.now().year
        month = options.get('month') or timezone.now().month
        first_day = timezone.datetime(year, month, 1)
        _, last_day_num = calendar.monthrange(year, month)
        last_day = timezone.datetime(year, month, last_day_num, 23, 59, 59)

        User = get_user_model()
        users = User.objects.all()
        created = 0
        for user in users:
            # count pickups created in month
            pickups_count = Pickup.objects.filter(waste_record__user=user, waste_record__created_at__gte=first_day, waste_record__created_at__lte=last_day).count()
            pickups_count = pickups_count or 0
            extra = max(0, pickups_count - 1)
            amount = 50 + (extra * 20)
            invoice_num = f"INV-{year}{month:02d}-{user.id}"
            p, created_flag = Payment.objects.get_or_create(user=user, month=first_day.date(), defaults={'amount': amount, 'invoice_number': invoice_num})
            if not created_flag:
                p.amount = amount
                if not p.invoice_number:
                    p.invoice_number = invoice_num
                p.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Generated/updated bills for {created} users for {year}-{month:02d}'))
