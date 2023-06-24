
# Juego de la vida

**Notas en Español**: hice un fork del repositorio de [emadehsan](github.com/emadehsan/life) y las únicas diferencias son:

1. Todos los textos traducidos al Español
2. He partido la Animación en varias escenas para facilitar crear varios videos
3. Fondo Blanco para verlo mejor en presentaciones con proyectores
4. Script de bash para generar los videos: `bash render_scenes.sh`

Los videos generados pueden ser utilizados en Power Point, Keynote o el sistema externo que sea.
El resto de instrucciones son como las del repositorio original.


Readme original:
-----

# Game of Life


[![YouTube video thumbnail](https://img.youtube.com/vi/qcbwzWlltNc/0.jpg)](https://www.youtube.com/watch?v=qcbwzWlltNc)

This code simulates Conway's Game of Life into a video 
using [manim](https://github.com/3b1b/manim/).

## Setup
* Clone this repository
* Install [manim](https://github.com/3b1b/manim/)
* Run `manimgl app.py AppLife`

## Create a video
Run 
```bash
manimgl app.py AppLife -o
```

## Further reading
* [Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life)
* [manim - Mathematical Animations Library by 3b1b](https://github.com/3b1b/manim/)
