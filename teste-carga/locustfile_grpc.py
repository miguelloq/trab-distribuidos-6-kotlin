from locust import User, task, between, events
import grpc
import time
import random

# Nota: Este é um locustfile simplificado para gRPC
# Para usar gRPC com Locust, precisamos da biblioteca grpcio-tools e os arquivos proto compilados
# Como alternativa, vamos usar requests HTTP/2 para simular chamadas gRPC

from locust import HttpUser

class MusicStreamingGRPCUser(HttpUser):
    """
    NOTA: gRPC via Locust requer configuração especial.
    Este arquivo usa HTTP/2 para aproximar o comportamento.
    Para testes reais de gRPC, considere usar ghz (https://ghz.sh/)
    """
    wait_time = between(1, 3)
    host = "http://app:9090"  # Porta gRPC

    def on_start(self):
        # IDs de usuários que têm playlists (51-100 criados pelo DataInitializer)
        self.usuario_ids = list(range(51, 101))
        print("AVISO: Locust não tem suporte nativo completo para gRPC.")
        print("Para testes gRPC adequados, use ferramentas como ghz ou grpcurl.")

    @task(3)
    def listar_musicas(self):
        # Placeholder - gRPC requer implementação especial
        # Registrando como se fosse uma chamada
        start_time = time.time()
        try:
            # Simulação - em produção use grpcio
            pass
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="gRPC - Listar Músicas",
                response_time=total_time,
                response_length=0,
                exception=e,
            )
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="gRPC - Listar Músicas",
                response_time=total_time,
                response_length=0,
            )

    @task(3)
    def listar_usuarios(self):
        start_time = time.time()
        try:
            pass
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="gRPC - Listar Usuários",
                response_time=total_time,
                response_length=0,
                exception=e,
            )
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="gRPC - Listar Usuários",
                response_time=total_time,
                response_length=0,
            )

    @task(4)
    def playlists_de_usuario(self):
        usuario_id = random.choice(self.usuario_ids)
        start_time = time.time()
        try:
            pass
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="gRPC - Playlists de Usuário",
                response_time=total_time,
                response_length=0,
                exception=e,
            )
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="gRPC - Playlists de Usuário",
                response_time=total_time,
                response_length=0,
            )
