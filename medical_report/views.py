from tkinter import W
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from matplotlib.style import context
from django.contrib import messages
from users.models import Profile
from users.views import profile
from .models import *
from .forms import ImageAddForm
from .ex import *
from notifications.signals import notify
# Create your views here.

# Gallery Image part
def allimage(request):
    profile = request.user.profile
    pr = profile.imageadd_set.all()
    # print(pr)
    context = {
        'pr':pr,
        'profile': profile
    }
    return render(request, "medical_report/allimage.html",context)


# CBC Report Image call  Part 
@login_required(login_url='login')
def cbc_(request):
    profile = request.user.profile
    pr3 = profile.totallcount_set.all()
    pr1 = profile.imageadd_set.all()
    cbc_list = Imageadd.objects.filter(image_owner = request.user.profile ,imagetype__image_type='CBC')
    
    data = []
    ref_val  = 10.2
    date_ = []
    
    check_values = request.POST.getlist('tag')
    check_values1 = request.POST.get('valu1')
    # print(check_values)

    if not check_values:
        pass
    else:
        for i in check_values:
            prof =  Imageadd.objects.get(image_id=i)
            pr1 = prof.totallcount_set.all()
            for p in pr1:
                if check_values1 == 'wbc':
                    data.append(p.wbc)
                    date_.append(prof.testdate)    
                if check_values1 == 'rbc':
                    data.append(p.rbc)
                    date_.append(prof.testdate)
                if check_values1 == 'plt':
                    data.append(p.plt)
                    date_.append(prof.testdate)
                if check_values1 == 'hbg':
                    data.append(p.hbg)
                    date_.append(prof.testdate)
                    
            pr2 = prof.absoluteleukocytecount_set.all()
            for p in pr2:
                if check_values1 == 'neutrophil':
                    data.append(p.neutrophil)
                    date_.append(prof.testdate)
                if check_values1 == 'lymphocyte':
                    data.append(p.lymphocyte)
                    date_.append(prof.testdate)
                if check_values1 == 'monocyte':
                    data.append(p.monocyte)
                    date_.append(prof.testdate)
                if check_values1 == 'eosinophil':
                    data.append(p.eosinophil)
                if check_values1 == 'basophil':
                    data.append(p.basophil)
                    date_.append(prof.testdate)
                    
            pr3 = prof.differentialleukocytecount_set.all()
            for p in pr3:
                if check_values1 == 'neutrophil2':
                    data.append(p.neutrophil2)
                    date_.append(prof.testdate)
                if check_values1 == 'lymphocyte2':
                    data.append(p.lymphocyte2)
                    date_.append(prof.testdate)
                if check_values1 == 'monocyte2':
                    data.append(p.monocyte2)
                    date_.append(prof.testdate)
                if check_values1 == 'eosinophil2':
                    data.append(p.eosinophil2)
                    date_.append(prof.testdate)
                if check_values1 == 'basophil2':
                    data.append(p.basophil2)
                    date_.append(prof.testdate)
                    
            pr4 = prof.redcellindices_set.all()
            for p in pr4:
                if check_values1 == 'pcv':
                    data.append(p.pcv)
                    date_.append(prof.testdate)
                if check_values1 == 'mcv':
                    data.append(p.mcv)
                    date_.append(prof.testdate)
                if check_values1 == 'mch':
                    data.append(p.mch)
                    date_.append(prof.testdate)
                if check_values1 == 'mchc':
                    data.append(p.mchc)
                    date_.append(prof.testdate)
                if check_values1 == 'rdw':
                    data.append(p.rdw)
                    date_.append(prof.testdate)
            pr5 = prof.pltpanel_set.all()
            for p in pr5:
                if check_values1 == 'pct':
                    data.append(p.pct)
                    date_.append(prof.testdate)
                if check_values1 == 'mpv':
                    data.append(p.mpv)
                    date_.append(prof.testdate)
                if check_values1 == 'pdw':
                    data.append(p.pdw)
                    date_.append(prof.testdate)
     
            
   
            else:
                pass
    # print(data)
    # print(date_)

    context = {'pr1':pr1,'cbc_list':cbc_list,'profile': profile,'pr3':pr3,'check_values':check_values,'check_values1':check_values1,'data':data,'ref_val':ref_val,'date_':date_}
    return render(request, "blood_medical_report/cbc.html",context)


