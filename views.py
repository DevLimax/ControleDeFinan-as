from models import Conta,Bancos,Status,Historico,Tipos,engine
from sqlmodel import Session, select
from datetime import date,timedelta
import matplotlib
import matplotlib.pyplot as plt

def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco == conta.banco)
        results = session.exec(statement).all()

        if results:
            print("Já existe uma conta nesse banco!")
            return
        
        session.add(conta)
        session.commit()
        return conta
    
def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
        
        return results
        
def desativar_conta(id: int):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        conta = session.exec(statement).first()

        if conta.saldo > 0:
            raise ValueError("Essa conta possui saldo!")
        
        conta.status = Status.INATIVO
        session.commit()
        
def ativar_conta(id: int):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        conta = session.exec(statement).first()

        if conta.status == Status.ATIVO:
            raise("Essa conta ja está ativa!")

        conta.status = Status.ATIVO
        session.commit()

def transferir_saldo(valor: float,id_conta_remetente: int,id_conta_destinatario: int):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id_conta_remetente)
        conta_remetente = session.exec(statement).first()
        if conta_remetente.saldo < valor:
            raise ValueError("Saldo insuficiente!")
        
        statement = select(Conta).where(Conta.id == id_conta_destinatario)
        conta_destinatario = session.exec(statement).first()
        if conta_destinatario.status == Status.INATIVO:
            raise InterruptedError(f"A conta do {conta_destinatario.banco.value} está inativa!")

        conta_remetente.saldo -= valor
        conta_destinatario.saldo += valor
        session.commit()

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == historico.conta_id)
        conta = session.exec(statement).first()

        if conta.status == Status.INATIVO:
            raise InterruptedError("Essa conta não está ativa!")
        
        if historico.tipo == Tipos.ENTRADA:
            conta.saldo += historico.valor
        else:
            if conta.saldo < historico.valor:
                raise ValueError("Saldo Insuficiente!")
            
            conta.saldo -= historico.valor

        session.add(historico)
        session.commit()
        return historico
    
def saldo_total():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
    
    total = 0
    for conta in contas:
        total += conta.saldo

    return float(total)

def buscar_historico_por_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        results = session.exec(statement).all()
        return results
    
def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status == Status.ATIVO)
        contas = session.exec(statement).all()
        bancos = [conta.banco.value for conta in contas]
        saldos = [conta.saldo for conta in contas]
        plt.bar(bancos, saldos)
        plt.show()




