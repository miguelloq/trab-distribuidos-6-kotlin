# 📊 Atualização do DataInitializer - Mais Dados para Testes

Este documento descreve as alterações feitas no DataInitializer para aumentar significativamente a quantidade de dados mockados.

## 📈 O Que Mudou?

### Antes ❌
- 50 usuários
- 200 músicas
- 100 playlists (2 por usuário)
- 5-15 músicas por playlist

### Depois ✅
- **200 usuários** (4x mais)
- **1000 músicas** (5x mais)
- **400 playlists** (2 por usuário)
- **~100 músicas por playlist** (média de 100 músicas)

## 🎯 Por Que Essas Mudanças?

1. **Testes mais realistas**: Volume de dados mais próximo de um cenário real
2. **Melhor avaliação de performance**: Identifica gargalos que não apareceriam com poucos dados
3. **Testes de escalabilidade**: Permite avaliar como a API se comporta com mais dados
4. **Comparação mais significativa**: Diferenças entre protocolos (REST/GraphQL/SOAP/gRPC) ficam mais evidentes
5. **Playlists grandes**: ~100 músicas por playlist testa serialização de payloads grandes (especialmente importante para comparar JSON vs XML vs Protocol Buffers)

## 📝 Arquivos Modificados

### 1. DataInitializer.kt
**Localização:** `src/main/kotlin/com/streaming/music/config/DataInitializer.kt`

**Alterações:**
- ✅ Geração combinatória de 200 nomes (100 primeiros nomes × 50 sobrenomes)
- ✅ 1000 músicas: 200 famosas + 800 geradas programaticamente
- ✅ 100+ artistas (expandido de ~37 para ~100)
- ✅ Playlists com 90-110 músicas aleatórias (antes: 5-15)
- ✅ Logs de progresso durante a criação (a cada 50 usuários e 100 músicas)

### 2. Testes Locust
**Arquivos:**
- `teste-carga/locustfile_rest.py`
- `teste-carga/locustfile_graphql.py`
- `teste-carga/locustfile_soap.py`
- `teste-carga/locustfile_grpc.py`

**Alterações:**
- ✅ IDs de usuários válidos atualizados: `range(1, 51)` → `range(1, 201)`
- ✅ Comentários atualizados refletindo novos volumes

### 3. Documentação
**Arquivos:**
- `teste-carga/README.md`
- `teste-carga/QUICKSTART.md`

**Alterações:**
- ✅ Números atualizados em toda documentação
- ✅ Notas sobre tempo de inicialização aumentado

## 🚀 Como Aplicar as Mudanças?

### Opção 1: Script Automático (Recomendado) ⭐

```bash
./reset_database.sh
```

Este script irá:
1. Parar todos os containers
2. Remover volumes do banco de dados
3. Rebuild da aplicação
4. Subir serviços novamente
5. Aguardar carregamento dos dados
6. Verificar se dados foram carregados corretamente

**Tempo estimado:** ~3-4 minutos

### Opção 2: Comandos Manuais

```bash
# 1. Parar e limpar
docker-compose down -v

# 2. Rebuild (opcional, mas recomendado)
docker-compose build --no-cache app

# 3. Subir serviços
docker-compose up -d

# 4. Aguardar inicialização (~2 minutos)
sleep 120

# 5. Verificar logs
docker logs music-streaming-app | tail -30
```

## ⏱️ Tempo de Inicialização

### Antes
- Inicialização: ~15-20 segundos
- DataInitializer: ~5 segundos

### Depois
- Inicialização: ~30-45 segundos
- DataInitializer: ~15-30 segundos
- **Total: ~60-90 segundos**

**⚠️ Importante:** Aguarde pelo menos **90 segundos** após `docker-compose up` antes de executar os testes de carga!

## 🔍 Como Verificar se os Dados Foram Carregados?

### Ver logs do DataInitializer:
```bash
docker logs music-streaming-app | grep "Dados mockados criados com sucesso" -A 5
```

**Saída esperada:**
```
Dados mockados criados com sucesso!
- 200 usuários
- 1000 músicas
- 400 playlists (2 por usuário, ~100 músicas cada)
```

### Testar API REST:
```bash
# Contar usuários
curl -s http://localhost:8080/api/usuarios | grep -o '"id"' | wc -l
# Esperado: 200

# Contar músicas
curl -s http://localhost:8080/api/musicas | grep -o '"id"' | wc -l
# Esperado: 1000

# Ver playlist de um usuário (deve ter ~100 músicas)
curl -s http://localhost:8080/api/playlists/usuario/1 | jq
```

