from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/')),
    path('accounts/', include('accounts.urls')),  # auth & registration
    path('locations/', include('locations.urls')),
    path('users/', include('users.urls')),
    path('workers/', include('workers.urls')),
    path('waste/', include('waste.urls')),
    path('payments/', include('payments.urls')),
    path('rewards/', include('rewards.urls')),
    path('adminpanel/', include('adminpanel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
