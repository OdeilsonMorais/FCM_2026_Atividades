import re
import pandas as pd
import pdfplumber
from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_PDF = Path(__file__).resolve().parent / "cadastro.pdf"



# ============================================================
# 1. FUNÇÃO PARA LER TODO O TEXTO DO PDF
# ============================================================

def ler_pdf(caminho_pdf):
    texto_completo = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()

            if texto_pagina:
                texto_completo += texto_pagina + "\n"

    return texto_completo


# ============================================================
# 2. FUNÇÃO PARA BUSCAR UM CAMPO COM REGEX
# ============================================================

def buscar_campo(padrao, texto):
    resultado = re.search(
        padrao,
        texto,
        flags=re.IGNORECASE | re.MULTILINE
    )

    if resultado:
        return resultado.group(1).strip()

    return None


# ============================================================
# 3. FUNÇÕES DE LIMPEZA / NORMALIZAÇÃO
# ============================================================

def limpar_cpf(cpf):
    """
    Remove pontos e hífen.
    Exemplo:
    876.946.333-90 -> 87694633390
    """

    if cpf is None:
        return None

    return re.sub(r"\D", "", cpf)


def limpar_telefone(telefone):
    """
    Remove parênteses, espaços e hífens.
    Exemplo:
    (12) 92134-9999 -> 12921349999
    """

    if telefone is None:
        return None

    return re.sub(r"\D", "", telefone)


def limpar_cep(cep):
    """
    Remove caracteres que não sejam números.
    Exemplo:
    32722-000 -> 32722000
    """

    if cep is None:
        return None

    return re.sub(r"\D", "", cep)


# ============================================================
# 4. FUNÇÃO PRINCIPAL DE EXTRAÇÃO DOS DADOS
# ============================================================

def extrair_dados(texto):

    # --------------------------------------------------------
    # Separa os registros sempre que encontrar "Nome:"
    # --------------------------------------------------------

    registros = re.split(
        r"(?i)(?=nome\s*:)",
        texto
    )

    # Remove registros vazios
    registros = [
        registro.strip()
        for registro in registros
        if registro.strip()
    ]


    dados = []


    # --------------------------------------------------------
    # Percorre cada cadastro encontrado
    # --------------------------------------------------------

    for registro in registros:

        # Nome
        nome = buscar_campo(
            r"nome\s*:\s*(.+)",
            registro
        )


        # Data de nascimento
        # Aceita:
        # Data de nascimento:
        # Dt nasc:
        nascimento = buscar_campo(
            r"(?:data\s+de\s+nascimento|dt\s+nasc)\s*:\s*(.+)",
            registro
        )


        # Endereço
        # Captura até encontrar CEP, quebra de linha ou fim
        endereco = buscar_campo(
            r"endere[cç]o\s*:\s*(.+?)(?=\s+CEP\s*:|\n|$)",
            registro
        )


        # CEP
        cep = buscar_campo(
            r"CEP\s*:\s*([\d\.\-]+)",
            registro
        )


        # Telefone
        # Aceita:
        # Tel:
        # Telefone:
        telefone = buscar_campo(
            r"(?:tel|telefone)\s*:\s*([\d\s\(\)\-]+)",
            registro
        )


        # CPF
        cpf = buscar_campo(
            r"cpf\s*:\s*([\d\.\-]+)",
            registro
        )


        # ----------------------------------------------------
        # Adiciona à lista
        # ----------------------------------------------------

        dados.append({

            "Nome": nome,

            "Data de nascimento": nascimento,

            "Endereço": endereco,

            "CEP": cep,

            "CEP limpo": limpar_cep(cep),

            "Telefone": telefone,

            "Telefone limpo": limpar_telefone(telefone),

            "CPF": cpf,

            "CPF limpo": limpar_cpf(cpf)
        })


    return dados


# ============================================================
# 5. EXECUÇÃO DO PROGRAMA
# ============================================================

texto_pdf = ler_pdf(ARQUIVO_PDF)


# Opcional:
# mostra o texto extraído do PDF
print("\n================ TEXTO EXTRAÍDO ================\n")

print(texto_pdf)


# ============================================================
# 6. EXTRAIR OS CADASTROS
# ============================================================

dados = extrair_dados(texto_pdf)


# ============================================================
# 7. CRIAR DATAFRAME
# ============================================================

df = pd.DataFrame(dados)


print("\n================ DADOS EXTRAÍDOS ================\n")

print(df)