---
Título: TPC 1 e 2
Data: 28 de Fevereiro de 2024
Autor: Joana Pereira
UC: SPLN
---

# Uso de templates para configuração de projetos

## Resumo

O script `word_freq.py` calcula a frequência de palavras em um texto. Ele possui várias opções para personalizar a saída, como ordenar alfabeticamente, capitalizar por referência.

## Dependências

Para correr o script, é necessário ter o **python3** instalado.

```sh
sudo apt install python3
```

A biblioteca jjcli:

```sh
pip install jjcli
```

## Instruções de Execução

Para executar o script, deve-se correr o seguinte comando:

```sh
python3 word_freq.py [options] input_files
```

### Opções Disponíveis

- -m 20 -> Mostrar as 20 palavras mais comuns.
- -n -> Ordenar alfabeticamente.
- -c -> Capitalização por referência.

### Exemplo de Execução

Para o arquivo de texto exemplo.txt, pode-se executar o script com a seguinte linha de comando:

```sh
wfreq -m 20 tests/Camilo-Amor_de_Perdicao.md
```

```sh
wfreq -n tests/Camilo-Amor_de_Perdicao.md
```
