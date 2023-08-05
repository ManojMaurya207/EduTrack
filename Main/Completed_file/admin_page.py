from customtkinter import *
import pymysql
from datetime import * 
from tkinter import ttk
from PIL import Image
from twilio.rest import Client
from tktooltip import ToolTip


#----------------------------------------------------------------Local Conection----------------------------------------------------------------

db=pymysql.connect(host="localhost",user="root",password="root",database="student_database",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)

#----------------------------------------------------------------Universal functions----------------------------------------------------------------

#flash message for adding form
def flash_message(text, flashlb):
    def clear_flash_message(flashlb):
        flashlb.configure(text="")
        flashlb.update()
    flashlb.configure(text=text)
    flashlb.update()
    flashlb.after(3000, clear_flash_message, flashlb)

def animate_frame(frame_to_animate):
    target_height = frame_to_animate.cget("height")
    frame_to_animate.configure(height=0)
    current_height = 0
    while current_height < target_height:
        current_height = min(current_height + 30, target_height)
        frame_to_animate.configure( height=current_height)
        frame_to_animate.update()
        #time.sleep(0.01)

def animate_text( element_to_animate, speed):
    sentence = element_to_animate.cget("text")
    element_to_animate.configure(text="")
    element_to_animate.update()
    def animate(index):
        if index < len(sentence):
            element_to_animate.configure(text=element_to_animate.cget("text") + sentence[index])
            element_to_animate.update()
            element_to_animate.after(speed, animate, index + 1)
    animate(0)


