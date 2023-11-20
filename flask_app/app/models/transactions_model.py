from app import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    value = db.Column(db.Float)
    description = db.Column(db.String(255))
    type = db.Column(db.Boolean)  # Flag indicando se é crédito 1 ou débito 0
    installments = db.Column(db.Integer)  # indica parcelamento
    planned = db.Column(db.Boolean)  # Flag indicando se foi planejado 1
    status = db.Column(db.Boolean)  # Indicando se foi realizado 1

    expense_category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.id'))
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    payment_source_id = db.Column(db.Integer, db.ForeignKey('payment_sources.id'))

    expense_category = db.relationship('ExpenseCategory', backref='transactions')
    payment_method = db.relationship('PaymentMethod', backref='transactions')
    payment_source = db.relationship('PaymentSource', backref='transactions')

    def __repr__(self):
        return f"Transaction(id={self.id}, date='{self.date}', value={self.value}, description='{self.description}')"
