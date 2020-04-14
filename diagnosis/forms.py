from django import forms
from diagnosis.models import Patient_data,data_base




class PatientdataCreation(forms.ModelForm):
    class Meta:
        model = Patient_data
        fields = ('name','age','city','state','patient_status')


class TestCovidForm(forms.ModelForm):
    class Meta:
        model = data_base
        # fields = ('name','age','city','state','phone','travelHistory','fever','bodyPain','runningNose','difficulty_Breathing','soreThroat')
        exclude=('date','infectionProb','bodyPain','runningNose','difficulty_Breathing','soreThroat')



class ZoneSelect(forms.Form):
    State = forms.CharField(max_length=128,required=False )
    city = forms.CharField(max_length=128,required=False )