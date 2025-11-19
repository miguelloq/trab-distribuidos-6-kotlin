package com.streaming.music

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class MusicStreamingApplication

fun main(args: Array<String>) {
    runApplication<MusicStreamingApplication>(*args)
}
