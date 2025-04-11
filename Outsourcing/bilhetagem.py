import pandas as pd


def criar_tabela_bilhetagem(con, cur):
    # Criar tabela
    try:
        cur.execute(
            "CREATE TABLE bilhetagem ( Id INTEGER PRIMARY KEY AUTOINCREMENT, Serie VARCHAR(100), Contrato VARCHAR(10), Localização VARCHAR(500), Tipo VARCHAR(10), Ano INTEGER, Mês INTEGER, Bilhetagem INTEGER, FOREIGN KEY (Serie) REFERENCES impressoras(Serie));"
        )
        con.commit()
        print("Tabela bilhetagem criada com sucesso")
    except Exception as exc:
        print(f"Ops! ocorreu um erro ao criar a tabela bilhetagem: {exc}")


def importar_bilhetagem(con, bilhetagem):
    """Importa dados de bilhetagem de um arquivo CSV para o banco de dados."""

    try:
        bilhetagem = pd.read_csv(bilhetagem)
        bilhetagem = bilhetagem[
            [
                "Serie",
                "Contrato",
                "Localização",
                "Tipo",
                "Ano",
                "Mês",
                "Bilhetagem",
            ]
        ]
        bilhetagem.to_sql("bilhetagem", con, if_exists="append", index=False)
        con.commit()
        print("Bilhetagem importada com sucesso.")
    except Exception as exc:
        print(f"Ops! ocorreu um erro ao importar a bilhetagem: {exc}")


def listar_bilhetagem(cur, **kwargs):
    """Lista dados de bilhetagem com base nos parâmetros fornecidos."""

    try:
        if "serie" in kwargs:
            return cur.execute("SELECT * FROM bilhetagem WHERE Serie = ?", (kwargs["serie"],))

        elif "contrato" in kwargs:
            return cur.execute(
                "SELECT * FROM bilhetagem WHERE Contrato = ?", (kwargs["contrato"],)
            )

        elif "localização" in kwargs:
            return cur.execute(
                "SELECT * FROM bilhetagem WHERE Localização = ?",
                (kwargs["localização"],),
            )

        elif "tipo" in kwargs:
            return cur.execute("SELECT * FROM bilhetagem WHERE Tipo = ?", (kwargs["tipo"],))

        elif "ano" in kwargs:
            return cur.execute("SELECT * FROM bilhetagem WHERE Ano = ?", (kwargs["ano"],))

        elif "mês" in kwargs:
            cur.execute("SELECT * FROM bilhetagem WHERE Mês = ?", (kwargs["mês"],))

        elif "bilhetagem" in kwargs:
            cur.execute(
                "SELECT * FROM bilhetagem WHERE Bilhetagem = ?", (kwargs["bilhetagem"],)
            )

    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao listar bilhetagem: {exc}")


def listar_bilhetagem_serie_ano_mes(con, cur, **kwargs):
    """Lista bilhetagem com base no número de série, ano e mês fornecidos."""

    """Tenta listar os dados e trata exceções em caso de erro."""
    try:

        if "serie" in kwargs and "ano" in kwargs and "mes" in kwargs:
            cur.execute(
                "SELECT * FROM bilhetagem WHERE Serie = ? AND Ano = ? AND Mês = ?",
                (kwargs["serie"], kwargs["ano"], kwargs["mes"]),
            )
            return cur.fetchall()
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao listar a bilhetagem: {exc}")
        con.rollback()
        return None


def listar_bilhetagem_por_tipo(cur, **kwargs):
    """Lista bilhetagem com base no tipo fornecido."""

    try:
        tipo = input("Insira o tipo de impressão: ")
        kwargs = {"tipo": tipo}
        resultado = listar_bilhetagem(cur, **kwargs)
        for row in resultado:
            print(dict(row))
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao listar a bilhetagem: {exc}")
