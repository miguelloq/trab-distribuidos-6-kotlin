package com.streaming.music.repository

import com.streaming.music.model.Musica
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface MusicaRepository : JpaRepository<Musica, Long>
