from pygame import *

# Инициализация и настройки экрана
window = display.set_mode((1280, 720))
display.set_caption('p')
# Предположим, что изображения существуют, иначе будет ошибка
try:
    background = transform.scale(image.load('blackspace.png'), (1280, 720))
    platforma = transform.scale(image.load('platforma.png'), (1280, 360))
    enemy_img = image.load('enemy_vampire.png')
    toxic_left_img = image.load('toxic lime_left.png')
    toxic_right_img = image.load('toxic lime_right.png')
except FileNotFoundError:
    print("Ошибка: Не найдены изображения! Убедитесь, что файлы лежат в той же папке.")
    exit()

game_started = False
# Флаг, чтобы не создавать переменные вне класса, лучше инкапсулировать, но оставим для совместимости со старым стилем
# Используем переменную класса или просто локальную в методе update, если нужно. 
# Для простоты оставим глобальную, но будем с ней осторожны.

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, x, y, sx, sy):
        super().__init__()
        self.image = transform.scale(pl_image, (sx, sy))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Физические параметры
        self.jump_power = -15  # Сила прыжка (отрицательная = вверх)
        self.speed_y = 0
        self.speed_x = 5
        self.gravity = 0.5
        self.is_jumping = False # Для предотвращения двойного прыжка

    def show(self):
        window.blit(self.image, self.rect.topleft)

class Player(GameSprite):
    def update(self):
        global game_started
        
        # 1. Движение влево/вправо
        keys = key.get_pressed()
        if keys[K_RIGHT]:
            self.rect.x += self.speed_x
        if keys[K_LEFT]:
            self.rect.x -= self.speed_x
            
        # Ограничение по краям экрана
        if self.rect.x < 0: self.rect.x = 0
        if self.rect.x + self.rect.width > 1280: self.rect.x = 1280 - self.rect.width

        # 2. Применяем гравитацию и движение по Y
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
        
        # 3. Проверка столкновения с платформой (землей)
        # Платформа находится сверху y=360, значит персонаж стоит на ней, если его низ касается верха платформы
        # rect.bottom == 360
        if self.rect.bottom >= 360:
            self.rect.bottom = 360
            self.speed_y = 0
            self.is_jumping = False # Разрешаем прыжок снова

        # 4. Обработка событий прыжка
        # Важно: прыжок должен срабатывать при НАЖАТИИ, а не при УДЕРЖАНИИ.
        # Для этого используем event.get() в основном цикле или флаг.
        
class Toxic_Lime_Left(GameSprite):
    def move(self):
        self.rect.y += 1.5
        if self.rect.y > 695:
            self.rect.y = 513
            self.rect.x = 264

class Toxic_Lime_Right(GameSprite):  
    def move(self):
        self.rect.y += 1.5
        if self.rect.y > 695:
            self.rect.y = 513
            self.rect.x = 991

# Создаем спрайты
player = Player(enemy_img, 5, 295, 65, 65)
toxic_lime_left = Toxic_Lime_Left(toxic_left_img, 264, 513, 25, 25)           
toxic_lime_right = Toxic_Lime_Right(toxic_right_img, 991, 513, 25, 25)  

clock = time.Clock() 
FPS = 60

game = True
while game:
    # Обработка событий (включая прыжок)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # Прыгаем, если игрок на земле
                if player.rect.bottom >= 360:
                    player.speed_y = player.jump_power
                    player.is_jumping = True
                # Запуск игры, если она не началась
                if not game_started:
                    game_started = True

    # Отрисовка
    window.blit(background, (0, 0))
    window.blit(platforma, (0, 360))
    
    # Обновление позиций
    player.update()
    toxic_lime_left.move()
    toxic_lime_right.move() 
    
    # Отрисовка спрайтов
    player.show()
    toxic_lime_left.show()
    toxic_lime_right.show()
    
    display.update()
    clock.tick(FPS)