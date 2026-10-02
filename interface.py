#interface.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def selecionar_arquivo():
    janela = tk.Tk()
    janela.withdraw()

    archive = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[("Arquivos Excel", "*.xlsx *.xls"),
                ("Todos os arquivos", "*.*")]    
    )

    janela.destroy()

    return archive #retorna o arquivo para fora da função

def selecionar_empresa_banco():

    janela = tk.Tk()
    janela.title("Selecione a empresa e banco")
    janela.geometry("450x350")

    tk.Label(janela, text="Selecione o banco", font=("Arial", 16)).pack(pady=10)
    banco_opcao = ["Daycoval", "Itaú", "Santander"]

    tk.Label(janela, text="Selecione a empresa", font=("Arial", 16)).pack(pady=10)
    empresa_opcao = ["Empresa 1", "Empresa 2", "Empresa 3", "Empresa 4", "Empresa 5", "Empresa 6", "Empresa 7", "Empresa 8"]

    selecao_banco = ttk.Combobox(janela, values=banco_opcao,
                       state="readonly", font=("Arial", 14))
    selecao_banco.pack(pady=15)
    selecao_banco.current(0)

    selecao_empresa = ttk.Combobox(janela, values=empresa_opcao,
                       state="readonly", font=("Arial", 14))
    selecao_empresa.pack(pady=15)
    selecao_empresa.current(0)

    banco = None
    empresa = None

    def confirmar():
        nonlocal banco, empresa
        banco = selecao_banco.get()
        empresa = selecao_empresa.get()
        print(f"Empresa selecionado: {empresa}")
        print(f"Banco selecionado: {banco}")
        janela.destroy()

    tk.Button(janela, text="Confirmar", command=confirmar, font=("Arial", 14)).pack(pady=10)
    janela.mainloop()
    return banco, empresa

def selecionar_natureza(historico, valor, data, naturezas):
    janela = tk.Tk()
    janela.title("Nova natureza")
    janela.geometry("600x300")

    tk.Label(
        janela,
        text=f"Nova natureza encontrada: ",
        font=("Arial", 12)
        ).pack(pady=10)
    
    tk.Label(
        janela,
        text= historico,
        font=("Arial", 12)
        ).pack(pady=10)


    tk.Label(
        janela,
        text= valor,
        font=("Arial", 12)
        ).pack(pady=10)


    tk.Label(
        janela,
        text= data,
        font=("Arial", 12)
        ).pack(pady=10)

    selecao = ttk.Combobox(
    janela,
    values=naturezas,
    state="readonly"
    )

    selecao.pack(pady=15)
    selecao.current(0)

    resultado = {
        "natureza": None,
        "cancelado": False
    }

    
    def confirmar():
        resultado["natureza"] = selecao.get()
        janela.destroy()
          
    def cancelar():
        resultado["cancelado"] = True
        janela.destroy()

    tk.Button(janela,
              text="Confirmar",
              command=confirmar
              ).pack()
    
    tk.Button(janela,
              text="Cancelar",
              command=cancelar
              ).pack()

    janela.mainloop()

    return resultado