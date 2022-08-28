# ATTENCE
Automated Face Detecting Attendance Marking Web Application
                        
<img align="right"  alt="ATTENCE-logo" src="https://user-images.githubusercontent.com/75007002/173594644-d01ad716-c98f-47bf-83fa-38af22a9abb2.png">                        
                                                                                                                                          
### About

Marking Attendance is a tedious task when done manually. Welcome to Attence, this is a Web Application helps to keep track of Attendance of Students using Face Detection. 

## Features
* Automated Attendance Tracking
* Track Attendance Records
* Graphical Representations of Attendance Records
* Admin Portal

## Supported Platforms
* Windows
* Linux
* macOS

## Requirements
* Compiler (Recommended: Visual Studio Code)
* MySQL Community Server 8.0.24
* CMake
* Dlib
* Python 3.9

## Installation of Requirements
1. Python 3.9
   * Install Python from this [Link](https://www.python.org/downloads/release/python-396/)
2. CMake
   * Install CMake from this [Link](https://cmake.org/download/)
3. DLib
   * Download dlib-19.22.99-cp39-cp39-win_amd64.whl
   * Run the above file in cmd
4. MySQL
   * Download Windows (x86, 32-bit), MSI Installer from [here](https://downloads.mysql.com/archives/installer/)
   * Then Run the above installed Installer and then please make note of the password.

## Installation of Libraries
Please enter the following commands to download the required libraries
```
  1. opencv
    >> pip install opencv-python
  2. face_recognition
    >> pip install face_recognition
  3. mysql.connector
    >> pip install mysql-connector-python
  4. flask
    >> pip install flask
  5. numpy
    >> pip install numpy
  
```
If any libraries in the App.py is not pre-installed please use "pip install XXXX" here XXXX be the library name in cmd.

## MySQL Configuration
Run the following commands in the MySQL Command Line Client
```
  mysql> create database attendance;
  mysql> use attendance;
  mysql> create table student(regno varchar(10),name varchar(30),UNIQUE(regno,name));
  mysql> create table markattd(regno varchar(10),name varchar(30),date varchar(20),time varchar(10),status varchar(5),UNIQUE(regno,date));
```
For complete information about MySQL Configuration please download this [PDF file](https://drive.google.com/file/d/1mx0s8rqFPvdBk5GFXLMuXOAWUlSJhwIg/view)

## Students List Configuration in the Application
Gather all the pictures of the required persons and name them as Regno-Name for example BE203-Rokith. And Save it to the StudentPhotos Folder

## Admin Login Credentials
Please Enter the following credentials to access the Admin Portal of the Application
```
  Username: admin
  Password: 1234
```

## How to Run the Program
1. Install ATTENCE Folder
2. Open Compiler
3. Say if you are using Visual Code Studio, then open the above installed Folder.
4. Now execute App.py file.
5. If there is no error in your installation, in the terminal you may find the following:
```
 * Serving Flask app 'App' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```
6. Use CTRL + Click the http://127.0.0.1:5000 this will open a brower or manually enter URL- http://127.0.0.1:5000/ in any of your browsers.
7. There you go, You have the Cover page of the ATTENCE Web Application in Front of you.
8. Explore more by navigating to all the available tabs, you can refer this [File](https://drive.google.com/file/d/1YmPsIJM3PCbtMz4i9zIwpm-vNDWGnlp0/view) to understand the architecture flow of the Web Application.

## User Interface

Website Cover Page
https://user-images.githubusercontent.com/75007002/173594410-a888cbde-ee18-4266-b242-9ee9770fd16c.mp4

Website Home Page
https://user-images.githubusercontent.com/75007002/173594468-6b634bef-16ef-4ed7-9e6f-53087ac8e546.mp4

Cover Page
![Cover](https://user-images.githubusercontent.com/75007002/187085351-e21c0025-10f1-4388-8d0f-9d07dbb392f8.png)

Admin Login Page
![Admin Login](https://user-images.githubusercontent.com/75007002/173593402-c1d2b9a6-259c-47d3-b4d6-8f7a6b19aef4.png)

Attendance Tracking Page for Admin
![Attendace Date Admin](https://user-images.githubusercontent.com/75007002/173593664-0688238f-f1c9-42fb-b7de-9abc4ab3d02a.png)

Attendance Tracking Page for Student
![Attendance Student](https://user-images.githubusercontent.com/75007002/173593781-5aab2db6-2793-4544-b862-e83986f9c569.png)

## Future Works
Face Detection can be spoofed by placing a photo of a person or an image in an mobile in front of the camera. Doing so even the absentees can get marked present   by their classmates. To avoid this we can deploy Liveliness-Test which uses Machine Learning to check whether the face detected is Real or Fake. You can read moreabout the same from this [article.](https://pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/)
