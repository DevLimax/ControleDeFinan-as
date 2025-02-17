from models import *
from views import *

class UI:
    def start(self):
        while(True):
            print('''
            [1] -> Criar conta
            [2] -> Desativar conta
            [3] -> Transferir dinheiro
            [4] -> Movimentar dinheiro
            [5] -> Total contas
            [6] -> Filtrar histórico
            [7] -> Gráfico
                  ''')
            
            choice = int(input("Escolha uma opção: "))

            if choice == 1:
                self._criar_conta()
            elif choice == 2:
                self._desativar_conta()
            elif choice == 3:
                self._transferir_saldo()
            elif choice == 4:
                self._movimentar_dinheiro()
            elif choice == 5:
                self._saldoTotal_contas()
            elif choice == 6:
                self._filtrar_movimentacoes()
            elif choice == 7:
                self._criar_grafico()
            else:
                break
            
    def _criar_conta(self):
        print("Digite o nome de um dos bancos listados abaixo:")
        for banco in Bancos:
            print(f"----{banco.value}----")

        banco = input(">:").title()
        valor = float(input("Digite o valor atual disponivel na conta:"))

        conta = Conta(saldo=valor,banco=Bancos(banco))
        criar_conta(conta)

    def _desativar_conta(self):
        print("Escolha a conta que deseja desativar:")
        for conta in listar_contas():
            if conta.saldo == 0.0 and conta.status == Status.ATIVO:
                print(f"{conta.id} -> {conta.banco.value} -> R${conta.saldo}")

            elif conta.status == Status.ATIVO:
                print(f"{conta.id} -> {conta.banco.value} -> R${conta.saldo}")
                
        
        choice_id = int(input(">:"))
        try:
            desativar_conta(choice_id)
            print("Conta desativada")
        except ValueError:
            print("Essa conta ainda possui saldo, faça uma transferência")


    def _transferir_saldo(self):
        print("Escolha a conta para retirar o dinheiro:")
        for conta in listar_contas():
            if conta.status == Status.ATIVO:
                print(f"{conta.id} -> {conta.banco.value} -> R${conta.saldo}")

        conta_retirar_id = int(input(">:"))

        print("Escolha a conta para enviar o dinheiro:")
        for conta in listar_contas():
            if conta.status == Status.ATIVO:
                print(f"{conta.id} -> {conta.banco.value} -> R${conta.saldo}")

        conta_enviar_id = int(input(">:"))

        valor = float(input("Digite o valor da transferência:"))

        transferir_saldo(id_conta_remetente=conta_retirar_id,id_conta_destinatario=conta_enviar_id,valor=valor)

    def _movimentar_dinheiro(self):
        print("Escolha a conta:")
        for conta in listar_contas():
            print(f"{conta.id} -> {conta.banco.value} -> R${conta.saldo}")

        choice_conta_id = int(input(">:"))

        valor = float(input("Digite o valor movimentado:"))

        print("Selecione o tipo de movimentação:")
        for tipo in Tipos:
            print(f"---{tipo.value}---")

        choice_tipo = input(">:").title()
        historico = Historico(conta_id=choice_conta_id,valor=valor,tipo=Tipos(choice_tipo))
        movimentar_dinheiro(historico=historico)

    def _saldoTotal_contas(self):
        print(f"R${saldo_total()}")

    def _filtrar_movimentacoes(self):
        from datetime import datetime
        print("Digite as datas no modelo (dd/mm/aaaa)")
        data_inicio = input("Digite a data de inicio:")
        data_fim = input("Digite a data de fim:")

        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
        data_fim = datetime.strptime(data_fim, '%d/%m/%Y').date()

        for historico in buscar_historico_por_datas(data_inicio=data_inicio,data_fim=data_fim):
            print(f"R${historico.valor} - {historico.tipo.value}")

    def _criar_grafico(self):
        criar_grafico_por_conta()


UI().start()





