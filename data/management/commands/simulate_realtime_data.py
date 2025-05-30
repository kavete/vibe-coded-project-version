from django.core.management.base import BaseCommand
import random
import time
from datetime import datetime
from data.models import Ward, WardCondition, Microcontroller, Patient, PatientVital
from django.utils import timezone


class Command(BaseCommand):
    help = 'Simulate real-time data from microcontrollers for testing HTMX updates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=5,
            help='Interval between data updates in seconds (default: 5)'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=0,
            help='Number of updates to generate (0 = infinite, default: 0)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        count = options['count']
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting real-time data simulation...')
        )
        self.stdout.write(f"⏱️  Update interval: {interval} seconds")
        if count > 0:
            self.stdout.write(f"🔢 Total updates: {count}")
        else:
            self.stdout.write("🔄 Running continuously (Ctrl+C to stop)")
        
        updates_made = 0
        
        try:
            while count == 0 or updates_made < count:
                # Randomly choose what type of data to create
                if random.choice([True, False]):
                    success = self.simulate_ward_condition_update()
                else:
                    success = self.simulate_patient_vital_update()
                
                if success:
                    updates_made += 1
                
                if count == 0 or updates_made < count:
                    time.sleep(interval)
                    
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING(f'\n🛑 Simulation stopped by user after {updates_made} updates.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Simulation error: {e}')
            )

    def simulate_ward_condition_update(self):
        """Simulate a microcontroller sending new ward condition data."""
        try:
            # Get a random ward
            wards = Ward.objects.all()
            if not wards:
                self.stdout.write(
                    self.style.WARNING("No wards found. Please create some wards first.")
                )
                return False
                
            ward = random.choice(wards)
              # Get or create a microcontroller for this ward
            microcontroller, created = Microcontroller.objects.get_or_create(
                ward=ward,
                defaults={
                    'serial_number': f'MC_{ward.slug.upper()}',
                    'location': f'{ward.name} - Environment Sensor',
                    'is_active': True
                }
            )
            
            # Generate realistic sensor data
            temperature = round(random.uniform(20.0, 26.0), 1)  # Hospital room temperature
            humidity = round(random.uniform(40.0, 60.0), 1)     # Comfortable humidity
            
            # Create new ward condition
            condition = WardCondition.objects.create(
                ward=ward,
                microcontroller=microcontroller,
                temperature=temperature,
                humidity=humidity,
                timestamp=timezone.now()
            )
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ Ward condition: {ward.name} - {temperature}°C, {humidity}%")
            )
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creating ward condition: {e}")
            )
            return False

    def simulate_patient_vital_update(self):
        """Simulate a patient monitoring device sending new vital data."""
        try:
            # Get a random patient
            patients = Patient.objects.filter(bed__isnull=False)
            if not patients:
                self.stdout.write(
                    self.style.WARNING("No patients with beds found. Please create some patients first.")
                )
                return False
            patient = random.choice(patients)
            
            # Generate realistic vital signs
            heart_rate = random.randint(60, 100)      # Normal resting heart rate
            blood_pressure_sys = random.randint(110, 140)  # Normal systolic
            blood_pressure_dia = random.randint(70, 90)   # Normal diastolic
            blood_pressure = f"{blood_pressure_sys}/{blood_pressure_dia}"  # Combined format
            temperature = round(random.uniform(36.0, 37.5), 1)  # Normal body temperature
            oxygen_saturation = random.randint(95, 100)         # Normal oxygen saturation
            
            # Create new patient vital
            vital = PatientVital.objects.create(
                patient=patient,
                heart_rate=heart_rate,
                blood_pressure=blood_pressure,
                temperature=temperature,
                oxygen_saturation=oxygen_saturation,
                bed=patient.bed,
                timestamp=timezone.now()
            )
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ Patient vital: {patient.name} - HR:{heart_rate}, BP:{blood_pressure}, Temp:{temperature}°C")
            )
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creating patient vital: {e}")
            )
            return False
