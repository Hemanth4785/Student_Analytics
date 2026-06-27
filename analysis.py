import pandas as pd
import numpy as np

def get_analytics_summary(conn):
    df = pd.read_sql("SELECT * FROM students", conn)
    
    # 1. Pull data directly into a pandas DataFrame
    if df.empty:
        return None
        
    # 2. To calculate total and average marks per student
    # FIXED: Replaced old column names with your exact database columns
    df['total_marks'] = df['Maths'] + df['Chemistry'] + df['Physics']
    df['average_marks'] = df['total_marks'] / 3
    
    # 3. Numpy operation
    all_averages = df['average_marks'].to_numpy()
    all_attendance = df['Attendance'].to_numpy() # FIXED: Capitalized 'Attendance'

    metrics = {
        "total_students": len(df),
        "global_average": round(np.mean(all_averages), 2),
        "median_score": round(np.median(all_averages), 2),
        "std_dev": round(np.std(all_averages), 2),
        "avg_attendance": round(np.mean(all_attendance), 2)
    }
    
    # 4. To find the toppers
    topper_row = df.loc[df['total_marks'].idxmax()]
    metrics['topper_name'] = topper_row['Name'] # FIXED: Capitalized 'Name'
    metrics['topper_score'] = round(topper_row['average_marks'], 2)

    return metrics

def export_to_csv(conn):
    df = pd.read_sql("SELECT * FROM students", conn)
    df.to_csv("students_report.csv", index=False)