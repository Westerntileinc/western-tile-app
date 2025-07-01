
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import pdfkit
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workorders.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='installer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, unique=True, nullable=False)
    work_order_code = db.Column(db.String(20), unique=True)
    status = db.Column(db.String(20), default="Pending")
    customer_name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    job_number = db.Column(db.String(50), unique=True)
    contract_number = db.Column(db.String(50))
    install_date = db.Column(db.String(50))
    sales_person = db.Column(db.String(100))
    installer = db.Column(db.String(100))
    labor_description = db.Column(db.Text)
    product_description = db.Column(db.Text)
    labor_cost = db.Column(db.Float)
    material_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    photo_filename = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
@login_required
def index():
    query = WorkOrder.query
    if current_user.role == 'installer':
        query = query.filter(WorkOrder.installer == current_user.username)

    installer_filter = request.args.get('installer')
    job_filter = request.args.get('job')
    if installer_filter:
        query = query.filter(WorkOrder.installer.contains(installer_filter))
    if job_filter:
        query = query.filter(WorkOrder.job_number.contains(job_filter))

    orders = query.order_by(WorkOrder.created_at.desc()).all()
    return render_template('index.html', orders=orders, user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
