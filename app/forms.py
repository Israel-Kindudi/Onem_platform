from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileAllowed, FileRequired

class JobSeekerForm(FlaskForm):
    # Connexion Details
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password1 = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Confirmer mot de passe', validators=[DataRequired(), EqualTo('password1')])

    # Personal Details
    nom = StringField('Nom', validators=[DataRequired()])
    post_nom = StringField('Post-nom')
    prenom = StringField('Prénom', validators=[DataRequired()])
    lieu_naissance = StringField('Lieu de naissance', validators=[DataRequired()])
    date_naissance = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    nationalite = StringField('Nationalité', validators=[DataRequired()])
    sexe = SelectField('Sexe', choices=[('Homme', 'Homme'), ('Femme', 'Femme')], validators=[DataRequired()])
    etat_civil = SelectField('Etat civil', choices=[('Célibataire', 'Célibataire'), ('Marié/e', 'Marié/e'), ('Veuf/ve', 'Veuf/ve')], validators=[DataRequired()])
    personnes_charge = IntegerField('Nombre de personnes à charge', validators=[DataRequired(), NumberRange(min=0)])

    # Contact Information
    telephone = StringField('Téléphone', validators=[DataRequired()])
    telephone2 = StringField('Téléphone 2')
    email = StringField('E-mail', validators=[DataRequired(), Email()])

    # Documents
    identite_type = SelectField('Documents de preuve d\'identité', choices=[('Carte d\'identité', 'Carte d\'identité'), ('Carte d\'électeur', 'Carte d\'électeur'), ('Passeport', 'Passeport'), ('Autre', 'Autre')], validators=[DataRequired()])
    identite_autre = StringField('Autre (à préciser)')
    identite_document = FileField('Documents de preuve d\'identité', validators=[FileRequired(), FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDFs and images only!')])
    adresse_numero = StringField('Numéro', validators=[DataRequired()])
    adresse_rue = StringField('Rue/avenue', validators=[DataRequired()])
    adresse_quartier = StringField('Quartier', validators=[DataRequired()])
    adresse_commune = StringField('Commune', validators=[DataRequired()])
    adresse_ville = StringField('Ville', validators=[DataRequired()])
    adresse_district = StringField('District', validators=[DataRequired()])
    adresse_province = StringField('Province', validators=[DataRequired()])
    adresse_pays = StringField('Pays de résidence', validators=[DataRequired()])

    # Education and Documents
    niveau_etudes = SelectField('Niveau d\'études', choices=[
        ('0', '0'), ('Prim', 'Prim'), ('CO', 'CO'), ('PP4', 'PP4'), ('PP5/A3', 'PP5/A3'), 
        ('D6/A2', 'D6/A2'), ('Cap', 'Cap'), ('G3/A1', 'G3/A1'), ('L2', 'L2'), 
        ('D.E.S.', 'D.E.S.'), ('Doct', 'Doct')
    ], validators=[DataRequired()])
    diplome_document = FileField('Photo du diplôme', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDFs and images only!')])
    diplome_pays = StringField('Pays d\'obtention de votre titre', validators=[DataRequired()])
    diplome_equivalence = FileField('Photo du document d\'équivalence', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDFs and images only!')])
    diplome_institution = StringField('Nom de l\'institution', validators=[DataRequired()])
    diplome_ville = StringField('Ville', validators=[DataRequired()])
    diplome_intitule = StringField('Intitulé exact repris sur le titre', validators=[DataRequired()])
    diplome_debut = DateField('Année de début', format='%Y-%m-%d', validators=[DataRequired()])
    diplome_fin = DateField('Année de fin', format='%Y-%m-%d', validators=[DataRequired()])

    # Professional Training
    formation_intitule = StringField('Intitulé de la formation professionnelle suivie')
    formation_lieu_dates = StringField('Lieu et dates (de … à ….)')
    formation_organisme = StringField('Organisme de formation')
    formation_qualifiante = SelectField('Formation qualifiante ou certificative', choices=[('Qualifiante', 'Qualifiante'), ('Certificative', 'Certificative')])
    formation_certificative_document = FileField('Photo du brevet de réussite', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDFs and images only!')])

    # Skills
    langue_parlee = StringField('Langue parlée')
    langue_niveau = StringField('Niveau')
    bureautique_programme = StringField('Nom du programme')
    bureautique_niveau = StringField('Niveau de maîtrise')
    bureautique_exemple = StringField('Exemple d\'opérations que vous pouvez réaliser')
    
    # Driving License
    permis_conduire = SelectField('Avez-vous un permis de conduire ?', choices=[('Non', 'Non'), ('Oui', 'Oui')])
    permis_categorie = SelectField('Catégorie', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')])
    
    # Salary and Motivation
    salaire_souhaite = IntegerField('Montant de salaire souhaité (en $)', validators=[DataRequired(), NumberRange(min=0)])
    raison_inscription = StringField('Raisons de votre inscription à l\'ONEM', validators=[DataRequired()])
    
    # Job Search
    premiere_inscription = SelectField('Est-ce votre première inscription à l’ONEM ?', choices=[('Oui', 'Oui'), ('Non', 'Non')], validators=[DataRequired()])
    numero_carte = StringField('Numéro repris sur votre Carte de Demandeur d\'Emploi', validators=[DataRequired()])
    dernier_emploi = StringField('Dernier emploi occupé', validators=[DataRequired()])
    duree_emploi = StringField('Durée (De ... à ...)', validators=[DataRequired()])
    motif_fin_contrat = SelectField('Motif de fin de contrat', choices=[('Démission', 'Démission'), ('Licenciement', 'Licenciement'), ('Fin de contrat', 'Fin de contrat')], validators=[DataRequired()])
    fonction_occupee = StringField('Fonction occupée', validators=[DataRequired()])
    emploi_recherche = StringField('Emploi recherché (Profession/métier)', validators=[DataRequired()])
    choix1 = StringField('1er choix', validators=[DataRequired()])
    choix2 = StringField('2ème choix', validators=[DataRequired()])
    
    # Previous Experience
    experience1_fonction = StringField('Fonction occupée 1')
    experience1_periode = StringField('Période 1 (De ... à ...)')
    experience2_fonction = StringField('Fonction occupée 2')
    experience2_periode = StringField('Période 2 (De ... à ...)')
    experience3_fonction = StringField('Fonction occupée 3')
    experience3_periode = StringField('Période 3 (De ... à ...)')
    
    # Submit
    submit = SubmitField('Register')

class CompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    tender_details = StringField('Tender Details', validators=[DataRequired()])
    submit = SubmitField('Submit Tender')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
