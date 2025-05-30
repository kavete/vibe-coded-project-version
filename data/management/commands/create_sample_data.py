from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from data.models import Ward, WardCondition, Microcontroller, Bed, Patient, Doctor, PatientVital


class Command(BaseCommand):
    help = 'Create sample data for testing the dashboard'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create wards
        wards_data = [
            {'name': 'ICU Ward', 'slug': 'icu-ward'},
            {'name': 'General Ward', 'slug': 'general-ward'},
            {'name': 'Emergency Ward', 'slug': 'emergency-ward'},
        ]
        
        for ward_data in wards_data:
            ward, created = Ward.objects.get_or_create(
                slug=ward_data['slug'],
                defaults={'name': ward_data['name']}
            )
            if created:
                self.stdout.write(f'Created ward: {ward.name}')
                
                # Create microcontroller for ward
                microcontroller = Microcontroller.objects.create(
                    serial_number=f'MC-{ward.slug.upper()}',
                    location=f'{ward.name} Main',
                    is_active=True,
                    ward=ward
                )
                
                # Create beds for ward
                for bed_num in range(1, 4):  # 3 beds per ward
                    bed = Bed.objects.create(
                        ward=ward,
                        bed_number=str(bed_num)
                    )
                    
                    # Create patient for bed
                    patient = Patient.objects.create(
                        name=f'Patient {ward.name} {bed_num}',
                        date_of_birth=timezone.now().date() - timedelta(days=random.randint(365*20, 365*80)),
                        bed=bed
                    )
        
        # Create doctors
        doctors_data = [
            {'name': 'Dr. Smith', 'email': 'smith@hospital.com', 'specialization': 'Cardiology'},
            {'name': 'Dr. Johnson', 'email': 'johnson@hospital.com', 'specialization': 'ICU'},
            {'name': 'Dr. Brown', 'email': 'brown@hospital.com', 'specialization': 'Emergency'},
        ]
        
        for doctor_data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                email=doctor_data['email'],
                defaults=doctor_data
            )
            if created:
                self.stdout.write(f'Created doctor: {doctor.name}')
        
        # Create historical ward conditions (last 24 hours)
        now = timezone.now()
        for ward in Ward.objects.all():
            for i in range(48):  # 48 data points over 24 hours (every 30 minutes)
                timestamp = now - timedelta(minutes=30 * i)
                
                # Simulate realistic temperature and humidity values
                base_temp = 22.0
                base_humidity = 45.0
                
                temperature = base_temp + random.uniform(-2, 3)
                humidity = base_humidity + random.uniform(-5, 10)
                
                WardCondition.objects.get_or_create(
                    ward=ward,
                    timestamp=timestamp,
                    defaults={
                        'temperature': round(temperature, 1),
                        'humidity': round(humidity, 1),
                        'microcontroller': ward.microcontroller
                    }
                )
          # Create patient vitals
        for patient in Patient.objects.all():
            for i in range(24):  # 24 data points over 24 hours (hourly)
                timestamp = now - timedelta(hours=i)
                
                systolic = random.randint(110, 140)
                diastolic = random.randint(70, 90)
                
                PatientVital.objects.get_or_create(
                    patient=patient,
                    timestamp=timestamp,
                    defaults={
                        'heart_rate': random.randint(60, 100),
                        'blood_pressure': f'{systolic}/{diastolic}',
                        'temperature': round(36.5 + random.uniform(-0.5, 1.0), 1),
                        'oxygen_saturation': random.randint(95, 100),
                        'bed': patient.bed
                    }
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {Ward.objects.count()} wards\n'
                f'- {Bed.objects.count()} beds\n'
                f'- {Patient.objects.count()} patients\n'
                f'- {Doctor.objects.count()} doctors\n'
                f'- {Microcontroller.objects.count()} microcontrollers\n'
                f'- {WardCondition.objects.count()} ward conditions\n'
                f'- {PatientVital.objects.count()} patient vitals'
            )
        )
