import pygame
from constantes import *
import json

def renderizar_texto(pantalla, texto: str, color: str, posicion_y: int, fuente: str):
    """Esta funcion renderiza y blitea un texto.

    Parametros:
    (pantalla) -> any
    (texto)-> str
    (color) -> str
    (posicion_y) -> int
    (fuente) -> str
    """
    texto_renderizado = fuente.render(texto, True, color)
    pantalla.blit(texto_renderizado, (650 - texto_renderizado.get_width()/2, posicion_y))

def mostrar_opciones(pantalla, n_pregunta: int, preguntas: list, resa: list, resb: list, resc: list, fuente):
    """
    Esta funcion va a renderizar por pantalla las preguntas y respuestas por orden segun listas paralelas.

    Parametros:
    (pantalla) -> any
    (n_pregunta)-> int
    (preguntas) -> list
    (resa) -> list
    (resb) -> list
    (resc) -> list
    (fuente) -> any
    """
    if n_pregunta <= len(preguntas)-1:
        renderizar_texto(pantalla, resa[n_pregunta], COLOR_VIOLETA, 150, fuente)
        renderizar_texto(pantalla, resb[n_pregunta], COLOR_VIOLETA, 210, fuente)
        renderizar_texto(pantalla, resc[n_pregunta], COLOR_VIOLETA, 270, fuente)

def mostrar_pregunta_tema(pantalla, n_pregunta: int, temas: list, preguntas: list, fuente):
    """
    Esta funcion va a renderizar por pantalla los temas y preguntas por orden segun listas paralelas.

    Parametros:
    (pantalla) -> any
    (n_pregunta)-> int
    (temas) -> list
    (preguntas) -> list
    (fuente) -> any
    """
    if n_pregunta <= len(preguntas)-1:
        renderizar_texto(pantalla, f"Tema: {temas[n_pregunta]}", COLOR_VIOLETA, 50, fuente)
        renderizar_texto(pantalla, preguntas[n_pregunta], COLOR_VIOLETA, 90, fuente)

def avanzar_personaje_casilleros_ariiba(coordenadas:list) -> list:
    """
    Esta funcion va a avanzar al personaje en la parte superior del tablero segun el casillero
    y retorna las coordenadas en forma de lista.

    Parametros:
    (coordenadas) -> list

    Return:
    (coordenadas) -> list
    """
    if coordenadas == [910,395]:#ultimo casillero de arriba
        coordenadas = [910,520]#primer casillero de abajo
    if coordenadas[0] <= 815:#del anteultimo casillero para atras
        coordenadas[0] += 95
    return coordenadas

def avanzar_personaje_casilleros_abajo(coordenadas:list) -> list:
    """
    Esta funcion va a avanzar al personaje en la parte inferior del tablero segun el casillero
    y retorna las coordenadas en forma de lista.

    Parametros:
    (coordenadas) -> list

    Return:
    (coordenadas) -> list   
    """
    if 150 < coordenadas[0]:#llegada
        coordenadas[0] -= 95
    return coordenadas

def retroceder_personaje_ariiba(coordenadas:list) -> list:
    """
    Esta funcion va a retroceder al personaje en la parte suprior del tablero segun el casillero
    y retorna las coordenadas en forma de lista.

    Parametros:
    (coordenadas) -> list

    Return:
    (coordenadas) -> list 
    """
    if coordenadas == [150,395]:#inicio
        coordenadas = [150,395]
    else:
        coordenadas[0] -= 95
    return coordenadas

def retroceder_personaje_abajo(coordenadas:list) -> list:
    """
    Esta funcion va a retroceder al personaje en la parte inferior del tablero segun el casillero
    y retorna las coordenadas en forma de lista.

    Parametros:
    (coordenadas) -> list

    Return:
    (coordenadas) -> list 
    """
    if coordenadas == [910,520]:#primer casillero de abajo
         coordenadas = [910,395]#ultimo casillero de arriba
    if coordenadas[0] != 910:
        coordenadas[0] += 95
    return coordenadas

def obtener_nombre_jugador(pantalla, puntaje: int) -> str:
    """
    Esta funcion le pide el nombre al jugador por pantalla y lo retorna,
    blitea el score del jugador y 'GAME OVER'.

    Parametros:
    (pantalla) -> any
    (puntaje) -> int

    Return:
    (nombre) -> str 
    """
    nombre = ""
    fuente = pygame.font.SysFont("Arial", 60)
    while True:
        
        pygame.display.flip()   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return nombre
                if event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode
        pantalla.fill(COLOR_VIOLETA)
        text_ingrese_nombre = fuente.render("Ingrese su nombre:", True, COLOR_BLANCO)
        pantalla.blit(text_ingrese_nombre, (660 - text_ingrese_nombre.get_width() / 2, 200))
        nombre_jugador = fuente.render(nombre, True, COLOR_BLANCO)
        pantalla.blit(nombre_jugador,(660 - text_ingrese_nombre.get_width() / 2, 400))
        texto_game_over = fuente.render(str("GAME OVER"), True, COLOR_BLANCO)
        pantalla.blit(texto_game_over,(660 - texto_game_over.get_width() / 2 , 100))
        texto_score = fuente.render(str(f"Score: {puntaje}"), True, COLOR_BLANCO)
        pantalla.blit(texto_score,(650 - texto_score.get_width()/2,810))

def guardar_puntajes(nombre: str, puntaje: int):
    """
    Esta funcion crea (si no existe) un archivo json (scores.json) donde guarda los puntajes y el nombre de los jugadores,
    ordena los puntajes de forma descendente .

    Parametros:
    (nombre) -> str
    (puntaje) -> int
    """
    try:
        with open('scores.json', 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    scores.append({"nombre": nombre, "score": puntaje})
    scores = sorted(scores, key=lambda s: s["score"], reverse=True)[:10]

    with open('scores.json', 'w') as file:
        json.dump(scores, file)          

def mostrar_puntajes(pantalla):
    """
    Esta funcion carga un archivo json y carga los puntajes de forma ordenada para renderizarlos por pantalla.

    Parametros:
    (pantalla) -> any
    """

    fuente_titulo = pygame.font.SysFont("Arial", 80)
    fuente_puntaje = pygame.font.SysFont("Arial", 50)
    try:
        with open('scores.json', 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    pantalla.fill(COLOR_VIOLETA)
    imagen_logo = pygame.image.load("logo-utn.png")
    imagen_logo = pygame.transform.scale(imagen_logo,(300,75))
    pantalla.blit(imagen_logo,(50,50))
    imagen_personaje = pygame.image.load("personaje.png")
    imagen_personaje = pygame.transform.scale(imagen_personaje,(300,300))
    pantalla.blit(imagen_personaje,(20,200))
    texto_titulo = fuente_titulo.render(str("Top 10 puntajes:"),True,COLOR_BLANCO)
    pantalla.blit(texto_titulo,(650 - texto_titulo.get_width()/2,50))
    y = 200
    for score in scores:
        texto_puntaje = fuente_puntaje.render(str(f"{ score['nombre']}: {score['score']}"),True,COLOR_BLANCO)
        pantalla.blit(texto_puntaje,(550,y))
        y += 50

    pygame.display.flip()