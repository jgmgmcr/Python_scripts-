# juego PONG

#############################   PASOS  ###################################
### 1. Crear la pantalla de juego
## 1.1 Configuración modelidades de juego
## 1.1.1 Número jugadores
## 1.1.2 Dificultad jugador-ia - En caso de 1 jugador
## 1.1.3 Velocidad de la pelota
## 1.1.4 Número de pelotas  jugar
### 2. Crear y mover las raquetas
### 3. Crear la pelota y moverla
### 4. Opciones y pantalla inicial
### 5. Crearla dinamica de juego
## 5.1 Detectar colisiones con las raquetas
## 5.2 Detectar colisiones con los bordes
## 5.3 Detectar cuando la pelota marca punto
## 5.4 Reiniciar-Continuar el juego
## 5.5 Mostrar el marcador
### 6. Finalizar el juego
## 6.1 Mostrar el ganador
## 6.2 Volver a la pantalla inicial
##########################################################################

import pygame
import random

### 1. Crear la pantalla de juego
# Configuración de la pantalla
ANCHO = 800  # Ancho de la ventana
ALTO = 600   # Alto de la ventana
BLANCO = (255, 255, 255)
FONDO = (1, 87, 155)  # NEGRO = (0, 0, 0) 
COLOR_BARRA = (200, 200, 200)

## 1.1 Configuración modelidades de juego
## 1.1.1 Número jugadores
num_jugadores = 1
jugadores = {
    '1': 1, 
    '2': 2}
## 1.1.2 Dificultad jugador-ia - En caso de 1 jugador
dificultad = 'media'
dificultades = {
    'facil': 0.4,   # Mayor probabilidad de error
    'media': 0.2,   # Menos probabilidad de error
    'dificil': 0.05 # Casi ningún error
}

## 1.1.3 Velocidad de la pelota y de las raquetas
velocidad = 'media'
# Velocidades variables
velocidades = {
    'lenta': 3,
    'media': 5,
    'rapida': 7
}
## 1.1.4 Número de pelotas  jugar
num_pelotas = 3

### 2. Crear y mover las raquetas
# Raqueta
class Raqueta(pygame.sprite.Sprite):  # La clase Raqueta hereda de pygame.sprite.Sprite, lo que la hace compatible con los grupos de sprites de Pygame. Esto permite gestionar múltiples objetos en el juego de manera eficiente.
    def __init__(self, x, y, velocidad): # Posición y velocidad inicial de la raqueta
        super().__init__()
        self.image = pygame.Surface((10, 100)) # Superficie rectangular que representa la raqueta, con tamaño (10, 100) (ancho x alto).
        self.image.fill(COLOR_BARRA) # Colorea la raqueta con el color definido por COLOR_BARRA
        self.rect = self.image.get_rect() # Rectángulo que define la posición y el área de colisión de la raqueta.
        self.rect.x = x # Coordenadas iniciales de la raqueta
        self.rect.y = y # Coordenadas iniciales de la raqueta
        self.velocidad = velocidad

    def mover(self, arriba=True):    # Movimiento de raqueta en eje y con limitaciones de alto y bajo
        if arriba and self.rect.top > 0:
            self.rect.y -= self.velocidad
        elif not arriba and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad
    
    def mover_ia(self, pelota, dificultad):
        # Simular error de movimiento
        if random.random() < dificultades.get(dificultad, 0.2):
            # Movimiento aleatorio o no moverse
            if random.random() < 0.5:  # La raqueta IA no se mueve con < 0,5 de probabilidad
                return
            self.mover(arriba=random.choice([True, False]))  # La raqueta IA se mueve hacia arriba o hacia abajo con la misma probabilidad

        # Lógica de seguimiento de la pelota con cierta imprecisión
        margen = dificultades.get(dificultad, 0.2) * 100  # Margen de error por dificultad (en pixeles)
        error = random.randint(-margen, margen)  # Error aleatorio
        self.rect.y = pelota.rect.y - self.rect.height / 2 - error  # Movimiento de la raqueta IA basado en la pelota

