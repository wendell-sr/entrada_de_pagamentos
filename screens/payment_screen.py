from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from database import Database

class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.input_date = TextInput(hint_text="Data (DD/MM/AAAA)", multiline=False)
        self.input_client = TextInput(hint_text="Cliente", multiline=False)
        self.input_value = TextInput(hint_text="Valor", input_filter="float", multiline=False)
        self.input_description = TextInput(hint_text="Descrição", multiline=False)

        self.payment_method = Spinner(
            text='Selecione o método',
            values=['Dinheiro', 'PIX', 'Cartão', 'PENDENTE']
        )

        btn_add = Button(text="Adicionar", size_hint=(1, 0.2))
        btn_add.bind(on_release=self.add_payment)

        layout.add_widget(self.input_date)
        layout.add_widget(self.input_client)
        layout.add_widget(self.input_value)
        layout.add_widget(self.input_description)
        layout.add_widget(self.payment_method)
        layout.add_widget(btn_add)

        self.add_widget(layout)

    def add_payment(self, instance):
        data = self.input_date.text
        cliente = self.input_client.text
        valor = self.input_value.text
        descricao = self.input_description.text
        metodo = self.payment_method.text

        if metodo == 'Selecione o método' or not all([data, cliente, valor, descricao]):
            popup = Popup(title='Erro', content=Label(text="Preencha todos os campos!"), size_hint=(0.6, 0.4))
            popup.open()
            return

        try:
            valor = float(valor)
            self.db.add_payment(data, valor, descricao, cliente, metodo)
            popup = Popup(title='Sucesso', content=Label(text="Pagamento adicionado com sucesso!"), size_hint=(0.6, 0.4))
            popup.open()

            self.input_date.text = ""
            self.input_client.text = ""
            self.input_value.text = ""
            self.input_description.text = ""
            self.payment_method.text = 'Selecione o método'
        except ValueError:
            popup = Popup(title='Erro', content=Label(text="Valor inválido!"), size_hint=(0.6, 0.4))
            popup.open()
