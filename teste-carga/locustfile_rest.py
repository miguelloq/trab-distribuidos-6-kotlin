"""
Locust test file for REST API endpoints
Testa 3 funcionalidades: listar músicas, listar usuários, listar músicas de uma playlist
"""
from locust import HttpUser, task, between
import random

# IDs de playlists válidas (400 playlists, IDs de 1 a 400)
VALID_PLAYLIST_IDS = list(range(1, 401))

class RestApiUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://app:8080"

    def on_start(self):
        """Executado quando um usuário virtual inicia"""
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @task(3)
    def listar_todas_musicas(self):
        """Task 1: Listar todas as músicas (1000 músicas)"""
        with self.client.get(
            "/api/musicas",
            headers=self.headers,
            catch_response=True,
            name="REST - Listar Todas Músicas"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(3)
    def listar_todos_usuarios(self):
        """Task 2: Listar todos os usuários (200 usuários)"""
        with self.client.get(
            "/api/usuarios",
            headers=self.headers,
            catch_response=True,
            name="REST - Listar Todos Usuários"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(4)
    def listar_musicas_playlist(self):
        """Task 3: Listar músicas de uma playlist (cada playlist tem ~100 músicas)"""
        playlist_id = random.choice(VALID_PLAYLIST_IDS)
        with self.client.get(
            f"/api/playlists/{playlist_id}/musicas",
            headers=self.headers,
            catch_response=True,
            name="REST - Listar Músicas de Playlist"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code} for playlist {playlist_id}")
