import requests
from pathlib import Path

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"
RAW_DATA_DIR = Path("data/raw")


def create_dirs():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def test_connection():
    print("Testando conexão com a ANS...")
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()
    print("Conexão OK ✅")


if __name__ == "__main__":
    create_dirs()
    test_connection()
