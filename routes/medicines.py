from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Medicine, Supplier, Stock

medicines_bp = Blueprint('medicines', __name__, url_prefix='/medicines')

@medicines_bp.route('/')
@login_required
def list():
    search = request.args.get('search', '').strip()
    query = Medicine.query.join(Stock, isouter=True)
    if search:
        query = query.filter(Medicine.name.ilike(f'%{search}%'))
    medicines = query.order_by(Medicine.name).all()
    return render_template('medicines/list.html', medicines=medicines, search=search)

@medicines_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    if request.method == 'POST':
        med = Medicine(
            name         = request.form['name'],
            generic_name = request.form.get('generic_name'),
            category     = request.form.get('category'),
            dosage_form  = request.form.get('dosage_form'),
            strength     = request.form.get('strength'),
            supplier_id  = request.form.get('supplier_id') or None,
            expiry_date  = request.form.get('expiry_date') or None,
            price        = float(request.form.get('price', 0)),
            reorder_level= int(request.form.get('reorder_level', 10)),
        )
        db.session.add(med)
        db.session.flush()  # get med.id before commit

        # Create stock entry
        stock = Stock(
            medicine_id  = med.id,
            quantity     = int(request.form.get('quantity', 0)),
            batch_number = request.form.get('batch_number'),
        )
        db.session.add(stock)
        db.session.commit()
        flash(f'Medicine "{med.name}" added successfully.', 'success')
        return redirect(url_for('medicines.list'))

    return render_template('medicines/form.html', medicine=None, suppliers=suppliers)

@medicines_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    med = Medicine.query.get_or_404(id)
    suppliers = Supplier.query.order_by(Supplier.name).all()
    if request.method == 'POST':
        med.name          = request.form['name']
        med.generic_name  = request.form.get('generic_name')
        med.category      = request.form.get('category')
        med.dosage_form   = request.form.get('dosage_form')
        med.strength      = request.form.get('strength')
        med.supplier_id   = request.form.get('supplier_id') or None
        med.expiry_date   = request.form.get('expiry_date') or None
        med.price         = float(request.form.get('price', 0))
        med.reorder_level = int(request.form.get('reorder_level', 10))

        if med.stock:
            med.stock.quantity     = int(request.form.get('quantity', 0))
            med.stock.batch_number = request.form.get('batch_number')

        db.session.commit()
        flash(f'Medicine "{med.name}" updated.', 'success')
        return redirect(url_for('medicines.list'))

    return render_template('medicines/form.html', medicine=med, suppliers=suppliers)

@medicines_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    med = Medicine.query.get_or_404(id)
    db.session.delete(med)
    db.session.commit()
    flash(f'Medicine "{med.name}" deleted.', 'warning')
    return redirect(url_for('medicines.list'))