## 📊 Impacto nos Testes de Carga

### Vantagens ✅
1. **Respostas maiores**: Teste real de serialização/deserialização
2. **Mais carga no banco**: Queries com mais dados
3. **Payload maior**: Especialmente SOAP (XML) vs gRPC (binário)
4. **Diferenças mais evidentes**: Comparação entre protocolos mais clara

### Considerações ⚠️
1. **Tempo de resposta maior**: Normal ter latências maiores
2. **Mais memória**: Aplicação pode usar mais RAM
3. **Testes mais longos**: Processamento de 1000 músicas vs 200
4. **Rede**: Transferência de dados maior

## 🎯 Executar Testes de Carga

Após carregar os novos dados:

```bash
# Validar ambiente primeiro
./teste-carga/validate_environment.sh

# Executar benchmark completo
./teste-carga/run_benchmark.sh
```

## 📈 Estrutura dos Novos Dados

### Usuários (200)
- Nomes: Combinação de 100 primeiros nomes + 50 sobrenomes
- Idade: Random entre 18-64 anos
- IDs: 1 a 200

### Músicas (1000)
- **0-199**: Músicas rock clássico famosas
- **200-399**: Músicas por gênero ("Rock Song 1", "Pop Song 2", etc)
- **400-599**: Músicas com adjetivos ("Electric Rock 1", "Acoustic Blues 2", etc)
- **600-799**: Tracks numeradas ("Track 1 - Jazz", etc)
- **800-999**: Músicas originais ("Original Song 1", etc)

### Artistas (~100)
Expandido de ~37 para ~100 artistas, incluindo:
- Rock clássico: Queen, Led Zeppelin, Pink Floyd, etc
- Rock moderno: Foo Fighters, Arctic Monkeys, Muse, etc
- Metal: Metallica, Iron Maiden, Slipknot, etc
- Alternative: Radiohead, The Cure, R.E.M., etc

### Playlists (400)
- 2 por usuário
- 90-110 músicas por playlist (média: 100)
- Nomes baseados em gêneros musicais
- Total de ~40.000 relações música-playlist

## 🐛 Troubleshooting

### Problema: "Dados já existem no banco"

**Causa:** O DataInitializer só carrega dados se o banco estiver vazio

**Solução:**
```bash
# Opção 1: Usar script
./reset_database.sh

# Opção 2: Manual
docker-compose down -v
docker-compose up -d
```

### Problema: Aplicação demora muito para iniciar

**Causa:** Criação de 1000 músicas + 400 playlists leva tempo

**Solução:** Normal! Aguarde até 2 minutos. Veja progresso nos logs:
```bash
docker logs -f music-streaming-app
```

### Problema: Erro "OutOfMemory" ou "Connection timeout"

**Causa:** Docker com pouca memória alocada

**Solução:** Aumente memória do Docker:
- Mac: Docker Desktop → Settings → Resources → Memory: 4GB+
- Linux: Configurar daemon do Docker

### Problema: Testes Locust falhando

**Causa:** Aplicação ainda inicializando ou sem dados

**Solução:**
```bash
# Verificar se app está pronto
curl http://localhost:8080/api/musicas

# Ver logs
docker logs music-streaming-app | tail -50

# Validar ambiente
./teste-carga/validate_environment.sh
```

## 📚 Referências

- DataInitializer.kt: [src/main/kotlin/com/streaming/music/config/DataInitializer.kt](src/main/kotlin/com/streaming/music/config/DataInitializer.kt)
- Testes Locust: [teste-carga/](teste-carga/)
- Documentação completa: [teste-carga/README.md](teste-carga/README.md)

## ✅ Checklist

Após aplicar as mudanças, verifique:

- [ ] Containers rodando: `docker-compose ps`
- [ ] Aplicação iniciada: `docker logs music-streaming-app | grep "Started"`
- [ ] Dados carregados: `docker logs music-streaming-app | grep "Dados mockados criados com sucesso"`
- [ ] 200 usuários: `curl -s http://localhost:8080/api/usuarios | grep -o '"id"' | wc -l`
- [ ] 1000 músicas: `curl -s http://localhost:8080/api/musicas | grep -o '"id"' | wc -l`
- [ ] Playlists com ~100 músicas: `curl -s http://localhost:8080/api/playlists/usuario/1`

---

**Data da atualização:** 2025-11-26
**Versão:** 2.0 - Dados expandidos
