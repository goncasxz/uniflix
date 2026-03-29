import os
import re
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def obter_nome():
    while True:
        nome = input("Nome Completo: ").strip().title()
        if len(nome) >= 2:
            return nome
        print("Nome muito curto. Por favor, insira um nome válido.")

def obter_email():
    while True:
        email = input("E-mail: ").strip().lower()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        print("E-mail inválido. Certifique-se de usar o formato correto (ex: nome@email.com).")

def obter_data_nascimento():
    while True:
        data_str = input("Data de Nascimento (DD/MM/AAAA): ").strip()
        try:
            data_nascimento = datetime.strptime(data_str, "%d/%m/%Y")
            if(data_nascimento > datetime.now()):
                print("Data de nascimento não pode ser no futuro. Por favor, insira uma data válida.")
                continue
            return data_nascimento
        except ValueError:
            print("Formato de data inválido. Use exatamente DD/MM/AAAA (ex: 15/05/1990).")

def coletar_dados():
    print("\n--- BEM-VINDO AO CADASTRO DO CINE-HORÓSCOPO UNIFLIX --- \n")

    print("Conectando ao banco de dados...")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("Conexão estabelecida com sucesso!\n")
    except ConnectionFailure:
        print("Erro: Falha ao conectar ao MongoDB. Verifique sua internet e a variável MONGO_URI.")
        return
    except Exception as e:
        print(f"Ocorreu um erro inesperado na conexão: {e}")
        return

    try:
        nome = obter_nome()
        email = obter_email()
        data_nascimento = obter_data_nascimento()
        cidade_pais = input("Cidade, País (Ex: Votorantim, BR): ").strip()
        genero = input("Gênero Cinematográfico Favorito (Opcional): ").strip().title()
        dia_mes_aniversario = data_nascimento.strftime("%d-%m")

        db = client["sample_mflix"]
        colecao = db["novos_usuarios"]

        novo_usuario = {
            "nome": nome,
            "email": email,
            "data_nascimento": data_nascimento,
            "dia_mes_aniversario": dia_mes_aniversario,
            "cidade_pais": cidade_pais,
            "genero_favorito": genero if genero else None,
            "data_cadastro": datetime.now()
        }

        resultado = colecao.insert_one(novo_usuario)
        print(f"\nSucesso! Usuário salvo no MongoDB com o _id: {resultado.inserted_id}")

    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante o cadastro: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    coletar_dados()