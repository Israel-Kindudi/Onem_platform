from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from forms import JobSeekerForm, CompanyForm
from models import db, JobSeeker, Company
import random
import string

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def generate_unique_id(province):
    return province[:3].upper() + ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/job_seeker', methods=['GET', 'POST'])
def register_job_seeker():
    form = JobSeekerForm()
    if form.validate_on_submit():
        unique_id = generate_unique_id(form.province.data)
        job_seeker = JobSeeker(name=form.name.data, email=form.email.data, province=form.province.data, unique_id=unique_id, documents=form.documents.data)
        db.session.add(job_seeker)
        db.session.commit()
        flash('Job Seeker registered successfully!')
        return redirect(url_for('index'))
    return render_template('register_job_seeker.html', form=form)

@app.route('/register/company', methods=['GET', 'POST'])
def register_company():
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data, email=form.email.data, tender_details=form.tender_details.data)
        db.session.add(company)
        db.session.commit()
        flash('Company registered and tender submitted successfully!')
        return redirect(url_for('index'))
    return render_template('register_company.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
