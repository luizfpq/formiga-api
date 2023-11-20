from app import db

class PaymentMethod(db.Model):
    __tablename__ = 'payment_method'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    method_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"PaymentMethod(id={self.id}, method_name='{self.method_name}')"
