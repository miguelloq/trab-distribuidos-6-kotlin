# Music Streaming Service - REST API

API REST desenvolvida em Kotlin com Spring Boot para gerenciamento de um serviço de streaming de músicas.

## 🛠️ Tecnologias

- **Kotlin** 1.9.20
- **Spring Boot** 3.2.0
- **Spring Data JPA**
- **PostgreSQL** 15
- **Docker & Docker Compose**

## 📋 Modelo de Dados

```
Usuario (id, nome, idade)
    ↓ 1:N
Playlist (id, nome, usuario_id)
    ↓ N:M
Musica (id, nome, artista)
```

## 🚀 Como Executar

### Opção 1: Com Docker Compose (Recomendado)

```bash
# Subir banco de dados e aplicação
docker-compose up -d

# Ver logs
docker-compose logs -f app
```

### Opção 2: Apenas Banco com Docker

```bash
# Subir apenas o PostgreSQL
docker-compose up -d postgres

# Executar a aplicação localmente
./gradlew bootRun
```

### Opção 3: Localmente sem Docker

1. Instale o PostgreSQL
2. Crie o banco:
```sql
CREATE DATABASE musicdb;
CREATE USER admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE musicdb TO admin;
```

3. Execute:
```bash
./gradlew bootRun
```

## 📡 Endpoints

Base URL: `http://localhost:8080/api`

### 1. Listar todos os usuários
```bash
GET /api/usuarios
```

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "idade": 25
  }
]
```

### 2. Listar todas as músicas
```bash
GET /api/musicas
```

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "nome": "Bohemian Rhapsody",
    "artista": "Queen"
  }
]
```

### 3. Listar playlists de um usuário
```bash
GET /api/playlists/usuario/{usuarioId}
```

**Exemplo:**
```bash
GET /api/playlists/usuario/1
```

**Resposta:**
```json
[
  {
    "id": 1,
    "nome": "Rock Clássico",
    "usuarioId": 1,
    "usuarioNome": "João Silva"
  }
]
```

### 4. Listar músicas de uma playlist
```bash
GET /api/playlists/{playlistId}/musicas
```

**Exemplo:**
```bash
GET /api/playlists/1/musicas
```

**Resposta:**
```json
{
  "id": 1,
  "nome": "Rock Clássico",
  "musicas": [
    {
      "id": 1,
      "nome": "Bohemian Rhapsody",
      "artista": "Queen"
    },
    {
      "id": 2,
      "nome": "Stairway to Heaven",
      "artista": "Led Zeppelin"
    }
  ]
}
```

## 🧪 Testando a API

### Criar Usuário
```bash
curl -X POST http://localhost:8080/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "idade": 25
  }'
```

### Criar Música
```bash
curl -X POST http://localhost:8080/api/musicas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Bohemian Rhapsody",
    "artista": "Queen"
  }'
```

### Script de População do Banco

Para facilitar os testes, você pode usar este script SQL:

```sql
-- Inserir usuários
INSERT INTO usuarios (nome, idade) VALUES 
  ('João Silva', 25),
  ('Maria Santos', 30);

-- Inserir músicas
INSERT INTO musicas (nome, artista) VALUES 
  ('Bohemian Rhapsody', 'Queen'),
  ('Stairway to Heaven', 'Led Zeppelin'),
  ('Hotel California', 'Eagles');

-- Inserir playlists
INSERT INTO playlists (nome, usuario_id) VALUES 
  ('Rock Clássico', 1),
  ('Favoritas', 1),
  ('Músicas Antigas', 2);

-- Relacionar músicas com playlists
INSERT INTO playlist_musica (playlist_id, musica_id) VALUES 
  (1, 1), (1, 2),
  (2, 1), (2, 3),
  (3, 2), (3, 3);
```

## 📦 Estrutura do Projeto

```
src/main/kotlin/com/streaming/music/
├── controller/          # Controllers REST
│   ├── UsuarioController.kt
│   ├── MusicaController.kt
│   └── PlaylistController.kt
├── service/            # Lógica de negócio
│   ├── UsuarioService.kt
│   ├── MusicaService.kt
│   └── PlaylistService.kt
├── repository/         # Acesso ao banco
│   ├── UsuarioRepository.kt
│   ├── MusicaRepository.kt
│   └── PlaylistRepository.kt
├── model/             # Entidades JPA
│   ├── Usuario.kt
│   ├── Musica.kt
│   └── Playlist.kt
├── dto/               # Data Transfer Objects
│   └── DTOs.kt
└── MusicStreamingApplication.kt
```

## 🛑 Parar a Aplicação

```bash
docker-compose down

# Para remover também os volumes (dados do banco)
docker-compose down -v
```

## 📝 Notas

- A aplicação roda na porta **8080**
- O PostgreSQL roda na porta **5432**
- O Hibernate está configurado para criar/atualizar as tabelas automaticamente (`ddl-auto: update`)
- Os logs SQL estão habilitados para facilitar o debug
