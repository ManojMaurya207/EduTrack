from customtkinter import *
import pymysql
from datetime import * 
import tkinter as tk
from PIL import Image
import pyttsx3

#       ___          _____          ___                       ___           ___           ___           ___     
#      /  /\        /  /::\        /__/\          ___        /  /\         /  /\         /  /\         /__/|    
#     /  /:/_      /  /:/\:\       \  \:\        /  /\      /  /::\       /  /::\       /  /:/        |  |:|    
#    /  /:/ /\    /  /:/  \:\       \  \:\      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/         |  |:|    
#   /  /:/ /:/_  /__/:/ \__\:|  ___  \  \:\    /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/  ___   __|  |:|    
#  /__/:/ /:/ /\ \  \:\ /  /:/ /__/\  \__\:\  /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/  /  /\ /__/\_|:|____
#  \  \:\/:/ /:/  \  \:\  /:/  \  \:\ /  /:/ /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\ /  /:/ \  \:\/:::::/
#   \  \::/ /:/    \  \:\/:/    \  \:\  /:/  \__\/  \:\   \  \::/~~~~   \  \::/       \  \:\  /:/   \  \::/~~~~ 
#    \  \:\/:/      \  \::/      \  \:\/:/        \  \:\   \  \:\        \  \:\        \  \:\/:/     \  \:\     
#     \  \::/        \__\/        \  \::/          \  \:\   \  \:\        \  \:\        \  \::/       \  \:\    
#      \__\/                       \__\/            \__\/    \__\/         \__\/         \__\/         \__\/    


#-------------------------------------------database connection------------------------------------------------------------------------------------

db=pymysql.connect(host='localhost',user='root',password='root',database="student_database",charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#-------------------------------------------------Global-----------------------------------------------------------------------------

current_image = 0
query="select * from student"
admin_stat=False
student_stat=True
teacher_stat=False
flag_bot=True
student_id=1
teacher_id=1
#-----------------------------------------------Common Functions----------------------------------------------------------------------------------------

#flash message for adding form
def flash_message(text, flashlb):
    def clear_flash_message(flashlb):
        flashlb.configure(text="")
        flashlb.update()
    flashlb.configure(text=text)
    flashlb.update()
    flashlb.after(3000, clear_flash_message, flashlb)


def reverse_animation( frame_to_animate, speed):
    target_width = frame_to_animate.cget("width")
    target_height = frame_to_animate.cget("height")
    current_width = target_width
    current_height = target_height

    while current_width > 0 or current_height > 0:
        current_width = max(current_width - speed, 0)
        current_height = max(current_height - speed, 0)
        frame_to_animate.configure(width=current_width, height=current_height)
        frame_to_animate.update()
        #time.sleep(0.01)

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

def animate_bot_frame( frame_to_animate, speed):
    target_width = frame_to_animate.cget("width")
    target_height = frame_to_animate.cget("height")
    frame_to_animate.configure(width=0, height=0)
    current_width = 0
    current_height = 0

    while current_width < target_width or current_height < target_height:
        current_width = min(current_width + speed, target_width)
        current_height = min(current_height + speed, target_height)
        frame_to_animate.configure(width=current_width, height=current_height)
        frame_to_animate.update()
        #time.sleep(0.01)


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    
    engine.say(text)
    engine.runAndWait()





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
            flash_message("Please enter a username",mass_lab)
            #tk.messagebox.showerror("WARNING","PLEASE! ENTER A USERNAME")
            return 0
        elif password=="" :
            flash_message("Please enter a password",mass_lab)
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
                import teacher_page
                teacher_page.teacher_page(teacher_id)
            elif admin_stat:
                import admin_page
                admin_page.admin_page()
            else :
                import student_page
                student_page.student_page(student_id)
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
                    flash_message("Registration successful",success_label)
                    
                    stud_id_entry.delete(0, END)
                    user_entry.delete(0, END)
                    pass_entry.delete(0, END)
                    Cpass_entry.delete(0, END)
                    
                elif password!=Cpass:
                    success_label.configure(text_color='red')
                    flash_message("Passwords don't match. Please check and try again.",success_label)
                elif exist==False:
                    success_label.configure(text_color='red')
                    flash_message("Invaild Sdudent ID",success_label)
                else:
                    success_label.configure(text_color='red')
                    flash_message("Please Try Again.",success_label)
                
            except:
                success_label.configure(text_color='red')
                flash_message("Try again",success_label)



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
        signup_win.iconbitmap("logo_icon.ico")
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
    window.iconbitmap("logo_icon.ico")
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


if __name__ == "__main__":
    login_page()