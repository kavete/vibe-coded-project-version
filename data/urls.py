from django.urls import path
from . import htmx_views

urlpatterns = [
    path('htmx/ward-conditions/', htmx_views.ward_conditions_partial, name='htmx_ward_conditions'),
    path('htmx/ward/<slug:ward_slug>/condition/', htmx_views.ward_condition_partial, name='htmx_ward_condition'),
    path('htmx/ward/<slug:ward_slug>/patient-vitals/', htmx_views.patient_vitals_partial, name='htmx_patient_vitals'),
    path('htmx/dashboard-stats/', htmx_views.dashboard_stats_partial, name='htmx_dashboard_stats'),
    
    # Chart data endpoints
    path('htmx/patient/<int:patient_id>/vitals-chart-data/', htmx_views.patient_vitals_chart_data, name='htmx_patient_vitals_chart_data'),
    path('htmx/ward/<slug:ward_slug>/conditions-chart-data/', htmx_views.ward_conditions_chart_data, name='htmx_ward_conditions_chart_data'),
      # Chart partial endpoints
    path('htmx/patient/<int:patient_id>/vitals-chart/', htmx_views.patient_vitals_chart_partial, name='htmx_patient_vitals_chart'),
    path('htmx/ward/<slug:ward_slug>/conditions-chart/', htmx_views.ward_conditions_chart_partial, name='htmx_ward_conditions_chart'),
    path('htmx/ward/<slug:ward_slug>/patient-charts/', htmx_views.patient_charts_multiple_partial, name='htmx_patient_charts_multiple'),
    path('htmx/dashboard-charts/', htmx_views.dashboard_charts_partial, name='htmx_dashboard_charts'),
]
