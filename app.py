from flask import Flask, render_template, request, redirect, url_for
from models import db, WorkOrder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workorders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("create_work_order"))

@app.route("/create", methods=["GET", "POST"])
def create_work_order():
    if request.method == "POST":
        work_order = WorkOrder(
            customer_name=request.form["customer_name"],
            company=request.form["company"],
            job_number=request.form["job_number"],
            contract_number=request.form["contract_number"],
            install_date=request.form["install_date"],
            installer=request.form["installer"],
            sales_person=request.form["sales_person"],
            labor_description=request.form["labor_description"],
            product_description=request.form["product_description"],
            labor_cost=request.form["labor_cost"],
            material_cost=request.form["material_cost"],
            notes=request.form["notes"]
        )
        db.session.add(work_order)
        db.session.commit()
        return redirect(url_for("list_work_orders"))
    return render_template("create_work_order.html")

@app.route("/orders")
def list_work_orders():
    orders = WorkOrder.query.order_by(WorkOrder.created_at.desc()).all()
    return render_template("work_orders.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
