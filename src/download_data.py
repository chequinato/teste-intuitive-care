
from datetime import datetime
from pathlib import Path
import requests
import logging
import sys


BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/IAP/"
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = Path("data/download_log.txt")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}



def quarter_generator(start_year, start_quarter):
    year = start_year
    quarter = start_quarter
    while year >= 2016:
        yield year, quarter
        quarter -= 1
        if quarter == 0:
            quarter = 4
            year -= 1



def download_file(url, dest):
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            stream=True,
            timeout=60,
            allow_redirects=True
        )
        return r.status_code == 200, r.status_code, r
    except Exception as e:
        logging.error(f"Erro ao tentar baixar {url}: {e}")
        return False, None, None



if __name__ == "__main__":
    now = datetime.now()
    current_quarter = (now.month - 1) // 3 + 1
    downloaded = 0
    tentativas = []

    logging.info("Buscando últimos 3 arquivos disponíveis...")

    # Padrões de diretório a tentar: raiz e subpasta por ano/trimestre
    def url_patterns(year, quarter):
        qt = f"{quarter}T"
        patterns = [
            f"{year}_{qt}_IAP.zip",  # padrão raiz
            f"{year}/{qt}/{year}_{qt}_IAP.zip",  # subdiretório ano/trimestre
            f"{year}/{qt}/IAP_{year}_{qt}.zip",  # variação nome
        ]
        return [BASE_URL + p for p in patterns]

    for year, quarter in quarter_generator(now.year, current_quarter):
        found = False
        for url in url_patterns(year, quarter):
            filename = url.split("/")[-1]
            filepath = RAW_DIR / filename
            logging.info(f"Tentando {url} ...")
            ok, status, response = download_file(url, filepath)
            tentativas.append({"url": url, "status": status})
            if ok:
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                logging.info(f"✅ Baixado com sucesso: {filename}")
                downloaded += 1
                found = True
                break
            else:
                logging.info(f"⛔ Indisponível (status {status})")
        if downloaded == 3:
            break

    if downloaded == 0:
        logging.warning("⚠️ Nenhum arquivo disponível foi encontrado.")
    else:
        logging.info(f"🎉 Download concluído ({downloaded} arquivos).")

    # Salva tentativas em arquivo para documentação
    import json
    with open("data/tentativas_download.json", "w", encoding="utf-8") as f:
        json.dump(tentativas, f, ensure_ascii=False, indent=2)
