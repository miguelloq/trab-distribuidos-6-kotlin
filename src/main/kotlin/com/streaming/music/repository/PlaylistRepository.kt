package com.streaming.music.repository

import com.streaming.music.model.Playlist
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.data.repository.query.Param
import org.springframework.stereotype.Repository

@Repository
interface PlaylistRepository : JpaRepository<Playlist, Long> {
    
    @Query("SELECT p FROM Playlist p WHERE p.usuario.id = :usuarioId")
    fun findByUsuarioId(@Param("usuarioId") usuarioId: Long): List<Playlist>
    
    @Query("SELECT p FROM Playlist p JOIN p.musicas m WHERE m.id = :musicaId")
    fun findByMusicaId(@Param("musicaId") musicaId: Long): List<Playlist>
}
