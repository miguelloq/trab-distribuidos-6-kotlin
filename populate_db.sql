-- Script de População do Banco de Dados
-- Execute após subir a aplicação pela primeira vez

-- Inserir usuários
INSERT INTO usuarios (nome, idade) VALUES 
  ('João Silva', 25),
  ('Maria Santos', 30),
  ('Pedro Costa', 22);

-- Inserir músicas
INSERT INTO musicas (nome, artista) VALUES 
  ('Bohemian Rhapsody', 'Queen'),
  ('Stairway to Heaven', 'Led Zeppelin'),
  ('Hotel California', 'Eagles'),
  ('Sweet Child O Mine', 'Guns N Roses'),
  ('Smells Like Teen Spirit', 'Nirvana'),
  ('Imagine', 'John Lennon'),
  ('Hey Jude', 'The Beatles'),
  ('One', 'Metallica');

-- Inserir playlists
INSERT INTO playlists (nome, usuario_id) VALUES 
  ('Rock Clássico', 1),
  ('Favoritas', 1),
  ('Músicas Antigas', 2),
  ('Heavy Metal', 3);

-- Relacionar músicas com playlists
-- Playlist 1: Rock Clássico (João)
INSERT INTO playlist_musica (playlist_id, musica_id) VALUES 
  (1, 1), -- Bohemian Rhapsody
  (1, 2), -- Stairway to Heaven
  (1, 3); -- Hotel California

-- Playlist 2: Favoritas (João)
INSERT INTO playlist_musica (playlist_id, musica_id) VALUES 
  (2, 1), -- Bohemian Rhapsody
  (2, 4), -- Sweet Child O Mine
  (2, 6); -- Imagine

-- Playlist 3: Músicas Antigas (Maria)
INSERT INTO playlist_musica (playlist_id, musica_id) VALUES 
  (3, 2), -- Stairway to Heaven
  (3, 6), -- Imagine
  (3, 7); -- Hey Jude

-- Playlist 4: Heavy Metal (Pedro)
INSERT INTO playlist_musica (playlist_id, musica_id) VALUES 
  (4, 4), -- Sweet Child O Mine
  (4, 5), -- Smells Like Teen Spirit
  (4, 8); -- One
