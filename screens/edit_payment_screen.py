from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.metrics import dp
from database import Database

class EditPaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.payment_id = None
        self.setup_ui()

    def apply_dark_theme(self, widget):
        from kivy.graphics import Color, Rectangle
        with widget.canvas.before:
            Color(0.07, 0.07, 0.07, 1)  # Fundo preto
            widget.bg_rect = Rectangle(size=widget.size, pos=widget.pos)
        widget.bind(size=lambda w, s: setattr(w.bg_rect, 'size', s))
        widget.bind(pos=lambda w, p: setattr(w.bg_rect, 'pos', p))

    def setup_ui(self):
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15))
        self.apply_dark_theme(layout)

        self.input_date = TextInput(
            hint_text="Data (DD/MM/AAAA)",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        self.input_client = TextInput(
            hint_text="Cliente",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        self.input_value = TextInput(
            hint_text="Valor",
            input_filter="float",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        self.input_description = TextInput(
            hint_text="Descrição",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )

        self.payment_method = Spinner(
            text="Selecione o método",
            values=["Dinheiro", "PIX", "Cartão", "PENDENTE"],
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0, 0.8, 1, 1)
        )

        button_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        btn_save = Button(
            text="Salvar",
            size_hint=(0.5, 1),
            background_color=(0, 0.8, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_save.bind(on_release=self.save_payment)

        btn_cancel = Button(
            text="Cancelar",
            size_hint=(0.5, 1),
            background_color=(0.8, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        btn_cancel.bind(on_release=self.cancel_edit)

        button_layout.add_widget(btn_save)
        button_layout.add_widget(btn_cancel)

        layout.add_widget(self.input_date)
        layout.add_widget(self.input_client)
        layout.add_widget(self.input_value)
        layout.add_widget(self.input_description)
        layout.add_widget(self.payment_method)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def load_payment(self, payment_id):
        self.payment_id = payment_id
        payment = self.db.execute_query("SELECT * FROM pagamentos WHERE id=?", (payment_id,))
        if payment:
            payment = payment[0]
            self.input_date.text = payment[1]
            self.input_value.text = str(payment[2])
            self.input_description.text = payment[3]
            self.input_client.text = payment[4]
            self.payment_method.text = payment[5]

    def save_payment(self, instance):
        if not self.payment_id:
            return

        data = self.input_date.text
        cliente = self.input_client.text
        valor_text = self.input_value.text
        descricao = self.input_description.text
        metodo = self.payment_method.text

        if metodo == "Selecione o método" or not all([data, cliente, valor_text, descricao]):
            popup = Popup(
                title="Erro",
                content=Label(text="Todos os campos são obrigatórios!"),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            return

        try:
            valor = float(valor_text)
            self.db.execute_query(
                """
                UPDATE pagamentos 
                SET data=?, valor=?, descricao=?, cliente=?, metodo=? 
                WHERE id=?
                """,
                (data, valor, descricao, cliente, metodo, self.payment_id)
            )
            popup = Popup(
                title="Sucesso",
                content=Label(text="Pagamento atualizado com sucesso!"),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            self.cancel_edit(None)
        except ValueError:
            popup = Popup(
                title="Erro",
                content=Label(text="Valor inválido!"),
                size_hint=(0.6, 0.4)
            )
            popup.open()

    def cancel_edit(self, instance):
        self.manager.current = 'list_payments'
