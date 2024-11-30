from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.popup import Popup
from database import Database

class ListPaymentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()

    def apply_dark_theme(self, widget):
        from kivy.graphics import Color, Rectangle
        with widget.canvas.before:
            Color(0.07, 0.07, 0.07, 1)
            widget.bg_rect = Rectangle(size=widget.size, pos=widget.pos)
        widget.bind(size=lambda w, s: setattr(w.bg_rect, 'size', s))
        widget.bind(pos=lambda w, p: setattr(w.bg_rect, 'pos', p))

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.apply_dark_theme(layout)

        # ScrollView para os pagamentos
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.payments_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.payments_layout.bind(minimum_height=self.payments_layout.setter('height'))
        scroll_view.add_widget(self.payments_layout)

        btn_back = Button(
            text="Voltar", size_hint=(1, None), height=dp(50),
            background_color=(0, 0.8, 1, 1), color=(1, 1, 1, 1)
        )
        btn_back.bind(on_release=self.go_back)

        layout.add_widget(scroll_view)
        layout.add_widget(btn_back)
        self.add_widget(layout)
        self.load_payments()

    def load_payments(self):
        self.payments_layout.clear_widgets()
        payments = self.db.get_all_payments()

        for payment in payments:
            payment_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))

            payment_label = Label(
                text=f"{payment[1]} - {payment[4]}: R$ {payment[2]:.2f}",
                size_hint=(0.7, 1),
                halign="left",
                valign="middle",
                color=(1, 1, 1, 1)
            )

            edit_btn = Button(
                text="Editar", size_hint=(0.15, 1),
                background_color=(0, 0.8, 1, 1), color=(1, 1, 1, 1)
            )
            edit_btn.bind(on_release=lambda instance, p=payment: self.edit_payment(p))

            delete_btn = Button(
                text="Excluir", size_hint=(0.15, 1),
                background_color=(0.8, 0, 0, 1), color=(1, 1, 1, 1)
            )
            delete_btn.bind(on_release=lambda instance, p=payment: self.delete_payment(p))

            payment_box.add_widget(payment_label)
            payment_box.add_widget(edit_btn)
            payment_box.add_widget(delete_btn)
            self.payments_layout.add_widget(payment_box)

    def edit_payment(self, payment):
        self.manager.get_screen('edit_payment').load_payment(payment[0])
        self.manager.current = 'edit_payment'

    def delete_payment(self, payment):
        popup = Popup(
            title="Confirmação",
            content=Label(text=f"Excluir pagamento de {payment[4]}?"),
            size_hint=(0.6, 0.4)
        )
        yes_btn = Button(text="Sim", size_hint=(1, None), height=dp(50), background_color=(0, 0.8, 1, 1))
        no_btn = Button(text="Não", size_hint=(1, None), height=dp(50), background_color=(0.8, 0, 0, 1))

        btn_layout = BoxLayout(size_hint=(1, None), height=dp(50))
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)

        popup.content = BoxLayout(orientation='vertical', spacing=dp(10))
        popup.content.add_widget(Label(text=f"Confirmar exclusão de {payment[4]}?", color=(1, 1, 1, 1)))
        popup.content.add_widget(btn_layout)

        yes_btn.bind(on_release=lambda instance: self.confirm_delete(payment[0], popup))
        no_btn.bind(on_release=popup.dismiss)
        popup.open()

    def confirm_delete(self, payment_id, popup):
        self.db.delete_payment(payment_id)
        popup.dismiss()
        self.load_payments()

    def go_back(self, instance):
        self.manager.current = 'calendar'
