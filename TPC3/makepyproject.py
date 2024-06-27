import json
import os
import jinja2
from glob import glob
import subprocess

# Função para obter o nome do módulo
def obter_nome_modulo():
    arquivos_py = glob("*.py")
    if len(arquivos_py) >= 1:
        return arquivos_py[0].replace(".py", "")
    else:
        return input("Modulo? ").replace(".py", "")

# Função para obter a versão do módulo
def obter_versao_modulo(nome_modulo):
    resultado = subprocess.run(f"grep __version__ {nome_modulo}.py", shell=True, capture_output=True, text=True)
    if resultado.stdout:
        return resultado.stdout.split("=")[-1].strip().replace('"', '')
    return "0.0.1"

# Função para carregar o METADATA.json
def carregar_metadata(caminho_metadata):
    if not os.path.exists(caminho_metadata):
        print("Erro: METADATA.json não encontrado.")
        return None
    with open(caminho_metadata, 'r') as arquivo:
        return json.load(arquivo)

# Função para gerar o conteúdo do pyproject.toml
def gerar_pyproject_toml(nome_modulo, versao, autor, email):
    template_str = '''
    [build-system]
    requires = ["flit_core >=3.2,<4"]
    build-backend = "flit_core.buildapi"

    [project]
    name = "{{ nome_modulo }}"
    authors = [
        {name = "{{ autor }}", email = "{{ email }}"},
    ]
    version = "{{ versao }}"
    readme = "README.md"
    classifiers = [
        "License :: OSI Approved :: MIT License",
    ]
    requires-python = ">=3.8"
    dynamic = ["description"]

    dependencies = [
        "jjcli",
        "jinja2"
    ]

    [project.scripts]
    {{ nome_modulo }} = "{{ nome_modulo }}:main"
    '''

    template = jinja2.Template(template_str)
    return template.render(nome_modulo=nome_modulo, versao=versao, autor=autor, email=email)

def main():
    nome_modulo = obter_nome_modulo()
    versao = obter_versao_modulo(nome_modulo)
    metadata = carregar_metadata("METADATA.json")
    if metadata:
        autor = metadata.get("Username", "")
        email = metadata.get("Email", "")
        conteudo_pyproject = gerar_pyproject_toml(nome_modulo, versao, autor, email)
        with open("pyproject.toml", "w") as arquivo_saida:
            arquivo_saida.write(conteudo_pyproject)
        print("pyproject.toml gerado com sucesso.")
    else:
        print("Falha ao carregar METADATA.json.")

if __name__ == "__main__":
    main()
