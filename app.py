from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            company_name TEXT,
            location TEXT,
            job_type TEXT,
            salary_range TEXT,
            application_deadline TEXT,
            job_description TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM jobs')
    jobs = c.fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

@app.route('/create_job', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        # Collect form data
        job_title = request.form['job_title']
        company_name = request.form['company_name']
        location = request.form['location']
        job_type = request.form['job_type']
        salary_range = f"{request.form.get('salary_min', '')} - {request.form.get('salary_max', '')}"
        application_deadline = request.form['application_deadline']
        job_description = request.form['job_description']

        # Insert into database
        conn = sqlite3.connect('jobs.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO jobs (
                job_title, company_name, location, job_type, 
                salary_range, application_deadline, job_description
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (job_title, company_name, location, job_type, 
              salary_range, application_deadline, job_description))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('create_job.html')

if __name__ == '__main__':
    app.run(debug=True)