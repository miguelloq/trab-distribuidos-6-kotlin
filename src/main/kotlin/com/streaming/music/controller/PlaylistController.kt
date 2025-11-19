package com.streaming.music.controller

import com.streaming.music.dto.PlaylistComMusicasDTO
import com.streaming.music.dto.PlaylistDTO
import com.streaming.music.service.PlaylistService
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/playlists")
class PlaylistController(private val playlistService: PlaylistService) {
    
    /**
     * Endpoint 3: Listar os dados de todas as playlists de um determinado usuário
     */
    @GetMapping("/usuario/{usuarioId}")
    fun listarPorUsuario(@PathVariable usuarioId: Long): ResponseEntity<List<PlaylistDTO>> {
        val playlists = playlistService.listarPlaylistsPorUsuario(usuarioId)
        return ResponseEntity.ok(playlists)
    }
    
    /**
     * Endpoint 4: Listar os dados de todas as músicas de uma determinada playlist
     */
    @GetMapping("/{playlistId}/musicas")
    fun listarMusicasDaPlaylist(@PathVariable playlistId: Long): ResponseEntity<PlaylistComMusicasDTO> {
        val playlist = playlistService.listarMusicasDaPlaylist(playlistId)
        return if (playlist != null) {
            ResponseEntity.ok(playlist)
        } else {
            ResponseEntity.notFound().build()
        }
    }
}
