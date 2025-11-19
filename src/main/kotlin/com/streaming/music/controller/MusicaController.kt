package com.streaming.music.controller

import com.streaming.music.dto.MusicaDTO
import com.streaming.music.service.MusicaService
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/musicas")
class MusicaController(private val musicaService: MusicaService) {
    
    /**
     * Endpoint 2: Listar os dados de todas as músicas mantidas pelo serviço
     */
    @GetMapping
    fun listarTodas(): ResponseEntity<List<MusicaDTO>> {
        val musicas = musicaService.listarTodas()
        return ResponseEntity.ok(musicas)
    }
    
    @PostMapping
    fun criar(@RequestBody request: CriarMusicaRequest): ResponseEntity<Map<String, Any>> {
        val musica = musicaService.criar(request.nome, request.artista)
        return ResponseEntity.ok(mapOf(
            "id" to musica.id!!,
            "nome" to musica.nome,
            "artista" to musica.artista
        ))
    }
}

data class CriarMusicaRequest(
    val nome: String,
    val artista: String
)