@login_required(login_url='login')
def cbc_analysis(request,pk):

    profile = request.user.profile
    # pr1 = profile.totallcount_set.all()
    # for i in pr1:
    #     print(i.imageid)
        
    prof =  Imageadd.objects.get(image_id=pk)
    pr1 = prof.totallcount_set.all()
    pr2 = prof.absoluteleukocytecount_set.all()
    pr3 = prof.differentialleukocytecount_set.all()
    pr4 = prof.redcellindices_set.all()
    pr5 = prof.pltpanel_set.all()

    
    context = {'prof':prof,'pr1':pr1,'pr2':pr2,'pr3':pr3,'pr4':pr4,'pr5':pr5,'profile':profile}
    return render(request, "blood_medical_report/cbc_analysis.html",context)



# ESR Report Image Part 
@login_required(login_url='login')
def esr_(request):
    profile = request.user.profile
    pr1 = profile.imageadd_set.all()
    esr_list = Imageadd.objects.filter(image_owner = request.user.profile ,imagetype__image_type='ESR')
    
    data = []
    ref_val_highest  = 13
    ref_val_lowest  = 1
    date_ = []
    
    check_values = request.POST.getlist('tag')
    check_values1 = request.POST.get('valu1')
    if not check_values:
        pass
    else:
        for i in check_values:
            prof =  Imageadd.objects.get(image_id=i)
            pr1 = prof.esrcount_set.all()
            for p in pr1:
                if check_values1 == 'esr':
                    data.append(p.esr)
                    date_.append(prof.testdate)  
            else:
                pass

    
    
    
    
    context = {'pr1':pr1,'esr_list':esr_list,'profile': profile,'check_values':check_values,'check_values1':check_values1,'data':data,'ref_val_highest':ref_val_highest,'ref_val_lowest':ref_val_lowest,'date_':date_}
    return render(request, "blood_medical_report/esr.html",context)



@login_required(login_url='login')
def esr_analysis(request,pk):

    # profile = request.user.profile
    # pr1 = profile.totallcount_set.all()
    # for i in pr1:
    #     print(i.imageid)
        
    prof =  Imageadd.objects.get(image_id=pk)
    pr1 = prof.esrcount_set.all()


    
    context = {'prof':prof,'pr1':pr1}
    return render(request, "blood_medical_report/esr_analysis.html",context)

# Hba1c Report Image Part 
@login_required(login_url='login')
def hba1c_(request):
    profile = request.user.profile
    pr1 = profile.imageadd_set.all()
    hba1c_list = Imageadd.objects.filter(image_owner = request.user.profile ,imagetype__image_type='hba1c')
    
        
    data = []
    ref_val_highest  = 7.0
    ref_val_lowest  = 6.0
    date_ = []
    
    check_values = request.POST.getlist('tag')
    check_values1 = request.POST.get('valu1')
    if not check_values:
        pass
    else:
        for i in check_values:
            prof =  Imageadd.objects.get(image_id=i)
            pr1 = prof.hba1c_set.all()
            for p in pr1:
                if check_values1 == 'hba1c':
                    data.append(p.hba1c)
                    date_.append(prof.testdate)  
            else:
                pass
    
    context = {'pr1':pr1,'hba1c_list':hba1c_list,'date_':date_,'check_values1':check_values1,'data':data,'ref_val_highest':ref_val_highest,'ref_val_lowest':ref_val_lowest}
    return render(request, "blood_medical_report/hba1c.html",context)






