import os
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

BASE_URL = os.getenv('BASE_URL', 'http://10.238.75.216/api')
USERNAME = os.getenv('API_USERNAME', 'username')
PASSWORD = os.getenv('API_PASSWORD', 'senha')
LOG_FOLDER = os.getenv('LOG_FOLDER')

TOKEN_URL = f"{BASE_URL}/token/"

# Função para obter o token de acesso
def get_access_token(username, password):
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
    else:
        print(f"Falha ao baixar o arquivo de log. Erro: {response.json()}")

# Exemplo de uso
if __name__ == "__main__":
    folder_path = "/var/log/nginx"  # Altere para o caminho do diretório desejado
    output_file = "access.log.1"  # Nome do arquivo para salvar o log baixado
    
    try:
        token = get_access_token(USERNAME, PASSWORD)
        # set_directory(token, folder_path)
        download_log(token, output_file)
    except Exception as e:
        print(f"Erro: {e}")