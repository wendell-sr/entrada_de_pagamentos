from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from database import Database
from datetime import datetime

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()

    def apply_dark_theme(self, widget):
        from kivy.graphics import Color, Rectangle
        with widget.canvas.before:
            Color(0.07, 0.07, 0.07, 1)  # Fundo preto
            widget.bg_rect = Rectangle(size=widget.size, pos=widget.pos)
        widget.bind(size=lambda w, s: setattr(w.bg_rect, 'size', s))
        widget.bind(pos=lambda w, p: setattr(w.bg_rect, 'pos', p))

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.apply_dark_theme(layout)

        # Input de datas
        self.start_date = TextInput(
            hint_text="Data Inicial (DD/MM/AAAA)",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        self.end_date = TextInput(
            hint_text="Data Final (DD/MM/AAAA)",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )

        # Spinner para selecionar o método de pagamento
        self.payment_method_spinner = Spinner(
            text="Todos os Métodos",
            values=["Todos os Métodos", "Dinheiro", "PIX", "Cartão", "PENDENTE"],
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0, 0.8, 1, 1)
        )

        # Botão para gerar relatório
        btn_generate = Button(
            text="Gerar Relatório",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0, 0.8, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_generate.bind(on_release=self.generate_report)

        # ScrollView para exibição do relatório
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.report_area = TextInput(
            readonly=True,
            size_hint=(1, None),
            height=dp(200),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        scroll_view.add_widget(self.report_area)

        # Botão de voltar
        btn_back = Button(
            text="Voltar",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0, 0.8, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_release=self.go_back)

        # Adiciona os widgets ao layout
        layout.add_widget(self.start_date)
        layout.add_widget(self.end_date)
        layout.add_widget(self.payment_method_spinner)
        layout.add_widget(btn_generate)
        layout.add_widget(scroll_view)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def generate_report(self, instance):
        start = self.start_date.text
        end = self.end_date.text
        selected_method = self.payment_method_spinner.text

        if not start or not end:
            self.report_area.text = "Insira as datas inicial e final!"
            return

        try:
            start_date = datetime.strptime(start, "%d/%m/%Y")
            end_date = datetime.strptime(end, "%d/%m/%Y")

            if start_date > end_date:
                self.report_area.text = "A data inicial não pode ser maior que a data final!"
                return

            payments = self.db.get_all_payments()
            filtered_payments = []

            total = 0
            total_pending = 0

            for payment in payments:
                payment_date = datetime.strptime(payment[1], "%d/%m/%Y")
                if start_date <= payment_date <= end_date:
                    # Verifica o método de pagamento
                    if selected_method == "Todos os Métodos" or payment[5].lower() == selected_method.lower():
                        filtered_payments.append(payment)
                        total += payment[2]
                        if payment[5].lower() == "pendente":
                            total_pending += payment[2]

            if not filtered_payments:
                self.report_area.text = "Nenhum pagamento encontrado no período."
                return

            # Ordena os pagamentos em ordem crescente de data
            filtered_payments.sort(key=lambda p: datetime.strptime(p[1], "%d/%m/%Y"))

            total_received = total - total_pending

            report = f"Relatório de Pagamentos ({start} - {end}):\n\n"
            for payment in filtered_payments:
                report += f"Data: {payment[1]}, Valor: R${payment[2]:.2f}, Cliente: {payment[4]}, Método: {payment[5]}\n"

            report += f"\nTotal: R${total:.2f}"
            report += f"\nTotal Pendentes: R${total_pending:.2f}"
            report += f"\nTotal Recebido: R${total_received:.2f}"

            self.report_area.text = report

        except ValueError:
            self.report_area.text = "Formato de data inválido! Use DD/MM/AAAA."


    def go_back(self, instance):
        self.manager.current = 'calendar'
