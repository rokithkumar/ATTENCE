# ATTENCE
Automated Face Detecting Attendance Marking Web Application

### About
Marking Attendance is a tedious task when done manually. Welcome to Attence, this is a Web Application helps to keep track of Attendance of Students using Face Detection. 

## Features
* Automated Attendance Tracking
* View Attendance Records
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
For complete information about MySQL Configuration please download this [PDF file]()

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
8. Explore more by navigating to all the available tabs, you can refer the XXX File to understand the architecture flow of the Web Appliction.

## Future Works
Face Detection can be spoofed by placing a photo of a person or an image in an mobile in front of the camera. Doing so even the absentees can get marked present   by their classmates. To avoid this we can deploy Liveliness-Test which uses Machine Learning to check whether the face detected is Real or Fake. You can read moreabout the same from this [article.](https://pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/)
