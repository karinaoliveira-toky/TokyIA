import re
import os
import time
from typing import List, Dict, Any
from pypdf import PdfReader
from google import genai
from google.genai import types

from app.core.security import SYSTEM_PROMPT
from app.core.config import settings

# Esquema de Metadados do Banco de Dados para orientar a geração de SQL
METADATAS_BANCO = """
Você tem acesso ao SQL Warehouse do Databricks com o catálogo 'tokstok' e os seguintes esquemas e tabelas:

1. Tabela de Vendas: `tokstok.quicksight.view_tokstok_vendas`
   - `data_venda` (DATE) - Data da venda.
   - `cod_filial` (INT) - Código da filial/loja.
   - `cod_produto` (INT) - Código do produto (SKU).
   - `gmv` (DOUBLE) - Volume Geral de Vendas (Faturamento bruto em reais).
   - `qtd_itens` (INT) - Quantidade de itens vendidos.
   - `canal` (STRING) - Canal de venda ('Digital' ou 'Loja Física').

2. Tabela de Estoque: `tokstok.quicksight.view_tokstok_estoque`
   - `data_referencia` (DATE) - Data do snapshot de estoque.
   - `cod_filial` (INT) - Código do Centro de Distribuição (CD) ou filial.
   - `cod_produto` (INT) - Código do produto (SKU).
   - `qtd_estoque` (INT) - Quantidade em estoque física.
   - `qtd_ruptura` (INT) - Quantidade de itens em falta/ruptura (valores > 0 indicam que há itens faltantes no estoque).

3. Tabela de Dimensão de Produto: `tokstok.quicksight.view_tokstok_dim_produto`
   - `cod_produto` (INT) - Código único do SKU.
   - `nome_produto` (STRING) - Nome ou descrição do produto.
   - `categoria` (STRING) - Categoria comercial (ex: 'Móveis', 'Decoração', 'Organização').

4. Tabela de Dimensão de Filial: `tokstok.quicksight.view_tokstok_dim_filial`
   - `cod_filial` (INT) - Código único da filial/loja.
   - `nome_filial` (STRING) - Nome da loja (ex: 'Extrema', 'Lar Center').
   - `regiao` (STRING) - Região geográfica ('Sul', 'Sudeste', 'Norte', 'Nordeste', 'Centro-Oeste').

5. Tabela de Metas: `tokstok.metas.venda_metas_bot`
   - `ano` (INT) - Ano da meta.
   - `mes` (INT) - Mês da meta.
   - `meta_gmv` (DOUBLE) - Meta de faturamento bruto (GMV) projetada em reais.
   - `marca` (STRING) - Marca ('Tok&Stok', 'Mobly', 'Guldi' ou 'Grupo Toky').

6. Tabela de Entregas e Logística: `tokstok.operations.shipment_delivery`
   - `order_id` (STRING) - ID único do pedido de venda.
   - `cod_filial` (INT) - Código da filial/loja de origem.
   - `sla_dias` (INT) - Prazo de entrega prometido em dias.
   - `tempo_entrega_dias` (INT) - Tempo real gasto na entrega em dias.
   - `status_entrega` (STRING) - Status da entrega ('Entregue', 'Pendente', 'Atrasado').
   - `custo_frete` (DOUBLE) - Custo unitário de frete do pedido.

7. Tabela de Cadeia de Suprimentos: `tokstok.supply.supply_chain`
   - `fornecedor_id` (INT) - ID único do fornecedor.
   - `nome_fornecedor` (STRING) - Razão social ou nome do fornecedor.
   - `item_atrasado` (INT) - Quantidade de itens em atraso de entrega deste fornecedor.
   - `sla_atendimento_dias` (INT) - Prazo contratual de atendimento em dias.

8. Tabela de Mensagens e Atendimento Weni (Tok&Stok): `cdc.tb_weni_mensagens_humanas_tokstok`
   - `mensagem_uuid` (STRING) - ID único da mensagem.
   - `room_uuid` (STRING) - ID da sala da conversa / chamado na plataforma Weni.
   - `telefone` (STRING) - Número de telefone do remetente / cliente.
   - `texto_mensagem` (STRING) - Texto e conteúdo completo da mensagem enviada.
   - `quem_enviou` (STRING) - Identifica o tipo de remetente da mensagem. Possui três categorias:
       * E-mail com domínio `@tokstok.com.br` (ex: `joao.silva@tokstok.com.br`) → mensagem enviada por um **ATENDENTE HUMANO** da Tok&Stok após derivação/transbordo.
       * Valor literal `IA de Atendimento` → mensagem enviada pela **IA de Atendimento** da plataforma Weni.
       * Apenas um nome (ex: `Maria`, `Carlos`) → mensagem enviada pelo **CLIENTE**.
   - `data_mensagem` (STRING) - Data e horário do envio da mensagem.

Diretrizes de geração de SQL:
- Use sempre nomes qualificados de tabelas (ex: `tokstok.quicksight.view_tokstok_vendas` ou `cdc.tb_weni_mensagens_humanas_tokstok`).
- Use JOINs adequados se a pergunta exigir junção de tabelas (ex: juntar dim_produto ou dim_filial para filtrar por categoria ou região).
- As consultas devem ser de leitura estrita (`SELECT`).
- Limite as consultas a no máximo 100 resultados (`LIMIT 100`).
- Faça consultas eficientes e seguras compatíveis com a sintaxe ANSI SQL do Databricks.
- ATENÇÃO (Dicionário de Dados): Siga rigorosamente as instruções de uso para cada tabela abaixo:

Instruções de Navegação e Uso de Cada Tabela:
1. databases_tmp.cdc_tickets_cs e cdc_tickets_cs_tokstok (Tickets)
Quando usar: Utilize para aceder ao "cabeçalho" do chamado de Customer Service. Aqui encontrará quem é o cliente (Nome, Email, CPF/CNPJ), o número do protocolo, a data de abertura e a qual número de pedido (ORDER_NUMBER) e item (ITEM_ID) a reclamação se refere. Nota: Cada linha é a combinação única de Ticket + Item.

2. databases_tmp.cdc_tasks_cs_new e cdc_tasks_cs_tokstok (Tasks)
Quando usar: Utilize para analisar as ações e o "funil" de atendimento dentro do ticket. Aqui encontrará qual assistente operou a tarefa, para qual fila/equipe foi direcionada e os campos preenchidos na tela do sistema (em formato JSON). Nota: Tem a restrição de apenas 1 item por ticket.

3. mos.orders.orders (Pedidos MOS)
Quando usar: É a tabela principal de transações. Utilize para encontrar o valor total pago, e a origem ou tipo de fluxo do pedido (venda comum, logística reversa ou assistência técnica - AST). A chave cod cruza com o ORDER_NUMBER do Customer Service.

4. mos.orders.orderitems (Itens do Pedido MOS)
Quando usar: Utilize para detalhar os produtos (SKUs) comprados dentro de um pedido. Mostra o preço unitário e o valor do frete do item. A chave cod cruza com o ITEM_ID do Customer Service.

5. mos.orders.orderitemstatuses (Status do Item MOS)
Quando usar: Utilize para consultar a linha do tempo sistémica do pedido. Contém o histórico completo de transição de status (ex: faturado, em trânsito, entregue) de cada item.

6. mos.orders.orderitemdisplacements (Rastreio / Tracking MOS)
Quando usar: Utilize para acompanhar a movimentação física da mercadoria. Indica qual foi o Centro de Distribuição (CD) de origem e qual a transportadora responsável por aquele trecho.

7. nexthub.core.deliveries (Notas Fiscais de Entrega)
Quando usar: Utilize para encontrar os dados de faturação e expedição. Contém a chave de 44 dígitos da DANFE e os dados fiscais de envio da mercadoria para o cliente.

8. nexthub.core.reverses (Notas Fiscais de Logística Reversa)
Quando usar: Utilize exclusivamente para fluxos de devolução ou recolha. Contém os dados das notas fiscais emitidas para que o produto regresse ao armazém.

9. oracle.gc.t_relaciona_pedido_oms_mos (Tabela De-Para GC x MOS)
Quando usar: MUITO IMPORTANTE. Utilize SEMPRE como ponte de ligação quando precisar de cruzar dados do sistema novo (MOS) com o ERP antigo da Tok&Stok (GC). O campo id_prod_mos traduz o ID do item entre os dois mundos.

10. dbt_prod.dbt_prod_gc.gc_pessoa (Cadastro de Pessoas Tok&Stok)
Quando usar: Utilize para aceder ao registo mestre de clientes, fornecedores e filiais do ecossistema Tok&Stok.

11. dbt_prod.dbt_prod_gc.gc_tok_grupo_entrega (Agrupamento TGE Tok&Stok)
Quando usar: Utilize para entender a lógica de expedição da Tok&Stok. O "TGE" agrupa os itens de um pedido que vão sair juntos no mesmo transporte.

12. dbt_prod.dbt_prod_gc.gc_tok_grupo_entrega_item (Itens do Agrupamento TGE)
Quando usar: Utilize para listar fisicamente quais os produtos que estão dentro de cada lote/agrupamento de entrega (TGE) específico.

13. dbt_prod.dbt_prod_gc.gc_item_ped_venda (Vendas Tok&Stok)
Quando usar: Utilize para identificar os SKUs (id_prod) transacionados com base no Agrupamento de Entrega (TGE), data e filial expedidora.

14. dbt_prod.dbt_prod_gc.gc_audit_item_ped_venda (Auditoria de Vendas Tok&Stok)
Quando usar: Utilize para consultar o histórico de alterações (log) de um pedido de venda no ERP. É útil para ver se uma data de entrega foi reagendada ou se um campo foi alterado manualmente.

15. dbt_prod.dbt_prod_mart_trgt_nfe.targ_mv_nf_saida (Notas Fiscais de Saída Tok&Stok)
Quando usar: Utilize para consultar as notas fiscais emitidas no ERP legado. É essencial para fluxos de Assistência Técnica (AST) cruzando com mos.orders.orders.

16. dbt_prod.dbt_prod_gc.gc_tok_status_grupo_entrega (Histórico de Status TGE)
Quando usar: Utilize para rastrear as atualizações e fases pelas quais um Agrupamento de Entrega (TGE) da Tok&Stok já passou.

17. dbt_prod.dbt_prod_gc.gc_tok_tipo_status_grupo_entrega (Dicionário de Status TGE)
Quando usar: Utilize como tabela de apoio (dimensão) para descrever as regras de negócio de cada status logístico do TGE (ex: "Aguardando Separação").

18. cdc.tb_weni_mensagens_humanas_tokstok (Mensagens de Atendimento Weni - IA, Clientes e Atendentes Derivados)
Quando usar: Utilize para analisar todas as mensagens trocadas entre clientes, a IA de atendimento na plataforma Weni para a Tok&Stok e o atendente humano que assumiu o contato após a derivação/transbordo.

Regras de negócio do campo `quem_enviou` (CRÍTICO — use SEMPRE estas regras para segmentar análises):
- **Atendente humano**: quando `quem_enviou` contiver `@tokstok.com.br` → use o filtro: `quem_enviou LIKE '%@tokstok.com.br%'`
- **IA de Atendimento**: quando `quem_enviou = 'IA de Atendimento'` → use o filtro: `quem_enviou = 'IA de Atendimento'`
- **Cliente**: quando `quem_enviou` NÃO contiver `@tokstok.com.br` E NÃO for `'IA de Atendimento'` → use o filtro: `quem_enviou != 'IA de Atendimento' AND quem_enviou NOT LIKE '%@tokstok.com.br%'`

Exemplos de análises possíveis:
- Volume de mensagens por tipo de remetente (cliente vs IA vs atendente)
- Quais atendentes mais responderam (agrupando por `quem_enviou` com filtro `@tokstok.com.br`)
- Salas de conversa (`room_uuid`) onde houve transbordo (onde aparecem mensagens de `@tokstok.com.br`)
- Tempo de atendimento comparando data da primeira mensagem do cliente vs primeira resposta do atendente
- Clientes que mais enviaram mensagens (agrupando por `telefone`)

ATENÇÃO IMPORTANTE DE SCHEMA PARA WENI:
A tabela `cdc.tb_weni_mensagens_humanas_tokstok` pertence EXCLUSIVAMENTE ao schema `cdc` (o nome exato da tabela no SQL do Databricks é `cdc.tb_weni_mensagens_humanas_tokstok`).
Ela NÃO pertence ao schema `databases_tmp`. Sempre que for consultada, utilize o nome completo `cdc.tb_weni_mensagens_humanas_tokstok`.
"""

