from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import pymysql
from django.core.files.storage import FileSystemStorage

global username, password, contact, email, address


def UserLogin(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    password = row[1]
                    break
        if password != 'none':
            output = '<center><img src="/static/password/'+password+'" alt="" width="400" height="300"  id="myImgId" onmousemove="getPos(event)"/></center>'
            context= {'data':output}
            return render(request, 'ShowAuthenticateImage.html', context)
        if password == 'none':
            context= {'data':'Invalid username'}
            return render(request, 'Login.html', context)


def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Reset(request):
    if request.method == 'GET':
       return render(request, 'Reset.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})


def getSpotValue(spot):
    if not isinstance(spot, str) or not spot.strip():
        print("DEBUG: Received invalid input for spot:", spot)  # Debugging
        return [0, 0]  # Return a default value or handle appropriately

    arr = spot.split(",")
    
    if len(arr) != 2:  # Ensure exactly two elements
        print("DEBUG: Spot does not contain two values:", spot)  # Debugging
        return [0, 0]  # Return a default value or handle appropriately

    try:
        values = [int(arr[0].strip()), int(arr[1].strip())]
    except ValueError:
        print("DEBUG: Spot contains non-integer values:", spot)  # Debugging
        return [0, 0]  # Return a default value or handle appropriately

    return values




def authspots(old_spot, new_spot):
    if not old_spot or not new_spot:
        return False  # Handle None values

    old_x, old_y = old_spot
    new_x, new_y = new_spot

    return (old_x - 10 <= new_x <= old_x + 10) and (old_y - 10 <= new_y <= old_y + 10)

def PasswordAuthAction(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Ensure username is fetched from request

        spot1 = getSpotValue(request.POST.get('t1'))
        spot2 = getSpotValue(request.POST.get('t2'))
        spot3 = getSpotValue(request.POST.get('t3'))
        spot4 = getSpotValue(request.POST.get('t4'))

        if None in (spot1, spot2, spot3, spot4):
            context = {'data': 'Invalid input values'}
            return render(request, 'Login.html', context)

        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='GraphPassword', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT spot1, spot2, spot3, spot4 FROM register WHERE username = %s", (username,))
            row = cur.fetchone()

            if row:
                old_spot1 = getSpotValue(row[0])
                old_spot2 = getSpotValue(row[1])
                old_spot3 = getSpotValue(row[2])
                old_spot4 = getSpotValue(row[3])

                if all(authspots(old, new) for old, new in zip((old_spot1, old_spot2, old_spot3, old_spot4), (spot1, spot2, spot3, spot4))):
                    context = {'data': f'Welcome {username}<br/>Login successful'}
                    return render(request, 'UserScreen.html', context)

        context = {'data': 'Invalid spot selection'}
        return render(request, 'Login.html', context)
           
                    

def PasswordAction(request):
    if request.method == 'POST':
        global username, password, contact, email, address
        spot1 = request.POST.get('t1', False)
        spot2 = request.POST.get('t2', False)
        spot3 = request.POST.get('t3', False)
        spot4 = request.POST.get('t4', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO register(username,password,contact,email,address,spot1,spot2,spot3,spot4) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"','"+spot1+"','"+spot2+"','"+spot3+"','"+spot4+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Signup Process Completed'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Error in signup process'}
            return render(request, 'Register.html', context)     

def RegisterAction(request):
    if request.method == 'POST':
        global username, password, contact, email, address
        username = request.POST.get('t1', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        password = request.FILES['t2'].name
        myfile = request.FILES['t2']
        fs = FileSystemStorage()
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,email FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break
                if row[1] == email:
                    output = email+" Email id already exists"
                    break
        if output == "none":
            fs.save('GraphPasswordApp/static/password/'+password, myfile)
            output = '<center><img src="/static/password/'+password+'" alt="" width="400" height="300"  id="myImgId" onmousemove="getPos(event)"/></center>'
            context= {'data':output}
            return render(request, 'ShowImage.html', context)
        else:
            context= {'data':output}
            return render(request, 'Register.html', context)
    

def ViewUsers(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Username', 'Password Image', 'Contact No', 'Email ID', 'Address', 'Spot1', 'Spot2', 'Spot3', 'Spot4']
        
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>" + font + arr[i] + "</th>"
        
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='GraphPassword', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM register")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>" + font + str(row[1]) + "</td>"  # Username (index 1)
                output += '<td><img src=/static/password/' + str(row[2]) + ' height=100 width=100/></td>'  # Password Image (index 2)
                output += "<td>" + font + str(row[3]) + "</td>"  # Contact No (index 3)
                output += "<td>" + font + str(row[4]) + "</td>"  # Email ID (index 4)
                output += "<td>" + font + str(row[5]) + "</td>"  # Address (index 5)
                output += "<td>" + font + str(row[6]) + "</td>"  # Spot1 (index 6)
                output += "<td>" + font + str(row[7]) + "</td>"  # Spot2 (index 7)
                output += "<td>" + font + str(row[8]) + "</td>"  # Spot3 (index 8)
                output += "<td>" + font + str(row[9]) + "</td>"  # Spot4 (index 9)

        context = {'data': output}        
        return render(request, 'ViewUsers.html', context)

def UpdatePassword(request):
    if request.method == 'POST':
        global username, password
        spot1 = request.POST.get('t1', False)
        spot2 = request.POST.get('t2', False)
        spot3 = request.POST.get('t3', False)
        spot4 = request.POST.get('t4', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update register set password='"+password+"',spot1='"+spot1+"',spot2='"+spot2+"',spot3='"+spot3+"',spot4='"+spot4+"' where username='"+username+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Password Reset Process Completed'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Error in reset password'}
            return render(request, 'Reset.html', context)  


def ResetAction(request):
    if request.method == 'POST':
        global username, password
        password = request.FILES['t1'].name
        myfile = request.FILES['t1']
        fs = FileSystemStorage()
        fs.save('GraphPasswordApp/static/password/'+password, myfile)
        output = '<center><img src="/static/password/'+password+'" alt="" width="400" height="300"  id="myImgId" onmousemove="getPos(event)"/></center>'
        context= {'data':output}
        return render(request, 'ShowResetImage.html', context)
        
def AdminLoginAction(request):
    if request.method == 'POST':
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if user == 'admin' and password == 'admin':
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid login'}
            return render(request, 'AdminLogin.html', context)