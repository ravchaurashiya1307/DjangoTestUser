from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
import re
from .email import Email
from django.shortcuts import render
from .decode import Decode
import smtplib
import requests
from . import executor
from django.contrib import messages

email=''

def login(request):
    if request.method=='POST':
        name = str(request.POST['name'])
        pwd = str(request.POST['password'])
        if(name=='admin' and pwd=='admin'):
            return redirect('/user/')
        else:
            return render(request, 'login.html', {'mymsg':'Invalid Details'})
    elif request.method == 'GET':
        return render(request, 'login.html')


def validateName(name):
    if(' ' in name):
        names=name.split()
    else:
        names=[name]
    for name in names:
        if(name.isalpha()):
            return True
        else:
            print('name prblm')
            return False

def validateDob(dob):
    from datetime import datetime
    date_string = dob
    date_string2 = "2002-04-22 00:00:00"
    dt=datetime.fromisoformat(date_string)
    dt2=datetime.fromisoformat(date_string2)
    if(dt.date()>dt2.date()):
        print('dob prblm')
        return False
    else:
        return True

def validateEmail(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return  True
    else:
        print('email prblm')
        return False

def validatePN(pn):
    if(pn.isnumeric()):
        res = requests.get(
            "http://apilayer.net/api/validate?access_key=86ef7c20efe78fe00b1ef87caf75ef76&number=91" + pn + "&country_code=&format=1")
        resJson=res.json()
        if(resJson['valid']==True):
            return True
        else:
            print('pn prblm')
            return False
    else:
        return False

def User(request):
    global email
    if request.method=='POST':
        em=Email()
        name = str(request.POST['name'])
        dob = str(request.POST['dob'])
        email = str(request.POST['email'])
        pn = str(request.POST['pn'])
        print(name, dob, email, pn)
        if(validateName(name) and validateDob(dob) and validateEmail(email) and validatePN(pn)):
            executor.submit(em.sendEmail)
            return HttpResponse("<title>Registration Successful</title><body><center>Your account is successfully created.</center></body>")
        else:
            messages.info(request, 'Invalid Details')
            return render(request, 'myform.html', {'mymsg':'Invalid Details'})
    elif request.method == 'GET':
        return render(request, 'myform.html')
