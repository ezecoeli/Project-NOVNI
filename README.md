# **NOVNI**: Aventura de un Alien en la Tierra

## Descripción del juego

Un juego en 2D de plataformas y dezplazamiento lateral en el que un alienígena debe sobrevivir y reparar su nave tras un aterrizaje forzoso en la Tierra. Durante su viaje, el jugador recolecta partes de la nave y combate enemigos mientras explora diversos niveles con diferentes desafíos.

El juego cuenta con:

* **Múltiples niveles:** Con diferentes fondos y desafíos.
* **Variedad de enemigos:** Con comportamientos únicos, como disparar y lanzar granadas.
* **Jefe final:** Con una barra de salud y ataques especiales.
* **Objetos:** Cajas de salud, munición y bombas que el jugador puede recoger.
* **Efectos de sonido y música:** Para ambientar la experiencia de juego.
* **Pantallas de transición y victoria:** Para una mejor experiencia narrativa.

## Tecnologías utilizadas

* **Pygame:** Librería de Python para el desarrollo de videojuegos.
* **Python:** Lenguaje de programación principal.

## Librerías y módulos

* `pygame`: Para la creación de la ventana del juego, manejo de eventos, gráficos, sonido, etc.
* `random`: Para generar números aleatorios (movimiento de enemigos, generación de objetos).
* `csv`: Para leer los datos de los niveles desde archivos CSV.
* `math`: Para funciones matemáticas (cálculo de seno para el movimiento de algunos elementos).
* `os`: Para interactuar con el sistema operativo (cargar imágenes y sonidos).
* `sys`: Para acceder a variables del sistema (detectar si el juego se ejecuta desde un ejecutable).


## Características y jugabilidad

El jugador controla a **NOVNI**, quien tiene habilidades especiales como el salto, disparo, y el uso de bombas.
A lo largo de los niveles, el jugador debe recolectar partes de la nave que le permitirán repararla y escapar de la Tierra.
Se debe luchar contra enemigos, evitando obstáculos y recogiendo recursos como salud, munición y bombas.

### Mecánicas de Juego

- Movimiento de izquierda a derecha.
- Salto.
- Disparos.
- Lanzar bombas.
- Recursos: Se pueden recoger cajas de salud, munición y bombas para ayudar a NOVNI en su misión.

**Controles:**

* **Flechas izquierda/derecha:** Mover al personaje.
* **Barra espaciadora:** Saltar.
* **A:** Disparar.
* **S:** Lanzar bomba.
* **Esc:** Salir del juego.

### Niveles

El juego cuenta con varios niveles, donde NOVNI pasará por diferentes localizaciones, cada una con nuevos desafíos, enemigos y obstáculos. El objetivo es llegar a la localización del cuartel X5G y recoger las partes necesarias de la nave para repararla.

### Música y Sonido

El juego contiene diferentes tipos de música para las diferentes isntancias del juego.
Se crearon sonidos para animaciones y acciones.

### Gráficos

El juego utiliza imágenes y sprites 2D para representar a los personajes, enemigos, elementos interactivos y fondos. Los niveles están diseñados a mano con detalles que dan la sensación de explorar diferentes entornos.

### Historia

NOVNI, un alienígena explorador, sufre un accidente con su nave espacial y se ve obligado a realizar un aterrizaje forzoso en la Tierra. Durante su travesía, deberá recolectar piezas de su nave con la esperanza de repararla y regresar a su hogar. Sin embargo, el rastreador de la nave ha dejado una última señal que apunta al cuartel X5G, donde NOVNI debe encontrar las piezas faltantes y resolver el misterio que lo ha traído hasta aquí. 
Para lograr su objetivo deberá enfrentar al Dr. Metroid y su ejército.
¿Podrá NOVNI llegar a su nave para repararla y volver a su hogar?

### Futuras implementaciones
* **Añadir efectos visuales:**  Como partículas y explosiones más elaboradas.
* **Optimizar el rendimiento:**  Para un juego más fluido.
* **Mejoras:** Corrección de errores.

## Cómo jugar

1. Clonar el repositorio.
2. Instalar las dependencias (`pygame`).
3. Ejecutar el archivo `main.py`.

## Contribuciones
¡Contribuciones son bienvenidas! Si deseas mejorar este proyecto, puedes hacer un fork del repositorio y enviar un pull request con tus cambios. Asegúrate de seguir las buenas prácticas de codificación y agregar comentarios en el código para mayor claridad.

# Licencia
Copyright (c) [2025] [Ezequiel Camilo Coeli]. Todos los derechos reservados.

Ninguna parte de este software puede ser reproducida, distribuida o utilizada sin el permiso explícito del autor.
