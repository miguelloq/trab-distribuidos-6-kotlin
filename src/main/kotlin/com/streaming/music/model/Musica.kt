package com.streaming.music.model

import com.fasterxml.jackson.annotation.JsonIgnore
import jakarta.persistence.*

@Entity
@Table(name = "musicas")
data class Musica(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @Column(nullable = false)
    val nome: String,
    
    @Column(nullable = false)
    val artista: String,
    
    @ManyToMany(mappedBy = "musicas")
    @JsonIgnore
    val playlists: MutableList<Playlist> = mutableListOf()
)
