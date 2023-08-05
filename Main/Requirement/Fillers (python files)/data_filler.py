import pymysql
import random
db=pymysql.connect(host="localhost",user="root",password="root",database="student_database",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)

indian_names = ["Aarav Patel", "Aditi Sharma", "Advait Singh", "Akshay Desai", "Alisha Gupta", "Aman Mehta", "Amrita Chauhan", "Ananya Bhatia",
    "Aniket Joshi", "Anisha Shah", "Ankit Kumar", "Anushka Reddy", "Arjun Malhotra", "Aryan Singh", "Avani Verma", "Ayush Gupta",
    "Chahat Sharma", "Devika Mehta", "Dhruv Patel", "Diya Singh", "Esha Kapoor", "Gaurav Sharma", "Gayatri Shah", "Harshita Patel",
    "Ishaan Gupta", "Ishika Sharma", "Jatin Kapoor", "Karan Malhotra", "Kavya Shah", "Krishna Chauhan", "Kritika Verma", "Mahi Kapoor",
    "Mannat Bajaj", "Mayank Singh", "Mehak Patel", "Mohit Choudhury", "Muskaan Gupta", "Nakshatra Sharma", "Naman Kapoor", "Nandini Patel",
    "Neha Malhotra", "Niharika Shah", "Nishant Verma", "Palak Chauhan", "Parth Patel", "Pranav Sharma", "Preeti Kapoor", "Raghav Malhotra",
    "Rashi Shah", "Rishabh Verma", "Riya Gupta", "Rohan Patel", "Sakshi Sharma", "Samar Kapoor", "Sanaya Malhotra", "Sanya Shah",
    "Shivansh Verma", "Shreya Chauhan", "Simran Kapoor", "Sneha Malhotra", "Suhana Shah", "Tanya Gupta", "Tarun Patel", "Trisha Sharma",
    "Ujjwal Verma", "Vansh Kapoor", "Varsha Shah", "Vedant Malhotra", "Vidhi Patel", "Vishal Sharma", "Yash Chauhan", "Zara Verma"]

name_genders = ["M", "F", "M", "M", "F", "M", "F", "F", "M", "F", "M", "F", "M", "M", "F", "M", "F", "F", "M", "F", "F", "M", "F", "F",
    "M", "F", "M", "M", "F", "F", "F", "M", "F", "M", "M", "F", "F", "F", "M", "M", "F", "F", "M", "F", "F", "M", "F", "F",
    "M", "F", "M", "M", "F", "M", "F", "F", "M", "F", "M", "M", "F", "F", "F", "F", "M", "F", "M", "F", "M", "M", "F", "M",
    "F", "M", "F", "M", "M", "F", "F", "M", "M", "F", "F", "F", "F", "M", "F", "M", "F", "M", "M", "F", "F", "M", "F", "M",
    "F", "M", "M", "F", "M", "F", "F", "M", "M", "F", "M", "M", "F", "F", "F", "F", "M", "M", "F", "M", "F", "F", "M", "F",
    "F", "F", "M", "F", "F", "M", "F", "M", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "M", "F", "F",
    "M", "F", "M", "F", "M", "F", "M", "F", "F", "M"]

indian_standards = ["5th std", "6th std", "7th std", "8th std", "9th std", "10th std"]


mumbai_addresses = ["1234 Marine Drive Nariman Point Mumbai Maharashtra India", "5678 Bandstand Promenade Bandra West Mumbai Maharashtra India", "9012 Juhu Tara Road Juhu Mumbai Maharashtra India", "3456 Andheri Kurla Road Andheri East Mumbai Maharashtra India", "7890 Worli Sea Face Worli Mumbai Maharashtra India", "2345 Hiranandani Gardens Powai Mumbai Maharashtra India", "6789 Colaba Causeway Colaba Mumbai Maharashtra India", "0123 Linking Road Santacruz West Mumbai Maharashtra India", "4567 Vile Parle West Vile Parle Mumbai Maharashtra India", "8901 Dadar West Dadar Mumbai Maharashtra India", "2345 Goregaon East Goregaon Mumbai Maharashtra India", "6789 Chembur Colony Chembur Mumbai Maharashtra India", "0123 Lower Parel Mumbai Maharashtra India", "4567 Thane West Thane Mumbai Maharashtra India", "8901 Kurla West Kurla Mumbai Maharashtra India"]


def generate_random_dob():
    year = random.randint(2005, 2013)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"

def generate_random_number():
    first_digit = random.choice(['9', '8', '7'])
    remaining_digits = ''.join(random.choices('0123456789', k=9))
    return int(first_digit + remaining_digits)



id =137
for name,gen in zip(indian_names,name_genders):
    add=random.choice(mumbai_addresses)
    std=random.choice(indian_standards)
    dob = generate_random_dob()
    phone = generate_random_number()
    cursor=db.cursor()
    cursor.execute("insert into student(stud_id,name,gen,std_code,dob,phone_no,address) values(%s,%s,%s,%s,%s,%s,%s)",(id,name,gen,std,dob,phone,add))
    db.commit()
    id+=1