from app import db

class ExpenseCategory(db.Model):
    __tablename__ = 'expense_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"ExpenseCategory(id={self.id}, category_name='{self.category_name}')"
    
    @classmethod
    def insert_initial_data(cls):
        expense_categories_data = [
            'Alimentação', 'Presentes', 'Saúde', 'Moradia', 'Transporte', 'Cuidados Pessoais',
            'Animais de estimação', 'Serviços de utilidade pública', 'Estudos', 'Recreação',
            'Master Nubank', 'Master Sicoob', 'Visa BB', 'Outros', 'Custos Bancários',
            'Celular', 'Telefonia e Internet', 'Descontos', 'Poupança', 'Investimento',
            'Assinatura', 'Empréstimo'
        ]
        for category_name in expense_categories_data:
            category = cls(category_name=category_name)
            db.session.add(category)
        db.session.commit()