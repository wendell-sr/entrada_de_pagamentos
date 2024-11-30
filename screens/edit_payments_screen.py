from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from database import Database


class EditPaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.payment_id = None  # Armazena o ID do pagamento sendo editado
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        self.input_date = TextInput(hint_text="Data (DD/MM/AAAA)", multiline=False)
        self.input_client = TextInput(hint_text="Cliente", multiline=False)
        self.input_value = TextInput(hint_text="Valor", input_filter="float", multiline=False)
        self.input_description = TextInput(hint_text="Descrição", multiline=False)

        self.payment_method = Spinner(
            text="Selecione o método",
            values=["Dinheiro", "PIX", "Cartão", "PENDENTE"]
        )

        btn_save = Button(text="Salvar Alterações", size_hint=(1, 0.2))
        btn_save.bind(on_release=self.save_payment)

        btn_cancel = Button(text="Cancelar", size_hint=(1, 0.2))
        btn_cancel.bind(on_release=self.cancel_edit)

        layout.add_widget(self.input_date)
        layout.add_widget(self.input_client)
        layout.add_widget(self.input_value)
        layout.add_widget(self.input_description)
        layout.add_widget(self.payment_method)
        layout.add_widget(btn_save)
        layout.add_widget(btn_cancel)

        self.add_widget(layout)

    def load_payment(self, payment_id):
        """Carrega os dados de um pagamento para edição."""
        self.payment_id = payment_id
        payment = self.db.execute_query("SELECT * FROM pagamentos WHERE id=?", (payment_id,))
        if payment:
            payment = payment[0]  # Pega a primeira linha do resultado
            self.input_date.text = payment[1]  # Data
            self.input_value.text = str(payment[2])  # Valor
            self.input_description.text = payment[3]  # Descrição
            self.input_client.text = payment[4]  # Cliente
            self.payment_method.text = payment[5]  # Método

    def save_payment(self, instance):
        """Salva as alterações no pagamento."""
        if not self.payment_id:
            popup = Popup(
                title="Erro",
                content=Label(text="Nenhum pagamento selecionado para editar!"),
                size_hint=(0.6, 0.4)
            )
            popup.open()
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

            # Limpar os campos após salvar
            self.clear_fields()
            self.manager.current = "list_payments"  # Retornar à lista de pagamentos
        except ValueError:
            popup = Popup(
                title="Erro",
                content=Label(text="Valor inválido!"),
                size_hint=(0.6, 0.4)
            )
            popup.open()

    def cancel_edit(self, instance):
        """Cancela a edição e volta para a lista de pagamentos."""
        self.clear_fields()
        self.manager.current = "list_payments"

    def clear_fields(self):
        """Limpa os campos de entrada."""
        self.input_date.text = ""
        self.input_client.text = ""
        self.input_value.text = ""
        self.input_description.text = ""
        self.payment_method.text = "Selecione o método"
