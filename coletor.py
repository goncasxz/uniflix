import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def coletar_dados():
    print("\n --- BEM-VINDO AO CADASTRO DO UNIFLIX --- \n")

    nome = input("Nome Completo: ")
    email = input("E-mail: ")
    data_nasc_str = input("Data de Nascimento (DD/MM/AAAA): ")
    cidade_estado = input("Cidade/Estado (Ex: Sorocaba/SP): ")
    genero = input("Gênero Cinematográfico Favorito (Opcional): ")

    if "@" not in email or len(nome) < 2:
        print("Erro: Dados inválidos. Verifique o nome ou e-mail informado.")
        return

    try:
        data_nascimento = datetime.strptime(data_nasc_str, "%d/%m/%Y")
    except ValueError:
        print("Erro: Formato de data inválido. Use DD/MM/AAAA.")
        return

    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')
        db = client["sample_mflix"]
        colecao = db["novos_usuarios"]

        novo_usuario = {
            "nome": nome.strip().title(),
            "email": email.strip().lower(),
            "data_nascimento": data_nascimento,
            "cidade_estado": cidade_estado.strip(),
            "genero_favorito": genero.strip().title() if genero else None,
            "data_cadastro": datetime.now()
        }

        resultado = colecao.insert_one(novo_usuario)
        print(f"\nSucesso! Usuário salvo no MongoDB com o _id: {resultado.inserted_id}")

    except ConnectionFailure:
        print("Erro: Falha ao conectar ao banco de dados.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        # Fechando a conexão
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    coletar_dados()