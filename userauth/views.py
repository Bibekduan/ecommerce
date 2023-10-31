from django.shortcuts import render,redirect
from .forms import UserRegisterForm,ProfileForm
from django.contrib.auth import login as auth_login,authenticate,logout as auth_logout
from django.contrib import messages
from django.conf import settings
User=settings.AUTH_USER_MODEL
from django.shortcuts import get_object_or_404

from userauth.models import User,Profile

# Create your views here.
def register_views(request):
    
    if request.method == "POST":
        form=UserRegisterForm(request.POST or None)
        if form.is_valid():
            user_form=form.save()
            username=form.cleaned_data['username']
            messages.success(request, f"Hey{username}Your Account is created")
            user_form=authenticate(username=form.cleaned_data['email'],
                                   password=form.cleaned_data['password1']
                                   )
            auth_login(request,user_form)
            return redirect('index')
            
     
    else:
        form=UserRegisterForm()
     
    context={
        'form':form,
    }
    return render(request,"userauth/sign-up.html",context)



def login(request):
    if request.user.is_authenticated:
        messages.success(request, f"Hey you are already Logged-in")
        return redirect('index')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)  # Use User model and 'email'
            user = authenticate(request, email=email, password=password)  # Use 'username' instead of 'email'

            if user is not None:
                auth_login(request, user) 
                messages.success(request, "Your Are Login Now")  
                return redirect('index')
            else:
                messages.warning(request, "User Does Not Exist, create an account.")
        
        except :
            messages.warning(request, f"Your user with email {email} does not exist")
    
        
    context = {}
    return render(request, "userauth/sign-in.html", context)


def logout(request):
    messages.success(request, "User Logged-out.")
    auth_logout(request)
    return redirect('sign-in')



# def profile_update(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     if request.method == "POST":
#         form=ProfileForm(request.POST,request.FILES)
#         if form.is_valid():
#             # profile_save=form.save(commit=False)
#             # profile_save.user=request.user
#             # profile_save.save()
#             form.save()
#             messages.success(request,"Profile update successfully")
#             return redirect('dashboard')
#     else:
#         form=ProfileForm(instance=profile)
#     context={
#         'form':form,
#         'profile':profile
#     }
#     return render(request,"userauth/profile-edit.html",context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def profile_update(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile update successfully")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, "userauth/profile-edit.html", context)





