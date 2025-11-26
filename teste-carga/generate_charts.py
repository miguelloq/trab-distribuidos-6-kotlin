#!/usr/bin/env python3
"""
Script para gerar gráficos dos testes de carga do Locust
Lê os arquivos CSV gerados e cria visualizações para cada endpoint e quantidade de usuários
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
import numpy as np

# Configurações
REPORTS_DIR = Path(__file__).parent / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"
USER_COUNTS = [100, 1000, 10000]
API_NAME = "API Kotlin - Music Streaming"

# Cores para os diferentes endpoints
ENDPOINT_COLORS = {
    "Listar Músicas": "#3498db",
    "Listar Usuários": "#e74c3c",
    "Playlists de Usuário": "#2ecc71",
    "Músicas da Playlist": "#f39c12"
}

def setup_directories():
    """Cria diretório de gráficos se não existir"""
    CHARTS_DIR.mkdir(exist_ok=True)
    print(f"Gráficos serão salvos em: {CHARTS_DIR}")

def load_report(user_count):
    """Carrega o CSV de estatísticas do Locust para uma quantidade de usuários"""
    stats_file = REPORTS_DIR / f"report_{user_count}_users_stats.csv"

    if not stats_file.exists():
        print(f"⚠️  Arquivo não encontrado: {stats_file}")
        return None

    try:
        df = pd.read_csv(stats_file)
        # Remove linhas agregadas (Total e Aggregated)
        df = df[~df['Name'].isin(['Aggregated', 'Total'])]
        return df
    except Exception as e:
        print(f"[ERRO] Erro ao ler {stats_file}: {e}")
        return None

def create_response_time_comparison_chart(data_by_users):
    """Gráfico comparando tempo de resposta médio por endpoint e quantidade de usuários"""
    fig, ax = plt.subplots(figsize=(14, 8))

    endpoints = []
    x_positions = []
    bar_width = 0.25

    # Organizar dados por endpoint
    endpoint_data = {}
    for user_count, df in data_by_users.items():
        if df is not None:
            for _, row in df.iterrows():
                endpoint = row['Name']
                if endpoint not in endpoint_data:
                    endpoint_data[endpoint] = {}
                endpoint_data[endpoint][user_count] = row['Average Response Time']

    # Criar barras agrupadas
    x = np.arange(len(endpoint_data))

    for i, user_count in enumerate(USER_COUNTS):
        values = [endpoint_data[ep].get(user_count, 0) for ep in endpoint_data.keys()]
        offset = (i - 1) * bar_width
        ax.bar(x + offset, values, bar_width, label=f'{user_count} usuários', alpha=0.8)

    ax.set_xlabel('Endpoint', fontsize=12, fontweight='bold')
    ax.set_ylabel('Tempo de Resposta Médio (ms)', fontsize=12, fontweight='bold')
    ax.set_title(f'{API_NAME}\nTempo de Resposta Médio por Endpoint', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(endpoint_data.keys(), rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'response_time_comparison.png', dpi=300, bbox_inches='tight')
    print("[OK] Grafico criado: response_time_comparison.png")
    plt.close()

def create_throughput_comparison_chart(data_by_users):
    """Gráfico comparando requisições por segundo por endpoint e quantidade de usuários"""
    fig, ax = plt.subplots(figsize=(14, 8))

    endpoint_data = {}
    for user_count, df in data_by_users.items():
        if df is not None:
            for _, row in df.iterrows():
                endpoint = row['Name']
                if endpoint not in endpoint_data:
                    endpoint_data[endpoint] = {}
                endpoint_data[endpoint][user_count] = row['Requests/s']

    x = np.arange(len(endpoint_data))
    bar_width = 0.25

    for i, user_count in enumerate(USER_COUNTS):
        values = [endpoint_data[ep].get(user_count, 0) for ep in endpoint_data.keys()]
        offset = (i - 1) * bar_width
        ax.bar(x + offset, values, bar_width, label=f'{user_count} usuários', alpha=0.8)

    ax.set_xlabel('Endpoint', fontsize=12, fontweight='bold')
    ax.set_ylabel('Requisições por Segundo (req/s)', fontsize=12, fontweight='bold')
    ax.set_title(f'{API_NAME}\nThroughput por Endpoint', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(endpoint_data.keys(), rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'throughput_comparison.png', dpi=300, bbox_inches='tight')
    print("[OK] Grafico criado: throughput_comparison.png")
    plt.close()

def create_failure_rate_chart(data_by_users):
    """Gráfico de taxa de falhas por endpoint e quantidade de usuários"""
    fig, ax = plt.subplots(figsize=(14, 8))

    endpoint_data = {}
    for user_count, df in data_by_users.items():
        if df is not None:
            for _, row in df.iterrows():
                endpoint = row['Name']
                if endpoint not in endpoint_data:
                    endpoint_data[endpoint] = {}
                # Calcular taxa de falha em porcentagem
                total_requests = row['Request Count']
                failures = row['Failure Count']
                failure_rate = (failures / total_requests * 100) if total_requests > 0 else 0
                endpoint_data[endpoint][user_count] = failure_rate

    x = np.arange(len(endpoint_data))
    bar_width = 0.25

    for i, user_count in enumerate(USER_COUNTS):
        values = [endpoint_data[ep].get(user_count, 0) for ep in endpoint_data.keys()]
        offset = (i - 1) * bar_width
        ax.bar(x + offset, values, bar_width, label=f'{user_count} usuários', alpha=0.8)

    ax.set_xlabel('Endpoint', fontsize=12, fontweight='bold')
    ax.set_ylabel('Taxa de Falhas (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'{API_NAME}\nTaxa de Falhas por Endpoint', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(endpoint_data.keys(), rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'failure_rate_comparison.png', dpi=300, bbox_inches='tight')
    print("[OK] Grafico criado: failure_rate_comparison.png")
    plt.close()

def create_percentile_charts(data_by_users):
    """Gráficos de percentis de tempo de resposta para cada endpoint"""
    percentile_cols = ['50%', '66%', '75%', '80%', '90%', '95%', '98%', '99%', '99.9%', '99.99%', '100%']

    # Obter todos os endpoints únicos
    all_endpoints = set()
    for df in data_by_users.values():
        if df is not None:
            all_endpoints.update(df['Name'].unique())

    for endpoint in all_endpoints:
        fig, ax = plt.subplots(figsize=(14, 8))

        for user_count in USER_COUNTS:
            df = data_by_users[user_count]
            if df is not None:
                endpoint_row = df[df['Name'] == endpoint]
                if not endpoint_row.empty:
                    # Extrair valores de percentis
                    percentiles = []
                    percentile_labels = []
                    for col in percentile_cols:
                        if col in endpoint_row.columns:
                            value = endpoint_row[col].values[0]
                            if pd.notna(value):
                                percentiles.append(value)
                                percentile_labels.append(col.replace('%', ''))

                    if percentiles:
                        ax.plot(percentile_labels, percentiles, marker='o',
                               label=f'{user_count} usuários', linewidth=2, markersize=6)

        ax.set_xlabel('Percentil', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tempo de Resposta (ms)', fontsize=12, fontweight='bold')
        ax.set_title(f'{API_NAME}\nDistribuição de Tempo de Resposta - {endpoint}',
                    fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')  # Escala logarítmica para melhor visualização

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Nome do arquivo seguro
        safe_filename = endpoint.replace(' ', '_').replace('/', '_').lower()
        plt.savefig(CHARTS_DIR / f'percentiles_{safe_filename}.png', dpi=300, bbox_inches='tight')
        print(f"[OK] Grafico criado: percentiles_{safe_filename}.png")
        plt.close()

def create_detailed_endpoint_charts(data_by_users):
    """Gráficos detalhados para cada combinação de endpoint e quantidade de usuários"""
    all_endpoints = set()
    for df in data_by_users.values():
        if df is not None:
            all_endpoints.update(df['Name'].unique())

    for endpoint in all_endpoints:
        for user_count in USER_COUNTS:
            df = data_by_users[user_count]
            if df is None:
                continue

            endpoint_row = df[df['Name'] == endpoint]
            if endpoint_row.empty:
                continue

            row = endpoint_row.iloc[0]

            # Criar figura com 2x2 subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(f'{API_NAME}\n{endpoint} - {user_count} Usuários',
                        fontsize=16, fontweight='bold')

            # 1. Estatísticas de tempo de resposta
            metrics = {
                'Mínimo': row['Min Response Time'],
                'Médio': row['Average Response Time'],
                'Máximo': row['Max Response Time'],
                'Mediana': row.get('50%', row['Average Response Time'])
            }
            colors_list = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
            ax1.bar(metrics.keys(), metrics.values(), color=colors_list, alpha=0.7)
            ax1.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
            ax1.set_title('Estatísticas de Tempo de Resposta', fontweight='bold')
            ax1.grid(axis='y', alpha=0.3)

            # 2. Volume de requisições
            req_data = {
                'Sucesso': row['Request Count'] - row['Failure Count'],
                'Falhas': row['Failure Count']
            }
            ax2.bar(req_data.keys(), req_data.values(), color=['#2ecc71', '#e74c3c'], alpha=0.7)
            ax2.set_ylabel('Número de Requisições', fontweight='bold')
            ax2.set_title(f'Total de Requisições: {row["Request Count"]:.0f}', fontweight='bold')
            ax2.grid(axis='y', alpha=0.3)

            # 3. Percentis de latência
            percentile_cols = ['50%', '75%', '90%', '95%', '99%']
            percentiles = []
            percentile_labels = []
            for col in percentile_cols:
                if col in row.index and pd.notna(row[col]):
                    percentiles.append(row[col])
                    percentile_labels.append(col)

            if percentiles:
                ax3.plot(percentile_labels, percentiles, marker='o',
                        linewidth=2, markersize=8, color='#9b59b6')
                ax3.fill_between(range(len(percentiles)), percentiles, alpha=0.3, color='#9b59b6')
                ax3.set_xlabel('Percentil', fontweight='bold')
                ax3.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
                ax3.set_title('Distribuição de Latência (Percentis)', fontweight='bold')
                ax3.grid(True, alpha=0.3)

            # 4. Métricas de performance
            perf_metrics = {
                'Req/s': row['Requests/s'],
                'Falhas/s': row['Failures/s'],
                'Tamanho\nMédio (bytes)': row['Average Content Size']
            }

            # Normalizar valores para visualização (diferentes escalas)
            ax4_twin = ax4.twinx()

            bars1 = ax4.bar([0, 1],
                           [perf_metrics['Req/s'], perf_metrics['Falhas/s']],
                           color=['#3498db', '#e74c3c'], alpha=0.7, width=0.4)
            ax4.set_ylabel('Requisições por Segundo', fontweight='bold')
            ax4.set_title('Métricas de Performance', fontweight='bold')
            ax4.set_xticks([0, 1, 2])
            ax4.set_xticklabels(['Req/s', 'Falhas/s', 'Tamanho\nMédio (bytes)'])

            bars2 = ax4_twin.bar([2],
                                [perf_metrics['Tamanho\nMédio (bytes)']],
                                color='#2ecc71', alpha=0.7, width=0.4)
            ax4_twin.set_ylabel('Tamanho Médio (bytes)', fontweight='bold')

            ax4.grid(axis='y', alpha=0.3)

            plt.tight_layout()

            # Salvar com nome seguro
            safe_endpoint = endpoint.replace(' ', '_').replace('/', '_').lower()
            filename = f'detailed_{safe_endpoint}_{user_count}_users.png'
            plt.savefig(CHARTS_DIR / filename, dpi=300, bbox_inches='tight')
            print(f"[OK] Grafico criado: {filename}")
            plt.close()

def create_summary_table(data_by_users):
    """Cria uma tabela resumo em formato de imagem"""
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.axis('tight')
    ax.axis('off')

    # Preparar dados para a tabela
    table_data = []
    table_data.append(['Endpoint', 'Usuários', 'Requisições', 'Req/s',
                      'Tempo Médio (ms)', 'P95 (ms)', 'P99 (ms)', 'Taxa Falhas (%)'])

    for user_count in USER_COUNTS:
        df = data_by_users[user_count]
        if df is not None:
            for _, row in df.iterrows():
                failure_rate = (row['Failure Count'] / row['Request Count'] * 100) if row['Request Count'] > 0 else 0
                table_data.append([
                    row['Name'],
                    f"{user_count}",
                    f"{row['Request Count']:.0f}",
                    f"{row['Requests/s']:.2f}",
                    f"{row['Average Response Time']:.2f}",
                    f"{row.get('95%', 0):.2f}",
                    f"{row.get('99%', 0):.2f}",
                    f"{failure_rate:.2f}"
                ])

    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.25, 0.1, 0.12, 0.1, 0.15, 0.1, 0.1, 0.13])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Estilizar cabeçalho
    for i in range(len(table_data[0])):
        cell = table[(0, i)]
        cell.set_facecolor('#3498db')
        cell.set_text_props(weight='bold', color='white')

    # Alternar cores das linhas
    for i in range(1, len(table_data)):
        for j in range(len(table_data[0])):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#ecf0f1')

    plt.title(f'{API_NAME}\nResumo dos Testes de Carga',
             fontsize=16, fontweight='bold', pad=20)

    plt.savefig(CHARTS_DIR / 'summary_table.png', dpi=300, bbox_inches='tight')
    print("[OK] Tabela resumo criada: summary_table.png")
    plt.close()

def main():
    print("=" * 60)
    print(f"Gerador de Gráficos - {API_NAME}")
    print("=" * 60)
    print()

    setup_directories()

    # Carregar dados de todos os testes
    print("\nCarregando reports...")
    data_by_users = {}
    for user_count in USER_COUNTS:
        print(f"  Carregando report de {user_count} usuários...")
        data_by_users[user_count] = load_report(user_count)

    # Verificar se há dados
    if all(df is None for df in data_by_users.values()):
        print("\n[ERRO] Nenhum report encontrado!")
        print("Execute os testes primeiro com: ./run_all_tests.sh")
        return

    print("\n" + "=" * 60)
    print("Gerando gráficos...")
    print("=" * 60)
    print()

    # Gerar todos os gráficos
    create_response_time_comparison_chart(data_by_users)
    create_throughput_comparison_chart(data_by_users)
    create_failure_rate_chart(data_by_users)
    create_percentile_charts(data_by_users)
    create_detailed_endpoint_charts(data_by_users)
    create_summary_table(data_by_users)

    print("\n" + "=" * 60)
    print("[OK] Todos os graficos foram gerados com sucesso!")
    print(f"[OK] Graficos salvos em: {CHARTS_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
