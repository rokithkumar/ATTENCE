#------ ATTENCE-AUTOMATED FACE DETECTING ATTENDANCE MARKING APPLICATION DEVELOPED BY ROKITHKUMAR -----

#We import Required Libraries
import cv2
from cv2 import rectangle
from cv2 import putText
from cv2 import VideoCapture
from flask import Flask,render_template,Response
from flask import request
from face_recognition import compare_faces,face_distance
from face_recognition import face_encodings,face_locations
from time import localtime,strftime
import numpy as np
import face_recognition
import os
import datetime
import mysql.connector

#Makes connection with mysql attendance database and inserts all the given parameters in the table markattd
def mysqlinsert(regno,name,date,time,status):
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="Rokith@1234",database="attendance")
    mycursor=mydb.cursor()
    sql="INSERT INTO markattd(regno,name,date,time,status) VALUES(%s,%s,%s,%s,%s)"
    val=(regno,name,date,time,status)
    mycursor.execute(sql,val)
    mydb.commit()

#Makes connection with mysql attendance database and gets count of status using  all the given parameters from the table markattd
def mysqlcountstatus2(date,status):
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="Rokith@1234",database="attendance")
    mycursor=mydb.cursor() 
    sql="SELECT COUNT(status) FROM markattd WHERE date=%s and status=%s"
    val=(date,status)
    mycursor.execute(sql,val)   
    data=mycursor.fetchall()
    return data

#Makes connection with mysql attendance database and gets details of students using  all the given parameters from the table markattd
def mysqlgetstud2(date,status):
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="Rokith@1234",database="attendance")
    mycursor=mydb.cursor() 
    sql="SELECT regno,name FROM markattd WHERE date=%s and status=%s"
    val=(date,status)
    mycursor.execute(sql,val)   
    data=mycursor.fetchall()
    return data

#Makes connection with mysql attendance database and gets count of status using  all the given parameters from the table markattd
def mysqlcountstatus3(name,regno,status):
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="Rokith@1234",database="attendance")
    mycursor=mydb.cursor() 
    sql="SELECT COUNT(status) FROM markattd WHERE name=%s and regno=%s and status=%s"
    val=(name,regno,status)
    mycursor.execute(sql,val)   
    data=mycursor.fetchall()
    return data

#Makes connection with mysql attendance database and gets date using  all the given parameters from the table markattd
def mysqlgetdate(name,regno,status):
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="Rokith@1234",database="attendance")
    mycursor=mydb.cursor() 
    sql="SELECT date FROM markattd WHERE name=%s and regno=%s and status=%s"
    val=(name,regno,status)
    mycursor.execute(sql,val)   
    data=mycursor.fetchall()
    return data

