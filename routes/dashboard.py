from flask import Blueprint, render_template
from flask_login import login_required
from models import db, Medicine, Stock, Sale, SaleItem, Supplier
from sqlalchemy import func
from datetime import date, timedelta, datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    today = date.today()

    total_medicines = Medicine.query.count()
    total_suppliers = Supplier.query.count()

    # Low stock count
    low_stock_count = db.session.query(Stock).join(Medicine).filter(
        Stock.quantity < Medicine.reorder_level
    ).count()

    # Expiring soon (within 30 days)
    expiring_count = Medicine.query.filter(
        Medicine.expiry_date.between(today, today + timedelta(days=30))
    ).count()

    # Today's sales

    todays_sales = Sale.query.filter(
      func.date(Sale.sale_date) == today
    ).all()
    todays_revenue = sum(float(s.total_amount) for s in todays_sales)

    # Recent 5 sales
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(5).all()

    # Low stock medicines for table
    low_stock_items = db.session.query(Medicine, Stock).join(Stock).filter(
        Stock.quantity < Medicine.reorder_level
    ).limit(5).all()

    return render_template('dashboard.html',
        total_medicines=total_medicines,
        low_stock_count=low_stock_count,
        expiring_count=expiring_count,
        todays_revenue=todays_revenue,
        todays_sales_count=len(todays_sales),
        recent_sales=recent_sales,
        low_stock_items=low_stock_items,
    )
