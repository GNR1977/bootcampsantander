# Sistema para Controle Bancário — Orientado a Objetos (UML/DIO)
# Versão 01 — Giuliano Nascimento Ribeiro
# Data de Entrega: 18/08/2025

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


# ========================= MODELO DE DOMÍNIO ========================= #

class Historico:
    """Armazena as transações de uma conta."""

    def __init__(self) -> None:
        self._transacoes: List[dict] = []

    def adicionar(self, tipo: str, valor: float) -> None:
        self._transacoes.append(
            {
                "tipo": tipo,
                "valor": float(valor),
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    @property
    def transacoes(self) -> List[dict]:
        return self._transacoes

    def contar_saques(self) -> int:
        return sum(1 for t in self._transacoes if t["tipo"] == "Saque")


class Conta:
    """Classe base para conta bancária."""

    _sequencial = 1  # simples gerador de número de conta

    def __init__(self, cliente: "Cliente", numero: int | None = None, agencia: str = "0001") -> None:
        self.agencia = agencia
        self.numero = numero or Conta._sequencial
        Conta._sequencial = max(Conta._sequencial, self.numero + 1)

        self._saldo: float = 0.0
        self.cliente = cliente
        self.historico = Historico()

    # Operações básicas
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print(f"Falha: valor de depósito inválido (R$ {valor:.2f}).")
            return False
        self._saldo += valor
        self.historico.adicionar("Depósito", valor)
        print(f"Depósito realizado com sucesso! R$ {valor:.2f}")
        return True

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print(f"Falha: valor de saque inválido (R$ {valor:.2f}).")
            return False
        if valor > self._saldo:
            print(f"Falha: saldo insuficiente. Saldo atual R$ {self._saldo:.2f}")
            return False
        self._saldo -= valor
        self.historico.adicionar("Saque", valor)
        print(f"Saque realizado com sucesso! R$ {valor:.2f}")
        return True

    @property
    def saldo(self) -> float:
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente: "Cliente") -> "Conta":
        return cls(cliente)


class ContaCorrente(Conta):
    """Conta Corrente com limite por saque e limite de quantidade de saques."""

    def __init__(self, cliente: "Cliente", numero: int | None = None, agencia: str = "0001", *, limite: float = 500.0, limite_saques: int = 3) -> None:
        super().__init__(cliente, numero, agencia)
        self.limite = float(limite)
        self.limite_saques = int(limite_saques)

    def sacar(self, valor: float) -> bool:
        if valor > self.limite:
            print(
                f"Falha: valor solicitado acima do limite por saque (R$ {self.limite:.2f})."
            )
            return False
        if self.historico.contar_saques() >= self.limite_saques:
            print(
                f"Falha: limite diário de saques atingido (máx {self.limite_saques})."
            )
            return False
        return super().sacar(valor)


class Transacao(ABC):
    """Interface para transações (UML: classe abstrata)."""

    @property
    @abstractmethod
    def valor(self) -> float:  # pragma: no cover - interface
        ...

    @abstractmethod
    def registrar(self, conta: Conta) -> bool:  # pragma: no cover - interface
        ...


@dataclass
class Deposito(Transacao):
    _valor: float

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> bool:
        return conta.depositar(self.valor)


@dataclass
class Saque(Transacao):
    _valor: float

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> bool:
        return conta.sacar(self.valor)


@dataclass
class Cliente:
    nome: str
    endereco: str
    contas: List[Conta] = field(default_factory=list)

    def adicionar_conta(self, conta: Conta) -> None:
        self.contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> bool:
        if conta not in self.contas:
            print("Falha: conta não pertence ao cliente.")
            return False
        return transacao.registrar(conta)


@dataclass
class PessoaFisica(Cliente):
    cpf: str = ""


# ========================= INTERFACE DE TERMINAL ========================= #

MENU = """
    ============= Opções Caixa Eletrônico =============

    1 - Depositar
    2 - Sacar
    3 - Extrato
    4 - Sair

    ===================================================

                Bem-vindo ao Banco GNR!!!!

    => """


def imprimir_extrato(conta: Conta) -> None:
    print("\n========= Extrato Bancário - Banco GNR =========")
    if not conta.historico.transacoes:
        print("Não houve movimentações bancárias.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['tipo']}: R$ {t['valor']:.2f} — {t['data']}")
    print(f"\nSaldo Atual: R$ {conta.saldo:.2f}")
    print("==============================================\n")


# ========================= APLICAÇÃO (loop principal) ========================= #

def main() -> None:
    # Exemplo simples: cria um cliente e uma conta corrente.
    cliente = PessoaFisica(nome="Giuliano Nascimento Ribeiro", endereco="Curitiba - PR", cpf="000.000.000-00")
    conta = ContaCorrente.nova_conta(cliente)
    cliente.adicionar_conta(conta)

    while True:
        escolha = input(MENU)

        if escolha == "1":
            try:
                valor = float(input("Informe o valor para Depósito: "))
            except ValueError:
                print("Falha: informe um número válido.")
                continue
            cliente.realizar_transacao(conta, Deposito(valor))

        elif escolha == "2":
            try:
                valor = float(input("Informe o valor para Saque: "))
            except ValueError:
                print("Falha: informe um número válido.")
                continue
            cliente.realizar_transacao(conta, Saque(valor))

        elif escolha == "3":
            imprimir_extrato(conta)

        elif escolha == "4":
            print("Obrigado por utilizar o sistema do Banco GNR!")
            break
        else:
            print("Falha na operação, é necessário escolher uma opção válida.")


if __name__ == "__main__":
    main()
