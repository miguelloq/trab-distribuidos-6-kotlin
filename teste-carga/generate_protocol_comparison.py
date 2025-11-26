#!/usr/bin/env python3
"""
Script para gerar gráficos comparativos de performance entre protocolos
Compara REST, GraphQL e SOAP em diferentes cenários de carga
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configurações
REPORTS_DIR = Path(__file__).parent / "reports"
CHARTS_DIR = REPORTS_DIR / "protocol_comparison"
PROTOCOLS = ["rest", "graphql", "soap"]
USER_COUNTS = [100, 1000, 10000]
API_NAME = "API Kotlin - Music Streaming"

# Cores para cada protocolo
PROTOCOL_COLORS = {
    "rest": "#3498db",      # Azul
    "graphql": "#e74c3c",   # Vermelho
    "soap": "#2ecc71"       # Verde
}

PROTOCOL_LABELS = {
    "rest": "REST",
    "graphql": "GraphQL",
    "soap": "SOAP"
}

def setup_directories():
    """Cria diretório de gráficos se não existir"""
    CHARTS_DIR.mkdir(exist_ok=True)
    print(f"Graficos serao salvos em: {CHARTS_DIR}")

def load_protocol_data(protocol, user_count):
    """Carrega dados de um protocolo específico"""
    stats_file = REPORTS_DIR / f"{protocol}_{user_count}_users_stats.csv"

    if not stats_file.exists():
        print(f"[AVISO] Arquivo nao encontrado: {stats_file}")
        return None

    try:
        df = pd.read_csv(stats_file)
        df = df[~df['Name'].isin(['Aggregated', 'Total'])]
        return df
    except Exception as e:
        print(f"[ERRO] Erro ao ler {stats_file}: {e}")
        return None

def create_avg_response_time_by_protocol(all_data):
    """Gráfico: Tempo médio de resposta por protocolo e carga"""
    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(USER_COUNTS))
    width = 0.25

    for i, protocol in enumerate(PROTOCOLS):
        avg_times = []
        for user_count in USER_COUNTS:
            data = all_data.get((protocol, user_count))
            if data is not None and not data.empty:
                # Média de todos os endpoints
                avg_time = data['Average Response Time'].mean()
                avg_times.append(avg_time)
            else:
                avg_times.append(0)

        offset = (i - 1) * width
        ax.bar(x + offset, avg_times, width,
               label=PROTOCOL_LABELS[protocol],
               color=PROTOCOL_COLORS[protocol], alpha=0.8)

    ax.set_xlabel('Numero de Usuarios Concorrentes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Tempo Medio de Resposta (ms)', fontsize=12, fontweight='bold')
    ax.set_title(f'{API_NAME}\nComparacao de Tempo de Resposta por Protocolo',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{u} usuarios' for u in USER_COUNTS])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'avg_response_time_by_protocol.png', dpi=300, bbox_inches='tight')
    print("[OK] Grafico criado: avg_response_time_by_protocol.png")
    plt.close()

def create_throughput_by_protocol(all_data):
    """Gráfico: Throughput (req/s) por protocolo e carga"""
    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(USER_COUNTS))
    width = 0.25

    for i, protocol in enumerate(PROTOCOLS):
        throughputs = []
        for user_count in USER_COUNTS:
            data = all_data.get((protocol, user_count))
            if data is not None and not data.empty:
                # Soma de req/s de todos os endpoints
                throughput = data['Requests/s'].sum()
                throughputs.append(throughput)
            else:
                throughputs.append(0)

        offset = (i - 1) * width
        ax.bar(x + offset, throughputs, width,
               label=PROTOCOL_LABELS[protocol],
               color=PROTOCOL_COLORS[protocol], alpha=0.8)

    ax.set_xlabel('Numero de Usuarios Concorrentes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Throughput Total (req/s)', fontsize=12, fontweight='bold')
    ax.set_title(f'{API_NAME}\nComparacao de Throughput por Protocolo',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{u} usuarios' for u in USER_COUNTS])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'throughput_by_protocol.png', dpi=300, bbox_inches='tight')
    print("[OK] Grafico criado: throughput_by_protocol.png")
    plt.close()

def create_p95_latency_by_protocol(all_data):
    """Gráfico: Latência P95 por protocolo e carga"""
    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(USER_COUNTS))
    width = 0.25

    for i, protocol in enumerate(PROTOCOLS):
        p95_latencies = []
        for user_count in USER_COUNTS:
            data = all_data.get((protocol, user_count))
            if data is not None and not data.empty and '95%' in data.columns:
                # Média do P95 de todos os endpoints
                p95 = data['95%'].mean()
                p95_latencies.append(p95)
            else:
                p95_latencies.append(0)

        offset = (i - 1) * width
        ax.bar(x + offset, p95_latencies, width,
               label=PROTOCOL_LABELS[protocol],
               color=PROTOCOL_COLORS[protocol], alpha=0.8)

    ax.set_xlabel('Numero de Usuarios Concorrentes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latencia P95 (ms)', fontsize=12, fontweight='bold')
    ax.set_title(f'{API_NAME}\nComparacao de Latencia P95 por Protocolo',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{u} usuarios' for u in USER_COUNTS])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'p95_latency_by_protocol.png', dpi=300, bbox_inches='tight')
    print("[OK] Grafico criado: p95_latency_by_protocol.png")
    plt.close()

def create_endpoint_comparison(all_data, endpoint_pattern):
    """Gráfico comparativo para um endpoint específico"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Tempo de resposta
    x = np.arange(len(USER_COUNTS))
    width = 0.25

    for i, protocol in enumerate(PROTOCOLS):
        avg_times = []
        for user_count in USER_COUNTS:
            data = all_data.get((protocol, user_count))
            if data is not None:
                endpoint_data = data[data['Name'].str.contains(endpoint_pattern, case=False, na=False)]
                if not endpoint_data.empty:
                    avg_times.append(endpoint_data['Average Response Time'].values[0])
                else:
                    avg_times.append(0)
            else:
                avg_times.append(0)

        offset = (i - 1) * width
        ax1.bar(x + offset, avg_times, width,
               label=PROTOCOL_LABELS[protocol],
               color=PROTOCOL_COLORS[protocol], alpha=0.8)

    ax1.set_xlabel('Numero de Usuarios', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Tempo Medio (ms)', fontsize=11, fontweight='bold')
    ax1.set_title(f'Tempo de Resposta - {endpoint_pattern}', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([str(u) for u in USER_COUNTS])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    # Throughput
    for i, protocol in enumerate(PROTOCOLS):
        throughputs = []
        for user_count in USER_COUNTS:
            data = all_data.get((protocol, user_count))
            if data is not None:
                endpoint_data = data[data['Name'].str.contains(endpoint_pattern, case=False, na=False)]
                if not endpoint_data.empty:
                    throughputs.append(endpoint_data['Requests/s'].values[0])
                else:
                    throughputs.append(0)
            else:
                throughputs.append(0)

        offset = (i - 1) * width
        ax2.bar(x + offset, throughputs, width,
               label=PROTOCOL_LABELS[protocol],
               color=PROTOCOL_COLORS[protocol], alpha=0.8)

    ax2.set_xlabel('Numero de Usuarios', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Req/s', fontsize=11, fontweight='bold')
    ax2.set_title(f'Throughput - {endpoint_pattern}', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([str(u) for u in USER_COUNTS])
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    plt.suptitle(f'{API_NAME}\nComparacao: {endpoint_pattern}',
                fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    safe_name = endpoint_pattern.lower().replace(' ', '_').replace('á', 'a').replace('ú', 'u').replace('í', 'i')
    plt.savefig(CHARTS_DIR / f'endpoint_{safe_name}.png', dpi=300, bbox_inches='tight')
    print(f"[OK] Grafico criado: endpoint_{safe_name}.png")
    plt.close()

def create_summary_table(all_data):
    """Tabela resumo comparativa"""
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.axis('tight')
    ax.axis('off')

    # Preparar dados
    table_data = []
    table_data.append(['Protocolo', 'Usuarios', 'Avg Response (ms)', 'P95 (ms)',
                      'P99 (ms)', 'Throughput (req/s)', 'Taxa Falhas (%)'])

    for protocol in PROTOCOLS:
        for user_count in USER_COUNTS:
            data = all_data.get((protocol, user_count))
            if data is not None and not data.empty:
                avg_resp = data['Average Response Time'].mean()
                p95 = data['95%'].mean() if '95%' in data.columns else 0
                p99 = data['99%'].mean() if '99%' in data.columns else 0
                throughput = data['Requests/s'].sum()

                total_req = data['Request Count'].sum()
                total_fail = data['Failure Count'].sum()
                fail_rate = (total_fail / total_req * 100) if total_req > 0 else 0

                table_data.append([
                    PROTOCOL_LABELS[protocol],
                    f"{user_count}",
                    f"{avg_resp:.2f}",
                    f"{p95:.2f}",
                    f"{p99:.2f}",
                    f"{throughput:.2f}",
                    f"{fail_rate:.2f}"
                ])

    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.12, 0.1, 0.15, 0.12, 0.12, 0.17, 0.15])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.5)

    # Estilizar cabeçalho
    for i in range(len(table_data[0])):
        cell = table[(0, i)]
        cell.set_facecolor('#3498db')
        cell.set_text_props(weight='bold', color='white')

    # Colorir por protocolo
    colors = {'REST': '#d6eaf8', 'GraphQL': '#fadbd8', 'SOAP': '#d5f4e6'}
    for i in range(1, len(table_data)):
        protocol = table_data[i][0]
        for j in range(len(table_data[0])):
            cell = table[(i, j)]
            cell.set_facecolor(colors.get(protocol, 'white'))

    plt.title(f'{API_NAME}\nResumo Comparativo de Performance por Protocolo',
             fontsize=16, fontweight='bold', pad=20)

    plt.savefig(CHARTS_DIR / 'summary_comparison_table.png', dpi=300, bbox_inches='tight')
    print("[OK] Tabela resumo criada: summary_comparison_table.png")
    plt.close()

def create_ranking_chart(all_data):
    """Gráfico de ranking: protocolo mais rápido em cada cenário"""
    fig, ax = plt.subplots(figsize=(14, 8))

    scenarios = []
    winner_protocols = []
    winner_times = []

    for user_count in USER_COUNTS:
        best_protocol = None
        best_time = float('inf')

        for protocol in PROTOCOLS:
            data = all_data.get((protocol, user_count))
            if data is not None and not data.empty:
                avg_time = data['Average Response Time'].mean()
                if avg_time < best_time:
                    best_time = avg_time
                    best_protocol = protocol

        if best_protocol:
            scenarios.append(f'{user_count} usuarios')
            winner_protocols.append(PROTOCOL_LABELS[best_protocol])
            winner_times.append(best_time)

    colors_list = [PROTOCOL_COLORS[p.lower()] for p in winner_protocols]

    bars = ax.barh(scenarios, winner_times, color=colors_list, alpha=0.8)

    # Adicionar labels
    for i, (bar, protocol) in enumerate(zip(bars, winner_protocols)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2,
               f'  {protocol}: {width:.1f}ms',
               ha='left', va='center', fontweight='bold')

    ax.set_xlabel('Tempo Medio de Resposta (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cenario de Carga', fontsize=12, fontweight='bold')
    ax.set_title(f'{API_NAME}\nProtocolo Mais Rapido por Cenario',
                fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'fastest_protocol_ranking.png', dpi=300, bbox_inches='tight')
    print("[OK] Grafico criado: fastest_protocol_ranking.png")
    plt.close()

def main():
    print("=" * 60)
    print(f"Gerador de Graficos Comparativos - {API_NAME}")
    print("Comparacao de Protocolos: REST vs GraphQL vs SOAP")
    print("=" * 60)
    print()

    setup_directories()

    # Carregar todos os dados
    print("\nCarregando dados dos testes...")
    all_data = {}

    for protocol in PROTOCOLS:
        for user_count in USER_COUNTS:
            print(f"  Carregando {protocol.upper()} - {user_count} usuarios...")
            data = load_protocol_data(protocol, user_count)
            all_data[(protocol, user_count)] = data

    # Verificar se há dados
    if all(v is None for v in all_data.values()):
        print("\n[ERRO] Nenhum dado encontrado!")
        print("Execute os testes primeiro com: ./run_protocol_tests.sh")
        return

    print("\n" + "=" * 60)
    print("Gerando graficos comparativos...")
    print("=" * 60)
    print()

    # Gerar gráficos
    create_avg_response_time_by_protocol(all_data)
    create_throughput_by_protocol(all_data)
    create_p95_latency_by_protocol(all_data)
    create_ranking_chart(all_data)

    # Gráficos por endpoint
    create_endpoint_comparison(all_data, "Listar Musicas")
    create_endpoint_comparison(all_data, "Listar Usuarios")
    create_endpoint_comparison(all_data, "Playlists de Usuario")

    create_summary_table(all_data)

    print("\n" + "=" * 60)
    print("[OK] Todos os graficos foram gerados com sucesso!")
    print(f"[OK] Graficos salvos em: {CHARTS_DIR}")
    print("=" * 60)
    print()
    print("Graficos gerados:")
    print("  - avg_response_time_by_protocol.png")
    print("  - throughput_by_protocol.png")
    print("  - p95_latency_by_protocol.png")
    print("  - fastest_protocol_ranking.png")
    print("  - endpoint_listar_musicas.png")
    print("  - endpoint_listar_usuarios.png")
    print("  - endpoint_playlists_de_usuario.png")
    print("  - summary_comparison_table.png")

if __name__ == "__main__":
    main()
