"""
Run this once to create the admin user:
    python seed.py
"""
from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@pharma.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Admin user created: admin / admin123')
    else:
        print('ℹ️  Admin user already exists.')
