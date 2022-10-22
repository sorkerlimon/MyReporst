from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserCreationForm,ProfleForm
# from medical_report.forms import GeneratecodeForm
from .models import Profile
import random, string


# Create your views here.
@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    context = {'profile': profile}
    x = profile.email
    x = x.split('@')[0]
    suffix = ['#', '@', '$', '*']
    middle1 = ''.join(random.choice(string.ascii_letters) for i in range(1))
    middle2 = ''.join(random.choice(string.ascii_letters) for j in range(1))
    

    # profile.ref_code = refercode
    # profile.save()
    if request.method == 'POST':
        check_values = request.POST.get('tag')
        if check_values:
            prof =  Profile.objects.get(id=check_values)
            refercode = random.choice(suffix)+middle1+x+middle2+random.choice(suffix)
            prof.ref_code = refercode
            prof.save()
        return redirect('profile')
    return render(request, 'users/profiles.html',context)





def loginUser(request):

    if request.user.is_authenticated: # url bolck Jokhon user login obosthay thakbe tokhn jno url e login lekhle login e na jay
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        try:
            user = User.objects.get(username=username)
        except:
            # messages.error(request,'User not found')
            pass
        
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            messages.success(request,'Successfully Logged In')
            login(request,user)
            return redirect('dashboard')
        else:
            # print('Username or password not found')
            messages.error(request,'User name or password not found')
        print(request.POST)
    return render(request, 'users/login_.html')


def logoutUser(request):
    logout(request)
    messages.info(request,'User Logout')
    return redirect('login')

def registerUser(request):
    
    form = CustomUserCreationForm()
    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                if not User.objects.filter(email=user.email).exists():
                    x = user.email
                    user.username = x
                    user.save()
                
                    
                
                    # login(request, user)
                    messages.success(request,'User Registration Successfully Registered')
                    return redirect('login')
            else:
                messages.error(request,'An error occurred while registering blabla')

                return redirect('login')
    except:
        messages.error(request,'An error occurred while registering user')

        return redirect('login')

    context = {'form':form}

    return render(request, 'users/register_.html',context)
 
@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    info = profile.email
    form = ProfleForm(instance=profile)
    context = {'form':form}
    
    if request.method == 'POST':
        form = ProfleForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            edit = form.save(commit=False)
            if edit.email == info:
                edit.save()
                return redirect('profile')
            elif not User.objects.filter(email=edit.email).exists():
                edit.username = edit.email
                edit.save()
                return redirect('profile')
            else:
                return redirect('edit-account')

    return render(request,'users/profile_form.html',context)


