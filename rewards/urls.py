from django.urls import path
from django.http import HttpResponse

app_name = 'rewards'


def index(request):
    return HttpResponse("Rewards placeholder")


urlpatterns = [
    path('', index, name='index'),
]
