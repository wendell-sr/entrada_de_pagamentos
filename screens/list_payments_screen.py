from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from database import Database

class ListPaymentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.payments_layout = GridLayout(cols=1, size_hint=(1, 0.8))

        btn_reload = Button(text="Atualizar", size_hint=(1, 0.2))
        btn_reload.bind(on_release=self.load_payments)

        layout.add_widget(self.payments_layout)
        layout.add_widget(btn_reload)
        self.add_widget(layout)

    def load_payments(self, instance=None):
        self.payments_layout.clear_widgets()
        payments = self.db.get_all_payments()

        for payment in payments:
            label = Label(text=f"{payment[1]}: {payment[4]} - R$ {payment[2]:.2f}")
            self.payments_layout.add_widget(label)
