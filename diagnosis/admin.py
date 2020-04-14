from django.contrib import admin
from diagnosis.models import data_base,Patient_data

# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display=('name','city','state','patient_status')
    search_fields=('name','city','state','patient_status')

class DatabaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display=('name','phone','city','state')
    search_fields=('name','phone','city','state')


admin.site.register(data_base,DatabaseAdmin)
admin.site.register(Patient_data,PatientAdmin)


