from app import db

class PaymentSource(db.Model):
    __tablename__ = 'payment_sources'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"PaymentSource(id={self.id}, source_name='{self.source_name}')"
    
    @classmethod
    def insert_initial_data(cls):
        payment_sources_data = [
            'Banco do Brasil', 'Sicoob', 'Nubank', 'Inter', 'Carteira', 'Salario'
        ]
        for source_name in payment_sources_data:
            source = cls(source_name=source_name)
            db.session.add(source)
        db.session.commit()