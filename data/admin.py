from django.contrib import admin
from .models import Doctor, Patient, Ward, Bed, Microcontroller, WardCondition, PatientVital
from django.utils.text import slugify

class WardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "ward_microcontroller")

admin.site.register(Ward, WardAdmin)
admin.site.register(Bed)
admin.site.register(Microcontroller)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'admission_date', 'bed', 'get_microcontroller')
    search_fields = ('name',)
    list_filter = ('admission_date', 'bed__ward')

    def get_microcontroller(self, obj):
        if obj.bed and obj.bed.microcontroller:
            return obj.bed.microcontroller.serial_number
        return None
    get_microcontroller.short_description = 'Microcontroller'

admin.site.register(Doctor)
admin.site.register(Patient, PatientAdmin)
admin.site.register(WardCondition)
admin.site.register(PatientVital)
