from pathlib import Path

#Inserir o diretorio do arquivo cadastro natureza.xlsx, que contem a lista de natureza de pagamentos, para que o programa possa ler e categorizar os pagamentos automaticamente
CAMINHO_CADASTRO = Path(r"G:\-DIRETORIO GENERICO\-ARQUIVO NATUREZAS\cadastro natureza.xlsx")

EMPRESAS = [
    "Empresa 1",
    "Empresa 2",
    "Empresa 3",
    "Empresa 4",
    "Empresa 5",
    "Empresa 6",
    "Empresa 7",
    "Empresa 8",
    ]

BANCOS = [
    "Daycoval",
    "Itaú",
    "Santander"
    ]

NATUREZAS = [
            "Acordo",
            "Acordo Judicial",
            "Adiantamento de Salário",
            "Aluguel",
            "Aplicação",
            "Bloqueio",
            "Certificado",
            "Combustível",
            "Condominio",
            "Cpa",
            "Devolução",
            "Despesa de Viagem",
            "Despesas Administrativas",
            "Despesas com Telefonia",
            "Despesas Diversas",
            "Emprestimo Consignado",
            "Extra / Freelancer",
            "Exportação",
            "Férias",
            "FGTS",
            "Fretes e Carretos",
            "IOF",
            "Imposto",
            "IPTU",
            "Juros",
            "Jurídico",
            "Manutenção",
            "Materia Prima",
            "Materiais Diversos",
            "Materiais Gráficos",
            "Material de Higiene e Limpeza",
            "Mensalidades",
            "Medicina e Segurança do Trabalho",
            "Mutuo",
            "PJ",
            "Plano de Saúde",
            "Qualidade",
            "Recebimento De Cliente",
            "Recebimento De Franquias",
            "Recebimento De Varejo",
            "Refeitorio",
            "Rescisão",
            "Retirada de Sócio",
            "Rolagem",
            "Salário",
            "Seguro",
            "Serviços de Terceiros",
            "Sindicato",
            "Sistemas",
            "Tarifa",
            "Taxas e Emolumentos",
            "Trabalhista",
            "Uniformes",
            "Vale Alimentação",
            "Vale Transporte"
    ]

      #CNPJs simulados para teste, caso queira testar com CNPJs reais, basta colocar os CNPJs reais no lugar dos simulados 
grupo = {"xxxxxxxxxxxxxx":"Mutuo", #simulated CNPJs
        "yyyyyyyyyyyyyy":"Mutuo",
        "zzzzzzzzzzzzzz":"Mutuo",
        "aaaaaaaaaaaaaa":"Mutuo",
        "bbbbbbbbbbbbbb":"Mutuo",
        "cccccccccccccc":"Mutuo",
    }

    #CPF simulados para teste, caso queira testar com CPFs reais, basta colocar os CPFs reais no lugar dos simulados
socios = {"xxxxxxxxxxx":"Mutuo"} #simulated CPFs


#historico manual para pagamentos com descrição generica, que não é possível identificar a natureza do pagamento, e que precisa ser categorizado manualmente
historicos_manuais = [
        "SISPAG FORNECEDORES",
        "PGTO VIA ARQUIVO:",
        "PAGFOR PIX OUTRA INST- DIFEREN",
        "PGTO FORNEC TIT PROPRIOS"
    ]

#naturezas manuais que podem ser pagas para a mesma pessoa mais de uma vez, e que precisam ser categorizadas manualmente
naturezas_manuais = [
        "Férias",
        "Rescisão",
        "Salário",
        "Adiantamento de Salário",
        "Extra / Freelancer",
        "PJ"
    ]