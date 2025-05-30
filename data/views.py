from django.shortcuts import render, get_object_or_404
from .models import Patient, Doctor, WardCondition, PatientVital, Bed, Microcontroller, Ward
from django.utils import timezone
from django.db.models import Max

def dashboard(request):
    # Get the latest ward condition for each ward
    latest_per_ward = (
        WardCondition.objects.values('ward')
        .annotate(latest=Max('timestamp'))
    )
    # Build a list of latest WardCondition objects for each ward
    latest_conditions = [
        WardCondition.objects.filter(ward=entry['ward'], timestamp=entry['latest']).first()
        for entry in latest_per_ward
    ]
    # Hero stats
    ward_count = Ward.objects.count()
    patient_count = Patient.objects.count()
    doctor_count = Doctor.objects.count()
    bed_count = Bed.objects.count()
    microcontroller_count = Microcontroller.objects.count()
    context = {
        'ward_conditions': latest_conditions,
        'ward_count': ward_count,
        'patient_count': patient_count,
        'doctor_count': doctor_count,
        'bed_count': bed_count,
        'microcontroller_count': microcontroller_count,
    }
    return render(request, 'data/dashboard.html', context)

def ward_detail(request, ward_slug):
    ward = get_object_or_404(Ward, slug=ward_slug)
    context = {
        'ward_name': ward.name,
        'ward_slug': ward.slug,
    }
    return render(request, 'data/ward_detail.html', context)

