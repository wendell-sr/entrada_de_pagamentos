from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from datetime import datetime
from calendar import monthrange
import locale
from datetime import datetime
from calendar import monthrange


locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now()  # Define o mês atual ao iniciar o calendário
        self.setup_ui()

    def apply_dark_theme(self, widget):
        from kivy.graphics import Color, Rectangle
        with widget.canvas.before:
            Color(0.07, 0.07, 0.07, 1)  # Fundo preto
            widget.bg_rect = Rectangle(size=widget.size, pos=widget.pos)
        widget.bind(size=lambda w, s: setattr(w.bg_rect, 'size', s))
        widget.bind(pos=lambda w, p: setattr(w.bg_rect, 'pos', p))

    def setup_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        self.apply_dark_theme(self.layout)
        self.add_widget(self.layout)
        self.setup_calendar()

    def setup_calendar(self):
        self.layout.clear_widgets()

        # Cabeçalho
        header = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        prev_btn = Button(
            text="<<", size_hint=(0.2, 1),
            background_color=(0, 0.8, 1, 1), color=(1, 1, 1, 1)
        )
        next_btn = Button(
            text=">>", size_hint=(0.2, 1),
            background_color=(0, 0.8, 1, 1), color=(1, 1, 1, 1)
        )
        month_label = Label(
            text=self.current_date.strftime("%B %Y").capitalize(),  # Nome do mês em português
            size_hint=(0.6, 1),
            color=(1, 1, 1, 1)
        )


        prev_btn.bind(on_release=self.previous_month)
        next_btn.bind(on_release=self.next_month)

        header.add_widget(prev_btn)
        header.add_widget(month_label)
        header.add_widget(next_btn)

        # Corpo do calendário
        calendar = GridLayout(cols=7, spacing=dp(2), size_hint=(1, 0.8))
        days_of_week = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for day in days_of_week:
            calendar.add_widget(Label(text=day, color=(1, 1, 1, 1)))

        first_day = datetime(self.current_date.year, self.current_date.month, 1).weekday()
        days_in_month = monthrange(self.current_date.year, self.current_date.month)[1]

        blank_days = (first_day + 1) % 7
        for _ in range(blank_days):
            calendar.add_widget(Label(text="", color=(1, 1, 1, 1)))

        for day in range(1, days_in_month + 1):
            day_btn = Button(
                text=str(day), background_color=(0.1, 0.1, 0.1, 1),
                color=(0, 0.8, 1, 1), size_hint=(1, None), height=dp(50)
            )
            day_btn.bind(on_release=lambda instance, d=day: self.select_date(d))
            calendar.add_widget(day_btn)

        # Rodapé
        footer = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        report_btn = Button(
            text="Relatórios", size_hint=(0.5, 1),
            background_color=(0, 0.8, 1, 1), color=(1, 1, 1, 1)
        )
        report_btn.bind(on_release=self.go_to_report)

        list_btn = Button(
            text="Lista de Pagamentos", size_hint=(0.5, 1),
            background_color=(0, 0.8, 1, 1), color=(1, 1, 1, 1)
        )
        list_btn.bind(on_release=self.go_to_list)

        footer.add_widget(report_btn)
        footer.add_widget(list_btn)

        self.layout.add_widget(header)
        self.layout.add_widget(calendar)
        self.layout.add_widget(footer)

    def next_month(self, instance):
        if self.current_date.year == 2025 and self.current_date.month == 12:
            return  # Limite superior
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.setup_calendar()

    def previous_month(self, instance):
        if self.current_date.year == 2024 and self.current_date.month == 1:
            return  # Limite inferior
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.setup_calendar()

    def select_date(self, day):
        selected_date = f"{day}/{self.current_date.month}/{self.current_date.year}"
        self.manager.get_screen('payment').input_date.text = selected_date
        self.manager.current = 'payment'

    def go_to_report(self, instance):
        self.manager.current = 'report'

    def go_to_list(self, instance):
        self.manager.current = 'list_payments'