@login_required(login_url='login')
def hba1c_analysis(request,pk):

        
    prof =  Imageadd.objects.get(image_id=pk)
    pr1 = prof.hba1c_set.all()


    
    context = {'prof':prof,'pr1':pr1}
    return render(request, "blood_medical_report/hba1c_analysis.html",context)

# Developer Details 
def developer(request):
    return render(request, "medical_report/developer.html")

# FAQ Details 
def faq(request):
    return render(request, "pages-faq.html")

# Contact Details 
def contact(request):
    return render(request, "pages-contact.html")

# Dashboard Details 
def dashboard(request):
    totallimage = []
    profile = request.user.profile
    pr1 = profile.imageadd_set.all()
    totallimage = len(pr1)
    context = {'profile': profile,'totallimage':totallimage}
    return render(request, "dashboard.html",context)


# Blood Analysis Part
@login_required(login_url='login')
def analysis(request):
    return render(request, "blood_medical_report/blood_analysis.html")


@login_required(login_url='login')
def bloodAnalysis(request):
    profile = request.user.profile
    pr1 = profile.totallcount_set.all()
    pr2 = profile.absoluteleukocytecount_set.all()
    
    # print(pr1)
    
    context = {'pr1':pr1,'pr2':pr2}
    return render(request, "blood_medical_report/blood_analysis.html",context)


# Urin Analysis Part

@login_required(login_url='login')
def urinAnalysis(request):
    return render(request, "medical_report/urin_analysis.html")

# Add Image Add Part
@login_required(login_url='login')
def addImage(request):
    return render(request, "blood_medical_report/blood_image_add.html")

