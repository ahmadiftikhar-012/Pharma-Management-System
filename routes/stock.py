from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Medicine, Stock

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

@stock_bp.route('/')
@login_required
def list():
    items = db.session.query(Medicine, Stock).join(Stock).order_by(Medicine.name).all()
    return render_template('stock/list.html', items=items)

@stock_bp.route('/update/<int:medicine_id>', methods=['GET', 'POST'])
@login_required
def update(medicine_id):
    med   = Medicine.query.get_or_404(medicine_id)
    stock = Stock.query.filter_by(medicine_id=medicine_id).first_or_404()

    if request.method == 'POST':
        action   = request.form.get('action', 'set')
        qty      = int(request.form.get('quantity', 0))
        batch    = request.form.get('batch_number', stock.batch_number)

        if action == 'add':
            stock.quantity += qty
        elif action == 'subtract':
            if stock.quantity - qty < 0:
                flash('Cannot subtract more than available stock.', 'danger')
                return redirect(url_for('stock.update', medicine_id=medicine_id))
            stock.quantity -= qty
        else:
            stock.quantity = qty

        stock.batch_number = batch
        db.session.commit()
        flash(f'Stock for "{med.name}" updated to {stock.quantity}.', 'success')
        return redirect(url_for('stock.list'))

    return render_template('stock/update.html', medicine=med, stock=stock)
