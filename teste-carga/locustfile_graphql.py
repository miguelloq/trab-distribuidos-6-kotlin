from locust import HttpUser, task, between
import random
import json

class MusicStreamingGraphQLUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # IDs de usuários que têm playlists (51-100 criados pelo DataInitializer)
        self.usuario_ids = list(range(51, 101))

    @task(3)
    def listar_musicas(self):
        query = """
        query {
            musicas {
                id
                nome
                artista
            }
        }
        """
        self.client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            name="GraphQL - Listar Músicas"
        )

    @task(3)
    def listar_usuarios(self):
        query = """
        query {
            usuarios {
                id
                nome
                idade
            }
        }
        """
        self.client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            name="GraphQL - Listar Usuários"
        )

    @task(4)
    def playlists_de_usuario(self):
        usuario_id = random.choice(self.usuario_ids)
        query = f"""
        query {{
            playlistsPorUsuario(usuarioId: {usuario_id}) {{
                id
                nome
                usuarioId
                usuarioNome
            }}
        }}
        """
        self.client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            name="GraphQL - Playlists de Usuário"
        )
