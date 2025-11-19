package com.streaming.music.service

import com.streaming.music.dto.MusicaDTO
import com.streaming.music.model.Musica
import com.streaming.music.repository.MusicaRepository
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
class MusicaService(private val musicaRepository: MusicaRepository) {
    
    @Transactional(readOnly = true)
    fun listarTodas(): List<MusicaDTO> {
        return musicaRepository.findAll().map { musica ->
            MusicaDTO(
                id = musica.id,
                nome = musica.nome,
                artista = musica.artista
            )
        }
    }
    
    @Transactional
    fun criar(nome: String, artista: String): Musica {
        val musica = Musica(nome = nome, artista = artista)
        return musicaRepository.save(musica)
    }
}
