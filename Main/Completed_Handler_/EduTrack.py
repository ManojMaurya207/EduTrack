from customtkinter import *
from datetime import * 
import tkinter as tk
from PIL import ImageTk,Image
import time 


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

def animate_frame(frame_to_animate):
    target_height = frame_to_animate.cget("height")
    frame_to_animate.configure(height=0)
    
    current_height = 0

    while current_height < target_height:
        current_height = min(current_height + 30, target_height)
        frame_to_animate.configure( height=current_height)
        frame_to_animate.update()



#---------------------------------------SPLASH SCREEN CODE START HERE---------------------------------------------------------------- 



def splash_loading():

    def count_to_100(progressbar):
        delay = 80
        def loop():
            progress_per = progressbar.get()
            percent = str(progress_per*100)
            load_lab_right.configure(text=f"{percent[:2]}/100")
            splash_root.update()
            if progress_per <= 100:
                
                splash_root.after(delay, loop)
        loop()
    current_text_index = 0
    def update_text():
        nonlocal current_text_index
        try:
            load_lab.configure(text=texts[current_text_index])
            animate_text(load_lab, 20)
            load_lab.update()
            current_text_index = (current_text_index + 1)
            load_lab.after(3000, update_text)
        except:
            time.sleep(1)
            splash_root.destroy()
            import login_page
            login_page.login_page()

    texts = [
        "Connecting database...",
        "Loading data...",
        "Preparing user interface...",
        "Finalizing setup...",
        "Almost there..."]
    
    set_appearance_mode("dark")
    set_default_color_theme("blue")
    splash_root = CTk()
    splash_root_width = 600
    splash_root_height = 250
    splash_root.title("WELCOME!")
    splash_root.overrideredirect(True)
    splash_root.geometry(f"{splash_root_width}x{splash_root_height}")
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x = int((screen_width - splash_root_width) / 2)
    y = int((screen_height - splash_root_height) / 2)
    splash_root.geometry(f"+{x}+{y}")

    main_frame=CTkFrame(splash_root,bg_color="#1C1F26",fg_color="#1C1F26",corner_radius=12,width = splash_root_width,height=splash_root_height)
    main_frame.place(x=0,y=0)
    
    photo1 = CTkImage(Image.open("splash_img.jpg"),size=(splash_root_width-150,splash_root_height))
    label1 = CTkLabel(main_frame,image=photo1, text="")
    label1.place(relx=0.5,rely=0.5,anchor=CENTER)    

    
    load_lab=CTkLabel(main_frame,text="Starting Up...",height=7,font=CTkFont(family="Helvetica",weight="bold",size=12),bg_color="#1C1F26",text_color="white")
    load_lab.place(relx=0.02,rely=0.93,anchor="w")
    animate_text(load_lab, 20)

    load_lab_right=CTkLabel(main_frame,text="0/100",height=7,font=CTkFont(family="Helvetica",weight="bold",size=12),bg_color="#1C1F26",text_color="white")
    load_lab_right.place(relx=0.99,rely=0.93,anchor="e")

    progressbar_1 = CTkProgressBar(main_frame,bg_color="#1C1F26",fg_color="#1C1F26",height=4,mode="determinate",width=splash_root_width-20,determinate_speed=0.55)
    progressbar_1.place(relx=0.5,rely=0.975,anchor="center")
    progressbar_1.start()
    
    label1.after(1000, update_text)
    count_to_100(progressbar_1)

    splash_root.mainloop()


if __name__ == "__main__":
    splash_loading()