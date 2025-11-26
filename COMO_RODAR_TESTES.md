# Como Rodar os Testes de Carga e Gerar Gráficos

Este guia explica como executar os testes de carga para comparar a performance dos protocolos REST, GraphQL e SOAP.

## Pré-requisitos

1. Docker e Docker Compose instalados
2. Aplicação rodando com `docker-compose up -d --build`
3. Python 3 instalado (para gerar gráficos)

## Passo a Passo

### 1️⃣ Rodar os Testes de Carga

**Clique duas vezes no arquivo:**
```
1_rodar_testes.bat
```

**O que vai acontecer:**
- Testes para REST com 100, 1000, 10000 usuários
- Testes para GraphQL com 100, 1000, 10000 usuários
- Testes para SOAP com 100, 1000, 10000 usuários
- Cada teste dura 120 segundos
- **Tempo total: ~20-25 minutos**

**OU via linha de comando:**
```bash
cd teste-carga
./run_protocol_tests.sh
```

### 2️⃣ Gerar os Gráficos

**Após os testes terminarem, clique duas vezes no arquivo:**
```
2_gerar_graficos.bat
```

**O que vai acontecer:**
- Lê os resultados dos testes (arquivos CSV)
- Gera 8 gráficos comparativos
- Abre a pasta com os gráficos automaticamente

**OU via linha de comando:**
```bash
cd teste-carga
python generate_protocol_comparison.py
```

## 📊 Gráficos Gerados

Os gráficos serão salvos em: `teste-carga/reports/protocol_comparison/`

1. **avg_response_time_by_protocol.png**
   - Compara tempo médio de resposta entre REST, GraphQL e SOAP
   - Para cada carga (100, 1000, 10000 usuários)

2. **throughput_by_protocol.png**
   - Compara throughput (requisições/segundo) entre protocolos
   - Mostra qual protocolo aguenta mais carga

3. **p95_latency_by_protocol.png**
   - Compara latência do percentil 95
   - Útil para ver consistência de performance

4. **fastest_protocol_ranking.png**
   - Ranking mostrando qual protocolo foi mais rápido em cada cenário
   - Facilita identificar o vencedor

5. **endpoint_listar_musicas.png**
   - Comparação específica para o endpoint de listar músicas
   - Tempo de resposta e throughput

6. **endpoint_listar_usuarios.png**
   - Comparação específica para o endpoint de listar usuários
   - Tempo de resposta e throughput

7. **endpoint_playlists_de_usuario.png**
   - Comparação específica para o endpoint de playlists por usuário
   - Tempo de resposta e throughput

8. **summary_comparison_table.png**
   - Tabela resumo com todas as métricas
   - Fácil visualização de todos os dados

## 🎯 O que os Testes Fazem

Cada teste simula usuários concorrentes fazendo requisições para:

**Endpoints testados:**
- **Listar Músicas** (GET todas as músicas)
- **Listar Usuários** (GET todos os usuários)
- **Playlists de Usuário** (GET playlists de um usuário específico)

**Protocolos testados:**
- **REST**: `/api/musicas`, `/api/usuarios`, `/api/playlists/usuario/{id}`
- **GraphQL**: Queries `musicas`, `usuarios`, `playlistsPorUsuario`
- **SOAP**: Operações SOAP equivalentes

**Cargas testadas:**
- **100 usuários**: Carga leve
- **1000 usuários**: Carga média
- **10000 usuários**: Carga pesada

## 📁 Estrutura de Arquivos

```
teste-carga/
├── locustfile_rest.py          # Testes para REST
├── locustfile_graphql.py       # Testes para GraphQL
├── locustfile_soap.py          # Testes para SOAP
├── run_protocol_tests.sh       # Script que roda todos os testes
├── generate_protocol_comparison.py  # Script que gera gráficos
└── reports/
    ├── rest_100_users.html     # Relatório REST 100 usuários
    ├── rest_100_users_stats.csv
    ├── graphql_100_users.html
    ├── graphql_100_users_stats.csv
    ├── soap_100_users.html
    ├── soap_100_users_stats.csv
    └── protocol_comparison/     # Pasta com gráficos
        ├── avg_response_time_by_protocol.png
        ├── throughput_by_protocol.png
        └── ...
```

## ⚠️ Notas Importantes

1. **Certifique-se que a aplicação está rodando:**
   ```bash
   docker-compose ps
   ```
   Deve mostrar os containers `app`, `postgres` e `locust` rodando.

2. **Se precisar limpar e recomeçar:**
   ```bash
   rm -rf teste-carga/reports/*
   ```

3. **Para ver os logs durante os testes:**
   ```bash
   docker-compose logs -f app
   ```

## 🐛 Problemas Comuns

**Erro: "Container not found"**
- Solução: Execute `docker-compose up -d --build`

**Erro: "Python not found"**
- Solução: Instale Python 3 ou use: `python3 generate_protocol_comparison.py`

**Erro: "Module not found: pandas"**
- Solução: Instale dependências: `pip install pandas matplotlib`

**Gráficos não aparecem**
- Verifique se os testes geraram os arquivos CSV em `teste-carga/reports/`
- Execute novamente o script de gráficos

## 📈 Interpretando os Resultados

- **Menor tempo de resposta = Melhor**
- **Maior throughput = Melhor**
- **Menor latência P95 = Mais consistente**

Compare os gráficos para decidir qual protocolo é melhor para seu caso de uso!
