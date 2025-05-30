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
