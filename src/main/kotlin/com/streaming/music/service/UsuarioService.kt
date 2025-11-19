package com.streaming.music.service

import com.streaming.music.dto.UsuarioDTO
import com.streaming.music.model.Usuario
import com.streaming.music.repository.UsuarioRepository
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
class UsuarioService(private val usuarioRepository: UsuarioRepository) {
    
    @Transactional(readOnly = true)
    fun listarTodos(): List<UsuarioDTO> {
        return usuarioRepository.findAll().map { usuario ->
            UsuarioDTO(
                id = usuario.id,
                nome = usuario.nome,
                idade = usuario.idade
            )
        }
    }
    
    @Transactional
    fun criar(nome: String, idade: Int): Usuario {
        val usuario = Usuario(nome = nome, idade = idade)
        return usuarioRepository.save(usuario)
    }
}
