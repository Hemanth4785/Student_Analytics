 Student Performance Analytics Dashboard 📊

This is a full-stack web app I built to track, store, and analyze student academic data. It's completely hosted in the cloud, using Flask for the backend, a cloud-managed TiDB MySQL database to keep data secure, and Pandas/NumPy to handle all the background math.

🌐 Check out the live app here: (https://student-analytics-76e7.onrender.com)

 🔥 What it does

Manage Student Records:You can add new students, view the entire roster, and delete records straight from a clean browser dashboard.
Smart Analytics:The app automatically runs calculations in the background to show running class averages, highest subject scores, and overall attendance tracking.
Cloud Database Integration:Tied directly into a production-ready "TiDB Cloud Serverless MySQL" cluster instance.
Download Reports:Hit a button to instantly download your current data view as a clean CSV spreadsheet log.

🛠️ Tech Stack

Frontend:Simple, responsive HTML5 and CSS3 templates.
Backend:Python Flask framework.
Data Processing:Pandas and NumPy.
Database:Cloud MySQL (via `mysql-connector-python`).
Hosting:Hosted on Render (using Gunicorn) and connected to "TiDB Cloud" (AWS Singapore cluster).
