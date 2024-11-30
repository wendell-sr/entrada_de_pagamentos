import datetime
import sqlite3
from calendar import monthrange
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.metrics import dp

# Definir cores
CYAN = get_color_from_hex('#00BCD4')
BLACK = get_color_from_hex('#121212')
DARK_GRAY = get_color_from_hex('#1E1E1E')
WHITE = get_color_from_hex('#FFFFFF')

# Configurar tema da janela
Window.clearcolor = BLACK
Window.size = (400, 600)

# Classe Database
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('pagamentos.db')
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
    
    def add_payment(self, data, valor, descricao, cliente, metodo):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO pagamentos (data, valor, descricao, cliente, metodo)
            VALUES (?, ?, ?, ?, ?)
        ''', (data, valor, descricao, cliente, metodo))
        self.conn.commit()
    
    def get_all_payments(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM pagamentos ORDER BY data DESC')
        return cursor.fetchall()

    def get_payment(self, payment_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM pagamentos WHERE id=?', (payment_id,))
        return cursor.fetchone()

    def update_payment(self, payment_id, data, valor, descricao, cliente, metodo):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE pagamentos 
            SET data=?, valor=?, descricao=?, cliente=?, metodo=?
            WHERE id=?
        ''', (data, valor, descricao, cliente, metodo, payment_id))
        self.conn.commit()

    def delete_payment(self, payment_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM pagamentos WHERE id = ?', (payment_id,))
        self.conn.commit()

db = Database()

class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.datetime.now()
        self.setup_calendar()

    def setup_calendar(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        header_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        btn_prev = Button(
            text='<', 
            background_color=CYAN,
            size_hint=(0.2, 1)
        )
        btn_prev.bind(on_release=self.previous_month)
        
        self.month_label = Label(
            text=f'{self.current_date.strftime("%B %Y")}',
            size_hint=(0.6, 1),
            color=WHITE
        )
        
        btn_next = Button(
            text='>', 
            background_color=CYAN,
            size_hint=(0.2, 1)
        )
        btn_next.bind(on_release=self.next_month)
        
        header_layout.add_widget(btn_prev)
        header_layout.add_widget(self.month_label)
        header_layout.add_widget(btn_next)
        layout.add_widget(header_layout)

        calendar_layout = GridLayout(cols=7, spacing=2, size_hint=(1, 0.8))
        
        days = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
        for day in days:
            calendar_layout.add_widget(
                Label(text=day, color=CYAN)
            )

        first_day = datetime.date(self.current_date.year, self.current_date.month, 1)
        month_days = monthrange(self.current_date.year, self.current_date.month)[1]

        for _ in range(first_day.weekday()):
            calendar_layout.add_widget(Label(text=''))

        for day in range(1, month_days + 1):
            btn = Button(
                text=str(day),
                background_color=CYAN,
                color=BLACK
            )
            btn.bind(on_release=self.select_date)
            calendar_layout.add_widget(btn)

        layout.add_widget(calendar_layout)

        btn_report = Button(
            text='Ver Relatórios',
            size_hint=(1, 0.1),
            background_color=CYAN,
            color=BLACK
        )
        btn_report.bind(on_release=self.go_to_report)
        layout.add_widget(btn_report)

        self.clear_widgets()
        self.add_widget(layout)

    def previous_month(self, instance):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.setup_calendar()

    def next_month(self, instance):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.setup_calendar()

    def select_date(self, instance):
        selected_date = f"{instance.text}/{self.current_date.month}/{self.current_date.year}"
        self.manager.current = 'payment'
        self.manager.get_screen('payment').input_date.text = selected_date

    def go_to_report(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'report'

class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        main_layout.background_color = BLACK

        title = Label(
            text="Novo Pagamento",
            color=CYAN,
            size_hint=(1, 0.1),
            font_size='20sp'
        )

        form_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint=(1, 0.8)
        )

        self.input_date = TextInput(
            hint_text="Data",
            readonly=True,
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height='40dp'
        )

        self.input_client = TextInput(
            hint_text="Cliente",
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height='40dp'
        )

        self.input_value = TextInput(
            hint_text="Valor",
            input_filter='float',
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height='40dp'
        )

        self.input_description = TextInput(
            hint_text="Descrição",
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height='40dp'
        )

        self.payment_method = Spinner(
            text='Selecione o método',
            values=['Dinheiro', 'PIX', 'Cartão', 'PENDENTE'],
            background_color=CYAN,
            color=BLACK,
            size_hint=(1, None),
            height='40dp'
        )

        btn_layout = BoxLayout(
            size_hint=(1, 0.1),
            spacing=10
        )
        
        btn_back = Button(
            text="Voltar",
            background_color=CYAN,
            color=BLACK,
            size_hint=(0.5, None),
            height='40dp'
        )
        btn_back.bind(on_release=self.go_back)
        
        btn_add = Button(
            text="Adicionar",
            background_color=CYAN,
            color=BLACK,
            size_hint=(0.5, None),
            height='40dp'
        )
        btn_add.bind(on_release=self.add_payment)

        form_layout.add_widget(self.input_date)
        form_layout.add_widget(self.input_client)
        form_layout.add_widget(self.input_value)
        form_layout.add_widget(self.input_description)
        form_layout.add_widget(self.payment_method)
        
        btn_layout.add_widget(btn_back)
        btn_layout.add_widget(btn_add)

        main_layout.add_widget(title)
        main_layout.add_widget(form_layout)
        main_layout.add_widget(btn_layout)

        self.add_widget(main_layout)

    def add_payment(self, instance):
        data = self.input_date.text
        valor_text = self.input_value.text
        descricao = self.input_description.text
        cliente = self.input_client.text
        metodo = self.payment_method.text

        if metodo == 'Selecione o método':
            popup = Popup(
                title='Erro',
                content=Label(text='Selecione um método de pagamento'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            return

        if not all([data, valor_text, descricao, cliente, metodo]):
            popup = Popup(
                title='Erro',
                content=Label(text='Todos os campos são obrigatórios'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            return

        try:
            valor = float(valor_text)
            db.add_payment(data, valor, descricao, cliente, metodo)
            self.input_value.text = ""
            self.input_description.text = ""
            self.input_client.text = ""
            self.payment_method.text = 'Selecione o método'
            popup = Popup(
                title='Sucesso',
                content=Label(text='Pagamento adicionado com sucesso!'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
        except ValueError:
            popup = Popup(
                title='Erro',
                content=Label(text='Valor inválido'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

    def go_back(self, instance):
        self.manager.current = 'calendar'

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(
            text="Relatório de Pagamentos",
            color=CYAN,
            size_hint=(1, None),
            height=40
        )
        
        period_layout = BoxLayout(size_hint=(1, None), height=40, spacing=10)
        self.start_date = TextInput(
            hint_text="Data Inicial (DD/MM/AAAA)",
            background_color=DARK_GRAY,
            foreground_color=WHITE
        )
        self.end_date = TextInput(
            hint_text="Data Final (DD/MM/AAAA)",
            background_color=DARK_GRAY,
            foreground_color=WHITE
        )
        
        btn_layout = BoxLayout(size_hint=(1, None), height=40, spacing=10)
        btn_back = Button(
            text="Voltar",
            background_color=CYAN,
            color=BLACK
        )
        btn_back.bind(on_release=self.go_back)
        
        btn_generate = Button(
            text="Gerar Relatório",
            background_color=CYAN,
            color=BLACK
        )
        btn_generate.bind(on_release=self.generate_report)
        
        self.report_area = TextInput(
            readonly=True,
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            size_hint=(1, 1)
        )
        
        period_layout.add_widget(self.start_date)
        period_layout.add_widget(self.end_date)
        btn_layout.add_widget(btn_back)
        btn_layout.add_widget(btn_generate)
        
        layout.add_widget(title)
        layout.add_widget(period_layout)
        layout.add_widget(btn_layout)
        layout.add_widget(self.report_area)
        
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'calendar'

    def generate_report(self, instance):
        start = self.start_date.text
        end = self.end_date.text
        
        if not start or not end:
            self.report_area.text = "Por favor, insira as datas inicial e final"
            return
        
        payments = db.get_all_payments()
        
        if not payments:
            self.report_area.text = "Nenhum pagamento encontrado no período"
            return
        
        report = f"Relatório de {start} até {end}\n\n"
        total = 0
        
        for payment in payments:
            _, data, valor, descricao, cliente, metodo = payment
            report += f"Data: {data}\n"
            report += f"Valor: R$ {valor:.2f}\n"
            report += f"Descrição: {descricao}\n"
            report += f"Cliente: {cliente}\n"
            report += f"Método: {metodo}\n"
            report += "-" * 30 + "\n"
            total += valor
        
        report += f"\nTotal: R$ {total:.2f}"
        self.report_area.text = report

class ListPaymentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_screen()

    def build_screen(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        title = Label(
            text="Pagamentos",
            color=CYAN,
            size_hint=(1, 0.1),
            font_size='20sp'
        )

        self.payments_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint=(1, 0.8)
        )
        self.load_payments()

        btn_layout = BoxLayout(
            size_hint=(1, 0.1),
            spacing=10
        )
        
        btn_back = Button(
            text="Voltar",
            background_color=CYAN,
            color=BLACK,
            size_hint=(1, None),
            height='40dp'
        )
        btn_back.bind(on_release=self.go_back)

        btn_layout.add_widget(btn_back)

        layout.add_widget(title)
        layout.add_widget(self.payments_layout)
        layout.add_widget(btn_layout)

        self.add_widget(layout)

    def load_payments(self):
        self.payments_layout.clear_widgets()
        payments = db.get_all_payments()

        for payment in payments:
            item = BoxLayout(
                orientation='horizontal',
                size_hint=(1, None),
                height='60dp',
                padding=5,
                spacing=5
            )
            
            info = f"{payment[1]} - {payment[4]}\nR$ {payment[2]:.2f}"
            label = Label(
                text=info,
                color=WHITE,
                size_hint=(0.7, 1),
                halign='left'
            )

            btn_edit = Button(
                text="Editar",
                background_color=CYAN,
                color=BLACK,
                size_hint=(0.15, 1)
            )
            btn_edit.bind(on_release=lambda x, id=payment[0]: self.edit_payment(id))

            btn_delete = Button(
                text="Excluir",
                background_color=get_color_from_hex('#FF5252'),
                color=WHITE,
                size_hint=(0.15, 1)
            )
            btn_delete.bind(on_release=lambda x, id=payment[0]: self.confirm_delete(id))

            item.add_widget(label)
            item.add_widget(btn_edit)
            item.add_widget(btn_delete)

            self.payments_layout.add_widget(item)

    def edit_payment(self, payment_id):
        self.manager.current = 'edit_payment'
        self.manager.get_screen('edit_payment').load_payment(payment_id)

    def confirm_delete(self, payment_id):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Confirmar exclusão?'))
        
        buttons = BoxLayout(size_hint=(1, 0.4), spacing=10)
        btn_yes = Button(text='Sim', background_color=get_color_from_hex('#FF5252'))
        btn_no = Button(text='Não', background_color=CYAN)

        buttons.add_widget(btn_no)
        buttons.add_widget(btn_yes)
        content.add_widget(buttons)

        popup = Popup(
            title='Confirmar',
            content=content,
            size_hint=(0.7, 0.3),
            background_color=DARK_GRAY
        )

        btn_yes.bind(on_release=lambda x: self.delete_payment(payment_id, popup))
        btn_no.bind(on_release=popup.dismiss)
        
        popup.open()

    def delete_payment(self, payment_id, popup):
        db.delete_payment(payment_id)
        popup.dismiss()
        self.load_payments()

    def go_back(self, instance):
        self.manager.current = 'calendar'

class EditPaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_id = None
        self.build_screen()

    def build_screen(self):
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        main_layout.background_color = BLACK

        title = Label(
            text="Editar Pagamento",
            color=CYAN,
            size_hint=(1, 0.1),
            font_size='20sp'
        )

        form_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint=(1, 0.8)
        )

        self.input_date = TextInput(
            hint_text="Data",
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height='40dp'
        )

        self.input_client = TextInput(
            hint_text="Cliente",
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height='40dp'
        )

        self.input_value = TextInput(
            hint_text="Valor",
            input_filter='float',
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height='40dp'
        )

        self.input_description = TextInput(
            hint_text="Descrição",
            background_color=DARK_GRAY,
            foreground_color=WHITE,
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height='40dp'
        )

        self.payment_method = Spinner(
            text='Selecione o método',
            values=['Dinheiro', 'PIX', 'Cartão', 'PENDENTE'],
            background_color=CYAN,
            color=BLACK,
            size_hint=(1, None),
            height='40dp'
        )

        btn_layout = BoxLayout(
            size_hint=(1, 0.1),
            spacing=10
        )
        
        btn_cancel = Button(
            text="Cancelar",
            background_color=get_color_from_hex('#FF5252'),
            color=WHITE,
            size_hint=(0.5, None),
            height='40dp'
        )
        btn_cancel.bind(on_release=self.go_back)
        
        btn_save = Button(
            text="Salvar",
            background_color=CYAN,
            color=BLACK,
            size_hint=(0.5, None),
            height='40dp'
        )
        btn_save.bind(on_release=self.save_payment)

        form_layout.add_widget(self.input_date)
        form_layout.add_widget(self.input_client)
        form_layout.add_widget(self.input_value)
        form_layout.add_widget(self.input_description)
        form_layout.add_widget(self.payment_method)
        
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_save)

        main_layout.add_widget(title)
        main_layout.add_widget(form_layout)
        main_layout.add_widget(btn_layout)

        self.add_widget(main_layout)

    def load_payment(self, payment_id):
        self.payment_id = payment_id
        payment = db.get_payment(payment_id)
        if payment:
            self.input_date.text = payment[1]
            self.input_value.text = str(payment[2])
            self.input_description.text = payment[3]
            self.input_client.text = payment[4]
            self.payment_method.text = payment[5]

    def save_payment(self, instance):
        data = self.input_date.text
        valor_text = self.input_value.text
        descricao = self.input_description.text
        cliente = self.input_client.text
        metodo = self.payment_method.text

        if metodo == 'Selecione o método':
            popup = Popup(
                title='Erro',
                content=Label(text='Selecione um método de pagamento'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            return

        if not all([data, valor_text, descricao, cliente, metodo]):
            popup = Popup(
                title='Erro',
                content=Label(text='Todos os campos são obrigatórios'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            return

        try:
            valor = float(valor_text)
            db.update_payment(self.payment_id, data, valor, descricao, cliente, metodo)
            popup = Popup(
                title='Sucesso',
                content=Label(text='Pagamento atualizado com sucesso!'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
        except ValueError:
            popup = Popup(
                title='Erro',
                content=Label(text='Valor inválido'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

    def go_back(self, instance):
        self.manager.current = 'list_payments'

class PaymentApp(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(PaymentScreen(name='payment'))
        sm.add_widget(ReportScreen(name='report'))
        sm.add_widget(ListPaymentsScreen(name='list_payments'))
        sm.add_widget(EditPaymentScreen(name='edit_payment'))
        return sm

if __name__ == '__main__':
    PaymentApp().run()
