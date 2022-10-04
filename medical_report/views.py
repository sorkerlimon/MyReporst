from tkinter import W
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from matplotlib.style import context

from users.models import Profile
from users.views import profile
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
    
    # print(pr1)
    
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
    # print(pr)

    if request.method == 'POST':
        form = ImageAddForm(request.POST , request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            
            # handle exception 
            wbc = []
            rbc = []
            plt = []
            hbg = []
            
            
            de = Detect_Text(image_file)
            al = all_text(de)
            
            wbc = specific_text_wbc(al)
            if wbc is None:
                print('Data not saved..')
                wbc = 0
            else:
                wbc = wbc
                    


            rbc = specific_text_rbc(al)
            if rbc is None:
                print('Data not saved..')
                rbc = 0
            else:
                rbc = rbc
                    

            plt = specific_text_plt(al)
            if plt is None:
                print('Data not saved..')
                plt = 0
            else:
                plt = plt
                    


            hbg = specific_text_hbg(al)
            if hbg is None:
                print('Data not saved..')
                hbg = 0
            else:
                hbg = hbg
                    
            
            obj = Totallcount(wbc=wbc,rbc=rbc,plt=plt,hbg=hbg)
            obj.image_owner = request.user.profile
            obj.save()
            
            # Only Image will save below this code 
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

# Patient find
@login_required(login_url='login')
def paitent(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        
        
        search_query = request.GET.get('search_query')
        # profileData =  Profile.objects.filter(id=search_query)
        userprofile = Profile.objects.filter(id=search_query)
        # profiles = Totallcount.objects.filter(image_owner="00877c6b-772b-4d8f-b95f-4c415c0ddcc5")
        profiles =  Totallcount.objects.filter(image_owner=search_query)
        

    context = {
       'profiles':profiles,
       'userprofile':userprofile,
     
    }
    return render(request, "medical_report/paitent.html",context)


