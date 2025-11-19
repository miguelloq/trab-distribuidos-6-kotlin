#!/bin/bash

# Script de Testes - Music Streaming Service REST API
# Certifique-se de que a aplicação está rodando em http://localhost:8080

BASE_URL="http://localhost:8080/api"

echo "========================================"
echo "TESTANDO API - Music Streaming Service"
echo "========================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Criar usuários
echo -e "${BLUE}1. Criando usuários...${NC}"
curl -X POST $BASE_URL/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "idade": 25}'
echo ""

curl -X POST $BASE_URL/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria Santos", "idade": 30}'
echo -e "\n"

# 2. Criar músicas
echo -e "${BLUE}2. Criando músicas...${NC}"
curl -X POST $BASE_URL/musicas \
  -H "Content-Type: application/json" \
  -d '{"nome": "Bohemian Rhapsody", "artista": "Queen"}'
echo ""

curl -X POST $BASE_URL/musicas \
  -H "Content-Type: application/json" \
  -d '{"nome": "Stairway to Heaven", "artista": "Led Zeppelin"}'
echo ""

curl -X POST $BASE_URL/musicas \
  -H "Content-Type: application/json" \
  -d '{"nome": "Hotel California", "artista": "Eagles"}'
echo -e "\n"

sleep 2

echo "========================================"
echo "TESTANDO OS 4 ENDPOINTS PRINCIPAIS"
echo "========================================"
echo ""

# Endpoint 1: Listar todos os usuários
echo -e "${GREEN}ENDPOINT 1: GET /api/usuarios${NC}"
echo "Listar os dados de todos os usuários do serviço"
echo "---"
curl -X GET $BASE_URL/usuarios
echo -e "\n\n"

sleep 1

# Endpoint 2: Listar todas as músicas
echo -e "${GREEN}ENDPOINT 2: GET /api/musicas${NC}"
echo "Listar os dados de todas as músicas mantidas pelo serviço"
echo "---"
curl -X GET $BASE_URL/musicas
echo -e "\n\n"

sleep 1

# Endpoint 3: Listar playlists de um usuário
echo -e "${GREEN}ENDPOINT 3: GET /api/playlists/usuario/1${NC}"
echo "Listar os dados de todas as playlists de um determinado usuário"
echo "---"
curl -X GET $BASE_URL/playlists/usuario/1
echo -e "\n\n"

sleep 1

# Endpoint 4: Listar músicas de uma playlist
echo -e "${GREEN}ENDPOINT 4: GET /api/playlists/1/musicas${NC}"
echo "Listar os dados de todas as músicas de uma determinada playlist"
echo "---"
curl -X GET $BASE_URL/playlists/1/musicas
echo -e "\n\n"

echo "========================================"
echo "TESTES CONCLUÍDOS!"
echo "========================================"
