@echo off
echo ============================================================
echo GERACAO DE GRAFICOS - COMPARACAO DE PROTOCOLOS
echo API Kotlin Music Streaming
echo ============================================================
echo.
echo Este script vai gerar graficos comparativos entre:
echo - REST vs GraphQL vs SOAP
echo.
echo Graficos que serao gerados:
echo - Tempo medio de resposta por protocolo
echo - Throughput por protocolo
echo - Latencia P95 por protocolo
echo - Ranking do protocolo mais rapido
echo - Comparacoes por endpoint
echo - Tabela resumo
echo.
pause

cd teste-carga
python generate_protocol_comparison.py

echo.
echo ============================================================
echo GRAFICOS GERADOS!
echo ============================================================
echo.
echo Os graficos estao em: teste-carga\reports\protocol_comparison\
echo.
echo Abra a pasta para visualizar os graficos!
echo.
pause

start "" "%CD%\reports\protocol_comparison"
