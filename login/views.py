from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm, EditUserChangeForm
# Create your views here.

#Singup View Function
def sign_up(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'thanks for creating your new account')
            fm.save()
    else:
        fm = SignUpForm()
    return render(request, 'login/homeRegister.html', {'form': fm})


    #login view fucntion
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'logged in successfully')  
                    return HttpResponseRedirect('/profile')                
        else: 
            fm = AuthenticationForm()
        return render(request, 'login/login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/profile')
            


    #logout view function


    #profile
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = EditUserChangeForm(request.POST, instance=request.user) 
            if fm.is_valid():
                messages.success(request, 'Updated Successfully!!')
                fm.save()
        else:
            fm = EditUserChangeForm(instance=request.user)
        return render(request, 'login/profile.html', {'name': request.user, 'form': fm})
    else : 
        return HttpResponseRedirect('login/')

def user_logout(request):
    logout(request)
    messages.success(request, 'logged out successfully!')
    return HttpResponseRedirect('/login')
   
def user_changeps(request):
    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            return HttpResponseRedirect('/profile/')
    else:
        fm = PasswordChangeForm(user=request)
    return render(request, 'login/changepassword.html', {'form': fm})
