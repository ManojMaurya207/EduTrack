from customtkinter import *
import pymysql
from datetime import * 
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import re
import time 
from twilio.rest import Client

db=pymysql.connect(host="localhost",user="root",password="root",database="student_database",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)

set_appearance_mode("light")
set_default_color_theme("blue")
admin_win=CTk()
admin_win.title("Admin home page")
screen_width = admin_win.winfo_screenwidth()
screen_height= admin_win.winfo_screenheight()
admin_win_width = screen_width
admin_win_height = screen_height
admin_win.geometry(f"{admin_win_width}x{admin_win_height}")

admin_win.geometry("+0+0")
admin_win.maxsize(width=1400,height=750)
admin_win.minsize(width=1400,height=750)
#admin_win.attributes('-fullscreen',True)

frame=CTkFrame(admin_win,width=1900,height=1000,fg_color="#66B3FF")
frame.pack()

#datetime
def date_time_display():
        
    def ct_time():
        now = datetime.now()
        ct_string = now.strftime("%H:%M:%S")
        return ct_string

    def ct_change():
        ct_string = ct_time()
        time_lb.configure(text=ct_string)
        f0.after(1000, ct_change)  # update every 1 second
    #logout_frame
    def logout_frame():
        delete_frames()
        date_time_display()
        def destroy_window():
            admin_win.destroy()
        #asking to logout
        log_lb=CTkLabel(f0,text="Do you want to logout ?",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        log_lb.place(relx=0.5,y=200,anchor=CENTER)
        log_bu=CTkButton(f0,text="Yes",height=45,command=destroy_window,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        log_bu.place(relx=0.5,y=300,anchor=CENTER)

    today = datetime.today()
    t_date= today.strftime("%B %d, %Y")
    #date and time 
    d_f=CTkFrame(f0,width=350,height=50,border_color="black",border_width=3,fg_color="white",corner_radius=40)
    d_f.place(x=730,y=5)
    time_lb=CTkLabel(d_f,width=110,height=30,text="",font=CTkFont("Helvetica",19),fg_color="white",corner_radius=40,text_color="black")
    time_lb.place(relx=0.8,rely=0.5,anchor=CENTER)
    date_lb=CTkLabel(d_f,text=t_date,width=150,height=30,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="white")
    date_lb.place(relx=0.3,rely=0.5,anchor=CENTER)
    ct_change()

    photo1=CTkImage(Image.open("logout1.png"),size=(50,50))
    edit_b=CTkButton(f0,image=photo1,command=logout_frame,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
    edit_b.place(x=1100,y=0)

#flash message for adding form
def flash_message2(text,flashlb):
                flashlb.configure(text=text)
                admin_win.update()
                time.sleep(3)
                flashlb.configure(text="")
                admin_win.update()

#Home frame
f0=CTkFrame(frame,width=1200,height=700,fg_color="#66B3FF")
f0.place(x=140,y=30)

#Dashboard
f1=CTkFrame(frame,width=100,height=680,fg_color="white",border_width=3,corner_radius=15,border_color="black")
f1.place(x=50,y=30)

#logo
photo=CTkImage(Image.open("logo2.png"),size=(60,60))
l1=CTkLabel(f1,image=photo,text=" ")
l1.place(x=18,y=40)

#hide indicators
def hide_indicators():
    home_indicate.configure(fg_color="white")
    student_indicate.configure(fg_color="white")
    teacher_indicate.configure(fg_color="white")
    timetable_indicate.configure(fg_color="white")

#to delete frames
def delete_frames():
    for f in f0.winfo_children():
        f.destroy()

#home_frame
def home_frame():
    date_time_display()
    #welcome label
    l2=CTkLabel(f0,text="Welcome Admin!",width=50,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)

    #no of students
    cursor=db.cursor()
    cursor.execute("Select count(*) count from student")
    data=cursor.fetchall()
    d=data[0]
    tot_st=d["count"]
    f3=CTkFrame(f0,width=240,height=130,fg_color="#FFFFCC",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)
    st_no=CTkLabel(f3,text=tot_st,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    st_no.place(x=20,y=10)
    t_st=CTkLabel(f3,text="Total students",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_st.place(x=20,y=90)

    #no of teachers
    cursor=db.cursor()
    cursor.execute("Select count(*) count from teacher")
    data=cursor.fetchall()
    d=data[0]
    tot_te=d["count"]
    f4=CTkFrame(f0,width=240,height=130,fg_color="#C7FAC7",border_width=3,corner_radius=12,border_color="black")
    f4.place(x=40,y=295)
    t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    t_no.place(x=20,y=10)
    t_te=CTkLabel(f4,text="Total Teachers",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_te.place(x=20,y=90)

    #no of standards
    cursor=db.cursor()
    cursor.execute("Select count(*) count from class")
    data=cursor.fetchall()
    d=data[0]
    tot_cl=d["count"]
    f5=CTkFrame(f0,width=240,height=130,fg_color="#F2C6C6",border_width=3,corner_radius=12,border_color="black")
    f5.place(x=40,y=500)
    c_no=CTkLabel(f5,text=tot_cl,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    c_no.place(x=20,y=10)
    t_c=CTkLabel(f5,text="Total Standards",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_c.place(x=20,y=90)

    #recent students
    f6=CTkFrame(f0,height=305,width=885,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f6.place(x=300,y=100)
    rec_stu_lb=CTkLabel(f0,text="Recently added students",font=CTkFont(family="Helvetica",size=20),text_color="white")
    rec_stu_lb.place(x=940,y=70)

    def treeview():
        cursor=db.cursor()
        cursor.execute("Select stud_id,name,gen,std_code,dob,phone_no from Student order by(stud_id)desc limit 5")
        data=cursor.fetchall()
        stud_id=[]
        name=[]
        gen=[]
        std=[]
        dob=[]
        mobile=[]

        for i in data:
                id=i.get("stud_id")
                na=i.get("name")
                ge=i.get("gen")
                st=i.get("std_code")
                bir=i.get("dob")
                mob=i.get("phone_no")
                stud_id.append(id)
                name.append(na)
                gen.append(ge)
                std.append(st)
                dob.append(bir)
                mobile.append(mob)

        stu_table=ttk.Treeview(f6,columns=("stu_id","name","gen","std","dob","mobile"),show="headings",height=5)
        style=ttk.Style(f6)
    
        style.theme_use("clam")
        style.configure("Treeview",rowheight=50,font=("Roboto"),background="#dac292",fieldbackground="#dac292", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("name",text="Name")
        stu_table.heading("stu_id",text="Student id")
        stu_table.heading("gen",text="Gender")
        stu_table.heading("std",text="Class")
        stu_table.heading("dob",text="Date of Birth")
        stu_table.heading("mobile",text="Mobile No")
        stu_table.column("stu_id",width=100,anchor=CENTER)
        stu_table.column("name",width=200,anchor=CENTER)
        stu_table.column("gen",width=100,anchor=CENTER)
        stu_table.column("std",width=130,anchor=CENTER)
        stu_table.column("dob",width=150,anchor=CENTER)
        stu_table.column("mobile",width=180,anchor=CENTER)

        for i in range(len(stud_id)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i],mobile[i]))
        stu_table.place(relx=0.5,rely=0.5,anchor=CENTER)
    treeview()

    #recent teachers
    f6=CTkFrame(f0,height=205,width=885,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f6.place(x=300,y=460)
    rec_stu_lb=CTkLabel(f0,text="Recently added Teahcers",font=CTkFont(family="Helvetica",size=20),text_color="white")
    rec_stu_lb.place(x=940,y=430)
    
    def treeview():
        cursor=db.cursor()
        cursor.execute("Select teacher_id,name,gen,quali,dob from teacher order by(teacher_id) desc limit 3")
        data=cursor.fetchall()
        stud_id=[]
        name=[]
        gen=[]
        std=[]
        dob=[]

        for i in data:
                id=i.get("teacher_id")
                na=i.get("name")
                ge=i.get("gen")
                st=i.get("quali")
                bir=i.get("dob")
                stud_id.append(id)
                name.append(na)
                gen.append(ge)
                std.append(st)
                dob.append(bir)

        stu_table=ttk.Treeview(f6,columns=("t_id","name","gen","quali","dob"),show="headings",height=3)
        style=ttk.Style(f6)
    
        style.theme_use("clam")
        style.configure("Treeview",rowheight=50,font=("Roboto"),background="#dac292",fieldbackground="#dac292", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("name",text="Name")
        stu_table.heading("t_id",text="Teahcer id")
        stu_table.heading("gen",text="Gender")
        stu_table.heading("quali",text="Qualification")
        stu_table.heading("dob",text="Date of Birth")
        stu_table.column("t_id",width=100,anchor=CENTER)
        stu_table.column("name",width=250,anchor=CENTER)
        stu_table.column("gen",width=100,anchor=CENTER)
        stu_table.column("quali",width=200,anchor=CENTER)
        stu_table.column("dob",width=210,anchor=CENTER)

        for i in range(len(stud_id)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i]))
        stu_table.place(relx=0.5,rely=0.5,anchor=CENTER)
    treeview()


#student_frame
def student_frame():
    date_time_display()

    #student section
    l2=CTkLabel(f0,text="Student's details",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)

    #frame for buttons 
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)
    
    def treeview():
        f9=CTkFrame(f0,width=875,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=310,y=100)
        cursor=db.cursor()
        cursor.execute("Select stud_id,name,gen,std_code,dob,phone_no from Student")
        data=cursor.fetchall()
        stud_id=[]
        name=[]
        gen=[]
        std=[]
        dob=[]
        mobile=[]

        for i in data:
                id=i.get("stud_id")
                na=i.get("name")
                ge=i.get("gen")
                st=i.get("std_code")
                bir=i.get("dob")
                mob=i.get("phone_no")
                stud_id.append(id)
                name.append(na)
                gen.append(ge)
                std.append(st)
                dob.append(bir)
                mobile.append(mob)
        global stu_table 
        stu_table=ttk.Treeview(f9,columns=("stu_id","name","gen","std","dob","mobile"),show="headings")
        style=ttk.Style(f9)
    
        style.theme_use("clam")
        style.configure("Treeview",rowheight=50,font=("Roboto"),background="#96DED1",fieldbackground="#96DED1", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("name",text="Name")
        stu_table.heading("stu_id",text="Student id")
        stu_table.heading("gen",text="Gender")
        stu_table.heading("std",text="Class")
        stu_table.heading("dob",text="Date of Birth")
        stu_table.heading("mobile",text="Mobile No")
        stu_table.column("stu_id",width=100,anchor=CENTER)
        stu_table.column("name",width=200,anchor=CENTER)
        stu_table.column("gen",width=100,anchor=CENTER)
        stu_table.column("std",width=100,anchor=CENTER)
        stu_table.column("dob",width=150,anchor=CENTER)
        stu_table.column("mobile",width=200,anchor=CENTER)

        for i in range(len(stud_id)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i],mobile[i]))
        stu_table.place(relx=0.5,rely=0.5,anchor=CENTER)
    

    def stu_hide_hover():
        vie_stu.configure(fg_color="#33CCFF")
        add_stu.configure(fg_color="#33CCFF")
        up_stu.configure(fg_color="#33CCFF")
        del_stu.configure(fg_color="#33CCFF")
        
    #view students
    def vie_stud():
        stu_hide_hover()
        vie_stu.configure(fg_color="#888888")
        treeview()

    treeview()
    vie_stu=CTkButton(f3,hover_color="#D9D9D0",command=vie_stud,text="View Students",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    vie_stu.place(x=120,y=45,anchor=CENTER)

    #add student
    def add_stud():
        stu_hide_hover()
        add_stu.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)
        main_lb=CTkLabel(f8,text="Student Admission",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(x=350,y=30)

        id_lb=CTkLabel(f8,text="Student id",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.1,y=120,anchor=CENTER)

        id_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        id_et.place(relx=0.3,y=125,anchor=CENTER)

        cursor=db.cursor()
        cursor.execute("select max(stud_id)+1 from student")
        data=cursor.fetchall()
        auto=data[0]
        auto_id=auto.get("max(stud_id)+1")
        id_et.insert(0,auto_id)
        id_et.configure(state="disabled")
        mobi_lb=CTkLabel(f8,text="Mobile No",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        mobi_lb.place(relx=0.6,y=120,anchor=CENTER)

        mobi_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        mobi_et.place(relx=0.8,y=125,anchor=CENTER)

        name_lb=CTkLabel(f8,text="Name",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        name_lb.place(relx=0.1,y=190,anchor=CENTER)

        name_et=CTkEntry(f8,corner_radius=30,height=30,width=200,border_width=2,font=("Roboto",12))
        name_et.place(relx=0.3,y=195,anchor=CENTER)

        add_lb=CTkLabel(f8,text="Address",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        add_lb.place(relx=0.6,y=190,anchor=CENTER)

        add_et=CTkTextbox(f8,corner_radius=10,height=100,width=200,border_width=2,font=("Roboto",15))
        add_et.place(relx=0.8,y=220,anchor=CENTER)

        gen_lb=CTkLabel(f8,text="Gender",width=120,height=35,corner_radius=8,font=CTkFont("Helvetica",20),text_color="black",bg_color="#96DED1")
        gen_lb.place(relx=0.1,y=250,anchor=CENTER)

        gender=StringVar()
        gen_op1=CTkRadioButton(f8,text="Male",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="M")
        gen_op1.place(relx=0.25,y=255,anchor=CENTER)

        gen_op2=CTkRadioButton(f8,text="Female",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="F")
        gen_op2.place(relx=0.35,y=255,anchor=CENTER)

        gen_op3=CTkRadioButton(f8,text="Others",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="O")
        gen_op3.place(relx=0.47,y=255,anchor=CENTER)

        std_lb=CTkLabel(f8,text="Standard",width=120,height=35,corner_radius=8,font=CTkFont("Helvetica",20),text_color="black",bg_color="#96DED1")
        std_lb.place(relx=0.1,y=390,anchor=CENTER)

        std_op=CTkOptionMenu(f8,width=180,values=["5th std","6th std","7th std","8th std","9th std","10th std"])
        std_op.place(relx=0.3,y=390,anchor=CENTER)

        date_lb=CTkLabel(f8,text="Date of Birth",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        date_lb.place(relx=0.1,y=310,anchor=CENTER)

        date_et=CTkEntry(f8,placeholder_text="YYYY-MM-DD",height=30,width=200,border_width=2,font=("Roboto",12))
        date_et.place(relx=0.3,y=315,anchor=CENTER)

        flash_massa=CTkLabel(f8,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#96DED1")
        flash_massa.place(relx=0.52,y=510,anchor=CENTER)

        #def for sending sms to student
        def send_sms_student(target_no,name,id):
            client=Client("ACd179a9bdb86d038b1e13fa72948571d1","8e4052b78df6a17a15e595fe804a91ab")
            student_id=str(id)
            message=client.messages.create(
            body=("-\n\n🎉 Congratulations!\n\nDear "+name+",\n\nWe are thrilled to inform you that your student ID has been generated.\n\nStudent id: "+student_id+"\n\nYou can use this student id to sign up and create your username and password\n\nWishing you a fantastic start to your educational endeavors!\n\nBest Regards,\nTeam Edutrack"),
            from_="+13613155246",
            to=target_no
            )
        
        def submit():
                global db
                id=id_et.get()
                name=name_et.get()
                gen=gender.get()
                std=std_op.get()
                dob=date_et.get()
                phone=mobi_et.get()
                phone_="+91"+phone
                add=add_et.get("1.0", "end-1c")
                flag_check=True
                if len(gen)==0 or len(phone)==0 or len(dob)==0 or len(name)==0 or len(add)==0 or len(id)==0:
                    flash_massa.configure(text_color="red")
                    flash_message2("Try Again",flash_massa)
                    flag_check=False
                cursor=db.cursor()
                flag_ph=True
                flag_nm=True
                flag_dob=True
                if len(phone)!=10 or not(phone.isdigit()) or not(phone[0] in ["9","8","7"]):
                    flag_ph=False
                for i in name:
                    if i.isnumeric():
                        flag_nm=False
                        break
                if len(name)==0:
                    flag_nm=False
                year=dob[0:4]
                year=int(year)
                if year<=2020:
                    flag_dob=True
                else:
                    flag_dob=False
                if flag_check==True and flag_ph==True and flag_nm==True and flag_dob==True:
                    cursor.execute("insert into student(stud_id,name,gen,std_code,dob,phone_no,address) values(%s,%s,%s,%s,%s,%s,%s)",(id,name,gen,std,dob,phone,add))
                    db.commit()
                    flash_massa.configure(text_color="green")
                    flash_message2("Student Added Successfully",flash_massa)
                    send_sms_student(phone_,name,id)
                    print(phone_,name,id)
                    print("message send")
                elif flag_ph==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Phone No",flash_massa)
                elif flag_nm==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Name",flash_massa)
                elif flag_dob==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Date of Birth",flash_massa)

        sub_bt=CTkButton(f8,text="Submit",command=submit,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        sub_bt.place(relx=0.52,y=470,anchor=CENTER)

    add_stu=CTkButton(f3,hover_color="#D9D9D0",command=add_stud,text="Add student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    add_stu.place(relx=0.5,y=120,anchor=CENTER)

    #remove student
    def del_stud():
        stu_hide_hover()
        del_stu.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)

        main_lb=CTkLabel(f8,text="Enter the detail to remove student",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(x=270,y=30)

        id_lb=CTkLabel(f8,text="Student id",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.4,y=120,anchor=CENTER)

        id_et=CTkEntry(f8,height=30,width=200,corner_radius=30,border_width=2,font=("Roboto",12))
        id_et.place(relx=0.58,y=120,anchor=CENTER)

        flash_massa=CTkLabel(f8,fg_color="#96DED1",bg_color="#96DED1",text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20))
        flash_massa.place(x=470,y=250,anchor=CENTER)
        

        def remove_stu():
                stu_id=id_et.get()
                flag_alpha=True
                for i in stu_id:
                     if i.isalpha():
                          flash_massa.configure(text_color="red")
                          flash_message2("Invalid Student id",flash_massa)
                          flag_alpha=False
                if len(stu_id)==0:
                    flash_massa.configure(text_color="red")
                    flash_message2("Enter a student id",flash_massa)
                cursor=db.cursor()
                cursor.execute("Select stud_id from Student")
                data=cursor.fetchall()
                flag=False
                for i in range(0,len(data)):
                    id=data[i]
                    st_id=id["stud_id"]
                    if int(st_id)==int(stu_id):
                        flag=True
        
                if flag==True and flag_alpha==True:
                    cursor.execute("delete from student where stud_id=%s",(stu_id))
                    db.commit()
                    flash_massa.configure(text_color="green")
                    flash_message2("Student Removed Successfully",flash_massa)
                else:
                    flash_massa.configure(text_color="red")
                    flash_message2("Student doesn't exist of the given id",flash_massa)

        del_bt=CTkButton(f8,text="Remove",command=remove_stu,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        del_bt.place(x=470,y=200,anchor=CENTER)

    del_stu=CTkButton(f3,hover_color="#D9D9D0",command=del_stud,text="Remove student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    del_stu.place(x=120,y=195,anchor=CENTER)

    #update student
    def up_stud():
        stu_hide_hover()
        up_stu.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)

        main_lb=CTkLabel(f8,text="Update student",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(relx=0.5,y=30,anchor=CENTER)

        id_lb=CTkLabel(f8,text="Student id",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.1,y=120,anchor=CENTER)

        id_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        id_et.place(relx=0.3,y=125,anchor=CENTER)

        def fetch():
            stud_id=id_et.get()
            cursor=db.cursor()
            cursor.execute("Select name,gen,std_code,dob,phone_no,address from student where stud_id=%s",(stud_id))
            data=cursor.fetchall()
            detail=data[0]
            name=detail.get("name")
            gen=detail.get('gen')
            std_code=detail.get('std_code')
            dob=detail.get('dob')
            phone=detail.get("phone_no")
            add=detail.get("address")
            #wipping entry
            mobi_et.delete(0,END)
            name_et.delete(0,END)
            add_et.delete(1.0,END)
            date_et.delete(0,END)
            #inserting entries
            mobi_et.insert(0,phone)
            name_et.insert(0,name)
            add_et.insert(INSERT,add)
            date_et.insert(0,dob)
            gender.set(gen)
            std_op.set(std_code)
        
        fet_bt=CTkButton(f8,text="fetch",command=fetch,height=20,width=60,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        fet_bt.place(relx=0.47,y=125,anchor=CENTER)

        mobi_lb=CTkLabel(f8,text="Mobile No",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        mobi_lb.place(relx=0.6,y=120,anchor=CENTER)

        mobi_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        mobi_et.place(relx=0.8,y=125,anchor=CENTER)

        name_lb=CTkLabel(f8,text="Name",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        name_lb.place(relx=0.1,y=190,anchor=CENTER)

        name_et=CTkEntry(f8,corner_radius=30,height=30,width=200,border_width=2,font=("Roboto",12))
        name_et.place(relx=0.3,y=195,anchor=CENTER)

        add_lb=CTkLabel(f8,text="Address",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        add_lb.place(relx=0.6,y=190,anchor=CENTER)

        add_et=CTkTextbox(f8,corner_radius=10,height=100,width=200,border_width=2,font=("Roboto",12))
        add_et.place(relx=0.8,y=220,anchor=CENTER)

        gen_lb=CTkLabel(f8,text="Gender",width=120,height=35,corner_radius=8,font=CTkFont("Helvetica",20),text_color="black",bg_color="#96DED1")
        gen_lb.place(relx=0.1,y=250,anchor=CENTER)

        gender=StringVar()
        gen_op1=CTkRadioButton(f8,text="Male",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="M")
        gen_op1.place(relx=0.25,y=255,anchor=CENTER)

        gen_op2=CTkRadioButton(f8,text="Female",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="F")
        gen_op2.place(relx=0.35,y=255,anchor=CENTER)

        gen_op3=CTkRadioButton(f8,text="Others",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="O")
        gen_op3.place(relx=0.47,y=255,anchor=CENTER)

        std_lb=CTkLabel(f8,text="Standard",width=120,height=35,corner_radius=8,font=CTkFont("Helvetica",20),text_color="black",bg_color="#96DED1")
        std_lb.place(relx=0.1,y=310,anchor=CENTER)

        std_op=CTkOptionMenu(f8,width=180,values=["5th std","6th std","7th std","8th std","9th std","10th std"])
        std_op.place(relx=0.3,y=315,anchor=CENTER)

        date_lb=CTkLabel(f8,text="Date of Birth",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        date_lb.place(relx=0.1,y=390,anchor=CENTER)

        date_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        date_et.place(relx=0.3,y=390,anchor=CENTER)

        flash_massa=CTkLabel(f8,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#96DED1")
        flash_massa.place(relx=0.5,y=510,anchor=CENTER)
        
        def update():
                global db
                id=id_et.get()
                flag_id=True
                if len(id)==0:
                    flag_id=False
                name=name_et.get()
                flag_nm=True
                if len(name)==0:
                    flag_nm=False
                gen=gender.get()
                flag_gen=True
                if len(gen)==0:
                    flag_gen=False
                std=std_op.get()
                flag_std=True
                if len(std)==0:
                    flag_std=False
                dob=date_et.get()
                phone=mobi_et.get()
                add=add_et.get()
                flag_add=True
                if len(add)==0:
                    flag_add=False
                cursor=db.cursor()
                flag_ph=True
                flag_dob=True
                if len(phone)!=10 or not(phone.isdigit()) or not(phone[0] in ["9","8","7"]):
                    flag_ph=False
                for i in name:
                    if i.isnumeric():
                        flag_nm=False
                        break
                year=dob[0:4]
                year=int(year)
                if year<=2020:
                    flag_dob=True
                else:
                    flag_dob=False
                if flag_ph==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Phone No",flash_massa)
                elif flag_nm==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Name",flash_massa)
                elif flag_dob==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Date of Birth",flash_massa)
                elif flag_id==False or flag_gen==False or flag_add==False or flag_std==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Try Again",flash_massa)
                elif flag_ph==True and flag_nm==True and flag_dob==True:
                    cursor.execute("Update student set name=%s,gen=%s,std_code=%s,dob=%s,phone_no=%s,address=%s where stud_id=%s",(name,gen,std,dob,phone,add,id))
                    db.commit()
                    flash_massa.configure(text_color="green")
                    flash_message2("Student Updated Successfully",flash_massa)

        up_bt=CTkButton(f8,text="Update",command=update,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        up_bt.place(x=470,y=470,anchor=CENTER)

    up_stu=CTkButton(f3,hover_color="#D9D9D0",command=up_stud,text="Update student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    up_stu.place(x=120,y=270,anchor=CENTER)

#teacher_frame
def teacher_frame():
    date_time_display()

    #teacher_section
    l2=CTkLabel(f0,text="Teacher's details",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)

    #frame for buttons 
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)

    def teach_hide_hover():
        vie_te.configure(fg_color="#33CCFF")
        add_t.configure(fg_color="#33CCFF")
        up_t.configure(fg_color="#33CCFF")
        del_t.configure(fg_color="#33CCFF")

    def treeview():
        f9=CTkFrame(f0,width=875,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=310,y=100)
        cursor=db.cursor()
        cursor.execute("Select teacher_id,name,gen,quali,dob from teacher")
        data=cursor.fetchall()
        stud_id=[]
        name=[]
        gen=[]
        std=[]
        dob=[]

        for i in data:
                id=i.get("teacher_id")
                na=i.get("name")
                ge=i.get("gen")
                st=i.get("quali")
                bir=i.get("dob")
                stud_id.append(id)
                name.append(na)
                gen.append(ge)
                std.append(st)
                dob.append(bir)

        stu_table=ttk.Treeview(f9,columns=("t_id","name","gen","quali","dob"),show="headings")
        style=ttk.Style(f9)
    

        style.theme_use("clam")
        style.configure("Treeview",rowheight=50,font=("Roboto"),background="#96DED1",fieldbackground="#96DED1", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("name",text="Name")
        stu_table.heading("t_id",text="Teahcer id")
        stu_table.heading("gen",text="Gender")
        stu_table.heading("quali",text="Qualification")
        stu_table.heading("dob",text="Date of Birth")
        stu_table.column("t_id",width=100,anchor=CENTER)
        stu_table.column("name",width=250,anchor=CENTER)
        stu_table.column("gen",width=130,anchor=CENTER)
        stu_table.column("quali",width=180,anchor=CENTER)
        stu_table.column("dob",width=190,anchor=CENTER)

        for i in range(len(stud_id)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i]))
        stu_table.place(relx=0.5,rely=0.5,anchor=CENTER)

    #view teachers
    def view_teach():
        teach_hide_hover()
        vie_te.configure(fg_color="#888888")
        treeview()
    treeview()

    vie_te=CTkButton(f3,text="View Teachers",hover_color="#D9D9D0",command=view_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    vie_te.place(x=120,y=45,anchor=CENTER)

    #add teacher
    def add_teach():
        teach_hide_hover()
        add_t.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)
        main_lb=CTkLabel(f8,text="Add Teacher's details",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(x=350,y=30)

        id_lb=CTkLabel(f8,text="Teacher id",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.1,y=120,anchor=CENTER)

        id_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        id_et.place(relx=0.3,y=125,anchor=CENTER)

        cursor=db.cursor()
        cursor.execute("select max(teacher_id)+1 from teacher")
        data=cursor.fetchall()
        auto=data[0]
        auto_id=auto.get("max(teacher_id)+1")
        id_et.insert(0,auto_id)
        id_et.configure(state="disabled")
        mobi_lb=CTkLabel(f8,text="Mobile No",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        mobi_lb.place(relx=0.6,y=120,anchor=CENTER)

        mobi_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        mobi_et.place(relx=0.8,y=125,anchor=CENTER)

        name_lb=CTkLabel(f8,text="Name",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        name_lb.place(relx=0.1,y=190,anchor=CENTER)

        name_et=CTkEntry(f8,corner_radius=30,height=30,width=200,border_width=2,font=("Roboto",12))
        name_et.place(relx=0.3,y=195,anchor=CENTER)

        add_lb=CTkLabel(f8,text="Address",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        add_lb.place(relx=0.6,y=190,anchor=CENTER)

        add_et=CTkTextbox(f8,corner_radius=10,height=70,width=200,border_width=2,font=("Roboto",12))
        add_et.place(relx=0.8,y=200,anchor=CENTER)

        user_lb=CTkLabel(f8,text="Username",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        user_lb.place(relx=0.6,y=280,anchor=CENTER)

        user_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        user_et.place(relx=0.8,y=280,anchor=CENTER)

        pass_lb=CTkLabel(f8,text="Password",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        pass_lb.place(relx=0.6,y=360,anchor=CENTER)

        pass_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        pass_et.place(relx=0.8,y=360,anchor=CENTER)

        gen_lb=CTkLabel(f8,text="Gender",width=120,height=35,corner_radius=8,font=CTkFont("Helvetica",20),text_color="black",bg_color="#96DED1")
        gen_lb.place(relx=0.1,y=250,anchor=CENTER)

        gender=StringVar()
        gen_op1=CTkRadioButton(f8,text="Male",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="M")
        gen_op1.place(relx=0.25,y=255,anchor=CENTER)

        gen_op2=CTkRadioButton(f8,text="Female",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="F")
        gen_op2.place(relx=0.35,y=255,anchor=CENTER)

        gen_op3=CTkRadioButton(f8,text="Others",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="O")
        gen_op3.place(relx=0.47,y=255,anchor=CENTER)

        quali_lb=CTkLabel(f8,text="Qualification",width=120,height=35,corner_radius=8,font=CTkFont("Helvetica",20),text_color="black",bg_color="#96DED1")
        quali_lb.place(relx=0.1,y=310,anchor=CENTER)

        quali_op=CTkOptionMenu(f8,width=180,values=["D.ed","B.ed","M.ed","Phd"])
        quali_op.place(relx=0.3,y=315,anchor=CENTER)

        date_lb=CTkLabel(f8,text="Date of Birth",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        date_lb.place(relx=0.1,y=390,anchor=CENTER)

        date_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        date_et.place(relx=0.3,y=390,anchor=CENTER)

        flash_massa=CTkLabel(f8,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#96DED1")
        flash_massa.place(relx=0.5,y=510,anchor=CENTER)

        def submit():
                global db
                id=id_et.get()
                name=name_et.get()
                gen=gender.get()
                quali=quali_op.get()
                dob=date_et.get()
                phone=mobi_et.get()
                address=add_et.get("1.0", "end-1c")
                username=user_et.get()
                password=pass_et.get()
                flag_check=True
                if len(gen)==0 or len(name)==0 or len(gen)==0 or len(dob)==0 or len(phone)==0 or len(address)==0 or len(username)==0 or len(id)==0:
                    flash_massa.configure(text_color="red")
                    flash_message2("Try Again",flash_massa)
                    flag_check=False
                cursor=db.cursor()
                flag_ph=True
                flag_nm=True
                flag_dob=True
                flag_pass=True
                if len(phone)!=10 or not(phone.isdigit()) or not(phone[0] in ["9","8","7"]):
                    flag_ph=False
                for i in name:
                    if i.isnumeric():
                        flag_nm=False
                        break
                year=dob[0:4]
                year=int(year)
                if year<=2020:
                    flag_dob=True
                else:
                    flag_dob=False
                if len(password)!=5:
                    flag_pass=False
                
                if flag_ph==True and flag_check==True and flag_nm==True and flag_dob==True:
                    cursor.execute("insert into teacher values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,name,gen,quali,dob,phone,address,username,password))
                    db.commit()
                    flash_massa.configure(text_color="green")
                    flash_message2("Teacher Added Successfully",flash_massa)
                elif flag_ph==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Phone No",flash_massa)
                elif flag_pass==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Password length",flash_massa)
                elif flag_nm==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Name",flash_massa)
                elif flag_dob==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Date of Birth",flash_massa)

        sub_bt=CTkButton(f8,text="Submit",command=submit,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        sub_bt.place(relx=0.52,y=470,anchor=CENTER)

    add_t=CTkButton(f3,text="Add Teacher",hover_color="#D9D9D0",command=add_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    add_t.place(x=120,y=120,anchor=CENTER)

    #remove teacher
    def del_teach():
        teach_hide_hover()
        del_t.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)

        main_lb=CTkLabel(f8,text="Enter the detail to remove Teacher",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(x=270,y=30)

        id_lb=CTkLabel(f8,text="Teacher id",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.4,y=120,anchor=CENTER)

        id_et=CTkEntry(f8,height=30,width=200,corner_radius=30,border_width=2,font=("Roboto",12))
        id_et.place(relx=0.58,y=120,anchor=CENTER)

        flash_massa=CTkLabel(f8,fg_color="#96DED1",bg_color="#96DED1",text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20))
        flash_massa.place(x=470,y=250,anchor=CENTER)

        def remove_teach():
            t_id=id_et.get()
            cursor=db.cursor()
            cursor.execute("Select teacher_id from teacher")
            data=cursor.fetchall()
            flag=False
            for i in range(0,len(data)):
                id=data[i]
                st_id=id["teacher_id"]
                if int(st_id)==int(t_id):
                    flag=True
    
            if flag==True:
                cursor.execute("delete from teacher where teacher_id=%s",(t_id))
                db.commit()
                flash_massa.configure(text_color="green")
                flash_message2("Teacher Removed Successfully",flash_massa)
            else:
                flash_massa.configure(text_color="red")
                flash_message2("Teacher doesn't exist of the given id",flash_massa)

        del_bt=CTkButton(f8,text="Remove",command=remove_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        del_bt.place(x=470,y=200,anchor=CENTER)

    del_t=CTkButton(f3,text="Remove Teacher",hover_color="#D9D9D0",command=del_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    del_t.place(x=120,y=195,anchor=CENTER)

    #update teacher
    def up_teach():
        teach_hide_hover()
        up_t.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)
        main_lb=CTkLabel(f8,text="Update Teacher",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(relx=0.5,y=30,anchor=CENTER)

        id_lb=CTkLabel(f8,text="Teacher id",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.1,y=120,anchor=CENTER)

        id_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        id_et.place(relx=0.3,y=125,anchor=CENTER)

        def fetch():
            t_id=id_et.get()
            cursor=db.cursor()
            cursor.execute("Select name,gen,quali,dob,phone_no,address,username,password from teacher where teacher_id=%s",(t_id))
            data=cursor.fetchall()
            detail=data[0]
            name=detail.get("name")
            gen=detail.get('gen')
            std_code=detail.get('quali')
            dob=detail.get('dob')
            phone=detail.get("phone_no")
            add=detail.get("address")
            user=detail.get("username")
            passwd=detail.get("password")
            mobi_et.insert(0,phone)
            name_et.insert(0,name)
            add_et.insert(0,add)
            date_et.insert(0,dob)
            gender.set(gen)
            quali_op.set(std_code)
            user_et.insert(0,user)
            pass_et.insert(0,passwd)
        
        fet_bt=CTkButton(f8,text="fetch",command=fetch,height=20,width=60,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        fet_bt.place(relx=0.47,y=125,anchor=CENTER)

        mobi_lb=CTkLabel(f8,text="Mobile No",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        mobi_lb.place(relx=0.6,y=120,anchor=CENTER)

        mobi_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        mobi_et.place(relx=0.8,y=125,anchor=CENTER)

        name_lb=CTkLabel(f8,text="Name",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        name_lb.place(relx=0.1,y=190,anchor=CENTER)

        name_et=CTkEntry(f8,corner_radius=30,height=30,width=200,border_width=2,font=("Roboto",12))
        name_et.place(relx=0.3,y=195,anchor=CENTER)

        add_lb=CTkLabel(f8,text="Address",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        add_lb.place(relx=0.6,y=190,anchor=CENTER)

        add_et=CTkEntry(f8,corner_radius=10,height=80,width=200,border_width=2,font=("Roboto",12))
        add_et.place(relx=0.8,y=200,anchor=CENTER)

        gen_lb=CTkLabel(f8,text="Gender",width=120,height=35,corner_radius=8,font=CTkFont("Helvetica",20),text_color="black",bg_color="#96DED1")
        gen_lb.place(relx=0.1,y=250,anchor=CENTER)

        gender=StringVar()
        gen_op1=CTkRadioButton(f8,text="Male",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="M")
        gen_op1.place(relx=0.25,y=255,anchor=CENTER)

        gen_op2=CTkRadioButton(f8,text="Female",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="F")
        gen_op2.place(relx=0.35,y=255,anchor=CENTER)

        gen_op3=CTkRadioButton(f8,text="Others",fg_color="black",font=CTkFont("Helvetica",20),variable=gender,value="O")
        gen_op3.place(relx=0.47,y=255,anchor=CENTER)

        quali_lb=CTkLabel(f8,text="Qualification",width=120,height=35,corner_radius=8,font=CTkFont("Helvetica",20),text_color="black",bg_color="#96DED1")
        quali_lb.place(relx=0.1,y=310,anchor=CENTER)

        quali_op=CTkOptionMenu(f8,width=180,values=["D.ed","B.ed","M.ed","Phd"])
        quali_op.place(relx=0.3,y=315,anchor=CENTER)

        date_lb=CTkLabel(f8,text="Date of Birth",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        date_lb.place(relx=0.1,y=390,anchor=CENTER)

        date_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        date_et.place(relx=0.3,y=390,anchor=CENTER)

        user_lb=CTkLabel(f8,text="Username",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        user_lb.place(relx=0.6,y=280,anchor=CENTER)

        user_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        user_et.place(relx=0.8,y=280,anchor=CENTER)

        pass_lb=CTkLabel(f8,text="Password",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        pass_lb.place(relx=0.6,y=360,anchor=CENTER)

        pass_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        pass_et.place(relx=0.8,y=360,anchor=CENTER)

        flash_massa=CTkLabel(f8,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#96DED1")
        flash_massa.place(relx=0.5,y=510,anchor=CENTER)
        
        def update():
                global db
                id=id_et.get()
                name=name_et.get()
                gen=gender.get()
                std=quali_op.get()
                dob=date_et.get()
                phone=mobi_et.get()
                add=add_et.get()
                cursor=db.cursor()
                user=user_et.get()
                passwd=pass_et.get()
                flag_ph=True
                flag_nm=True
                flag_dob=True
                flag_pass=True
                if len(phone)!=10 or not(phone.isdigit()) or not(phone[0] in ["9","8","7"]):
                    flag_ph=False
                for i in name:
                    if i.isnumeric():
                        flag_nm=False
                        break
                year=dob[0:4]
                year=int(year)
                if year<=2020:
                    flag_dob=True
                else:
                    flag_dob=False
                if len(passwd)<=5:
                    flag_pass=False
                if len(gen)==0 or len(name)==0 or len(add)==0 or len(phone)==0 or len(dob)==0 or len(id)==0 or len(user)==0:
                    flash_massa.configure(text_color="red")
                    flash_message2("Try Again",flash_massa)
                elif flag_ph==True and flag_nm==True and flag_dob==True:
                    cursor.execute("Update teacher set name=%s,gen=%s,quali=%s,dob=%s,phone_no=%s,address=%s,username=%s,password=%s where teacher_id=%s",(name,gen,std,dob,phone,add,user,passwd,id))
                    db.commit()
                    flash_massa.configure(text_color="green")
                    flash_message2("Teacher Updated Successfully",flash_massa)
                elif flag_ph==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Phone No",flash_massa)
                elif flag_pass==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid password length",flash_massa)
                elif flag_nm==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Name",flash_massa)
                elif flag_dob==False:
                    flash_massa.configure(text_color="red")
                    flash_message2("Invalid Date of Birth",flash_massa)

        up_bt=CTkButton(f8,text="Update",command=update,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        up_bt.place(x=470,y=470,anchor=CENTER)

    up_t=CTkButton(f3,text="Update Teacher",hover_color="#D9D9D0",command=up_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    up_t.place(x=120,y=270,anchor=CENTER)

#timetable_frame
def timetable_frame():
    date_time_display()
    #timetable_section
    l2=CTkLabel(f0,text="Classwise teacher's details",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)

    #frame for buttons 
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)

    def treeview(std_code):
        f9=CTkFrame(f0,width=625,height=555,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=290,y=90)
        cursor=db.cursor()
        cursor.execute("Select teacher.name,subject.sub_name From teacher,class,teach_class,subject where teacher_id=teacher_code and sub_id=sub_code and std_id=std_code and std_id=%s",(std_code))
        data=cursor.fetchall()
        teach_name=[]
        subject_name=[]

        for i in data:
                sub_name=i.get("name")
                teacher_name=i.get("sub_name")
                teach_name.append(teacher_name)
                subject_name.append(sub_name)

        stu_table=ttk.Treeview(f9,columns=("subject_name","teach_name"),show="headings")
        style=ttk.Style(f9)
        style.theme_use("clam")
        style.configure("Treeview",rowheight=50,font=("Roboto"),background="#96DED1",fieldbackground="#96DED1", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("subject_name",text="Subject")
        stu_table.heading("teach_name",text="Teacher Name")
        stu_table.column("teach_name",width=300,anchor=CENTER)
        stu_table.column("subject_name",width=300,anchor=CENTER)

        for i in range(len(teach_name)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(teach_name[i],subject_name[i]))
        stu_table.place(relx=0.5,rely=0.5,anchor=CENTER)
    def std_hide_hover():
        std_5.configure(fg_color="#33CCFF")
        std_6.configure(fg_color="#33CCFF")
        std_7.configure(fg_color="#33CCFF")
        std_8.configure(fg_color="#33CCFF")
        std_9.configure(fg_color="#33CCFF")
        std_10.configure(fg_color="#33CCFF")
    #list with all teacher's names
    cursor=db.cursor()
    cursor.execute("Select name from teacher")
    data=cursor.fetchall()
    teach_name=[]
    for i in data:
        teacher_name=i.get("name")
        teach_name.append(teacher_name)
    #def for getting the exact subject teacher
    def get_teacher_nm(sub_no,std_co):
        cursor=db.cursor()
        cursor.execute("select name from teacher where teacher_id=(select teacher_code from teach_class where sub_code=%s and std_code=%s)",(sub_no,std_co))
        data=cursor.fetchall()
        teacher=data[0]
        t_nm=teacher.get("name")
        return t_nm
    #def for edit button
    def edit_tt(std_code):
        f8=CTkFrame(f0,width=605,height=535,fg_color="#96DED1",bg_color="white",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=300,y=100)
        eng=CTkLabel(f8,text="English",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        eng.place(x=100,y=20)
        option_eng=CTkOptionMenu(f8,width=200,height=40,values=teach_name)
        option_eng.set(get_teacher_nm(1,std_code))
        option_eng.place(x=300,y=23)
        mara=CTkLabel(f8,text="Marathi",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        mara.place(x=100,y=90)
        option_mara=CTkOptionMenu(f8,width=200,height=40,values=teach_name)
        option_mara.set(get_teacher_nm(3,std_code))
        option_mara.place(x=300,y=93)
        hin=CTkLabel(f8,text="Hindi",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        hin.place(x=100,y=160)
        option_hin=CTkOptionMenu(f8,width=200,height=40,values=teach_name)
        option_hin.set(get_teacher_nm(2,std_code))
        option_hin.place(x=300,y=163)
        sci=CTkLabel(f8,text="Science",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        sci.place(x=100,y=230)
        option_sci=CTkOptionMenu(f8,width=200,height=40,values=teach_name)
        option_sci.place(x=300,y=233)
        option_sci.set(get_teacher_nm(5,std_code))
        math=CTkLabel(f8,text="Mathematics",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        math.place(x=100,y=300)
        option_math=CTkOptionMenu(f8,width=200,height=40,values=teach_name)
        option_math.set(get_teacher_nm(4,std_code))
        option_math.place(x=300,y=303)
        ss=CTkLabel(f8,text="Social Studies",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        ss.place(x=100,y=370)
        option_ss=CTkOptionMenu(f8,width=200,height=40,values=teach_name)
        option_ss.set(get_teacher_nm(6,std_code))
        option_ss.place(x=300,y=373)
        pt=CTkLabel(f8,text="Physical Training",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        pt.place(x=100,y=440)
        option_pt=CTkOptionMenu(f8,width=200,height=40,values=teach_name)
        option_pt.set(get_teacher_nm(7,std_code))
        option_pt.place(x=300,y=443)
        note=CTkLabel(f8,text="*Do not enter Same teacher for two subjects",height=25,width=170,corner_radius=20,text_color="black",fg_color="#96DED1",font=CTkFont("Helvetica",18))
        note.place(x=15,y=500)
        def save():
            t_eng=option_eng.get()
            t_mara=option_mara.get()
            t_hin=option_hin.get()
            t_sci=option_sci.get()
            t_math=option_math.get()
            t_ss=option_ss.get()
            t_pt=option_pt.get()
            def update_t(sub_t,sub_no,std_no):
                    cursor=db.cursor()
                    cursor.execute("update teach_class set teacher_code=(select teacher_id from teacher where name=%s) where sub_code=%s and std_code=%s",(sub_t,sub_no,std_no))
                    db.commit()
            update_t(t_eng,1,std_code)
            update_t(t_hin,2,std_code)
            update_t(t_mara,3,std_code)
            update_t(t_sci,5,std_code)
            update_t(t_math,4,std_code)
            update_t(t_ss,6,std_code)
            update_t(t_pt,7,std_code)
            flash_massa=CTkLabel(f0,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#66B3FF")
            flash_massa.place(relx=0.5,y=670,anchor=CENTER)
            flash_massa.configure(text_color="green")
            flash_message2("Updated Successfully",flash_massa)
            treeview(std_code)
            
        save_b=CTkButton(f8,command=save,text="Save",height=35,width=100,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        save_b.place(x=480,y=490)
    def std5():
        std_hide_hover()
        std_5.configure(fg_color="#888888")
        treeview("5th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("5th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)

    def std6():
        std_hide_hover()
        std_6.configure(fg_color="#888888")
        treeview("6th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("6th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)

    def std7():
        std_hide_hover()
        std_7.configure(fg_color="#888888")
        treeview("7th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("7th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)

    def std8():
        std_hide_hover()
        std_8.configure(fg_color="#888888")
        treeview("8th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("8th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)

    def std9():
        std_hide_hover()
        std_9.configure(fg_color="#888888")
        treeview("9th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("9th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)

    def std10():
        std_hide_hover()
        std_10.configure(fg_color="#888888")  
        treeview("10th std") 
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("10th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)

    std_5=CTkButton(f3,hover_color="#D9D9D0",command=std5,text="5th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_5.place(relx=0.5,y=45,anchor=CENTER)

    std_6=CTkButton(f3,hover_color="#D9D9D0",command=std6,text="6th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_6.place(relx=0.5,y=120,anchor=CENTER)

    std_7=CTkButton(f3,hover_color="#D9D9D0",command=std7,text="7th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_7.place(relx=0.5,y=195,anchor=CENTER)

    std_8=CTkButton(f3,hover_color="#D9D9D0",command=std8,text="8th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_8.place(relx=0.5,y=270,anchor=CENTER)

    std_9=CTkButton(f3,hover_color="#D9D9D0",command=std9,text="9th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_9.place(relx=0.5,y=345,anchor=CENTER)

    std_10=CTkButton(f3,hover_color="#D9D9D0",command=std10,text="10th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_10.place(relx=0.5,y=420,anchor=CENTER)


#to indicate
def indicate(lb,frame):
    hide_indicators()
    lb.configure(fg_color="#0066ff")
    delete_frames()
    frame()

#home indicator
home_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
home_indicate.place(x=10,y=150)

#student indicator
student_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
student_indicate.place(x=10,y=250)

#teacher indicator
teacher_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
teacher_indicate.place(x=10,y=350)

#timetable indicator
timetable_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
timetable_indicate.place(x=10,y=450)

#to initialize the admin_win
indicate(home_indicate,home_frame)

#home button
photo1=CTkImage(Image.open("home.png"),size=(50,50))
b1=CTkButton(f1,command=lambda: indicate(home_indicate,home_frame),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="white")
b1.place(x=17,y=150)

#student button
photo2=CTkImage(Image.open("college.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(student_indicate,student_frame),image=photo2,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=250)

#teacher button 
photo3=CTkImage(Image.open("class.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(teacher_indicate,teacher_frame),image=photo3,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=350)

#timetable button 
photo4=CTkImage(Image.open("timetable.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(timetable_indicate,timetable_frame),image=photo4,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=450)

admin_win.mainloop()