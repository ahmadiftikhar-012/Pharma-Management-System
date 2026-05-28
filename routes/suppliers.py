from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Supplier

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

@suppliers_bp.route('/')
@login_required
def list():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template('suppliers/list.html', suppliers=suppliers)

@suppliers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        s = Supplier(
            name           = request.form['name'],
            contact_person = request.form.get('contact_person'),
            phone          = request.form.get('phone'),
            email          = request.form.get('email'),
            address        = request.form.get('address'),
        )
        db.session.add(s)
        db.session.commit()
        flash('Supplier added.', 'success')
        return redirect(url_for('suppliers.list'))
    return render_template('suppliers/form.html', supplier=None)

@suppliers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    s = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        s.name           = request.form['name']
        s.contact_person = request.form.get('contact_person')
        s.phone          = request.form.get('phone')
        s.email          = request.form.get('email')
        s.address        = request.form.get('address')
        db.session.commit()
        flash('Supplier updated.', 'success')
        return redirect(url_for('suppliers.list'))
    return render_template('suppliers/form.html', supplier=s)

@suppliers_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    s = Supplier.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Supplier deleted.', 'warning')
    return redirect(url_for('suppliers.list'))