class AIService:
    _client = None
    _pdf_context = None

    @classmethod
    def _carregar_dicionario(cls) -> str:
        if cls._pdf_context is not None:
            return cls._pdf_context
            
        pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "plaintext", "System Prompt - Dicionário Databricks.pdf"))
        
        pdf_texto = ""
        try:
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                texto = []
                for page in reader.pages:
                    texto.append(page.extract_text() or "")
                pdf_texto = "\n".join(texto)
                print("[INFO] Dicionário PDF carregado com sucesso.")
        except Exception as e:
            print(f"[ERRO PDF] Falha ao carregar dicionário PDF: {e}.")
            
        # Combina os metadados cadastrados com o PDF para garantir todas as tabelas novas
        cls._pdf_context = f"{METADATAS_BANCO}\n\n{pdf_texto}".strip()
        return cls._pdf_context

    @classmethod
    def _get_client(cls) -> genai.Client:
        if cls._client is None:
            cls._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return cls._client

    @classmethod
    def _chamar_api_com_retry(cls, model: str, contents: str, config: types.GenerateContentConfig, max_tentativas: int = 3) -> str:
        """
        Chama a API Gemini com retry automático e backoff exponencial.
        Trata erros de sobrecarga (429/ResourceExhausted) automaticamente.
        """
        client = cls._get_client()
        for tentativa in range(1, max_tentativas + 1):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )
                return response.text
            except Exception as e:
                erro_str = str(e).lower()
                eh_sobrecarga = any(k in erro_str for k in ["429", "overloaded", "resource_exhausted", "resourceexhausted", "quota"])
                if eh_sobrecarga and tentativa < max_tentativas:
                    espera = 2 ** tentativa  # 2s, 4s, 8s...
                    print(f"[RETRY] API sobrecarregada. Tentativa {tentativa}/{max_tentativas}. Aguardando {espera}s...")
                    time.sleep(espera)
                else:
                    raise
        raise RuntimeError("Número máximo de tentativas excedido.")

    @classmethod
    def gerar_sql(cls, mensagem: str) -> str:
        """
        Interpreta o prompt do usuário e gera uma consulta SQL segura e válida,
        ou retorna um erro de validação de coluna.
        """
        contexto_banco = cls._carregar_dicionario()
        
        prompt = f"""
Você é um especialista em engenharia de dados e SQL do Databricks.
Sua única tarefa é ler a pergunta do usuário e gerar uma consulta SQL válida (dialeto Databricks/Spark SQL) para responder a ela, com base no Dicionário Databricks fornecido.

{contexto_banco}

**Instruções de Validação de Coluna**:
Se a pergunta do usuário referenciar uma tabela do dicionário, mas solicitar ou fizer menção a uma coluna que NÃO está descrita na respectiva tabela do Dicionário, você NÃO deve gerar SQL, nem tentar adivinhar ou chutar nomes de colunas. Em vez disso, você deve retornar exatamente a seguinte string e parar:
ERRO_COLUNA_INEXISTENTE: [Liste aqui, separadas por vírgula, todas as colunas corretas disponíveis na tabela referenciada para ajudar o usuário]

**Instruções de Saída (se as colunas existirem)**:
- Retorne APENAS a query SQL.
- Não adicione textos explicativos, nem blocos de markdown adicionais (como ```sql ou ```). Retorne o texto puro da consulta SQL diretamente.
- A consulta SQL gerada deve ser estritamente de leitura (SELECT, WITH, SHOW SCHEMAS ou SHOW TABLES).

Pergunta do usuário:
"{mensagem}"
"""
        
        texto = cls._chamar_api_com_retry(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,  # Baixa temperatura para manter a precisão do SQL
            )
        )
        
        # Limpa qualquer formatação markdown acidental que o modelo possa ter colocado
        sql_query = texto.strip()
        sql_query = re.sub(r"^```sql\s*", "", sql_query, flags=re.IGNORECASE)
        sql_query = re.sub(r"^```\s*", "", sql_query)
        sql_query = re.sub(r"```$", "", sql_query)
        
        return sql_query.strip()

    @classmethod
    def gerar_resposta_final(cls, mensagem: str, sql_query: str, resultados: List[Dict[str, Any]]) -> str:
        """
        Gera uma resposta executiva (estilo Chief of Staff) integrando os dados reais retornados do banco.
        """
        client = cls._get_client()
        dicionario_banco = cls._carregar_dicionario()
        
        # Formata os registros retornados para passar como contexto de texto
        contexto_dados = ""
        if not resultados:
            contexto_dados = "Nenhum resultado foi retornado pelo banco de dados para esta consulta."
        else:
            contexto_dados = "Registros encontrados no Databricks:\n"
            for i, r in enumerate(resultados):
                contexto_dados += f"Registro #{i+1}: {r}\n"
                
        prompt = f"""
Você é a TokyIA, assistente estratégica de nível Chefe de Gabinete (Chief of Staff) do Grupo Toky.
Escreva uma resposta analítica e de alto nível para o Diretor baseando-se estritamente nas informações do Dicionário Databricks e nos dados reais extraídos abaixo.

Dicionário de Bases e Tabelas Mapeadas:
{dicionario_banco}

Pergunta do Diretor:
"{mensagem}"

Consulta SQL Executada no Databricks:
```sql
{sql_query}
```

Dados reais retornados do Banco de Dados:
{contexto_dados}

Instruções de Comportamento:
- Seja direta, executiva e utilize o estilo BLUF (Bottom Line Up Front).
- Se o Diretor perguntar quais bases, tabelas ou esquemas você tem acesso, liste com clareza todas as tabelas e visões mapeadas no catálogo `tokstok` e seus respectivos escopos (Vendas, Estoque, Dimensão Produto, Dimensão Filial, Metas, Logística/Shipment e Suprimentos).
- Baseie as suas métricas e números estritamente nos dados reais retornados. Não alucine e não crie dados que não estão nos resultados.
- Se a consulta SQL não retornou dados ou deu erro (e a pergunta não for sobre listagem de bases), admita com transparência ("Muro de Vidro") que não foi possível encontrar os dados na base e sugira refinar a busca.
"""
        
        texto = cls._chamar_api_com_retry(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
            )
        )
        
        return texto
