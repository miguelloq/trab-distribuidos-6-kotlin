package com.streaming.music.soap

import com.streaming.music.service.MusicaService
import com.streaming.music.service.PlaylistService
import com.streaming.music.service.UsuarioService
import jakarta.xml.bind.annotation.*
import org.springframework.ws.server.endpoint.annotation.Endpoint
import org.springframework.ws.server.endpoint.annotation.PayloadRoot
import org.springframework.ws.server.endpoint.annotation.RequestPayload
import org.springframework.ws.server.endpoint.annotation.ResponsePayload

/**
 * Endpoint SOAP para o serviço de streaming de música.
 *
 * WSDL disponível em: http://localhost:8080/ws/musicStreaming.wsdl
 * Endpoint SOAP: http://localhost:8080/ws
 */
@Endpoint
class MusicStreamingSoapEndpoint(
    private val usuarioService: UsuarioService,
    private val musicaService: MusicaService,
    private val playlistService: PlaylistService
) {

    companion object {
        const val NAMESPACE_URI = "http://streaming.com/music/soap"
    }

    /**
     * Listar todos os usuários do serviço
     */
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "listarUsuariosRequest")
    @ResponsePayload
    fun listarUsuarios(@RequestPayload request: ListarUsuariosRequest): ListarUsuariosResponse {
        val usuarios = usuarioService.listarTodos()

        return ListarUsuariosResponse().apply {
            this.usuarios = usuarios.map { usuario ->
                UsuarioSoap().apply {
                    id = usuario.id ?: 0
                    nome = usuario.nome
                    idade = usuario.idade
                }
            }
        }
    }

    /**
     * Listar todas as músicas mantidas pelo serviço
     */
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "listarMusicasRequest")
    @ResponsePayload
    fun listarMusicas(@RequestPayload request: ListarMusicasRequest): ListarMusicasResponse {
        val musicas = musicaService.listarTodas()

        return ListarMusicasResponse().apply {
            this.musicas = musicas.map { musica ->
                MusicaSoap().apply {
                    id = musica.id ?: 0
                    nome = musica.nome
                    artista = musica.artista
                }
            }
        }
    }

    /**
     * Listar todas as playlists de um determinado usuário
     */
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "listarPlaylistsPorUsuarioRequest")
    @ResponsePayload
    fun listarPlaylistsPorUsuario(@RequestPayload request: ListarPlaylistsPorUsuarioRequest): ListarPlaylistsPorUsuarioResponse {
        val playlists = playlistService.listarPlaylistsPorUsuario(request.usuarioId)

        return ListarPlaylistsPorUsuarioResponse().apply {
            this.playlists = playlists.map { playlist ->
                PlaylistSoap().apply {
                    id = playlist.id ?: 0
                    nome = playlist.nome
                    usuarioId = playlist.usuarioId
                    usuarioNome = playlist.usuarioNome
                }
            }
        }
    }

    /**
     * Listar todas as músicas de uma determinada playlist
     */
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "listarMusicasDaPlaylistRequest")
    @ResponsePayload
    fun listarMusicasDaPlaylist(@RequestPayload request: ListarMusicasDaPlaylistRequest): ListarMusicasDaPlaylistResponse {
        val playlist = playlistService.listarMusicasDaPlaylist(request.playlistId)

        return ListarMusicasDaPlaylistResponse().apply {
            if (playlist != null) {
                this.playlist = PlaylistComMusicasSoap().apply {
                    id = playlist.id ?: 0
                    nome = playlist.nome
                    musicas = playlist.musicas.map { musica ->
                        MusicaSoap().apply {
                            id = musica.id ?: 0
                            nome = musica.nome
                            artista = musica.artista
                        }
                    }
                }
            }
        }
    }
}

// ===================================
// Classes JAXB para Request/Response
// ===================================

@XmlRootElement(name = "listarUsuariosRequest", namespace = MusicStreamingSoapEndpoint.NAMESPACE_URI)
@XmlAccessorType(XmlAccessType.FIELD)
class ListarUsuariosRequest

@XmlRootElement(name = "listarUsuariosResponse", namespace = MusicStreamingSoapEndpoint.NAMESPACE_URI)
@XmlAccessorType(XmlAccessType.FIELD)
class ListarUsuariosResponse {
    @XmlElement(name = "usuarios")
    var usuarios: List<UsuarioSoap> = emptyList()
}

@XmlRootElement(name = "listarMusicasRequest", namespace = MusicStreamingSoapEndpoint.NAMESPACE_URI)
@XmlAccessorType(XmlAccessType.FIELD)
class ListarMusicasRequest

@XmlRootElement(name = "listarMusicasResponse", namespace = MusicStreamingSoapEndpoint.NAMESPACE_URI)
@XmlAccessorType(XmlAccessType.FIELD)
class ListarMusicasResponse {
    @XmlElement(name = "musicas")
    var musicas: List<MusicaSoap> = emptyList()
}

@XmlRootElement(name = "listarPlaylistsPorUsuarioRequest", namespace = MusicStreamingSoapEndpoint.NAMESPACE_URI)
@XmlAccessorType(XmlAccessType.FIELD)
class ListarPlaylistsPorUsuarioRequest {
    @XmlElement(required = true)
    var usuarioId: Long = 0
}

@XmlRootElement(name = "listarPlaylistsPorUsuarioResponse", namespace = MusicStreamingSoapEndpoint.NAMESPACE_URI)
@XmlAccessorType(XmlAccessType.FIELD)
class ListarPlaylistsPorUsuarioResponse {
    @XmlElement(name = "playlists")
    var playlists: List<PlaylistSoap> = emptyList()
}

@XmlRootElement(name = "listarMusicasDaPlaylistRequest", namespace = MusicStreamingSoapEndpoint.NAMESPACE_URI)
@XmlAccessorType(XmlAccessType.FIELD)
class ListarMusicasDaPlaylistRequest {
    @XmlElement(required = true)
    var playlistId: Long = 0
}

@XmlRootElement(name = "listarMusicasDaPlaylistResponse", namespace = MusicStreamingSoapEndpoint.NAMESPACE_URI)
@XmlAccessorType(XmlAccessType.FIELD)
class ListarMusicasDaPlaylistResponse {
    @XmlElement(name = "playlist")
    var playlist: PlaylistComMusicasSoap? = null
}

// ===================================
// Classes JAXB para tipos de dados
// ===================================

@XmlAccessorType(XmlAccessType.FIELD)
class UsuarioSoap {
    var id: Long = 0
    var nome: String = ""
    var idade: Int = 0
}

@XmlAccessorType(XmlAccessType.FIELD)
class MusicaSoap {
    var id: Long = 0
    var nome: String = ""
    var artista: String = ""
}

@XmlAccessorType(XmlAccessType.FIELD)
class PlaylistSoap {
    var id: Long = 0
    var nome: String = ""
    var usuarioId: Long = 0
    var usuarioNome: String = ""
}

@XmlAccessorType(XmlAccessType.FIELD)
class PlaylistComMusicasSoap {
    var id: Long = 0
    var nome: String = ""
    @XmlElement(name = "musicas")
    var musicas: List<MusicaSoap> = emptyList()
}
