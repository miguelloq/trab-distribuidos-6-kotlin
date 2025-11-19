package com.streaming.music.service

import com.streaming.music.dto.MusicaDTO
import com.streaming.music.dto.PlaylistComMusicasDTO
import com.streaming.music.dto.PlaylistDTO
import com.streaming.music.repository.PlaylistRepository
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
class PlaylistService(private val playlistRepository: PlaylistRepository) {
    
    @Transactional(readOnly = true)
    fun listarPlaylistsPorUsuario(usuarioId: Long): List<PlaylistDTO> {
        return playlistRepository.findByUsuarioId(usuarioId).map { playlist ->
            PlaylistDTO(
                id = playlist.id,
                nome = playlist.nome,
                usuarioId = playlist.usuario.id!!,
                usuarioNome = playlist.usuario.nome
            )
        }
    }
    
    @Transactional(readOnly = true)
    fun listarMusicasDaPlaylist(playlistId: Long): PlaylistComMusicasDTO? {
        val playlist = playlistRepository.findById(playlistId).orElse(null) ?: return null
        
        return PlaylistComMusicasDTO(
            id = playlist.id,
            nome = playlist.nome,
            musicas = playlist.musicas.map { musica ->
                MusicaDTO(
                    id = musica.id,
                    nome = musica.nome,
                    artista = musica.artista
                )
            }
        )
    }
}
