from datetime import datetime
import uuid


class Autenticacao:

    def __init__(self):
        self.__token: str = ""

    def validar_credenciais(self, cpf: str, senha: str) -> bool:
        credenciais_validas = {"123.456.789-00": "senha123"}
        return credenciais_validas.get(cpf) == senha

    def gerar_token(self) -> str:
        self.__token = str(uuid.uuid4())
        print(f"  [Autenticacao] Token gerado: {self.__token}")
        return self.__token

    def invalidar_sessao(self, token: str) -> None:
        if self.__token == token:
            self.__token = ""
            print("  [Autenticacao] Sessão invalidada / token revogado.")
        else:
            print("  [Autenticacao] Token não encontrado.")

    @property
    def token(self) -> str:
        return self.__token


class Agencia:

    def __init__(self, id_agencia: int, id_cliente: int, localidade: str):
        self.IdAgencia: int = id_agencia
        self.IDcliente: int = id_cliente
        self.Localidade: str = localidade

    def cadastra_usuario(self) -> str:
        msg = f"Usuário cadastrado na agência {self.IdAgencia} – {self.Localidade}"
        print(f"  [Agencia] {msg}")
        return msg


class Conta:

    def __init__(self, id_contas: int, id_cliente: int, id_agencia: int,
                 saldo_inicial: float = 0.0):
        self.__IDcontas: int = id_contas
        self.__IDcliente: int = id_cliente
        self.__IdAgencia: int = id_agencia
        self.__saldo: float = saldo_inicial

    @property
    def id_contas(self):
        return self.__IDcontas

    @property
    def saldo(self):
        return self.__saldo

    def verificar_saldo(self) -> str:
        msg = f"Saldo disponível: R$ {self.__saldo:.2f}"
        print(f"  [Conta] {msg}")
        return msg

    def consultar_investimento(self) -> str:
        msg = "Consulta de investimentos realizada."
        print(f"  [Conta] {msg}")
        return msg

    def debitar(self, valor: float) -> bool:
        if valor <= self.__saldo:
            self.__saldo -= valor
            print(f"  [Conta] Debitado R$ {valor:.2f}. Novo saldo: R$ {self.__saldo:.2f}")
            return True

        print("  [Conta] Saldo insuficiente para débito.")
        return False

    def saldo_suficiente(self, valor: float) -> bool:
        return self.__saldo >= valor


class Pagamento:

    def __init__(self, id_pagamento: int, valor: float):
        self.__IDpagamento: int = id_pagamento
        self.__Valor: float = valor
        self.__status: str = "pendente"

    @property
    def status(self):
        return self.__status

    @property
    def valor(self):
        return self.__Valor

    def verificar_saldo(self, conta: Conta) -> bool:
        suficiente = conta.saldo_suficiente(self.__Valor)
        print(f"  [Pagamento] Saldo suficiente: {suficiente}")
        return suficiente

    def realizar_pagamento(self, conta: Conta) -> bool:
        if self.verificar_saldo(conta):
            if conta.debitar(self.__Valor):
                self.__status = "concluido"
                print(f"  [Pagamento] Pagamento #{self.__IDpagamento} realizado com sucesso.")
                return True

        self.__status = "falhou"
        print(f"  [Pagamento] Pagamento #{self.__IDpagamento} falhou – saldo insuficiente.")
        return False

    def receber_pagamento(self, conta: Conta) -> bool:
        print("  [Pagamento] Recebimento registrado.")
        self.__status = "recebido"
        return True

    def ver_status(self) -> str:
        print(f"  [Pagamento] Status: {self.__status}")
        return self.__status


class Usuario:

    def __init__(self, id_cliente: int, id_agencia: int, nome: str,
                 cpf: str, data_nasc: datetime, local: str):
        self.__IDcliente: int = id_cliente
        self.__idAgencia: int = id_agencia
        self.__Nome: str = nome
        self.__cpf: str = cpf
        self.__dataNasc: datetime = data_nasc
        self.__Local: str = local
        self.__token_sessao: str = ""
        self.__autenticacao = Autenticacao()

    @property
    def nome(self):
        return self.__Nome

    @property
    def cpf(self):
        return self.__cpf

    def realizar_login(self, senha: str) -> bool:

        print("\n[ATIVIDADE] Realizando login...")
        print(f"  Usuário '{self.__Nome}' submetendo credenciais.")

        if self.__autenticacao.validar_credenciais(self.__cpf, senha):
            self.__token_sessao = self.__autenticacao.gerar_token()
            print("  Login bem-sucedido. Sessão ativa registrada.")
            return True

        print("  Credenciais inválidas. Exibindo mensagem de erro.")
        return False

    def consultar_saldo(self, conta: Conta) -> str:
        print("\n[ATIVIDADE] Consultando saldo...")
        return conta.verificar_saldo()

    def realizar_pagamento(self, conta: Conta, valor: float,
                           id_pagamento: int = 1) -> str:

        print("\n[ATIVIDADE] Realizando pagamento...")

        pagamento = Pagamento(id_pagamento, valor)
        sucesso = pagamento.realizar_pagamento(conta)

        if sucesso:
            comprovante = (
                f"COMPROVANTE #{id_pagamento} | "
                f"Valor: R$ {valor:.2f} | "
                f"Status: {pagamento.ver_status()} | "
                f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )

            print(f"  Comprovante gerado: {comprovante}")
            return comprovante

        print("  Notificação de erro: saldo insuficiente.")
        return "ERRO: Saldo insuficiente."

    def realizar_investimento(self, conta: Conta) -> str:
        print("\n[ATIVIDADE] Realizando investimento...")
        resultado = conta.consultar_investimento()
        print(f"  Investimento registrado para '{self.__Nome}'.")
        return resultado

    def log_out(self) -> None:

        print("\n[ATIVIDADE] Realizando logout...")
        self.__autenticacao.invalidar_sessao(self.__token_sessao)
        self.__token_sessao = ""
        print("  Sessão encerrada com sucesso.")


if __name__ == "__main__":

    print("=" * 55)
    print("   SISTEMA BANCÁRIO SANTANDER – Demonstração")
    print("=" * 55)

    agencia = Agencia(
        id_agencia=1,
        id_cliente=42,
        localidade="São Paulo"
    )

    agencia.cadastra_usuario()

    conta = Conta(
        id_contas=1001,
        id_cliente=42,
        id_agencia=1,
        saldo_inicial=1500.00
    )

    usuario = Usuario(
        id_cliente=42,
        id_agencia=1,
        nome="Ezequiel Cruz",
        cpf="123.456.789-00",
        data_nasc=datetime(1990, 6, 15),
        local="São Paulo"
    )

    print("\n>>> Tentativa de login com senha errada:")
    usuario.realizar_login("senhaErrada")

    print("\n>>> Login correto:")
    logado = usuario.realizar_login("senha123")

    if logado:

        usuario.consultar_saldo(conta)

        usuario.realizar_pagamento(
            conta,
            valor=200.00,
            id_pagamento=101
        )

        usuario.realizar_pagamento(
            conta,
            valor=5000.00,
            id_pagamento=102
        )

        usuario.realizar_investimento(conta)

        usuario.log_out()

    print("\n" + "=" * 55)
    print("   Fim da demonstração.")
    print("=" * 55)