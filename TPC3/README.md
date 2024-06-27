---
Título: TPC3
Data: 5 de março de 2024
Autor: Joana Pereira
UC: SPLN
---

# Uso de templates para configuração de projetos

## Resumo

O script `makepyproject.py` cria um template Jinja2 para configuração de projetos Python, com o objetivo de facilitar a criação de projetos Python. Este template é usado para criar o ficheiro `pyproject.toml`, que contém as informações necessárias para configurar o projeto.

## Dependências

Para correr o script, é necessário ter o **python3** instalado.

```sh
sudo apt install python3
```

A biblioteca jjcli:

```sh
pip install jjcli
```

E a biblioteca jinja2:

```sh
pip install jinja2
```

## Instruções de Execução
Para executar o script, deve-se correr o seguinte comando:

```sh
python3 makepyproject.py
```