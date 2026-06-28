import os
import urllib.parse as urlparse
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from analysis import get_analytics_summary, export_to_csv

app = Flask(__name__)

# database connection
def get_db_connection():
    db_url = os.environ.get("mysql://X9FotYhjvHf7oBo.root:<PASSWORD>@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/sys") #key
    
    if db_url:
        url = urlparse.urlparse(db_url)
        return mysql.connector.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],  
            port=url.port or 3306
        )
    else:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Venomrd@47",
            database="sample"
        )

# 1: main dashboard
@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # get all student row for html table
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    # Get calculated statistics from our analysis file
    analytics = get_analytics_summary(conn)
    cursor.close()
    conn.close()
    
    return render_template('index.html', students=students, analytics=analytics)

# 2: Add Student Form and logic
@app.route('/add', methods=['GET', 'POST'])
def add_students():
    if request.method == 'POST':
        # Grab data out of the html form fields
        name = request.form['name']
        dept = request.form['department']
        Maths = int(request.form['Maths_marks'])
        Chemistry = int(request.form['Chemistry_marks'])
        Physics = int(request.form['Physics_marks'])
        attendance = float(request.form['attendance'])

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """INSERT INTO students(Name, Department, Maths, Chemistry, Physics, Attendance) 
                   VALUES(%s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(query, (name, dept, Maths, Chemistry, Physics, attendance))
        
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    return render_template('add_students.html')

# 3: DELETE STUDENT
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE ID=%s", (id,)) 
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

# 4: CSV Export
@app.route('/export')
def export_report():
    conn = get_db_connection()
    export_to_csv(conn)
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)