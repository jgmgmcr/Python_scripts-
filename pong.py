# juego PONG

#############################   PASOS  ###################################
# 1. Crear clases para las distintas partes del juego
## 1.1 Variables comunes de Pantalla de juego
## 1.2 Menu inicio (Jugadores - dificultad - velocidad - pelotas)
## 1.3 Crear y mover las raquetas
## 1.4 Crear la pelota y moverla
## 1.5 Dibujar pista de juego y marcadores
## 1.6 Crear la dinámica de juego
### 1.6.1 Detectar colisiones con las raquetas
### 1.6.2 Detectar colisiones con los bordes
### 1.6.3 Detectar cuando la pelota marca punto (toca los bordes izquierdo o derecho)
### 1.6.4 Reiniciar-Continuar el juego tras punto anotado
### 1.6.5 Fin de partida y Mostrar el marcador
### 1.6.6. Volver a menú de inicio
# 2. Ejecutar juego
##########################################################################

import pygame
import random
#import pygame.mixer

### 1. Crear la pantalla de juego
## 1.1 Variables comunes de Pantalla de juego
# Configuración de la pantalla
ANCHO = 800  # Ancho de la ventana
ALTO = 600   # Alto de la ventana
BLANCO = (255, 255, 255)
FONDO = (1, 87, 155)  
COLOR_BARRA = (200, 200, 200)

## Modalidades de juego
# Número jugadores
jugadores = {
    '1': 1, 
    '2': 2
}
# Dificultad jugador-ia - En caso de 1 jugador
dificultades = {
    'facil': 0.99,   # Mayor probabilidad de error
    'media': 0.4,   # Menos probabilidad de error
    'dificil': 0.1 # Casi ningún error
}
# Velocidad de la pelota y de las raquetas
velocidades = {
    'lenta': 3,
    'media': 5,
    'rapida': 7
}
# Número de pelotas a jugar
num_pelotas = {
    '1': 1,
    '3': 3,
    '5': 5
}

