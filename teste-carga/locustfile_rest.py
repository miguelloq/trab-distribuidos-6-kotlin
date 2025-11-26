from locust import HttpUser, task, between
import random

class MusicStreamingRESTUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # IDs de usuários que têm playlists (51-100 criados pelo DataInitializer)
        self.usuario_ids = list(range(51, 101))

    @task(3)
    def listar_musicas(self):
        self.client.get("/api/musicas", name="REST - Listar Músicas")

    @task(3)
    def listar_usuarios(self):
        self.client.get("/api/usuarios", name="REST - Listar Usuários")

    @task(4)
    def playlists_de_usuario(self):
        usuario_id = random.choice(self.usuario_ids)
        self.client.get(
            f"/api/playlists/usuario/{usuario_id}",
            name="REST - Playlists de Usuário"
        )
