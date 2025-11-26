@echo off
echo ============================================================
echo TESTES DE CARGA - COMPARACAO DE PROTOCOLOS
echo API Kotlin Music Streaming
echo ============================================================
echo.
echo Este script vai executar testes de carga para:
echo - Protocolos: REST, GraphQL, SOAP
echo - Cargas: 100, 1000, 10000 usuarios
echo - Duracao de cada teste: 120 segundos
echo.
echo Tempo total estimado: ~20-25 minutos
echo.
pause

cd teste-carga
bash run_protocol_tests.sh

echo.
echo ============================================================
echo TESTES CONCLUIDOS!
echo ============================================================
echo.
echo Proximos passos:
echo 1. Execute o arquivo: 2_gerar_graficos.bat
echo.
pause
