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
import kotlin.random.Random

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
        if (usuarioRepository.count() > 0) {
            logger.info("Dados já existem no banco. Pulando inicialização.")
            return
        }

        logger.info("Inicializando dados mockados...")

        // Gerar 200 nomes de usuários
        val primeirosNomes = listOf(
            "João", "Maria", "Pedro", "Ana", "Carlos", "Julia", "Lucas", "Beatriz", "Rafael", "Fernanda",
            "Gabriel", "Camila", "Felipe", "Larissa", "Bruno", "Amanda", "Rodrigo", "Juliana", "Thiago", "Patricia",
            "Daniel", "Mariana", "Diego", "Isabela", "Leonardo", "Carolina", "Mateus", "Leticia", "Vinicius", "Natalia",
            "Gustavo", "Bianca", "Henrique", "Rafaela", "Marcos", "Aline", "Paulo", "Sabrina", "Ricardo", "Vanessa",
            "Eduardo", "Jessica", "Fábio", "Priscila", "André", "Tatiana", "Renato", "Giovanna", "Marcelo", "Claudia",
            "Alessandro", "Adriana", "Alexandre", "Alice", "Anderson", "Andrea", "Antonio", "Angelica", "Augusto", "Barbara",
            "Bernardo", "Bruna", "Caio", "Carla", "Cesar", "Cristina", "Danilo", "Daniela", "Denis", "Denise",
            "Edson", "Elaine", "Emerson", "Elisa", "Erick", "Erica", "Everton", "Evelyn", "Fabricio", "Fabiana",
            "Fernando", "Flavia", "Francisco", "Gabriela", "Guilherme", "Giovana", "Heitor", "Helena", "Hugo", "Heloisa",
            "Igor", "Ingrid", "Ivan", "Iris", "Jair", "Janaina", "Jean", "Jennifer", "Jose", "Joana"
        )

        val sobrenomes = listOf(
            "Silva", "Santos", "Oliveira", "Costa", "Souza", "Ferreira", "Almeida", "Lima", "Gomes", "Ribeiro",
            "Martins", "Rodrigues", "Carvalho", "Barbosa", "Pereira", "Araujo", "Nascimento", "Rocha", "Mendes", "Dias",
            "Castro", "Cardoso", "Monteiro", "Nunes", "Ramos", "Freitas", "Teixeira", "Moreira", "Pinto", "Batista",
            "Vieira", "Correia", "Fernandes", "Cavalcanti", "Azevedo", "Melo", "Barros", "Campos", "Miranda", "Moura",
            "Soares", "Santana", "Machado", "Lopes", "Cunha", "Nogueira", "Cruz", "Farias", "Duarte", "Borges"
        )

        val nomes = mutableListOf<String>()
        for (i in 0 until 200) {
            nomes.add("${primeirosNomes[i % primeirosNomes.size]} ${sobrenomes[i % sobrenomes.size]}")
        }

        val usuarios = mutableListOf<Usuario>()
        logger.info("Criando 200 usuários...")
        for (i in 0 until 200) {
            val usuario = usuarioRepository.save(Usuario(nome = nomes[i], idade = Random.nextInt(18, 65)))
            usuarios.add(usuario)
        }
        logger.info("Criados 200 usuários")

        // Músicas base (200 músicas famosas)
        val musicasBase = listOf(
            "Bohemian Rhapsody", "Stairway to Heaven", "Hotel California", "Smells Like Teen Spirit", "Sweet Child O' Mine",
            "Back in Black", "Comfortably Numb", "November Rain", "Imagine", "Hey Jude",
            "Let It Be", "Yesterday", "Come Together", "While My Guitar Gently Weeps", "Here Comes the Sun",
            "Purple Rain", "Like a Rolling Stone", "Satisfaction", "Paint It Black", "Sympathy for the Devil",
            "Gimme Shelter", "Angie", "Brown Sugar", "Start Me Up", "Miss You",
            "Don't Stop Believin'", "Any Way You Want It", "Faithfully", "Separate Ways", "Open Arms",
            "Kashmir", "Black Dog", "Whole Lotta Love", "Rock and Roll", "Immigrant Song",
            "Free Bird", "Simple Man", "Sweet Home Alabama", "Tuesday's Gone", "Gimme Three Steps",
            "Dream On", "Walk This Way", "Sweet Emotion", "I Don't Want to Miss a Thing", "Crazy",
            "Born to Run", "Thunder Road", "Dancing in the Dark", "The River", "Streets of Philadelphia",
            "One", "Enter Sandman", "Nothing Else Matters", "Master of Puppets", "Fade to Black",
            "Welcome to the Jungle", "Paradise City", "Patience", "Don't Cry", "Knockin' on Heaven's Door",
            "Livin' on a Prayer", "You Give Love a Bad Name", "Wanted Dead or Alive", "It's My Life", "Bad Medicine",
            "Another Brick in the Wall", "Wish You Were Here", "Time", "Money", "Shine On You Crazy Diamond",
            "Under Pressure", "Killer Queen", "Don't Stop Me Now", "We Are the Champions", "Radio Ga Ga",
            "Sweet Dreams", "Here I Go Again", "Is This Love", "Still of the Night", "Fool for Your Loving",
            "The Final Countdown", "Carrie", "Rock the Night", "Superstitious", "Cherokee",
            "Africa", "Hold the Line", "Rosanna", "I Won't Hold You Back", "Georgy Porgy",
            "Eye of the Tiger", "Burning Heart", "High on You", "I Can't Hold Back", "The Search Is Over",
            "More Than a Feeling", "Peace of Mind", "Foreplay/Long Time", "Rock & Roll Band", "Smokin'",
            "Carry On Wayward Son", "Dust in the Wind", "Point of Know Return", "Play the Game Tonight", "Hold On",
            "Roundabout", "Owner of a Lonely Heart", "Long Distance Runaround", "I've Seen All Good People", "Starship Trooper",
            "Tom Sawyer", "Limelight", "The Spirit of Radio", "Closer to the Heart", "Subdivisions",
            "Run to the Hills", "The Number of the Beast", "Hallowed Be Thy Name", "Fear of the Dark", "The Trooper",
            "Ace of Spades", "Overkill", "Killed by Death", "Bomber", "Motorhead",
            "Breaking the Law", "Living After Midnight", "You've Got Another Thing Comin'", "Painkiller", "Electric Eye",
            "Rainbow in the Dark", "Holy Diver", "The Last in Line", "We Rock", "Stand Up and Shout",
            "Man on the Silver Mountain", "Since You Been Gone", "Stone Cold", "Street of Dreams", "Spotlight Kid",
            "Bark at the Moon", "Crazy Train", "Mr. Crowley", "Flying High Again", "Shot in the Dark",
            "Highway to Hell", "T.N.T.", "You Shook Me All Night Long", "Thunderstruck", "Shoot to Thrill",
            "Smoke on the Water", "Highway Star", "Child in Time", "Perfect Strangers", "Burn",
            "Paranoid", "Iron Man", "War Pigs", "N.I.B.", "Fairies Wear Boots",
            "Sharp Dressed Man", "La Grange", "Tush", "Legs", "Gimme All Your Lovin'",
            "American Woman", "No Sugar Tonight", "These Eyes", "Undun", "Share the Land",
            "Spirit in the Sky", "In the Year 2525", "The Pusher", "Magic Carpet Ride", "Born to Be Wild",
            "All Right Now", "Fire and Water", "Wishing Well", "My Brother Jake", "The Hunter",
            "Black Magic Woman", "Oye Como Va", "Europa", "Evil Ways", "Samba Pa Ti",
            "Long Train Runnin'", "China Grove", "Listen to the Music", "Black Water", "Takin' It to the Streets",
            "Jessica", "Ramblin' Man", "Midnight Rider", "Blue Sky", "Melissa",
            "Blue Collar Man", "Come Sail Away", "Renegade", "Lady", "Babe"
        )

        // Gerar 1000 músicas (200 base + 800 geradas)
        val musicasNomes = mutableListOf<String>()
        musicasNomes.addAll(musicasBase)

        // Adicionar músicas geradas para completar 1000
        val generos = listOf("Rock", "Pop", "Blues", "Jazz", "Metal", "Country", "Folk", "Indie", "Punk", "Alternative")
        val adjetivos = listOf("Electric", "Acoustic", "Live", "Remix", "Unplugged", "Studio", "Classic", "Modern", "Vintage", "New")

        for (i in musicasBase.size until 1000) {
            val musicaNome = when {
                i < 400 -> "${generos[i % generos.size]} Song ${i - musicasBase.size + 1}"
                i < 600 -> "${adjetivos[i % adjetivos.size]} ${generos[i % generos.size]} ${i - 399}"
                i < 800 -> "Track ${i - 599} - ${generos[i % generos.size]}"
                else -> "Original Song ${i - 799}"
            }
            musicasNomes.add(musicaNome)
        }

        val artistas = listOf(
            "Queen", "Led Zeppelin", "Eagles", "Nirvana", "Guns N' Roses",
            "AC/DC", "Pink Floyd", "The Beatles", "Prince", "The Rolling Stones",
            "Journey", "Lynyrd Skynyrd", "Aerosmith", "Bruce Springsteen", "Metallica",
            "Bon Jovi", "Whitesnake", "Europe", "Toto", "Survivor",
            "Boston", "Kansas", "Yes", "Rush", "Iron Maiden",
            "Motörhead", "Judas Priest", "Dio", "Rainbow", "Ozzy Osbourne",
            "Deep Purple", "Black Sabbath", "ZZ Top", "The Guess Who", "Norman Greenbaum",
            "Free", "Santana", "U2", "Coldplay", "Radiohead",
            "Foo Fighters", "Red Hot Chili Peppers", "Pearl Jam", "Soundgarden", "Alice in Chains",
            "The Who", "The Doors", "Jimi Hendrix", "Cream", "Eric Clapton",
            "David Bowie", "Elton John", "Billy Joel", "Paul McCartney", "John Lennon",
            "R.E.M.", "The Cure", "Depeche Mode", "New Order", "The Smiths",
            "Oasis", "Blur", "Pulp", "Suede", "The Verve",
            "Green Day", "Blink-182", "The Offspring", "Sum 41", "Simple Plan",
            "Linkin Park", "System of a Down", "Disturbed", "Slipknot", "Korn",
            "Pantera", "Megadeth", "Slayer", "Anthrax", "Testament",
            "Dream Theater", "Tool", "A Perfect Circle", "Porcupine Tree", "Opeth",
            "The Strokes", "Arctic Monkeys", "Franz Ferdinand", "The Killers", "Muse",
            "Kings of Leon", "The Black Keys", "Cage the Elephant", "Imagine Dragons", "Twenty One Pilots"
        )

        val musicas = mutableListOf<Musica>()
        logger.info("Criando 1000 músicas...")
        for (i in 0 until 1000) {
            val musica = musicaRepository.save(
                Musica(
                    nome = musicasNomes[i],
                    artista = artistas[Random.nextInt(artistas.size)]
                )
            )
            musicas.add(musica)
            if ((i + 1) % 100 == 0) {
                logger.info("  Criadas ${i + 1} músicas...")
            }
        }
        logger.info("Criadas 1000 músicas")

        val playlistNomes = listOf(
            "Rock Clássico", "Anos 90", "Favoritas", "Para Treinar", "Relaxar",
            "Trabalho", "Festa", "Viagem", "Nostalgia", "Top Hits",
            "Acústico", "Metal Pesado", "Blues", "Jazz", "Pop Rock",
            "Indie", "Punk Rock", "Hard Rock", "Soft Rock", "Progressive Rock"
        )

        var playlistCount = 0
        logger.info("Criando playlists (2 por usuário, ~100 músicas cada)...")
        usuarios.forEachIndexed { index, usuario ->
            // Primeira playlist
            val playlist1 = Playlist(
                nome = "${playlistNomes[Random.nextInt(playlistNomes.size)]} - ${usuario.nome.split(" ")[0]}",
                usuario = usuario
            )
            // Adiciona de 90 a 110 músicas aleatórias
            val musicasAleatorias1 = musicas.shuffled().take(Random.nextInt(90, 111))
            playlist1.musicas.addAll(musicasAleatorias1)
            playlistRepository.save(playlist1)
            playlistCount++

            // Segunda playlist
            val playlist2 = Playlist(
                nome = "${playlistNomes[Random.nextInt(playlistNomes.size)]} - ${usuario.nome.split(" ")[0]} 2",
                usuario = usuario
            )
            // Adiciona de 90 a 110 músicas aleatórias diferentes
            val musicasAleatorias2 = musicas.shuffled().take(Random.nextInt(90, 111))
            playlist2.musicas.addAll(musicasAleatorias2)
            playlistRepository.save(playlist2)
            playlistCount++

            if ((index + 1) % 50 == 0) {
                logger.info("  Criadas playlists para ${index + 1} usuários...")
            }
        }

        logger.info("Dados mockados criados com sucesso!")
        logger.info("- 200 usuários")
        logger.info("- 1000 músicas")
        logger.info("- $playlistCount playlists (2 por usuário, ~100 músicas cada)")
    }
}
