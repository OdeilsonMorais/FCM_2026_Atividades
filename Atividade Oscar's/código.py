import argparse
import csv
import json
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


URL = "https://www.scrapethissite.com/pages/ajax-javascript/"
CAMPOS = ["ano", "titulo", "indicacoes", "premios", "melhor_filme"]


class AnosParser(HTMLParser):
    """Identifica os anos nos links da página, sem fixar uma lista no código."""

    def __init__(self):
        super().__init__()
        self.anos = set()

    def handle_starttag(self, tag, attrs):
        atributos = dict(attrs)
        if tag == "a" and "year-link" in atributos.get("class", "").split():
            ano = atributos.get("id", "")
            if ano.isdigit():
                self.anos.add(int(ano))


def baixar(url):
    """Faz uma requisição com limite de tempo e até três tentativas."""
    requisicao = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for tentativa in range(3):
        try:
            with urlopen(requisicao, timeout=30) as resposta:
                return resposta.read().decode("utf-8")
        except HTTPError as erro:
            if erro.code not in (429, 500, 502, 503, 504) or tentativa == 2:
                raise
        except (URLError, TimeoutError):
            if tentativa == 2:
                raise
        time.sleep(2 ** tentativa)


def coletar_filmes():
    parser = AnosParser()
    parser.feed(baixar(URL))
    if not parser.anos:
        raise ValueError("Nenhum ano encontrado. Verifique se a página mudou.")

    registros = []
    for ano in sorted(parser.anos, reverse=True):
        # Mesmos parâmetros usados pelo JavaScript para preencher a tabela.
        parametros = urlencode({"ajax": "true", "year": ano})
        filmes = json.loads(baixar(f"{URL}?{parametros}"))
        if not isinstance(filmes, list) or not filmes:
            raise ValueError(f"Resposta inesperada ou vazia para o ano {ano}.")
        for filme in filmes:
            if int(filme["year"]) != ano:
                raise ValueError(f"Ano inconsistente na resposta de {ano}.")
            registros.append({
                "ano": ano,
                "titulo": filme["title"].strip(),
                "indicacoes": int(filme["nominations"]),
                "premios": int(filme["awards"]),
                # A API omite este campo quando o filme não venceu Melhor Filme.
                "melhor_filme": bool(filme.get("best_picture", False)),
            })
        print(f"{ano}: {len(filmes)} filmes")
        time.sleep(0.3)
    return registros


def salvar(registros, pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    with (pasta / "filmes_oscar.csv").open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS, delimiter=";")
        escritor.writeheader()
        escritor.writerows(registros)

def main():
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("--saida", type=Path, default=Path(__file__).resolve().parent,
                            help="Pasta para salvar o CSV(padrão: pasta do script).")
    opcoes = argumentos.parse_args()
    try:
        registros = coletar_filmes()
        salvar(registros, opcoes.saida)
    except (URLError, TimeoutError, ValueError, KeyError, TypeError, OSError) as erro:
        argumentos.exit(1, f"Falha na coleta ou gravação: {erro}\n")
    print(f"Total: {len(registros)} filmes. Arquivos salvos em {opcoes.saida.resolve()}")


if __name__ == "__main__":
    main()
