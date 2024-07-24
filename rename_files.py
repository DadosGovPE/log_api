import os
import pathlib
import re

# Função para extrair a data da primeira linha do arquivo de log e renomear o arquivo
def rename_log_file(file_path):
    date_pattern = re.compile(r'\[(\d{2})/(\w{3})/(\d{4}):')
    month_map = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                 "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    with open(file_path, 'r') as f:
        first_line = f.readline()
    
    match = date_pattern.search(first_line)
    if match:
        day, month_str, year = match.groups()
        month = month_map[month_str]
        new_file_name = f"{year}{month}{day}-log"
        new_file_path = file_path.with_name(new_file_name)
        os.rename(file_path, new_file_path)
        print(f"Arquivo renomeado para: {new_file_path}")
    else:
        print(f"Data não encontrada na primeira linha do arquivo de log: {file_path}")

# Função para processar todos os arquivos na pasta especificada
def rename_all_logs_in_directory(directory_path):
    path = pathlib.Path(directory_path)
    log_files = path.glob('access*')  # Assumindo que todos os arquivos começam com 'access'
    
    for log_file in log_files:
        rename_log_file(log_file)

# Exemplo de uso
if __name__ == "__main__":
    directory_path = r'\\10.238.112.42\SEPLAG\arquivos_compartilhados\IGPE\log_pfc'  # Altere para o caminho do diretório desejado
    
    try:
        rename_all_logs_in_directory(directory_path)
    except Exception as e:
        print(f"Erro: {e}")
