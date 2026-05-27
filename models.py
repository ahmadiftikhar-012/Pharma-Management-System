from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ──────────────────────────────────────────
# User model (login system)
# ──────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80),  nullable=False, unique=True)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.Enum('admin', 'cashier'), default='cashier')
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'

# ──────────────────────────────────────────
# Supplier model
# ──────────────────────────────────────────
class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(120), nullable=False)
    contact_person = db.Column(db.String(100))
    phone          = db.Column(db.String(20))
    email          = db.Column(db.String(120))
    address        = db.Column(db.Text)

    medicines = db.relationship('Medicine', backref='supplier', lazy=True)

    def __repr__(self):
        return f'<Supplier {self.name}>'

# ──────────────────────────────────────────
# Medicine model
# ──────────────────────────────────────────
class Medicine(db.Model):
    __tablename__ = 'medicines'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    generic_name  = db.Column(db.String(120))
    category      = db.Column(db.String(80))
    dosage_form   = db.Column(db.String(80))
    strength      = db.Column(db.String(50))
    supplier_id   = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    expiry_date   = db.Column(db.Date)
    price         = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    reorder_level = db.Column(db.Integer, nullable=False, default=10)

    stock      = db.relationship('Stock', backref='medicine', uselist=False, lazy=True)
    sale_items = db.relationship('SaleItem', backref='medicine', lazy=True)

    @property
    def is_expiring_soon(self):
        if self.expiry_date:
            delta = (self.expiry_date - date.today()).days
            return 0 <= delta <= 30
        return False

    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < date.today()
        return False

    @property
    def is_low_stock(self):
        if self.stock:
            return self.stock.quantity < self.reorder_level
        return True

    def __repr__(self):
        return f'<Medicine {self.name}>'

# ──────────────────────────────────────────
# Stock model
# ──────────────────────────────────────────
class Stock(db.Model):
    __tablename__ = 'stock'

    id           = db.Column(db.Integer, primary_key=True)
    medicine_id  = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity     = db.Column(db.Integer, nullable=False, default=0)
    batch_number = db.Column(db.String(80))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Stock medicine_id={self.medicine_id} qty={self.quantity}>'

# ──────────────────────────────────────────
# Sale model
# ──────────────────────────────────────────
class Sale(db.Model):
    __tablename__ = 'sales'

    id             = db.Column(db.Integer, primary_key=True)
    sale_date      = db.Column(db.DateTime, default=datetime.utcnow)
    customer_name  = db.Column(db.String(120))
    total_amount   = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    payment_method = db.Column(db.Enum('cash', 'card', 'online'), default='cash')

    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Sale id={self.id} total={self.total_amount}>'

# ──────────────────────────────────────────
# SaleItem model (junction: Sale <-> Medicine)
# ──────────────────────────────────────────
class SaleItem(db.Model):
    __tablename__ = 'sale_items'

    id          = db.Column(db.Integer, primary_key=True)
    sale_id     = db.Column(db.Integer, db.ForeignKey('sales.id'),     nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity    = db.Column(db.Integer, nullable=False)
    unit_price  = db.Column(db.Numeric(10, 2), nullable=False)

    @property
    def subtotal(self):
        return self.quantity * float(self.unit_price)

    def __repr__(self):
        return f'<SaleItem sale={self.sale_id} med={self.medicine_id}>'