# Blood Image Part Add
@login_required(login_url='login')
def bloodImage(request):
    profile = request.user.profile
    print(profile.gender)

    if request.method == 'POST':
        form = ImageAddForm(request.POST , request.FILES)
        if form is not None:
            try:
                if form.is_valid():
                    image_file = form.cleaned_data['image']
                    instance = form.save(commit=False)
                    instance.image_owner = request.user.profile
                    instance.save()
                    messages.success(request,'Image Upload Successfully')
                    
                    de = Detect_Text(image_file)
                    al = all_text(de)
                    value = specific_text(al)

                    # handle exception 
                    wbc = []
                    rbc = []
                    plt = []
                    hbg = []
                    if value.get("wbc") == None:
                        wbc = -1
                    else:
                        wbc = value["wbc"]
                    
                    if value.get("rbc") == None:
                        rbc = -1
                    else:
                        rbc = value["rbc"]          

                    if value.get("plt") == None:
                        plt = -1
                    else:
                        plt = value["plt"]
                            
                    if value.get("hbg") == None:
                        hbg = -1
                    else:
                        hbg = value["hbg"]        

                    total_count = False   
                    if wbc != -1 or rbc !=-1 or plt !=-1 or hbg != -1:
                        obj = Totallcount(wbc=wbc,rbc=rbc,plt=plt,hbg=hbg)
                        obj.image_owner = request.user.profile                        
                        obj.imageid= instance
                        obj.save()
                        total_count = True
                    
                    neutrophil = []
                    lymphocyte = []
                    monocyte = []
                    eosinophil = [] 
                    basophil = []
                    if value.get("neutrophil") == None:
                        neutrophil = -1
                    else:
                        neutrophil = value["neutrophil"]
                    
                    if value.get("lymphocyte") == None:
                        lymphocyte = -1
                    else:
                        lymphocyte = value["lymphocyte"]
                    
                    if value.get("monocyte") == None:
                        monocyte = -1
                    else:
                        monocyte = value["monocyte"]
                    
                    if value.get("eosinophil") == None:
                        eosinophil = -1
                    else:
                        eosinophil = value["eosinophil"]
                    
                    if value.get("basophil") == None:
                        basophil = -1
                    else:
                        basophil = value["basophil"]
                    
                    abs_leuk_count = False
                    if neutrophil != -1 or lymphocyte !=-1 or monocyte !=-1 or eosinophil != -1 or basophil != -1:
                        obj = Absoluteleukocytecount(neutrophil=neutrophil,lymphocyte=lymphocyte,monocyte=monocyte,eosinophil=eosinophil, basophil=basophil)
                        obj.image_owner = request.user.profile                        
                        obj.imageid= instance
                        obj.save()
                        abs_leuk_count = True
                    
                    neutrophil2 = []
                    lymphocyte2 = []
                    monocyte2 = []
                    eosinophil2 = [] 
                    basophil2 = []
                    if value.get("neutrophil%") == None:
                        neutrophil2 = -1
                    else:
                        neutrophil2 = value["neutrophil%"]
                    
                    if value.get("lymphocyte%") == None:
                        lymphocyte2 = -1
                    else:
                        lymphocyte2 = value["lymphocyte%"]
                    
                    if value.get("monocyte%") == None:
                        monocyte2 = -1
                    else:
                        monocyte2 = value["monocyte%"]
                    
                    if value.get("eosinophil%") == None:
                        eosinophil2 = -1
                    else:
                        eosinophil2 = value["eosinophil%"]
                    
                    if value.get("basophil%") == None:
                        basophil2 = -1
                    else:
                        basophil2 = value["basophil%"]
                    
                    dif_leuk_count = False
                    if neutrophil2 != -1 or lymphocyte2 !=-1 or monocyte2 !=-1 or eosinophil2 != -1 or basophil2 != -1:
                        obj = Differentialleukocytecount(neutrophil2=neutrophil2,lymphocyte2=lymphocyte2,monocyte2=monocyte2,eosinophil2=eosinophil2, basophil2=basophil2)
                        obj.image_owner = request.user.profile                        
                        obj.imageid= instance
                        obj.save()
                        dif_leuk_count = True
                    

                    pcv = []
                    mcv = []
                    mch = []
                    mchc = [] 
                    rdw = []
                    if value.get("pcv") == None:
                        pcv = -1
                    else:
                        pcv = value["pcv"]
                    
                    if value.get("mcv") == None:
                        mcv = -1
                    else:
                        mcv = value["mcv"]
                    
                    if value.get("mch") == None:
                        mch = -1
                    else:
                        mch = value["mch"]
                    
                    if value.get("mchc") == None:
                        mchc = -1
                    else:
                        mchc = value["mchc"]
                    
                    if value.get("rdw") == None:
                        rdw = -1
                    else:
                        rdw = value["rdw"]
                    
                    redcellindices_count = False
                    if pcv != -1 or mcv !=-1 or mch !=-1 or mchc != -1 or rdw != -1:
                        obj = Redcellindices(pcv=pcv,mcv=mcv,mch=mch,mchc=mchc, rdw=rdw)
                        obj.image_owner = request.user.profile                        
                        obj.imageid= instance
                        obj.save()
                        redcellindices_count = True
                    

                    pct = []
                    mpv = []
                    pdw = []
                    if value.get("pct") == None:
                        pct = -1
                    else:
                        pct = value["pct"]
                    
                    if value.get("mpv") == None:
                        mpv = -1
                    else:
                        mpv = value["mpv"]
                    
                    if value.get("pdw") == None:
                        pdw = -1
                    else:
                        pdw = value["pdw"]
                    
                    pltpanel_count = False
                    if pct != -1 or mpv !=-1 or pdw != -1:
                        obj = Pltpanel(pct=pct,mpv=mpv,pdw=pdw)
                        obj.image_owner = request.user.profile                        
                        obj.imageid= instance
                        obj.save()
                        pltpanel_count = True
                    
                    esr = []
                    
                    if value.get("esr") == None:
                        esr = -1
                    else:
                        esr = value["esr"]
                    
                    esr_count = False
                    # print(value)
                    if esr != -1:
                        # print(esr)
                        obj = Esrcount( esr=esr )
                        obj.image_owner = request.user.profile
                        obj.imageid= instance
                        obj.save()
                        esr_count = True
                        
                    
                    hba1c = []
                    
                    if value.get("hba1c") == None:
                        hba1c = -1
                    else:
                        hba1c = value["hba1c"]
                    
                    hba1c_count = False
                    # print(value)
                    if hba1c != -1:
                        # print(esr)
                        obj = Hba1c( hba1c=hba1c )
                        obj.image_owner = request.user.profile
                        obj.imageid= instance
                        obj.save()
                        hba1c_count = True
                    
                    # Only Image will save below this code 

                    # instance = form.save(commit=False)
                    # instance.image_owner = request.user.profile
                    # instance.save()

                    if total_count or abs_leuk_count or dif_leuk_count or redcellindices_count or pltpanel_count:
                        x = 'CBC'
                        obj = Imagetype(image_type=x)
                        obj.image_owner = request.user.profile
                        obj.imageid= instance
                        obj.save()
                        # messages.success(request,'Image Upload Successfully')
                    if esr_count:
                        x = 'ESR'
                        obj = Imagetype(image_type=x)
                        obj.image_owner = request.user.profile
                        obj.imageid= instance
                        obj.save()
                        # messages.success(request,'Image Upload Successfully')
                    if hba1c_count:
                        x = 'hba1c'
                        obj = Imagetype(image_type=x)
                        obj.image_owner = request.user.profile
                        obj.imageid= instance
                        obj.save()
                        # messages.success(request,'Image Upload Successfully')
                        
                    
                    notify.send(request.user, recipient=request.user, verb='Image Upload Successfully')
                    
                    return redirect('bloodImage')
                    
            except:
               
                return HttpResponse(f'Please select atleast one file ...')
                
            else:
                
                return HttpResponse(f'Please select atleast one file ....')
        
        
    else:
        
        form = ImageAddForm()
        
    return render(request, "blood_medical_report/blood_image_add.html",{'form':form,'profile': profile})

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
        if search_query is not None:
            try:
                profile = Profile.objects.get(ref_code=search_query)

                profiles =  Totallcount.objects.filter(image_owner=profile)
                print(profile.id)
                
                context = {
                    'profiles':profiles,
                    'profile':profile,
                }
                return render(request, "medical_report/paitent.html",context)
            except:
                return HttpResponse(f'No User availabe {search_query} !! Please input valid user ID ...',{'search_query':search_query})
                
    else:
        return HttpResponse(f'No User availabe {search_query} !! Please input valid user ID ...',{'search_query':search_query})
    
    
