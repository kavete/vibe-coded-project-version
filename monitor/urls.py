from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from data.views import dashboard, ward_detail
'''dashboard_htmx, ward_detail_htmx '''
from data import htmx_views

urlpatterns = [
    # Dashboard views
    path('', dashboard, name='dashboard'),
    path('ward/<slug:ward_slug>/', ward_detail, name='ward_detail'),
    path('', include('data.urls')),
    path('admin/', admin.site.urls),
]
