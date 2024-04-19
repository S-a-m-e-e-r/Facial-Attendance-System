from tkinter import *
from tkinter import messagebox
import time
import cv2
import numpy as np
import face_recognition
import pickle
import os
from datetime import datetime
def start():

    data = pickle.loads(open('encodings', "rb").read())
    encodeListKnown = data["encodings"]
    classNames = data["names"]

    def markAttendance(name):
        now=datetime.now()
        d=now.strftime('%d/%m/%y')
        x=d.replace('/','_')
        x=('Attendance_' + x + '.csv')
        file='Sheets_Attendance/'+x
        with open('Sheets_Attendance/'+x, 'a') as f:
            pass
        with open(file,'r+') as f:
            myDataList=f.readlines()
            nameList=[]
            for line in myDataList:
                entry=line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now=datetime.now()
                dtstring = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtstring}')

    cap=cv2.VideoCapture(0)
    while True:
        success,img=cap.read()
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            print(faceDis)
            matchIndex=np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                y1,x2,y2,x1=faceLoc
                y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)

        cv2.imshow('Webcam',img)
        k=cv2.waitKey(20)
        if k==27:#press escape key to close the cam.read()
            break
    cap.release()
    cv2.destroyAllWindows()


def add():

    path = 'Images_Show'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImage = cv2.imread(f'{path}/{cl}')
        images.append(curImage)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(images):
        encodeList=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            print(img)
            encode=face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    msg = messagebox.showinfo('Information', "Be patient until we update your Dataset you will get a message after updation\n So, donot press any key")
    encodelistknown = findEncodings(images)
    print("Dataset is Updated")
    msg=messagebox.showinfo('Information',"Database Updated Successfully")
    data = {"encodings": encodelistknown, "names": classNames}
    f = open("\encodings", "wb")
    f.write(pickle.dumps(data))
    f.close()
    cv2.destroyAllWindows()

#photo=PhotoImage(file=".\Images_Show\Face.png")

root=Tk()
root.title("HOME PAGE")
#root.iconphoto(False,photo)
mywidth=1024
def disable_event():
    Msgbox = messagebox.askquestion('Exit Application', 'Are you sure , You want to exit the application')
    if Msgbox == 'yes':
        sys.exit()
    else:
        pass
root.protocol("WM_DELETE_WINDOW",disable_event)
root.resizable(0,0)
myheight=600
scrwidth=root.winfo_screenwidth()
scrheight=root.winfo_screenheight()
xLeft=int((scrwidth/2)-(mywidth/2))
yTop=int((scrheight/2)-(myheight/2))
root.geometry(str(mywidth)+ "x" +str(myheight)+"+"+str(xLeft)+"+"+str(yTop))


#-----------------new window-------------------------


def start_now():
    start()

def exit_now():
    Msgbox = messagebox.askquestion('Exit Application', 'Are you sure , You want to exit the application')
    if Msgbox == 'yes':
        sys.exit()
    else:
        pass

def file_now():
    now = datetime.now()
    d = now.strftime('%d/%m/%y')
    x = d.replace('/', '_')
    x = ('Attendance_' + x + '.csv')
    file = 'Sheets_Attendance/' + x
    open=os.system("start excel.exe "+file)

def open_file_now():
    #copy the file location of your image folder
    o1=os.startfile("Images_Show")
    Msgbox = messagebox.askquestion('Update Dataset', '''You have opened the file so you need to update the Dateset\n Click 'YES' to update''')
    if Msgbox == 'yes':
        add()
    else:
         messagebox.showinfo('Information', 'Dataset is not upto date, so the the updates in the File will no be affected to your Dataset')
def openNewWindow():
    root.withdraw()
    root1=Toplevel(root)
    root1.title("ADMIN PAGE")

    def disable_event():
        Msgbox = messagebox.askquestion('Exit Application', 'Are you sure , You want to exit the application')
        if Msgbox == 'yes':
            sys.exit()
        else:
            pass

    root1.protocol("WM_DELETE_WINDOW", disable_event)
    root1.resizable(0, 0)
    #root.iconphoto(False, photo)
    bg1 = PhotoImage(file="pictures/AdminPanel.png")
    root1.geometry(str(mywidth) + "x" + str(myheight) + "+" + str(xLeft) + "+" + str(yTop))
    # Create Canvas
    canvas2 = Canvas(root1, width=1024,
                     height=600)

    canvas2.pack(fill="both", expand=True)
    canvas2.create_text(1024, 600 )

    # Display image
    canvas2.create_image(0, 0, image=bg1, anchor="nw")
    add = PhotoImage(file="pictures/AddButton.png")
    f = PhotoImage(file="pictures/FileButton.png")
    b= PhotoImage(file="pictures/BackButton.png")


    # Create Buttons
    button2 = Button(root1, text="Add",image=add,command=open_file_now)
    button2["bg"]="white"
    button2["border"]="0"
    button2.pack()
    button3 = Button(root1, text="Add",image=f,command=file_now)
    button3["bg"]="white"
    button3["border"]="0"
    button3.pack()
    def show():
        root.deiconify()
        root1.withdraw()
    button6 = Button(root1, text="Exit",image=b,command=show)
    button6["bg"] = "white"
    button6["border"] = "0"
    #button6.pack()

    # Display Buttons
    Add_canvas = canvas2.create_window(67, 150, anchor="nw", window=button2)
    File_canvas = canvas2.create_window(67, 270, anchor="nw", window=button3)
    Back_canvas = canvas2.create_window(67, 390, anchor="nw", window=button6)

    root1.mainloop()




#-------------------------------------------------
bg = PhotoImage(file="pictures/MainPage.png")

# Create Canvas
canvas1 = Canvas(root, width=400,
                 height=400)

canvas1.pack(fill="both", expand=True)

# Display image
canvas1.create_image(0, 0 , image=bg,anchor="nw")

# Add Text
#canvas1.create_text(200, 250, )
#------------------------------------password-------------------------
# Create Buttons
s=PhotoImage(file="pictures/StartButton.png")
a=PhotoImage(file="pictures/AdminButton.png")
e=PhotoImage(file="pictures/ExitButton.png")
button1 = Button(root,text="Start",image=s,command=start_now)
button1["bg"]="white"
button1["border"]="0"
button4 = Button(root,image=a,command=openNewWindow)
button4["bg"]="white"
button4["border"]="0"
button5=Button(root,text="Exit",image=e,command=exit_now)
button5["bg"]="white"
button5["border"]="0"

# Display Buttons
Start_canvas = canvas1.create_window(67, 150,anchor="nw",window=button1)
Admin_canvas = canvas1.create_window(67, 270, anchor="nw",window=button4)
Exit_canvas = canvas1.create_window(67, 390, anchor="nw",window=button5)


#-------------------------------Creating digital clock----------------------


#lbl_canvas.pack(anchor='se')


root.mainloop()