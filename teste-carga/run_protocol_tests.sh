#!/bin/bash

# Script para executar testes de carga comparando diferentes protocolos
# Protocolos: REST, GraphQL, SOAP
# Cargas: 100, 1000, 10000 usuários

echo "======================================================"
echo "Testes de Carga - Comparação de Protocolos"
echo "API Kotlin - Music Streaming"
echo "======================================================"

# Duração de cada teste
DURATION="120s"

# Lista de protocolos
PROTOCOLS=("rest" "graphql" "soap")

# Lista de quantidade de usuários
USER_COUNTS=(100 1000 10000)

for PROTOCOL in "${PROTOCOLS[@]}"
do
    echo ""
    echo "======================================================"
    echo "Protocolo: ${PROTOCOL^^}"
    echo "======================================================"

    for USERS in "${USER_COUNTS[@]}"
    do
        # Calcular spawn rate (10% dos usuários por segundo, mínimo 10)
        SPAWN_RATE=$((USERS / 10))
        if [ $SPAWN_RATE -lt 10 ]; then
            SPAWN_RATE=10
        fi

        echo ""
        echo "------------------------------------------------------"
        echo "Testando $PROTOCOL com $USERS usuários"
        echo "Spawn rate: $SPAWN_RATE usuarios/segundo"
        echo "Duração: $DURATION"
        echo "------------------------------------------------------"

        docker exec music-streaming-locust locust \
          -f //teste-carga/locustfile_${PROTOCOL}.py \
          --host=http://app:8080 \
          --headless \
          -u $USERS \
          -r $SPAWN_RATE \
          -t $DURATION \
          --html //teste-carga/reports/${PROTOCOL}_${USERS}_users.html \
          --csv //teste-carga/reports/${PROTOCOL}_${USERS}_users

        echo "[OK] Teste $PROTOCOL com $USERS usuários concluído!"

        # Pausa entre testes para estabilizar
        if [ "$PROTOCOL" != "soap" ] || [ $USERS -ne 10000 ]; then
            echo "Aguardando 20 segundos antes do próximo teste..."
            sleep 20
        fi
    done
done

echo ""
echo "======================================================"
echo "Todos os testes foram concluídos!"
echo "======================================================"
echo ""
echo "Protocolos testados: REST, GraphQL, SOAP"
echo "Cargas testadas: 100, 1000, 10000 usuários"
echo ""
echo "Para gerar os gráficos comparativos, execute:"
echo "python teste-carga/generate_protocol_comparison.py"
echo ""
echo "NOTA: Para testar gRPC, use ferramentas especializadas"
echo "como ghz (https://ghz.sh/) ou grpcurl, pois Locust"
echo "não tem suporte nativo completo para gRPC."
