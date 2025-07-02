from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    job_number = db.Column(db.String(50))
    contract_number = db.Column(db.String(50))
    install_date = db.Column(db.String(50))
    installer = db.Column(db.String(100))
    sales_person = db.Column(db.String(100))
    labor_description = db.Column(db.Text)
    product_description = db.Column(db.Text)
    labor_cost = db.Column(db.Float)
    material_cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
