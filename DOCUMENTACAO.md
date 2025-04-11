# Documentação do Sistema de Outsourcing

## Visão Geral
Sistema de gerenciamento de impressoras, chamados e bilhetagem desenvolvido em Python com SQLite. Permite:
- Cadastro e consulta de impressoras
- Abertura e acompanhamento de chamados técnicos
- Controle de bilhetagem (contagem de impressões)

## Estrutura de Arquivos
```
.
├── main.py                # Ponto de entrada do sistema
├── requirements.txt       # Dependências do projeto
├── db/                    # Banco de dados SQLite
├── planilhas/             # Arquivos CSV de entrada
│   ├── glpi.csv           # Dados de chamados
│   ├── impressoras.csv    # Dados de impressoras  
│   └── bilhetagem.csv     # Dados de bilhetagem
└── Outsourcing/           # Módulos do sistema
    ├── bilhetagem.py      # Gerenciamento de bilhetagem
    ├── chamados.py        # Gerenciamento de chamados
    └── impressoras.py     # Gerenciamento de impressoras
```

## Módulos Principais

### main.py
- Menu principal e navegação
- Funções auxiliares (limpeza de terminal)
- Conexão com banco de dados
- Importação inicial de dados

### bilhetagem.py
- `criar_tabela_bilhetagem()`: Cria tabela no banco de dados
- `importar_bilhetagem()`: Importa dados de CSV
- `listar_bilhetagem()`: Consultas com filtros
- `listar_bilhetagem_serie_ano_mes()`: Consulta específica

### chamados.py  
- `importar_chamados()`: Importa dados de CSV
- `atualizar_chamados()`: Relaciona chamados com impressoras
- `listar_chamados()`: Consultas com filtros
- `criar_nova_tabela()`: Estrutura otimizada

### impressoras.py
- `criar_tabela_impressoras()`: Cria tabela no banco
- `importar_impressoras()`: Importa dados de CSV  
- `listar_impressoras()`: Consultas com filtros
- `remanejar_impressora()`: Atualiza localização
- `deletar_impressora()`: Remove registro

## Requisitos do Sistema
- Python 3.x
- Dependências:
  - pandas==2.2.3
  - numpy==2.2.4
  - python-dateutil==2.9.0.post0
  - pytz==2025.2
  - six==1.17.0
  - tzdata==2025.2

## Como Executar
1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Prepare os arquivos CSV na pasta `planilhas/`:
- glpi.csv
- impressoras.csv  
- bilhetagem.csv

3. Execute o sistema:
```bash
python main.py
```

4. Siga o menu interativo para:
- Consultar impressoras
- Gerenciar chamados
- Verificar bilhetagem

## Observações
- O banco de dados SQLite é criado automaticamente na primeira execução
- Os arquivos CSV devem seguir a estrutura esperada pelos módulos
- O sistema foi desenvolvido para Windows (comando `cls` para limpar terminal)
