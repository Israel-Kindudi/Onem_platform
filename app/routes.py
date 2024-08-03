from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app import db
from app.forms import JobSeekerForm, CompanyForm, AdminLoginForm
from app.models import JobSeeker, Company, Admin
from app.email import send_email
import random
import string
import os
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_id(province):
    return province[:3].upper() + ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register/job_seeker', methods=['GET', 'POST'])
def register_job_seeker():
    form = JobSeekerForm()
    if form.validate_on_submit():
        files = {}
        for file_field in ['identite_document', 'diplome_document', 'diplome_equivalence', 'formation_certificative_document']:
            file = getattr(form, file_field).data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                files[file_field] = file_path
            
        unique_id = generate_unique_id(form.province.data)
        job_seeker = JobSeeker(
            name=form.nom.data,
            email=form.email.data,
            province=form.province.data,
            unique_id=unique_id,
            documents=files.get('identite_document', ''),
            diplome=files.get('diplome_document', ''),
            equivalence=files.get('diplome_equivalence', ''),
            formation_certificative=files.get('formation_certificative_document', ''),
            **{field: getattr(form, field).data for field in [
                'username', 'prenom', 'post_nom', 'lieu_naissance', 'date_naissance', 
                'nationalite', 'sexe', 'etat_civil', 'personnes_charge', 'telephone', 
                'telephone2', 'adresse_numero', 'adresse_rue', 'adresse_quartier', 
                'adresse_commune', 'adresse_ville', 'adresse_district', 'adresse_province', 
                'adresse_pays', 'niveau_etudes', 'diplome_pays', 'diplome_institution', 
                'diplome_ville', 'diplome_intitule', 'diplome_debut', 'diplome_fin', 
                'formation_intitule', 'formation_lieu_dates', 'formation_organisme', 
                'formation_qualifiante', 'langue_parlee', 'langue_niveau', 'bureautique_programme', 
                'bureautique_niveau', 'bureautique_exemple', 'permis_conduire', 'permis_categorie', 
                'salaire_souhaite', 'raison_inscription', 'premiere_inscription', 'numero_carte', 
                'dernier_emploi', 'duree_emploi', 'motif_fin_contrat', 'fonction_occupee', 
                'emploi_recherche', 'choix1', 'choix2', 'experience1_fonction', 'experience1_periode', 
                'experience2_fonction', 'experience2_periode', 'experience3_fonction', 'experience3_periode'
            ]}
        )
        db.session.add(job_seeker)
        db.session.commit()
        flash('Job Seeker registered successfully!')
        return redirect(url_for('main.index'))
    return render_template('register_de.html', form=form)

@bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data, email=form.email.data, tender_details=form.tender_details.data)
        db.session.add(company)
        db.session.commit()
        flash('Company registered and tender submitted successfully!')
        return redirect(url_for('main.index'))
    return render_template('register_company.html', form=form)

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.admin_login'))
        session['admin_id'] = admin.id
        return redirect(url_for('main.admin_dashboard'))
    return render_template('admin_login.html', form=form)

@bp.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('main.admin_login'))
    job_seekers = JobSeeker.query.all()
    return render_template('admin_dashboard.html', job_seekers=job_seekers)

@bp.route('/admin/approve/<int:job_seeker_id>')
def approve_job_seeker(job_seeker_id):
    if 'admin_id' not in session:
        return redirect(url_for('main.admin_login'))
    job_seeker = JobSeeker.query.get(job_seeker_id)
    if job_seeker:
        job_seeker.is_verified = True
        db.session.commit()
        flash(f'Job Seeker {job_seeker.name} has been approved.')
        send_email(job_seeker.email, 'Your documents have been approved', 'Your documents have been approved by the admin.')
    return redirect(url_for('main.admin_dashboard'))
