import pygame
import sys


FPS = 50
pygame.init()
WIDTH = 500
HEIGHT = 500
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
def load_image(name, colorkey=None):
    fullname = f'data\\{name}'
    image = pygame.image.load(fullname).convert_alpha()
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def types(self):
        return self.type


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, j, positions):
        if j == 1:
            if sum([1 for i in positions if self.rect.y - tile_height in range(i[1], i[1] + tile_height) and self.rect.x in range(i[0], i[0] + tile_width)]) == 0:
                self.rect.y -= tile_height
        elif j == 2:
            if sum([1 for i in positions if self.rect.y + tile_height in range(i[1], i[1] + tile_height) and self.rect.x in range(i[0], i[0] + tile_width)]) == 0:
                self.rect.y += tile_height
        elif j == 3:
            if sum([1 for i in positions if self.rect.y in range(i[1], i[1] + tile_height) and self.rect.x - tile_width in range(i[0], i[0] + tile_width)]) == 0:
                self.rect.x -= tile_width
        elif j == 4:
            if sum([1 for i in positions if self.rect.y in range(i[1], i[1] + tile_height) and self.rect.x + tile_width in range(i[0], i[0] + tile_width)]) == 0:
                self.rect.x += tile_width


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


# основной персонаж
player = None
camera = Camera()
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клеткахs
    return new_player, x, y
for i in sys.argv:
    if '.txt' in i:
        player, level_x, level_y = generate_level(load_level(i))
start_screen()
last_w = 0
last_s = 0
last_a = 0
last_d = 0
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
    screen.fill(BLACK)
    for i in tiles_group:
        screen.blit(i.image, i.rect)
    screen.blit(player.image, player.rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        last_w = 1
    else:
        if last_w:
            last_w = 0
            player.move(1, [(i.rect.x, i.rect.y) for i in tiles_group if i.types() == 'wall'])
    if keys[pygame.K_s]:
        last_s = 1
    else:
        if last_s:
            last_s = 0
            player.move(2, [(i.rect.x, i.rect.y) for i in tiles_group if i.types() == 'wall'])
    if keys[pygame.K_a]:
        last_a = 1
    else:
        if last_a:
            last_a = 0
            player.move(3, [(i.rect.x, i.rect.y) for i in tiles_group if i.types() == 'wall'])
    if keys[pygame.K_d]:
        last_d = 1
    else:
        if last_d:
            last_d = 0
            player.move(4, [(i.rect.x, i.rect.y) for i in tiles_group if i.types() == 'wall'])
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    for sprite in tiles_group:
        if sprite.rect.x not in range(int(player.rect.x - WIDTH / 2), int(player.rect.x + WIDTH / 2)):
            if sprite.rect.x < player.rect.x:
                sprite.rect.x += WIDTH
            elif sprite.rect.x > player.rect.x:
                sprite.rect.x -= WIDTH
        if sprite.rect.y not in range(int(player.rect.y - HEIGHT / 2), int(player.rect.y + HEIGHT / 2)):
            if sprite.rect.y < player.rect.y:
                sprite.rect.y += HEIGHT
            elif sprite.rect.y > player.rect.y:
                sprite.rect.y -= HEIGHT
        for sprite2 in tiles_group:
            if sprite2.rect.x == sprite.rect.x and sprite2.rect.y == sprite.rect.y and not sprite is sprite2:
                tiles_group.remove(sprite2)

    pygame.display.flip()