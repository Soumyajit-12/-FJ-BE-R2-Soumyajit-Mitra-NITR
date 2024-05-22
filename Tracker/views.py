from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
# from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
from django.contrib.auth.models import User
import datetime

# Create your views here.
records = Records.objects.all()

def index(request):
    global current_user
    if request.method == 'POST':
        errors = []
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            request.session['username'] = User.objects.filter(username=username)[0].username
            return redirect(home)
        else:
            errors.append('Invalid login credentials')
            return render(request, 'index.html',{'errors':errors})
    else:
        return render(request, 'index.html')

def signup(request):
    global current_user
    if request.method == 'POST':
        errors = []
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=username).exists():
            errors.append('Username already exists! Try logging in')
            return render(request, 'SignUp.html',{'errors':errors})
        elif cpassword == password:
            u = User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username, password=password, is_superuser=0)
            u.save()
            request.session['username'] = username
            return redirect(home)
        elif cpassword != password:
            errors.append('Passwords does not match')
            return render(request, 'SignUp.html',{'errors':errors})
        else:
            errors.append('An unknown error occurred. Please try again!')
            return render(request, 'SignUp.html',{'errors':errors})
    else:
        return render(request, 'SignUp.html')
    
def home(request):
    username = request.session['username']
    curr = datetime.datetime.now()
    incomes = Records.objects.filter(username=username,type="income",date__year=curr.year,date__month=curr.month)
    expenses = Records.objects.filter(username=username,type="expense",date__year=curr.year,date__month=curr.month)
    credit = 0
    debit = 0
    profit = False
    loss = False
    for i in incomes:
        credit += int(i.amount)
    for i in expenses:
        debit += int(i.amount)
    if(credit >= debit):
        overall = credit - debit
        profit = True
    else:
        overall = debit - credit
        loss = True
    return render(request, 'home.html', {'name':username,'credit':credit,'debit':debit,'profit':profit,'loss':loss,'overall':overall})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def api_records_list(request):
    username = request.session['username']
    records = list(Records.objects.filter(username=username).values())
    return JsonResponse({'data': records})

def form(request):
    username = request.session['username']
    if request.method == 'POST':
        errors = []
        type = request.POST['type']
        amount = int(request.POST['amount'])
        category = request.POST['category']
        description = request.POST['description']
        date = request.POST['date']

        if amount <= 0:
            errors.append("Invalid amount input")
            return render(request, 'form.html',{'errors':errors})
        else:
            r = Records.objects.create(username=username,type=type,amount=amount,category=category,description=description,date=date)
            r.save()
            return redirect(home)
    else:
        return render(request, 'form.html')
    
def delete(request,id):
    r = Records.objects.get(id=id)
    r.delete()
    return redirect(home)