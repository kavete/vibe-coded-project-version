from django.db import models




class Microcontroller(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100, blank=True)  # e.g., 'Ward', 'Bed', etc.
    is_active = models.BooleanField(default=True)
    ward = models.OneToOneField('Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='microcontroller')
    # Only one microcontroller per ward for ward monitoring

    def __str__(self):
        return self.serial_number
class Ward(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    ward_microcontroller = models.OneToOneField(Microcontroller, on_delete=models.DO_NOTHING, related_name="ward_microcontroller", blank=True, null=True)

    def __str__(self):
        return self.name
    
class Bed(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=20)
    microcontroller = models.OneToOneField(Microcontroller, on_delete=models.SET_NULL, null=True, blank=True, related_name='bed')
    # Only one microcontroller per bed

    class Meta:
        unique_together = ('ward', 'bed_number')

    def __str__(self):
        return f"Ward {self.ward.name} - Bed {self.bed_number}"

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    patients = models.ManyToManyField('Patient', related_name='doctors', blank=True)
    # Many-to-many: a doctor can have many patients, a patient can have many doctors

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    admission_date = models.DateField(auto_now_add=True)
    bed = models.OneToOneField(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient')
    # Only one patient per bed, only one bed per patient

    def __str__(self):
        return self.name

class WardCondition(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='ward_conditions')
    microcontroller = models.ForeignKey(Microcontroller, on_delete=models.SET_NULL, null=True, blank=True, related_name='ward_conditions')
    # Microcontroller can be null if not assigned

    def __str__(self):
        return f"{self.ward.name} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S') }"

class PatientVital(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vitals')
    timestamp = models.DateTimeField(auto_now_add=True)
    heart_rate = models.IntegerField()
    blood_pressure = models.CharField(max_length=20)
    temperature = models.FloatField()
    oxygen_saturation = models.FloatField()
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_vitals')

    def __str__(self):
        return f"{self.patient.name} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
