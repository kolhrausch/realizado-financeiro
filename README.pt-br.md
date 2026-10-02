# Automação do Realizado Financeiro

Ferramenta em Python que automatiza a elaboração do realizado financeiro a partir de extratos bancários.

## O problema

Na rotina atual, é preciso analisar os extratos de diversas empresas, que possuem várias contas em diferentes bancos. Cada entrada e saída precisa ser identificada e classificada de acordo com sua natureza: mútuos entre empresas, matéria-prima, fornecedores, impostos, despesas, transferências, entre outras. Feito à mão, esse processo é lento e sujeito a inconsistências.

## A solução

A automação importa um extrato bancário e classifica seus lançamentos com base em um cadastro de naturezas. Quando encontra um histórico novo, pede ao usuário que informe a natureza, e essa classificação passa a valer para as próximas execuções.

Exemplos:

- Um PIX entre empresas do grupo é classificado como **Mútuo**;
- O pagamento a determinado fornecedor é classificado como **Matéria-prima**;
- Históricos recorrentes são associados automaticamente à sua natureza.

O resultado é um relatório em Excel padronizado, com data, histórico, tipo (débito/crédito), natureza, valor, empresa e banco.

## Como funciona

1. O usuário seleciona o extrato, o banco e a empresa.
2. O programa lê o extrato e cruza cada histórico com o cadastro de naturezas.
3. Regras específicas (como a identificação de PIX por CPF/CNPJ) tratam os casos conhecidos.
4. Para cada histórico sem classificação, uma janela pede a natureza.
5. As novas classificações são gravadas no cadastro, que fica compartilhado entre os usuários.
6. O relatório `Realizado <banco> <empresa>.xlsx` é gerado.

## Bancos suportados

| Banco     | Status             |
|-----------|--------------------|
| Santander | Disponível         |
| Itaú      | Disponível         |
| Daycoval  | Disponível         |


## Tecnologias

Python, pandas, NumPy, tkinter (interface), openpyxl e lxml (leitura de extratos), PyInstaller (geração do executável).

## Estrutura

```
├── main.py             # fluxo principal
├── interface.py        # janelas (tkinter)
├── processamento.py    # leitura dos extratos e regras de classificação
└── config.py           # listas de bancos, empresas e naturezas
```

## Como executar

```
pip install pandas numpy openpyxl lxml
python main.py
```

Para gerar o executável (Windows):

```
pip install pyinstaller
pyinstaller --onefile --name ConciliadorBancario main.py
```


