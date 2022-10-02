from tkinter import W
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Blood_report,Totallcount
from .forms import ImageAddForm
from .ex import Detect_Text,all_text,specific_text_wbc,specific_text_rbc,specific_text_plt,specific_text_hbg
# Create your views here.

def allimage(request):
    profile = request.user.profile
    pr = profile.imageadd_set.all()
    print(pr)
    context = {
        'pr':pr
    }
    return render(request, "medical_report/allimage.html",context)


# Developer Details 
def developer(request):
    return render(request, "medical_report/developer.html")


# Blood Analysis Part
@login_required(login_url='login')
def analysis(request):
    return render(request, "blood_medical_report/blood_analysis.html")


@login_required(login_url='login')
def bloodAnalysis(request):
    profile = request.user.profile
    pr = profile.blood_report_set.all()
    pr1 = profile.totallcount_set.all()
    
    print(pr1)
    
    context = {'pr': pr,'pr1':pr1}
    return render(request, "blood_medical_report/blood_analysis.html",context)


# Urin Analysis Part

@login_required(login_url='login')
def urinAnalysis(request):
    return render(request, "medical_report/urin_analysis.html")

# Add Image Add Part
@login_required(login_url='login')
def addImage(request):
    return render(request, "blood_medical_report/blood_image_add.html")

# Blood Image Part
@login_required(login_url='login')
def bloodImage(request):
    profile = request.user.profile
    pr = profile.imageadd_set.all()
    print(pr)

    if request.method == 'POST':
        form = ImageAddForm(request.POST , request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            
            de = Detect_Text(image_file)
            al = all_text(de)
            
            wbc = specific_text_wbc(al)

            rbc = specific_text_rbc(al)

            plt = specific_text_plt(al)

            hbg = specific_text_hbg(al)

            # profile = request.user.profile
            obj = Totallcount(wbc=wbc,rbc=rbc,plt=plt,hbg=hbg)
            obj.image_owner = request.user.profile
            obj.save()
            
              
            instance = form.save(commit=False)
            instance.image_owner = request.user.profile
            instance.save()
            
            return redirect('bloodImage')
        
        
    else:
        form = ImageAddForm()
    return render(request, "blood_medical_report/blood_image_add.html",{'form':form,'pr': pr})


# Urin Image Part
@login_required(login_url='login')
def urinImage(request):
    return render(request, "medical_report/urin_image_add.html")

