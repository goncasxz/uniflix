# 🎬 Cine-Horóscopo: Recomendador de Filmes Automatizado

## 📖 Sobre o Projeto
O Cine-Horóscopo é uma aplicação desenvolvida como projeto acadêmico para a disciplina de Banco de Dados NoSQL (UNISO). O sistema atua como um "horóscopo cinematográfico", coletando dados de novos usuários via terminal e acionando uma automação inteligente em nuvem que recomenda um filme baseado na exata data de aniversário do usuário (dia e mês), enviando o resultado final por e-mail com auxílio de IA.

## ⚙️ Arquitetura do Sistema
O projeto é dividido em dois grandes blocos que se comunicam via banco de dados:

* **1. Coletor de Dados (Python):** Um script interativo que roda no terminal, valida entradas de dados do usuário (nome, e-mail, data de nascimento) e salva o documento no MongoDB Atlas de forma segura.
* **2. Orquestrador (Make/n8n):** Uma automação orientada a eventos (Trigger) que escuta o banco de dados. Ao detectar um novo usuário, o orquestrador:
  * Extrai o dia e mês de nascimento.
  * Realiza uma query complexa (usando `$expr`) na coleção de filmes para encontrar uma obra lançada na mesma data, priorizando a maior nota do IMDB.
  * Consome APIs externas (Clima/IA).
  * Dispara um e-mail personalizado com a recomendação.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Banco de Dados:** MongoDB Atlas (NoSQL)
* **Bibliotecas Python:** `pymongo`, `python-dotenv`, `datetime`, `re`
* **Orquestração & Automação:** Make.com (antigo Integromat)

## 🚀 Como Executar Localmente

### Pré-requisitos
* Python instalado na máquina.
* Uma conta no MongoDB Atlas com um cluster configurado.
* As coleções `novos_usuarios` e `movies` (do dataset `sample_mflix`) disponíveis no cluster.

### Passos para Instalação

1. Clone este repositório:
   ```bash
   git clone [https://github.com/seu-usuario/exercicio_uniflix.git](https://github.com/seu-usuario/exercicio_uniflix.git)
   cd exercicio_uniflix
   ```
