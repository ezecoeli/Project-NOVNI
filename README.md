# NOVNI: Aventura de un Alien en la Tierra

## Descripción del Proyecto
Un juego de aventura 2D en el que un alienígena debe sobrevivir y reparar su nave tras un aterrizaje forzoso en la Tierra. Durante su viaje, el jugador recolecta partes de la nave y combate enemigos, todo mientras explora diversos niveles con diferentes desafíos.

## Herramientas y Tecnologías utilizadas:

- ** Python: Lenguaje para el desarrollo del juego.
- ** Pygame: Biblioteca para la creación de videojuegos 2D, utilizada para gráficos, sonido, animaciones y control de eventos.
- ** csv: Gestión de datos del mundo del juego, como la creación de niveles y la persistencia del progreso.
- ** pygame.mixer: Implementación de música y efectos de sonido.
- ** pygame.sprite: Sistema de manejo de objetos interactivos, como el jugador, los enemigos y los elementos del entorno.

## Características del Juego
### Jugabilidad
El jugador controla a NOVNI, quien tiene habilidades especiales como el salto, disparo, y el uso de bombas.
A lo largo de los niveles, el jugador debe recolectar partes de la nave que le permitirán repararla y escapar de la Tierra.
Se debe luchar contra enemigos, evitando obstáculos y recogiendo recursos como salud, munición y bombas.

### Mecánicas de Juego
- Movimiento de izquierda a derecha.
- Salto.
- Disparos.
- Lanzar bombas.
- Recursos: Se pueden recoger cajas de salud, munición y bombas para ayudar a NOVNI en su misión.

### Niveles
El juego cuenta con varios niveles, donde NOVNI pasará por diferentes localizaciones, cada una con nuevos desafíos, enemigos y obstáculos. El objetivo es llegar a la localización del cuartel X5G y recoger las partes necesarias de la nave para repararla.

## Música y Sonido
El juego contiene diferentes tipos de música (menú y juego).
Se crearon sonidos para animaciones y acciones.

## Gráficos
El juego utiliza imágenes y sprites 2D para representar a los personajes, enemigos, elementos interactivos y fondos. Los niveles están diseñados a mano con detalles que dan la sensación de explorar diferentes entornos.

## Estructura del Código
El código está dividido en varias clases, cada una responsable de diferentes aspectos del juego:

Clases de objetos (Decoración, Agua, Salida, etc.): Estas clases controlan elementos del entorno, como decoraciones estáticas, agua y puntos de salida para los niveles.
Clases de interacción (ItemBox, HealthBar, etc.): Estas clases permiten al jugador interactuar con el mundo del juego, como recoger objetos y visualizar la barra de salud.
Mecánicas de explosiones y transiciones: Se implementan animaciones para explosiones y efectos de transición entre pantallas (como fade in/out).
Mecánicas de la interfaz y eventos de juego: La lógica de control del flujo del juego, como las entradas del teclado, los menús, las pantallas de "Game Over" y las transiciones entre niveles, está gestionada dentro del bucle principal del juego.

## Historia
NOVNI, un alienígena explorador, se encuentra en la Tierra después de sufrir un accidente con su nave espacial. Durante su travesía, deberá recolectar piezas de su nave, con la esperanza de reparar la cápsula de escape y regresar a su hogar. Sin embargo, el rastreador de la nave ha dejado una última señal que apunta al cuartel X5G, donde NOVNI debe encontrar las piezas faltantes y resolver el misterio que lo ha traído hasta aquí.

A lo largo del viaje, NOVNI contará con la ayuda de algunos humanos que le ofrecerán asistencia en su misión, pero también tendrá que enfrentarse a varios peligros y enemigos. ¿Podrá NOVNI escapar de la Tierra y volver a su hogar?

## Futuras implementaciones
- El jugador interactúa con personajes humanos que le ayudarán en su misión.
- Se añadirán mas niveles.
- Se implementarán objetos que el jugador debe recoger para reparar su nave.

# Contribuciones
¡Contribuciones son bienvenidas! Si deseas mejorar este proyecto, puedes hacer un fork del repositorio y enviar un pull request con tus cambios. Asegúrate de seguir las buenas prácticas de codificación y agregar comentarios en el código para mayor claridad.
