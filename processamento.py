#processamento.py
import pandas as pd
import numpy as np

from interface import selecionar_natureza
from config import CAMINHO_CADASTRO, NATUREZAS
from config import grupo
from config import socios
from config import historicos_manuais
from config import naturezas_manuais




def ler_extrato(archive, header, tabela_com=None):
    try:
        return pd.read_excel(archive, header=header)
    except ValueError:
        with open(archive, "rb") as f:
            inicio = f.read(300).lower()
        if b"<html" in inicio or b"<table" in inicio or b"<!doctype" in inicio:
            return pd.read_html(archive, match=tabela_com, header=0,
                                thousands=None, encoding="utf-8")[0]
        return pd.read_csv(archive, header=header, sep=None,
                           engine="python", encoding="latin-1")


def para_numero(col):
    """Converte '2.100,17', '-60,00' e '-' em número. Se já for número, mantém."""
    if pd.api.types.is_numeric_dtype(col):
        return col.fillna(0)
    limpo = (col.astype(str).str.strip()
             .str.replace(".", "", regex=False)
             .str.replace(",", ".", regex=False))
    return pd.to_numeric(limpo, errors="coerce").fillna(0)


def regra_pix(df):

    pix = df["Histórico"].astype(str).str.extract(
        r'PIX RECEBIDO\s+(\d{11}|\d{14})',
        expand=False
    )

    for cpf_socio, nat in socios.items():
        df.loc[pix == cpf_socio, "Natureza"] = nat

    for cnpj_grupo, nat in grupo.items():
        df.loc[pix == cnpj_grupo, "Natureza"] = nat

    numeros_especiais = list(socios.keys()) + list(grupo.keys())

    df.loc[
        pix.notna() & ~pix.isin(numeros_especiais),
        "Natureza"
    ] = "Recebimento De Cliente"

    return df




def processar_santander(archive, empresa, banco, naturezas):

    dados_sant = pd.read_excel(archive, header=2)

    dados_sant = dados_sant.merge(
        naturezas,
        left_on="Histórico",
        right_on="Descrição Extrato",
        how="left")

    if empresa in ("Empresa 1", "Empresa 2"):
        dados_sant = regra_pix(dados_sant)

    sem_natureza = dados_sant[dados_sant["Natureza"].isna()]
    naturezas_novas_sant = []
    escolhas_linha = {}   # índice da linha -> natureza (casos manuais)
    memorizados = set()   # históricos já memorizados nesta execução

    print("Total de linhas:", len(dados_sant))
    print("Linhas sem natureza:", len(sem_natureza))

    for index, row in sem_natureza.iterrows():

        historico = row["Histórico"]

        if historico in memorizados:
            continue

        resultado = selecionar_natureza(
            historico=historico,
            valor=row["Valor (R$)"],
            data=row["Data"],
            naturezas=NATUREZAS
        )

        natureza = resultado["natureza"]
        if resultado["cancelado"] or natureza is None:
            raise SystemExit("Cancelado")

        manual = (any(t in historico for t in historicos_manuais)
                  or natureza in naturezas_manuais)

        if manual:
            escolhas_linha[index] = natureza
        else:
            naturezas_novas_sant.append({"Natureza": natureza,
                                         "Descrição Extrato": historico})
            memorizados.add(historico)

        print("Natureza escolhida:", natureza)

    naturezas = pd.concat([naturezas, pd.DataFrame(naturezas_novas_sant)])
    naturezas = naturezas.drop_duplicates("Descrição Extrato")
    naturezas.to_excel(CAMINHO_CADASTRO, index=False)

    dados_sant = pd.read_excel(archive, header=2)
    dados_sant = dados_sant.merge(
        naturezas,
        left_on="Histórico",
        right_on="Descrição Extrato",
        how="left")

    dados_sant["Débito/Crédito"] = np.where(
        dados_sant["Valor (R$)"] > 0, "Crédito", "Débito"
    )

    if empresa in ("Empresa 1", "Empresa 2"):
        dados_sant = regra_pix(dados_sant)


    for idx, nat in escolhas_linha.items():
        dados_sant.loc[idx, "Natureza"] = nat

    dados_sant["Banco"] = banco
    dados_sant["Empresa"] = empresa

    dados_sant = dados_sant[[
        "Data",
        "Histórico",
        "Débito/Crédito",
        "Natureza",
        "Valor (R$)",
        "Empresa",
        "Banco"
    ]]

    dados_sant.to_excel(f"Realizado {banco} {empresa}.xlsx", index=False)




