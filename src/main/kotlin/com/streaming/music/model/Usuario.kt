package com.streaming.music.model

import com.fasterxml.jackson.annotation.JsonManagedReference
import jakarta.persistence.*

@Entity
@Table(name = "usuarios")
data class Usuario(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @Column(nullable = false)
    val nome: String,
    
    @Column(nullable = false)
    val idade: Int,
    
    @OneToMany(mappedBy = "usuario", cascade = [CascadeType.ALL], orphanRemoval = true)
    @JsonManagedReference
    val playlists: MutableList<Playlist> = mutableListOf()
)
