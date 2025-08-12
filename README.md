🎯 Analisador de Grid para Corridas

Este projeto é uma aplicação web desenvolvida com Streamlit para analisar dados de grids de corrida, focando na identificação de padrões sequenciais específicos, denominados P1 e P2. A ferramenta oferece uma interface visual e interativa para colar dados brutos de corridas e receber uma análise detalhada e estilizada em tempo real.

✨ Funcionalidades Principais

Análise Contínua de Corridas: Identifica a relação entre corridas consecutivas para encontrar padrões.

Detecção de Padrões P1 e P2: Lógica customizada para marcar ocorrências onde o vencedor da corrida atual tem uma relação específica com os pilotos da corrida anterior.

P1: O vencedor da corrida atual chegou em 1º ou 4º na corrida anterior.

P2: O vencedor da corrida atual chegou em 2º ou 3º na corrida anterior.

Dashboard Interativo: Apresenta os resultados em uma tabela principal com códigos de cores e tooltips que explicam cada padrão encontrado.

Resumo Geral: Métricas e gráficos que resumem a contagem total de padrões P1 e P2.

Análise de Sequências: Uma tabela dedicada que mostra apenas as sequências de padrões P1 e P2 consecutivos, ajudando a visualizar tendências.

Modo de Depuração: Uma visão detalhada da lógica de análise, mostrando a relação entre corridas anteriores e atuais para validar os resultados.

Interface Moderna: UI limpa e responsiva, com suporte a temas claro e escuro, para uma melhor experiência do usuário.

🛠️ Tecnologias Utilizadas

Python: Linguagem de programação principal.

Streamlit: Framework utilizado para construir a interface web interativa.

Pandas: Biblioteca para manipulação e análise dos dados em formato de DataFrame.


Site para teste: https://speedwayrun.streamlit.app/

Tabela para copiar e colar para teste :

H	1	4	7	10	13	16	19	22	25	28	31	34	37	40	43	46	49	52	55	58	

4	2-4	1-3	2-1	4-2	1-4	1-3	2-4	4-3	4-1	2-4	2-4	3-1	4-1								

3	4-3	1-4	4-1	4-1	3-2	2-3	4-1	1-4	2-3	1-3	2-1	3-2	1-3	1-3	2-4	2-3	4-2	4-2	1-3	4-3	2

2	1-2	2-1	3-4	2-3	3-2	3-4	2-4	3-4	1-3	1-4	2-1	2-3	2-4	4-2	1-4	4-1	2-4	4-3	4-1	2-4	6

1	1-4	2-1	2-1	1-3	4-3	4-2	2-4	3-2	1-4	2-4	1-2	2-4	3-1	2-3	2-3	2-3	3-2	1-4	4-3	4-1	8

0	3-4	2-1	3-1	3-1	2-3	3-1	1-4	2-1	1-3	2-1	2-1	3-1	1-2	2-1	4-3	4-2	4-2	1-4	1-3	2-3	4

23	3-4	3-1	2-1	4-3	4-2	3-1	3-4	1-4	1-2	4-2	2-4	4-2	4-1	3-4	1-3	2-1	3-4	1-4	1-4	2-1	4
