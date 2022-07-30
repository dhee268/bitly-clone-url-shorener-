import string

from django.db import connection
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import random

# Create your views here.
def xyz(request):
    return render(request,"home.html")
def handlingShortUrl(request,**kwargs):
    url= kwargs.get('url')
    cursor=connection.cursor()
    query="select long_link from links where short_link='" + url + "'"
    cursor.execute(query)
    data=cursor.fetchone()
    print(data)
    if data is None:
        return render(request,"home.html")
    else:
        return redirect(data[0])
def signUp(request):
    email=request.POST['email']
    psw=request.POST['psw']
    cursor=connection.cursor()
    query1="select * from users where email='"+email+"'"
    cursor.execute(query1)
    data=cursor.fetchall()
    if(len(data)!=0):
        data = {"email": "already signUp", "password": ""}
        return render(request,"first.html",data)
    else:
        otp=random.randint(100000,999999)
        strotp=str(otp)
        query="insert into users (email, password,otp) values (%s, %s, %s)"
        # query = "select * from city where name= '" + email + "'"
        value=(email,psw,strotp)
        cursor.execute(query,value)
        print(cursor.rowcount)
        body='your otp for our portal you signed up with email '+email+' is ' + strotp
        send_mail('OTP for verification',body,'dheerajkumarjha.2cse23@jecrc.ac.in',['dheerajkumarjha268@gmail.com'])
        data={"email":email}
        return render(request,"signupsuccess.html",data)



def signin(request):
    return render(request,"login.html")


def login(request):
    email = request.POST['email']
    psw = request.POST['psw']
    cursor = connection.cursor()
    # query1 = "select * from users where email='" + email + "'"
    # cursor.execute(query1)
    values=[email,'']
    res=cursor.callproc('signin',values)
    data = cursor.fetchone()
    if data==None:
        data = {"email": "not signUp", "password": ""}
        return render(request, "first.html", data)
    else:
        if data[2] == 0:
            data = {"email": "you are not verified", "password": ""}
            return render(request, "first.html", data)
        if data[1]==psw:
            cursor = connection.cursor()
            query1 = "select * from links where created_by='" + email + "'"
            cursor.execute(query1)
            data = cursor.fetchall()
            data={"data":data}
            return render(request, "afterLogin.html", data)
        else:
            data = {"email": "password is not correct", "password": ""}
            return render(request, "first.html", data)

def otpVerification(request):
    email = request.POST['email']
    otp = request.POST['otp']
    cursor = connection.cursor()
    query1 = "select * from users where email='" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data is not None:
        if data[3] == otp:
            query2 = "update users set is_verify=1 where email='" + email + "'"
            cursor.execute(query2)
            if cursor.rowcount==1:
                print("otp verified success")
                data = {"email": "otp verified success"}
                return render(request, "first.html", data)
        else:
            data = {"email": "otp not verified success"}
            return render(request, "first.html", data)


def generateShortUrl():
    letters=string.ascii_letters + string.digits
    shortUrl=''
    for i in range(6):
        shortUrl=shortUrl+''.join(random.choice(letters))
    return shortUrl



def urlshortner(request):
    longLink=request.GET['link']
    customUrl=request.GET['customurl']
    if customUrl is None or customUrl == '':
        shortUrl=''
    else:
        cursor = connection.cursor()
        query1 = "select * from links where short_link='" + customUrl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        if data is not None:
            data = {"email": "alredy custom url exist try someother url"}
            return render(request, "first.html", data)
        else:
            query2 = "insert into links (long_link,short_link) values (%s, %s)"
            value=(longLink,customUrl)
            cursor.execute(query2,value)
            data = {"email": "your URL is shorten with nano.co/"+customUrl}
            return render(request, "first.html", data)
    if shortUrl is not None or shortUrl !='':
        while True:
            shortUrl=generateShortUrl()
            cursor = connection.cursor()
            query1 = "select * from links where short_link='" + shortUrl + "'"
            cursor.execute(query1)
            data = cursor.fetchone()
            if data is None:#to get the short url
                break
        query2 = "insert into links (long_link,short_link) values (%s, %s)"
        value=(longLink,shortUrl)
        cursor.execute(query2,value)
        data = {"email": "your URL is shorten with nano.co/"+shortUrl}
        return render(request, "first.html", data)

