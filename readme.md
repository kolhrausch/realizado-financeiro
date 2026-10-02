# Financial Actuals Automation

🇧🇷 [Leia em português](README.pt-BR.md)

A Python tool that automates the preparation of the financial actuals ("realizado financeiro") from bank statements.

## The problem

Preparing the actuals means going through the statements of several companies, each with multiple accounts at different banks. Every inflow and outflow has to be identified and classified by its nature: intercompany loans, raw materials, suppliers, taxes, expenses, transfers, and so on. Done by hand, this is slow and prone to inconsistencies.

## The solution

The tool imports a bank statement and classifies its transactions using a lookup table of known descriptions. When it finds a description it doesn't know, it asks the user for the category, and that choice is remembered for future runs.

Examples:

- A PIX transfer between group companies is classified as **Mutuo** (intercompany loan);
- A payment to a given supplier is classified as **Materia Prima** (raw material);
- Recurring descriptions are matched to their category automatically.

The output is a standardized Excel report with date, description, debit/credit, category, amount, company and bank.

## How it works

1. The user picks the statement file, the bank and the company.
2. The program reads the statement and matches each description against the lookup table.
3. Specific rules (such as identifying PIX transfers by CPF/CNPJ) handle known cases.
4. For each unclassified description, a window asks for the category.
5. New classifications are saved to the lookup table, which can be shared across users.
6. The report `Realizado <bank> <company>.xlsx` is generated.

## Supported banks

| Bank      | Status    |
|-----------|-----------|
| Santander | Available |
| Itaú      | Available |
| Daycoval  | Available |

## Tech stack

Python, pandas, NumPy, tkinter (UI), openpyxl and lxml (statement parsing), PyInstaller (executable build).

## Project structure

```
├── main.py             # main flow
├── interface.py        # windows (tkinter)
├── processamento.py    # statement parsing and classification rules
└── config.py           # lists of banks, companies and categories
```

## Getting started

```
pip install pandas numpy openpyxl lxml
python main.py
```

Set `CAMINHO_CADASTRO` in `config.py` to point to the category lookup spreadsheet (a sample `cadastro natureza.xlsx` is included). For team use, point it to a shared network folder. Sample statements for each bank are included in the repository.

To build a Windows executable:

```
pip install pyinstaller
pyinstaller --onefile --name ConciliadorBancario --hidden-import lxml --hidden-import openpyxl main.py
```

## Data and privacy

This repository contains only fictitious sample data. Real statements, lookup tables, company identifiers and generated reports are not included.

## Status

Work in progress.