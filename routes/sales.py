from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from models import db, Sale, SaleItem, Medicine, Stock
from datetime import date, datetime

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/')
@login_required
def list():
    sales = Sale.query.order_by(Sale.sale_date.desc()).all()
    return render_template('sales/list.html', sales=sales)

@sales_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    medicines = Medicine.query.join(Stock).filter(Stock.quantity > 0).order_by(Medicine.name).all()

    if request.method == 'POST':
        customer      = request.form.get('customer_name', 'Walk-in')
        payment       = request.form.get('payment_method', 'cash')
        medicine_ids  = request.form.getlist('medicine_id[]')
        quantities    = request.form.getlist('quantity[]')

        if not medicine_ids:
            flash('Add at least one medicine to the sale.', 'danger')
            return render_template('sales/new.html', medicines=medicines)

        total = 0.0
        items_data = []

        for med_id, qty in zip(medicine_ids, quantities):
            med   = Medicine.query.get(int(med_id))
            qty   = int(qty)
            stock = Stock.query.filter_by(medicine_id=med.id).first()

            if not med or qty <= 0:
                continue
            if stock.quantity < qty:
                flash(f'Insufficient stock for {med.name}.', 'danger')
                return render_template('sales/new.html', medicines=medicines)

            subtotal = float(med.price) * qty
            total   += subtotal
            items_data.append((med, qty, float(med.price), stock))

        # All checks passed — commit atomically
        sale = Sale(customer_name=customer, total_amount=total, payment_method=payment, sale_date=datetime.now())
        db.session.add(sale)
        db.session.flush()

        for med, qty, price, stock in items_data:
            db.session.add(SaleItem(
                sale_id=sale.id, medicine_id=med.id,
                quantity=qty, unit_price=price
            ))
            stock.quantity -= qty

        db.session.commit()
        flash(f'Sale #{sale.id} recorded. Total: Rs. {total:.2f}', 'success')
        return redirect(url_for('sales.receipt', id=sale.id))

    return render_template('sales/new.html', medicines=medicines)

@sales_bp.route('/receipt/<int:id>')
@login_required
def receipt(id):
    sale = Sale.query.get_or_404(id)
    return render_template('sales/receipt.html', sale=sale)
