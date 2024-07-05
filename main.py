import pygame
from datos24 import lista
from constantes import *
from funciones import *

"""
Nombre: Giménez María de los Milagros
"""

temas = []
preguntas = []
respuestas_a = []
respuestas_b = []
respuestas_c = []
respuestas_correctas = []

for diccionario in lista:
    temas.append(diccionario["tema"])
    preguntas.append(diccionario["pregunta"])
    respuestas_a.append(diccionario["a"])
    respuestas_b.append(diccionario["b"])
    respuestas_c.append(diccionario["c"])
    respuestas_correctas.append(diccionario["correcta"])

coordenadas = [150,395]
comenzar = False
n_pregunta = 0
tema = ""
pregunta = ""
respuesta_a = ""
respuesta_b = ""
respuesta_c = ""
flag_game_over = False
puntaje = 0
ya_respondio = False
avanza1 = False
retrocede1 = False
flag_mostrar_puntajes = False
flag_musica = True
pygame.init()
#musica
pygame.mixer.init()  # Inicializa el módulo de sonido
sonido_boton = pygame.mixer.Sound("boton.mp3")
sonido_res_correcta = pygame.mixer.Sound("correcta.mp3")
sonido_res_incorrecta = pygame.mixer.Sound("incorrecta.mp3")
musica = pygame.mixer.Sound("Stress.mp3")
musica.set_volume(0.5)
musica.play(-1)
#timer
timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos,1000)
segundos = "5"

pantalla = pygame.display.set_mode((1300, 900))
pygame.display.set_caption("Carrera de Mente")
imagen_nube = pygame.image.load("nube.png")
imagen_nube = pygame.transform.scale(imagen_nube,(800,700))
imagen_casilleros = pygame.image.load("casilleros.png")
imagen_casilleros = pygame.transform.scale(imagen_casilleros,(1000,300))
imagen_personaje = pygame.image.load("personaje.png")
imagen_personaje = pygame.transform.scale(imagen_personaje,(200,200))
imagen_personaje_abajo = pygame.image.load("personaje_abajo.png")
imagen_personaje_abajo = pygame.transform.scale(imagen_personaje_abajo,(200,200))
imagen_logo = pygame.image.load("logo-utn.png")
imagen_logo = pygame.transform.scale(imagen_logo,(300,75))
imagen_volumen = pygame.image.load("volumen.png")
imagen_volumen = pygame.transform.scale(imagen_volumen,(80,80))
imagen_no_volumen = pygame.image.load("novolumen.png")
imagen_no_volumen = pygame.transform.scale(imagen_no_volumen,(120,80))

fuente = pygame.font.SysFont("Arial", 35)
fuente_pregunta_tema = pygame.font.SysFont("Arial", 28)
fuente_game_over = pygame.font.SysFont("Arial", 70)
texto_terminar = fuente.render("Terminar", True, COLOR_BLANCO)
texto_comenzar = fuente.render("Comenzar", True, COLOR_BLANCO)
texto_score = fuente.render(str(f"Score: {puntaje}"), True, COLOR_VIOLETA)

flag_correr = True

