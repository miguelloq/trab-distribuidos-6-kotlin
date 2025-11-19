package com.streaming.music.graphql

import com.streaming.music.dto.MusicaDTO
import com.streaming.music.dto.PlaylistComMusicasDTO
import com.streaming.music.dto.PlaylistDTO
import com.streaming.music.dto.UsuarioDTO
import com.streaming.music.service.MusicaService
import com.streaming.music.service.PlaylistService
import com.streaming.music.service.UsuarioService
import org.springframework.graphql.data.method.annotation.Argument
import org.springframework.graphql.data.method.annotation.QueryMapping
import org.springframework.stereotype.Controller

/**
 * Controller GraphQL para o serviço de streaming de música.
 *
 * Endpoint: POST /graphql
 * GraphiQL UI: /graphiql (para testes)
 */
@Controller
class MusicStreamingGraphQLController(
    private val usuarioService: UsuarioService,
    private val musicaService: MusicaService,
    private val playlistService: PlaylistService
) {

    /**
     * Query: Listar todos os usuários do serviço
     *
     * Exemplo de query:
     * query {
     *   usuarios {
     *     id
     *     nome
     *     idade
     *   }
     * }
     */
    @QueryMapping
    fun usuarios(): List<UsuarioDTO> {
        return usuarioService.listarTodos()
    }

    /**
     * Query: Listar todas as músicas mantidas pelo serviço
     *
     * Exemplo de query:
     * query {
     *   musicas {
     *     id
     *     nome
     *     artista
     *   }
     * }
     */
    @QueryMapping
    fun musicas(): List<MusicaDTO> {
        return musicaService.listarTodas()
    }

    /**
     * Query: Listar todas as playlists de um determinado usuário
     *
     * Exemplo de query:
     * query {
     *   playlistsPorUsuario(usuarioId: "1") {
     *     id
     *     nome
     *     usuarioId
     *     usuarioNome
     *   }
     * }
     */
    @QueryMapping
    fun playlistsPorUsuario(@Argument usuarioId: Long): List<PlaylistDTO> {
        return playlistService.listarPlaylistsPorUsuario(usuarioId)
    }

    /**
     * Query: Listar todas as músicas de uma determinada playlist
     *
     * Exemplo de query:
     * query {
     *   musicasDaPlaylist(playlistId: "1") {
     *     id
     *     nome
     *     musicas {
     *       id
     *       nome
     *       artista
     *     }
     *   }
     * }
     */
    @QueryMapping
    fun musicasDaPlaylist(@Argument playlistId: Long): PlaylistComMusicasDTO? {
        return playlistService.listarMusicasDaPlaylist(playlistId)
    }
}
