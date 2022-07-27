from django.db import connection
from django.shortcuts import render

# Create your views here.
def xyz(request):
    return render(request,"index.html")
def signUp(request):
    email=request.GET['email']
    psw=request.GET['psw']
    cursor=connection.cursor()
    query="insert into users (email, password) values (%s, %s)"
    # query = "select * from city where name= '" + email + "'"
    value=(email,psw)
    cursor.execute(query,value)
    print(cursor.rowcount)
    # row=cursor.fetchone()
    # print(row)
    data={"email":email,"password":psw}
    return render(request,"first.html",data)