## 1.2 Menu inicio (Jugadores - dificultad - velocidad - pelotas)
class MenuInicio:
    """Clase para el menú de inicio"""

    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.fuente = pygame.font.Font(None, 34)
        self.opciones_seleccionadas = {
            'Jugadores': None,
            'Dificultad': None,
            'Velocidad': None,
            'Pelotas': None
        }
        self.modo_2_jugadores = False

    def mostrar_texto(self, texto, y):
        """Mostrar texto centrado en la pantalla"""
        # Renderiza el título del juego
        titulo_render = self.fuente.render("Pong", True, BLANCO)
        titulo_rect = titulo_render.get_rect(center=(ANCHO // 2, ALTO // 2 - 180))
        self.pantalla.blit(titulo_render, titulo_rect)
        # Renderiza el texto proporcionado
        texto_render = self.fuente.render(texto, True, BLANCO)
        texto_rect = texto_render.get_rect(center=(ANCHO // 2, ALTO // 2 + y))
        self.pantalla.blit(texto_render, texto_rect)

    def ejecutar_menu_inicio(self):
        """Ejecuta el menú de inicio y devuelve las opciones seleccionadas"""
        seleccionando = True
        modo_seleccionado = None

        # Muestra el título y las opciones de configuración
        while seleccionando:
            self.pantalla.fill(FONDO)

            # Paso 1: Elegir modo de juego
            if not modo_seleccionado:
                self.mostrar_texto("- Modo de Juego:", -100)
                self.mostrar_texto("1 (Jugador vs IA)", -50)
                self.mostrar_texto("2 (Jugador vs Jugador)", 0)
                self.mostrar_texto("Pulsa la tecla correspondiente", 50)
            # Paso 2: Elegir dificultad IA (solo si es 1 jugador)
            elif modo_seleccionado == "1 jugador" and not hasattr(self, 'dificultad_confirmada'):
                self.mostrar_texto("- Dificultad IA:", -100)
                self.mostrar_texto("F (Fácil)", -50)
                self.mostrar_texto("M (Medio)", 0)
                self.mostrar_texto("D (Difícil)", 50)
                self.mostrar_texto("Pulsa la tecla correspondiente", 100)
            # Paso 3: Elegir velocidad del juego
            elif not hasattr(self, 'velocidad_confirmada'):
                self.mostrar_texto("- Velocidad del Juego:", -100)
                self.mostrar_texto("L (Lenta)", -50)
                self.mostrar_texto("V (Media)", 0)
                self.mostrar_texto("R (Rápida)", 50)
                self.mostrar_texto("Pulsa la tecla correspondiente", 100)
            # Paso 4: Elegir número de pelotas
            elif not hasattr(self, 'num_pelotas_confirmada'):
                self.mostrar_texto("- Número de Pelotas:", -100)
                self.mostrar_texto("1 (Una)", -50)
                self.mostrar_texto("3 (Tres)", 0)
                self.mostrar_texto("5 (Cinco)", 50)
                self.mostrar_texto("Pulsa la tecla correspondiente", 100)
            # Paso 5: Confirmar inicio
            else:
                self.mostrar_texto("Configuración Completa", -50)
                self.mostrar_texto("Pulsa ESPACE para iniciar", 0)
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
                            self.opciones_seleccionadas['Jugadores'] = 1
                            self.modo_2_jugadores = False
                        elif evento.key == pygame.K_2:
                            modo_seleccionado = "2 jugadores"
                            self.opciones_seleccionadas['Jugadores'] = 2
                            self.modo_2_jugadores = True
                            setattr(self, 'dificultad_confirmada', True)  # No necesita dificultad IA
                    elif modo_seleccionado == "1 jugador" and not hasattr(self, 'dificultad_confirmada'):
                        if evento.key == pygame.K_f:
                            self.opciones_seleccionadas['Dificultad'] = 'facil'
                            setattr(self, 'dificultad_confirmada', True)
                        elif evento.key == pygame.K_m:
                            self.opciones_seleccionadas['Dificultad'] = 'medio'
                            setattr(self, 'dificultad_confirmada', True)
                        elif evento.key == pygame.K_d:
                            self.opciones_seleccionadas['Dificultad'] = 'dificil'
                            setattr(self, 'dificultad_confirmada', True)
                    elif not hasattr(self, 'velocidad_confirmada'):
                        if evento.key == pygame.K_l:
                            self.opciones_seleccionadas['Velocidad'] = 'lenta'
                            setattr(self, 'velocidad_confirmada', True)
                        elif evento.key == pygame.K_v:
                            self.opciones_seleccionadas['Velocidad'] = 'media'
                            setattr(self, 'velocidad_confirmada', True)
                        elif evento.key == pygame.K_r:
                            self.opciones_seleccionadas['Velocidad'] = 'rapida'
                            setattr(self, 'velocidad_confirmada', True)
                    elif not hasattr(self, 'num_pelotas_confirmada'):
                        if evento.key == pygame.K_1:
                            self.opciones_seleccionadas['Pelotas'] = 1
                            setattr(self, 'num_pelotas_confirmada', True)
                        elif evento.key == pygame.K_3:
                            self.opciones_seleccionadas['Pelotas'] = 3
                            setattr(self, 'num_pelotas_confirmada', True)
                        elif evento.key == pygame.K_5:
                            self.opciones_seleccionadas['Pelotas'] = 5
                            setattr(self, 'num_pelotas_confirmada', True)
                    elif hasattr(self, 'num_pelotas_confirmada'):   # Confirmar inicio 
                        if evento.key == pygame.K_SPACE:
                            return True 
    
        return False



## 1.3 Crear y mover las raquetas
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
        #print(f"Dificultad seleccionada: {dificultad}")  # Verificar la dificultad
        # Simular error de movimiento
        if random.random() < dificultades.get(dificultad, 0.2):
            # Movimiento aleatorio o no moverse
            if random.random() < 0.5:  # La raqueta IA no se mueve con < 0,5 de probabilidad
                return
            self.mover(arriba=random.choice([True, False]))  # La raqueta IA se mueve hacia arriba o hacia abajo con la misma probabilidad

        # Lógica de seguimiento de la pelota con cierta imprecisión
        margen = int(dificultades.get(dificultad, 0.2) * 150)  # Margen de error por dificultad (en pixeles)
        error = random.randint(-margen, margen)  # Error aleatorio
        self.rect.y = pelota.rect.y - self.rect.height / 2 - error  # Nueva posición de la raqueta IA



## 1.4 Crear la pelota y moverla
# Clase para la pelota con velocidades variables
# Su funcionalidad incluye la inicialización de la posición, la asignación de velocidades variables, el movimiento, y la detección de colisiones con los bordes superior e inferior de la pantalla.
class Pelota(pygame.sprite.Sprite):
    def __init__(self, Velocidad):
        super().__init__()
        self.image = pygame.Surface((15, 15)) # Superficie gráfica de la pelota
        self.image.fill(BLANCO) # Color blanco, de la pelota
        self.rect = self.image.get_rect() # Rectángulo que define la posición y el área de colisión de la pelota
        self.rect.center = (ANCHO // 2, ALTO // 2) # Posición inicial de la pelota donde ANCHO y ALTO son las dimensiones de la ventana.
        # En Python, se usa el operador barra doble // para realizar una división. Este operador // divide al primer número por el segundo número y redondea hacia abajo el resultado al entero más cercano
        
        velocidad_base = velocidades.get(Velocidad,5) # Si no se especifica un nivel de velocidad, por defecto se utiliza 'media' (5 píxeles por frame)
        
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


## 1.5 Dibujar pista de juego y marcadores
class PistaJuego:
    def __init__(self):
        self.pelotas_jugadas = 0 # Contador de pelotas jugadas
        self.puntuacion_izq = 0 # Puntuación del jugador izquierdo
        self.puntuacion_der = 0 # Puntuación del jugador derecho
        self.fuente = pygame.font.Font(None, 34) # Fuente para el marcador

    # Dibuja la pista de juego y los marcadores en la pantalla
    def dibujar_marcador(self, pantalla):
        marcador_izq = self.fuente.render(str(self.puntuacion_izq), True, BLANCO) # Renderiza el marcador izquierdo
        marcador_der = self.fuente.render(str(self.puntuacion_der), True, BLANCO) # Renderiza el marcador derecho
        pantalla.blit(marcador_izq, (ANCHO // 2 - 100, 10)) # Posiciona el marcador izquierdo en la pantalla
        pantalla.blit(marcador_der, (ANCHO // 2 + 100, 10)) # Posiciona el marcador derecho en la pantalla
        # Dibujar una línea blanca vertical en el centro de la pantalla
        pygame.draw.line(pantalla, BLANCO, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)




## 1.6 Crear la dinámica de juego
### 1.6.1 Detectar colisiones con las raquetas
class DinamicaJuego:
    def __init__(self, pantalla, opciones_seleccionadas):
        self.pantalla = pantalla
        self.opciones_seleccionadas = opciones_seleccionadas
        self.raqueta_1 = Raqueta(50, ALTO // 2 - 50, velocidades[opciones_seleccionadas['Velocidad']])
        self.raqueta_2 = Raqueta(ANCHO - 60, ALTO // 2 - 50, velocidades[opciones_seleccionadas['Velocidad']])
        self.pelota = Pelota(velocidades[opciones_seleccionadas['Velocidad']])
        self.pista = PistaJuego()

    ### 1.6.1 Detectar colisiones con las raquetas
    def colision_raqueta(self):
        if self.pelota.rect.colliderect(self.raqueta_1.rect):
            self.pelota.velocidad_x *= -1  # Invertir dirección horizontal
            self.pelota.rect.left = self.raqueta_1.rect.right  # Ajustar posición para evitar traspaso
            self.pelota.velocidad_y *= random.choice([1, -1])  # Variar dirección vertical
            #sonido_golpe.play()  # Reproducir sonido de golpe
        elif self.pelota.rect.colliderect(self.raqueta_2.rect):
            self.pelota.velocidad_x *= -1  # Invertir dirección horizontal
            self.pelota.rect.right = self.raqueta_2.rect.left  # Ajustar posición para evitar traspaso
            self.pelota.velocidad_y *= random.choice([1, -1])  # Variar dirección vertical
            #sonido_golpe.play()  # Reproducir sonido de golpe

    ### 1.6.3 Detectar cuando la pelota marca punto (toca los bordes izquierdo o derecho)
    def punto_anotado(self):
        if self.pelota.rect.left <= 0:
            self.pista.puntuacion_der += 1 # Anotar punto
            #sonido_gol.play() # Reproducir sonido de gol
            return 'derecha' # Devolver el lado que anotó el punto
        elif self.pelota.rect.right >= ANCHO:
            self.pista.puntuacion_izq += 1
            #sonido_gol.play() # Reproducir sonido de gol
            return 'izquierda'
        return False

    def reiniciar_juego(self):
        self.pelota.rect.center = (ANCHO // 2, ALTO // 2)
        self.pelota.velocidad_x = velocidades[self.opciones_seleccionadas['Velocidad']] * random.choice([1, -1])
        self.pelota.velocidad_y = velocidades[self.opciones_seleccionadas['Velocidad']] * random.choice([1, -1])
        self.pista.pelotas_jugadas += 1

    def fin_partida(self):
        return self.pista.pelotas_jugadas >= self.opciones_seleccionadas['Pelotas']

    #def volver_menu_inicio(self):
    #    if self.fin_partida():
    #        return True
    #    return False

    def ejecutar(self):
        reloj = pygame.time.Clock()
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

            # Movimiento de las raquetas
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_w]:
                self.raqueta_1.mover(arriba=True)
            if teclas[pygame.K_s]:
                self.raqueta_1.mover(arriba=False)
            if self.opciones_seleccionadas['Jugadores'] == 2:
                if teclas[pygame.K_UP]:
                    self.raqueta_2.mover(arriba=True)
                if teclas[pygame.K_DOWN]:
                    self.raqueta_2.mover(arriba=False)
            else:
                self.raqueta_2.mover_ia(self.pelota, self.opciones_seleccionadas['Dificultad'])

            # Actualizar pelota
            self.pelota.update()  # Aquí se maneja el rebote en los bordes superior e inferior
            self.colision_raqueta()  # Aquí se maneja el rebote con las raquetas

            # Verificar si se anotó un punto
            if self.punto_anotado():
                self.reiniciar_juego()

            # Dibujar elementos
            self.pantalla.fill(FONDO)
            self.pantalla.blit(self.raqueta_1.image, self.raqueta_1.rect)
            self.pantalla.blit(self.raqueta_2.image, self.raqueta_2.rect)
            self.pantalla.blit(self.pelota.image, self.pelota.rect)
            self.pista.dibujar_marcador(self.pantalla)

            pygame.display.flip()
            reloj.tick(60)

            # Verificar fin de partida
            if self.fin_partida():
                self.pantalla.fill(FONDO)
                texto_puntuacion = self.pista.fuente.render(f"Puntuación final:  {self.pista.puntuacion_izq}  |  {self.pista.puntuacion_der}", True, BLANCO)
                rect_puntuacion = texto_puntuacion.get_rect(center=(ANCHO // 2, ALTO // 4))
                self.pantalla.blit(texto_puntuacion, rect_puntuacion)

                texto_ganador = self.pista.fuente.render("Jugador 1 Gana", True, BLANCO) if self.pista.puntuacion_izq > self.pista.puntuacion_der else self.pista.fuente.render("Jugador 2 Gana", True, BLANCO)
                rect_ganador = texto_ganador.get_rect(center=(ANCHO // 2, ALTO // 3))
                self.pantalla.blit(texto_ganador, rect_ganador)

                texto_fin = self.pista.fuente.render("Fin de la partida", True, BLANCO)
                rect_fin = texto_fin.get_rect(center=(ANCHO // 2, ALTO // 2))
                self.pantalla.blit(texto_fin, rect_fin)

                texto_nueva_partida = self.pista.fuente.render("Pulsa ESPACE para jugar de nuevo", True, BLANCO)
                rect_nueva_partida = texto_nueva_partida.get_rect(center=(ANCHO // 2, ALTO // 1.5))
                self.pantalla.blit(texto_nueva_partida, rect_nueva_partida)

                pygame.display.flip()

                # Esperar a que el jugador pulse ESPACE o cierre la ventana
                esperando = True
                while esperando:
                    for evento in pygame.event.get():
                        if evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_SPACE:
                                esperando = False
                                ejecutando = True  
                                # Salir del bucle de la partida
                                # Reiniciar el juego
                                menu = MenuInicio()
                                if menu.ejecutar_menu_inicio():
                                    self.__init__(self.pantalla, menu.opciones_seleccionadas)  # Reiniciar la dinámica del juego
                                else:
                                    ejecutando = False
                                    pygame.quit()
                                    return
                        elif evento.type == pygame.QUIT:
                            esperando = False
                            ejecutando = False
                            pygame.quit()
                            return

                
                
# 2. Inicializar Pygame
pygame.init()
pygame.display.set_caption("Pong!!")
## Inicializar el mixer de sonido
#pygame.mixer.init()
## Cargar los sonidos
#sonido_golpe = pygame.mixer.Sound("sonido_golpe.wav")
#sonido_gol = pygame.mixer.Sound("sonido_gol.wav")
#sonido_golpe.set_volume(0.5)  # 50% de volumen
#sonido_gol.set_volume(1.0)  # 100% de volumen

# Ejecutar el juego
if __name__ == "__main__":
    menu = MenuInicio()
    if menu.ejecutar_menu_inicio():
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        juego = DinamicaJuego(pantalla, menu.opciones_seleccionadas)
        juego.ejecutar()