#----------------------------------------------------------------Local Functions----------------------------------------------------------------

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
    logout_b=CTkButton(f0,image=photo1,command=logout_frame,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
    logout_b.place(x=1100,y=0)
    ToolTip(logout_b,msg="Logout",delay=0)

#to indicate
def indicate(lb,frame):
    hide_indicators()
    lb.configure(fg_color="#0066ff")
    delete_frames()
    frame()

#for removing attendence
def delete_attendance_record(student_id):
    #data access from database
    cursor=db.cursor()
    cursor.execute("Select * from student")
    s_data=cursor.fetchall()
    id=s_data[-1]["stud_id"]
    
    if int(student_id)>100 and int(student_id)<=int(id):
        cursor=db.cursor()
        cursor.execute("Select * from student where stud_id=%s",(student_id,))
        s_data=cursor.fetchall()
        if len(s_data)!=0:
            data1=s_data[0]
            Std=data1.get("std_code")
            
            cursor = db.cursor()
            cursor.execute("select count(*) from student where std_code=%s and stud_id<%s", (Std, student_id))
            s_data = cursor.fetchall()

            roll_index = s_data[0]["count(*)"]       
            cursor.execute("select attendance_date,attend_sheet from attendance where stand_code=%s",(Std))
            data_sheet=cursor.fetchall()
            new_sheet=""
            for i in range(len(data_sheet)):
                date=data_sheet[i].get("attendance_date")
                sheet=data_sheet[i].get("attend_sheet")
                new_sheet=sheet[:roll_index]+sheet[int(roll_index)+1:]

                cursor = db.cursor()
                cursor.execute(" update attendance set attend_sheet=%s where attendance_date=%s and stand_code=%s", (new_sheet,date,Std))
                db.commit()

#def for removing record
def remove(entry,table,id,flash):
    entry=entry.get()
    flag_alpha=True
    for i in entry:
            if i.isalpha():
                flag_alpha=False
    if len(entry)==0:
        flash.configure(text_color="red")
        flash_message("Enter a "+table+" id",flash)
    elif flag_alpha==False:
        flash.configure(text_color="red")
        flash_message("Invalid "+table+" id",flash)
    else:
        try:
            cursor=db.cursor()
            cursor.execute("Select "+id+" from "+table+" where "+id+"=%s",(entry))
            data=cursor.fetchall()
            if id=="stud_id":
                cursor.execute("delete from complain where stud_code=%s",(entry))
                db.commit()
                cursor.execute("delete from grade where stud_code=%s",(entry))
                db.commit()
                delete_attendance_record(entry)
            if len(data)!=0:
                cursor.execute("delete from "+table+" where "+id+"=%s",(entry))
                db.commit()
                flash.configure(text_color="green")
                flash_message(table+" Removed Successfully",flash)
            else:
                flash.configure(text_color="red")
                flash_message(table+" doesn't exist of the given id",flash)
        except pymysql.Error:
            flash.configure(text_color="red")
            flash_message("Teacher assinged to class",flash)

#def for validating dob
def validate_dob(year,month,date,dob,flag_dob):
    flag_alpha=True
    for i in dob:
        if i.isalpha():
            flag_alpha=False
            flag_dob=False
    if flag_alpha==True:
        year=int(year)
        month=int(month)
        date=int(date)
        if len(dob)==10 and year<=2020 :
                if month<=12:
                    if month in (1,3,5,7,8,10,12):
                        if 1<=date<=31:
                            flag_dob=True
                        else:
                            flag_dob=False
                    elif month in (4,6,9,11):
                        if 1<=date<=30:
                            flag_dob=True
                        else:
                            flag_dob=False
                    elif month==2:
                        if year%4==0:
                            if 1<=date<=29:
                                flag_dob=True
                            else:
                                flag_dob=False
                        else:
                            if 1<=date<=28:
                                flag_dob=True
                            else:
                                flag_dob=False
                else:
                    flag_dob=False
        else:
            flag_dob=False
    return flag_dob

#hide indicators
def hide_indicators():
    home_indicate.configure(fg_color="white")
    student_indicate.configure(fg_color="white")
    teacher_indicate.configure(fg_color="white")
    timetable_indicate.configure(fg_color="white")
    complain_indicate.configure(fg_color="white")

#to delete frames
def delete_frames():
    for f in f0.winfo_children():
        f.destroy()



#---------------------------------------------------------------Home Frame----------------------------------------------------------------



#home_frame
def home_frame():
    global departments
    date_time_display()
    #welcome label
    l2=CTkLabel(f0,text="Welcome Admin!",width=50,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=0)

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
    f4.place(x=40,y=245)
    t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    t_no.place(x=20,y=10)
    t_te=CTkLabel(f4,text="Total Teachers",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_te.place(x=20,y=90)

    #Pending Complains
    departments=[]
    cursor=db.cursor()
    cursor.execute("SELECT distinct(depart) FROM complain WHERE solution IS NULL and `to`=%s",("Admin"))
    data=cursor.fetchall()
    f5=CTkScrollableFrame(f0,width=210,height=245,fg_color="#F2C6C6",border_width=3,corner_radius=12,border_color="black")
    f5.place(x=40,y=390)
    pen_lb=CTkLabel(f5,fg_color="#dac292",height=40,width=150,corner_radius=20,text="Pending",font=CTkFont(family="Helvetica",weight="bold",size=20),text_color="black")
    pen_lb.grid(row=0,column=1,padx=10)
    for i in range(len(data)):
        new=data[i]
        departments.append(new['depart'])

    if len(departments)==0:
        new_b=CTkLabel(f5,text="No Complains",height=45,width=180,corner_radius=20,text_color="black",fg_color="#F2C6C6",font=CTkFont(family="Helvetica",weight="bold",size=20))
        new_b.grid(row=3,column=1,padx=10,pady=10)

    r=1
    y_pad=2
    for i in departments:
        new_b=CTkButton(f5,text=i,height=45,width=180,border_width=2,border_color="black",corner_radius=20,text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        new_b.configure(command=lambda new=new_b: indicate(complain_indicate,complain_frame))
        new_b.grid(row=r,column=1,padx=10,pady=y_pad+7)
        r+=1

    #recent students
    f6=CTkFrame(f0,height=305,width=885,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f6.place(x=300,y=100)
    animate_frame(f6)
    rec_stu_lb=CTkLabel(f0,text="Recently added students",font=CTkFont(family="Helvetica",size=20),text_color="white")
    rec_stu_lb.place(x=940,y=70)
    animate_text(rec_stu_lb,20)
    
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
    animate_frame(f6)
    rec_stu_lb=CTkLabel(f0,text="Recently added Teahcers",font=CTkFont(family="Helvetica",size=20),text_color="white")
    rec_stu_lb.place(x=940,y=430)
    animate_text(rec_stu_lb,20)
    
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



#----------------------------------------------------------------Student Frame----------------------------------------------------------------



#student_frame
def student_frame():
    date_time_display()

    #student section
    l2=CTkLabel(f0,text="Student's details",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)

    #frame for buttons 
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)
    animate_frame(f3)
    
    def treeview():
        f9=CTkFrame(f0,width=875,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=310,y=100)
        animate_frame(f9)
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

    vie_stu=CTkButton(f3,hover_color="#D9D9D0",command=vie_stud,text="View Students",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    vie_stu.place(x=120,y=45,anchor=CENTER)
    animate_text(vie_stu,20)


    #add student
    def add_stud():
        stu_hide_hover()
        add_stu.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)
        animate_frame(f8)

        main_lb=CTkLabel(f8,text="Student Admission",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(relx=0.5,y=40,anchor=CENTER)
        animate_text(main_lb,20)

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

        flash_massa=CTkLabel(f8,text_color="#04C34D",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#96DED1")
        flash_massa.place(relx=0.52,y=510,anchor=CENTER)

        #def for sending sms to student
        def send_sms_student(target_no,name,id):
            client=Client("<Account SID>","<Auth Token>")
            student_id=str(id)
            message=client.messages.create(
            body=("-\n\n🎉 Congratulations!\n\nDear "+name+",\n\nWe are thrilled to inform you that your student ID has been generated.\n\nStudent id: "+student_id+"\n\nYou can use this student id to sign up and create your username and password\n\nWishing you a fantastic start to your educational endeavors!\n\nBest Regards,\nTeam Edutrack"),
            from_="<My Twilio phone number>",
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
                flash_message("Try Again",flash_massa)
                flag_check=False
            else:
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
                special_characters = "!@#$%^&*()_+}~`-=;'/.,<>?|"
                if len(name)==0 or any(char in special_characters for char in name):
                    flag_nm=False
                year=dob[0:4]
                date=dob[8:10]
                month=dob[5:7]
                flag_dob=validate_dob(year,month,date,dob,flag_dob)
                if flag_check==True and flag_ph==True and flag_nm==True and flag_dob==True:
                    cursor.execute("insert into student(stud_id,name,gen,std_code,dob,phone_no,address) values(%s,%s,%s,%s,%s,%s,%s)",(id,name,gen,std,dob,phone,add))
                    db.commit()
                    flash_massa.configure(text_color="#04C34D")
                    flash_message("Student Added Successfully",flash_massa)
                    send_sms_student(phone_,name,id)
                elif flag_nm==False:
                    flash_massa.configure(text_color="red")
                    flash_message("Invalid Name",flash_massa)
                elif flag_dob==False:
                    flash_massa.configure(text_color="red")
                    flash_message("Invalid Date of Birth",flash_massa)
                elif flag_ph==False:
                    flash_massa.configure(text_color="red")
                    flash_message("Invalid Phone No",flash_massa)


        sub_bt=CTkButton(f8,text="Submit",command=submit,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        sub_bt.place(relx=0.52,y=470,anchor=CENTER)

    add_stu=CTkButton(f3,hover_color="#D9D9D0",command=add_stud,text="Add student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    add_stu.place(relx=0.5,y=120,anchor=CENTER)
    animate_text(add_stu,20)

    #remove student
    def del_stud():
        stu_hide_hover()
        del_stu.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)

        main_lb=CTkLabel(f8,text="Enter the detail to remove student",text_color="black",font=CTkFont("Helvetica",35))
        main_lb.place(relx=0.5,rely=0.3,anchor=CENTER)

        id_lb=CTkLabel(f8,text="Student id",width=120,height=45,corner_radius=8,font=("Helvetica",23),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.41,rely=0.44,anchor=CENTER)

        id_et=CTkEntry(f8,justify=CENTER,height=45,width=170,corner_radius=30,border_width=2,font=("Roboto",20))
        id_et.place(relx=0.58,rely=0.44,anchor=CENTER)

        flash_massa=CTkLabel(f8,fg_color="#96DED1",bg_color="#96DED1",text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20))
        flash_massa.place(relx=0.5,rely=0.7,anchor=CENTER)

        del_bt=CTkButton(f8,text="Remove",command=lambda: remove(id_et,"Student","stud_id",flash_massa),height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        del_bt.place(relx=0.5,rely=0.6,anchor=CENTER)

    del_stu=CTkButton(f3,hover_color="#D9D9D0",command=del_stud,text="Remove student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    del_stu.place(x=120,y=195,anchor=CENTER)

    #update student
    def up_stud():
        stu_hide_hover()
        up_stu.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)
        animate_frame(f8)

        main_lb=CTkLabel(f8,text="Update student",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(relx=0.5,y=30,anchor=CENTER)
        animate_text(main_lb,20)

        id_lb=CTkLabel(f8,text="Student id",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.1,y=120,anchor=CENTER)

        id_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        id_et.place(relx=0.3,y=125,anchor=CENTER)

        def fetch():
            stud_id=id_et.get()
            flag_check=True
            if len(stud_id)==0:
                flash_massa.configure(text_color="red")
                flash_message("Try Again",flash_massa)
                flag_check=False
            if flag_check==True:
                cursor=db.cursor()
                cursor.execute("Select name,gen,std_code,dob,phone_no,address from student where stud_id=%s",(stud_id))
                data=cursor.fetchall()
                if len(data)==0:
                    flash_massa.configure(text_color="red")
                    flash_message("Student of given id doesn't exist",flash_massa)
                if len(data)!=0:   
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

        flash_massa=CTkLabel(f8,text_color="#04C34D",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#96DED1")
        flash_massa.place(relx=0.5,y=510,anchor=CENTER)
        
        def update():
                global db
                id=id_et.get()
                name=name_et.get()
                gen=gender.get()
                std=std_op.get()
                dob=date_et.get()
                phone=mobi_et.get()
                add=add_et.get("1.0", "end-1c")
                if len(gen)==0 or len(phone)==0 or len(dob)==0 or len(name)==0 or len(add)==0 or len(id)==0:
                    flash_massa.configure(text_color="red")
                    flash_message("Try Again",flash_massa)
                else:
                    cursor=db.cursor()
                    flag_ph=True
                    flag_nm=True
                    flag_dob=True
                    if  len(phone)!=10 or not(phone.isdigit()) or not(phone[0] in ["9","8","7"]):
                        flag_ph=False
                    for i in name :
                        if i.isnumeric():
                            flag_nm=False
                            break
                    special_characters = "!@#$%^&*()_+}~`-=;'/.,<>?|"
                    if len(name)==0 or any(char in special_characters for char in name):
                        flag_nm=False
                    year=dob[0:4]
                    date=dob[8:10]
                    month=dob[5:7]
                    flag_dob=validate_dob(year,month,date,dob,flag_dob)
                    if flag_ph==True and flag_nm==True and flag_dob==True:
                        cursor.execute("Update student set name=%s,gen=%s,std_code=%s,dob=%s,phone_no=%s,address=%s where stud_id=%s",(name,gen,std,dob,phone,add,id))
                        db.commit()
                        flash_massa.configure(text_color="#04C34D")
                        flash_message("Student Updated Successfully",flash_massa)
                    elif flag_nm==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Name",flash_massa)
                    elif flag_dob==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Date of Birth",flash_massa)
                    elif flag_ph==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Phone No",flash_massa)
                    

        up_bt=CTkButton(f8,text="Update",command=update,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        up_bt.place(x=440,y=470,anchor=CENTER)

    up_stu=CTkButton(f3,hover_color="#D9D9D0",command=up_stud,text="Update student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    up_stu.place(x=120,y=270,anchor=CENTER)
    animate_text(up_stu,20)
    vie_stu.invoke()



#----------------------------------------------------------------Teacher Frame----------------------------------------------------------------


#teacher_frame
def teacher_frame():
    date_time_display()

    #teacher_section
    l2=CTkLabel(f0,text="Teacher's details",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)
    animate_frame(l2)

    #frame for buttons 
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)
    animate_frame(f3)

    def teach_hide_hover():
        vie_te.configure(fg_color="#33CCFF")
        add_t.configure(fg_color="#33CCFF")
        up_t.configure(fg_color="#33CCFF")
        del_t.configure(fg_color="#33CCFF")

    def treeview_teacher():
        f9=CTkFrame(f0,width=875,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=310,y=100)
        animate_frame(f9)
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
        treeview_teacher()

    vie_te=CTkButton(f3,text="View Teachers",hover_color="#D9D9D0",command=view_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    vie_te.place(x=120,y=45,anchor=CENTER)
    animate_text(vie_te,20)

    #add teacher
    def add_teach():
        teach_hide_hover()
        add_t.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)
        animate_frame(f8)
        main_lb=CTkLabel(f8,text="Add Teacher's details",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(relx=0.5,y=40,anchor=CENTER)
        animate_text(main_lb,20)
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

        flash_massa=CTkLabel(f8,text_color="#04C34D",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#96DED1")
        flash_massa.place(relx=0.52,y=510,anchor=CENTER)

        #def for sending sms to teacher
        def send_sms_teacher(target_no,name,id,user,passwd):
            client=Client("<Account SID>","<Auth Token>")
            teacher_id=str(id)
            message=client.messages.create(
            body=("-\n\n🎉 Congratulations!\n\nDear "+name+",\n\nCongratulations on joining our institution as a teacher.we would like to provide you with your teacher ID, username, and password for accessing our online systems\nTeacher Id:"+teacher_id+"\nUsername:"+user+"\nPassword:"+passwd+"\nPlease ensure to keep this information confidential and secure. Your username and password will grant you access to our online platforms, including our learning management system, attendance tracking system, grade management system and more\nShould you have any further queries or need additional information, please do not hesitate to contact the administration office.\n\nBest Regards,\nTeam Edutrack"),
            from_="<My Twilio phone number>",
            to=target_no
            )

        def submit():
                global db
                id=id_et.get()
                name=name_et.get()
                gen=gender.get()
                quali=quali_op.get()
                dob=date_et.get()
                phone=mobi_et.get()
                phone_="+91"+phone
                address=add_et.get("1.0", "end-1c")
                username=user_et.get()
                password=pass_et.get()
                if len(gen)==0 or len(name)==0 or len(gen)==0 or len(dob)==0 or len(phone)==0 or len(address)==0 or len(username)==0 or len(id)==0:
                    flash_massa.configure(text_color="red")
                    flash_message("Try Again",flash_massa)
                else:
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
                    special_characters = "!@#$%^&*()_+}~`-=;'/.,<>?|"
                    if len(name)==0 or any(char in special_characters for char in name):
                        flag_nm=False
                    year=dob[0:4]
                    date=dob[8:10]
                    month=dob[5:7]
                    flag_dob=validate_dob(year,month,date,dob,flag_dob)
                    if len(password)<5:
                        flag_pass=False       
                    if flag_pass==True and flag_ph==True and flag_nm==True and flag_dob==True:
                        cursor.execute("insert into teacher values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,name,gen,quali,dob,phone,address,username,password))
                        db.commit()
                        flash_massa.configure(text_color="#04C34D")
                        flash_message("Teacher Added Successfully",flash_massa)
                        send_sms_teacher(phone_,name,id,username,password)
                    elif flag_nm==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Name",flash_massa)
                    elif flag_dob==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Date of Birth",flash_massa)
                    elif flag_ph==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Phone No",flash_massa)
                    elif flag_pass==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Password length",flash_massa)

        sub_bt=CTkButton(f8,text="Submit",command=submit,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        sub_bt.place(relx=0.52,y=470,anchor=CENTER)

    add_t=CTkButton(f3,text="Add Teacher",hover_color="#D9D9D0",command=add_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    add_t.place(x=120,y=120,anchor=CENTER)
    animate_text(add_t,20)
    #remove teacher
    def del_teach():
        teach_hide_hover()
        del_t.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)
        animate_frame(f8)

        main_lb=CTkLabel(f8,text="Enter the detail to remove Teacher",text_color="black",font=CTkFont("Helvetica",35))
        main_lb.place(relx=0.5,rely=0.3,anchor=CENTER)
        animate_text(main_lb,20)
        id_lb=CTkLabel(f8,text="Teacher id",width=120,height=35,corner_radius=8,font=("Helvetica",23),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.41,rely=0.44,anchor=CENTER)

        id_et=CTkEntry(f8,justify=CENTER,height=45,width=170,corner_radius=30,border_width=2,font=("Helvetica",23))
        id_et.place(relx=0.58,rely=0.44,anchor=CENTER)

        flash_massa=CTkLabel(f8,fg_color="#96DED1",bg_color="#96DED1",text_color="#04C34D",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20))
        flash_massa.place(relx=0.5,rely=0.7,anchor=CENTER)

        del_bt=CTkButton(f8,text="Remove",command=lambda: remove(id_et,"Teacher","teacher_id",flash_massa),height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        del_bt.place(relx=0.5,rely=0.6,anchor=CENTER)

    del_t=CTkButton(f3,text="Remove Teacher",hover_color="#D9D9D0",command=del_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    del_t.place(x=120,y=195,anchor=CENTER)
    animate_text(del_t,20)
    #update teacher
    def up_teach():
        teach_hide_hover()
        up_t.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=875,height=560,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=310,y=100)
        animate_frame(f8)

        main_lb=CTkLabel(f8,text="Update Teacher",text_color="black",font=CTkFont("Helvetica",30))
        main_lb.place(relx=0.5,y=30,anchor=CENTER)
        animate_text(main_lb,20)

        id_lb=CTkLabel(f8,text="Teacher id",width=120,height=35,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="#96DED1")
        id_lb.place(relx=0.1,y=120,anchor=CENTER)

        id_et=CTkEntry(f8,height=30,width=200,border_width=2,font=("Roboto",12))
        id_et.place(relx=0.3,y=125,anchor=CENTER)

        def fetch():
            t_id=id_et.get()
            if len(t_id)==0:
                flash_massa.configure(text_color="red")
                flash_message("Try Again",flash_massa)
            else:
                t_id=id_et.get()
                cursor=db.cursor()
                cursor.execute("Select name,gen,quali,dob,phone_no,address,username,password from teacher where teacher_id=%s",(t_id))
                data=cursor.fetchall()
                if len(data)==0:
                    flash_massa.configure(text_color="red")
                    flash_message("Teacher of given id doesn't exist",flash_massa)
                detail=data[0]
                name=detail.get("name")
                gen=detail.get('gen')
                std_code=detail.get('quali')
                dob=detail.get('dob')
                phone=detail.get("phone_no")
                add=detail.get("address")
                user=detail.get("username")
                passwd=detail.get("password")

                #wipping data
                mobi_et.delete(0,END)
                name_et.delete(0,END)
                add_et.delete(0,END)
                date_et.delete(0,END)
                user_et.delete(0,END)
                pass_et.delete(0,END)

                #inserting data
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

        flash_massa=CTkLabel(f8,text_color="#04C34D",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#96DED1")
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
                if len(gen)==0 or len(name)==0 or len(gen)==0 or len(dob)==0 or len(phone)==0 or len(add)==0 or len(user)==0 or len(id)==0:
                    flash_massa.configure(text_color="red")
                    flash_message("Try Again",flash_massa)
                else:
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
                    special_characters = "!@#$%^&*()_+}~`-=;'/.,<>?|"
                    if len(name)==0 or any(char in special_characters for char in name):
                        flag_nm=False
                    year=dob[0:4]
                    date=dob[8:10]
                    month=dob[5:7]
                    flag_dob=validate_dob(year,month,date,dob,flag_dob)
                    if len(passwd)<5:
                        flag_pass=False       
                    if flag_pass==True and flag_ph==True and flag_nm==True and flag_dob==True:
                        cursor.execute("Update teacher set name=%s,gen=%s,quali=%s,dob=%s,phone_no=%s,address=%s,username=%s,password=%s where teacher_id=%s",(name,gen,std,dob,phone,add,user,passwd,id))
                        db.commit()
                        flash_massa.configure(text_color="#04C34D")
                        flash_message("Teacher Updated Successfully",flash_massa)
                    elif flag_nm==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Name",flash_massa)
                    elif flag_dob==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Date of Birth",flash_massa)
                    elif flag_ph==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Phone No",flash_massa)
                    elif flag_pass==False:
                        flash_massa.configure(text_color="red")
                        flash_message("Invalid Password length",flash_massa)

        up_bt=CTkButton(f8,text="Update",command=update,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        up_bt.place(x=440,y=470,anchor=CENTER)

    up_t=CTkButton(f3,text="Update Teacher",hover_color="#D9D9D0",command=up_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    up_t.place(x=120,y=270,anchor=CENTER)
    animate_text(up_t,20)
    vie_te.invoke()



#----------------------------------------------------------------Teacher Assignment Frame----------------------------------------------------------------


#teacher_assign_frame
def teacher_assign_frame():
    date_time_display()
    #timetable_section
    l2=CTkLabel(f0,text="Classwise teacher's details",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)

    #frame for buttons 
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)
    animate_frame(f3)

    def treeview(std_code):
        f9=CTkFrame(f0,width=625,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=290,y=100)
        animate_frame(f9)
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
        f8=CTkFrame(f0,width=605,height=540,fg_color="#96DED1",bg_color="white",border_width=0,corner_radius=12,border_color="black")
        f8.place(x=300,y=110)
        animate_frame(f8)
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
            flash_massa=CTkLabel(f0,text_color="#04C34D",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#66B3FF")
            flash_massa.place(relx=0.5,y=690,anchor=CENTER)
            flash_massa.configure(text_color="#04C34D")
            flash_message("Updated Successfully",flash_massa)
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
        ToolTip(edit_b,msg="Edit Teacher assignment")

    def std6():
        std_hide_hover()
        std_6.configure(fg_color="#888888")
        treeview("6th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("6th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)
        ToolTip(edit_b,msg="Edit Teacher assignment")

    def std7():
        std_hide_hover()
        std_7.configure(fg_color="#888888")
        treeview("7th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("7th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)
        ToolTip(edit_b,msg="Edit Teacher assignment")

    def std8():
        std_hide_hover()
        std_8.configure(fg_color="#888888")
        treeview("8th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("8th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)
        ToolTip(edit_b,msg="Edit Teacher assignment")

    def std9():
        std_hide_hover()
        std_9.configure(fg_color="#888888")
        treeview("9th std")
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("9th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)
        ToolTip(edit_b,msg="Edit Teacher assignment")

    def std10():
        std_hide_hover()
        std_10.configure(fg_color="#888888")  
        treeview("10th std") 
        #edit button
        photo1=CTkImage(Image.open("pencil.png"),size=(50,50))
        edit_b=CTkButton(f0,command=lambda: edit_tt("10th std"),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=920,y=100)
        ToolTip(edit_b,msg="Edit Teacher assignment")

    std_5=CTkButton(f3,hover_color="#D9D9D0",command=std5,text="5th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_5.place(relx=0.5,y=45,anchor=CENTER)
    animate_text(std_5,20)
    std_6=CTkButton(f3,hover_color="#D9D9D0",command=std6,text="6th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_6.place(relx=0.5,y=120,anchor=CENTER)
    animate_text(std_6,20)
    std_7=CTkButton(f3,hover_color="#D9D9D0",command=std7,text="7th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_7.place(relx=0.5,y=195,anchor=CENTER)
    animate_text(std_7,20)
    std_8=CTkButton(f3,hover_color="#D9D9D0",command=std8,text="8th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_8.place(relx=0.5,y=270,anchor=CENTER)
    animate_text(std_8,20)
    std_9=CTkButton(f3,hover_color="#D9D9D0",command=std9,text="9th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_9.place(relx=0.5,y=345,anchor=CENTER)
    animate_text(std_9,20)
    std_10=CTkButton(f3,hover_color="#D9D9D0",command=std10,text="10th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    std_10.place(relx=0.5,y=420,anchor=CENTER)
    animate_text(std_10,20)
    std_5.invoke()


#----------------------------------------------------------------Complain Frame----------------------------------------------------------------



#complain_frame
def complain_frame():
    global buttons_complain
    date_time_display()
    def show_complains(btn,depart):
        for i in buttons_complain:
            if btn==i:
                btn.configure(fg_color="#888888")
            else:
                i.configure(fg_color="#33CCFF")
        open_f=CTkFrame(f0,width=870,height=560,fg_color="#FFE5B4",border_width=3,corner_radius=12,border_color="black")
        open_f.place(x=325,y=100)
        animate_frame(open_f)
        all=CTkLabel(open_f,text=depart+" - Related Complains",height=45,width=470,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
        all.place(x=20,y=20)
        scroll_f=CTkScrollableFrame(open_f,width=810,corner_radius=20,fg_color="#B6E5D8",height=430)
        scroll_f.place(relx=0.5,rely=0.55,anchor=CENTER)
        cursor=db.cursor()
        cursor.execute("Select complain_id,subject from complain where `to`=%s and depart=%s",("Admin",depart))
        data=cursor.fetchall()
        def comp_desc(id):
            sol_lb=CTkLabel(open_f,text="Solution",height=45,width=170,corner_radius=20,text_color="black",fg_color="#e4d1d1",font=CTkFont("Helvetica",20))
            sol_lb.place(x=650,y=20)
            all=CTkLabel(open_f,text=" ",height=45,width=470,corner_radius=20,text_color="black",fg_color="#FFE5B4",font=CTkFont("Helvetica",20))
            all.place(x=20,y=20)
            #back button
            photo1=CTkImage(Image.open("back.png"),size=(40,40))
            edit_b=CTkButton(open_f,command=lambda param=depart,new_b=btn: show_complains(new_b, param),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#FFE5B4",corner_radius=10)
            edit_b.place(x=20,y=18)
            ToolTip(edit_b,msg="Back")
            sol_f=CTkFrame(open_f,width=860,height=470,fg_color="#FFE5B4",border_width=0,corner_radius=12)
            sol_f.place(relx=0.5,rely=0.55,anchor=CENTER)
            cursor=db.cursor()
            cursor.execute("Select stud_code,description,solution,hide from complain where complain_id=%s",(id))
            result=cursor.fetchall()
            stud_id=result[0]['stud_code']
            desc=result[0]['description']
            solu=result[0]['solution']
            anon=result[0]['hide']
            id_lb=CTkLabel(sol_f,text="Complain id",height=25,width=170,corner_radius=20,text_color="black",fg_color="#FFE5B4",font=CTkFont("Helvetica",20))
            id_lb.place(x=15,y=10)
            id_et=CTkEntry(sol_f,height=30,width=75,border_width=3,corner_radius=30,font=("Roboto",15))
            id_et.place(x=155,y=10)
            stid_lb=CTkLabel(sol_f,text="Student id",height=25,width=170,corner_radius=20,text_color="black",fg_color="#FFE5B4",font=CTkFont("Helvetica",20))
            stid_lb.place(x=415,y=10)
            stid_et=CTkEntry(sol_f,height=30,width=75,border_width=3,corner_radius=30,font=("Roboto",15))
            stid_et.place(x=555,y=10)
            desc_t=CTkTextbox(sol_f,font=CTkFont("Helvetica",20),width=824,height=150,fg_color="#ffff99",border_width=3,corner_radius=12,border_color="black")
            desc_t.place(x=15,y=50)
            sol_t=CTkTextbox(sol_f,font=CTkFont("Helvetica",20),width=824,height=200,fg_color="#e6f7ff",border_width=3,corner_radius=12,border_color="black")
            sol_t.place(x=15,y=220)
            #inserting values
            id_et.insert(0,id)
            stid_et.insert(0,stud_id)
            desc_t.insert('0.0',desc)
            desc_t.configure(state="disabled")
            id_et.configure(state="disabled")
            stid_et.configure(state="disabled")
            if anon==1:
                stid_et.destroy()
                stid_lb1=CTkLabel(sol_f,text="Anonymous",height=25,width=70,corner_radius=10,text_color="#04C34D",fg_color="#FFE5B4",font=CTkFont("Helvetica",18))
                stid_lb1.place(x=550,y=10)
                
            if solu==None:
                sol_t.insert('0.0',"Pending")
            else:
                sol_t.insert('0.0',solu)
            def save_sol():
                flash_massa=CTkLabel(sol_f,text_color="#04C34D",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#FFE5B4")
                flash_massa.place(relx=0.5,rely=0.95,anchor=CENTER)
                solution=sol_t.get("1.0", "end-1c")
                if len(solution)==0:
                    flash_massa.configure(text_color="red")
                    flash_message("Try Again",flash_massa)
                else:
                    solution=sol_t.get("1.0", "end-1c")
                    cursor=db.cursor()
                    cursor.execute('update complain set solution=%s where complain_id=%s',(solution,id))
                    db.commit()
                    flash_massa.configure(text_color="#04C34D")
                    flash_message("Saved Successfully",flash_massa)
            save_b=CTkButton(sol_f,text="Save",command=save_sol,height=35,width=100,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
            save_b.place(relx=0.9,rely=0.95,anchor=CENTER)
        r=0
        y_pad=0
        for i in range(len(data)):
            id=data[i]['complain_id']
            id=str(id)
            sub=data[i]['subject']
            new_b=CTkButton(scroll_f,hover_color="#D9D9D0",command=lambda param=id: comp_desc(param),text=id+"       "+sub,height=45,width=790,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
            new_b.grid(row=r,column=1,padx=10,pady=y_pad+10)
            animate_text(new_b,20)
            r+=1
    

    l2=CTkLabel(f0,text="Complain Section",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)
    new_f=CTkScrollableFrame(f0,width=240,height=535,fg_color="white",border_width=2,corner_radius=12,border_color="black")
    new_f.place(x=40,y=100)
    animate_frame(new_f)
    cursor=db.cursor()
    cursor.execute('select distinct(depart) from complain where `to`=%s',("Admin"))
    depart=cursor.fetchall()
    departments=[]
    for i in range(len(depart)):
        new=depart[i]
        departments.append(new['depart'])
    buttons_complain=[]
    r=0
    y_pad=0
    for i in departments:
        new_b=CTkButton(new_f,hover_color="#D9D9D0",text=i,height=45,width=200,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        new_b.grid(row=r,column=1,padx=10,pady=y_pad+10)
        new_b.configure(command=lambda param=i,new_b=new_b: show_complains(new_b, param))
        animate_text(new_b,20)
        buttons_complain.append(new_b)
        r+=1
    buttons_complain[0].invoke()




#----------------------------------------------------------------Admin's Main Window----------------------------------------------------------------


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
# admin_win.iconbitmap("logo_icon.ico")

frame=CTkFrame(admin_win,width=1900,height=1000,fg_color="#66B3FF")
frame.pack()

#Home frame
f0=CTkFrame(frame,width=1200,height=700,fg_color="#66B3FF")
f0.place(x=140,y=20)

#Dashboard
f1=CTkFrame(frame,width=100,height=655,fg_color="white",border_width=3,corner_radius=15,border_color="black")
f1.place(x=50,y=30)

#logo
photo=CTkImage(Image.open("logo.png"),size=(60,60))
l1=CTkLabel(f1,image=photo,text=" ")
l1.place(x=18,y=40)

#home indicator
home_indicate=CTkLabel(f1,fg_color="white",text=" ",height=55,width=2,corner_radius=9)
home_indicate.place(x=7,y=150)

#student indicator
student_indicate=CTkLabel(f1,fg_color="white",text=" ",height=55,width=2,corner_radius=9)
student_indicate.place(x=7,y=250)

#teacher indicator
teacher_indicate=CTkLabel(f1,fg_color="white",text=" ",height=55,width=2,corner_radius=9)
teacher_indicate.place(x=7,y=350)

#timetable indicator
timetable_indicate=CTkLabel(f1,fg_color="white",text=" ",height=55,width=2,corner_radius=9)
timetable_indicate.place(x=7,y=450)

#complain indicator
complain_indicate=CTkLabel(f1,fg_color="white",text=" ",height=55,width=2,corner_radius=9)
complain_indicate.place(x=7,y=550)

#to initialize the admin_win
indicate(home_indicate,home_frame)

#home button
photo1=CTkImage(Image.open("home.png"),size=(50,50))
b1=CTkButton(f1,command=lambda: indicate(home_indicate,home_frame),image=photo1,text="",hover_color="#white",cursor="hand2",width=15,height=40,fg_color="white")
b1.place(x=17,y=150)
ToolTip(b1,msg="Home",delay=0)


#student button
photo2=CTkImage(Image.open("college.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(student_indicate,student_frame),image=photo2,text=" ",hover_color="#white",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=250)
ToolTip(b2,msg="Student Section",delay=0)


#teacher button 
photo3=CTkImage(Image.open("class.png"),size=(50,50))
b3=CTkButton(f1,command=lambda: indicate(teacher_indicate,teacher_frame),image=photo3,text=" ",hover_color="#white",cursor="hand2",width=15,height=40,fg_color="white")
b3.place(x=15,y=350)
ToolTip(b3,msg="Teacher Section",delay=0)


#timetable button 
photo4=CTkImage(Image.open("timetable.png"),size=(50,50))
b4=CTkButton(f1,command=lambda: indicate(timetable_indicate,teacher_assign_frame),image=photo4,text=" ",hover_color="#white",cursor="hand2",width=15,height=40,fg_color="white")
b4.place(x=15,y=450)
ToolTip(b4,msg="Teacher Assignment",delay=0)


#complain button
photo4=CTkImage(Image.open("report.png"),size=(50,50))
b5=CTkButton(f1,command=lambda: indicate(complain_indicate,complain_frame),image=photo4,text=" ",hover_color="#white",cursor="hand2",width=15,height=40,fg_color="white")
b5.place(x=15,y=550)
ToolTip(b5,msg="Complain Section")

admin_win.mainloop()