# Main page user activation profile 
@login_required(login_url='login')
def navprofile(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'navbar1.html',context)


# CBC images gallery 
def cbcimage(request):
    profile = request.user.profile
    pr1 = profile.imageadd_set.all()
    cbc_list = Imageadd.objects.filter(image_owner = request.user.profile ,imagetype__image_type='CBC')
    # print(pr1)
    
    
    context = {'pr1':pr1,'cbc_list':cbc_list,'profile': profile}
    return render(request, "blood_medical_report/cbc_image_gallery.html",context)

# esr images gallery 
def esrimage(request):
    profile = request.user.profile
    pr1 = profile.imageadd_set.all()
    esr_list = Imageadd.objects.filter(image_owner = request.user.profile ,imagetype__image_type='ESR')
    print(esr_list)
    
    
    context = {'pr1':pr1,'esr_list':esr_list,'profile': profile}
    return render(request, "blood_medical_report/esr_image_gallery.html",context)


# hba1c images gallery 
def hba1c(request):
    profile = request.user.profile
    pr1 = profile.imageadd_set.all()
    hba1c_list = Imageadd.objects.filter(image_owner = request.user.profile ,imagetype__image_type='hba1c')
    
    context = {'pr1':pr1,'hba1c_list':hba1c_list,'profile': profile}
    return render(request, "blood_medical_report/hba1c_image_gallery.html",context)