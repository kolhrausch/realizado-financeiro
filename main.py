#main.py
import pandas as pd
import traceback
from tkinter import messagebox

try:
    from interface import selecionar_arquivo, selecionar_empresa_banco
    from config import BANCOS, EMPRESAS, CAMINHO_CADASTRO
    from processamento import processar_santander, processar_itau, processar_daycoval

    print("Iniciando programa")

    naturezas = pd.read_excel(CAMINHO_CADASTRO)

    archive = selecionar_arquivo()
    processar_arquivo = (archive)

    print("Arquivo selecionado", archive)

    banco, empresa = selecionar_empresa_banco()

    print("Empresa", empresa)
    print("Banco", banco)
    print("Cadastro de naturezas carregado")

    if banco == "Santander":

        print("Entrando no processamento Santander")

        processar_santander(
            archive,
            empresa,
            banco,
            naturezas
        )

        print("Processamento Santander terminou")

    if banco == "Itaú":
        print("Entrando no processamento Itaú")
        processar_itau(
            archive,
            empresa,
            banco,
            naturezas
        )
        print("Processamento Itaú terminou")

    if banco == "Daycoval":
        print("Entrando no processamento Daycoval")
        processar_daycoval(
            archive, 
            empresa, 
            banco, 
            naturezas
            )
        print("Processamento Daycoval terminou")

except SystemExit:
    pass  
except Exception:
    messagebox.showerror("Erro", traceback.format_exc())