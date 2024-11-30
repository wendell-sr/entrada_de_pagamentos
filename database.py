import sqlite3

class Database:
    def __init__(self, db_name='pagamentos.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                valor REAL NOT NULL,
                descricao TEXT NOT NULL,
                cliente TEXT NOT NULL,
                metodo TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def execute_query(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
            return None

    def add_payment(self, data, valor, descricao, cliente, metodo):
        self.execute_query('''
            INSERT INTO pagamentos (data, valor, descricao, cliente, metodo)
            VALUES (?, ?, ?, ?, ?)
        ''', (data, valor, descricao, cliente, metodo))

    def get_all_payments(self):
        return self.execute_query('SELECT * FROM pagamentos ORDER BY data DESC')

    def delete_payment(self, payment_id):
        self.execute_query('DELETE FROM pagamentos WHERE id = ?', (payment_id,))
