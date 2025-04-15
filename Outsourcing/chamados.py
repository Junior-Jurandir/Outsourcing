import pandas as pd


def importar_chamados(
    con, chamados
):  # Importa chamados de um arquivo CSV para o banco de dados

    try:
        chamados = pd.read_csv(chamados)
        chamados_filtrados = chamados[
            [
                '﻿"ID"',
                "Título",
                "Status",
                "Requerente - Requerente",
                "Localização",
                "Descrição",
            ]
        ].copy()
        chamados_filtrados.rename(
            columns={'﻿"ID"': "ID"}, inplace=True
        )  # Fixing the column name without hidden characters
        chamados_filtrados.to_sql("chamados", con, if_exists="replace", index=False)
        con.commit()
        print("Chamados importados com sucesso.")
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao importar os chamados: {exc}")


def coluna_existe(cur, table, column):  # Verifica se uma coluna existe em uma tabela
    try:
        cur.execute(f"PRAGMA table_info({table});")
        columns = [row[1] for row in cur.fetchall()]
        return column in columns
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao verificar a existência da coluna: {exc}")
        return False


def adicionar_coluna(cur, con):  # Adiciona uma coluna a uma tabela
    try:
        if not coluna_existe(cur, "chamados", "serie_impressora"):
            cur.execute("ALTER TABLE chamados ADD COLUMN serie_impressora TEXT;")
            con.commit()
            print("Coluna 'serie_impressora' adicionada com sucesso.")
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao adicionar a coluna: {exc}")


def atualizar_chamados(
    cur, con
):  # Atualiza os chamados com base na série da impressora
    try:
        query = """
            UPDATE chamados
            SET serie_impressora = (
                SELECT i.serie
                FROM impressoras i
                WHERE chamados.Descrição LIKE '%' || i.serie || '%'
                LIMIT 1
            )
            WHERE EXISTS (
                SELECT 1 FROM impressoras i
                WHERE chamados.Descrição LIKE '%' || i.serie || '%'
            );
        """
        cur.execute(query)
        con.commit()
        print("Chamados atualizados com sucesso.")
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao atualizar os chamados: {exc}")


def criar_nova_tabela(
    cur, con
):  # Recria a tabela de chamados para definir a chave primária e adicionar a chave estrangeira (SQLite não suporta 'ALTER TABLE ADD FOREIGN KEY').
    try:
        cur.execute("PRAGMA foreign_keys = OFF;")  # Desativar restrições temporariamente
        cur.execute("DROP TABLE IF EXISTS chamados_nova;")
        cur.execute(
            """
            CREATE TABLE chamados_nova(
                Id INTEGER PRIMARY KEY,
                Título TEXT NOT NULL,
                Status TEXT NOT NULL,
                Requerente TEXT,
                Localizacao TEXT NOT NULL,
                Descricao TEXT NOT NULL,
                Serie_impressora TEXT,
                FOREIGN KEY (Serie_impressora) REFERENCES impressoras(Serie)
            );
        """
        )

        cur.execute(
            """
            INSERT INTO chamados_nova (Id, Título, Status, Requerente, Localizacao, Descricao, Serie_impressora)
            SELECT Id, Título, Status, "Requerente - Requerente", Localização, Descrição, Serie_impressora FROM chamados;
            """
        )

        cur.execute("DROP TABLE chamados;")  # Remover tabela antiga
        cur.execute("ALTER TABLE chamados_nova RENAME TO chamados;")  # Renomear nova tabela
        cur.execute("PRAGMA foreign_keys = ON;")  # Reativar restrições
        con.commit()
        print("Tabela 'chamados' recriada com sucesso.")
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao recriar a tabela: {exc}")
        con.rollback()


def listar_chamados(cur, **kwargs):  # Lista chamados com base em critérios fornecidos

    try:
        if "id" in kwargs:
            return cur.execute("SELECT * FROM chamados WHERE ID = ?", (kwargs["id"],))

        elif "titulo" in kwargs:
            return cur.execute(
                "SELECT * FROM chamados WHERE Título = ?", (kwargs["titulo"],)
            )

        elif "status" in kwargs:
            return cur.execute(
                "SELECT * FROM chamados WHERE Status = ?", (kwargs["status"],)
            )

        elif "requerente" in kwargs:
            return cur.execute(
                "SELECT * FROM chamados WHERE Requerente - Requerente = ?",
                (kwargs["requerente"],),
            )

        elif "Local" in kwargs:
            return cur.execute(
                "SELECT * FROM chamados WHERE Localização = ?", (kwargs["Local"],)
            )

        elif "serie" in kwargs:
            return cur.execute(
                "SELECT * FROM chamados WHERE Descricao LIKE ?",
                (f"%{kwargs['serie']}%",),
            )

    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao listar os chamados: {exc}")


def exportar_chamados_para_csv(con, caminho_arquivo):
    """Exporta a tabela de chamados para um arquivo CSV
    
    Args:
        con: Conexão com o banco de dados
        caminho_arquivo: Caminho completo para o arquivo CSV de saída
    """
    try:
        # Ler a tabela chamados para um DataFrame
        df = pd.read_sql("SELECT * FROM chamados", con)
        
        # Exportar para CSV
        df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig')
        print(f"Chamados exportados com sucesso para {caminho_arquivo}")
    except Exception as exc:
        print(f"Ops! Ocorreu um erro ao exportar os chamados: {exc}")