while flag_correr:
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_correr = False


        if evento.type == pygame.USEREVENT:
            if comenzar:
                segundos = int(segundos)-1
                if int(segundos) == -1:
                    n_pregunta += 1
                    if n_pregunta >= len(preguntas):
                        flag_game_over = True         
                    else:
                        segundos = "5"
                        ya_respondio = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            if not flag_game_over:
                if 20 < x < 100 and 800 < y < 880:#boton sonido
                    if flag_musica:
                        musica.stop()
                        flag_musica = False
                    else:
                        musica.play(-1)
                        flag_musica = True
                        
                if 205 < x < 400 and 800 < y < 855:#boton comenzar
                    if flag_musica:
                        sonido_boton.play()
                    comenzar = True
                    if n_pregunta >= len(preguntas):
                        flag_game_over = True
                   # else:
                        #ya_respondio = False
                            
                if 900 < x < 1100 and 800 < y < 860:#boton terminar
                    if flag_musica:
                        sonido_boton.play()
                    flag_game_over = True

                if not ya_respondio:
                    if respuestas_correctas[n_pregunta] == "a":
                        if 490 < x < 875 and 150 < y < 185:#opcion a
                            if flag_musica:
                                sonido_res_correcta.play()
                            puntaje += 10
                            if coordenadas[1] == 395:#si esta arriba
                                if coordenadas[0] == 625 and not avanza1:#si esta en el casillero avanza1 por primera vez
                                    coordenadas[0] += 190
                                    avanza1 = True#avanza1 ya no se usa
                                else:#avanza normal
                                    coordenadas = avanzar_personaje_casilleros_ariiba(coordenadas)
                            else:#si esta abajo
                                if coordenadas == [625,520] and not retrocede1:#si esta en el casillero retrocede 1 por primera vez
                                    coordenadas[0] = 720
                                    retrocede1 = True#retrocede1 ya no se usa mas
                                else:#avanza normal
                                    coordenadas = avanzar_personaje_casilleros_abajo(coordenadas)
                            ya_respondio = True
                            segundos = "0"

                        elif 500 < x < 875 and 210 < y < 245 or 500 < x < 875 and 270 < y < 305:#opcion b y c
                            if flag_musica:
                                sonido_res_incorrecta.play()
                            if coordenadas[1] == 395:#si esta arriba
                                coordenadas = retroceder_personaje_ariiba(coordenadas)
                            else:#si esta abajo
                                coordenadas = retroceder_personaje_abajo(coordenadas)
                            ya_respondio = True
                            segundos = "0"
                
                    if respuestas_correctas[n_pregunta] == "b":
                        if 500 < x < 875 and 210 < y < 245:#opcion b
                            if flag_musica:
                                sonido_res_correcta.play()
                            puntaje += 10
                            if coordenadas[1] == 395:
                                if coordenadas[0] == 625 and not avanza1:
                                    coordenadas[0] += 190
                                    avanza1 = True
                                else:
                                    coordenadas = avanzar_personaje_casilleros_ariiba(coordenadas)
                            else:
                                if coordenadas == [625,520] and not retrocede1:
                                    coordenadas[0] = 720
                                    retrocede1 = True
                                else:
                                    coordenadas = avanzar_personaje_casilleros_abajo(coordenadas)
                            ya_respondio = True
                            segundos = "0"
                    
                        elif 500 < x < 875 and 150 < y < 185 or 500 < x < 875 and 270 < y < 305:#opcion a y c
                            if flag_musica:
                                sonido_res_incorrecta.play()
                            if coordenadas[1] == 395:
                                coordenadas = retroceder_personaje_ariiba(coordenadas)
                            else:
                                coordenadas = retroceder_personaje_abajo(coordenadas)
                            ya_respondio = True
                            segundos = "0"

                    if respuestas_correctas[n_pregunta] == "c":
                        if 500 < x < 875 and 270 < y < 305:#opcion c
                            if flag_musica:
                                sonido_res_correcta.play()
                            puntaje += 10
                            if coordenadas[1] == 395:
                                if coordenadas[0] == 625 and not avanza1:
                                    coordenadas[0] += 190
                                    avanza1 = True
                                else:
                                    coordenadas = avanzar_personaje_casilleros_ariiba(coordenadas)
                            else:
                                if coordenadas == [625,520] and not retrocede1:
                                    coordenadas[0] = 720
                                    retrocede1 = True
                                else:
                                    coordenadas = avanzar_personaje_casilleros_abajo(coordenadas)
                            ya_respondio = True
                            segundos = "0"

                        elif 500 < x < 875 and 150 < y < 185 or 500 < x < 875 and 210 < y < 245:#opcion a y b
                            if flag_musica:
                                sonido_res_incorrecta.play()
                            if coordenadas[1] == 395:
                                coordenadas = retroceder_personaje_ariiba(coordenadas)
                            else:
                                coordenadas = retroceder_personaje_abajo(coordenadas)
                            ya_respondio = True
                            segundos = "0"

    pantalla.fill(COLOR_BLANCO)
    pantalla.blit(imagen_nube,(250,-120))
    pantalla.blit(imagen_casilleros,(120,500))
    pantalla.blit(imagen_logo,(50,50))
    if coordenadas[1] == 395:
        pantalla.blit(imagen_personaje,coordenadas)
    else:
        pantalla.blit(imagen_personaje_abajo,coordenadas)

    pygame.draw.rect(pantalla, COLOR_VIOLETA, (200,800,200,60), border_radius=15)#comenzar
    pygame.draw.rect(pantalla, COLOR_VIOLETA, (900,800,200,60), border_radius=15)#terminar
    if comenzar:
        pygame.draw.rect(pantalla, COLOR_BLANCO, (490,150,375,35), border_radius=15)#a
        pygame.draw.rect(pantalla, COLOR_BLANCO, (490,210,375,35), border_radius=15)#b
        pygame.draw.rect(pantalla, COLOR_BLANCO, (490,270,375,35), border_radius=15)#c

    texto_score = fuente.render(str(f"Score: {puntaje}"), True, COLOR_VIOLETA)
    pantalla.blit(texto_score,(650 - texto_score.get_width()/2,810))
    pantalla.blit(texto_comenzar,(220,810))
    pantalla.blit(texto_terminar,(930,810))
    segundos_texto = fuente.render(str(f"Tiempo: {segundos}"),True,COLOR_VIOLETA)
    pantalla.blit(segundos_texto,(1050,100))

    if comenzar:
        mostrar_pregunta_tema(pantalla,n_pregunta,temas,preguntas,fuente_pregunta_tema)
        mostrar_opciones(pantalla,n_pregunta,preguntas,respuestas_a,respuestas_b,respuestas_c,fuente)
    
    if flag_game_over:
        nombre = obtener_nombre_jugador(pantalla, puntaje)
        guardar_puntajes(nombre,puntaje)
        comenzar = False
        flag_game_over = False
        flag_mostrar_puntajes = True

    if flag_mostrar_puntajes:
        mostrar_puntajes(pantalla)

    if flag_musica:
        pantalla.blit(imagen_volumen,(20,800))
    else:
        pantalla.blit(imagen_no_volumen,(-10,800))

    pygame.display.flip() #actualizacion de pantalla

pygame.quit()
