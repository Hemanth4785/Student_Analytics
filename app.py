import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from analysis import get_analytics_summary, export_to_csv

app = Flask(__name__)

# database connection setup
def get_db_connection():
    # 1. Attempt to pull from Render Environment Variables first
    db_url = os.environ.get("DATABASE_URL")
    
    if db_url:
        try:
            # Parse connection string format: mysql://username:password@hostname:port/database
            clean_url = db_url.replace("mysql://", "")
            credentials, host_info = clean_url.split("@")
            username, password = credentials.split(":")
            host_port, database_name = host_info.split("/")
            hostname, port = host_port.split(":")
            
            return mysql.connector.connect(
                host=hostname,
                user=username,
                password=password,
                database=database_name,
                port=int(port)
            )
        except Exception as e:
            print(f"Error parsing DATABASE_URL, falling back: {e}")
            
    # 2. Hardcoded fallback using your active TiDB Cloud parameters
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        user="X9FotYhjvHf7oBo.root",
        password="frG0dw5Rd6jcHLPg",
        database="sys",
        port=4000
    )

# 1: Main Dashboard
@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all student rows for the HTML table
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    # Get calculated statistics from analysis engine
    analytics = get_analytics_summary(conn)
    cursor.close()
    conn.close()
    
    return render_template('index.html', students=students, analytics=analytics)

# 2: Add Student Form Processing
@app.route('/add', methods=['GET', 'POST'])
def add_students():
    if request.method == 'POST':
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

# 3: Delete Student record
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE ID=%s", (id,)) 
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

# 4: Export report to CSV
@app.route('/export')
def export_report():
    conn = get_db_connection()
    export_to_csv(conn)
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Dynamic binding setup for Render cluster routing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)