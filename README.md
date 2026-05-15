# TokyIA — Inteligência Corporativa Grupo Toky

Este projeto é um assistente estratégico de alto nível (Chefe de Gabinete) desenvolvido para o **Grupo Toky**, integrando dados e operações da **Tok&Stok**, **Mobly** e **Guldi**. O sistema utiliza uma arquitetura RAG (Retrieval-Augmented Generation) para fornecer análises precisas, seguras e baseadas em dados internos.

## 🏗️ Estrutura do Projeto

O repositório está dividido em duas partes principais: **Backend** (API) e **Frontend** (Interface do Usuário).

### 📂 [Backend](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend) (FastAPI)
Localizado no diretório `/backend`, é o motor de processamento e inteligência.

*   **[app/api/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/app/api/)**: Contém os endpoints da API (ex: `/chat`).
*   **[app/core/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/app/core/)**: Configurações globais, variáveis de ambiente e segurança.
*   **[app/models/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/app/models/)**: Definições de esquemas Pydantic e modelos de dados.
*   **[app/services/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/app/services/)**: Lógica de negócio, incluindo a integração com o Google Gemini e o sistema RAG.
*   **[main.py](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/main.py)**: Ponto de entrada da aplicação FastAPI.
*   **requirements.txt**: Dependências do Python (FastAPI, Google GenAI, etc).

### 📂 [Frontend](file:///c:/Users/karina.oliveira/Desktop/TokyAI/frontend) (Next.js)
Interface moderna e responsiva construída com Next.js 14 e TailwindCSS.

*   **[app/chat/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/frontend/app/chat/)**: Interface principal de interação com a IA.
*   **[app/painel/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/frontend/app/painel/)**: Painel de visualização e controle.
*   **[public/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/frontend/public/)**: Ativos estáticos (imagens, ícones e backgrounds premium).
*   **tailwind.config.ts**: Configurações de design, incluindo o sistema de cores e efeitos de glassmorphism.

---

## 🚀 Como Executar

### 1. Configuração do Backend
1. Navegue até a pasta `backend`:
   ```bash
   cd backend
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado).
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente no arquivo `.env` (ex: `GOOGLE_API_KEY`).
5. Inicie o servidor:
   ```bash
   python main.py
   ```
   A API estará disponível em `http://localhost:8000`.

### 2. Configuração do Frontend
1. Navegue até a pasta `frontend`:
   ```bash
   cd frontend
   ```
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
   Acesse a aplicação em `http://localhost:3000`.

---

## 🛡️ Segurança e Diretrizes
A TokyIA opera sob diretrizes rigorosas:
- **BLUF (Bottom Line Up Front)**: Respostas diretas e executivas.
- **Muro de Vidro**: Não alucina; se a informação não estiver na base de dados, a IA informa que não possui o dado.
- **Neutralidade**: Foco exclusivo em operações corporativas, bloqueando temas sensíveis ou fora de escopo.

---
*Desenvolvido para o Grupo Toky.*
