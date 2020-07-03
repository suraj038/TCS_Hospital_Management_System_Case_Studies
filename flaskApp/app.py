# import all the eseentials libraries
from flask import Flask,request,render_template,flash,redirect,url_for,session,logging
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import date
import json
import math
import os

app=Flask(__name__)
# Configure Database
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="Hospital"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

# Route for the Login Page
@app.route('/',methods=['GET','POST'])
def home():
    session['login']=False
    session['update']=True
    if request.method=='POST':
        username=request.form['username']
        passo=request.form['password']
        cur=mysql.connection.cursor()
        result=cur.execute("select * from userstore  where username=%s",[username])
        if result>0:
            data=cur.fetchone()
            if data['password']==passo:
                session['login']=True
                return redirect(url_for('mainpage'))
            else:
                return render_template('login.html',error="Invalid Username and Password")
        else:
            return render_template('login.html',error="Please enter your valid username and password")
    return render_template('login.html')

# Route for patient creation page
@app.route('/create',methods=['GET','POST'])
def create():
    if request.method=="POST":
        details=request.form
        ssn=details['id']
        name=details['name']
        age=details['age']
        admission=details['admission']
        bed=details['bed']
        address=details['address']
        state=details['stt']
        city=details['city']
        status=details['status']
        cur = mysql.connection.cursor()
        # SQL Queries
        cur.execute("INSERT INTO patients VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (None, name, age, admission, bed, address, city, state, status))
        mysql.connection.commit()
        cur.close()
        return render_template('create.html', message="Patient's Registered Successfully")
    return render_template('create.html')

# Route for mainpage
@app.route('/mainpage',methods=['GET','POST'])
def mainpage():
    return render_template('mainpage.html')

# Route for Patient Update Page
@app.route('/update',methods=['POST','GET'])
def update():
    if request.method=='POST' and request.form['btn']=='Get':
        session['update']=False
        Form=request.form
        sid=request.form['id']
        cur=mysql.connection.cursor()
        # SQL Queries
        result=cur.execute("select * from patients where PatientID=%s",[sid])
        mysql.connection.commit()
        if(result>0):
            data=cur.fetchone()
            cur.close()
            Form.id=int(data['PatientID'])
            Form.name=data['PatientName']
            Form.age=int(data['Age'])
            Form.admission=data['DateofAdmission']
            Form.bed=data['Typeofbed']
            Form.address=data['Address']
            Form.stt=data['State']
            session['state']=data['State']
            Form.city=data['City']
            Form.status=data['Status']
            return render_template("update.html",form=Form)
        else:
            session['update']=True
            return render_template('update.html', error="Invalid Patient ID")
    if request.method=="POST" and request.form['btn']=='Update':
        session['update']=True
        details=request.form
        ssn=details['id']
        name=details['name']
        age=details['age']
        admission=details['admission']
        bed=details['bed']
        address=details['address']
        state=details['stt']
        if state=="":
            state=session['update']
            session.pop('state')
        city=details.get('city')
        status=details['status']
        cur=mysql.connection.cursor()
        check = cur.execute("UPDATE patients SET PatientName = %s, Age = %s, DateofAdmission=%s, Typeofbed=%s, Address = %s, State=%s, City=%s, Status = %s where PatientID = %s", ( name, age, admission, bed, address, state, city, status, ssn))
        mysql.connection.commit()
        if(check>0):
            mysql.connection.commit()
            cur.close()
            return render_template("update.html", updated="Patients Data Updated Successfully")
        else:
            return render_template("update.html",error="Invalid Patient ID, Sorry!")
    return render_template('update.html')

# Route for patient Delete Page
@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=='POST' and request.form['btn']=="Get":
        session['update']=False
        Form=request.form
        sid=request.form['id']
        cur=mysql.connection.cursor()
        # SQL Queries
        result=cur.execute("select * from patients where PatientID=%s",[sid])
        mysql.connection.commit()
        
        if(result>0):
            data=cur.fetchone()
            cur.close()
            Form.id=int(data['PatientID'])
            Form.name=data['PatientName']
            Form.age=int(data['Age'])
            Form.admission=data['DateofAdmission']
            Form.bed=data['Typeofbed']
            Form.address=data['Address']
            Form.stt=data['State']
            Form.city=data['City']
            Form.status=data['Status']
            return render_template('delete.html',form=Form)
        else:
            return render_template('delete.html',error="Invalid Patient Id, Sorry!")

    if request.method=='POST' and request.form['btn']=='Delete':
        session['update']=True
        sid=request.form['id']
        cur=mysql.connection.cursor()
        # SQL Queries
        result=cur.execute("delete from patients where PatientID=%s",[sid])
        mysql.connection.commit()
        cur.close()
        if result>0:
            return render_template('delete.html',deleted="Patient Removed/Deleted Successfully")
        else:
            return render_template('delete.html',error="Something Went Wrong, Try Again!!!")
    return render_template('delete.html')

# Route for viewing all the patients who are ACTIVE
@app.route('/view')
def view():
    cur=mysql.connection.cursor()
    # SQL Queries
    result=cur.execute("select * from patients where Status=%s",["Active"])
    data=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if result>0:
        return render_template('view.html',data=data)
    else:
        return  render_template("view.html",error="No Patient's Found, Sorry!")

# Route for Patient Search Page
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST' and request.form['btn']=='search':
        Form=request.form
        sid=request.form['id']
        cur=mysql.connection.cursor()
        # SQL Queries
        result=cur.execute("select * from patients where PatientID=%s",[sid])
        mysql.connection.commit()
        if(result>0):
            data=cur.fetchone()
            cur.close()
            Form.id=int(data['PatientID'])
            Form.name=data['PatientName']
            Form.age=int(data['Age'])
            Form.admission=data['DateofAdmission']
            Form.bed=data['Typeofbed']
            Form.address=data['Address']
            Form.stt=data['State']
            Form.city=data['City']
            Form.status=data['Status']
            return render_template('search.html',form=Form, search="Patient Found, Success!")
        else:
            return render_template('search.html',error="Invalid Patient ID / Patient Not found, Sorry!")
    return render_template('search.html')

# Route for getting all the patients with issued medicines
@app.route('/patientmedicine',methods=['GET','POST'])
def patientmedicine():
    data=""
    if request.method=='POST' :
        sid=int(request.form['id'])
        session['username']=sid
        cur=mysql.connection.cursor()
        cur1=mysql.connection.cursor()
        # SQL Queries
        result=cur.execute("select * from patients where PatientID=%s",[sid])
        cur1.execute("select a.MedicineName,b.QuantityIssued,a.Rateofmedicine from medicine_master  a,tracking_medicines b where a.MedicineID=b.IDofMedicineIssued and b.PatientID=%s",[sid])       
        data=cur.fetchone()
        data1=list(cur1.fetchall())
        print(data1)
        mysql.connection.commit()
        cur1.close() 
        cur.close()
        print(data1)
        if result>0:
            return render_template('patientmedicine.html',data=data,data1=data1)
        else:
            return render_template('patientmedicine.html',error="Invalid PatientID, Sorry!",data=data)
    return render_template('patientmedicine.html',data=data)

# Route for Issuing the medicines to patients
@app.route('/issuemedicine',methods=['GET','POST'])
def issuemedicine():
    if request.method=='POST' and request.form['btn']=="search":
        session['iss']=True
        Form=request.form
        name=request.form['name']
        amount=int(request.form['quantity'])
        cur=mysql.connection.cursor()
        # SQL Queries
        result=cur.execute("select MedicineName,QuantityAvailable ,Rateofmedicine from medicine_master where MedicineName=%s",[name])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if(result>0):
            if int(data['QuantityAvailable'])>=amount:
                m=dict()
                m['rate']=data['Rateofmedicine']
                m['amnt']=amount*int(data['Rateofmedicine'])
                Form.name=name
                Form.quantity=amount
                return render_template('issuemedicine.html',m=m,form=Form)
                
            else:
                error="Expected Quantity Unavailable, sorry! Total no. of quantity available is "+str(data['QuantityAvailable'])
                return render_template('issuemedicine.html',error=error)
        else:
            error="Sorry! Medicine Name Invalid"
            return render_template('issuemedicine.html',error=error)
    if request.method=='POST' and request.form['btn']=="issue":
        amant=request.form['quantity']
        name=request.form['name']
        cur=mysql.connection.cursor()
        result=cur.execute("select QuantityAvailable,MedicineID from  medicine_master where MedicineName=%s",[name])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if result>0:
            amnt=int(data['QuantityAvailable'])-int(amant)
            cur=mysql.connection.cursor()
            cur.execute("update medicine_master set QuantityAvailable=%s where MedicineName=%s",[amnt,name])
            mysql.connection.commit()
            cur.close()
            cur=mysql.connection.cursor()
            cur.execute("insert into tracking_medicines values(%s,%s,%s)",(session['username'],data['MedicineID'],amant))
            mysql.connection.commit()
            cur.close()
            session['iss']=False
            return render_template("issuemedicine.html")
        else:
            return render_template("issuemedicine.html", error="Please confirm the availability of medicines!")
        
    if request.method=='POST' and request.form['btn']=="update":
        if session['iss']!=False:
            amant=request.form['quantity']
            name=request.form['name']
            cur=mysql.connection.cursor()
            result=cur.execute("select QuantityAvailable,MedicineID from  medicine_master where MedicineName=%s",[name])
            data=cur.fetchone()
            mysql.connection.commit()
            cur.close()
            if result>0:
                amnt=int(data['QuantityAvailable'])-int(amant)
                cur=mysql.connection.cursor()
                cur.execute("update medicine_master set QuantityAvailable=%s where MedicineName=%s",[amnt,name])
                mysql.connection.commit()
                cur.close()
                cur=mysql.connection.cursor()
                cur.execute("insert into tracking_medicines values(%s,%s,%s)",(session['username'],data['MedicineID'],amant))
                mysql.connection.commit()
                cur.close()
                session['iss']=False
                session['username']="somethingelse"
                return render_template('mainpage.html',medicine="Medicines Issued Successfully!")
        else:
                session['iss']=False
                session['username']="somethingelse"
                return render_template('mainpage.html',medicine="Medicines Issued Successfully!")
    return render_template('issuemedicine.html')

# Route for getting all the Patients with Test Name and Quantity
@app.route('/patientdiagnostic',methods=['GET','POST'])
def patientdiagnostic():
    data=""
    if request.method=='POST' :
        sid=int(request.form['id'])
        session['diagnostic']=sid
        cur=mysql.connection.cursor()
        cur1=mysql.connection.cursor()
        # SQL Queries
        result=cur.execute("select * from patients where PatientID=%s",[sid])
        cur1.execute("select a.TestName,a.Chargefortest from diagnostics_master a,tracking_diagnostics b where a.TestID=b.TestID and b.PatientID=%s",[sid])       
        data=cur.fetchone()
        data1=list(cur1.fetchall())
        print(data1)
        mysql.connection.commit()
        cur1.close() 
        cur.close()
        print(data1)
        if result>0:
            return render_template('patientdiagnostic.html',data=data,data1=data1)
        else:
            return render_template('patientdiagnostic.html',error="Invalid PatientID, Sorry!",data=data)
    return render_template('patientdiagnostic.html',data=data)

# Route for adding new Test Name for particular Patients
@app.route('/diagnostics',methods=["GET","POST"])
def diagnostic():
    data=""
    l=list()
    cur=mysql.connection.cursor()
    cur.execute("select * from diagnostics_master")
    data=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    for i in data:
        l.append(i['TestName'])
    
    if request.method=="POST" and request.form['btn']=="search1":
        n=list()
        name=request.form['id']
        cur=mysql.connection.cursor()
        # SQL Query
        result=cur.execute("select * from diagnostics_master where TestName=%s ",[name])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if result>0:
            session['up']=True
            render_template("diagnostics.html",data=data)
        else:
            return render_template("diagnostics.html", error="Test Name Invalid!", data=data, l=l)
    if request.method=="POST" and request.form['btn']=="add":
        testname=str(request.form["id"])
        cur=mysql.connection.cursor()
        # SQL Query
        result=cur.execute("select * from diagnostics_master where TestName=%s",[testname])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if result>0:
            cur=mysql.connection.cursor()
            # SQL Query
            cur.execute("insert into tracking_diagnostics values(%s,%s)",(session['diagnostic'],data['TestID']))
            mysql.connection.commit()
            cur.close()
            session['up']=False
            return render_template('diagnostics.html',l=l,data="")
        else:
            error=error="Sorry! Test ID Not Found"
            return render_template('diagnostics.html',l=l,data=data,error=error)
    
    if request.method=='POST' and request.form['btn']=="update":
        if session['up']!=False:
            testname=str(request.form["id"])
            cur=mysql.connection.cursor()
            # SQL Query
            result=cur.execute("select * from diagnostics_master where TestName=%s",[testname])
            data=cur.fetchone()
            mysql.connection.commit()
            cur.close()
            if result>0:
                cur=mysql.connection.cursor()
                # SQL Query
                cur.execute("insert into tracking_diagnostics values(%s,%s)",(session['diagnostic'],data['TestID']))
                mysql.connection.commit()
                cur.close()
                session['diagnostic']=False
                session['username']="somethingelse"
                session.pop('diagnostic')
                return render_template('mainpage.html',diagnostic="Diagnostic Added Successfully!")
        else:
                session['username']="somethingelse"
                session.pop('diagnostic')
                return render_template('mainpage.html',diagnostic="Diagnostic Added Successfully!")

    return render_template('diagnostics.html',l=l,data=data)

# Route for Fianl Billing for patient who is going to be Status="DISCHARGE"
@app.route('/finalbilling',methods=['GET','POST'])
def finalbilling():
    data=""
    sum1=0
    sum2=0
    sum=0
    num=0
    d={'General':2000,'Shared':4000,'Single':8000}
    dat=""
    if request.method=='POST' and request.form['btn']=="search":
        id=request.form['id']
        cur=mysql.connection.cursor()
        # SQL Query
        result=cur.execute("select * from patients where PatientID=%s",[id])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        
        if result>0:
            # Difference between "Date of joining" and "Date of Discharge"
            date2=str(date.today())
            date1=str(data['DateofAdmission'])
            date2=date2.split('-')
            date1=date1.split('-')
            date2=date(int(date2[0]),int(date2[1]),int(date2[2]))
            date1=date(int(date1[0]),int(date1[1]),int(date1[2]))
            var=str(date2-date1)
            var=var.split(' ')
            if len(var)>1:
                var1=int(var[0])
                var2=d[data['Typeofbed']]
                sum=var1*var2
                num=var1
            cur=mysql.connection.cursor()
            # SQL Query
            cur.execute("select a.MedicineName, b.QuantityIssued ,a.Rateofmedicine from medicine_master a,tracking_medicines b where a.MedicineId=b.IDofMedicineIssued and b.PatientID=%s",[id])
            data1=cur.fetchall()
            mysql.connection.commit()
            cur.close()
            for i in data1:
                sum1+=int(i['QuantityIssued'])*int(i['Rateofmedicine'])
            cur=mysql.connection.cursor()
            # SQL Query
            cur.execute("select b.TestName,b.Chargefortest from  diagnostics_master b,tracking_diagnostics a where a.TestID=b.TestID and a.PatientID=%s",[id])
            data2=cur.fetchall()
            mysql.connection.commit()
            cur.close()
            for i in data2:
                sum2+=int(i['Chargefortest'])
            return render_template('finalbilling.html',data=data,data1=data1,data2=data2,sum=sum,sum1=sum1,sum2=sum2,date2=date2,num=num)
        else:
            return render_template("finalbilling.html", data=data, error="Sorry! Patient ID Not Found")

    if request.method=="POST" and request.form['btn']=="confirm":
        id=request.form['id']
        cur=mysql.connection.cursor()
        # SQL Query
        cur.execute("delete from patients where PatientID=%s",[id])
        mysql.connection.commit()
        cur.close()
        return render_template('mainpage.html',finalbilling="Patient Discarged Sucessfully!")

    return render_template('finalbilling.html',data=data)


if __name__=='__main__':
    app.secret_key="suraj"
    app.run(debug=True)