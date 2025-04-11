import pandas as pd


def criar_tabela_impressoras(con, cur):  # Cria a tabela impressoras no banco de dados
    try:
        cur.execute(
            "CREATE TABLE impressoras (Serie VARCHAR(100) PRIMARY KEY, Contrato VARCHAR(10), Localização VARCHAR(500), Tipo VARCHAR(10))"
        )
        con.commit()
        print("Tabela impressoras criada com sucesso.")
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao criar a tabela impressoras: {exc}")
        con.rollback()


def importar_impressoras(
    con, bilhetagem
):  # Importa impressoras de um arquivo CSV para o banco de dados

    try:
        impressoras = pd.read_csv(bilhetagem)
        impressoras = impressoras[
            [
                "Serie",
                "Contrato",
                "Localização",
                "Tipo",
            ]
        ]
        impressoras.to_sql("impressoras", con, if_exists="append", index=False)
        con.commit()
        print("Impressoras importadas com sucesso.")
    except Exception as exc:
        print(f"Ops! ocorreu um erro ao importar as impressoras: {exc}")


def listar_impressoras(
    cur, **kwargs
):  # Lista impressoras com base em critérios fornecidos

    try:
        if "serie" in kwargs:
            return cur.execute(
                "SELECT Serie, Contrato, Localização, Tipo FROM impressoras WHERE Serie = ?",
                (kwargs["serie"],),
            )
        elif "contrato" in kwargs:
            return cur.execute(
                "SELECT Serie, Contrato, Localização, Tipo FROM impressoras WHERE Contrato = ?",
                (kwargs["contrato"]),
            )
        elif "localização" in kwargs:
            return cur.execute(
                "SELECT Serie, Contrato, Localização, Tipo FROM impressoras WHERE Localização = ?",
                (kwargs["localização"]),
            )
        elif "tipo" in kwargs:
            return cur.execute(
                "SELECT Serie, Contrato, Localização, Tipo FROM impressoras WHERE Tipo = ?",
                (kwargs["tipo"]),
            )
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao listar impressoras: {exc}")


def remanejar_impressora(
    con, cur, serie, nova_localização
):  # Atualiza a localização de uma impressora

    try:
        cur.execute(
            "UPDATE impressoras SET Localização = ? WHERE Serie = ?",
            (nova_localização, serie),
        )
        con.commit()
        print("Impressora remanejada com sucesso.")
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao remanejar impressora: {exc}")
        con.rollback()


def deletar_impressora(con, cur, serie):  # Deleta uma impressora do banco de dados

    try:
        cur.execute("DELETE FROM impressoras WHERE Serie = ?", (serie,))
        con.commit()
        print("Impressora deletada com sucesso.")
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao deletar impressora: {exc}")
        con.rollback()
