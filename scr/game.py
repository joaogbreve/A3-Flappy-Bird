import pygame
import random

# Configuração da tela do jogo
pygame.init()
HEI = 720
WID = 549
TEL = pygame.display.set_mode((WID, HEI))
pygame.display.set_caption("Flappy Bird - Trabalho A3")

# Configuração do timing do jogo
CLOCK = pygame.time.Clock()
FPS = 60

# Localização dos assets do jogo
IMG = '../assets/images/'
SOU = '../assets/sounds/'
FON = '../assets/fonts/'
# https://www.fontspace.com/category/flappy-bird
FONT = pygame.font.Font(FON +"2.ttf", 25)

# Inicialização do som do jogo
pygame.mixer.init()
PONTO = pygame.mixer.Sound(SOU + 'point.wav')
PONTO.set_volume(0.3)
MORTE = pygame.mixer.Sound(SOU + 'hit.wav')
MORTE.set_volume(0.3)
PULO = pygame.mixer.Sound(SOU + 'wing.wav')
PULO.set_volume(0.3)
PLAY = pygame.mixer.Sound(SOU + 'swoosh.wav')
PLAY.set_volume(0.3)

# Dict para imagens dos números
NUM_IMAGES = {str(i): pygame.image.load(IMG + f'{i}.png') for i in range(10)}

MSG_TUTORIAL = {
    1: "pule com espaco",
    2: "evite os tubos",
    3: "sobreviva o quanto conseguir",
    4: "aperte m para voltar ao menu",
    5: "aperte p para iniciar o jogo",
}

MSG_MENU_PRINCIPAL = {
    1: "aperte p para iniciar o jogo",
    2: "iniciar o jogo",
    3: "aperte t para ver o tutorial",
    4: "ver o tutorial",
}

MSG_TELA_MORTE = {
    1: "aperte r para reiniciar",
    2: "aperte m para voltar ao menu",
}

class TelaManager:
    def __init__(self):
        self.pontuacao = 0
        self.current = MenuPrincipal(self)

    def go_to(self, tela):
        self.current = tela

class Tela:
    def __init__(self, manager):
        self.manager = manager

    def handle_events(self, events): pass
    def update(self): pass
    def draw(self, superficie): pass

class TelaMorte(Tela):
    def __init__(self, manager):
        super().__init__(manager)
        self.FUNDONOITE = pygame.image.load(IMG + 'background-night.png')
        self.logo = pygame.image.load(IMG + 'gameover.png')
        self.logo = pygame.transform.scale(self.logo, (368, 94))
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx = WID // 2
        self.logo_rect.y = 100

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    self.manager.go_to(MenuPrincipal(self.manager))
                if e.key == pygame.K_r:
                    self.manager.go_to(TelaJogo(self.manager))

    def draw(self, superficie):
        superficie.blit(self.FUNDONOITE, (0, 0))
        superficie.blit(self.logo, self.logo_rect)
        CentVariosTextos(superficie, MSG_TELA_MORTE, [1, 2], FONT)

class TelaTutorial(Tela):
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    self.manager.go_to(MenuPrincipal(self.manager))
                elif e.key == pygame.K_p:
                    self.manager.go_to(TelaJogo(self.manager))

    def draw(self, superficie):
        superficie.fill((0, 100, 200))
        CentVariosTextos(superficie, MSG_TUTORIAL, [1, 2, 3, 4, 5], FONT, espaco=30)

class MenuPrincipal(Tela):
    def __init__(self, manager):
        super().__init__(manager)
        self.FUNDOMENU = pygame.image.load(IMG + 'background-day.png')
        self.logo = pygame.image.load(IMG + 'logo.png')
        self.logo = pygame.transform.scale(self.logo, (368, 94))
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx = WID // 2
        self.logo_rect.y = 100

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    PLAY.play()
                    self.manager.go_to(TelaJogo(self.manager))
                if e.key == pygame.K_t:
                    self.manager.go_to(TelaTutorial(self.manager))

    def draw(self, superficie):
        superficie.blit(self.FUNDOMENU, (0, 0))
        superficie.blit(self.logo, self.logo_rect)
        CentVariosTextos(superficie, MSG_MENU_PRINCIPAL, [1, 3], FONT, espaco=30)

