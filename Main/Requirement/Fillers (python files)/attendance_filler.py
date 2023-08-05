import pymysql
import random
from datetime import date, timedelta
# First connection
db = pymysql.connect(host="localhost", user="root", password="root", database="student_database",
                     charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

stand_list = ["5th std", "6th std", "7th std", "8th std", "9th std", "10th std"]

for Std in stand_list:
    cursor = db.cursor()
    cursor.execute("SELECT teacher.teacher_id, subject.sub_id FROM teacher, class, teach_class, subject "
                "WHERE teacher_id = teacher_code AND sub_id = sub_code AND std_id = std_code AND std_id = %s", (Std,))
    data = cursor.fetchall()
    subject_id = []
    teach_id = []
    for i in data:
        teacher_id = i.get("teacher_id")
        sub_id = i.get("sub_id")

        teach_id.append(teacher_id)
        subject_id.append(sub_id)

    cursor.execute("SELECT COUNT(*) FROM student WHERE std_code = %s", (Std,))
    tot = cursor.fetchall()
    total_stud = tot[0].get("COUNT(*)")


    def generate():
        random1 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
        sheet = ""
        for _ in range(total_stud):
            sheet += str(random.choice(random1))
        return sheet


    start_date = date(2023, 6, 15)
    end_date = date(2023, 8, 4)
    date_list = []
    while start_date <= end_date:
        date_list.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)

    for sub_code in subject_id:
        for to_date in date_list:
            result = generate()
            cursor = db.cursor()
            cursor.execute("INSERT INTO attendance VALUES (%s, %s, %s, %s)", (Std, sub_code, to_date, result))
            db.commit()
