from django.urls import path
from . import htmx_views

urlpatterns = [
    path('htmx/ward-conditions/', htmx_views.ward_conditions_partial, name='htmx_ward_conditions'),
    path('htmx/ward/<slug:ward_slug>/condition/', htmx_views.ward_condition_partial, name='htmx_ward_condition'),
    path('htmx/ward/<slug:ward_slug>/patient-vitals/', htmx_views.patient_vitals_partial, name='htmx_patient_vitals'),
    path('htmx/dashboard-stats/', htmx_views.dashboard_stats_partial, name='htmx_dashboard_stats'),
    

]
