
import sys
import unicodedata
import pygame

# Instale o Pygame no terminal: python -m pip install pygame
# Execute este arquivo: python jogo.py

pygame.init()
pygame.key.start_text_input()

LARGURA, ALTURA = 1000, 700
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("duvida ou confia")
RELOGIO = pygame.time.Clock()

FUNDO = (18, 22, 38)
PAINEL = (32, 40, 64)
PAINEL_ATIVO = (48, 60, 91)
BRANCO = (245, 247, 255)
CINZA = (174, 184, 207)
AZUL = (75, 135, 245)
VERDE = (55, 190, 130)
VERMELHO = (230, 75, 95)
AMARELO = (255, 205, 92)

FONTE_PEQUENA = pygame.font.SysFont("arial", 18)
FONTE = pygame.font.SysFont("arial", 24)
FONTE_MEDIA = pygame.font.SysFont("arial", 32, bold=True)
FONTE_TITULO = pygame.font.SysFont("arial", 46, bold=True)

TOP10 = {
    "Músicas populares": [
        "Die With A Smile", "APT.", "Birds of a Feather", "Espresso",
        "Beautiful Things", "Lose Control", "Too Sweet", "Please Please Please",
        "Not Like Us", "I Had Some Help"
    ],
    "Filmes famosos": [
        "Titanic", "Avatar", "Vingadores: Ultimato", "Star Wars: O Despertar da Força",
        "Vingadores: Guerra Infinita", "Homem-Aranha: Sem Volta Para Casa",
        "Jurassic World", "O Rei Leão", "Os Vingadores", "Velozes e Furiosos 7"
    ],
    "Jogos populares": [
        "Minecraft", "Grand Theft Auto V", "Tetris", "Wii Sports", "PUBG",
        "Mario Kart 8", "Red Dead Redemption 2", "Skyrim", "Terraria", "The Witcher 3"
    ],
    "Desenhos e animes": [
        "Dragon Ball", "Naruto", "One Piece", "Pokémon", "Demon Slayer",
        "Attack on Titan", "Os Simpsons", "Bob Esponja", "Tom e Jerry", "Rick and Morty"
    ],
    "Esportes": [
        "Futebol", "Basquete", "Críquete", "Tênis", "Vôlei",
        "Tênis de mesa", "Beisebol", "Golfe", "Rúgbi", "Fórmula 1"
    ],
}

def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn").strip()

def escrever(texto, x, y, fonte=FONTE, cor=BRANCO, centro=False):
    imagem = fonte.render(str(texto), True, cor)
    rect = imagem.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    TELA.blit(imagem, rect)

def botao(rect, legenda, cor=AZUL, fonte=FONTE):
    cor_final = tuple(min(255, c + 18) for c in cor) if rect.collidepoint(pygame.mouse.get_pos()) else cor
    pygame.draw.rect(TELA, cor_final, rect, border_radius=10)
    imagem = fonte.render(legenda, True, BRANCO)
    TELA.blit(imagem, imagem.get_rect(center=rect.center))

