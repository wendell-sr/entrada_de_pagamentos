from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from database import Database

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.start_date = TextInput(hint_text="Data Inicial (DD/MM/AAAA)", multiline=False)
        self.end_date = TextInput(hint_text="Data Final (DD/MM/AAAA)", multiline=False)
        self.report_area = TextInput(readonly=True, size_hint=(1, 0.8))

        btn_generate = Button(text="Gerar Relatório", size_hint=(1, 0.2))
        btn_generate.bind(on_release=self.generate_report)

        layout.add_widget(self.start_date)
        layout.add_widget(self.end_date)
        layout.add_widget(btn_generate)
        layout.add_widget(self.report_area)

        self.add_widget(layout)

    def generate_report(self, instance):
        start = self.start_date.text
        end = self.end_date.text

        if not start or not end:
            self.report_area.text = "Insira as datas inicial e final!"
            return

        payments = self.db.get_all_payments()
        if not payments:
            self.report_area.text = "Nenhum pagamento encontrado no período."
            return

        report = f"Relatório de Pagamentos ({start} - {end}):\n\n"
        total = 0

        for payment in payments:
            report += f"Data: {payment[1]}, Valor: R${payment[2]:.2f}, Cliente: {payment[4]}, Método: {payment[5]}\n"
            total += payment[2]

        report += f"\nTotal: R${total:.2f}"
        self.report_area.text = report
