from django.shortcuts import render,redirect
from django.contrib import messages
from random import randint
from datetime import date,timedelta
from diagnosis.forms import PatientdataCreation,TestCovidForm,ZoneSelect
from django.http import Http404
from diagnosis.models import data_base,Patient_data
# Create your views here.

india_states= ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]

def India_Covid():
    covid_Values = []
    for i in india_states:
        try:
            covid_Values.append(Patient_data.objects.filter(state = i).count())
        except:
            pass
    return covid_Values




def index(request):
    
    if request.method=='POST':
        state=request.POST.get('state')
        city=request.POST.get('city')
        form = ZoneSelect(request.POST)
        if form.is_valid():
            circle_total=Patient_data.objects.filter(state = state, city=city).count()
            pass
        else:
            print("form invalid")
    else:
        form=ZoneSelect()
    context={
        'form':form,
        'report': 0
    }
    return render(request,'diagnosis/index.html',context)


def PatientEntry(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form= PatientdataCreation(request.POST) 
            if form.is_valid():
                form.save()
                messages.success(request,f'Hi your patient details has been saved successfully.')
                return redirect('index')
            else:
                messages.success(request,f' Please enter valid input.')
                return redirect('entry')
        
        form= PatientdataCreation()
        context = {
            'staff': 1,
            'form':form,
        }

        return render(request,'diagnosis/input.html',context)
    else:
        raise Http404()


def TestCovid(request):
    if request.method=='POST':
        try:
            bodypain=request.POST.get("bodypain")
            runnynose=request.POST.get("runnynose")
            diffbreath=request.POST.get("diffbreath")
            sorethroat=request.POST.get("sorethroat")
        except:
            messages.success(request,f'Please enter valid details.')
        form= TestCovidForm(request.POST) 
        if form.is_valid():
            obj=form.save(commit=False)
            if (bodypain):obj.bodyPain=bodypain
            if (runnynose):obj.runningNose=runnynose
            if (diffbreath):obj.difficulty_Breathing=diffbreath
            if (sorethroat):obj.soreThroat=sorethroat
            inf_prob=(int(obj.soreThroat) *8)+(int(obj.runningNose)*8)+(int(obj.bodyPain)*8)+(int(obj.difficulty_Breathing)*8)+(int(obj.fever)*8)+(int(obj.travelHistory)*7)
            obj.infectionProb=inf_prob
            print(inf_prob)
            obj.save()
            zone=''
            color=''
            if inf_prob:
                if inf_prob<50:
                    messages.success(request,f'Very low {inf_prob}%')
                    zone="SAFE ZONE"
                    color="Congrats!"
                elif 60>inf_prob>50:
                    messages.info(request,f'High {inf_prob}%')
                    zone="VULNERABLE ZONE"
                    color="Opps!"
                else:
                    messages.error(request,f'Very high {inf_prob}%')
                    zone="CRITICAL ZONE"
                    color="Caution!"
            
            total_tested=data_base.objects.all().count()
            total_detected=data_base.objects.filter(infectionProb__gt = 50).count()
            context = {
                    'tests_all': total_tested,
                    'detected': total_detected,
                    'name':obj.name,
                    'zone':zone,
                    'prob':inf_prob,
                    'color':color,
                    'report':1,
            }
            return render(request,'diagnosis/index.html',context)
            
        else:
            messages.success(request,f'Please enter valid details.')
    
    else:
        form= TestCovidForm()
    context = {
        'staff': 0,
        'form':form,
    }
    return render(request,'diagnosis/input.html',context)


