import os
import pathlib
import requests
from dotenv import load_dotenv
import re

# Carregar variáveis do .env
load_dotenv()
BASE_URL='http://10.238.75.216/api'

USERNAME = os.getenv('API_USERNAME', 'username')
PASSWORD = os.getenv('API_PASSWORD', 'senha')
LOG_FOLDER = os.getenv('LOG_FOLDER')

TOKEN_URL = f"{BASE_URL}/token/"

# Função para obter o token de acesso
def get_access_token(username, password):
    print(username)
    print(password)
    print(TOKEN_URL)
    response = requests.post(TOKEN_URL, data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("access")
    else:
        raise Exception("Falha na autenticação")

# Função para definir o diretório
def set_directory(token, folder_path):
    url = f"{BASE_URL}/set_folder/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"folder": folder_path}
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        print("Diretório definido com sucesso.")
    else:
        print(f"Falha ao definir o diretório. Erro: {response.json()}")

# Função para baixar o arquivo de log
def download_log(token, file_path):
    url = f"{BASE_URL}/download_log/"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Arquivo de log baixado com sucesso.")
        return file_path
    else:
        print(f"Falha ao baixar o arquivo de log. Erro: {response.json()}")
        return None

def rename_log_file(file_path):
    date_pattern = re.compile(r'\[(\d{2})/(\w{3})/(\d{4}):')
    month_map = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                 "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    with open(file_path, 'r') as f:
        first_line = f.readline()
        print(first_line)
    
    match = date_pattern.search(first_line)
    if match:
        day, month_str, year = match.groups()
        month = month_map[month_str]
        new_file_name = f"{year}{month}{day}-log"
        new_file_path = file_path.with_name(new_file_name)
        os.rename(file_path, new_file_path)
        print(f"Arquivo renomeado para: {new_file_path}")
    else:
        print("Data não encontrada na primeira linha do arquivo de log.")


# Exemplo de uso
if __name__ == "__main__":
    folder_path = "/var/log/nginx"  # Altere para o caminho do diretório desejado
    path = pathlib.Path(r'//10.238.112.42/SEPLAG/arquivos_compartilhados/IGPE/log_pfc/access.log.1')
    output_file = path
    # output_file = r'//192.168.4.32/SEPLAG/NCD/access.log.1'  # Nome do arquivo para salvar o log baixado
    
    try:
        token = get_access_token(USERNAME, PASSWORD)
        # set_directory(token, folder_path)
        downloaded_file_path = download_log(token, output_file)
        if downloaded_file_path:
            print("ENTROU")
            rename_log_file(downloaded_file_path)

    except Exception as e:
        print(f"Erro: {e}")