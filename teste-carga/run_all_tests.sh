#!/bin/bash

# Script para executar todos os testes de carga com diferentes quantidades de usuários
# Os reports serão gerados em teste-carga/reports/

echo "======================================"
echo "Iniciando testes de carga - API Kotlin"
echo "======================================"

# Duração de cada teste
DURATION="120s"

# Lista de quantidade de usuários para testar
USER_COUNTS=(100 1000 10000)

for USERS in "${USER_COUNTS[@]}"
do
    # Calcular spawn rate (10% dos usuários por segundo, mínimo 10)
    SPAWN_RATE=$((USERS / 10))
    if [ $SPAWN_RATE -lt 10 ]; then
        SPAWN_RATE=10
    fi

    echo ""
    echo "======================================"
    echo "Executando teste com $USERS usuários"
    echo "Spawn rate: $SPAWN_RATE usuarios/segundo"
    echo "Duração: $DURATION"
    echo "======================================"

    docker exec music-streaming-locust locust \
      -f /teste-carga/locustfile.py \
      --host=http://app:8080 \
      --headless \
      -u $USERS \
      -r $SPAWN_RATE \
      -t $DURATION \
      --html /teste-carga/reports/report_${USERS}_users.html \
      --csv /teste-carga/reports/report_${USERS}_users

    echo "Teste com $USERS usuários concluído!"
    echo "Reports salvos em: teste-carga/reports/report_${USERS}_users.*"

    # Pequena pausa entre os testes para a aplicação se estabilizar
    if [ $USERS -ne 10000 ]; then
        echo "Aguardando 30 segundos antes do próximo teste..."
        sleep 30
    fi
done

echo ""
echo "======================================"
echo "Todos os testes foram concluídos!"
echo "======================================"
echo "Para gerar os gráficos, execute:"
echo "python teste-carga/generate_charts.py"
