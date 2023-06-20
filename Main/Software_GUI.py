from customtkinter import *
import pymysql
from datetime import * 
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import time 
import wikipedia
import random
import speech_recognition as sr
import pyttsx3
#-------------------------------------------database connection------------------------------------------------------------------------------------

db=pymysql.connect(host='localhost',user='root',password='root',database="student_database",charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#-------------------------------------------------Global-----------------------------------------------------------------------------

current_image = 0
query="select * from student"
admin_stat=False
student_stat=True
teacher_stat=False
student_id=1
teacher_id=1
#---------------------------------------login pages code starts here-----------------------------------------------------------------------------------------------

def login_page():
    # Toggle password visibility
    def toggle_password():
        if e2.cget("show") =="*":
            e2.configure(show="")
            peek1.configure(image=img5)
        elif e2.cget("show")=="":
            e2.configure(show="*")
            peek1.configure(image=img4, fg_color="#e0e0eb")

    
    # validation of login and password  
    def validate_login():
        global query,db,admin_stat,student_stat,teacher_stat,student_id,teacher_id
        cursor=db.cursor()
        cursor.execute(query)
        data=cursor.fetchall()
        num=len(data)
        username = e1.get()
        password = e2.get()
        if username=="" :
            flash_message("Please enter a username")
            #tk.messagebox.showerror("WARNING","PLEASE! ENTER A USERNAME")
            return 0
        elif password=="" :
            flash_message("Please enter a password")
            #tk.messagebox.showerror("WARNING","PLEASE! ENTER A PASSWORD")  
            return 0  

        access=False
        for i in range(0,num):
                
            user=data[i]
            username_data=user['username']
            password_data=user['password']
            if username == username_data and password == password_data:
                access=True
                if teacher_stat==True:
                    teacher_id=user["teacher_id"]
            
                if student_stat==True:
                    student_id=user["stud_id"]
                    
                break

        # Massagebox username and password
        if access == True:
            #Opening main pages
            tk.messagebox.showinfo("Login successful!", "Welcome back, " + username + " !")
            window.destroy()
            if teacher_stat:
                teacher_page(teacher_id)
            elif admin_stat:
                admin_page()
            else :
                student_page(student_id)
        else:
            tk.messagebox.showerror("Invalid username or password", "Please try again.")
            e2.delete(0, END)


    def clear_entry():
        if len(e1.get())!=0  or len(e2.get())!=0:
            e1.delete(0, END)
            e2.delete(0, END)


    def blind_password():
        if e2.cget("show")=="":
            e2.configure(show="*")
            peek1.configure(image=img4, fg_color="#e0e0eb")


    
    
    
    def flash_message(text):
        mass_lab.config(text=text)
        window.update()
        mass_lab.after(3000)
        mass_lab.config(text="")
        window.update()

    def change_image(direction):
        global current_image,query,admin_stat,student_stat,teacher_stat
        
        current_image += direction
        
        if current_image > 2:
            current_image = 0
        elif current_image < 0:
            current_image = 2
        
        # Change the image in the label widget
        if current_image == 0:
            b2.configure(state="normal",fg_color="#3b8ed0",text="SIGN UP")
            b1.place(x=50,y=240)
            image_label.configure(image=img1)
            clear_entry()
            student_stat=True
            admin_stat=False
            teacher_stat=False
            blind_password()
            query="select * from student"
            l1.configure(text="STUDENTS LOGIN")
            
        
        elif current_image == 1:
            b2.configure(state="disabled",fg_color="#e0e0eb",text="")
            b1.place(x=127,y=240)
            image_label.configure(image=img2)
            clear_entry() 
            student_stat=False
            admin_stat=True
            teacher_stat=False   
            blind_password()
            query="select * from admin"
            l1.configure(text="ADMIN LOGIN")
            
        else:
            b2.configure(state="disabled",fg_color="#e0e0eb",text="")
            b1.place(x=127,y=240)
            image_label.configure(image=img3)
            clear_entry() 
            admin_stat=False
            student_stat=False
            teacher_stat=True
            blind_password()
            query="select * from teacher"
            l1.configure(text="TEACHERS LOGIN")


    def sign_up():
        def flash_message1(text):
            success_label.configure(text=text)
            signup_win.update()
            time.sleep(2)
            success_label.configure(text="")
            signup_win.update()
    
        def submit_form():
            
            try:
                exist=False
                stud_id = stud_id_entry.get()
                username = user_entry.get()
                password = pass_entry.get()
                Cpass = Cpass_entry.get()
                cursor = db.cursor()
                cursor.execute("select stud_id from student")
                data_id=cursor.fetchall()

                for i in range(0,len(data_id)):
                    user=data_id[i]
                    user_id=user["stud_id"]  
                    if int(stud_id)==int(user_id):
                        exist=True
                
                if password==Cpass and username!="" and password!="" and Cpass!="" and stud_id!=""and exist==True:
                    query1 = "update student set username=%s,password=%s where stud_id=%s"
                    val = (username, password,stud_id)
                    cursor = db.cursor()
                    cursor.execute(query1, val)
                    db.commit()
                    success_label.configure(text_color='green')
                    flash_message1("Registration successful")
                    
                    stud_id_entry.delete(0, END)
                    user_entry.delete(0, END)
                    pass_entry.delete(0, END)
                    Cpass_entry.delete(0, END)
                    
                elif password!=Cpass:
                    success_label.configure(text_color='red')
                    flash_message1("Passwords don't match. Please check and try again.")
                elif exist==False:
                    success_label.configure(text_color='red')
                    flash_message1("Invaild Sdudent ID")
                else:
                    success_label.configure(text_color='red')
                    flash_message1("Please Try Again.")
                
            except:
                success_label.configure(text_color='red')
                flash_message1("Try again")



        def check_strength(password):
            score = 0
            length = len(password)
            
            if length >= 8 and length <= 15:
                score += 1
            #uppercase letters
            if any(c.isupper() for c in password):
                score += 1
            #lowercase letters
            if any(c.islower() for c in password):
                score += 1
            #check digits
            if any(c.isdigit() for c in password):
                score += 1
            #check symbols
            if any(c in "!@#$%^&*()_+{}[];:'\"<>,.?/|\\" for c in password):
                score += 1
            
            return score

        def show_strength(event):
            password = pass_entry.get()
            strength = check_strength(password)
            if strength < 2:
                strength_label.configure(text="Weak",text_color="red")
            elif strength < 4:
                strength_label.configure(text="Moderate",text_color="#ff9900")
            else:
                strength_label.configure(text="Strong",text_color="green")
        
        signup_win = CTk()
        signup_win.title("SIGN UP FORM")

        # Set the size of the window
        window_width = 390
        window_height = 470
        signup_win.geometry(f"{window_width}x{window_height}")


        screen_width = signup_win.winfo_screenwidth()
        screen_height = signup_win.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        signup_win.geometry(f"+{x}+{y}")


        screen=CTkFrame(signup_win,width=390,height=470,fg_color="#c2c2d6")
        screen.place(relx=0.5,rely=0.5,anchor=CENTER)

        # create header label
        header_label = CTkLabel(screen, text="SIGN UP FORM", font=("Arial", 18))
        header_label.place(relx=0.5,y=30,anchor=CENTER)

        # create input fields
        stud_id_label = CTkLabel(screen, text="Student_ID :", font=("Arial", 12))
        stud_id_label.place(x=100, y=100,anchor=CENTER)
        stud_id_entry = CTkEntry(screen, font=("Arial", 12))
        stud_id_entry.place(x=250, y=100,anchor=CENTER)

        user_label = CTkLabel(screen, text="Username :", font=("Arial", 12))
        user_label.place(x=100, y=150,anchor=CENTER)
        user_entry = CTkEntry(screen, font=("Arial", 12))
        user_entry.place(x=250, y=150,anchor=CENTER)
        
        strength_label=CTkLabel(screen,text="",width=130,height=11,bg_color="#c2c2d6")
        strength_label.place(x=250,y=224,anchor=CENTER)

        pass_lb = CTkLabel(screen, text="Password :", font=("Arial", 12))
        pass_lb.place(x=100, y=200,anchor=CENTER)
        pass_entry = CTkEntry(screen, font=("Arial", 12))
        pass_entry.place(x=250, y=200,anchor=CENTER)
        pass_entry.bind("<KeyRelease>", show_strength)
        

        Cpass_lb = CTkLabel(screen, text="Confirm Password :", font=("Arial", 12))
        Cpass_lb.place(x=100, y=250,anchor=CENTER)
        Cpass_entry = CTkEntry(screen,show="*",font=("Arial", 12))
        Cpass_entry.place(x=250, y=250,anchor=CENTER)

        # create submit button
        submit_button = CTkButton(screen, text="Submit", command=submit_form, font=("Arial", 12))
        submit_button.place(relx=0.5, y=360,anchor=CENTER)

        success_label = CTkLabel(screen, text="",text_color="green" ,font=("Arial", 12))
        success_label.place(relx=0.5,y=430,anchor=CENTER)
        
        signup_win.mainloop()

    set_appearance_mode("light")
    set_default_color_theme("blue")
    window=CTk()
    screen_width = window.winfo_screenwidth()
    screen_height= window.winfo_screenheight()
    window_width = screen_width
    window_height = screen_height
    window.geometry(f"{window_width}x{window_height}")

    window.geometry("+0+0")
    window.maxsize(width=1400,height=750)
    window.minsize(width=1400,height=750)
    #window.attributes('-fullscreen',True)
    window.title("Login page")

    frame= CTkFrame(window,fg_color="white",width=1400,height=750)
    frame.place(x=0,y=0)

    img1 = CTkImage(Image.open("student.png"),size=(600,600))
    img2 = CTkImage(Image.open("admin.png"),size=(600,600))
    img3 = CTkImage(Image.open("teacher.png"),size=(600,600))

    img4=CTkImage(Image.open("closed_eye.png"),size=(27,27))
    img5=CTkImage(Image.open("open_eye.png"),size=(30,30))

    img6=CTkImage(Image.open("left_arrow.png"),size=(20,20))
    img7=CTkImage(Image.open("right_arrow.png"),size=(20,20))

    # label to display the images
    image_label = CTkLabel(frame,text="", image=img1)
    image_label.place(x=400,rely=0.5,anchor=CENTER)


    frame1=CTkFrame(frame,width=330,height=390,fg_color="#e0e0eb",corner_radius=20)
    frame1.place(relx=0.78,rely=0.48,anchor=tk.CENTER)
    l1=CTkLabel(frame1,text="STUDENTS LOGIN",font=("Century Gothic",20))
    l1.place(x=160,y=60,anchor=CENTER)

    e1=CTkEntry(frame1,height=30,width=220,placeholder_text="Username",font=("Microsoft YaHei UI light",15))
    e1.place(x=50,y=110)
    e2=CTkEntry(frame1,show = "*",height=30,width=220,placeholder_text="Password",font=("Microsoft YaHei UI light",15))
    e2.place(x=50,y=165)
    
    b2=CTkButton(frame1,width=80,text="SIGN UP",cursor="hand2",font=("Microsoft YaHei UI light",15),command=sign_up)
    b2.place(x=190,y=240)

    b1=CTkButton(frame1,width=80,text="LOGIN",cursor="hand2",font=("Microsoft YaHei UI light",15),command=validate_login)
    b1.place(x=50,y=240)
    window.bind('<Return>', lambda event=None: b1.invoke())
    
    b3=CTkLabel(frame1,width=80,text="Forget Password ?",text_color="blue", cursor="hand2",font=("Microsoft YaHei UI light",12))
    b3.place(x=50,y=293)
    peek1= CTkButton(frame1,width=20, text="",fg_color="#e0e0eb",image=img4,hover_color="#e0e0eb",font=("Arial", 12),
                    cursor="hand2", bg_color="#e0e0eb", command=toggle_password)
    peek1.place(x=270,y=160)

    mass_lab=tk.Label(frame1, text="",bg="#e0e0eb",fg="red",font=("Microsoft YaHei UI light",11))
    mass_lab.place(x=160,y=370,anchor=CENTER)

    prev_button = CTkButton(frame1,width=6,text="",fg_color="#e0e0eb" ,image=img6,hover_color="#c2c2d6",command=lambda: change_image(-1))
    prev_button.place(x=10,y=45)
    window.bind('<Left>', lambda event=None: prev_button.invoke())
    next_button = CTkButton(frame1,width=6, text="",fg_color="#e0e0eb",image=img7,hover_color="#c2c2d6",command=lambda: change_image(1))
    next_button.place(x=280,y=45)
    window.bind('<Right>', lambda event=None: next_button.invoke())
    window.mainloop()   




















#-------------------------------------------Admin_pages code starts here-------------------------------------------------------------















def admin_page():

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
        today = datetime.today()
        t_date= today.strftime("%B %d, %Y")
        #date and time 
        d_f=CTkFrame(f0,width=350,height=50,border_color="black",border_width=3,fg_color="white",corner_radius=40)
        d_f.place(x=820,y=0)
        time_lb=CTkLabel(d_f,width=110,height=30,text="",font=CTkFont("Helvetica",19),fg_color="white",corner_radius=40,text_color="black")
        time_lb.place(relx=0.8,rely=0.5,anchor=CENTER)
        date_lb=CTkLabel(d_f,text=t_date,width=150,height=30,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="white")
        date_lb.place(relx=0.3,rely=0.5,anchor=CENTER)
        ct_change()

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
        logout_indicate.configure(fg_color="white")

    #to delete frames
    def delete_frames():
        for f in f0.winfo_children():
            f.destroy()

    #home_frame
    def home_frame():
        date_time_display()
        #welcome label
        l2=CTkLabel(f0,text="Welcome Admin!",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
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
        f6=CTkFrame(f0)
        f6.place(x=300,y=100)
        rec_stu_lb=CTkLabel(f0,text="Recently added students",font=CTkFont(family="Helvetica",size=20),text_color="white")
        rec_stu_lb.place(x=950,y=70)

        def treeview():
            f8=CTkFrame(f6,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.pack()
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

            stu_table=ttk.Treeview(f8,columns=("stu_id","name","gen","std","dob","mobile"),show="headings",height=5)
            style=ttk.Style(f8)
        
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
            stu_table.column("std",width=100,anchor=CENTER)
            stu_table.column("dob",width=200,anchor=CENTER)
            stu_table.column("mobile",width=200,anchor=CENTER)


            for i in range(len(stud_id)-1,-1,-1):
                    stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i],mobile[i]))
            stu_table.pack()
        treeview()

        #recent teachers
        f6=CTkFrame(f0)
        f6.place(x=300,y=450)
        rec_stu_lb=CTkLabel(f0,text="Recently added Teahcers",font=CTkFont(family="Helvetica",size=20),text_color="white")
        rec_stu_lb.place(x=950,y=410)
        
        def treeview():
            f8=CTkFrame(f6,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.pack()
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

            stu_table=ttk.Treeview(f8,columns=("t_id","name","gen","quali","dob"),show="headings",height=3)
            style=ttk.Style(f8)
        
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
            stu_table.column("gen",width=70,anchor=CENTER)
            stu_table.column("quali",width=200,anchor=CENTER)
            stu_table.column("dob",width=300,anchor=CENTER)

            for i in range(len(stud_id)-1,-1,-1):
                    stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i]))
            stu_table.pack()
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
            f9=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f9.place(x=300,y=100)
            f8=CTkFrame(f9,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.pack()
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
            stu_table=ttk.Treeview(f8,columns=("stu_id","name","gen","std","dob","mobile"),show="headings")
            style=ttk.Style(f8)
        

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
            stu_table.column("dob",width=200,anchor=CENTER)
            stu_table.column("mobile",width=200,anchor=CENTER)


            for i in range(len(stud_id)-1,-1,-1):
                    stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i],mobile[i]))
            stu_table.pack()
        


        def stu_hide_hover():
            vie_stu.configure(fg_color="#33CCFF")
            add_stu.configure(fg_color="#33CCFF")
            up_stu.configure(fg_color="#33CCFF")
            del_stu.configure(fg_color="#33CCFF")
            
        #view details
        def vie_stud():
            stu_hide_hover()
            vie_stu.configure(fg_color="#888888")
            treeview()

        treeview()
        vie_stu=CTkButton(f3,hover_color="#888888",command=vie_stud,text="View Students",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        vie_stu.place(x=120,y=45,anchor=CENTER)

        #add student
        def add_stud():
            stu_hide_hover()
            add_stu.configure(fg_color="#888888")
            f8=CTkFrame(f0,width=900,height=535,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=300,y=100)
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

            add_et=CTkEntry(f8,corner_radius=10,height=100,width=200,border_width=2,font=("Roboto",12))
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

            def submit():
                    global db
                    try:
                        id=id_et.get()
                        name=name_et.get()
                        gen=gender.get()
                        std=std_op.get()
                        dob=date_et.get()
                        phone=mobi_et.get()
                        add=add_et.get()
                        cursor=db.cursor()
                        cursor.execute("insert into student(stud_id,name,gen,std_code,dob,phone_no,address) values(%s,%s,%s,%s,%s,%s,%s)",(id,name,gen,std,dob,phone,add))
                        db.commit()
                    except:
                        flash_massa.configure(text_color="red")
                        flash_message2("Try Again",flash_massa)
                    else:
                        flash_message2("Student Added Successfully",flash_massa)

            sub_bt=CTkButton(f8,text="Submit",command=submit,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
            sub_bt.place(x=470,y=470,anchor=CENTER)

        add_stu=CTkButton(f3,hover_color="#888888",command=add_stud,text="Add student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        add_stu.place(relx=0.5,y=120,anchor=CENTER)

        #remove student
        def del_stud():
            stu_hide_hover()
            del_stu.configure(fg_color="#888888")
            f8=CTkFrame(f0,width=900,height=535,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=300,y=100)

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
                    cursor=db.cursor()
                    cursor.execute("Select stud_id from Student")
                    data=cursor.fetchall()
                    flag=False
                    for i in range(0,len(data)):
                        id=data[i]
                        st_id=id["stud_id"]
                        if int(st_id)==int(stu_id):
                            flag=True
            
                    if flag==True:
                        cursor.execute("delete from student where stud_id=%s",(stu_id))
                        db.commit()
                        flash_massa.configure(text_color="green")
                        flash_message2("Student Removed Successfully",flash_massa)
                    else:
                        flash_massa.configure(text_color="red")
                        flash_message2("Student doesn't exist of the given id",flash_massa)

            del_bt=CTkButton(f8,text="Remove",hover_color="#888888",command=remove_stu,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
            del_bt.place(x=470,y=200,anchor=CENTER)

        del_stu=CTkButton(f3,hover_color="#888888",command=del_stud,text="Remove student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        del_stu.place(x=120,y=195,anchor=CENTER)

        #update student
        def up_stud():
            stu_hide_hover()
            up_stu.configure(fg_color="#888888")
            f8=CTkFrame(f0,width=900,height=535,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=300,y=100)

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
                mobi_et.insert(0,phone)
                name_et.insert(0,name)
                add_et.insert(0,add)
                date_et.insert(0,dob)
                gender.set(gen)
                std_op.set(std_code)
            
            fet_bt=CTkButton(f8,text="fetch",command=fetch,hover_color="#888888",height=20,width=60,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
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

            add_et=CTkEntry(f8,corner_radius=10,height=100,width=200,border_width=2,font=("Roboto",12))
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
                    try:
                        id=id_et.get()
                        name=name_et.get()
                        gen=gender.get()
                        std=std_op.get()
                        dob=date_et.get()
                        phone=mobi_et.get()
                        add=add_et.get()
                        cursor=db.cursor()
                        print(name,gen,std,dob)
                        cursor.execute("Update student set name=%s,gen=%s,std_code=%s,dob=%s,phone_no=%s,address=%s where stud_id=%s",(name,gen,std,dob,phone,add,id))
                        db.commit()
                    except:
                        flash_massa.configure(text_color="red")
                        flash_message2("Try Again",flash_massa)
                    else:
                        flash_message2("Student Updated Successfully",flash_massa)


            up_bt=CTkButton(f8,text="Update",command=update,hover_color="#888888",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
            up_bt.place(x=470,y=470,anchor=CENTER)

        up_stu=CTkButton(f3,hover_color="#888888",command=up_stud,text="update student",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
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
            f9=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f9.place(x=300,y=100)
            f8=CTkFrame(f9,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.pack()
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

            stu_table=ttk.Treeview(f8,columns=("t_id","name","gen","quali","dob"),show="headings")
            style=ttk.Style(f8)
        

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
            stu_table.column("gen",width=70,anchor=CENTER)
            stu_table.column("quali",width=200,anchor=CENTER)
            stu_table.column("dob",width=300,anchor=CENTER)

            for i in range(len(stud_id)-1,-1,-1):
                    stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i]))
            stu_table.pack()

        #view details
        def view_teach():
            teach_hide_hover()
            vie_te.configure(fg_color="#888888")
            treeview()
        treeview()

        vie_te=CTkButton(f3,text="View Teachers",hover_color="#888888",command=view_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        vie_te.place(x=120,y=45,anchor=CENTER)


        #add teacher
        def add_teach():
            teach_hide_hover()
            add_t.configure(fg_color="#888888")
            f8=CTkFrame(f0,width=900,height=535,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=300,y=100)
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

            add_et=CTkEntry(f8,corner_radius=10,height=70,width=200,border_width=2,font=("Roboto",12))
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
                    try:
                        flash_message2("Teacher Added Successfully",flash_massa)
                        id=id_et.get()
                        name=name_et.get()
                        gen=gender.get()
                        quali=quali_op.get()
                        dob=date_et.get()
                        phone=mobi_et.get()
                        address=add_et.get()
                        username=user_et.get()
                        password=pass_et.get()
                        cursor=db.cursor()
                        cursor.execute("insert into teacher values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,name,gen,quali,dob,phone,address,username,password))
                        db.commit()
                    except :
                        flash_massa.configure(text_color="red")
                        flash_message2("Try Again")

            sub_bt=CTkButton(f8,text="Submit",command=submit,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
            sub_bt.place(x=470,y=470,anchor=CENTER)
        add_t=CTkButton(f3,text="Add Teacher",hover_color="#888888",command=add_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        add_t.place(x=120,y=120,anchor=CENTER)

        #remove teacher

        def del_teach():
            teach_hide_hover()
            del_t.configure(fg_color="#888888")
            f8=CTkFrame(f0,width=900,height=535,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=300,y=100)

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

            del_bt=CTkButton(f8,text="Remove",hover_color="#888888",command=remove_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
            del_bt.place(x=470,y=200,anchor=CENTER)
        del_t=CTkButton(f3,text="Remove Teacher",hover_color="#888888",command=del_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        del_t.place(x=120,y=195,anchor=CENTER)

        #update teacher
        def up_teach():
            teach_hide_hover()
            up_t.configure(fg_color="#888888")
            f8=CTkFrame(f0,width=900,height=535,fg_color="#96DED1",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=300,y=100)
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
            
            fet_bt=CTkButton(f8,text="fetch",command=fetch,hover_color="#888888",height=20,width=60,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
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
                    try:
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
                        cursor.execute("Update teacher set name=%s,gen=%s,quali=%s,dob=%s,phone_no=%s,address=%s,username=%s,password=%s where teacher_id=%s",(name,gen,std,dob,phone,add,user,passwd,id))
                        db.commit()
                    except:
                        flash_massa.configure(text_color="red")
                        flash_message2("Try Again",flash_massa)
                    else:
                        flash_message2("Teacher Updated Successfully",flash_massa)


            up_bt=CTkButton(f8,text="Update",command=update,hover_color="#888888",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
            up_bt.place(x=470,y=470,anchor=CENTER)

        up_t=CTkButton(f3,text="Update Teacher",hover_color="#888888",command=up_teach,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
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
            f9=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f9.place(x=300,y=100)
            f8=CTkFrame(f9,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.pack()
            cursor=db.cursor()
            cursor.execute("SELECT teacher.name,subject.sub_name From teacher,class,teach_class,subject where teacher_id=teacher_code and sub_id=sub_code and std_id=std_code and std_id=%s",(std_code))
            data=cursor.fetchall()
            teach_name=[]
            subject_name=[]

            for i in data:
                    teacher_name=i.get("name")
                    sub_name=i.get("sub_name")
                    teach_name.append(teacher_name)
                    subject_name.append(sub_name)

            stu_table=ttk.Treeview(f8,columns=("teach_name","subject_name"),show="headings")
            style=ttk.Style(f8)
        
            style.theme_use("clam")
            style.configure("Treeview",rowheight=50,font=("Roboto"),background="#96DED1",fieldbackground="#96DED1", foreground="black")
            style.configure("Treeview.Heading",font=("Roboto"))
            stu_table.heading("teach_name",text="Teacher Name")
            stu_table.heading("subject_name",text="Subject")
            stu_table.column("teach_name",width=300,anchor=CENTER)
            stu_table.column("subject_name",width=300,anchor=CENTER)

            for i in range(len(teach_name)-1,-1,-1):
                    stu_table.insert(parent="",index=0,values=(teach_name[i],subject_name[i]))
            stu_table.pack()
        
        def std5():
            treeview("5th std")
        def std6():
            treeview("6th std")
        def std7():
            treeview("7th std")
        def std8():
            treeview("8th std")
        def std9():
            treeview("9th std")
        def std10():  
            treeview("10th std") 

        std_5=CTkButton(f3,hover_color="#888888",command=std5,text="5th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        std_5.place(relx=0.5,y=45,anchor=CENTER)

        std_6=CTkButton(f3,hover_color="#888888",command=std6,text="6th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        std_6.place(relx=0.5,y=120,anchor=CENTER)

        std_7=CTkButton(f3,hover_color="#888888",command=std7,text="7th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        std_7.place(relx=0.5,y=195,anchor=CENTER)

        std_8=CTkButton(f3,hover_color="#888888",command=std8,text="8th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        std_8.place(relx=0.5,y=270,anchor=CENTER)

        std_9=CTkButton(f3,hover_color="#888888",command=std9,text="9th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        std_9.place(relx=0.5,y=345,anchor=CENTER)

        std_10=CTkButton(f3,hover_color="#888888",command=std10,text="10th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        std_10.place(relx=0.5,y=420,anchor=CENTER)
        

    #logout_frame
    def logout_frame():
        date_time_display()
        def destroy_window():
            admin_win.destroy()
            login_page()
            #asking to logout
        log_lb=CTkLabel(f0,text="Do you want to logout ?",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        log_lb.place(relx=0.5,y=200,anchor=CENTER)
        log_bu=CTkButton(f0,text="Yes",height=45,command=destroy_window,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        log_bu.place(relx=0.5,y=300,anchor=CENTER)

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

    #logout indicator
    logout_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    logout_indicate.place(x=10,y=550)

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

    #logout button 
    photo4=CTkImage(Image.open("logout.png"),size=(50,50))
    b2=CTkButton(f1,command=lambda: indicate(logout_indicate,logout_frame),image=photo4,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
    b2.place(x=15,y=550)

    admin_win.mainloop()













#-----------------------------------------STUDENT_PAGE'S CODE STARTS HERE-----------------------------------------------------------



















def student_page(student_id):


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
            today = datetime.today()
            t_date= today.strftime("%B %d, %Y")
            #date and time 
            d_f=CTkFrame(f0,width=350,height=50,border_color="black",border_width=3,fg_color="white",corner_radius=40)
            d_f.place(x=820,y=30)
            time_lb=CTkLabel(d_f,width=110,height=30,text="",font=CTkFont("Helvetica",19),fg_color="white",corner_radius=40,text_color="black")
            time_lb.place(relx=0.8,rely=0.5,anchor=CENTER)
            date_lb=CTkLabel(d_f,text=t_date,width=150,height=30,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="white")
            date_lb.place(relx=0.3,rely=0.5,anchor=CENTER)
            ct_change()

    #Treeview
    def treeview():
            f8=CTkFrame(f0,width=1140,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=55,y=150)
            cursor=db.cursor()
            cursor.execute("SELECT teacher.teacher_id,teacher.name,teacher.quali ,teacher.phone_no,subject.sub_name FROM teacher, class , teach_class , subject where teacher_id=teacher_code and sub_id=sub_code and std_id=std_code and std_id=%s",(Std))
            data=cursor.fetchall()
            teach_id=[]
            teach_name=[]
            teach_quali=[]
            teach_phone=[]
            subject_name=[]


            for i in data:
                    teacher_id=i.get("teacher_id")
                    teacher_name=i.get("name")
                    teacher_quali=i.get("quali")
                    sub_name=i.get("sub_name")
                    
                    teach_id.append(teacher_id)
                    teach_name.append(teacher_name)
                    teach_quali.append(teacher_quali)
                    subject_name.append(sub_name)

            stu_table=ttk.Treeview(f8,columns=("teach_id","teach_name","teach_quali","subject_name"),show="headings")
            style=ttk.Style(f8)
        
            style.theme_use("clam")
            style.configure("Treeview",rowheight=60,font=("Roboto"),background="#96DED1",fieldbackground="#96DED1", foreground="black")
            style.configure("Treeview.Heading",font=("Roboto"))
            stu_table.heading("teach_id",text="Teacher_id")
            stu_table.heading("teach_name",text="Teacher_name")
            stu_table.heading("teach_quali",text="Teacher_quali")
            stu_table.heading("subject_name",text="Subject")

            stu_table.column("teach_id",width=290,anchor=CENTER)
            stu_table.column("teach_name",width=290,anchor=CENTER)
            stu_table.column("teach_quali",width=290,anchor=CENTER)

            stu_table.column("subject_name",width=290,anchor=CENTER)

            for i in range(len(teach_name)-1,-1,-1):
                    stu_table.insert(parent="",index=0,values=(teach_id[i],teach_name[i],teach_quali[i],subject_name[i]))
            stu_table.pack()



    #talk
    speaking=False
    def talk():
        global speaking
        engine=pyttsx3.init()
        if speaking:
            engine.stop()
            speaking = False
        else:
            speaking = True
            engine.say(summary)
            engine.runAndWait()
            



    #Search Ingne
    def search_ig():
        input = CTkEntry(f0, width = 350,height=40,font=("halvetica",20),fg_color="#ffe6cc",text_color="black",border_width=3,corner_radius=12,border_color="black",placeholder_text=" Search with StudentHub",placeholder_text_color="grey")
        input.place(x=100,y=90)

        result=''
        



        def listen():
            tk.messagebox.showinfo("Speak", "Listening...")
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)  
                audio = r.listen(source, timeout=1) 
                
            try:
                result = r.recognize_google(audio)
                input.delete(0, END)
                input.insert(0, result)
                engine = pyttsx3.init()
                engine.setProperty('rate', 150) 
                engine.say("You said " + result)  
                engine.runAndWait()
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))



        def search():
            global result,summary
            result = input.get()
            summary = wikipedia.summary(result, sentences=3)
            text.delete('1.0', END) # clear the text widge
            text.insert('1.0',summary)


        f8=CTkFrame(f0,width=1140,height=501,fg_color="white",border_width=3,corner_radius=2,border_color="black")
        text = tk.Text(f8,font =('halvetica',20),width=94,borderwidth=2,yscrollcommand=10,background="#ffe6cc")

        photo7=CTkImage(Image.open("search_logo.png"),size=(30,30))
        button5 = CTkButton(f0,image=photo7,text='',width=50,height=40,fg_color="#e0e0eb")
        button5.configure(command=search)                                                 
        button5.place(x=450,y=90)

        photo8 = CTkImage(Image.open("mic.png"), size=(30, 30))
        button5 = CTkButton(f0, image=photo8, text='', width=50, height=40, fg_color="#e0e0eb",command=listen)
        button5.place(x=510, y=90)

        photo8 = CTkImage(Image.open("speaker.png"), size=(30, 30))
        button5 = CTkButton(f0, image=photo8, text='', width=50, height=40, fg_color="#e0e0eb",command=talk)
        button5.place(x=570, y=90)

        text.place(x=2,y=0)
        f8.place(x=70,y=140)




    #quotes
    def quotes():
        try:
            # create a list of quotes
            quotes = [
                "Be the change you wish to see in the world.",
                "The only way to do great work is to love what you do.",
                "Not all who wander are lost.",
                "Believe you can and you're halfway there.",
                "If you want to go fast, go alone. If you want to go far, go together.",
                "It does not matter how slowly you go as long as you do not stop.",
                "Life is what happens when you're busy making other plans.",
                "It is during our darkest moments that we must focus to see the light.",
                "You must be the change you wish to see in the world.",
                "The future belongs to those who believe in the beauty of their dreams.",
                "The best way to predict the future is to invent it."]

            # randomly select a quote from the list
            selected_quote = random.choice(quotes)

            label=CTkLabel(f6,text=selected_quote ,width=40,height=50,font=("bold",18),text_color="black",bg_color="transparent")
            label.place(relx=0.5,rely=0.7,anchor=CENTER)
            quotes_lb=CTkLabel(f6,text="Thought of the day!",width=50,height=20,font=("bold",30),text_color="black",bg_color="transparent")
            quotes_lb.place(relx=0.5,rely=0.3,anchor=CENTER)
            quotes_wall=CTkImage(Image.open("qoutes_bg.png"),size=(70,70))
            quotes_wlb=CTkLabel(f6,text="",image=quotes_wall,width=50,height=20,bg_color="transparent")
            quotes_wlb.place(relx=0.1,rely=0.27,anchor=CENTER)
        except Exception as e:
            pass

    #identiy card
    def id_card(student_id):
        global f6,Std
        cursor=db.cursor()
        query1=f"Select * from student where stud_id={student_id}"
        cursor.execute(query1)
        s_data=cursor.fetchall()
        data1=s_data[0]
            
            
            
        su_id=data1.get("stud_id")
        Name=data1.get("name")
        Dob=data1.get("dob")
        Std=data1.get("std_code")
        Address=data1.get("address")
        mobile=data1.get("phone_no")

        l2=CTkLabel(f0,text=("Welcome "+ Name),font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        l2.place(x=55,y=20)

        #attendence graph 
        f6=CTkFrame(f0,width=550,height=180,fg_color="#ffe6cc",border_width=3,corner_radius=12,border_color="black")
        f6.place(x=55,y=90)
        quotes()
        f7=CTkFrame(f0,width=590,height=380,fg_color="#ffffe6",border_width=3,corner_radius=12,border_color="black")
        f7.place(x=630,y=90)
            
        photo5=CTkImage(Image.open("id_back.png"),size=(575,170))
        l3=CTkLabel(f7,image=photo5,text="")
        l3.place(x=6,y=5)
        photo6=CTkImage(Image.open("background.jpeg"),size=(575,20))
        l3=CTkLabel(f7,image=photo6,text="")
        l3.place(x=7,y=347)

        f9=CTkFrame(f7,width=160,height=160,border_width=3,corner_radius=12,border_color="black")
        f9.place(x=310,y=110)

        photo6=CTkImage(Image.open("student_photo.png"),size=(150,150))
        l4=CTkLabel(f7,image=photo6,text=" ")
        l4.place(x=315,y=115)

        photo7=CTkImage(Image.open("logo2.png"),size=(70,70))
        l5=CTkLabel(f7,image=photo7,text=" ",bg_color='#6FD0FE')
        l5.place(x=60,y=15)

        l6=CTkLabel(f7,text="IDENTITY CARD",bg_color='#6FD0FE',font=("Helvetica",25),text_color="black")
        l6.place(x=170,y=33)

        id_lb=CTkLabel(f7,text=("STU.ID :  " + str(su_id)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        id_lb.place(x=15,y=135)

        name_lb=CTkLabel(f7,text=("NAME :   " + Name),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        name_lb.place(x=15,y=170)

        dob_lb=CTkLabel(f7,text=("DOB    :  " + str(Dob)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        dob_lb.place(x=15,y=205)

        std_lb=CTkLabel(f7,text=("STD    :  "+ Std),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        std_lb.place(x=15,y=240)

        mobile_lb=CTkLabel(f7,text=("MOBILE NO. :  " + str(mobile)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        mobile_lb.place(x=15,y=275)

        address_lb=CTkLabel(f7,text=("ADDRESS :  " + Address),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        address_lb.place(x=15,y=310)

    #to delete frames
    def delete_frames():
        for f in f0.winfo_children():
            f.destroy()

    #to indicate
    def indicate(lb,frame):
        hide_indicators()
        lb.configure(fg_color="#0066ff")
        delete_frames()
        frame()

    #hide indicators
    def hide_indicators():
        home_indicate.configure(fg_color="white")
        student_indicate.configure(fg_color="white")
        teacher_indicate.configure(fg_color="white")
        logout_indicate.configure(fg_color="white")


    #--------------------------------------------home frames code -----------------------------------------------------------------------------------


    #home_frame
    def home_frame(): 
        #date and time 
        id_card(student_id)
        date_time_display()
        f8=CTkFrame(f0,width=550,height=350,fg_color="#ccb3ff",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=55,y=300)
        l2=CTkLabel(f8,text="About School!",font=CTkFont(family="Helvetica",weight="bold",size=30),text_color="black")
        l2.place(x=40,y=30)
        about_text=CTkLabel(f8,text="\nSince 1982 we are working for education to strengthen the \nfuture of our all dear children.We aim to work in building 21st\ncentury skills as it is the call of the modernised future.Our\nVision is to provide education at an impactable scale\nand create the education awareness as far as possible.",font=CTkFont(family="Helvetica",size=20),height=200,width=40,text_color="black",bg_color="#ccb3ff")
        about_text.place(x=5,y=75)

    #student_frame
    def student_frame():
        global result

        #date and time 
        date_time_display()
        #student section
        l2=CTkLabel(f0,text="Search with StudentHub",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        l2.place(x=55,y=20)
        search_ig()


    #-------------------------------------------------------------Taught_frame-----------------------------------------------------------------------


    #Taught by teacher
    def Schedule():
        #date and time 
        date_time_display()

        #teacher_section
        l2=CTkLabel(f0,text="Taught by!",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        l2.place(x=55,y=20)

        #table to see teacher details 
        
        treeview()
        
    #logout_frame
    def logout_frame():
        date_time_display()
        def destroy_student():
            student_win.destroy()
            login_page()
        #asking to logout
        log_lb=CTkLabel(f0,text="Do you want to logout ?",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        log_lb.place(relx=0.4,y=200,anchor=CENTER)
        log_bu=CTkButton(f0,text="Yes",height=45,command=destroy_student,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        log_bu.place(relx=0.4,y=300,anchor=CENTER)


    #------------------------------------------------------main window code ----------------------------------------------------------------------


    #main window
    def main_window():
        global f0,student_id,home_indicate,student_indicate,teacher_indicate,logout_indicate,student_win
        set_appearance_mode("light")
        set_default_color_theme("blue")
        student_win=CTk()
        student_win.title("Student home page")
        screen_width = student_win.winfo_screenwidth()
        screen_height= student_win.winfo_screenheight()
        student_win_width = screen_width
        student_win_height = screen_height
        student_win.geometry(f"{student_win_width}x{student_win_height}")
        student_win.geometry("+0+0")
        student_win.maxsize(width=1400,height=750)
        student_win.minsize(width=1400,height=750) 
        #student_win.attributes('-fullscreen',True)
        frame=CTkFrame(student_win,width=1900,height=1000,fg_color="#66B3FF")
        frame.pack()
        #Home frame
        f0=CTkFrame(frame,width=1400,height=700,fg_color="#66B3FF")
        f0.place(x=140,y=30)
        #Dashboard
        f1=CTkFrame(frame,width=100,height=680,fg_color="white",border_width=3,corner_radius=15,border_color="black")
        f1.place(x=50,y=35)
        #logo
        photo=CTkImage(Image.open("logo2.png"),size=(60,60))
        l1=CTkLabel(f1,image=photo,text=" ")
        l1.place(x=18,y=40)
        #home indicator
        home_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
        home_indicate.place(x=10,y=150)
        
        student_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
        student_indicate.place(x=10,y=250)
        
        teacher_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
        teacher_indicate.place(x=10,y=350)
        #
        logout_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
        logout_indicate.place(x=10,y=450)
        #to initialize the student_win
        indicate(home_indicate,home_frame)
        #home button
        photo1=CTkImage(Image.open("home.png"),size=(50,50))
        b1=CTkButton(f1,command=lambda: indicate(home_indicate,home_frame),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="white")
        b1.place(x=17,y=150)
        #search button
        photo2=CTkImage(Image.open("search_logo.png"),size=(50,50))
        b2=CTkButton(f1,command=lambda: indicate(student_indicate,student_frame),image=photo2,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
        b2.place(x=15,y=250)
        #taught button 
        photo3=CTkImage(Image.open("Schedule.png"),size=(50,50))
        b2=CTkButton(f1,command=lambda: indicate(teacher_indicate,Schedule),image=photo3,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
        b2.place(x=15,y=350)
        #logout button 
        photo4=CTkImage(Image.open("logout.png"),size=(50,50))
        b2=CTkButton(f1,command=lambda: indicate(logout_indicate,logout_frame),image=photo4,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
        b2.place(x=15,y=450)

        student_win.mainloop()

    main_window()










#-----------------------------------------TEACHER_PAGE'S CODE STARTS HERE-----------------------------------------------------------










def teacher_page(teacher_id):
    set_appearance_mode("light")
    set_default_color_theme("blue")
    teacher_win=CTk()
    teacher_win.title("Teacher home page")
    screen_width = teacher_win.winfo_screenwidth()
    screen_height= teacher_win.winfo_screenheight()
    teacher_win_width = screen_width
    teacher_win_height = screen_height
    teacher_win.geometry(f"{teacher_win_width}x{teacher_win_height}")
    teacher_win.geometry("+0+0")
    teacher_win.maxsize(width=1400,height=750)
    teacher_win.minsize(width=1400,height=750)
    #teacher_win.attributes('-fullscreen',True)

    frame=CTkFrame(teacher_win,width=1900,height=1000,fg_color="#66B3FF")
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
        today = datetime.today()
        t_date= today.strftime("%B %d, %Y")
        #date and time 
        d_f=CTkFrame(f0,width=350,height=50,border_color="black",border_width=3,fg_color="white",corner_radius=40)
        d_f.place(x=820,y=30)
        time_lb=CTkLabel(d_f,width=110,height=30,text="",font=CTkFont("Helvetica",19),fg_color="white",corner_radius=40,text_color="black")
        time_lb.place(relx=0.8,rely=0.5,anchor=CENTER)
        date_lb=CTkLabel(d_f,text=t_date,width=150,height=30,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="white")
        date_lb.place(relx=0.3,rely=0.5,anchor=CENTER)
        ct_change()

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
        logout_indicate.configure(fg_color="white")

    #to delete frames
    def delete_frames():
        for f in f0.winfo_children():
            f.destroy()

    def id_card(teacher_id):
        cursor=db.cursor()
        query1=f"Select * from teacher where teacher_id={teacher_id}"
        cursor.execute(query1)
        data0=cursor.fetchall()
        data1=data0[0]
            
        tr_id=data1["teacher_id"]
        Name=data1["name"]
        Dob=data1["dob"]
        quali=data1["quali"]
        Address=data1["address"]
        mobile=data1["phone_no"]

        l2=CTkLabel(f0,text=("Welcome "+ Name),font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        l2.place(x=55,y=20)
        f7=CTkFrame(f0,width=590,height=380,fg_color="#ffffe6",border_width=3,corner_radius=12,border_color="black")
        f7.place(x=580,y=100)
        photo5=CTkImage(Image.open("id_back.png"),size=(575,170))
        l3=CTkLabel(f7,image=photo5,text="")
        l3.place(x=6,y=5)
        photo6=CTkImage(Image.open("background.jpeg"),size=(575,20))
        l3=CTkLabel(f7,image=photo6,text="")
        l3.place(x=7,y=347)
        f9=CTkFrame(f7,width=160,height=160,border_width=3,corner_radius=12,border_color="black")
        f9.place(x=310,y=110)
        photo6=CTkImage(Image.open("teacher_photo.png"),size=(150,150))
        l4=CTkLabel(f7,image=photo6,text=" ")
        l4.place(x=315,y=115)
        photo7=CTkImage(Image.open("logo2.png"),size=(70,70))
        l5=CTkLabel(f7,image=photo7,text=" ",bg_color='#6FD0FE')
        l5.place(x=60,y=15)

        l6=CTkLabel(f7,text="IDENTITY CARD",bg_color='#6FD0FE',font=("Helvetica",25),text_color="black")
        l6.place(x=170,y=33)
        id_lb=CTkLabel(f7,text=("TEACHER.ID :  " + str(tr_id)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        id_lb.place(x=15,y=135)
        name_lb=CTkLabel(f7,text=("NAME :   " + Name),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        name_lb.place(x=15,y=170)
        dob_lb=CTkLabel(f7,text=("DOB    :  " + str(Dob)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        dob_lb.place(x=15,y=205)
        std_lb=CTkLabel(f7,text=("Quali. : "+ quali),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        std_lb.place(x=15,y=240)
        mobile_lb=CTkLabel(f7,text=("MOBILE NO. :  " + str(mobile)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        mobile_lb.place(x=15,y=275)
        address_lb=CTkLabel(f7,text=("ADDRESS :  " + Address),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
        address_lb.place(x=15,y=310)
        
    def quotes():
        try:
            quotes = [
                "Be the change you wish to see in the world.",
                "I have a dream.",
                "The only way to do great work is to love what you do.",
                "Not all who wander are lost.",
                "Believe you can and you're halfway there.",
                "In three words I can sum up everything I've learned about life: it goes on.",
                "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                "If you want to go fast, go alone. If you want to go far, go together.",
                "It does not matter how slowly you go as long as you do not stop.",
                "Life is what happens when you're busy making other plans.",
                "The greatest glory in living lies not in never falling, but in rising every time we fall.",
                "It is during our darkest moments that we must focus to see the light.",
                "You must be the change you wish to see in the world.",
                "The future belongs to those who believe in the beauty of their dreams.",
                "The best way to predict the future is to invent it.",
                "I can't change the direction of the wind, but I can adjust my sails to always reach my destination."]
            # randomly selecting a quote from the list
            selected_quote = random.choice(quotes)
            label = CTkLabel(board1, text=selected_quote, width=40, height=50, font=("bold", 15), text_color="white", bg_color="transparent")
            label.place(relx=0.5, rely=0.5, anchor=CENTER)
            quotes_lb = CTkLabel(board1, text=f"QUOTES :", width=50, height=20, font=("bold", 30), text_color="white", bg_color="transparent")
            quotes_lb.place(relx=0.2, rely=0.5, anchor=CENTER)
        except Exception as e:
            pass

    #home_frame
    def home_frame():
        global board1
        date_time_display()
        id_card(teacher_id)
        #welcome label


        #no of students in 5th
        cursor=db.cursor()
        cursor.execute("Select count(*) count from student where std_code=%s",("5th std"))
        data=cursor.fetchall()
        d=data[0]
        tot_st=d["count"]

        #teacher_win.update()
        f3=CTkFrame(f0,width=240,height=110,fg_color="#FFFFCC",border_width=3,corner_radius=12,border_color="black")
        f3.place(x=40,y=98)
        st_no=CTkLabel(f3,text=tot_st,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        st_no.place(x=20,y=10)
        t_st=CTkLabel(f3,text="5th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
        t_st.place(x=20,y=75)

        #no of students in 6th
        cursor=db.cursor()
        cursor.execute("Select count(*) count from student where std_code=%s",("6th std"))
        data=cursor.fetchall()
        d=data[0]
        tot_te=d["count"]
        f4=CTkFrame(f0,width=240,height=110,fg_color="#C7FAC7",border_width=3,corner_radius=12,border_color="black")
        f4.place(x=40,y=230)
        t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        t_no.place(x=20,y=10)
        t_te=CTkLabel(f4,text="6th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
        t_te.place(x=20,y=75)

        #no of students in 7th
        cursor=db.cursor()
        cursor.execute("Select count(*) count from student where std_code=%s",("7th std"))
        data=cursor.fetchall()
        d=data[0]
        tot_te=d["count"]
        f4=CTkFrame(f0,width=240,height=110,fg_color="#FFFFCC",border_width=3,corner_radius=12,border_color="black")
        f4.place(x=40,y=360)
        t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        t_no.place(x=20,y=10)
        t_te=CTkLabel(f4,text="7th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
        t_te.place(x=20,y=75)

        #no of students in 8th
        cursor=db.cursor()
        cursor.execute("Select count(*) count from student where std_code=%s",("8th std"))
        data=cursor.fetchall()
        d=data[0]
        tot_te=d["count"]
        f4=CTkFrame(f0,width=240,height=110,fg_color="#C7FAC7",border_width=3,corner_radius=12,border_color="black")
        f4.place(x=300,y=98)
        t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        t_no.place(x=20,y=10)
        t_te=CTkLabel(f4,text="8th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
        t_te.place(x=20,y=75)
        
        #no of students in 9th
        cursor=db.cursor()
        cursor.execute("Select count(*) count from student where std_code=%s",("9th std"))
        data=cursor.fetchall()
        d=data[0]
        tot_te=d["count"]
        f4=CTkFrame(f0,width=240,height=110,fg_color="#FFFFCC",border_width=3,corner_radius=12,border_color="black")
        f4.place(x=300,y=230)
        t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        t_no.place(x=20,y=10)
        t_te=CTkLabel(f4,text="9th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
        t_te.place(x=20,y=75)

        #no of students in 10th
        cursor=db.cursor()
        cursor.execute("Select count(*) count from student where std_code=%s",("10th std"))
        data=cursor.fetchall()
        d=data[0]
        tot_te=d["count"]
        f4=CTkFrame(f0,width=240,height=110,fg_color="#C7FAC7",border_width=3,corner_radius=12,border_color="black")
        f4.place(x=300,y=360)
        t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        t_no.place(x=20,y=10)
        t_te=CTkLabel(f4,text="10th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
        t_te.place(x=20,y=75)
        #Quotes
        board1=CTkFrame(f0,width=1140,height=110,fg_color="#3b3a30",border_width=5,corner_radius=12,border_color="black")
        board1.place(x=40,y=520)
        quotes()

    #student_frame
    def attendance_frame():
        date_time_display()

        #student section
        l2=CTkLabel(f0,text="Classwise Details",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        l2.place(x=40,y=30)

        #frame for buttons 
        f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f3.place(x=40,y=100)
        

        def treeview(query,val):
            f9=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f9.place(x=300,y=100)
            f8=CTkFrame(f9,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.pack()
            cursor=db.cursor()
            cursor.execute(query,val)
            data=cursor.fetchall()
            stud_id=[]
            name=[]
            gen=[]
            std=[]
            dob=[]

            for i in data:
                    id=i.get("stud_id")
                    na=i.get("name")
                    ge=i.get("gen")
                    st=i.get("std_code")
                    bir=i.get("dob")
                    stud_id.append(id)
                    name.append(na)
                    gen.append(ge)
                    std.append(st)
                    dob.append(bir)

            stu_table=ttk.Treeview(f8,columns=("stud_id","name","gen","std_code","dob"),show="headings",height=10)
            style=ttk.Style(f8)
        

            style.theme_use("clam")
            style.configure("Treeview",rowheight=50,font=("Roboto"),background="#96DED1",fieldbackground="#96DED1", foreground="black")
            style.configure("Treeview.Heading",font=("Roboto"))
            stu_table.heading("name",text="Name")
            stu_table.heading("stud_id",text="Student id")
            stu_table.heading("gen",text="Gender")
            stu_table.heading("std_code",text="Class")
            stu_table.heading("dob",text="Date of Birth")
            stu_table.column("stud_id",width=200,anchor=CENTER)
            stu_table.column("name",width=200,anchor=CENTER)
            stu_table.column("gen",width=100,anchor=CENTER)
            stu_table.column("std_code",width=100,anchor=CENTER)
            stu_table.column("dob",width=300,anchor=CENTER)

            for i in range(len(stud_id)-1,-1,-1):
                    stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i],std[i],dob[i]))
            stu_table.pack()
            
            
        def hide_hover():
            stand_5.configure(fg_color="#33CCFF")
            stand_6.configure(fg_color="#33CCFF")
            stand_7.configure(fg_color="#33CCFF")
            stand_8.configure(fg_color="#33CCFF")
            stand_9.configure(fg_color="#33CCFF")
            stand_10.configure(fg_color="#33CCFF")
            
        #view details
        def std_5():
            hide_hover()
            stand_5.configure(fg_color="#888888")
            val=("5th std",)
            query="select * from student where std_code = %s"
            treeview(query,val)


        stand_5=CTkButton(f3,hover_color="#888888",command=std_5,text="5th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_5.place(x=120,y=45,anchor=CENTER)

        def std_6():
            hide_hover()
            stand_6.configure(fg_color="#888888")
            val=("6th std",)
            query="select * from student where std_code = %s"
            treeview(query,val)
        
        stand_6=CTkButton(f3,hover_color="#888888",command=std_6,text="6th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_6.place(x=120,y=120,anchor=CENTER)


        def std_7():
            hide_hover()
            stand_7.configure(fg_color="#888888")
            val=("7th std",)
            query="select * from student where std_code = %s"
            treeview(query,val)

        stand_7=CTkButton(f3,hover_color="#888888",command=std_7,text="7th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_7.place(x=120,y=195,anchor=CENTER)

        #update student
        def std_8():
            hide_hover()
            stand_8.configure(fg_color="#888888")
            val=("8th std",)
            query="select * from student where std_code = %s"
            treeview(query,val)
        stand_8=CTkButton(f3,hover_color="#888888",command=std_8,text="8th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_8.place(x=120,y=270,anchor=CENTER)

        def std_9():
            hide_hover()
            stand_9.configure(fg_color="#888888")
            val=("9th std",)
            query="select * from student where std_code = %s"
            treeview(query,val)
        stand_9=CTkButton(f3,hover_color="#888888",command=std_9,text="9th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_9.place(x=120,y=345,anchor=CENTER)

        def std_10():
            hide_hover()
            stand_10.configure(fg_color="#888888")
            val=("10th std",)
            query="select * from student where std_code = %s"
            treeview(query,val)
        stand_10=CTkButton(f3,hover_color="#888888",command=std_10,text="10th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_10.place(x=120,y=420,anchor=CENTER)

    #teacher_frame
    def timetable_frame():
        date_time_display()
        
        def treeview():
            f9=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f9.place(x=300,y=100)
            f8=CTkFrame(f9,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.pack()
            cursor=db.cursor()
            cursor.execute("select class.std_id,subject.sub_name from teacher,class,teach_class,subject where teacher.teacher_id=teach_class.teacher_code and class.std_id=teach_class.std_code and subject.sub_id=teach_class.sub_code and teacher.teacher_id=%s",(teacher_id))
            data=cursor.fetchall()
            std_i=[]
            subject_name=[]

            for i in data:
                    teacher_name=i.get("std_id")
                    sub_name=i.get("sub_name")
                    std_i.append(teacher_name)
                    subject_name.append(sub_name)

            stu_table=ttk.Treeview(f8,columns=("std_i","subject_name"),show="headings")
            style=ttk.Style(f8)
        
            style.theme_use("clam")
            style.configure("Treeview",rowheight=50,font=("Roboto"),background="#dac292",fieldbackground="#dac292", foreground="black")
            style.configure("Treeview.Heading",font=("Roboto"))
            stu_table.heading("std_i",text="Standard")
            stu_table.heading("subject_name",text="Subject")
            stu_table.column("std_i",width=500,anchor=CENTER)
            stu_table.column("subject_name",width=500,anchor=CENTER)

            for i in range(len(std_i)-1,-1,-1):
                    stu_table.insert(parent="",index=0,values=(std_i[i],subject_name[i]))
            stu_table.pack()

        #teacher_section
        l2=CTkLabel(f0,text="Teacher's Timetable",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        l2.place(x=40,y=30)
        f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f3.place(x=40,y=100)

        #frame for buttons 

        def hide_hover():
            stand_5.configure(fg_color="#33CCFF")
            stand_6.configure(fg_color="#33CCFF")
            stand_7.configure(fg_color="#33CCFF")
        
        #view details
        def time_tb():
            hide_hover()
            stand_5.configure(fg_color="#888888")
            f8=CTkFrame(f0,width=900,height=532,fg_color="white",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=300,y=100)
            photo1=CTkImage(Image.open("timetable_img.jpg"),size=(885,495))
            lb=CTkLabel(f8,image=photo1,text="",width=890,height=500)
            lb.place(relx=0.5,rely=0.5,anchor=CENTER)

        stand_5=CTkButton(f3,hover_color="#888888",command=time_tb,text="Time Table",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_5.place(x=120,y=45,anchor=CENTER)

        def my_sub():
            hide_hover()
            stand_6.configure(fg_color="#888888")
            treeview()
        stand_6=CTkButton(f3,hover_color="#888888",command=my_sub,text="My Classes",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_6.place(x=120,y=120,anchor=CENTER)


        def about():
            hide_hover()
            stand_7.configure(fg_color="#888888")
            f8=CTkFrame(f0,width=900,height=532,fg_color="#ccb3ff",border_width=3,corner_radius=12,border_color="black")
            f8.place(x=300,y=100)
            l2=CTkLabel(f8,text="About Us!",font=CTkFont(family="Helvetica",weight="bold",size=30),text_color="black")
            l2.place(x=40,y=30)
            about_text=CTkLabel(f8,text="\nSince 1982 we are working for education to strengthen the future of our all dear children.\n\nWe aim to work in building 21st century skills as it is the call of the modernised future.\n\nOur Vision is to provide education at a impactable scale and create the education awareness\n\n as far as possible.",font=CTkFont(family="Helvetica",size=20),height=50,width=100,text_color="black")
            about_text.place(x=40,y=100)        
        stand_7=CTkButton(f3,hover_color="#888888",command=about,text="About",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        stand_7.place(x=120,y=195,anchor=CENTER)



    #to indicate
    def indicate(lb,frame):
        hide_indicators()
        lb.configure(fg_color="#0066ff")
        delete_frames()
        frame()

    #logout_frame
    def logout_frame():
        date_time_display()
        def destroy_teacher():
            teacher_win.destroy()
            login_page()
        #asking to logout
        log_lb=CTkLabel(f0,text="Do you want to logout ?",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        log_lb.place(relx=0.5,y=200,anchor=CENTER)
        log_bu=CTkButton(f0,text="Yes",height=45,command=destroy_teacher,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        log_bu.place(relx=0.5,y=300,anchor=CENTER)


    #home indicator
    home_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    home_indicate.place(x=10,y=150)

    #student indicator
    student_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    student_indicate.place(x=10,y=250)
    #teacher indicator
    teacher_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    teacher_indicate.place(x=10,y=350)
    #logout indicator
    logout_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    logout_indicate.place(x=10,y=450)
    #to initialize the teacher_win
    indicate(home_indicate,home_frame)
    #home button
    photo1=CTkImage(Image.open("home.png"),size=(50,50))
    b1=CTkButton(f1,command=lambda: indicate(home_indicate,home_frame),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="white")
    b1.place(x=17,y=150)

    #student button
    photo2=CTkImage(Image.open("attendence.png"),size=(50,50))
    b2=CTkButton(f1,command=lambda: indicate(student_indicate,attendance_frame),image=photo2,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
    b2.place(x=15,y=250)

    #teacher button 
    photo3=CTkImage(Image.open("time_table.png"),size=(50,50))
    b2=CTkButton(f1,command=lambda: indicate(teacher_indicate,timetable_frame),image=photo3,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
    b2.place(x=15,y=350)

    #logout button 
    photo4=CTkImage(Image.open("logout.png"),size=(50,50))
    b2=CTkButton(f1,command=lambda: indicate(logout_indicate,logout_frame),image=photo4,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
    b2.place(x=15,y=450)

    teacher_win.mainloop()






#---------------------------------------SPLASH SCREEN CODE START HERE---------------------------------------------------------------- 




def splash_loading():
    def load_image():
        global photo, gif_frames
        # Load the image
        image = Image.open("splash.gif")
        photo = ImageTk.PhotoImage(image)
        label.configure(image=photo)
        
        # Load the GIF image
        gif = Image.open("splash.gif")
        gif_frames = []
        try:
            while True:
                gif_frames.append(ImageTk.PhotoImage(gif))
                gif.seek(len(gif_frames))
        except EOFError:
            pass
        
        splash_root.after(0, animate, 0) 

    def animate(frame_num):
        label.configure(image=gif_frames[frame_num])
        frame_num += 1
        if frame_num == len(gif_frames):
            frame_num = 0
        splash_root.after(70, animate, frame_num)

    splash_root = CTk()
    splash_root_width = 600
    splash_root_height = 300
    splash_root.title("WELCOME!")
    splash_root.geometry(f"{splash_root_width}x{splash_root_height}")
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x = int((screen_width - splash_root_width) / 2)
    y = int((screen_height - splash_root_height) / 2)
    splash_root.geometry(f"+{x}+{y}")

    label = tk.Label(splash_root, text="")
    label.pack()

    load_image()

    def destroy_screen():
        time.sleep(1)
        splash_root.destroy()
        login_page()

    splash_root.after(5000, destroy_screen)

    splash_root.mainloop()

splash_loading()