def processar_itau(archive, empresa, banco, naturezas):

    dados_itau = pd.read_excel(archive, header=9)

    # remove linhas de saldo (na=False evita erro com células vazias)
    dados_itau = dados_itau[~dados_itau["Lançamento"].astype(str).str.strip().str.upper().str.startswith("SALDO")]

    dados_itau["Razão Social"] = dados_itau["Razão Social"].fillna(dados_itau["Lançamento"])

    dados_itau = dados_itau.merge(
        naturezas,
        left_on="Razão Social",
        right_on="Descrição Extrato",
        how="left")

    sem_natureza = dados_itau[dados_itau["Natureza"].isna()]
    naturezas_novas_itau = []
    escolhas_linha = {}
    memorizados = set()

    print("Total de linhas:", len(dados_itau))
    print("Linhas sem natureza:", len(sem_natureza))

    for index, row in sem_natureza.iterrows():

        historico = row["Razão Social"]

        if historico in memorizados:
            continue

        resultado = selecionar_natureza(
            historico=historico,
            valor=row["Valor (R$)"],
            data=row["Data"],
            naturezas=NATUREZAS
        )

        natureza = resultado["natureza"]
        if resultado["cancelado"] or natureza is None:
            raise SystemExit("Cancelado")

        manual = (any(t in historico for t in historicos_manuais)
                  or natureza in naturezas_manuais)

        if manual:
            escolhas_linha[index] = natureza
        else:
            naturezas_novas_itau.append({"Natureza": natureza,
                                         "Descrição Extrato": historico})
            memorizados.add(historico)

        print("Natureza escolhida:", natureza)

    naturezas = pd.concat([naturezas, pd.DataFrame(naturezas_novas_itau)])
    naturezas = naturezas.drop_duplicates("Descrição Extrato")
    naturezas.to_excel(CAMINHO_CADASTRO, index=False)

    mapa_novas = {n["Descrição Extrato"]: n["Natureza"] for n in naturezas_novas_itau}
    dados_itau["Natureza"] = dados_itau["Natureza"].fillna(dados_itau["Razão Social"].map(mapa_novas))

    dados_itau["Débito/Crédito"] = np.where(
        dados_itau["Valor (R$)"] > 0, "Crédito", "Débito"
    )

    for idx, nat in escolhas_linha.items():
        dados_itau.loc[idx, "Natureza"] = nat

    dados_itau["Banco"] = banco
    dados_itau["Empresa"] = empresa

    dados_itau = dados_itau[[
        "Data",
        "Razão Social",
        "Débito/Crédito",
        "Natureza",
        "Valor (R$)",
        "Empresa",
        "Banco"
    ]]

    dados_itau.to_excel(f"Realizado {banco} {empresa}.xlsx", index=False)



def processar_daycoval(archive, empresa, banco, naturezas):

    dados = ler_extrato(archive, header=6, tabela_com="Lancamento")
    dados.columns = dados.columns.str.strip()

    # tira linhas vazias e de saldo
    dados = dados.dropna(subset=["Lancamento"])
    dados = dados[~dados["Lancamento"].astype(str).str.strip().str.lower().str.startswith("saldo")]

    # padroniza espaços e quebras de linha do histórico
    dados["Lancamento"] = (dados["Lancamento"].astype(str)
                           .str.replace(r"\s+", " ", regex=True)
                           .str.strip())

    # junta débito e crédito numa coluna só ("-" e vazio viram 0)
    for col in ["Debito (R$)", "Credito (R$)"]:
        dados[col] = para_numero(dados[col])
    dados["Valor (R$)"] = dados["Credito (R$)"] + dados["Debito (R$)"]

    dados = dados.merge(
        naturezas,
        left_on="Lancamento",
        right_on="Descrição Extrato",
        how="left")

    sem_natureza = dados[dados["Natureza"].isna()]
    naturezas_novas = []
    escolhas_linha = {}
    memorizados = set()

    print("Total de linhas:", len(dados))
    print("Linhas sem natureza:", len(sem_natureza))

    for index, row in sem_natureza.iterrows():

        historico = row["Lancamento"]

        if historico in memorizados:
            continue

        resultado = selecionar_natureza(
            historico=historico,
            valor=row["Valor (R$)"],
            data=row["Data"],
            naturezas=NATUREZAS
        )

        natureza = resultado["natureza"]
        if resultado["cancelado"] or natureza is None:
            raise SystemExit("Cancelado")

        manual = (any(t in historico for t in historicos_manuais)
                  or natureza in naturezas_manuais)

        if manual:
            escolhas_linha[index] = natureza
        else:
            naturezas_novas.append({"Natureza": natureza,
                                    "Descrição Extrato": historico})
            memorizados.add(historico)

        print("Natureza escolhida:", natureza)

    naturezas = pd.concat([naturezas, pd.DataFrame(naturezas_novas)])
    naturezas = naturezas.drop_duplicates("Descrição Extrato")
    naturezas.to_excel(CAMINHO_CADASTRO, index=False)

    mapa_novas = {n["Descrição Extrato"]: n["Natureza"] for n in naturezas_novas}
    mascara = dados["Natureza"].isna()
    dados.loc[mascara, "Natureza"] = dados.loc[mascara, "Lancamento"].map(mapa_novas)

    dados["Débito/Crédito"] = np.where(dados["Valor (R$)"] > 0, "Crédito", "Débito")

    for idx, nat in escolhas_linha.items():
        dados.loc[idx, "Natureza"] = nat

    dados["Banco"] = banco
    dados["Empresa"] = empresa

    dados = dados[[
        "Data",
        "Lancamento",
        "Débito/Crédito",
        "Natureza",
        "Valor (R$)",
        "Empresa",
        "Banco"
    ]]

    dados.to_excel(f"Realizado {banco} {empresa}.xlsx", index=False)