# TokyIA — Inteligência Corporativa Grupo Toky

Este projeto é um assistente estratégico de alto nível (Chefe de Gabinete) desenvolvido para o **Grupo Toky**, integrando dados e operações da **Tok&Stok**, **Mobly** e **Guldi**. 

O sistema utiliza uma arquitetura **Text-to-SQL** conectada diretamente ao **Databricks SQL Warehouse** (Catálogo `tokstok`) para obter métricas de negócios em tempo real e responder a perguntas complexas de faturamento, estoque, logística e suprimentos via inteligência artificial (Google Gemini).

---

## 🏗️ Estrutura do Projeto

O repositório está dividido em duas partes principais: **Backend** (API) e **Frontend** (Interface do Usuário).

### 📂 [Backend](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend) (FastAPI)
Localizado no diretório `/backend`, é o motor de processamento e inteligência.

*   **[app/api/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/app/api/)**: Contém os endpoints da API (ex: `/chat`, `/status`, `/logs`).
*   **[app/core/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/app/core/)**: Configurações globais, segurança e filtros de diretrizes corporativas.
*   **[app/models/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/app/models/)**: Modelos e esquemas de dados (Pydantic).
*   **[app/services/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/app/services/)**: Lógica de negócio, incluindo a geração de queries SQL via Gemini (`gemini-2.5-flash`), execução de queries no Databricks e formatação da resposta executiva final.
*   **[main.py](file:///c:/Users/karina.oliveira/Desktop/TokyAI/backend/main.py)**: Ponto de entrada da aplicação FastAPI.
*   **requirements.txt**: Dependências do Python (FastAPI, Google GenAI, etc).

### 📂 [Frontend](file:///c:/Users/karina.oliveira/Desktop/TokyAI/frontend) (Next.js)
Interface moderna, rápida e responsiva construída com Next.js 14 e TailwindCSS.

*   **[app/chat/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/frontend/app/chat/)**: Interface de chat com fluxo de mensagens e auditoria/visualização de query SQL executada.
*   **[app/painel/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/frontend/app/painel/)**: Painel de visualização e controle operacional.
*   **[public/](file:///c:/Users/karina.oliveira/Desktop/TokyAI/frontend/public/)**: Ativos estáticos (imagens, ícones e backgrounds premium).
*   **tailwind.config.ts**: Configurações do sistema de design (Cores corporativas, efeitos de vidro/glassmorphism).

---

## 💾 Tabelas Mapeadas (Databricks)

A TokyIA foi projetada para interagir com o catálogo `tokstok` e possui conhecimento do esquema das seguintes tabelas/views:

1.  **Vendas**: `tokstok.quicksight.view_tokstok_vendas` (data, filial, SKU, gmv/faturamento, itens, canal)
2.  **Estoque**: `tokstok.quicksight.view_tokstok_estoque` (data, filial, SKU, quantidade, rupturas)
3.  **Dimensão Produto**: `tokstok.quicksight.view_tokstok_dim_produto` (SKU, nome, categoria comercial)
4.  **Dimensão Filial**: `tokstok.quicksight.view_tokstok_dim_filial` (filial, nome da loja/CD, região)
5.  **Metas**: `tokstok.metas.venda_metas_bot` (ano, mês, meta gmv, marca/grupo)
6.  **Logística e Entregas**: `tokstok.operations.shipment_delivery` (order_id, filial, SLA prometido, tempo real gasto, status, custo de frete)
7.  **Suprimentos**: `tokstok.supply.supply_chain` (fornecedor, nome, itens em atraso, SLA contratual)
8.  **Atendimento Humano Weni**: `cdc.tb_weni_mensagens_humanas_tokstok` (mensagem_uuid, room_uuid, telefone, texto_mensagem, quem_enviou, data_mensagem)

---

## 🚀 Como Executar

### 1. Configuração do Backend
1. Navegue até a pasta `backend`:
   ```bash
   cd backend
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie e configure o arquivo `.env` com as credenciais necessárias:
   ```env
   GEMINI_API_KEY=sua_gemini_api_key
   RETRIEVAL_PROVIDER=databricks_sql
   DATABRICKS_HOST=https://seu-host-databricks.cloud.databricks.com/
   DATABRICKS_TOKEN=seu_token_databricks
   DATABRICKS_SQL_HTTP_PATH=caminho_http_warehouse
   ```
5. Inicie o servidor:
   ```bash
   python main.py
   ```
   A API estará disponível em `http://localhost:8000`. Acesse `http://localhost:8000/docs` para ver a documentação interativa das rotas.

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

A TokyIA opera sob diretrizes corporativas rígidas no pipeline de execução de dados:
- **Validação de SQL Seguro**: Apenas consultas de leitura estrita (`SELECT` e `WITH`) são permitidas. Qualquer tentativa de alteração de dados (`INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.) é bloqueada pelo backend.
- **Limitação de Resultados**: Consultas no Databricks são limitadas a no máximo 100 resultados para evitar lentidão e estouro de memória.
- **BLUF (Bottom Line Up Front)**: As respostas são construídas com uma abordagem de comunicação executiva, com a conclusão principal no início.
- **Muro de Vidro**: Não há alucinação de dados. Se os dados reais retornados forem nulos ou a query der erro, a IA reportará com transparência que não possui aquela informação.
- **Neutralidade**: Filtros internos barram solicitações fora do contexto corporativo do Grupo Toky, assuntos sensíveis, ou discussões de competidores que não constem nos dados.

---
*Desenvolvido para o Grupo Toky.*
