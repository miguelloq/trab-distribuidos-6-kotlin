# Comandos Úteis - Music Streaming Service

## Docker Compose

### Iniciar os serviços
```bash
docker-compose up -d
```

### Ver logs da aplicação
```bash
docker-compose logs -f app
```

### Ver logs do banco
```bash
docker-compose logs -f postgres
```

### Parar os serviços
```bash
docker-compose down
```

### Parar e remover volumes (apaga dados)
```bash
docker-compose down -v
```

### Rebuild da aplicação
```bash
docker-compose up -d --build
```

## Gradle

### Compilar o projeto
```bash
./gradlew build
```

### Executar localmente
```bash
./gradlew bootRun
```

### Limpar build
```bash
./gradlew clean
```

## PostgreSQL

### Conectar ao banco via Docker
```bash
docker exec -it music-streaming-db psql -U admin -d musicdb
```

### Comandos úteis no psql
```sql
-- Listar tabelas
\dt

-- Descrever tabela
\d usuarios
\d musicas
\d playlists
\d playlist_musica

-- Ver dados
SELECT * FROM usuarios;
SELECT * FROM musicas;
SELECT * FROM playlists;
SELECT * FROM playlist_musica;

-- Sair
\q
```

### Popular banco de dados
```bash
docker exec -i music-streaming-db psql -U admin -d musicdb < populate_db.sql
```

## Testando Endpoints

### Testar todos os endpoints (script automático)
```bash
./test_endpoints.sh
```

### Testar endpoints individualmente

#### 1. Listar usuários
```bash
curl http://localhost:8080/api/usuarios | jq
```

#### 2. Listar músicas
```bash
curl http://localhost:8080/api/musicas | jq
```

#### 3. Listar playlists de um usuário
```bash
curl http://localhost:8080/api/playlists/usuario/1 | jq
```

#### 4. Listar músicas de uma playlist
```bash
curl http://localhost:8080/api/playlists/1/musicas | jq
```

### Criar dados

#### Criar usuário
```bash
curl -X POST http://localhost:8080/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "idade": 25}' | jq
```

#### Criar música
```bash
curl -X POST http://localhost:8080/api/musicas \
  -H "Content-Type: application/json" \
  -d '{"nome": "Bohemian Rhapsody", "artista": "Queen"}' | jq
```

## Monitoramento

### Ver uso de recursos
```bash
docker stats
```

### Ver containers rodando
```bash
docker ps
```

### Verificar logs de erro
```bash
docker-compose logs app | grep ERROR
```

## Troubleshooting

### Porta 8080 já em uso
```bash
# Encontrar processo usando a porta
lsof -i :8080

# Matar processo
kill -9 <PID>
```

### Porta 5432 já em uso
```bash
# Encontrar processo usando a porta
lsof -i :5432

# Matar processo
kill -9 <PID>
```

### Recriar banco do zero
```bash
docker-compose down -v
docker-compose up -d
```

### Ver todas as networks Docker
```bash
docker network ls
```

### Inspecionar network
```bash
docker network inspect music-streaming-service_music-network
```