#App Flask
app=Flask(__name__)
def gen():
    #First we gather all the images from folder "StudentPhotos" and store details(name,regno derived from filename) in a list
    path='StudentPhotos'
    images=[]
    Tnames=[]
    myList=os.listdir(path)
    for pic in myList:
        imgx=cv2.imread(f'{path}/{pic}')
        images.append(imgx)
        Tnames.append(os.path.splitext(pic)[0])
        name=[]
        regno=[]
        Snames=[]
        for i in range(len(Tnames)):
            stud=(Tnames[i].split("-"))
            name.append(stud[1])
            regno.append(stud[0])
        for k in name:
            Snames.append(k)
    #Store the details of student regno as key and name as value in an dictionary
    studdict=dict(zip(regno,name))
    #We store the student details in a seperate table student having columns regno and name
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="Rokith@1234",database="attendance")
    mycursor=mydb.cursor()
    #We gather existing students details in the student table
    mycursor.execute("select regno from student")
    data=mycursor.fetchall()
    available=[]
    for ele in data:
        available.append(ele[0])
    #Remove above existing students from list containing all the student details
    toadd=set(regno).difference(available)
    #Then we add only new student which are not avilable in the student table to a list
    letsadd=[]
    for k in toadd:
        letsadd.append(k)
    #Then we Insert those students into the student table
    for k in range(len(letsadd)):
        sql="INSERT INTO student(regno,name) VALUES(%s,%s)"
        val=(letsadd[k],studdict[letsadd[k]])
        mycursor.execute(sql,val)
        mydb.commit()

    #Function which will find the encodings of all the available images
    def FindEncodings(images):
        encodeList=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    #The function MarkAbsent marks the absentees of the previous day
    #This below function will take regno and name as input
    #This function inserts student details and current date and time and status as "A" into mysql-markattd table
    def MarkAbsent():
        mydb=mysql.connector.connect(host="localhost",user="root",passwd="Rokith@1234",database="attendance")
        mycursor=mydb.cursor()
        now=datetime.datetime.today()-datetime.timedelta(days=3)
        fordate=now.strftime('%d-%m-%y')
        t=localtime()
        current_time = strftime("%H:%M:%S",t)
        mycursor.execute("""select regno from markattd where date=%s""",(fordate,))
        data=mycursor.fetchall()
        pres=[]
        for ele in data:
            pres.append(ele[0])
        for t in range(len(Snames)):
            Snames[t]=Snames[t].upper()
        abs=set(regno).difference(pres)
        absente=[]
        for i in abs:
            absente.append(i)
        for l in range(len(absente)):
            mysqlinsert(absente[l],studdict[absente[l]].upper(),fordate,current_time,"A")

    #The function MarkPresent will mark the students who are present in the given date
    #This below function will take regno and name as input and return result(int) 
    #This function inserts student details and current date and time and status as "P" into mysql-markattd table
    def MarkPresent(regnum,name):
        #We try to insert the student's status
        try:
            now=datetime.datetime.today()
            fordate=now.strftime('%d-%m-%y')
            t=localtime()
            current_time = strftime("%H:%M:%S",t)
            mysqlinsert(regnum,name,fordate,current_time,"P")
            return 0
        #If any error occurs like already marked present as we have the unique(regno,name) in markattd table in mysql
        #So we can't mark the same student same date twice in the markattd table so we return 1
        except:
            error="You are Marked present"
        return 1

    #We get the Encodings of the Students Faces Available in our Application Resource
    ListofEncoded=FindEncodings(images)
    #We mark the absentees of the previous day
    MarkAbsent()
    cap=VideoCapture(0)
    process_frame=True
    #We use these lists to store face locations,face names and found face encodings
    list_faceloc=[]
    list_facenames=[]
    list_faceencod=[]
    cur_frame=True
    while(1):
        ret,img=cap.read()
        newimg=cv2.resize(img,(0,0),None,0.25,0.25)
        newimg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        #Check every alternate frame or frame number which is even
        if cur_frame:
            list_faceloc=face_locations(newimg)
            list_faceencod=face_encodings(newimg,list_faceloc)
            list_facenames=[]
            for enocdeFace in list_faceencod:
                matches=compare_faces(ListofEncoded,enocdeFace)
                name="Unkown"
                faceDis=face_distance(ListofEncoded,enocdeFace)
                #Find the best Match from available List of encoded faces
                matchIndex=np.argmin(faceDis)
                dispname=name
                if matches[matchIndex]:
                    name=Snames[matchIndex].upper()
                    regnum=regno[matchIndex]
                    #We call the MarkPresent function to mark the status of above detected student
                    res=MarkPresent(regnum,name)
                    now=datetime.datetime.today()
                    fordate=now.strftime('%d-%m-%y')
                    paths="ImagesTaken"
                    #We change the display name from "NAME" TO "NAME-PRESENT" if the student has been marked present
                    if res==1:
                        img_name=fordate+"-"+regnum+"-"+name+".png"
                        cv2.imwrite(os.path.join(paths,img_name), img)
                        dispname=name+"-PRESENT"
                    else:
                        dispname=name
                #We add the above detected name to the list in which names of students detected in current frame are available
                list_facenames.append(dispname)
        cur_frame=not cur_frame

        #In all detected faces and names we display them in the video source by marking a rectangle around their face
        #with their name at the bottom and status at the top
        for (top,right,bottom,left),name in zip(list_faceloc,list_facenames):
            rectangle(img,(left,top),(right,bottom),(0,255,0),2)
            #Once marked present it displays "PRESENT" on top of detected face in order to inform students
            #that they have been marked Present
            if "-PRESENT" in name:
                displays=name.split("-")
                rectangle(img,(left,top-35),(right,top),(0,255,0),cv2.FILLED)
                putText(img,displays[1],(left+6,top-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
                rectangle(img,(left,bottom-35),(right,bottom),(0,255,0),cv2.FILLED)
                putText(img,displays[0],(left+6,bottom-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
            #Before marking him/her present it only displays thier(student) name
            else:
                rectangle(img,(left,bottom-35),(right,bottom),(0,255,0),cv2.FILLED)
                putText(img,name,(left+6,bottom-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        #Sends all the frames to the attendance.html where it displays this captured video Source
        ret,buffer=cv2.imencode('.jpeg',img)
        img=buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+img+b'\r\n\r\n')

#This View function(index) will returns the web respone which is cover page(cover.html) once the App.py is Executed
@app.route('/')
def index():
    return render_template('cover.html')

#This View function(base) will return home page(index.html) whenever Home Tab is Pressed
@app.route('/home')
def base():
    return render_template('index.html')

#This View function(attendance) will return (attendance.html) whenever Attendance Tab is Pressed
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

#This View function(update) will return (display.html) whenever Update Tab is Pressed
@app.route('/update')
def update():
    return render_template('display.html',e="UPDATE",d="Coming Soon",r="Page Under Construction")

#This View function(student) will return (student.html) whenever Student Tab is Pressed
@app.route('/student')
def student():
    return render_template('student.html')

#The below function helps us to create a dictionary of student's details here regno is key and name is value
namel=[]
regnol=[]
def createdict():
    path='StudentPhotos'
    images=[]
    Tnames=[]
    myList=os.listdir(path)
    for cl in myList:
        imgx=cv2.imread(f'{path}/{cl}')
        images.append(imgx)
        Tnames.append(os.path.splitext(cl)[0])
        Snames=[]
        for i in range(len(Tnames)):
            stud=(Tnames[i].split("-"))
            namel.append(stud[1])
            regnol.append(stud[0])

#The view function(showattendance) returns the attendance records of a particular student by redirecring to showattd.html page 
@app.route('/showattendance',methods=['POST'])
def showattendance():
    #we call the createdict function
    createdict()
    #Take name and regno as input from user using HTML Form in student.html page
    name=request.form['name']
    regnom=request.form['regnom']
    #We convert the input received to upper case eventhough we print the "inputs are case sensitive" below the form to make
    #it easy for user and to ease the comparision as the details are in uppercase in the backend(mysql)

    #Here we check the presence of the input recevied in the above created dictionary
    for i in range(len(regnol)):
        if regnol[i].upper()==regnom.upper():
            if namel[i].upper()==name.upper():
                flag=1
                break
        else:
            flag=0

    name=name.upper()
    regnom=regnom.upper()
    if flag==1:
        #We get the count of days on which the above student is Present
        data=mysqlcountstatus3(name,regnom,"P")
        for ele in data:
            totalpresent=ele[0]

        #We get the dates on which the above student is Present
        data=mysqlgetdate(name,regnom,"P")
        presentdate=[]
        for ele in data:
            for i in ele:
                presentdate.append(i)

        #We create a dictionary to store the present details of the above student making date as key and status as value
        summary={}
        for k in range(len(presentdate)):
            summary[presentdate[k]]="Present"

        #We get the count of days on which the above student is Absent
        data=mysqlcountstatus3(name,regnom,"A")
        for ele in data:
            totalabsent=ele[0]

        #We get the dates on which the above student is Absent
        data=mysqlgetdate(name,regnom,"A")
        absentdate=[]
        for ele in data:
            for i in ele:
                absentdate.append(i)
        
        #We add the absent details of the above given student where already the present details are available
        for k in range(len(absentdate)):
            summary[absentdate[k]]="Absent"
        #So basically this dict summary contains the dates as key and status("Present"/"Absent") as values for given student

        #We sort the dict on  the basis of date(key) in ascending order
        dictionary1 = sorted(summary)
        sort_summary = {key:summary[key] for key in dictionary1}
        totaldays=totalpresent+totalabsent
        
        #We create a dictionary date to store the absent and present count for the pie chart
        data = {'Status' : 'Number of Days', 'Present' : totalpresent, 'Absent' : totalabsent}
        return render_template('showattd.html',n=name,r=regnom,p=totalpresent,a=totalabsent,t=totaldays,pd=presentdate,ad=absentdate,data=data,sumry=sort_summary)
    
    #If the credentials are invlaid it returns display.html showing that the student's details are invalid
    elif flag==0:
        return render_template('display.html',e="Error",d="Student Details seems to be Incorrect",r="Please check the Student's Name and Registration Number")

#This View function(video_feed) will return Video Source(Response) whenever Attendance Tab is Pressed
@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace;boundary=frame')

#This View function(admin) will return Admin Login Page(adminlogin.html) whenever Admin Tab is Pressed
@app.route('/admin')
def admin():
    return render_template('adminlogin.html')

#This View function(adminpage) will return Admin Page(admin.html) whenever Admin Login form is filled with valid Credentials
@app.route('/adminpage',methods=['POST'])
def getadmin():
    username=request.form['username']
    password=request.form['pass']
    if username=="admin" and password=="1234":
        return render_template('adminpage.html',rest="")
    #If Invalid Credentials Then it returns Error Page(display.html) showing the Credentials are Invalid
    else:
        return render_template('display.html',e="Error",d="Invalid Credentials",r="Please Check Your Credentials")
    
#This View function(adminresult) will return Attendance records of an particular date which is given as input
#by the Admin on the admin.html page
@app.route('/adminresult',methods=['POST'])
def adminresult():
        date=request.form['date']
        if len(date)==0:
            title="Please Select the Date First"
            return render_template('adminresult.html',head=title,data=data) 
        else:
            #First we change the received input(date) from the admin.html page into our required format
            #Change String(date) Format from "YYYY-MM-DD" to "DD-MM-YY"
            print(date)
            tempdate=[]
            attddate=""
            k=len(date)
            for i in reversed(range(len(date))):
                tempdate.append(date[i])
            for j in tempdate:
                attddate=attddate+j
            attddate=list(attddate)
            attddate[0],attddate[1]=attddate[1],attddate[0]
            attddate[3],attddate[4]=attddate[4],attddate[3] 
            finaldate=""      
            for k in range(len(attddate)-2):
                finaldate=finaldate+attddate[k]

            #Gets the Count of Students Present on a Particular Date
            data=mysqlcountstatus2(finaldate,"P")
            for ele in data:
                totalpresent=ele[0]

            #Gets the Details of Students Present on a Particular Date
            stdpresentregno=[]
            stdpresentname=[]
            data=mysqlgetstud2(finaldate,"P")
            for ele in data:
                stdpresentregno.append(ele[0])
                stdpresentname.append(ele[1])

            #Gets the Count of Students Absent on a Particular Date
            data=mysqlcountstatus2(finaldate,"A")
            for ele in data:
                totalabsent=ele[0]

            #Gets the Details of Students Absent on a Particular Date
            data=mysqlgetstud2(finaldate,"A")
            stdabsentregno=[]
            stdabsentname=[]
            for ele in data:
                stdabsentregno.append(ele[0])
                stdabsentname.append(ele[1])
                
            #Creating a Dictionary(present,absent) to store students details as regno as key and name as value as per the status
            present={}
            absent={}
            for key in  stdpresentregno: 
                for value in stdpresentname:
                    present[key]=value
                    stdpresentname.remove(value)
                    break
            for key in  stdabsentregno: 
                for value in stdabsentname:
                    absent[key]=value
                    stdabsentname.remove(value)
                    break
            #So here above we have students details who were present on above given date in present dictionary
            # and similarly for the absent dictionary

            totalstud=totalabsent+totalpresent
            title="Attendace Record of the Day: "+finaldate
            error="Attendance Record of the Day "+finaldate+" is Currently Unvailable"
            total="Total Number of Students: "+str(totalstud)
            pres="Number of Students who were Present: "+str(totalpresent)
            abs="Number of Students who were Absent: "+str(totalabsent)
            data = {'Status' : 'Number of Students', 'Present' : totalpresent, 'Absent' : totalabsent}

            #If total number of students count not equal to 0 then  return the attendance records of the particular date
            if totalstud!=0:
                return render_template('adminresult.html',head=title,tot=total,pres=pres,abs=abs,data=data,present=present,absent=absent)
            #If the total number of students present is zero then we may display that the attendance for that particular
            #date has not been marked yet
            else:
                return render_template('adminresult.html',head=error,data=data,present=present,absent=absent)    

#This View function(upload) will return (upload.html) whenever Admin Wants to Add a new Student
@app.route('/upload')
def upload():
    return render_template('upload.html')
ALLOWED_EXTENSIONS={'jpg','jpeg','png','JPG','JPEG','PNG'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#This View function(addnew) will return (upload.html) with Custom  Display messages
# everytime a File is Uploaded in the upload.html page
@app.route('/addnew',methods=['POST','GET'])
def addnew():
    if request.method=='POST':
        message2="Please Check the File Name"
        message3="Filename Format: Regno-Name, Example: BE201-Obama"
        file=request.files['file']
        filename=file.filename
        #Using If-Else to check the Upload File Name Format(Required 'BEXXX-Name' here X needs to be a Digit) Ex. BE203-Rokith
        if filename=='':
            message1="Error! Filename is Empty"
            return render_template('upload.html',status=message1,sol=message2,formt=message3)
        if filename[0]=='B' and filename[1]=='E' and filename[2].isdigit()  and filename[3].isdigit()  and filename[4].isdigit()  and allowed_file(filename):
            file.save(os.path.join("StudentPhotos",filename))
            message1="File Uploaded Sucessfully"
            message2="Please Close this Tab and Navigate back to Admin Page"
            return render_template('upload.html',status=message1,formt=message2)
        if allowed_file(filename)!=True:
            message1="Wrong File Type"
            message3="Allowed File Types: .jpeg .jpg .png"
            message2="Please make sure that file is a Picture"
            return render_template('upload.html',status=message1,sol=message2,formt=message3)
        else:
            print(filename)
            print(filename.rsplit('.', 1)[1])
            message1="Wrong File Name"
            return render_template('upload.html',status=message1,sol=message2,formt=message3)

if __name__=='__main__':
    app.run(debug=True)

#---------------- END OF Appy.py PROGRAM CODE ----------------