def caixa(rect, valor, ativa=False, dica=""):
    pygame.draw.rect(TELA, PAINEL_ATIVO if ativa else PAINEL, rect, border_radius=8)
    pygame.draw.rect(TELA, AZUL if ativa else (76, 87, 117), rect, 2 if ativa else 1, border_radius=8)
    conteudo = valor if valor else dica
    imagem = FONTE_PEQUENA.render(conteudo, True, BRANCO if valor else CINZA)
    TELA.blit(imagem, (rect.x + 10, rect.y + (rect.height - imagem.get_height()) // 2))

def fundo(titulo, subtitulo=""):
    TELA.fill(FUNDO)
    pygame.draw.circle(TELA, (26, 34, 57), (0, 0), 220)
    pygame.draw.circle(TELA, (24, 31, 53), (LARGURA, ALTURA), 260)
    escrever(titulo, LARGURA // 2, 48, FONTE_TITULO, BRANCO, True)
    if subtitulo:
        escrever(subtitulo, LARGURA // 2, 94, FONTE_PEQUENA, CINZA, True)

# Todas as áreas clicáveis têm posições fixas.
BOTAO_MENOS = pygame.Rect(350, 130, 50, 42)
BOTAO_MAIS = pygame.Rect(500, 130, 50, 42)
BOTAO_CATEGORIA = pygame.Rect(350, 590, 300, 55)
CAMPOS_NOME = [pygame.Rect(80 + (i // 5) * 430, 235 + (i % 5) * 62, 380, 46) for i in range(10)]
BOTOES_CATEGORIA = {
    nome: pygame.Rect(250, 150 + i * 78, 500, 58)
    for i, nome in enumerate(TOP10.keys())
}
BOTAO_VOLTAR = pygame.Rect(40, 620, 150, 48)
BOTAO_COMECAR = pygame.Rect(690, 620, 270, 48)
CAIXA_RESPOSTA = pygame.Rect(395, 385, 500, 52)
BOTAO_ENVIAR = pygame.Rect(535, 455, 220, 54)
BOTAO_DUVIDAR = pygame.Rect(340, 390, 230, 58)
BOTAO_CONFIAR = pygame.Rect(600, 390, 230, 58)
BOTAO_CONTINUAR = pygame.Rect(370, 450, 260, 58)
BOTAO_NOVAMENTE = pygame.Rect(350, 430, 300, 58)
BOTAO_SAIR = pygame.Rect(390, 510, 220, 50)
BOTAO_VOLTAR_DESAFIO = pygame.Rect(100, 615, 170, 48)

estado = "menu"
quantidade = 4
nomes = [f"Jogador {i+1}" for i in range(10)]
campo_nome_ativo = 0
categoria = "Músicas populares"
jogadores = []
indice_atual = 0
resposta = ""
texto_resposta = ""
campo_resposta_ativo = True
desafiante = None
mensagem = ""
detalhe = ""
aviso = ""

def jogadores_ativos():
    return [j for j in jogadores if j["ativo"]]

def jogador_da_vez():
    vivos = jogadores_ativos()
    if not vivos:
        return None
    return vivos[indice_atual % len(vivos)]

def iniciar_partida():
    global jogadores, indice_atual, estado, resposta, texto_resposta, desafiante, aviso
    jogadores = [{"nome": nomes[i].strip() or f"Jogador {i+1}", "ativo": True} for i in range(quantidade)]
    indice_atual = 0
    resposta = ""
    texto_resposta = ""
    desafiante = None
    aviso = ""
    estado = "resposta"

def proximo_turno():
    global indice_atual, estado, resposta, texto_resposta, desafiante, aviso
    vivos = jogadores_ativos()
    if len(vivos) <= 1:
        estado = "fim"
        return
    atual = jogador_da_vez()
    if atual in vivos:
        indice_atual = (vivos.index(atual) + 1) % len(vivos)
    resposta = ""
    texto_resposta = ""
    desafiante = None
    aviso = ""
    estado = "resposta"

def desenhar_menu():
    fundo("DUVIDA OU CONFIA", "Configure os jogadores")
    escrever("Quantidade de jogadores:", 80, 140)
    botao(BOTAO_MENOS, "−", PAINEL_ATIVO)
    botao(BOTAO_MAIS, "+", PAINEL_ATIVO)
    escrever(quantidade, 450, 151, FONTE_MEDIA, BRANCO, True)
    escrever("Clique em um campo e digite o nome. Use Backspace para apagar.", 80, 198, FONTE_PEQUENA, CINZA)
    for i in range(quantidade):
        caixa(CAMPOS_NOME[i], nomes[i], campo_nome_ativo == i, f"Nome do jogador {i+1}")
    botao(BOTAO_CATEGORIA, "Escolher categoria", VERDE)

def desenhar_categorias():
    fundo("Escolha uma categoria", "As listas de referência ficam escondidas dos jogadores")
    for nome, rect in BOTOES_CATEGORIA.items():
        botao(rect, nome, VERDE if nome == categoria else AZUL)
    botao(BOTAO_VOLTAR, "Voltar", PAINEL_ATIVO)
    botao(BOTAO_COMECAR, "Começar partida", VERDE)

def desenhar_lista_jogadores():
    escrever("Jogadores", 60, 125, FONTE, BRANCO)
    y = 165
    for j in jogadores:
        cor = VERDE if j["ativo"] else CINZA
        status = "EM JOGO" if j["ativo"] else "ELIMINADO"
        pygame.draw.rect(TELA, PAINEL, pygame.Rect(60, y, 260, 38), border_radius=7)
        escrever(j["nome"], 72, y + 8, FONTE_PEQUENA, cor)
        escrever(status, 220, y + 9, pygame.font.SysFont("arial", 13), cor)
        y += 44
    escrever(f"Restam {len(jogadores_ativos())} jogador(es)", 60, min(y + 5, 640), FONTE_PEQUENA, AMARELO)

def desenhar_resposta():
    fundo("Sua vez!", f"Categoria: {categoria}")
    desenhar_lista_jogadores()
    atual = jogador_da_vez()
    if not atual:
        return
    pygame.draw.rect(TELA, PAINEL, pygame.Rect(355, 145, 585, 405), border_radius=16)
    escrever("Quem está jogando?", 395, 180, FONTE_PEQUENA, CINZA)
    escrever(atual["nome"], 395, 215, FONTE_MEDIA, VERDE)
    escrever("Digite uma resposta que você afirma estar no Top 10.", 395, 280, FONTE_PEQUENA)
    escrever("Clique na caixa abaixo e digite:", 395, 325, FONTE_PEQUENA, CINZA)
    caixa(CAIXA_RESPOSTA, texto_resposta, campo_resposta_ativo, "Digite sua resposta...")
    botao(BOTAO_ENVIAR, "Confirmar resposta", VERDE)
    escrever("Depois, os outros jogadores podem confiar ou duvidar.", 395, 525, FONTE_PEQUENA, CINZA)
    if aviso:
        escrever(aviso, 395, 555, FONTE_PEQUENA, AMARELO)

def desenhar_desafio():
    fundo("Duvida ou confia?", f"Categoria: {categoria}")
    atual = jogador_da_vez()
    if not atual:
        return
    pygame.draw.rect(TELA, PAINEL, pygame.Rect(300, 150, 640, 360), border_radius=16)
    escrever(f"{atual['nome']} respondeu:", 340, 190, FONTE_PEQUENA, CINZA)
    escrever(f"“{resposta}”", 340, 245, FONTE_MEDIA, AMARELO)
    escrever("Alguém duvida dessa resposta?", 340, 330, FONTE)
    botao(BOTAO_DUVIDAR, "Duvidar", VERMELHO)
    botao(BOTAO_CONFIAR, "Confiar", VERDE)
    escrever("Se todos confiarem, ninguém é eliminado.", 340, 475, FONTE_PEQUENA, CINZA)

def desenhar_escolher_desafiante():
    fundo("Quem está duvidando?", "Escolha quem desafiou a resposta")
    atual = jogador_da_vez()
    if atual:
        escrever(f"{atual['nome']} respondeu: “{resposta}”", 100, 130, FONTE_MEDIA, AMARELO)
    escrever("Clique no nome de quem duvida:", 100, 190, FONTE)
    candidatos = [j for j in jogadores_ativos() if j is not atual]
    for i, j in enumerate(candidatos):
        rect = pygame.Rect(100 + (i % 2) * 410, 245 + (i // 2) * 72, 360, 54)
        botao(rect, j["nome"], VERMELHO)
    botao(BOTAO_VOLTAR_DESAFIO, "Voltar", PAINEL_ATIVO)

# FUNÇÃO CORRIGIDA
def resolver_desafio():
    global estado, mensagem, detalhe

    atual = jogador_da_vez()
    lista = {normalizar(item) for item in TOP10[categoria]}

    if normalizar(resposta) in lista:
        # Resposta correta: quem duvidou é eliminado.
        desafiante["ativo"] = False
        mensagem = f"{desafiante['nome']} foi eliminado!"
        detalhe = f"“{resposta}” estava na lista do Top 10. {atual['nome']} acertou!"

    else:
        # Resposta errada: quem respondeu é eliminado.
        atual["ativo"] = False
        mensagem = f"{atual['nome']} foi eliminado!"
        detalhe = f"“{resposta}” não estava na lista do Top 10. {desafiante['nome']} tinha razão!"

    estado = "resultado"

def desenhar_resultado():
    fundo("Resultado do desafio")
    pygame.draw.rect(TELA, PAINEL, pygame.Rect(170, 170, 660, 340), border_radius=16)
    escrever(mensagem, 500, 245, FONTE_MEDIA, AMARELO, True)
    escrever(detalhe, 500, 315, FONTE, BRANCO, True)
    botao(BOTAO_CONTINUAR, "Continuar", VERDE)

def desenhar_fim():
    fundo("Fim de jogo!")
    vivos = jogadores_ativos()
    if vivos:
        escrever(f"Vencedor: {vivos[0]['nome']}", 500, 270, FONTE_TITULO, VERDE, True)
    escrever("Só termina quando resta um jogador.", 500, 340, FONTE, BRANCO, True)
    botao(BOTAO_NOVAMENTE, "Jogar novamente", VERDE)
    botao(BOTAO_SAIR, "Sair", VERMELHO)

rodando = True
while rodando:
    RELOGIO.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos

            if estado == "menu":
                campo_nome_ativo = None
                for i in range(quantidade):
                    if CAMPOS_NOME[i].collidepoint(pos):
                        campo_nome_ativo = i
                        break
                if BOTAO_MENOS.collidepoint(pos):
                    quantidade = max(3, quantidade - 1)
                    if campo_nome_ativo is not None:
                        campo_nome_ativo = min(campo_nome_ativo, quantidade - 1)
                elif BOTAO_MAIS.collidepoint(pos):
                    quantidade = min(10, quantidade + 1)
                elif BOTAO_CATEGORIA.collidepoint(pos):
                    estado = "categoria"

            elif estado == "categoria":
                if BOTAO_VOLTAR.collidepoint(pos):
                    estado = "menu"
                elif BOTAO_COMECAR.collidepoint(pos):
                    iniciar_partida()
                else:
                    for nome, rect in BOTOES_CATEGORIA.items():
                        if rect.collidepoint(pos):
                            categoria = nome
                            break

            elif estado == "resposta":
                campo_resposta_ativo = CAIXA_RESPOSTA.collidepoint(pos)
                if BOTAO_ENVIAR.collidepoint(pos):
                    if texto_resposta.strip():
                        resposta = texto_resposta.strip()
                        texto_resposta = ""
                        aviso = ""
                        estado = "desafio"
                    else:
                        aviso = "Digite uma resposta antes de confirmar."

            elif estado == "desafio":
                if BOTAO_DUVIDAR.collidepoint(pos):
                    estado = "escolher_desafiante"
                elif BOTAO_CONFIAR.collidepoint(pos):
                    proximo_turno()

            elif estado == "escolher_desafiante":
                if BOTAO_VOLTAR_DESAFIO.collidepoint(pos):
                    estado = "desafio"
                else:
                    atual = jogador_da_vez()
                    candidatos = [j for j in jogadores_ativos() if j is not atual]
                    for i, j in enumerate(candidatos):
                        rect = pygame.Rect(100 + (i % 2) * 410, 245 + (i // 2) * 72, 360, 54)
                        if rect.collidepoint(pos):
                            desafiante = j
                            resolver_desafio()
                            break

            elif estado == "resultado":
                if BOTAO_CONTINUAR.collidepoint(pos):
                    proximo_turno()

            elif estado == "fim":
                if BOTAO_NOVAMENTE.collidepoint(pos):
                    estado = "menu"
                    campo_nome_ativo = 0
                elif BOTAO_SAIR.collidepoint(pos):
                    rodando = False

        elif evento.type == pygame.KEYDOWN:
            if estado == "menu" and campo_nome_ativo is not None:
                if evento.key == pygame.K_BACKSPACE:
                    nomes[campo_nome_ativo] = nomes[campo_nome_ativo][:-1]
                elif evento.key == pygame.K_RETURN:
                    campo_nome_ativo = None

            elif estado == "resposta" and campo_resposta_ativo:
                if evento.key == pygame.K_BACKSPACE:
                    texto_resposta = texto_resposta[:-1]
                elif evento.key == pygame.K_RETURN:
                    if texto_resposta.strip():
                        resposta = texto_resposta.strip()
                        texto_resposta = ""
                        aviso = ""
                        estado = "desafio"
                    else:
                        aviso = "Digite uma resposta antes de confirmar."

            elif evento.key == pygame.K_ESCAPE:
                if estado == "categoria":
                    estado = "menu"
                elif estado == "escolher_desafiante":
                    estado = "desafio"

        elif evento.type == pygame.TEXTINPUT:
            if estado == "menu" and campo_nome_ativo is not None:
                i = campo_nome_ativo
                if len(nomes[i]) < 20:
                    nomes[i] += evento.text
            elif estado == "resposta" and campo_resposta_ativo:
                if len(texto_resposta) < 50:
                    texto_resposta += evento.text

    if estado == "menu":
        desenhar_menu()
    elif estado == "categoria":
        desenhar_categorias()
    elif estado == "resposta":
        desenhar_resposta()
    elif estado == "desafio":
        desenhar_desafio()
    elif estado == "escolher_desafiante":
        desenhar_escolher_desafiante()
    elif estado == "resultado":
        desenhar_resultado()
    elif estado == "fim":
        desenhar_fim()

    pygame.display.flip()

pygame.key.stop_text_input()
pygame.quit()
sys.exit()

