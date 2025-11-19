package com.streaming.music.config

import com.streaming.music.model.Musica
import com.streaming.music.model.Playlist
import com.streaming.music.model.Usuario
import com.streaming.music.repository.MusicaRepository
import com.streaming.music.repository.PlaylistRepository
import com.streaming.music.repository.UsuarioRepository
import org.springframework.boot.CommandLineRunner
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.transaction.annotation.Transactional
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service

@Configuration
class DataInitializer(private val dataInitializerService: DataInitializerService) {

    @Bean
    fun initData(): CommandLineRunner {
        return CommandLineRunner {
            dataInitializerService.initializeData()
        }
    }
}

@Service
class DataInitializerService(
    private val usuarioRepository: UsuarioRepository,
    private val musicaRepository: MusicaRepository,
    private val playlistRepository: PlaylistRepository
) {
    private val logger = LoggerFactory.getLogger(DataInitializerService::class.java)

    @Transactional
    fun initializeData() {
        // Verifica se já existem dados
        if (usuarioRepository.count() > 0) {
            logger.info("Dados já existem no banco. Pulando inicialização.")
            return
        }

        logger.info("Inicializando dados mockados...")

        // Criar usuários
        val usuario1 = usuarioRepository.save(Usuario(nome = "João Silva", idade = 25))
        val usuario2 = usuarioRepository.save(Usuario(nome = "Maria Santos", idade = 30))
        val usuario3 = usuarioRepository.save(Usuario(nome = "Pedro Oliveira", idade = 22))

        // Criar músicas
        val musica1 = musicaRepository.save(Musica(nome = "Bohemian Rhapsody", artista = "Queen"))
        val musica2 = musicaRepository.save(Musica(nome = "Stairway to Heaven", artista = "Led Zeppelin"))
        val musica3 = musicaRepository.save(Musica(nome = "Hotel California", artista = "Eagles"))
        val musica4 = musicaRepository.save(Musica(nome = "Smells Like Teen Spirit", artista = "Nirvana"))
        val musica5 = musicaRepository.save(Musica(nome = "Sweet Child O' Mine", artista = "Guns N' Roses"))
        val musica6 = musicaRepository.save(Musica(nome = "Back in Black", artista = "AC/DC"))
        val musica7 = musicaRepository.save(Musica(nome = "Comfortably Numb", artista = "Pink Floyd"))
        val musica8 = musicaRepository.save(Musica(nome = "November Rain", artista = "Guns N' Roses"))

        // Criar playlists para usuário 1
        val playlist1 = Playlist(nome = "Rock Clássico", usuario = usuario1)
        playlist1.musicas.addAll(listOf(musica1, musica2, musica3))
        playlistRepository.save(playlist1)

        val playlist2 = Playlist(nome = "Anos 90", usuario = usuario1)
        playlist2.musicas.addAll(listOf(musica4, musica5))
        playlistRepository.save(playlist2)

        // Criar playlists para usuário 2
        val playlist3 = Playlist(nome = "Favoritas", usuario = usuario2)
        playlist3.musicas.addAll(listOf(musica1, musica5, musica6, musica7))
        playlistRepository.save(playlist3)

        // Criar playlist para usuário 3
        val playlist4 = Playlist(nome = "Para Treinar", usuario = usuario3)
        playlist4.musicas.addAll(listOf(musica4, musica6, musica8))
        playlistRepository.save(playlist4)

        logger.info("Dados mockados criados com sucesso!")
        logger.info("- 3 usuários")
        logger.info("- 8 músicas")
        logger.info("- 4 playlists")
    }
}
