"""
Locust test file for SOAP API endpoints
Testa 3 funcionalidades: listar músicas, listar usuários, listar músicas de uma playlist
"""
from locust import HttpUser, task, between
import random

# IDs de playlists válidas (400 playlists, IDs de 1 a 400)
VALID_PLAYLIST_IDS = list(range(1, 401))

# Namespace do SOAP
SOAP_NAMESPACE = "http://streaming.com/music/soap"

class SoapApiUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://app:8080"

    def on_start(self):
        """Executado quando um usuário virtual inicia"""
        self.headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": ""
        }
        self.soap_endpoint = "/api/ws"

    @task(3)
    def listar_todas_musicas(self):
        """Task 1: Listar todas as músicas (1000 músicas)"""
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:mus="{SOAP_NAMESPACE}">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:listarMusicasRequest/>
   </soapenv:Body>
</soapenv:Envelope>"""

        with self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            catch_response=True,
            name="SOAP - Listar Todas Músicas"
        ) as response:
            if response.status_code == 200 and b"musicas" in response.content:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(3)
    def listar_todos_usuarios(self):
        """Task 2: Listar todos os usuários (200 usuários)"""
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:mus="{SOAP_NAMESPACE}">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:listarUsuariosRequest/>
   </soapenv:Body>
</soapenv:Envelope>"""

        with self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            catch_response=True,
            name="SOAP - Listar Todos Usuários"
        ) as response:
            if response.status_code == 200 and b"usuarios" in response.content:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(4)
    def listar_musicas_playlist(self):
        """Task 3: Listar músicas de uma playlist (cada playlist tem ~100 músicas)"""
        playlist_id = random.choice(VALID_PLAYLIST_IDS)
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:mus="{SOAP_NAMESPACE}">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:listarMusicasDaPlaylistRequest>
         <mus:playlistId>{playlist_id}</mus:playlistId>
      </mus:listarMusicasDaPlaylistRequest>
   </soapenv:Body>
</soapenv:Envelope>"""

        with self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            catch_response=True,
            name="SOAP - Listar Músicas de Playlist"
        ) as response:
            if response.status_code == 200 and b"musicas" in response.content:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code} for playlist {playlist_id}")
