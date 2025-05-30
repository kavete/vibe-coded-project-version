from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Ward, WardCondition, Patient, PatientVital, Microcontroller, Bed, Doctor


def dashboard_stats_partial(request):
    """Return dashboard statistics as partial HTML"""
    context = {
        'ward_count': Ward.objects.count(),
        'bed_count': Bed.objects.count(),
        'patient_count': Patient.objects.count(),
        'doctor_count': Doctor.objects.count(),
        'microcontroller_count': Microcontroller.objects.filter(is_active=True).count(),
    }
    return render(request, 'data/partials/dashboard_stats.html', context)


def ward_conditions_partial(request):
    """Return all ward conditions as partial HTML"""
    ward_conditions = []
    for ward in Ward.objects.all():
        latest_condition = WardCondition.objects.filter(ward=ward).order_by('-timestamp').first()
        if latest_condition:
            ward_conditions.append(latest_condition)
    
    context = {'ward_conditions': ward_conditions}
    return render(request, 'data/partials/ward_conditions.html', context)


def ward_condition_partial(request, ward_slug):
    """Return specific ward condition as partial HTML"""
    ward = get_object_or_404(Ward, slug=ward_slug)
    latest_condition = WardCondition.objects.filter(ward=ward).order_by('-timestamp').first()
    
    context = {
        'condition': latest_condition,
        'ward': ward,
    }
    return render(request, 'data/partials/ward_condition.html', context)


def patient_vitals_partial(request, ward_slug):
    """Return patient vitals for a specific ward as partial HTML"""
    ward = get_object_or_404(Ward, slug=ward_slug)
    
    # Get all patients in beds within this ward
    patients_in_ward = Patient.objects.filter(bed__ward=ward).select_related('bed')
    
    patient_vitals = []
    for patient in patients_in_ward:
        latest_vital = PatientVital.objects.filter(patient=patient).order_by('-timestamp').first()
        if latest_vital:
            patient_vitals.append(latest_vital)
    
    context = {'patient_vitals': patient_vitals}
    return render(request, 'data/partials/patient_vitals.html', context)


def patient_vitals_chart_data(request, patient_id):
    """Return patient vitals chart data as JSON for Plotly"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Get last 24 hours of vitals
    time_threshold = timezone.now() - timedelta(hours=24)
    vitals = PatientVital.objects.filter(
        patient=patient,
        timestamp__gte=time_threshold
    ).order_by('timestamp')
    
    timestamps = [vital.timestamp.strftime('%H:%M') for vital in vitals]
    heart_rates = [vital.heart_rate for vital in vitals]
    temperatures = [vital.temperature for vital in vitals]
    oxygen_saturations = [vital.oxygen_saturation for vital in vitals]
    
    chart_data = {
        'timestamps': timestamps,
        'heart_rates': heart_rates,
        'temperatures': temperatures,
        'oxygen_saturations': oxygen_saturations,
        'patient_name': patient.name
    }
    
    return JsonResponse(chart_data)


def ward_conditions_chart_data(request, ward_slug):
    """Return ward conditions chart data as JSON for Plotly"""
    ward = get_object_or_404(Ward, slug=ward_slug)
    
    # Get last 24 hours of conditions
    time_threshold = timezone.now() - timedelta(hours=24)
    conditions = WardCondition.objects.filter(
        ward=ward,
        timestamp__gte=time_threshold
    ).order_by('timestamp')
    
    timestamps = [condition.timestamp.strftime('%H:%M') for condition in conditions]
    temperatures = [condition.temperature for condition in conditions]
    humidity_levels = [condition.humidity for condition in conditions]
    
    chart_data = {
        'timestamps': timestamps,
        'temperatures': temperatures,
        'humidity_levels': humidity_levels,
        'ward_name': ward.name
    }
    
    return JsonResponse(chart_data)


def patient_vitals_chart_partial(request, patient_id):
    """Return patient vitals chart as partial HTML"""
    patient = get_object_or_404(Patient, id=patient_id)
    context = {
        'patient': patient,
        'chart_id': f'patient-vitals-{patient.id}'
    }
    return render(request, 'data/partials/patient_vitals_chart.html', context)


def ward_conditions_chart_partial(request, ward_slug):
    """Return ward conditions chart as partial HTML"""
    ward = get_object_or_404(Ward, slug=ward_slug)
    context = {
        'ward': ward,
        'chart_id': f'ward-conditions-{ward.slug}'
    }
    return render(request, 'data/partials/ward_conditions_chart.html', context)


def dashboard_charts_partial(request):
    """Return dashboard overview charts as partial HTML"""
    # Get data for overview charts
    recent_vitals = PatientVital.objects.filter(
        timestamp__gte=timezone.now() - timedelta(hours=1)
    ).order_by('-timestamp')[:10]
    
    context = {
        'recent_vitals': recent_vitals,
    }
    return render(request, 'data/partials/dashboard_charts.html', context)


def patient_charts_multiple_partial(request, ward_slug):
    """Return multiple patient charts for a ward as partial HTML"""
    ward = get_object_or_404(Ward, slug=ward_slug)
    
    # Get all patients in beds within this ward
    patients_in_ward = Patient.objects.filter(bed__ward=ward).select_related('bed')
    
    patient_vitals = []
    for patient in patients_in_ward:
        latest_vital = PatientVital.objects.filter(patient=patient).order_by('-timestamp').first()
        if latest_vital:
            patient_vitals.append(latest_vital)
    
    context = {'patient_vitals': patient_vitals}
    return render(request, 'data/partials/patient_charts_multiple.html', context)
