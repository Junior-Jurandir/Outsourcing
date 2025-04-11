# Importando as bibliotecas necessárias para o funcionamento do sistema
import sqlite3
import os
from Outsourcing import chamados
from Outsourcing import impressoras
from Outsourcing import bilhetagem

# Definindo e instanciando a conexão com o banco de dados
con = sqlite3.connect("./db/Outsourcing.db")
cur = con.cursor()
cur.row_factory = sqlite3.Row

# Definindo os paths dos arquivos CSV que serão utilizados

path_glpi = "./planilhas/glpi.csv"
path_impressora = "./planilhas/impressoras.csv"
path_bilhetagem = "./planilhas/bilhetagem.csv"


def limpar_terminal():
    """Limpa o terminal, dependendo do sistema operacional."""

    os.system("cls" if os.name == "nt" else "clear")


def menu():
    """Exibe o menu principal e gerência a navegação entre as opções."""

    print("Menu:")
    print("1 - Impressoras")
    print("2 - Chamados")
    print("3 - Bilhetagem")
    print("4 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        menu_impressoras()
    elif opcao == "2":
        menu_chamados()
    elif opcao == "3":
        menu_bilhetagem()
    else:
        print("Saindo...")
        limpar_terminal()


def menu_impressoras():
    """Exibe o menu de impressoras e gerência as opções disponíveis."""

    print("Menu Impressoras:")
    print("1 - Pesquisar impressoras por nº de série")
    print("2 - Pesquisar impressoras por localização")
    print("3 - Pesquisar impressoras por tipo")
    print("4 - Voltar ao menu principal")
    print("5 - Limpar terminal")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print("Pesquisando impressoras por nº de série...")
        pesquisar_impresoras_por_serie()
    elif opcao == "2":
        print("Pesquisando impressoras por localização...")
        pesquisar_impresoras_por_localizacao()
    elif opcao == "3":
        print("Pesquisando impressoras por tipo...")
        pesquisar_impresoras_por_tipo()
    elif opcao == "4":
        menu()
    else:
        limpar_terminal()


def menu_chamados():
    """Exibe o menu de chamados e gerência as opções disponíveis."""

    print("Menu Chamados:")
    print("1 - Pesquisar chamados por nº de chamado")
    print("2 - Pesquisar chamados por status")
    print("3 - Pesquisar chamado por impressora")
    print("4 - Voltar ao menu principal")
    print("5 - Limpar terminal")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print("Pesquisando chamados por nº de chamado...")
        pesquisar_chamado_por_id()
    elif opcao == "2":
        print("Pesquisando chamados por status...")
        pesquisar_chamados_por_status()
    elif opcao == "3":
        print("Pesquisando chamados por impressora...")
        pesquisar_chamados_por_impressora()
    elif opcao == "4":
        menu()
    else:
        limpar_terminal()


def menu_bilhetagem():
    """Exibe o menu de bilhetagem e gerência as opções disponíveis."""

    print("Menu Bilhetagem:")
    print("1 - Pesquisar bilhetagem por nº de série, ano e mês")
    print("2 - Voltar ao menu principal")

    if input("Escolha uma opção: ") == "1":
        print("Pesquisando bilhetagem por nº de série, ano e mês...")
        pesquisar_bilhetagem_por_serie_ano_mes()
    elif input("Escolha uma opção: ") == "2":
        menu()
    else:
        limpar_terminal()


def pesquisar_impresoras_por_serie():
    """Pesquisa impressoras pelo número de série fornecido pelo usuário."""

    serie = input("Insira o nº de serie da impressora: ")
    kwargs = {"serie": serie}
    resultado = impressoras.listar_impressoras(cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


def pesquisar_impresoras_por_localizacao():
    """Pesquisa impressoras pela localização fornecida pelo usuário."""

    localizacao = input("Insira a localização da impressora: ")
    kwargs = {"localizacao": localizacao}
    resultado = impressoras.listar_impressoras(cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


def pesquisar_impresoras_por_tipo():
    """Pesquisa impressoras pelo tipo fornecido pelo usuário."""

    tipo = input("Insira o tipo da impressora: ")
    kwargs = {"tipo": tipo}
    resultado = impressoras.listar_impressoras(cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


def pesquisar_chamado_por_id():
    """Pesquisa chamados pelo ID fornecido pelo usuário."""

    id = input("Insira o ID do chamado: ")
    kwargs = {"id": id}
    resultado = chamados.listar_chamados(cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


def pesquisar_chamados_por_titulo():
    """Pesquisa chamados pelo título fornecido pelo usuário."""

    titulo = input("Insira o título do chamado: ")
    kwargs = {"titulo": titulo}
    resultado = chamados.listar_chamados(cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


def pesquisar_chamados_por_status():
    """Pesquisa chamados pelo status fornecido pelo usuário."""

    status = input("Insira o status do chamado: ")
    kwargs = {"status": status}
    resultado = chamados.listar_chamados(cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


def pesquisar_chamados_por_requerente():
    requerente = input("Insira o nome do requerente do chamado: ")
    kwargs = {"requerente": requerente}
    resultado = chamados.listar_chamados(cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


def pesquisar_chamados_por_impressora():
    """Pesquisa chamados pela impressora associada, usando o número de série."""

    serie = input("Insira o nº de serie da impressora do chamado: ")
    kwargs = {"serie": serie}
    resultado = chamados.listar_chamados(cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


def pesquisar_bilhetagem_por_serie_ano_mes():
    """Pesquisa bilhetagem pelo número de série, ano e mês fornecidos pelo usuário."""

    serie = input("Insira o nº de serie da bilhetagem: ")
    ano = input("Insira o ano da bilhetagem: ")
    mes = input("Insira o mês da bilhetagem: ")
    kwargs = {"serie": serie, "ano": ano, "mes": mes}
    resultado = bilhetagem.listar_bilhetagem_serie_ano_mes(con, cur, **kwargs)

    for row in resultado:
        print(dict(row))

    menu()


# Criando tabelas no banco de dados Outsourcing.db
# try:
#    chamados.criar_tabela_chamados(con, cur)
#    impressoras.criar_tabela_impressoras(con, cur)
#    bilhetagem.criar_tabela_bilhetagem(con, cur)
# except Exception as exc:
#    print(f"Ops! ocorreu um erro ao criar as tabelas: {exc}")


# Importando dados e transformando em tabelas no banco de dados Outsourcing.db

try:
    chamados.importar_chamados(con, path_glpi)
    impressoras.importar_impressoras(con, path_impressora)
    bilhetagem.importar_bilhetagem(con, path_bilhetagem)
    chamados.adicionar_coluna(cur, con)
    chamados.atualizar_chamados(cur, con)
    chamados.criar_nova_tabela(cur, con)

except Exception as exc:
    print(f"Ops! ocorreu um erro ao importar os dados: {exc}")


menu()
