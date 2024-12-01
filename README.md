# Entrada de Pagamentos

Um aplicativo de gerenciamento de pagamentos simples e eficiente, desenvolvido com **Kivy**. Ele permite registrar, listar, editar e excluir pagamentos, além de exibir relatórios detalhados e utilizar um calendário interativo para organizar suas finanças.

---

## Funcionalidades

- **Registro de Pagamentos**: Adicione pagamentos com informações como valor, descrição, data e método de pagamento.
- **Listagem de Pagamentos**: Visualize todos os pagamentos cadastrados, com suporte a rolagem para listas extensas.
- **Edição e Exclusão**: Edite ou exclua pagamentos diretamente da lista de registros.
- **Relatórios**: Geração de relatórios detalhados com valores totais, pendentes e recebidos.
- **Calendário Interativo**: Navegue entre meses e selecione datas para visualizar ou adicionar pagamentos.
- **Modo Escuro**: Interface visual moderna e confortável, com um tema escuro e detalhes em azul ciano.

---

## Pré-requisitos

- **Python 3.8+**
- **Dependências do Projeto**:
  - `kivy`
  - `pillow`
  - `sqlite3`

---

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/wendell-sr/entrada_de_pagamentos.git
   cd entrada_de_pagamentos

2. Crie e ative um ambiente virtual:

   ```
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

   

   ## Uso

   1. Execute o aplicativo:

      ```
      python main.py
      ```

   2. Interaja com a interface:

      - Navegue pelo calendário.
      - Adicione, edite e exclua pagamentos.
      - Gere relatórios financeiros.

   ------

   ## Estrutura do Projeto

   - **`main.py`**: Ponto de entrada do aplicativo.
   - **`calendar_screen.py`**: Gerencia a interface e a lógica do calendário.
   - **`list_payments_screen.py`**: Exibe a lista de pagamentos e permite edição ou exclusão.
   - **`payment_screen.py`**: Tela para adicionar novos pagamentos.
   - **`report_screen.py`**: Tela de relatórios financeiros detalhados.
   - **`database.py`**: Gerencia a interação com o banco de dados SQLite.

   ------

   ## Contribuição

   Contribuições são bem-vindas! Siga os passos abaixo para colaborar:

   1. Crie um fork do repositório.

   2. Faça suas alterações em uma branch separada:

      ```
      git checkout -b minha-branch
      ```

   3. Envie um pull request explicando suas mudanças.

   

