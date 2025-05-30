from django.core.management.base import BaseCommand
from data.models import Ward, WardCondition, Microcontroller
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Create a single test ward condition to test real-time updates'

    def handle(self, *args, **options):
        try:
            # Check if we have any wards
            wards = Ward.objects.all()
            self.stdout.write(f"Found {wards.count()} wards in database")
            
            for ward in wards:
                self.stdout.write(f"Ward: {ward.name} (slug: {ward.slug})")
            
            if not wards.exists():
                self.stdout.write(self.style.ERROR('No wards found. Please create some wards first.'))
                return
                
            # Get the first ward
            ward = wards.first()
            
            # Get or create a microcontroller for this ward
            microcontroller, created = Microcontroller.objects.get_or_create(
                ward=ward,
                defaults={
                    'serial_number': f'MC_{ward.slug.upper()}',
                    'location': f'{ward.name} - Environment Sensor',
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f"Created microcontroller: {microcontroller.serial_number}")
            else:
                self.stdout.write(f"Using existing microcontroller: {microcontroller.serial_number}")
            
            # Generate realistic sensor data
            temperature = round(random.uniform(20.0, 26.0), 1)
            humidity = round(random.uniform(40.0, 60.0), 1)
            
            # Create new ward condition
            condition = WardCondition.objects.create(
                ward=ward,
                microcontroller=microcontroller,
                temperature=temperature,
                humidity=humidity,
                timestamp=timezone.now()
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created ward condition:\n'
                    f'  Ward: {ward.name}\n'
                    f'  Temperature: {temperature}°C\n'
                    f'  Humidity: {humidity}%\n'
                    f'  Timestamp: {condition.timestamp}\n'
                    f'  ID: {condition.id}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating ward condition: {e}')
            )
