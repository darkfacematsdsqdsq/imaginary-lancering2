from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialiseer de Flask-applicatie
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Vervang dit door een echte, veilige sleutel

# Configureer de SQLite-database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Definieer het User-model voor databasegebruikers
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Email als leesbare string
    password = db.Column(db.String(150), nullable=False)  # Gehashte wachtwoorden als string

# Registratiepagina en -functionaliteit
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Controleer of de gebruiker al bestaat
        if User.query.filter_by(email=email).first():
            return "Email bestaat al. Probeer een ander e-mailadres."
        
        # Voeg de nieuwe gebruiker toe
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Inlogpagina en -functionaliteit
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Haal de gebruiker op met het opgegeven e-mailadres
        user = User.query.filter_by(email=email).first()
        
        # Controleer wachtwoord en log gebruiker in
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return "Je bent succesvol ingelogd!"
        return "Ongeldige inloggegevens!"
    return render_template('login.html')

# Start de applicatie en maak de database aan als deze nog niet bestaat
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Maak de database tabellen aan binnen de juiste context
    app.run(debug=True)
