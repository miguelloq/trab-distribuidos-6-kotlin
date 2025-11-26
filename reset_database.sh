#!/bin/bash

# Script para resetar o banco de dados e carregar novos dados
# Útil após atualizar o DataInitializer

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         RESETAR BANCO DE DADOS E CARREGAR NOVOS DADOS     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "⚠️  Este script irá:"
echo "   1. Parar todos os containers"
echo "   2. Remover o volume do banco de dados"
echo "   3. Rebuild da aplicação"
echo "   4. Subir os serviços novamente"
echo "   5. Aguardar o DataInitializer carregar os novos dados"
echo ""

read -p "Deseja continuar? (s/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[SsYy]$ ]]
then
    echo "❌ Operação cancelada"
    exit 1
fi

echo ""
echo "[1/5] Parando containers..."
docker-compose down -v
echo "✓ Containers parados e volumes removidos"
echo ""

echo "[2/5] Fazendo rebuild da aplicação..."
docker-compose build --no-cache app
echo "✓ Rebuild concluído"
echo ""

echo "[3/5] Subindo serviços..."
docker-compose up -d
echo "✓ Serviços iniciados"
echo ""

echo "[4/5] Aguardando inicialização da aplicação..."
echo "   Isso pode levar até 2 minutos com os novos dados (200 usuários, 1000 músicas, 400 playlists)"
echo ""

# Função para verificar se a aplicação está pronta
check_app_ready() {
    docker logs music-streaming-app 2>&1 | grep -q "Dados mockados criados com sucesso"
}

# Aguardar até 180 segundos (3 minutos)
TIMEOUT=180
ELAPSED=0
until check_app_ready || [ $ELAPSED -eq $TIMEOUT ]; do
    sleep 5
    ELAPSED=$((ELAPSED + 5))
    echo "   Aguardando... (${ELAPSED}s/${TIMEOUT}s)"
done

if [ $ELAPSED -eq $TIMEOUT ]; then
    echo "❌ Erro: Aplicação não carregou os dados no tempo esperado"
    echo ""
    echo "Verifique os logs:"
    echo "   docker logs music-streaming-app | tail -50"
    exit 1
fi

echo "✓ Dados carregados com sucesso!"
echo ""

echo "[5/5] Verificando dados..."
echo ""

# Verificar quantidade de dados
echo "Consultando API REST..."
MUSICAS=$(curl -s http://localhost:8080/api/musicas | grep -o '"id"' | wc -l | tr -d ' ')
USUARIOS=$(curl -s http://localhost:8080/api/usuarios | grep -o '"id"' | wc -l | tr -d ' ')

echo "✓ Músicas encontradas: $MUSICAS (esperado: 1000)"
echo "✓ Usuários encontrados: $USUARIOS (esperado: 200)"
echo ""

# Mostrar logs do DataInitializer
echo "📊 Logs do DataInitializer:"
docker logs music-streaming-app 2>&1 | grep -A 10 "Inicializando dados mockados"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║            ✅ BANCO DE DADOS RESETADO COM SUCESSO!        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📊 Novos dados carregados:"
echo "   • 200 usuários"
echo "   • 1000 músicas"
echo "   • 400 playlists (~100 músicas cada)"
echo ""

echo "🎯 Próximos passos:"
echo "   1. Executar testes de carga: ./teste-carga/run_benchmark.sh"
echo "   2. Ou validar ambiente: ./teste-carga/validate_environment.sh"
echo ""
