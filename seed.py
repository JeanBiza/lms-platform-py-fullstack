from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    existing = User.query.filter_by(role="admin").first()
    if not existing:
        admin = User(name="Admin", email="admin", role="admin", department="admin")
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()
        print("Default admin created.")
    else:
        print("Admin already exists, skipping.")