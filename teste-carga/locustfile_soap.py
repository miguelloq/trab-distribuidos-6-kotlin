from locust import HttpUser, task, between
import random

class MusicStreamingSOAPUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # IDs de usuários que têm playlists (51-100 criados pelo DataInitializer)
        self.usuario_ids = list(range(51, 101))

    @task(3)
    def listar_musicas(self):
        soap_body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:soap="http://streaming.com/music/soap">
    <soapenv:Header/>
    <soapenv:Body>
        <soap:listarMusicasRequest/>
    </soapenv:Body>
</soapenv:Envelope>"""

        self.client.post(
            "/ws",
            data=soap_body,
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": ""
            },
            name="SOAP - Listar Músicas"
        )

    @task(3)
    def listar_usuarios(self):
        soap_body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:soap="http://streaming.com/music/soap">
    <soapenv:Header/>
    <soapenv:Body>
        <soap:listarUsuariosRequest/>
    </soapenv:Body>
</soapenv:Envelope>"""

        self.client.post(
            "/ws",
            data=soap_body,
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": ""
            },
            name="SOAP - Listar Usuários"
        )

    @task(4)
    def playlists_de_usuario(self):
        usuario_id = random.choice(self.usuario_ids)
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:soap="http://streaming.com/music/soap">
    <soapenv:Header/>
    <soapenv:Body>
        <soap:listarPlaylistsPorUsuarioRequest>
            <soap:usuarioId>{usuario_id}</soap:usuarioId>
        </soap:listarPlaylistsPorUsuarioRequest>
    </soapenv:Body>
</soapenv:Envelope>"""

        self.client.post(
            "/ws",
            data=soap_body,
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": ""
            },
            name="SOAP - Playlists de Usuário"
        )
