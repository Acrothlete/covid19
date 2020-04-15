from django.shortcuts import render,redirect
from django.contrib import messages
from random import randint
from datetime import date,timedelta
from diagnosis.forms import PatientdataCreation,TestCovidForm,ZoneSelect
from django.http import Http404
from diagnosis.models import data_base,Patient_data
# Create your views here.



State_short=[('KA', 'Karnataka'), ('AP', 'Andhra Pradesh'), ('KL', 'Kerala'), ('TN', 'Tamil Nadu'), ('MH', 'Maharashtra'), ('UP', 'Uttar Pradesh'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('RJ', 'Rajasthan'), ('HP', 'Himachal Pradesh'), ('JK', 'Jammu & Kashmir'), ('TG', 'Telangana'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chattisgarh'), ('HR', 'Haryana'), ('JH', 'Jharkhand'), ('MP', 'Madhya Pradesh'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Orissa'), ('PB', 'Punjab'), ('SK', 'Sikkim'), ('TR', 'Tripura'), ('UA', 'Uttarakhand'), ('WB', 'West Bengal'), ('AN', 'Andaman & Nicobar'), ('CH', 'Chandigarh'), ('DN', 'Dadra & Nagar Haveli'), ('DD', 'Daman & Diu'), ('DL', 'Delhi'), ('LD', 'Lakshadweep'), ('PY', 'Pondicherry')]



def India_Covid():
    x = []
    y=[]
    for i in State_short:
        # try:
        state=str(i[1])
        x.append(Patient_data.objects.filter(state = state).count())
        y.append(data_base.objects.filter(state = state).count())
        # except
    return [x,y]


def India_circle():
    offical_city_total=Patient_data.objects.all().count()
    offical_city_found=Patient_data.objects.filter(patient_status = 'Positive').count()
    local_city_total=data_base.objects.all().count()
    local_city_found=data_base.objects.filter(infectionProb__gt = 50).count()
    circular_data=[offical_city_total,offical_city_found,local_city_total,local_city_found]
    return circular_data    



def index(request):
    state_name=[]
    for i in State_short:
        state_name.append(i[0])
    if request.method=='POST':
        state=str(request.POST.get('state'))
        city=str(request.POST.get('city')).strip()
        form = ZoneSelect(request.POST)
        if form.is_valid():
            # try:

            ofct=Patient_data.objects.filter(state = state, city = city).count()
            ofcf=Patient_data.objects.filter(state = state , city = city, patient_status = 'Positive').count()
            lct=data_base.objects.filter(state = state, city = city).count()
            lcf=data_base.objects.filter(state = state, city = city,infectionProb__gt = 50).count()
            heading = city
            circular_data=[ofct,ofcf,lct,lcf]
            context= {
                'heading':heading,
                'chart': 1,
                'circular_data':circular_data,
                'state_name': state_name,
                'offical_value': India_Covid()[0],
                'local_value': India_Covid()[1],
                'form':form,
                'report': 0
            }
            return render(request,'diagnosis/index.html',context)
            # except:
            # messages.success(request,f' Please enter valid input.')
        else:
            pass
            
    else:
        form=ZoneSelect()
        
        context= {
                'heading':'India',
                'chart': 1,
                'circular_data':India_circle(),
                'state_name': state_name,
                'offical_value': India_Covid()[0],
                'local_value': India_Covid()[1],
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


