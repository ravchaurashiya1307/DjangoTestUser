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
from .models import NewUser, NewForm

email=''
id=0

def login(request):
    if request.method=='POST':
        name = str(request.POST['name'])
        pwd = str(request.POST['password'])
        if(name=='admin' and pwd=='admin'):
            return redirect('/user/')
        else:
            return render(request, 'login.html', {'mymsg':'Invalid Details'})
    elif request.method == 'GET':
        # NewUser.objects.all().delete()
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
    global email, id
    if request.method=='POST':
        em=Email()
        form = NewForm(request.POST, request.FILES)
        a=form.data.dict()
        file=request.FILES['image']
        print(file)
        name = str(a['name'])
        dob = str(a['dob'])
        email = str(a['email'])
        pn = str(a['phone'])
        # print(name, dob, email, pn)
        #
        # print(form.data.dict()['name'])

        if(form.is_valid() and validateName(name) and validateDob(dob) and validateEmail(email) and validatePN(pn)):
            form.save()
            print(form.files.get('image'))
            executor.submit(em.sendEmail)
            b = NewUser.objects.filter(name=name)
            c = b.objects.filter(dob=dob)
            d = c.objects.filter(phone=pn)
            e = d.objects.filter(email=email)
            for x in e:
                data=x
                break
            # return render(request, 'success.html',{'x':form.data.dict(), 'image':file})
            return render(request, 'success.html',{'x':data, 'image':file})
        else:
            messages.info(request, 'Invalid Details')
            return render(request, 'myform.html', {'mymsg':'Invalid Details', 'form':NewForm})
    elif request.method == 'GET':
        return render(request, 'myform.html', {'form':NewForm})


def viewUsers(request):
    a = NewUser.objects.all()
    userDict={}
    i=0
    userDict['name']=[]
    userDict['email']=[]
    userDict['dob']=[]
    userDict['pn']=[]
    for x in a:
        userDict['name'].append(x.name)
        userDict['email'].append(x.email)
        userDict['dob'].append(x.dob)
        userDict['pn'].append(x.phone)
    import pandas as pd
    df=pd.DataFrame(userDict)
    df.to_csv("data.csv")
    return render(request, 'myform2.html', {'data': a})
