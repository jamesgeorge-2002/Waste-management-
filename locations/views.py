from django.http import JsonResponse
from .models import Ward


def wards_for_localbody(request):
    lb = request.GET.get('local_body')
    if not lb:
        return JsonResponse({'error': 'local_body required'}, status=400)
    wards = Ward.objects.filter(local_body_id=lb).order_by('number')
    data = [{'id': w.id, 'number': w.number, 'name': w.name} for w in wards]
    return JsonResponse({'wards': data})
