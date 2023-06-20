from customtkinter import *
import pymysql

db = pymysql.connect(host="localhost", user="root", password="root", database="student_database", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
cursor.execute("SELECT name FROM student WHERE std_code=%s", ("10th std"))
data = cursor.fetchall()

def mark_attendance():
    attend = ""
    for Checkbox in  Checkboxs:
        if Checkbox.get() == 1:
            attend += "1"
        else:
            attend += "0"
    print(attend)

root = CTk()
root.title("Attendance")
root.geometry("900x800")

# Create Checkboxs for each student
Checkboxs = []
i = 10

for student_data in data:
    Checkbox_var = IntVar()
    Checkbox = CTkEntry(root, text=student_data["name"], variable=Checkbox_var)
    Checkbox.configure(border_width=2,checkbox_width=20,checkbox_height=20)
    Checkbox.place(relx=0.5, y=i,anchor=CENTER)
    Checkboxs.append(Checkbox_var)
    i += 40

# Create a button to mark attendance
mark_button = CTkButton(root, text="Mark Attendance", command=mark_attendance)
mark_button.place(relx=0.5, y=i+50,anchor=CENTER)

root.mainloop()







from ttkwidgets import CheckboxTreeview
import tkinter as tk
import pymysql

db = pymysql.connect(host="localhost", user="root", password="root", database="student_database", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
cursor.execute("SELECT name FROM student WHERE std_code=%s", ("10th std"))
data=cursor.fetchall()
stud_id=[]
name=[]


for i in data:
        id=i.get("stud_id")
        na=i.get("name")
        stud_id.append(id)
        name.append(na)

root = tk.Tk()
tree = CheckboxTreeview(root)

for row in name:
    tree.insert('', 'end', values=row)
tree.pack()
root.mainloop()