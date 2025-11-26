# 🔧 Correção dos Testes de Carga

## 📝 O Que Foi Corrigido?

### Problema Identificado
Os testes estavam testando **listar playlists de um usuário** quando o objetivo era testar **listar músicas de uma playlist**.

### Por Que a Mudança Faz Sentido?
1. **Payloads maiores**: Cada playlist tem ~100 músicas, retornando muito mais dados
2. **Comparação real**: Testa serialização de listas grandes (JSON vs XML vs Protocol Buffers)
3. **Cenário realista**: Ver músicas de uma playlist é mais comum que listar playlists
4. **Objetivo original**: Por isso as playlists foram criadas com ~100 músicas cada!

## ✅ Funcionalidades Testadas (CORRIGIDO)

### Antes ❌
1. Listar todas as músicas (1000)
2. Listar todos os usuários (200)
3. ~~Listar playlists de um usuário~~ (retorna apenas 2 playlists, pouco dado)

### Depois ✅
1. **Listar todas as músicas** (1000 músicas)
2. **Listar todos os usuários** (200 usuários)
3. **Listar músicas de uma playlist** (~100 músicas por playlist)

## 📊 Impacto nos Testes

### Volume de Dados Retornados

| Funcionalidade | Registros | Tamanho Aproximado |
|----------------|-----------|-------------------|
| Listar músicas | 1000 músicas | ~100KB (JSON) |
| Listar usuários | 200 usuários | ~10KB (JSON) |
| **Músicas de playlist** | **~100 músicas** | **~10KB (JSON)** |

### Comparação de Protocolos

Agora os testes comparam melhor os protocolos porque:

1. **REST (JSON)**: Texto, legível, ~10KB por playlist
2. **GraphQL (JSON)**: Similar ao REST, mas pode customizar campos
3. **SOAP (XML)**: Verboso, tags XML adicionam overhead (~15-20KB)
4. **gRPC (Protocol Buffers)**: Binário, compacto (~5-7KB)

A diferença de tamanho fica **muito mais evidente** com ~100 músicas!

## 🔄 Alterações Feitas

### 1. Locustfiles (REST, GraphQL, SOAP, gRPC)
- ✅ Mudado de `VALID_USER_IDS` para `VALID_PLAYLIST_IDS`
- ✅ Range atualizado: `range(1, 401)` (400 playlists)
- ✅ Endpoints/queries atualizados para listar músicas de playlist
- ✅ Nomes das tasks atualizados

### 2. Endpoints por Protocolo

**REST:**
- Antes: `GET /api/playlists/usuario/{usuarioId}`
- Depois: `GET /api/playlists/{playlistId}/musicas`

**GraphQL:**
- Antes: `playlistsPorUsuario(usuarioId: Long)`
- Depois: `musicasDaPlaylist(playlistId: Long)`

**SOAP:**
- Antes: `<mus:listarPlaylistsPorUsuarioRequest>`
- Depois: `<mus:listarMusicasDaPlaylistRequest>`

**gRPC:**
- Antes: `ListarPlaylistsPorUsuario(UsuarioIdRequest)`
- Depois: `ListarMusicasDaPlaylist(PlaylistIdRequest)`

### 3. Documentação
- ✅ QUICKSTART.md atualizado
- ✅ ATUALIZACAO_DADOS.md atualizado
- ✅ generate_charts.py - nomes das tasks atualizados

## 🎯 Como Testar

### 1. Testar Manualmente
```bash
# REST - Ver músicas da playlist 1
curl http://localhost:8080/api/playlists/1/musicas | jq

# GraphQL - Ver músicas da playlist 1
curl -X POST http://localhost:8080/api/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ musicasDaPlaylist(playlistId: 1) { id nome musicas { id nome artista } } }"}'
```

### 2. Executar Testes de Carga
```bash
# Resetar banco (se necessário)
./reset_database.sh

# Executar benchmark completo
./teste-carga/run_benchmark.sh
```

## 📈 Resultados Esperados

Com essa mudança, você verá diferenças mais evidentes entre os protocolos:

### Tempo de Resposta Esperado
- **gRPC**: Mais rápido (binário, HTTP/2)
- **REST**: Rápido (JSON eficiente)
- **GraphQL**: Similar ao REST
- **SOAP**: Mais lento (XML verboso)

### Throughput (RPS)
- **gRPC**: Maior throughput
- **REST**: Bom throughput
- **GraphQL**: Similar ao REST
- **SOAP**: Menor throughput

### Tamanho do Payload
- **gRPC**: ~5-7KB (binário compacto)
- **REST/GraphQL**: ~10KB (JSON)
- **SOAP**: ~15-20KB (XML verboso)

## ✅ Checklist de Verificação

Após executar os testes, verifique:

- [ ] Testes de carga executam sem erros
- [ ] Task "Músicas de Playlist" aparece nos resultados
- [ ] Payloads estão maiores (comparar com versão anterior)
- [ ] Diferenças entre protocolos são mais evidentes
- [ ] Gráficos mostram "Músicas de Playlist" corretamente

## 📚 Arquivos Modificados

- `teste-carga/locustfile_rest.py`
- `teste-carga/locustfile_graphql.py`
- `teste-carga/locustfile_soap.py`
- `teste-carga/locustfile_grpc.py`
- `teste-carga/generate_charts.py`
- `teste-carga/QUICKSTART.md`
- `ATUALIZACAO_DADOS.md`
- `CORRECAO_TESTES.md` (novo)

---

**Data da correção:** 2025-11-26
**Versão:** 2.1 - Testes corrigidos para músicas de playlist
