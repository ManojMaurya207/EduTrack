from customtkinter import *
import pymysql
from datetime import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import random
from tkPDFViewer import tkPDFViewer as pdf
import webbrowser
import time



teacher_id=513
#----------------------------------------------------------------local connections----------------------------------------------------------------

#first connection 
db=pymysql.connect(host="localhost",user="root",password="root",database="student_database",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)


#----------------------------------------------------------------Universal functions----------------------------------------------------------------
def animate_frame(frame_to_animate):
    target_height = frame_to_animate.cget("height")
    frame_to_animate.configure(height=0)
    
    current_height = 0

    while current_height < target_height:
        current_height = min(current_height + 30, target_height)
        frame_to_animate.configure( height=current_height)
        frame_to_animate.update()
        #time.sleep(0.01)

def animate_text(element_to_animate, speed):
    sentence=element_to_animate.cget("text")
    element_to_animate.configure(text="")
    teacher_win.update()
    def animate(index):
        if index < len(sentence):
            element_to_animate.configure(text=element_to_animate.cget("text") + sentence[index])
            teacher_win.update()
            teacher_win.after(speed, animate, index + 1)

    animate(0)

def flash_message(text, flashlb):
    def clear_flash_message(flashlb):
        flashlb.configure(text="")
        flashlb.update()
    flashlb.configure(text=text)
    flashlb.update()
    flashlb.after(3000, clear_flash_message, flashlb)

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
            teacher_win.destroy()
        
        log_lb=CTkLabel(f0,text="Do you want to logout ?",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
        log_lb.place(relx=0.5,y=200,anchor=CENTER)
        log_bu=CTkButton(f0,text="Yes",height=45,command=destroy_window,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        log_bu.place(relx=0.5,y=300,anchor=CENTER)

    today = datetime.today()
    t_date= today.strftime("%B %d, %Y")
    #date and time 
    d_f=CTkFrame(f0,width=350,height=50,border_color="black",border_width=3,fg_color="white",corner_radius=40)
    d_f.place(x=750,y=5)
    time_lb=CTkLabel(d_f,width=110,height=30,text="",font=CTkFont("Helvetica",19),fg_color="white",corner_radius=40,text_color="black")
    time_lb.place(relx=0.8,rely=0.5,anchor=CENTER)
    date_lb=CTkLabel(d_f,text=t_date,width=150,height=30,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="white")
    date_lb.place(relx=0.3,rely=0.5,anchor=CENTER)
    ct_change()

    photo1=CTkImage(Image.open("logout1.png"),size=(50,50))
    edit_b=CTkButton(f0,image=photo1,command=logout_frame,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
    edit_b.place(x=1120,y=0)


#hide indicators
def hide_indicators():
    home_indicate.configure(fg_color="white")
    student_indicate.configure(fg_color="white")
    teacher_indicate.configure(fg_color="white")
    grade_indicate.configure(fg_color="white")
    complain_indicate.configure(fg_color="white")

#to delete frames
def delete_frames():
    for f in f0.winfo_children():
        f.destroy()

def id_card(teacher_id):
    global Name
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
    gender=data1["gen"]
    
    l2=CTkLabel(f0,text=("Welcome "+ Name),font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=55,y=20)
    
    f7=CTkFrame(f0,width=548,height=338,fg_color="#ffffe6",border_width=3,corner_radius=12,border_color="black")
    f7.place(x=580,y=100)
    photo5=CTkImage(Image.open("id_back.png"),size=(538,160))
    l3=CTkLabel(f7,image=photo5,text="")
    l3.place(x=5,y=5)
    

    photo6=CTkImage(Image.open("male_teach.png"),size=(150,150))
    if gender=="M":
        pass
    else:
        photo6=CTkImage(Image.open("female_teach.png"),size=(150,150))
    l4=CTkLabel(f7,image=photo6,text=" ",fg_color="transparent")
    l4.place(x=315,y=115)

    photo7=CTkImage(Image.open("logo.png"),size=(70,70))
    l5=CTkLabel(f7,image=photo7,text=" ",bg_color='#6FD0FE')
    l5.place(x=60,y=15)
    l6=CTkLabel(f7,text="IDENTITY CARD",bg_color='#6FD0FE',font=("Helvetica",25),text_color="black")
    l6.place(x=170,y=33)
    id_lb=CTkLabel(f7,text=("TEACHER.ID :  " + str(tr_id)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    id_lb.place(x=15,y=115)
    name_lb=CTkLabel(f7,text=("NAME :   " + Name),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    name_lb.place(x=15,y=150)
    dob_lb=CTkLabel(f7,text=("DOB    :  " + str(Dob)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    dob_lb.place(x=15,y=185)
    std_lb=CTkLabel(f7,text=("Quali  : "+ quali),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    std_lb.place(x=15,y=220)
    mobile_lb=CTkLabel(f7,text=("MOBILE NO. :  " + str(mobile)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    mobile_lb.place(x=15,y=255)
    address_lb=CTkLabel(f7,text=("ADDRESS :  " + Address),width=100,height=35,corner_radius=8,font=("Helvetica",15),wraplength=500,text_color="black",bg_color="#ffffe6")
    address_lb.place(x=15,y=290)

def quotes():
    try:
        # create a list of quotes
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

        # randomly select a quote from the list
        selected_quote = random.choice(quotes)

        label = CTkLabel(board1, text=selected_quote, width=40, height=50, font=("bold", 15), text_color="white", bg_color="transparent")
        label.place(relx=0.5, rely=0.5, anchor=CENTER)
        quotes_lb = CTkLabel(board1, text=f"QUOTES :", width=50, height=20, font=("bold", 30), text_color="white", bg_color="transparent")
        quotes_lb.place(relx=0.2, rely=0.5, anchor=CENTER)
    except Exception as e:
        pass


#----------------------------------------------------------------home_frame----------------------------------------------------------------



#home_frame
def home_frame():
    global board1
    date_time_display()
    id_card(teacher_id)

    cursor = db.cursor()
    grade_levels = ["5th std", "6th std", "7th std", "8th std", "9th std", "10th std"]
    positions = [(40, 98), (40, 230), (40, 360), (300, 98), (300, 230), (300, 360)]
    fg_colors = ["#FFFFCC", "#C7FAC7", "#FFFFCC", "#C7FAC7", "#FFFFCC", "#C7FAC7"]

    for i, grade_level in enumerate(grade_levels):
        cursor.execute("SELECT COUNT(*) AS count FROM student WHERE std_code = %s", (grade_level,))
        data = cursor.fetchone()
        total_students = data["count"]

        frame = CTkFrame(f0, width=240, height=110, fg_color=fg_colors[i], border_width=3, corner_radius=12, border_color="black")
        frame.place(x=positions[i][0], y=positions[i][1])

        label_count = CTkLabel(frame, text=total_students, font=CTkFont(family="Helvetica", weight="bold", size=50), text_color="black")
        label_count.place(x=20, y=10)

        label_grade = CTkLabel(frame, text=grade_level, font=CTkFont(family="Helvetica", weight="bold", size=25), text_color="black")
        label_grade.place(x=20, y=75)

    board1 = CTkFrame(f0, width=1140, height=110, fg_color="#3b3a30", border_width=5, corner_radius=12, border_color="black")
    board1.place(x=40, y=520)

    quotes()




#------------------------------------------------------------------Attendance Frame----------------------------------------------------------------





#attendance_frame
def attendance_frame():
    #date_time_display()
    l2 = CTkLabel(f0, text="Student Attendance", font=CTkFont(family="Helvetica", weight="bold", size=50),text_color="black")
    l2.place(x=40, y=30)
    #animate_text(l2,25)
    def attend_view(btn, val):
        for i in buttons_attendance:
            if btn == i:
                btn.configure(fg_color="#888888")
            else:
                i.configure(fg_color="#33CCFF")
        
        cursor = db.cursor()
        cursor.execute("select sub_code from teach_class where teacher_code=%s and std_code=%s", (teacher_id,val))
        sub = cursor.fetchall()
        sub1=sub[0]["sub_code"]
        
        cursor.execute("select sub_name from subject where sub_id=%s", (sub1))
        data3 = cursor.fetchall()
        sub_name=data3[0]["sub_name"]

        open_f = CTkFrame(f0, width=900, height=560, fg_color="#FFE5B4", border_width=3, corner_radius=12,border_color="black")
        open_f.place(x=295, y=100)
        animate_frame(open_f)
        sr_lbl = CTkLabel(open_f,text="Sr.",height=45,width=40,corner_radius=20,text_color="black", fg_color="#ccffe6", font=CTkFont("Helvetica", 18))
        sr_lbl.place(x=30, y=13)
        id_lbl = CTkLabel(open_f,text="ID",height=45,width=100,corner_radius=20,text_color="black",fg_color="#ccffe6", font=CTkFont("Helvetica", 18))
        id_lbl.place(x=125, y=13)
        nm_lbl = CTkLabel(open_f,text="Name",height=45,width=150,corner_radius=20,text_color="black",fg_color="#ccffe6", font=CTkFont("Helvetica", 18))
        nm_lbl.place(x=270, y=13)
        pre_lbl = CTkLabel(open_f,text="Previous",height=45,width=150,corner_radius=20,text_color="black",fg_color="#ccffe6", font=CTkFont("Helvetica", 18))
        pre_lbl.place(x=450, y=13)
        today = datetime.today()
        to_date= today.strftime("%d/%m/%Y")
        tod_lbl = CTkLabel(open_f, text=f"Today ({to_date})", height=45, width=200, corner_radius=20, text_color="black",fg_color="#ccffe6", font=CTkFont("Helvetica", 18))
        tod_lbl.place(x=650, y=13)
        animate_text(tod_lbl,25)
        flash_massa=CTkLabel(open_f,text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#FFE5B4")
        flash_massa.place(relx=0.5, rely=0.95,anchor=CENTER)

        scroll_f = CTkScrollableFrame(open_f, width=820, height=400, corner_radius=20,border_width=2,border_color="#3941B8", fg_color="#B6E5D8")
        scroll_f.place(x=20, y=65)

        subject=CTkLabel(open_f,text=sub_name,height=35,width=100,corner_radius=20,text_color="black",fg_color="#ccffe6", font=CTkFont("Helvetica", 17))
        subject.place(x=30, rely=0.92)
        

        def insert_att(list1,p,flag):
            cursor = db.cursor()
            cursor.execute("select attend_sheet,attendance_date from attendance where stand_code=%s and sub_code=%s order by attendance_date;", (val,sub1))
            data = cursor.fetchall()
            if len(data) == 0:
                pass
            else:
                data_sheet = data[-p]["attend_sheet"]
                for i in range(len(data_sheet)):
                    status=data_sheet[i]
                    list1[i].delete(0,END)
                    if status=="0":
                        list1[i].configure(fg_color="#ffcccc")
                        list1[i].configure(state="normal")
                        list1[i].insert(0,status )
                    else:
                        list1[i].configure(state="normal",fg_color="#c8f7ea")
                        list1[i].insert(0,status )
                    if flag=="dis":
                        list1[i].configure(state="disabled")

        def selected_insertion():
            cursor = db.cursor()
            cursor.execute("select attendance_date from attendance where stand_code=%s and sub_code=%s order by attendance_date;", (val,sub1))
            data = cursor.fetchall()
            if len(data) == 0:
                flash_massa.configure(text_color="red")
                flash_message("Attendance not taken",flash_massa)
            else:
                data_date=str(data[-1]["attendance_date"])
                today = datetime.today()
                to_date = today.strftime("%Y-%m-%d")
                
                if data_date == to_date:
                    insert_att(att_mark_list,1,"nr")
                    if len(data)>1:
                        insert_att(pre_mark_list,2,"dis")
                else:
                    insert_att(pre_mark_list,1,"dis")            

        #submit attendance_sheet
        def submit_sheet():

            sv_mks.configure(text="Saved",fg_color="#00ace6",hover_color="#0fb9f2")
            result = ""
            check_val=""
            for entry in att_mark_list:
                value = entry.get()
                if value == "":
                    check_val+=""
                    result += "0" 
                else:
                    check_val+="@"
                    result += value[0]
            if len(check_val) == 0:
                flash_massa.configure(text_color="red")
                flash_message("Attendance not entered",flash_massa)
            else:
                for entry in att_mark_list:
                    value = entry.get()
                    if value == "":
                        entry.configure(fg_color="#ffcccc")
                        entry.insert(0,"0")
                today = datetime.today()
                to_date = today.strftime("%Y-%m-%d")
                try:
                    cursor = db.cursor()
                    cursor.execute("insert into attendance VALUES(%s, %s, %s, %s)",(val,sub1, to_date, result))
                    db.commit()
                    flash_massa.configure(text_color="green")
                    flash_message("Attendance Recorded",flash_massa)
                except pymysql.err.OperationalError:
                    cursor.execute("UPDATE attendance SET attend_sheet = %s WHERE stand_code = %s AND sub_code = %s AND attendance_date = %s",(result,val,sub1, to_date ))
                    db.commit()
                    insert_att(att_mark_list,1,"nr")
                    flash_massa.configure(text_color="green")
                    flash_message("Attendance Updated",flash_massa)
            """except pymysql.err.OperationalError:
            flash_massa.configure(text_color="red")
            flash_message("Attendance already taken",flash_massa) """           

         

        
        cursor = db.cursor()
        cursor.execute("select stud_id,name from student where std_code=%s", (val,))
        data = cursor.fetchall()
        id_list = []
        name_list = []
        for i in data:
            id_list.append(i['stud_id'])
            name_list.append(i['name'])

        r = 1
        pre_mark_list = []
        att_mark_list = []
        for i in range(len(data)):
            sr_nm = CTkLabel(scroll_f, text=i+1, height=45, width=40, text_color="black", fg_color="#B6E5D8",font=CTkFont("Helvetica", 19))
            sr_nm.grid(row=r, column=0, padx=10 , pady= 5)
            s_id = CTkLabel(scroll_f, text=id_list[i], height=45, width=40, text_color="black", fg_color="#B6E5D8",font=CTkFont("Helvetica", 19))
            s_id.grid(row=r, column=1,padx=45, pady= 5)
            s_nm = CTkLabel(scroll_f, text=name_list[i], height=45, width=40, text_color="black", fg_color="#B6E5D8",font=CTkFont("Helvetica", 19))
            s_nm.grid(row=r, column=2,padx=40, pady= 5)
            pre_mark = CTkEntry(scroll_f, height=45,state="disabled",width=65,justify="center", text_color="black", fg_color="#C5C5C5",font=CTkFont("Helvetica", 19))
            pre_mark.grid(row=r, column=3,padx=(40,65), pady= 5)
            pre_mark_list.append(pre_mark)
            att_mark = CTkEntry(scroll_f, height=45, width=65,justify="center", text_color="black", fg_color="#c8f7ea",font=CTkFont("Helvetica", 19))
            att_mark.grid(row=r, column=4,padx=(75,0), pady= 5)
            att_mark_list.append(att_mark)

            r += 1
        
        sv_mks = CTkButton(open_f,command=submit_sheet, hover_color="#D9D9D0", text="Save", height=40, width=170, border_width=2,corner_radius=20, border_color="black", text_color="black", fg_color="#33CCFF",font=CTkFont("Helvetica", 20))
        sv_mks.place(x=705, y=513)
        selected_insertion()
        

    f3 = CTkFrame(f0, width=240, height=560, fg_color="white", border_width=3, corner_radius=12, border_color="black")
    f3.place(x=40, y=100)
    animate_frame(f3)
    cursor = db.cursor()
    cursor.execute("SELECT class.std_id FROM teacher, class, teach_class, subject WHERE teacher.teacher_id = teach_class.teacher_code AND class.std_id = teach_class.std_code AND subject.sub_id = teach_class.sub_code AND teacher.teacher_id = %s ORDER BY CAST(class.std_id AS UNSIGNED) ASC", (teacher_id,))
    data = cursor.fetchall()
    std_id_list = []
    for i in data: 
        std_name = i.get("std_id")
        std_id_list.append(std_name)
    
    buttons_attendance = []
    r = 45
    for i in std_id_list:
        new_b = CTkButton(f3, hover_color="#D9D9D0", text=i, height=45, width=170, border_width=2, corner_radius=20,border_color="black", text_color="black", fg_color="#33CCFF", font=CTkFont("Helvetica", 20))
        new_b.place(relx=0.5, y=r,anchor=CENTER)
        animate_text(new_b,40)
        new_b.configure(command=lambda btn=new_b, param=i: attend_view(btn, param))
        buttons_attendance.append(new_b)
        r += 70
    buttons_attendance[0].invoke()
    teacher_win.mainloop()





#----------------------------------------------------------------Teacher Workspace Frame------------------------------------------------










#teacher_workspace_frame
def timetable_frame():
    date_time_display()
    
    def treeview():
        f9=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=300,y=100)
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

        stu_table=ttk.Treeview(f9,columns=("std_i","subject_name"),show="headings",height=13)
        style=ttk.Style(f9)
    
        style.theme_use("clam")
        style.configure("Treeview",rowheight=49,font=("Roboto"),background="#dac290",fieldbackground="#dac292", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("std_i",text="Standard")
        stu_table.heading("subject_name",text="Subject")
        stu_table.column("std_i",width=545,anchor=CENTER)
        stu_table.column("subject_name",width=545,anchor=CENTER)

        for i in range(len(std_i)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(std_i[i],subject_name[i]))
        stu_table.place(relx=0.5,rely=0.5,anchor=CENTER)  
        
    #teacher_section
    l2=CTkLabel(f0,text="Teacher's Workspace",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)

    #frame for buttons 
    def hide_hover():
        tt_lb.configure(fg_color="#33CCFF")
        stand_6.configure(fg_color="#33CCFF")
        notes_bt.configure(fg_color="#33CCFF")
    
    #view details
    def time_tb():
        hide_hover()
        tt_lb.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=900,height=560,fg_color="#ffffb3",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=300,y=100)
        time_lb=CTkLabel(f8,fg_color="#FFD586",height=50,width=150,corner_radius=20,text="Teachers Assignments",font=CTkFont(family="Helvetica",size=30),text_color="black")
        time_lb.place(x=300,y=20)

        #subject and class
        cursor=db.cursor()
        subject=['Eng','Hin','Mara','Math','Sci','SS','PT']
        cursor.execute('select std_id from class')
        data=cursor.fetchall()
        newy=160
        newx=130
        for i in range(len(subject)):
            time_lb=CTkLabel(f8,fg_color="#FFD586",height=40,width=80,corner_radius=20,text=subject[i],font=CTkFont(family="Helvetica",size=20),text_color="black")
            time_lb.place(x=60,y=newy,anchor=CENTER)
            newy+=60
        for i in range(len(data)):
            time_lb=CTkLabel(f8,fg_color="#FFD586",height=40,width=80,corner_radius=20,text=data[i]['std_id'],font=CTkFont(family="Helvetica",size=20),text_color="black")
            time_lb.place(x=newx,y=80)
            newx+=125

        #fetching teachers_names
        newx=180
        for i in range(len(data)):
            cursor=db.cursor()
            cursor.execute("select teacher.name from teacher,teach_class where teach_class.std_code=%s and teach_class.teacher_code=teacher.teacher_id",(data[i]['std_id']))
            new_d=cursor.fetchall()
            teacher_list=[]
            for j in new_d:
                teacher_list.append(j['name'])
            newy=160
            for i in range(len(teacher_list)):
                time_lb=CTkLabel(f8,fg_color="#ffffb3",wraplength=80,height=45,corner_radius=20,text=teacher_list[i],font=CTkFont(family="Helvetica",size=16),text_color="black")
                time_lb.place(x=newx,y=newy,anchor=CENTER)
                newy+=60
            newx+=125

    tt_lb=CTkButton(f3,hover_color="#D9D9D0",command=time_tb,text="Mapping",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    tt_lb.place(x=120,y=45,anchor=CENTER)

    def my_sub():
        hide_hover()
        stand_6.configure(fg_color="#888888")
        treeview()
    stand_6=CTkButton(f3,hover_color="#D9D9D0",command=my_sub,text="My Classes",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_6.place(x=120,y=120,anchor=CENTER)

    def notes():
        global select_lb
        hide_hover()
        notes_bt.configure(fg_color="#888888")
        new_f=CTkFrame(f0,fg_color='#ffcc99',width=900,height=560,border_width=3,corner_radius=12,border_color="black")
        new_f.place(x=300,y=100)
        flash_massa=CTkLabel(new_f,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#ffcc99")
        flash_massa.place(x=270,y=520,anchor=CENTER)
        title=CTkLabel(new_f,text="Title",height=45,width=130,corner_radius=20,text_color="black",fg_color= "#b3d9ff",font=CTkFont("Helvetica",20))
        title.place(x=20,y=20)
        tl_et=CTkTextbox(new_f,height=10,width=400,corner_radius=15,border_width=2,font=("Roboto",18))
        tl_et.place(x=20,y=70) 
        title=CTkLabel(new_f,text="Standard",height=45,width=130,corner_radius=20,text_color="black",fg_color= "#b3d9ff",font=CTkFont("Helvetica",20))
        title.place(x=20,y=163)
        all=CTkLabel(new_f,text="All Notes",height=45,width=200,corner_radius=20,text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        all.place(x=570,y=20) 
        scroll_f=CTkScrollableFrame(new_f,width=400,corner_radius=20,border_color='black',border_width=2,fg_color="#ccffcc",height=430)
        scroll_f.place(relx=0.73,rely=0.55,anchor=CENTER)
        note=[]
        def show_pdf(n_id):
            cursor=db.cursor()
            cursor.execute("Select path from notes where note_id=%s",(n_id))
            data=cursor.fetchone()
            path = data["path"]
            edge_path="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
            webbrowser.get('edge').open(path)
        def all_notes():
            cursor=db.cursor()
            cursor.execute("Select notes.note_id,subject.sub_name,notes.title from subject join notes on subject.sub_id=notes.sub_code where notes.teacher_code=%s order by subject.sub_id",(teacher_id))
            data=cursor.fetchall()
            r=0
            y_pad=0
            for i in range(len(data)):
                note_id=data[i]['note_id']
                sub=data[i]['sub_name']
                dep=data[i]['title']
                new_b=CTkButton(scroll_f,hover_color="#D9D9D0",command=lambda param=note_id: show_pdf(param),text=sub+"     "+dep,height=45,width=330,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
                new_b.grid(row=r,column=1,padx=10,pady=y_pad+10)
                r+=1
        all_notes()

        #fetching classes
        cursor=db.cursor()
        cursor.execute("select class.std_id from teacher,class,teach_class,subject where teacher.teacher_id=teach_class.teacher_code and class.std_id=teach_class.std_code and subject.sub_id=teach_class.sub_code and teacher.teacher_id=%s",(teacher_id))
        data=cursor.fetchall()
        std_i=[]

        for i in data:
            std_name=i.get("std_id")
            std_i.append(std_name)
        std_op=CTkOptionMenu(new_f,width=160,height=30,values=std_i)
        std_op.place(x=243,y=185,anchor=CENTER)
        ch_fi=CTkLabel(new_f,text="Choose File",height=45,width=130,corner_radius=20,text_color="black",fg_color= "#b3d9ff",font=CTkFont("Helvetica",20))
        ch_fi.place(x=20,y=280)
        #browse files
        def browse():
            global path
            file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            path=''
            if file_path:
                select_lb.configure(text='file selected',text_color='green')
                path=file_path
        
        #adding note
        def add_n():
            global path
            flag_check=True
            std_code=std_op.get()
            cursor=db.cursor()
            cursor.execute("select subject.sub_id from teacher,class,teach_class,subject where teacher.teacher_id=teach_class.teacher_code and class.std_id=teach_class.std_code and subject.sub_id=teach_class.sub_code and teacher.teacher_id=%s and class.std_id=%s",(teacher_id,std_code))
            data=cursor.fetchall()
            subject_name=[]
            for i in data:
                sub_name=i.get("sub_id")
                subject_name.append(sub_name)
            sub_code=subject_name[0]
            title=tl_et.get("1.0", "end-1c")
            lb_text=select_lb.cget("text")
            if len(title)==0:
                flag_check=False
            elif lb_text=="No File Selected":
                flag_check=False
            if flag_check==True:
                cursor=db.cursor()
                cursor.execute("insert into notes(std_code,teacher_code,sub_code,title,path) values(%s,%s,%s,%s,%s)",(std_code,teacher_id,sub_code,title,path))
                db.commit()
                all_notes()
                flash_massa.configure(text_color='green')
                flash_message('Note Added',flash_massa)
            else:
                flash_massa.configure(text_color='red')
                flash_message('Try Again',flash_massa)
                
        file_lb=CTkButton(new_f,text="Browse",command= lambda :browse(),height=35,width=160,corner_radius=20,border_color='black',border_width=2,text_color="black",fg_color= "#cceeff",font=CTkFont("Helvetica",20))
        file_lb.place(x=170,y=285) 
        select_lb=CTkLabel(new_f,text="No File Selected",height=35,width=160,corner_radius=20,text_color="red",fg_color="#ffcc99",font=CTkFont("Helvetica",20))
        select_lb.place(x=163,y=330)
        add_note=CTkButton(new_f,command= lambda: add_n(),hover_color="#D9D9D0",text="Add Note",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        add_note.place(x=100,y=520,anchor=CENTER)
    notes_bt=CTkButton(f3,hover_color="#D9D9D0",command=notes,text="Notes",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    notes_bt.place(x=120,y=195,anchor=CENTER) 



#to indicate
def indicate(lb,frame):
    hide_indicators()
    lb.configure(fg_color="#0066ff")
    delete_frames()
    frame()





















#----------------------------------------------------------------Grade Frames----------------------------------------------------------------






#grade_frame
def grade_frame():
    date_time_display()
    #asking to grade
    l2=CTkLabel(f0,text="Student Grades",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)

    def get_grade(obt_mks):
        if obt_mks>=105:
            obt_grd="A+"
        elif obt_mks>=90:
            obt_grd="A"
        elif obt_mks>=75:
            obt_grd="B+"
        elif obt_mks>=60:
            obt_grd="B"
        elif obt_mks>=45:
            obt_grd="C"
        else:
            obt_grd="E"
        return obt_grd
    
    def passing_eligibility(mks_obt,mks):
        for i in mks_obt:
                    if int(i.get())<mks:
                        i.configure(fg_color="#ffcccc")
                    else:
                        i.configure(fg_color="#c8f7ea")

    def add_grades(btn,std):
        global flash_message,flash_massa
        for i in buttons_grade:
            if i==btn:
                btn.configure(fg_color="#888888")
            else:
                i.configure(fg_color="#33CCFF")
        open_f=CTkFrame(f0,width=900,height=560,fg_color="#FFE5B4",border_width=3,corner_radius=12,border_color="black")
        open_f.place(x=295,y=100)
        animate_frame(open_f)
        flash_massa=CTkLabel(open_f,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#FFE5B4")
        flash_massa.place(relx=0.5,rely=0.95,anchor=CENTER)
        all=CTkLabel(open_f,text="Examination Type",height=45,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
        all.place(x=20,y=20)
        option_exam=CTkOptionMenu(open_f,width=200,height=40,values=["Unit I","Mid Term","Unit II","Final Term"])
        option_exam.place(x=230,y=23)
        def show_student_list():
















































            
            # e_t="Unit I"
            e_t="Mid Term"
            cursor=db.cursor()
            cursor.execute("select sub_code from teach_class where teacher_code=%s and std_code=%s",(teacher_id,std))
            subject=cursor.fetchall()
            sub_code=subject[0]['sub_code']
            if e_t=="Unit I" or e_t=="Unit II":#unit exam section
                flash_massa=CTkLabel(open_f,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#FFE5B4")
                flash_massa.place(relx=0.5,rely=0.95,anchor=CENTER)
                
                all=CTkLabel(open_f,text="",height=45,width=500,corner_radius=20,text_color="black",fg_color="#FFE5B4",font=CTkFont("Helvetica",20))
                all.place(x=20,y=20)
                #back button
                photo1=CTkImage(Image.open("back.png"),size=(40,40))
                edit_b=CTkButton(open_f,command=lambda param=std,btn1=btn: add_grades(btn1,param),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#FFE5B4",corner_radius=10)
                edit_b.place(x=20,y=20)
                scroll_f=CTkScrollableFrame(open_f,border_width=2,border_color="#3941B8",width=820,corner_radius=20,fg_color="#B6E5D8",height=330)
                scroll_f.place(x=20,y=123)
                s_id=CTkLabel(open_f,text="id",height=45,width=140,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
                s_id.place(x=40,y=70)
                s_nm=CTkLabel(open_f,text="Name",height=45,width=200,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
                s_nm.place(x=200,y=70)
                ob_mk=CTkLabel(open_f,text="Marks Obtained",height=45,width=200,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
                ob_mk.place(x=430,y=70)
                ob_gr=CTkLabel(open_f,text="Out of",height=45,width=200,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
                ob_gr.place(x=650,y=70)
                ex_ty=CTkLabel(open_f,text=e_t,height=45,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
                ex_ty.place(relx=0.5,y=35,anchor=CENTER)
                cursor=db.cursor()
                cursor.execute("select * from grade where stud_code=(select stud_id from student where std_code=%s limit 1) and sub_code=%s and exam_type=%s",(std,sub_code,e_t))
                count=cursor.fetchall()
                if len(count)!=0:
                    et_mks.destroy()
                    cursor=db.cursor()
                    cursor.execute("select student.stud_id,student.name,grade.obt_mks from student,grade where student.stud_id=grade.stud_code and grade.exam_type=%s and grade.sub_code=%s and student.stud_id in (select stud_id from student where std_code=%s)",(e_t,sub_code,std))
                    data=cursor.fetchall()
                    id=[]
                    nms=[]
                    obt_mk=[]

                    for i in data:
                        id.append(i['stud_id'])
                        nms.append(i['name'])
                        obt_mk.append(i['obt_mks'])
                    r=1
                    for i in range(len(data)):
                        s_id=CTkLabel(scroll_f,text=id[i],height=45,width=40,text_color="black",fg_color="#B6E5D8",font=CTkFont("Helvetica",20))
                        s_id.grid(row=r, column=1,padx=50, pady= 5)
                        s_nm=CTkLabel(scroll_f,text=nms[i],height=45,width=40,text_color="black",fg_color="#B6E5D8",font=CTkFont("Helvetica",20))
                        s_nm.grid(row=r, column=2,padx=30, pady= 5)
                        r+=1
                    #marks_obtained
                    mks_obt=[]
                    r=1
                    for i in range(len(data)):
                        mk_e=CTkEntry(scroll_f,justify="center",fg_color="#c8f7ea",height=40,width=80,text_color="black",font=CTkFont("Helvetica",18))
                        mk_e.grid(row=r,column=3,padx=80, pady=5)
                        mk_e.insert(0,obt_mk[i])
                        mks_obt.append(mk_e)
                        r+=1
                    
                    #checking passing eligibility
                    passing_eligibility(mks_obt,7)
                    #out_of
                    out_of=[]
                    r=1
                    for i in range(len(data)):
                        mk_e=CTkEntry(scroll_f,justify="center",height=40,fg_color="#c8f7ea",width=80,text_color="black",font=CTkFont("Helvetica",18))
                        mk_e.grid(row=r,column=4,padx=50, pady=5)
                        out_of.append(mk_e)
                        r+=1
                    for i in out_of:
                        i.insert(0,"20")
                        i.configure(state="disabled")
            
                    def update_unit_marks():
                        flag_len=True
                        flag_check=True
                        wrong_list=[]
                        for i in mks_obt:                    
                            if len(i.get())==0:
                                flag_len=False
                            elif i.get().isalpha() or int(i.get())>20 or int(i.get())<0:
                                flag_check=False
                                wrong_list.append(i)         
                        if flag_check==False:
                            for i in wrong_list:
                                i.delete(0,END)
                            flash_massa.configure(text_color="red")
                            flash_message("Invalid marks entered",flash_massa)
                        elif flag_len==False:
                            flash_massa.configure(text_color="red")
                            flash_message("Marks not entered",flash_massa)
                        elif flag_check==True and flag_len==True:
                            passing_eligibility(mks_obt,7)
                            for i in range(len(id)):
                                stud_code=id[i]
                                obt_mks=int(mks_obt[i].get())
                                cursor=db.cursor()
                                cursor.execute("update grade set obt_mks=%s where exam_type=%s and sub_code=%s and stud_code=%s",(obt_mks,e_t,sub_code,stud_code))
                                db.commit()
                            flash_massa.configure(text_color="green")
                            flash_message("Updated Successfully",flash_massa)

                    sv_mks=CTkButton(open_f,command=update_unit_marks,hover_color="#D9D9D0",text="Update",height=40,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
                    sv_mks.place(x=700,y=505)

                else:
                    et_mks.destroy()
                    cursor=db.cursor()
                    cursor.execute("select stud_id,name from student where std_code=%s",(std))
                    data=cursor.fetchall()
                    id=[]
                    nms=[]
                    for i in data:
                        id.append(i['stud_id'])
                        nms.append(i['name'])
                    r=1
                    for i in range(len(data)):
                        s_id=CTkLabel(scroll_f,text=id[i],height=45,width=40,text_color="black",fg_color="#B6E5D8",font=CTkFont("Helvetica",20))
                        s_id.grid(row=r, column=1,padx=50, pady= 5)
                        s_nm=CTkLabel(scroll_f,text=nms[i],height=45,width=40,text_color="black",fg_color="#B6E5D8",font=CTkFont("Helvetica",20))
                        s_nm.grid(row=r, column=2,padx=30, pady= 5)
                        r+=1
                    #marks_obtained
                    mks_obt=[]
                    r=1
                    mks_obt1=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,6,7,8,9,10,11,12,13,14,15,16,17,18,19,11,12,13,14,15,16]
                    for i in range(len(data)):
                        m=random.choice(mks_obt1)
                        mk_e=CTkEntry(scroll_f,justify="center",fg_color="#c8f7ea",height=40,width=80,text_color="black",font=CTkFont("Helvetica",18))
                        mk_e.grid(row=r,column=3,padx=80, pady=5)
                        mk_e.insert(0,f"{m}")
                        mks_obt.append(mk_e)
                        r+=1
                    #out_of
                    out_of=[]
                    r=1
                    for i in range(len(data)):
                        mk_e=CTkEntry(scroll_f,justify="center",height=40,fg_color="#c8f7ea",width=80,text_color="black",font=CTkFont("Helvetica",18))
                        mk_e.grid(row=r,column=4,padx=50, pady=5)
                        out_of.append(mk_e)
                        r+=1
                    for i in out_of:
                        i.insert(0,"20")
                        i.configure(state="disabled")
                    teacher_win.update()
                    flag_re=True
                    def save_unit_mks():
                        nonlocal flag_re
                        flag_len=True
                        flag_check=True
                        wrong_list=[]
                        for i in mks_obt:                    
                            if len(i.get())==0:
                                flag_len=False
                            elif i.get().isalpha() or int(i.get())>20 or int(i.get())<0:
                                flag_check=False
                                wrong_list.append(i)         
                        if flag_check==False:
                            for i in wrong_list:
                                i.delete(0,END)
                            flash_massa.configure(text_color="red")
                            flash_message("Invalid marks entered",flash_massa)
                        elif flag_len==False:
                            flash_massa.configure(text_color="red")
                            flash_message("Marks not entered",flash_massa)
                        elif flag_check==True and flag_len==True:
                            if flag_re:
                                passing_eligibility(mks_obt,7)
                                for i in range(len(id)):
                                    stud_code=id[i]
                                    obt_mks=int(mks_obt[i].get())
                                    cursor=db.cursor()
                                    cursor.execute("insert into grade(stud_code, sub_code, obt_mks, exam_type) values(%s,%s,%s,%s)",(stud_code,sub_code,obt_mks,e_t))
                                    db.commit()
                                flash_massa.configure(text_color="green")
                                flash_message("Saved Successfully",flash_massa)
                                flag_re=False
                            else:
                                flash_massa.configure(text_color="red")
                                flash_message("Marks Already Entered",flash_massa)

                    sv_mks=CTkButton(open_f,command=save_unit_mks,hover_color="#D9D9D0",text="Save",height=40,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
                    sv_mks.place(x=700,y=505)
                    sv_mks.invoke()
            
            else:#term exam section
                flash_massa=CTkLabel(open_f,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#FFE5B4")
                flash_massa.place(relx=0.5,rely=0.95,anchor=CENTER)

                if e_t=="Mid Term":
                    unit_state="Unit I"
                else:
                    unit_state="Unit II"
                cursor=db.cursor()
                cursor.execute("select * from grade where stud_code=(select stud_id from student where std_code=%s limit 1) and sub_code=%s and exam_type=%s",(std,sub_code,unit_state))
                count=cursor.fetchall()
                if len(count)==0:
                    flash_massa.configure(text_color="red")
                    flash_message(unit_state+ " marks not entered",flash_massa)
                else:
                    et_mks.destroy()
                    all=CTkLabel(open_f,text="",height=45,width=500,corner_radius=20,text_color="black",fg_color="#FFE5B4",font=CTkFont("Helvetica",20))
                    all.place(x=20,y=20)
                    #back button
                    photo1=CTkImage(Image.open("back.png"),size=(40,40))
                    edit_b=CTkButton(open_f,command=lambda param=std,btn1=btn: add_grades(btn1,param),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#FFE5B4",corner_radius=10)
                    edit_b.place(x=20,y=20)
                    scroll_f=CTkScrollableFrame(open_f,border_width=2,border_color="#3941B8",width=820,corner_radius=20,fg_color="#B6E5D8",height=330)
                    scroll_f.place(x=20,y=123)
                    s_id=CTkLabel(open_f,text="id",height=45,width=40,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
                    s_id.place(x=30,y=70)
                    s_nm=CTkLabel(open_f,text="Name",height=45,width=200,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
                    s_nm.place(x=100,y=70)
                    in_mk=CTkLabel(open_f,text="Internal Marks/20",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",18))
                    in_mk.place(x=320,y=70)
                    ex_mk=CTkLabel(open_f,text="External Marks/80",height=45,width=170,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",18))
                    ex_mk.place(x=510,y=70)
                    ob_gr=CTkLabel(open_f,text="Grades/120",height=45,width=150,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",18))
                    ob_gr.place(x=700,y=70)
                    ex_ty=CTkLabel(open_f,text=e_t,height=45,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
                    ex_ty.place(relx=0.5,y=35,anchor=CENTER)

                    #checking for update marks for term
                    cursor=db.cursor()
                    cursor.execute("select * from grade where exam_type=%s and sub_code=%s and stud_code in (select stud_id from student where std_code=%s)",(e_t,sub_code,std))
                    count=cursor.fetchall()
                    if len(count)!=0:
                        cursor=db.cursor()
                        cursor.execute("select student.stud_id,student.name,grade.internal_mk,grade.external_mk,grade.obt_grd from student,grade where student.stud_id=grade.stud_code and grade.exam_type=%s and grade.sub_code=%s and stud_id in (select stud_id from student where std_code=%s)",(e_t,sub_code,std))
                        data=cursor.fetchall()
                        id=[]
                        nms=[]
                        inter_mr=[]
                        exter_mr=[]
                        obt_grd=[]
                    
                        for i in data:
                            id.append(i['stud_id'])
                            nms.append(i['name'])
                            inter_mr.append(i['internal_mk'])
                            exter_mr.append(i['external_mk'])
                            obt_grd.append(i['obt_grd'])
                        r=1
                        for i in range(len(data)):
                            s_id=CTkLabel(scroll_f,text=id[i],height=45,width=40,text_color="black",fg_color="#B6E5D8",font=CTkFont("Helvetica",20))
                            s_id.grid(row=r,column=0,pady=10)
                            s_nm=CTkLabel(scroll_f,text=nms[i],height=45,width=40,text_color="black",fg_color="#B6E5D8",font=CTkFont("Helvetica",20))
                            s_nm.grid(row=r,column=1,pady=10,padx=40)
                            r+=1

                        #internal_marks
                        internal_mk=[]
                        r=1
                        for i in range(len(data)):
                            mk_e=CTkEntry(scroll_f,justify="center",fg_color="#c8f7ea",height=40,width=80,text_color="black",font=CTkFont("Helvetica",18))
                            mk_e.grid(row=r,column=3,padx=30, pady=5)
                            mk_e.insert(0,inter_mr[i])
                            internal_mk.append(mk_e)
                            r+=1

                        #external_marks
                        external_mk=[]
                        r=1
                        for i in range(len(data)):
                            mk_e=CTkEntry(scroll_f,justify="center",fg_color="#c8f7ea",height=40,width=80,text_color="black",font=CTkFont("Helvetica",18))
                            mk_e.grid(row=r,column=4,padx=80, pady=5)
                            mk_e.insert(0,exter_mr[i])
                            external_mk.append(mk_e)
                            r+=1
                        #obtained_grade
                        ob_gr=[]
                        r=1
                        for i in range(len(data)):
                            mk_e=CTkEntry(scroll_f,justify="center",fg_color="#c8f7ea",height=40,width=80,text_color="black",font=CTkFont("Helvetica",18))
                            mk_e.grid(row=r,column=5,padx=20, pady=5)
                            mk_e.insert(0,obt_grd[i])
                            ob_gr.append(mk_e)
                            r+=1
                        #checking passing eligibility
                        passing_eligibility(external_mk,28)
                        #calculate_grades
                        def cal_grades():
                            global unit1_mk
                            cursor=db.cursor()
                            cursor.execute('Select grade.obt_mks from grade join student on grade.stud_code = student.stud_id where grade.sub_code =%s and student.std_code = %s and grade.exam_type = %s',(sub_code,std,unit_state))
                            data=cursor.fetchall()
                            unit1_mk=[]
                            for i in range(len(data)):
                                new=data[i]['obt_mks']
                                unit1_mk.append(new)
                            flag_len=True
                            flag_check=True
                            wrong_list=[]
                            for i in internal_mk:                    
                                if len(i.get())==0:
                                    flag_len=False
                                elif i.get().isalpha() or int(i.get())>20 or int(i.get())<0:
                                    flag_check=False
                                    wrong_list.append(i) 
                            for i in external_mk:                    
                                if len(i.get())==0:
                                    flag_len=False
                                elif i.get().isalpha() or int(i.get())>80 or int(i.get())<0:
                                    flag_check=False
                                    wrong_list.append(i)       
                            if flag_check==False:
                                for i in wrong_list:
                                    i.delete(0,END)
                                flash_massa.configure(text_color="red")
                                flash_message("Invalid marks entered",flash_massa)
                            elif flag_len==False:
                                flash_massa.configure(text_color="red")
                                flash_message("Marks not entered",flash_massa)
                            elif flag_check==True and flag_len==True:
                                    passing_eligibility(external_mk,28)
                                    for i in range(len(id)):
                                        obt_mks=int(internal_mk[i].get())+int(external_mk[i].get())+int(unit1_mk[i])
                                        obt_grd=get_grade(obt_mks)
                                        ob_gr[i].configure(state="normal")
                                        ob_gr[i].delete(0,END)
                                        ob_gr[i].insert(0,obt_grd)
                                        ob_gr[i].configure(state="disabled")
                                        
                        def update_term_mks():
                            for i in range(len(id)):
                                stud_code=id[i]
                                obt_mk1=int(internal_mk[i].get())+int(external_mk[i].get())
                                obt_mks=int(internal_mk[i].get())+int(external_mk[i].get())+int(unit1_mk[i])
                                inter_mk=internal_mk[i].get()
                                exter_mk=external_mk[i].get()
                                obt_grd=get_grade(obt_mks)
                                cursor=db.cursor()
                                cursor.execute("update grade set obt_mks=%s,obt_grd=%s,internal_mk=%s,external_mk=%s where stud_code=%s and sub_code=%s and exam_type=%s",(obt_mk1,obt_grd,inter_mk,exter_mk,stud_code,sub_code,e_t))
                                db.commit()
                            flash_massa.configure(text_color="green")
                            flash_message("Updated Successfully",flash_massa)    

                        cal_mks=CTkButton(open_f,command=cal_grades,hover_color="#D9D9D0",text="Calculate Grades",height=40,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
                        cal_mks.place(x=20,y=505)
                        sv_mks=CTkButton(open_f,command=update_term_mks,hover_color="#D9D9D0",text="Update",height=40,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
                        sv_mks.place(x=700,y=505)

                    else:
                        cursor=db.cursor()
                        cursor.execute("select stud_id,name from student where std_code=%s",(std))
                        data=cursor.fetchall()
                        id=[]
                        nms=[]
                        for i in data:
                            id.append(i['stud_id'])
                            nms.append(i['name'])
                        r=1
                        for i in range(len(data)):
                            s_id=CTkLabel(scroll_f,text=id[i],height=45,width=40,text_color="black",fg_color="#B6E5D8",font=CTkFont("Helvetica",20))
                            s_id.grid(row=r,column=0,pady=10)
                            s_nm=CTkLabel(scroll_f,text=nms[i],height=45,width=40,text_color="black",fg_color="#B6E5D8",font=CTkFont("Helvetica",20))
                            s_nm.grid(row=r,column=1,pady=10,padx=40)
                            r+=1
                        
                        #internal_marks
                        internal_mk=[]
                        r=1
                        mks_obt1=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,6,7,8,9,10,11,12,13,14,15,16,17,18,19,11,12,13,14,15,16]
                        for i in range(len(data)):
                            m=random.choice(mks_obt1)
                            mk_e=CTkEntry(scroll_f,justify="center",fg_color="#c8f7ea",height=40,width=80,text_color="black",font=CTkFont("Helvetica",18))
                            mk_e.grid(row=r,column=3,padx=30, pady=5)
                            mk_e.insert(0,m)
                            internal_mk.append(mk_e)
                            r+=1

                        #external_marks
                        external_mk=[]
                        r=1
                        mks_obt2=[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]
                        for i in range(len(data)):
                            m=random.choice(mks_obt2)
                            mk_e=CTkEntry(scroll_f,justify="center",fg_color="#c8f7ea",height=40,width=80,text_color="black",font=CTkFont("Helvetica",18))
                            mk_e.grid(row=r,column=4,padx=80, pady=5)
                            mk_e.insert(0,m)
                            external_mk.append(mk_e)
                            r+=1

                        #grade_obtained
                        grade_ob=[]
                        r=1
                        for i in range(len(data)):
                            mk_e=CTkEntry(scroll_f,state="disabled",justify="center",fg_color="#c8f7ea",height=40,width=80,text_color="black",font=CTkFont("Helvetica",18))
                            mk_e.grid(row=r,column=5,padx=20, pady=5)
                            grade_ob.append(mk_e)
                            r+=1

                        #calculate_grades
                        def cal_grades():
                            global unit1_mk
                            cursor=db.cursor()
                            cursor.execute('Select grade.obt_mks from grade join student on grade.stud_code = student.stud_id where grade.sub_code =%s and student.std_code = %s and grade.exam_type = %s',(sub_code,std,unit_state))
                            data=cursor.fetchall()
                            unit1_mk=[]
                            for i in range(len(data)):
                                new=data[i]['obt_mks']
                                unit1_mk.append(new)
                            flag_len=True
                            flag_check=True
                            wrong_list=[]
                            for i in internal_mk:                    
                                if len(i.get())==0:
                                    flag_len=False
                                elif i.get().isalpha() or int(i.get())>20 or int(i.get())<0:
                                    flag_check=False
                                    wrong_list.append(i) 
                            for i in external_mk:                    
                                if len(i.get())==0:
                                    flag_len=False
                                elif i.get().isalpha() or int(i.get())>80 or int(i.get())<0:
                                    flag_check=False
                                    wrong_list.append(i)       
                            if flag_check==False:
                                for i in wrong_list:
                                    i.delete(0,END)
                                flash_massa.configure(text_color="red")
                                flash_message("Invalid marks entered",flash_massa)
                            elif flag_len==False:
                                flash_massa.configure(text_color="red")
                                flash_message("Marks not entered",flash_massa)
                            elif flag_check==True and flag_len==True:
                                passing_eligibility(external_mk,28)
                                for i in range(len(id)):
                                    obt_mks=int(internal_mk[i].get())+int(external_mk[i].get())+int(unit1_mk[i])
                                    obt_grd=get_grade(obt_mks)
                                    grade_ob[i].configure(state="normal")
                                    grade_ob[i].delete(0,END)
                                    grade_ob[i].insert(0,obt_grd)
                                    grade_ob[i].configure(state="disabled")

                        flag_1=True            
                        def save_term_mks():
                            nonlocal flag_1
                            if flag_1:
                                for i in range(len(id)):
                                    stud_code=id[i]
                                    obt_mk1=int(internal_mk[i].get())+int(external_mk[i].get())
                                    obt_mks=int(internal_mk[i].get())+int(external_mk[i].get())+int(unit1_mk[i])
                                    inter_mk=internal_mk[i].get()
                                    exter_mk=external_mk[i].get()
                                    obt_grd=get_grade(obt_mks)
                                    cursor=db.cursor()
                                    cursor.execute("insert into grade(stud_code, sub_code, obt_mks, obt_grd, exam_type, internal_mk, external_mk) values(%s,%s,%s,%s,%s,%s,%s)",(stud_code,sub_code,obt_mk1,obt_grd,e_t,inter_mk,exter_mk))
                                    db.commit()
                                flash_massa.configure(text_color="green")
                                flash_message("Saved Successfully",flash_massa)
                                flag_1=False  

                            else:
                                flash_massa.configure(text_color="red")
                                flash_message("Marks Already Entered",flash_massa)

                                  

                        cal_mks=CTkButton(open_f,command=cal_grades,hover_color="#D9D9D0",text="Calculate Grades",height=40,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
                        cal_mks.place(x=20,y=505)
                        cal_mks.invoke()
                        time.sleep(2)
                        sv_mks=CTkButton(open_f,command=save_term_mks,hover_color="#D9D9D0",text="Save",height=40,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
                        sv_mks.place(x=700,y=505) 
                        sv_mks.invoke()

        et_mks=CTkButton(open_f,command=show_student_list,hover_color="#D9D9D0",text="Enter marks",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
        et_mks.place(x=700,y=20)
        et_mks.invoke()

    cursor=db.cursor()
    cursor.execute("SELECT class.std_id FROM teacher, class, teach_class, subject WHERE teacher.teacher_id = teach_class.teacher_code AND class.std_id = teach_class.std_code AND subject.sub_id = teach_class.sub_code AND teacher.teacher_id = %s ORDER BY CAST(class.std_id AS UNSIGNED) ASC", (teacher_id,))
    data=cursor.fetchall()
    std_i=[]

    for i in data:
            teacher_name=i.get("std_id")
            std_i.append(teacher_name)
    buttons_grade=[]
    r=45
    
    for i in std_i:
        new_b=CTkButton(f3,hover_color="#D9D9D0",text=i,height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        new_b.place(relx=0.5, y=r,anchor=CENTER)
        new_b.configure(command=lambda new=new_b,std=i: add_grades(new,std))
        animate_text(new_b,40)
        buttons_grade.append(new_b)
        r+=70
    num=0
    def treverse1():
        nonlocal num
        try:
            buttons_grade[num].invoke()
            num+=1
            teacher_win.after(3000,treverse1)
        except:
            pass
    treverse1()

    



#------------------------------------------------------------COMPLAIN FRAME------------------------------------------------------------------------------------------------------------------------------------




def complain_frame():
    global buttons_complain
    date_time_display()
    def show_complains(btn,depart):
        for i in buttons_complain:
            if btn==i:
                btn.configure(fg_color="#888888")
            else:
                i.configure(fg_color="#33CCFF")
        open_f=CTkFrame(f0,width=880,height=560,fg_color="#FFE5B4",border_width=3,corner_radius=12,border_color="black")
        open_f.place(x=325,y=100)
        animate_frame(open_f,)
        all=CTkLabel(open_f,text=depart+" - Related Complains",height=45,width=470,corner_radius=20,text_color="black",fg_color= "#ccffe6",font=CTkFont("Helvetica",20))
        all.place(x=20,y=20)
        scroll_f=CTkScrollableFrame(open_f,width=810,corner_radius=20,fg_color="#B6E5D8",height=430)
        scroll_f.place(relx=0.5,rely=0.55,anchor=CENTER)
        cursor=db.cursor()
        cursor.execute("select complain_id,subject from complain where (`to`=%s or `to`= %s) and depart=%s",("All Teachers",Name,depart))
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
                flash_massa=CTkLabel(sol_f,text_color="green",text="",width=120,height=35,corner_radius=8,font=("Helvetica",20),bg_color="#FFE5B4")
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
                    flash_massa.configure(text_color="green")
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
            r+=1


    l2=CTkLabel(f0,text="Complain Section",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)
    new_f=CTkScrollableFrame(f0,width=240,height=535,fg_color="white",border_width=2,corner_radius=12,border_color="black")
    new_f.place(x=40,y=100)
    cursor=db.cursor()
    cursor.execute('select distinct depart from complain where `to`=%s or `to`=%s',("All Teachers",Name))
    depart=cursor.fetchall()
    departments=[]
    for i in range(len(depart)):
        new=depart[i]
        departments.append(new['depart'])
        
    r=0
    y_pad=0
    buttons_complain=[]
    for i in departments:
        new_b=CTkButton(new_f,hover_color="#D9D9D0",text=i,height=45,width=200,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color="#33CCFF",font=CTkFont("Helvetica",20))
        new_b.grid(row=r,column=1,padx=10,pady=y_pad+10)
        new_b.configure(command=lambda param=i,new_b=new_b: show_complains(new_b, param))
        buttons_complain.append(new_b)
        animate_text(new_b,40)
        r+=1
    buttons_complain[0].invoke()

    



#----------------------------------------------------------------Teachers Main Window----------------------------------------------------------------



set_appearance_mode("light")
set_default_color_theme("blue")
teacher_win=CTk()
teacher_win.title("Teacher home page")
teacher_win.geometry(f"{teacher_win.winfo_screenwidth()}x{teacher_win.winfo_screenwidth()}")
teacher_win.geometry("+0+0")
teacher_win.maxsize(width=1400,height=750)
teacher_win.minsize(width=1400,height=750)
#teacher_win.attributes('-fullscreen',True)
teacher_win.iconbitmap("logo_icon.ico")

frame=CTkFrame(teacher_win,width=1920,height=1080,fg_color="#66B3FF")
frame.pack()
#Home frame
f0=CTkFrame(frame,width=1200,height=700,fg_color="#66B3FF")
f0.place(x=140,y=30)
#Dashboard
f1=CTkFrame(frame,width=100,height=680,fg_color="white",border_width=3,corner_radius=15,border_color="black")
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

#grade indicator
grade_indicate=CTkLabel(f1,fg_color="white",text=" ",height=55,width=2,corner_radius=9)
grade_indicate.place(x=7,y=450)

#grade indicator
complain_indicate=CTkLabel(f1,fg_color="white",text=" ",height=55,width=2,corner_radius=9)
complain_indicate.place(x=7,y=550)

#to initialize the teacher_win
indicate(home_indicate,home_frame)

#home button
photo1=CTkImage(Image.open("home.png"),size=(50,50))
b1=CTkButton(f1,command=lambda: indicate(home_indicate,home_frame),image=photo1,text="",hover_color="white",cursor="hand2",width=15,height=40,fg_color="white")
b1.place(x=17,y=150)

#student button
photo2=CTkImage(Image.open("attendence.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(student_indicate,attendance_frame),image=photo2,text=" ",hover_color="white",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=250)

#teacher button 
photo3=CTkImage(Image.open("time_table.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(teacher_indicate,timetable_frame),image=photo3,text=" ",hover_color="white",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=350)

#grade button 
photo4=CTkImage(Image.open("grade.png"),size=(50,50))
b3=CTkButton(f1,command=lambda: indicate(grade_indicate,grade_frame),image=photo4,text=" ",hover_color="white",cursor="hand2",width=15,height=40,fg_color="white")
b3.place(x=15,y=450)
b3.invoke()
#complain button
photo5=CTkImage(Image.open("report.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(complain_indicate,complain_frame),image=photo5,text=" ",hover_color="white",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=550)
teacher_win.mainloop()