# O jogo funciona dentro desta tela em específico
class TelaJogo(Tela):
    def __init__(self, manager):
        super().__init__(manager)
        self.FUNDODIA = pygame.image.load(IMG + 'background-day.png')
        self.CHAO = pygame.image.load(IMG + 'base.png')
        self.LARGURA_FUNDO = self.FUNDODIA.get_width()
        self.LARGURA_CHAO = self.CHAO.get_width()

        self.mov_chao = 0
        self.mov_fundo = 0
        self.vel_chao = 4
        self.vel_fundo = 2

        self.jogador_grupo = pygame.sprite.Group()
        self.flappy = Jogador(100, HEI // 2)
        self.jogador_grupo.add(self.flappy)

        self.canos = pygame.sprite.Group()
        self.tempo_ultimo_cano = pygame.time.get_ticks()
        self.delay_entre_pipes = 1500

        self.pontuacao = 0


    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.flappy.pular()
                PULO.play()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                self.manager.go_to(MenuPrincipal(self.manager))


    def update(self):
        self.mov_fundo -= self.vel_fundo
        if self.mov_fundo <= -self.LARGURA_FUNDO:
            self.mov_fundo = 0

        self.mov_chao -= self.vel_chao
        if self.mov_chao <= -self.LARGURA_CHAO:
            self.mov_chao = 0

        self.jogador_grupo.update()

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_cano > self.delay_entre_pipes:
            self.tempo_ultimo_cano = tempo_atual
            novo_cano = Canos(WID + 50)
            self.canos.add(novo_cano)

        self.canos.update()

        for cano in self.canos:
            if not cano.ponto_contado and cano.top_rect.right < self.flappy.rect.left:
                cano.ponto_contado = True
                self.pontuacao += 1
                PONTO.play()
                print("PONTOS:", self.pontuacao) #debugging

        for cano in self.canos:
            if self.flappy.rect.colliderect(cano.top_rect) or self.flappy.rect.colliderect(cano.bottom_rect):
                self.manager.pontuacao = self.pontuacao
                MORTE.play()
                self.manager.go_to(TelaMorte(self.manager))

    def draw(self, superficie):
        superficie.blit(self.FUNDODIA, (self.mov_fundo, 0))
        superficie.blit(self.FUNDODIA, (self.mov_fundo + self.LARGURA_FUNDO, 0))

        self.jogador_grupo.draw(superficie)
        for cano in self.canos:
            cano.draw(superficie)

        superficie.blit(self.CHAO, (self.mov_chao, 612))
        superficie.blit(self.CHAO, (self.mov_chao + self.LARGURA_CHAO, 612))
        ConvPontos(self.pontuacao, superficie, 250, 20)

# Converte pontuação de int para imagem
def ConvPontos(score, surface, x, y):
    for digito in str(score):
        imagem = NUM_IMAGES[digito]
        surface.blit(imagem, (x, y))
        x += imagem.get_width()

def CentVariosTextos(superficie, textos_dict, chaves, fonte, cor=(255, 255, 255), espaco=100):
    linhas = [textos_dict[chave] for chave in chaves]
    total_altura = sum(fonte.size(linha)[1] for linha in linhas) + espaco * (len(linhas) - 1)
    inicio_y = (HEI - total_altura) // 2

    for linha in linhas:
        texto_renderizado = fonte.render(linha, True, cor)
        texto_rect = texto_renderizado.get_rect(center=(WID // 2, inicio_y + texto_renderizado.get_height() // 2))
        superficie.blit(texto_renderizado, texto_rect)
        inicio_y += texto_renderizado.get_height() + espaco


# ---------------------------------------------------------------------------------

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_down = pygame.image.load(IMG + 'redbird-downflap.png')
        self.image_mid = pygame.image.load(IMG + 'redbird-midflap.png')
        self.image_up = pygame.image.load(IMG + 'redbird-upflap.png')
        self.image = self.image_mid
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocidade = 0
        self.gravidade = 0.5
        self.forca_pulo = -10

    def update(self):
        self.velocidade += self.gravidade
        self.rect.y += self.velocidade

        if self.rect.bottom > 612:
            self.rect.bottom = 612
            self.velocidade = 0

        if self.velocidade > 0:
            self.image = self.image_up
        elif self.velocidade == 0:
            self.image = self.image_mid

    def pular(self):
        self.velocidade = self.forca_pulo
        self.image = self.image_down

class Canos(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image_cano = pygame.image.load(IMG + 'pipe-green.png')
        self.image_cano_top = pygame.transform.flip(self.image_cano, False, True)

        self.gap = 180  # Espaço entre os canos.
        self.velocidade = 4

        self.altura = random.randint(150, 450)
        self.top_rect = self.image_cano_top.get_rect(midbottom=(x, self.altura - self.gap // 2))
        self.bottom_rect = self.image_cano.get_rect(midtop=(x, self.altura + self.gap // 2))

        self.ponto_contado = False

    def update(self):
        self.top_rect.x -= self.velocidade
        self.bottom_rect.x -= self.velocidade

        # reset logic (optional, or remove pipes when offscreen)
        if self.top_rect.right < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image_cano_top, self.top_rect)
        surface.blit(self.image_cano, self.bottom_rect)

# ---------------------------------------------------------------------------------

manager = TelaManager()
RUNNING = True

while RUNNING:
    CLOCK.tick(FPS)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            RUNNING = False

    manager.current.handle_events(events)
    manager.current.update()
    manager.current.draw(TEL)

    pygame.display.update()

pygame.quit()
