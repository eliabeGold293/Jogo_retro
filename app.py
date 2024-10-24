import pygame
import os
import random

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
tela_largura = 500
tela_altura = 800
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption('InteresteLLar')

# Carregar imagens
imagem_nave_jogador = pygame.image.load(os.path.join('imgs', 'R.png')).convert_alpha()
imagem_nave_inimiga = pygame.image.load(os.path.join('imgs', 'nave_inimiganv.png')).convert_alpha()
imagem_projetil = pygame.image.load(os.path.join('imgs', 'tiro_img.png')).convert_alpha()
imagem_projetil_inimigo = pygame.image.load(os.path.join('imgs', 'projetil_inimigo.gif')).convert_alpha()
coracao_imagem = pygame.image.load(os.path.join('imgs', 'newcoracao.png')).convert_alpha()
explosao = pygame.image.load(os.path.join('imgs', 'explosaorm.png')).convert_alpha()  # imagem explosão
background = pygame.image.load(os.path.join('imgs', 'backgroundoutrom.png')).convert_alpha()

# Ajustar o tamanho das imagens
imagem_nave_jogador = pygame.transform.scale(imagem_nave_jogador, (50, 50))
imagem_nave_inimiga = pygame.transform.scale(imagem_nave_inimiga, (50, 50))
imagem_projetil = pygame.transform.scale(imagem_projetil, (10, 20))
imagem_projetil_inimigo = pygame.transform.scale(imagem_projetil_inimigo, (10, 20))
coracao_imagem = pygame.transform.scale(coracao_imagem, (30, 30))
background = pygame.transform.scale(background, (tela_largura, tela_altura))

# Definindo as fontes
pygame.font.init()
fonte_pontos = pygame.font.Font('PixelCaps-LOnE.ttf', 25)
fonte_menu = pygame.font.Font('PixelCaps-LOnE.ttf', 25)

# Carregar música de fundo
#pygame.mixer.music.load(os.path.join('musicas_e_sons', 'musica_fundo.mp3'))
pygame.mixer.music.load(os.path.join('musicas_e_sons', 'musica_fundo2.mp3'))
pygame.mixer.music.play(-1)

# Classe da Nave do Jogador
class NaveJogador:
    def __init__(self):
        self.imagem = imagem_nave_jogador
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.x = tela_largura // 2 - self.largura // 2
        self.y = tela_altura - self.altura - 10
        self.velocidade = 5
        self.vidas = 5

    def mover(self, sentido):
        if sentido == "direita" and self.x + self.largura < tela_largura:
            self.x += self.velocidade
        elif sentido == "esquerda" and self.x > 0:
            self.x -= self.velocidade
        elif sentido == "cima" and self.y > 0:
            self.y -= self.velocidade
        elif sentido == "baixo" and self.y + self.altura < tela_altura:
            self.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

# Classe da Nave Inimiga
class NaveInimiga:
    def __init__(self):
        self.imagem = pygame.transform.flip(imagem_nave_inimiga, True, False)
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.x = random.randint(0, tela_largura - self.largura)
        self.y = 0
        self.velocidade = 2
        self.tempo_disparo = 0
        self.cadencia_tiro = 2000  # Tempo entre os disparos em milissegundos
        self.ultimo_disparo = 0  # Armazena o tempo do último disparo

    def mover(self):
        self.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

    def disparar(self, tempo_atual):
        if tempo_atual - self.ultimo_disparo >= self.cadencia_tiro:
            self.ultimo_disparo = tempo_atual
            return ProjetilInimigo(self.x, self.y)
        return None