# Clase para la pelota con velocidades variables
# Su funcionalidad incluye la inicialización de la posición, la asignación de velocidades variables, el movimiento, y la detección de colisiones con los bordes superior e inferior de la pantalla.
class Pelota(pygame.sprite.Sprite):
    def __init__(self, velocidad='media'):
        super().__init__()
        self.image = pygame.Surface((15, 15)) # Superficie gráfica de la pelota
        self.image.fill(BLANCO) # Color blanco, de la pelota
        self.rect = self.image.get_rect() # Rectángulo que define la posición y el área de colisión de la pelota
        self.rect.center = (ANCHO // 2, ALTO // 2) # Posición inicial de la pelota donde ANCHO y ALTO son las dimensiones de la ventana.
        # En Python, se usa el operador barra doble // para realizar una división. Este operador // divide al primer número por el segundo número y redondea hacia abajo el resultado al entero más cercano
        
        velocidad_base = velocidades.get(velocidad, 5) # Si no se especifica un nivel de velocidad, por defecto se utiliza 'media' (5 píxeles por frame)
        
        # Se asignan velocidades iniciales en las direcciones x e y
        # random.choice((1, -1)) asegura que la pelota puede moverse inicialmente hacia la izquierda o derecha, y hacia arriba o abajo.
        self.velocidad_x = velocidad_base * random.choice((1, -1))
        self.velocidad_y = velocidad_base * random.choice((1, -1))

    # Actualiza la posición de la pelota sumando las velocidades a sus coordenadas
    # Ejemplo explicativo: Si self.velocidad_x = 5, significa que la pelota se moverá 5 píxeles a la derecha en cada frame.
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebotar en bordes superior e inferior
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:  # Si la pelota alcanza el borde superior (self.rect.top <= 0) o inferior (self.rect.bottom >= ALTO)
            self.velocidad_y *= -1 # Invierte la dirección vertical multiplicando self.velocidad_y por -1. Esto cambia la dirección de la pelota en el eje y simulando un rebote.

# Clase principal del juego
class Pong:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Pong")
        self.fuente = pygame.font.Font(None, 34)
        
        # Configuraciones iniciales
        self.modo_2_jugadores = num_jugadores  # Por defecto, inicia en modo 1 jugador
        self.dificultad_ia = dificultad  # Por defecto, inicia en dificultad media
        self.velocidad_juego = velocidad  # Por defecto, inicia en velocidad media
        self.num_pelotas = num_pelotas  # Por defecto, inicia con 3 pelotas
        
        # Reinicia el juego al comenzar la partida
        self.reiniciar_juego_nueva_pelota() # Reinicia el juego completo, volviendo a la pantalla de inicio.


    # Reinicia el juego completo, volviendo a la pantalla de inicio.    
    def reiniciar_juego_completo(self):
        self.puntuacion_izq = 0  # Puntuación del jugador izquierdo
        self.puntuacion_der = 0  # Puntuación del jugador derecho    
        self.pelotas_jugadas = 0  # Contador de pelotas jugadas
        self.pantalla_inicio()  # Muestra la pantalla de inicio

    # Pantalla de inicio con opciones de configuración paso a paso
    def pantalla_inicio(self):
        # Presentación pantalla de inicio
        def mostrar_texto(texto, y):
            """Mostrar texto centrado en la pantalla"""
            # Renderiza el título del juego
            titulo_render = self.fuente.render("Pong", True, BLANCO)
            titulo_rect = titulo_render.get_rect(center=(ANCHO // 2, ALTO // 2 - 180))
            self.pantalla.blit(titulo_render, titulo_rect)
            # Renderiza el texto proporcionado
            texto_render = self.fuente.render(texto, True, BLANCO)
            texto_rect = texto_render.get_rect(center=(ANCHO // 2, ALTO // 2 + y))
            self.pantalla.blit(texto_render, texto_rect)

        
        # Opciones de configuración
        seleccionando = True
        modo_seleccionado = None

        # Muestra el título y las opciones de configuración
        while seleccionando:
            self.pantalla.fill(FONDO)

            # Paso 1: Elegir modo de juego
            if not modo_seleccionado:
                mostrar_texto("1. Modo de Juego:", -100)
                mostrar_texto("1 (Jugador vs IA)", -50)
                mostrar_texto("2 (Jugador vs Jugador)", 0)
                mostrar_texto("Pulsa la tecla correspondiente", 50)
            # Paso 2: Elegir dificultad IA (solo si es 1 jugador)
            elif modo_seleccionado == "1 jugador" and not hasattr(self, 'dificultad_confirmada'):
                mostrar_texto("2. Dificultad IA:", -100)
                mostrar_texto("F (Fácil)", -50)
                mostrar_texto("M (Medio)", 0)
                mostrar_texto("D (Difícil)", 50)
                mostrar_texto("Pulsa la tecla correspondiente", 100)
            # Paso 3: Elegir velocidad del juego
            elif not hasattr(self, 'velocidad_confirmada'):
                mostrar_texto("3. Velocidad del Juego:", -100)
                mostrar_texto("L (Lenta)", -50)
                mostrar_texto("V (Media)", 0)
                mostrar_texto("R (Rápida)", 50)
                mostrar_texto("Pulsa la tecla correspondiente", 100)
            # Paso 4: Elegir número de pelotas
            elif not hasattr(self, 'num_pelotas_confirmada'):
                mostrar_texto("4. Número de Pelotas:", -100)
                mostrar_texto("1 (Una)", -50)
                mostrar_texto("3 (Tres)", 0)
                mostrar_texto("5 (Cinco)", 50)
                mostrar_texto("Pulsa la tecla correspondiente", 100)
            # Paso 5: Confirmar inicio
            else:
                mostrar_texto("Configuración Completa", -50)
                mostrar_texto("Pulsa ESPACE para iniciar", 0)
                pygame.display.flip()   # Actualiza la pantalla

            pygame.display.flip()   # Actualiza la pantalla

            
            # Gestión de eventos en la configuración
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                elif evento.type == pygame.KEYDOWN:
                    if not modo_seleccionado:
                        if evento.key == pygame.K_1:
                            modo_seleccionado = "1 jugador"
                            self.modo_2_jugadores = False
                        elif evento.key == pygame.K_2:
                            modo_seleccionado = "2 jugadores"
                            self.modo_2_jugadores = True
                            setattr(self, 'dificultad_confirmada', True)  # No necesita dificultad IA
                    elif modo_seleccionado == "1 jugador" and not hasattr(self, 'dificultad_confirmada'):
                        if evento.key == pygame.K_f:
                            dificultad_ia = 'facil'
                            setattr(self, 'dificultad_confirmada', True)
                        elif evento.key == pygame.K_m:
                            dificultad_ia = 'medio'
                            setattr(self, 'dificultad_confirmada', True)
                        elif evento.key == pygame.K_d:
                            dificultad_ia = 'dificil'
                            setattr(self, 'dificultad_confirmada', True)
                    elif not hasattr(self, 'velocidad_confirmada'):
                        if evento.key == pygame.K_l:
                            velocidad_juego = 'lenta'
                            setattr(self, 'velocidad_confirmada', True)
                        elif evento.key == pygame.K_v:
                            velocidad_juego = 'media'
                            setattr(self, 'velocidad_confirmada', True)
                        elif evento.key == pygame.K_r:
                            velocidad_juego = 'rapida'
                            setattr(self, 'velocidad_confirmada', True)
                    elif not hasattr(self, 'num_pelotas_confirmada'):
                        if evento.key == pygame.K_1:
                            num_pelotas = 1
                            setattr(self, 'num_pelotas_confirmada', True)
                        elif evento.key == pygame.K_3:
                            num_pelotas = 3
                            setattr(self, 'num_pelotas_confirmada', True)
                        elif evento.key == pygame.K_5:
                            num_pelotas = 5
                            setattr(self, 'num_pelotas_confirmada', True)
                    elif hasattr(self, 'num_pelotas_confirmada'):
                        if evento.key == pygame.K_SPACE:
                            self.dificultad_ia = dificultad_ia
                            self.velocidad_juego = velocidad_juego
                            return True 
    
        return False

    def reiniciar_juego_nueva_pelota(self):
        # Crear una nueva pelota con la velocidad configurada
        self.pelota = Pelota(self.velocidad_juego)

        # velocidad juego
        velocidad_raqueta = velocidades.get(self.velocidad_juego, 5) # Velocidad de las raquetas, por defecto 'media' (5 píxeles por frame)

        self.raqueta_izq = Raqueta(50, ALTO // 2 - 50, velocidad_raqueta)
        self.raqueta_der = Raqueta(ANCHO - 60, ALTO // 2 - 50, velocidad_raqueta)

        # La puntuación y el modo de juego se mantienen constantes
        if not hasattr(self, 'puntuacion_izq'):
            self.puntuacion_izq = 0
        if not hasattr(self, 'puntuacion_der'):
            self.puntuacion_der = 0

        # El contador de pelotas jugadas se incrementa
        if not hasattr(self, 'pelotas_jugadas'):
            self.pelotas_jugadas = 0
        self.pelotas_jugadas += 1

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
        
        # Control de raquetas
        teclas = pygame.key.get_pressed()
        
        # Raqueta izquierda
        if teclas[pygame.K_w]:
            self.raqueta_izq.mover(arriba=True)
        if teclas[pygame.K_s]:
            self.raqueta_izq.mover(arriba=False)
        
        # Raqueta derecha
        if self.modo_2_jugadores:
            # Control de segundo jugador
            if teclas[pygame.K_UP]:
                self.raqueta_der.mover(arriba=True)
            if teclas[pygame.K_DOWN]:
                self.raqueta_der.mover(arriba=False)
        else:
            # IA para raqueta derecha con dificultad
            self.raqueta_der.mover_ia(self.pelota, self.dificultad_ia)
        
        return True

    def dibujar(self):
        # Limpiar pantalla
        self.pantalla.fill(FONDO)
        
        # Línea central
        pygame.draw.line(self.pantalla, BLANCO, 
                         (ANCHO//2, 0), (ANCHO//2, ALTO), 2)
        
        # Dibujar elementos
        self.pantalla.blit(self.raqueta_izq.image, self.raqueta_izq.rect)
        self.pantalla.blit(self.raqueta_der.image, self.raqueta_der.rect)
        self.pantalla.blit(self.pelota.image, self.pelota.rect)
        
        # Marcador de puntuación
        texto_puntuacion = self.fuente.render(
            f"{self.puntuacion_izq} : {self.puntuacion_der}", 
            True, BLANCO
        )
        texto_rect = texto_puntuacion.get_rect(center=(ANCHO//2, 30))
        self.pantalla.blit(texto_puntuacion, texto_rect)
        
        # Información de configuración
        texto_config = self.fuente.render(
            f"IA: {self.dificultad_ia.capitalize()} | Vel: {self.velocidad_juego.capitalize()}", 
            True, BLANCO
        )
        texto_config_rect = texto_config.get_rect(center=(ANCHO//2, ALTO-60))
        self.pantalla.blit(texto_config, texto_config_rect)
        
        # Contador de pelotas
        texto_pelotas = self.fuente.render(
            f"Pelotas: {self.pelotas_jugadas}/{num_pelotas}", 
            True, BLANCO
        )
        texto_pelotas_rect = texto_pelotas.get_rect(center=(ANCHO//2, ALTO-30))
        self.pantalla.blit(texto_pelotas, texto_pelotas_rect)
        
        # Actualizar pantalla
        pygame.display.flip()               

    def actualizar(self):
        # Mover pelota
        self.pelota.update()

        # Colisión con raquetas
        if pygame.sprite.collide_rect(self.pelota, self.raqueta_izq) or \
           pygame.sprite.collide_rect(self.pelota, self.raqueta_der):
            self.pelota.velocidad_x *= -1

        # Verificar si se ha anotado un punto
        lado = self.punto_anotado()
        if lado:
            self.pelotas_jugadas += 1
            if self.puntuacion_izq >= num_pelotas or self.puntuacion_der >= num_pelotas:
                self.mostrar_ganador()
                self.reiniciar_juego_completo()
            else:
                self.reiniciar_juego_nueva_pelota()

    def ejecutar_juego(self):
        """Bucle principal del juego."""
        reloj = pygame.time.Clock()
        jugando = True

        while jugando:
            # Manejar eventos
            if not self.manejar_eventos():
                jugando = False

            # Actualizar posiciones
            self.actualizar()

            # Dibujar en pantalla
            self.dibujar()

            # Limitar FPS
            reloj.tick(60)

        # Volver a la pantalla de inicio al finalizar
        if not self.pantalla_inicio():
            pygame.quit()

    def punto_anotado(self):
        """
        Verifica si se ha anotado un punto y reinicia el juego si es necesario.
        """
        if self.pelota.rect.left <= 0:
            self.puntuacion_der += 1
            return "der"
        elif self.pelota.rect.right >= ANCHO:
            self.puntuacion_izq += 1
            return "izq"
        return None

    def mostrar_ganador(self):
        # Pantalla de ganador
        self.pantalla.fill(FONDO)
        
        # Determinar ganador 
        if self.puntuacion_izq >= num_pelotas:
            texto_ganador = self.fuente.render("¡Jugador Izquierdo Gana!", True, BLANCO)
        else:
            texto_ganador = self.fuente.render("¡Jugador Derecho Gana!", True, BLANCO)
        
        # Mostrar puntuación final
        texto_puntuacion = self.fuente.render(
            f"Puntuación Final: {self.puntuacion_izq} - {self.puntuacion_der}", 
            True, BLANCO
        )
        
        # Instrucciones para reiniciar
        texto_reiniciar = self.fuente.render(
            "Presiona ESPACIO para jugar de nuevo", 
            True, BLANCO
        )
        
        # Posicionar textos
        ganador_rect = texto_ganador.get_rect(center=(ANCHO//2, ALTO//3))
        puntuacion_rect = texto_puntuacion.get_rect(center=(ANCHO//2, ALTO//2))
        reiniciar_rect = texto_reiniciar.get_rect(center=(ANCHO//2, 2*ALTO//3))
        
        # Dibujar textos
        self.pantalla.blit(texto_ganador, ganador_rect)
        self.pantalla.blit(texto_puntuacion, puntuacion_rect)
        self.pantalla.blit(texto_reiniciar, reiniciar_rect)
        
        pygame.display.flip()
        
        # Esperar acción del usuario
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        # Reiniciar todo el juego
                        self.puntuacion_izq = 0
                        self.puntuacion_der = 0
                        self.pelotas_jugadas = 0
                        return True
        return False
    
        pygame.time.wait(3000)  # Esperar 2 segundos antes de reiniciar el juego completo
        self.reiniciar_juego_completo()

# Ejecutar el juego
if __name__ == "__main__":
    juego = Pong()
    if juego.pantalla_inicio():
        juego.ejecutar_juego()
    pygame.quit()


#####   falla la seleccion en la configuración del juego
