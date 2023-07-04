from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import SignUpForm, AddRecordForm
from .models import Record


def home(request):

    records = Record.objects.all()

    #check to if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in! Please try again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})
    

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully register! Welcome")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete = Record.objects.get(id=pk)
        delete.delete()
        messages.success(request, "Record deleted successfully...")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that!")
        return redirect('home')
    
def add_record(requset):
    form = AddRecordForm(requset.POST or None)
    if requset.user.is_authenticated:
        if requset.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(requset, "Record Added...")
                return redirect('home')
        return render(requset, 'add_record.html', {'form':form})
    else:
        messages.success(requset, "You must be logged in!")
        return redirect('home')
    

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record have been update...")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success("You must be logged in!")
        return redirect('home')