# Classe do Projetil do Jogador
class Projetil:
    def __init__(self, x, y):
        self.imagem = imagem_projetil
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.x = x + (25 - self.largura // 2)
        self.y = y
        self.velocidade = 10

    def mover(self):
        self.y -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

# Classe do Projetil Inimigo
class ProjetilInimigo:
    def __init__(self, x, y):
        self.imagem = imagem_projetil_inimigo
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.x = x + (25 - self.largura // 2)
        self.y = y + 50  # Ajuste para disparar a partir da parte inferior da nave
        self.velocidade = 5

    def mover(self):
        self.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

# Classe do Coração
class Coracao:
    def __init__(self, x, y):
        self.imagem = coracao_imagem
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.x = x
        self.y = y
        self.velocidade = 2  # velocidade com que o coração cai

    def mover(self):
        self.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

# Classe da Explosão
class Explosao:
    def __init__(self, x, y, largura_nave):
        # Redimensionar a imagem da explosão com base na largura da nave inimiga
        fator_redimensionamento = 1.5  # Ajuste este valor para aumentar ou diminuir a explosão
        self.imagem = pygame.transform.scale(explosao, (int(largura_nave * fator_redimensionamento), int(largura_nave * fator_redimensionamento)))
        self.x = x
        self.y = y
        self.duracao = 500  # Duração da explosão em milissegundos
        self.inicio = pygame.time.get_ticks()

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x - self.imagem.get_width() // 2, self.y - self.imagem.get_height() // 2))

    def esta_expirada(self):
        return pygame.time.get_ticks() - self.inicio > self.duracao

# Função para mostrar a tela de menu
def mostrar_menu():
    while True:
        tela.fill((0, 0, 0))
        texto_menu = fonte_menu.render('InteresteLLar', True, (255, 255, 255))
        texto_start = fonte_menu.render('Pressione ENTER para iniciar', True, (255, 255, 255))
        tela.blit(texto_menu, (tela_largura // 2 - texto_menu.get_width() // 2, 200))
        tela.blit(texto_start, (tela_largura // 2 - texto_start.get_width() // 2, 400))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return  # Inicia o jogo

# Função para mostrar a tela de Game Over
def mostrar_game_over(pontos):
    while True:
        tela.fill((0, 0, 0))
        texto_game_over = fonte_menu.render('GAME OVER', True, (255, 0, 0))
        texto_pontuacao = fonte_pontos.render(f'Pontos: {pontos}', True, (255, 255, 255))
        texto_reiniciar = fonte_menu.render('Pressione ENTER para reiniciar', True, (255, 255, 255))
        tela.blit(texto_game_over, (tela_largura // 2 - texto_game_over.get_width() // 2, 200))
        tela.blit(texto_pontuacao, (tela_largura // 2 - texto_pontuacao.get_width() // 2, 400))
        tela.blit(texto_reiniciar, (tela_largura // 2 - texto_reiniciar.get_width() // 2, 500))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return  # Reinicia o jogo

def main():
    clock = pygame.time.Clock()
    run = True
    nave_jogador = NaveJogador()
    naves_inimigas = []
    projeteis = []
    projeteis_inimigos = []
    coracoes = []  # Lista para armazenar corações
    explosoes = []  # Lista para armazenar explosões
    pontos = 0

    # Variáveis de controle de disparo
    tempo_disparo = 0
    cadencia_tiro = 200

    while run:
        clock.tick(60)
        tela.blit(background, (0, 0))

        tempo_atual = pygame.time.get_ticks()  # Tempo atual em milissegundos

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False

        # Movimentação da nave do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            nave_jogador.mover("direita")
        if keys[pygame.K_a]:
            nave_jogador.mover("esquerda")
        if keys[pygame.K_w]:
            nave_jogador.mover("cima")
        if keys[pygame.K_s]:
            nave_jogador.mover("baixo")

        # Disparo contínuo quando a barra de espaço estiver pressionada
        if keys[pygame.K_SPACE]:
            if tempo_disparo >= cadencia_tiro:
                if len(projeteis) < 5:
                    projeteis.append(Projetil(nave_jogador.x, nave_jogador.y))
                tempo_disparo = 0
        tempo_disparo += clock.get_time()

        # Adicionar novas naves inimigas
        if random.randint(1, 50) == 1:
            naves_inimigas.append(NaveInimiga())

        # Atualizar e desenhar naves inimigas
        for nave in list(naves_inimigas):
            nave.mover()
            nave.desenhar(tela)

            if nave.y > tela_altura:
                naves_inimigas.remove(nave)

            # Verifica colisão com a nave do jogador
            if (nave.x < nave_jogador.x + nave_jogador.largura and
                nave.x + nave.largura > nave_jogador.x and
                nave.y < nave_jogador.y + nave_jogador.altura and
                nave.y + nave.altura > nave_jogador.y):
                nave_jogador.vidas -= 1
                naves_inimigas.remove(nave)

            # Dispara projétil da nave inimiga
            projeteis_inimigo = nave.disparar(tempo_atual)
            if projeteis_inimigo:
                projeteis_inimigos.append(projeteis_inimigo)

        # Verificar se o jogo deve parar
        if nave_jogador.vidas <= 0:
            mostrar_game_over(pontos)
            return

        # Atualizar e desenhar projéteis do jogador
        projeteis_para_remover = []
        for projeteis_ativos in projeteis:
            projeteis_ativos.mover()
            projeteis_ativos.desenhar(tela)

            if projeteis_ativos.y < 0:
                projeteis_para_remover.append(projeteis_ativos)

            # Verifica colisão com as naves inimigas
            for nave in list(naves_inimigas):
                if (projeteis_ativos.x < nave.x + nave.largura and
                    projeteis_ativos.x + projeteis_ativos.largura > nave.x and
                    projeteis_ativos.y < nave.y + nave.altura and
                    projeteis_ativos.y + projeteis_ativos.altura > nave.y):
                    explosoes.append(Explosao(nave.x + nave.largura // 2, nave.y + nave.altura // 2, nave.largura))
                    naves_inimigas.remove(nave)
                    projeteis_para_remover.append(projeteis_ativos)
                    pontos += 1

                    # Tenta dropar um coração
                    if random.random() < 0.18:  # 18% de chance de dropar um coração
                        coracoes.append(Coracao(nave.x + nave.largura // 2 - 15, nave.y + nave.altura))  # Ajuste a posição do coração
                    break

        # Remover projeteis do jogador que estão fora da tela ou que colidiram
        for projeteis_ativos in projeteis_para_remover:
            if projeteis_ativos in projeteis:
                projeteis.remove(projeteis_ativos)

        # Atualizar e desenhar projéteis inimigos
        for projeteis_inimigo in list(projeteis_inimigos):
            projeteis_inimigo.mover()
            projeteis_inimigo.desenhar(tela)

            if projeteis_inimigo.y > tela_altura:
                projeteis_inimigos.remove(projeteis_inimigo)

            # Verifica colisão com a nave do jogador
            if (projeteis_inimigo.x < nave_jogador.x + nave_jogador.largura and
                projeteis_inimigo.x + projeteis_inimigo.largura > nave_jogador.x and
                projeteis_inimigo.y < nave_jogador.y + nave_jogador.altura and
                projeteis_inimigo.y + projeteis_inimigo.altura > nave_jogador.y):
                nave_jogador.vidas -= 1
                projeteis_inimigos.remove(projeteis_inimigo)

        # Atualizar e desenhar corações
        coracoes_para_remover = []
        for coracao in list(coracoes):
            coracao.mover()
            coracao.desenhar(tela)

            # Verifica se o coração saiu da tela
            if coracao.y > tela_altura:
                coracoes_para_remover.append(coracao)

            # Verifica colisão com a nave do jogador
            if (coracao.x < nave_jogador.x + nave_jogador.largura and
                coracao.x + coracao.largura > nave_jogador.x and
                coracao.y < nave_jogador.y + nave_jogador.altura and
                coracao.y + coracao.altura > nave_jogador.y):

                if nave_jogador.vidas < 5:  # Verifica se o jogador tem menos de 5 vidas
                    nave_jogador.vidas += 1  # Aumenta a vida do jogador
                coracoes_para_remover.append(coracao)

        # Remover corações que saíram da tela ou foram coletados
        for coracao in coracoes_para_remover:
            if coracao in coracoes:
                coracoes.remove(coracao)

        # Desenhar as explosões
        for explosao in list(explosoes):
            explosao.desenhar(tela)
            if explosao.esta_expirada():
                explosoes.remove(explosao)

        # Desenhar a nave do jogador
        nave_jogador.desenhar(tela)

        # Mostrar pontuação e vidas como corações
        texto_pontos = fonte_pontos.render(f'Pontos: {pontos}', True, (255, 255, 255))
        tela.blit(texto_pontos, (10, 10))

        # Desenhar corações
        for i in range(nave_jogador.vidas):
            tela.blit(coracao_imagem, (10 + i * 35, 70))  # Aumentar o espaçamento entre os corações

        # Atualizar a tela
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    mostrar_menu()
    while True:
        main()
