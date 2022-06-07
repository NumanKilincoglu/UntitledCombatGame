import webbrowser
import pygame, sys, AlternativeButton

from Button import Button
import mysql.connector

pygame.init()
Screen = pygame.display.set_mode((1280, 720))
bachground_height = 550
panel_height = 450
GRAVITY = 0.69
login_background = pygame.image.load("assets/Backgrounds/girisekran4.jpg").convert_alpha()
scores_background = pygame.image.load("assets/Backgrounds/scoreboard.png").convert_alpha()
back_ground = pygame.image.load("assets/Backgrounds/menu.jpg").convert_alpha()
panel = pygame.image.load("assets/Backgrounds/panel.png").convert_alpha()
select_screen_image = pygame.image.load('assets/Backgrounds/selectscreen.png').convert_alpha()
select_screen_backgound_image = pygame.image.load('assets/Backgrounds/champ_background.jpeg').convert_alpha()
start_image = pygame.image.load('assets/kilinclar.png').convert_alpha()
ok_img = pygame.image.load('assets/Backgrounds/ok.png').convert_alpha()
mali_image = pygame.image.load('assets/Characters/HeroKnight/Idle/0.png').convert_alpha()
bandit_image = pygame.image.load('assets/Characters/bandit/Idle/0.png').convert_alpha()
numan_image = pygame.image.load('assets/Characters/Light Bandit/Idle/0.png').convert_alpha()
start_image = pygame.transform.scale(start_image, (int(start_image.get_width() * 5), int(start_image.get_height() * 5)))
start_button = AlternativeButton.MaliButton(567, 50, start_image, 0.5)
char_scale = 2
hitboxes = []
health_list = []
attack_player = None
first_player_name = ''
second_player_name = ''

winner = 0

player1_point = 0
player2_point = 0

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


def max_id():
    conn = mysql.connector.connect(user=, password='', host=, database=)
    cursor = conn.cursor()
    cursor.execute("select max(Id) from players")
    id = cursor.fetchone()[0]
    conn.close()
    return id


def update_point(first_player_name, second_player_name, player1_point, player2_point, winner):
    if first_player_name is not None and player1_point is not None and second_player_name is not None and player2_point is not None:
        conn = mysql.connector.connect(user=, password='', host=, database=)
        mycursor = conn.cursor()
        point1 = get_point(first_player_name)
        point2 = get_point(second_player_name)

        if winner == 1:
            point1 += 10
        if winner == 2:
            point2 += 10

        sql1 = "UPDATE players SET point = %s WHERE name = %s"
        val = (point1, first_player_name)
        val2 = (point2, second_player_name)
        mycursor.execute(sql1, val)
        mycursor.execute(sql1, val2)
        conn.commit()
        conn.close()


def insert_db(name, char_name):
    if fetchUserDb(name) == False:
        id = max_id()
        id += 1
        conn = mysql.connector.connect(user=, password='', host='', database='')
        cursor = conn.cursor()
        sql = """INSERT INTO players(id, name, character_name,point)VALUES (%s, %s, %s, %s)"""
        record = (id, name, char_name, 0)
        cursor.execute(sql, record)
        conn.commit()
        conn.close()


def get_point(player_name):
    conn = mysql.connector.connect(user='', password='', host='', database='')
    cursor = conn.cursor()
    sql1 = ("select point from players WHERE name = %s")
    val = player_name
    cursor.execute(sql1, (val,))
    point = cursor.fetchone()[0]
    conn.close()
    return point


def fetchUserDb(name):
    query = ("SELECT id,name FROM players WHERE name='" + name + "'")
    connection = mysql.connector.connect(user='', password='', host='', database='')
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchone()

    if results is not None:
        return True
    else:
        return False


class Leaderboard(pygame.font.Font):
    font = None
    scores = None

    def __init__(self):
        self.scores = None
        self.score = 0
        self.font = getfont(40)

    def getScores(self):
        conn = mysql.connector.connect(user='', password='', host='', database='')
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM players")
        self.scores = mycursor.fetchall()

    def draw(self):
        padding_y = 0
        max_scores = 8
        nbr_scores = 1
        for score in self.scores:
            if nbr_scores <= max_scores:
                Screen.blit(self.font.render("  " + str(score[1]) + "                            " + str(score[3]), 1,
                                             (0, 0, 0)), (350, 190 + padding_y))
                padding_y += 65
                nbr_scores += 1


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:

                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def champ_button(image, x, y):
    return AlternativeButton.MaliButton(x, y, image, char_scale)


class Champ():

    def __init__(self, name, image, scale, selected):
        self.image = image
        self.name = name
        self.x = image.get_width()
        self.y = image.get_height()
        self.scale = scale
        self.selected = selected

    def draw(self):
        Screen.blit(self.image, ((Screen.get_width() - self.x) / 2, (Screen.get_height() - self.y) / 2))


mali_button_image = pygame.transform.scale(mali_image, (int(mali_image.get_width()),
                                                        int(mali_image.get_height())))
bandit_button_image = pygame.transform.scale(bandit_image, (int((bandit_image.get_width() * 2.3) / 2),
                                                            int((bandit_image.get_height() * 2.3) / 2)))
numan_button_image = pygame.transform.scale(numan_image, (int((numan_image.get_width() * 2.3) / 2),
                                                          int((numan_image.get_height() * 2.3) / 2)))
mali_button = champ_button(mali_button_image, 321, 375)
bandit_button = champ_button(bandit_button_image, 595, 380)
numan_button = champ_button(numan_button_image, 837, 378)
mali_image = pygame.transform.scale(mali_image, (int((mali_image.get_width() * 4) / 2),
                                                 int((mali_image.get_height() * 4) / 2)))
bandit_image = pygame.transform.scale(bandit_image, (int((bandit_image.get_width() * 9) / 2),
                                                     int((bandit_image.get_height() * 3.55) / 2)))
numan_image = pygame.transform.scale(numan_image, (int((numan_image.get_width() * 9) / 2),
                                                   int((numan_image.get_height() * 3.55) / 2)))
mali = Champ('HeroKnight', mali_image, char_scale, False)
bandit = Champ('bandit', bandit_image, char_scale, False)
numan = Champ('Light Bandit', numan_image, char_scale, False)
champ_list = [mali, bandit, numan]

panel = pygame.transform.scale(panel, (1280, panel_height))
scale = 3

pygame.display.set_caption('Game!')

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define player action variables
moving_left = False
moving_right = False

# define colours
BG = (144, 201, 120)


class HealthBar():
    def __init__(self, max_hp, player_health, x, y):
        self.posX = x
        self.posY = y
        self.player_health = player_health
        self.max_hp = max_hp

    def draw_health_bar(self, player_health):
        self.current_hp = player_health
        self.healthBarRed = (self.posX, self.posY, self.max_hp * 3, 60)
        self.healthBarGreen = (self.posX, self.posY, self.current_hp * 3, 60)
        pygame.draw.rect(Screen, (255, 0, 0), self.healthBarRed)
        pygame.draw.rect(Screen, (0, 255, 0), self.healthBarGreen)


class Character(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.posX = x
        self.posY = y
        self.air = True
        self.attack = False
        self.attack_range = pygame.Rect(0, 0, 0, 0)
        self.velocity_y = 0
        self.jump = False
        self.alive = True
        self.action = 0  # atack 3
        self.direction = 1
        self.flip = False
        self.animationList = []
        self.animation_index = 0
        self.animation_update_time = pygame.time.get_ticks()
        self.attacking1 = False
        self.attacking2 = False
        self.player_health = 100
        temp_animation_list = []

        for i in range(8):
            img = pygame.image.load(f'assets/Characters/{self.char_type}/Idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_animation_list.append(img)
        self.animationList.append(temp_animation_list)
        temp_animation_list = []
        for i in range(4):
            img = pygame.image.load(f'assets/Characters/{self.char_type}/Run/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_animation_list.append(img)
        self.animationList.append(temp_animation_list)
        temp_animation_list = []
        for i in range(1):
            img = pygame.image.load(f'assets/Characters/{self.char_type}/Jump/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_animation_list.append(img)
        self.animationList.append(temp_animation_list)
        temp_animation_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/Characters/{self.char_type}/Attack/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_animation_list.append(img)
        self.animationList.append(temp_animation_list)
        self.image = self.animationList[self.action][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hitbox = (self.posX / 2, self.posY / 2, 128, 128)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            self.action = 1

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
            self.action = 1

        if self.air == False and self.jump == True:
            self.velocity_y = -10
            self.jump = False
            self.air = True

        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y

        if self.rect.bottom + dy > 460:
            dy = 460 - self.rect.bottom
            self.air = False
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.x <= 40 - self.image.get_width() / 2:
            self.rect.x = 40 - self.image.get_width() / 2
        if self.rect.x > 1245 - self.image.get_width() / 2:
            self.rect.x = 1245 - self.image.get_width() / 2

    def update_animations(self):
        delay = 100
        # update image depending on current frame
        self.image = self.animationList[self.action][self.animation_index]
        if self.action == 3:
            if pygame.time.get_ticks() - self.animation_update_time > delay:
                self.animation_update_time = pygame.time.get_ticks()
                self.animation_index += 1
                if self.animation_index == 7:
                    self.attack = False
                    self.action = 0
        else:

            if pygame.time.get_ticks() - self.animation_update_time > delay:
                self.animation_update_time = pygame.time.get_ticks()
                self.animation_index += 1

            if self.animation_index >= len(self.animationList[self.action]):
                self.animation_index = 0

    def attackFunc(self):  # hitboxes
        liste = [item for item in hitboxes]
        x1 = liste[0][0]
        w1 = liste[0][2]
        x2 = liste[1][0]
        w2 = liste[1][2]

        if self.animation_index == 6:
            if self.attacking1:
                if self.direction == 1:  # saga vurus
                    self.attack_range = pygame.Rect(self.rect.x + self.rect.width - 95, self.rect.centery - 60, 95, 128)
                    if (self.attack_range.x + self.attack_range.width >= x2) and (
                            self.attack_range.x + self.attack_range.width <= x2 + w2) or (
                            self.attack_range.x >= x2) and (
                            self.attack_range.x <= x2 + w2):
                        health_list[1] -= 10

                if self.direction == -1:
                    self.attack_range = pygame.Rect(self.rect.x, self.rect.centery - 60, 95, 128)
                    if (self.attack_range.x >= x2) and (self.attack_range.x <= x2 + w2) or (
                            self.attack_range.x + self.attack_range.w >= x2) and (
                            self.attack_range.x + self.attack_range.w <= x2 + w2):
                        health_list[1] -= 10

            self.attacking1 = False
            if self.attacking2:
                if self.direction == 1:  # saga vurus
                    self.attack_range = pygame.Rect(self.rect.x + self.rect.width - 95, self.rect.centery - 60, 95, 128)
                    if (self.attack_range.x + self.attack_range.width >= x1) and (
                            self.attack_range.x + self.attack_range.width <= x1 + w1) or (
                            self.attack_range.x >= x1) and (
                            self.attack_range.x <= x1 + w1):
                        health_list[0] -= 10

                if self.direction == -1:  # sola vurus
                    self.attack_range = pygame.Rect(self.rect.x, self.rect.centery - 60, 95, 128)
                    if (self.attack_range.x >= x1) and (self.attack_range.x <= x1 + w1) or (
                            self.attack_range.x + self.attack_range.w >= x1) and (
                            self.attack_range.x + self.attack_range.w <= x1 + w1):
                        health_list[0] -= 10

            self.attacking2 = False

    def check_action(self, n_action):
        if n_action != self.action:
            self.action = n_action
            self.animation_index = 0
            self.animation_update_time = pygame.time.get_ticks()

    def draw(self):
        self.hitbox = (self.rect.centerx - 55, self.rect.centery - 60, 95, 128)
        Screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


def drawBackGround():
    back_ground = pygame.image.load("assets/Backgrounds/background1.png")
    back_ground = pygame.transform.scale(back_ground, (1280, 550))
    Screen.blit(back_ground, ((0, 0)))


def drawPanel():
    Screen.blit(panel, (0, bachground_height))


def getfont(size):
    return pygame.font.Font("assets/fonts/pixelart.ttf", size)


def main_menu(first_player_name, second_player_name):

    pygame.mixer.music.load("Musics/selectscreen.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)
    play_button = Button(image=pygame.image.load("assets/Buttons/PlayRect.png"), pos=(640, 250), text_input="PLAY",
                         font=getfont(75), base_color="#d7fcd4", hovering_color="White")
    leaderboard_button = Button(image=pygame.image.load("assets/Buttons/Options Rect.png"), pos=(640, 400),
                                text_input="Leader Board", font=getfont(65), base_color="#d7fcd4",
                                hovering_color="White")

    quit_button = Button(image=pygame.image.load("assets/Buttons/QuitRect.png"), pos=(640, 550), text_input="QUIT",
                         font=getfont(75), base_color="#d7fcd4", hovering_color="White")
    github_image = pygame.image.load("assets/Icons/github-sign.png")
    github_image = pygame.transform.scale(github_image, (45, 45))
    github_button = Button(image=github_image, pos=(75, 650), text_input="", font=getfont(10), base_color="#d7fcd4",
                           hovering_color="White")
    linkedin_image = pygame.image.load("assets/Icons/linkedin.png")
    linkedin_image = pygame.transform.scale(linkedin_image, (45, 45))
    linkedintButton = Button(image=linkedin_image, pos=(140, 650), text_input="", font=getfont(10),
                             base_color="#d7fcd4",
                             hovering_color="White")
    not_mute_img = pygame.image.load("assets/Icons/notmuted.png")
    not_mute_img = pygame.transform.scale(not_mute_img, (50, 50))
    mute_img = pygame.image.load("assets/Icons/muted.png")
    mute_image = pygame.transform.scale(mute_img, (50, 50))
    muteButton = Button(image=not_mute_img, pos=(50, 80), text_input="", font=getfont(10),
                        base_color="#d7fcd4",
                        hovering_color="White")
    while True:
        Screen.blit(back_ground, ((0, 0)))
        pygame.display.set_caption("Main Menu")

        menu_text = getfont(100).render("Main Menu", True, "#000000")
        menu_rect = menu_text.get_rect(center=(640, 100))

        Screen.blit(menu_text, menu_rect)
        button_list = [play_button, leaderboard_button, quit_button, github_button, linkedintButton, muteButton]

        menu_mouse_position = pygame.mouse.get_pos()

        for button in button_list:
            button.changeColor(menu_mouse_position)
            button.update(Screen)

        for event in pygame.event.get():
            menu_mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_position):
                    select_screen(first_player_name, second_player_name)

                if leaderboard_button.checkForInput(menu_mouse_position):
                    leaderBoard()

                if github_button.checkForInput(menu_mouse_position):
                    webbrowser.open("https://github.com/NumanKilincoglu")
                    webbrowser.open("https://github.com/MuhammedAliGulcemal")

                if linkedintButton.checkForInput(menu_mouse_position):
                    webbrowser.open("https://www.linkedin.com/in/muhammed-ali-g%C3%BClcemal-b0507721b")
                    webbrowser.open("https://www.linkedin.com/in/numankilincoglu")

                if muteButton.checkForInput(menu_mouse_position):
                    if muteButton.musicOn:
                        pygame.mixer.music.unpause()
                        muteButton.updateImage(not_mute_img, Screen)
                        muteButton.musicOn = False
                    else:
                        pygame.mixer.music.pause()
                        muteButton.updateImage(mute_image, Screen)
                        muteButton.musicOn = True

                if quit_button.checkForInput(menu_mouse_position):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


champ_name1 = ''
champ_name2 = ''


def select_screen(first_player_name, second_player_name):

    counter = 0
    temp = -1
    champ1 = None
    champ2 = None
    first = None
    second = None
    run = True
    while run:
        clock.tick(FPS)
        Screen.blit(select_screen_backgound_image, (0, 0))
        Screen.blit(select_screen_image, (0, 0))
        if mali_button.draw(Screen):
            pygame.mixer.music.load("Musics/sovalye.mp3")
            pygame.mixer.music.play()
            mali.selected = True
            bandit.selected = False
            numan.selected = False
            temp = 0
        if bandit_button.draw(Screen):
            pygame.mixer.music.load("Musics/haydut.mp3")
            pygame.mixer.music.play()
            mali.selected = False
            bandit.selected = True
            numan.selected = False
            temp = 1
        if numan_button.draw(Screen):
            pygame.mixer.music.load("Musics/eskiya.mp3")
            pygame.mixer.music.play()
            mali.selected = False
            bandit.selected = False
            numan.selected = True
            temp = 2

        for champ in champ_list:
            if counter == 0:
                if champ.selected:
                    champ1 = Character(champ.name, 264 - champ.image.get_width() / 2,
                                       345 - champ.image.get_height() / 2, 3, 5)
                    champ_name1 = champ.name
                    champ.selected = False
            elif counter == 1:
                if champ.selected:
                    champ2 = Character(champ.name, 1220 - champ.image.get_width() / 2,
                                       345 - champ.image.get_height() / 2, 3, 5)
                    champ_name2 = champ.name
                    champ2.flip = True
                    champ.selected = False
        if champ1 is not None:
            champ1.update_animations()
            champ1.draw()
            champ1.check_action(0)
        if champ2 is not None:
            champ2.update_animations()
            champ2.draw()
            champ2.check_action(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if start_button.draw(Screen):
            if temp != -1:
                counter += 1
                if counter == 1:
                    if temp == 0:
                        first = Character('HeroKnight', 110, 390, 3, 5)
                    elif temp == 1:
                        first = Character('bandit', 110, 380, 3, 5)
                    elif temp == 2:
                        first = Character('Light Bandit', 110, 380, 3, 5)
                    temp = -1
                if counter == 2:
                    if temp == 0:
                        second = Character('HeroKnight', 1170, 390, 3, 5)
                    elif temp == 1:
                        second = Character('bandit', 1170, 380, 3, 5)
                    elif temp == 2:
                        second = Character('Light Bandit', 1170, 380, 3, 5)
                    if first is not None and second is not None:
                        insert_db(first_player_name, champ_name1)
                        insert_db(second_player_name, champ_name2)
                        play(False, False, False, False, first, second, first_player_name, second_player_name)
                        run = False

        pygame.display.update()


def movement(player, moving_right, moving_left):
    if player.alive:
        if player.air:
            player.attack = False
            player.check_action(2)
        elif moving_right or moving_left:
            player.attack = False
            player.check_action(1)
        elif player.attack:
            player.check_action(3)
            player.attackFunc()
        else:
            player.attack = False
            player.check_action(0)
        player.move(moving_left, moving_right)


def updateHitboxArray(first_player, second_player):
    hitboxes.clear()
    hitboxes.append(first_player.hitbox)
    hitboxes.append(second_player.hitbox)


def win_screen(winner, name):
    return_menu_button = Button(image=ok_img, pos=(100, 80), text_input="", font=getfont(10),
                                base_color="#d7fcd4",
                                hovering_color="White")
    quit_button = Button(image=pygame.image.load("assets/Buttons/QuitRect.png"), pos=(640, 600), text_input="QUIT",
                         font=getfont(75), base_color="#d7fcd4", hovering_color="White")
    run = True
    while run:
        clock.tick(FPS)
        Screen.fill((156, 103, 200))
        winner_txt = getfont(50).render(name + ' WINS!', True, "#000000")
        Screen.blit(winner_txt, (int((Screen.get_width() - winner_txt.get_width()) / 2),
                                 int((Screen.get_height() - winner.get_height()) / 2) - 50))
        Screen.blit(winner, (
            int((Screen.get_width() - winner.get_width()) / 2), int((Screen.get_height() - winner.get_height()) / 2)))
        pygame.display.set_caption("Winner")
        menu_mouse_position = pygame.mouse.get_pos()
        button_list = [return_menu_button, quit_button]
        for button in button_list:
            button.changeColor(menu_mouse_position)
            button.update(Screen)

        for event in pygame.event.get():
            menu_mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_menu_button.checkForInput(menu_mouse_position):
                    main_menu(first_player_name, second_player_name)
                if quit_button.checkForInput(menu_mouse_position):
                    sys.exit(0)

            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


def play(fp_moving_left, fp_moving_right, sp_moving_left, sp_moving_right, first_player, second_player,
         first_player_name, second_player_name):
    pygame.mixer.music.load("Musics/ingame.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    health_list.append(first_player.player_health)
    health_list.append(second_player.player_health)
    second_player.flip = True
    hitboxes.append(first_player.hitbox)
    hitboxes.append(second_player.hitbox)
    health_list[0] = 100
    health_list[1] = 100
    p1_health_bar = HealthBar(max_hp=100, player_health=health_list[0], x=150, y=600)
    p2_health_bar = HealthBar(max_hp=100, player_health=health_list[1], x=850, y=600)

    run = True
    while run:

        clock.tick(FPS)
        drawBackGround()
        drawPanel()
        pygame.display.set_caption("Let's Play")
        first_player.update_animations()
        first_player.draw()
        second_player.update_animations()
        second_player.draw()
        movement(first_player, fp_moving_right, fp_moving_left)
        movement(second_player, sp_moving_right, sp_moving_left)
        updateHitboxArray(first_player, second_player)
        p1_health_bar.draw_health_bar(health_list[0])
        p2_health_bar.draw_health_bar(health_list[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sp_moving_left = True
                if event.key == pygame.K_RIGHT:
                    sp_moving_right = True
                if second_player.alive and event.key == pygame.K_UP:
                    pygame.mixer.music.load("Musics/ziplama.mp3")
                    pygame.mixer.music.play()
                    second_player.jump = True
                if event.key == pygame.K_a:
                    fp_moving_left = True
                if event.key == pygame.K_d:
                    fp_moving_right = True
                if first_player.alive and event.key == pygame.K_w:
                    pygame.mixer.music.load("Musics/ziplama.mp3")
                    pygame.mixer.music.play()
                    first_player.jump = True
                if first_player.alive and event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("Musics/saldiri.mp3")
                    pygame.mixer.music.play()
                    first_player.attack = True
                    first_player.attacking1 = True
                if second_player.alive and event.key == pygame.K_k:
                    pygame.mixer.music.load("Musics/saldiri.mp3")
                    pygame.mixer.music.play()
                    second_player.attack = True
                    second_player.attacking2 = True
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    fp_moving_left = False
                if event.key == pygame.K_d:
                    fp_moving_right = False
                if event.key == pygame.K_LEFT:
                    sp_moving_left = False
                if event.key == pygame.K_RIGHT:
                    sp_moving_right = False

        if health_list[0] == 0 or health_list[1] == 0:
            if health_list[0] == 0:
                player2_point = 10
                player1_point = 0
                winner = 2
                update_point(first_player_name, second_player_name, player1_point, player2_point, winner)
                win_screen(second_player.image, second_player_name)
                run = False
            elif health_list[1] == 0:
                player2_point = 10
                player1_point = 0
                winner = 1
                update_point(first_player_name, second_player_name, player1_point, player2_point, winner)
                win_screen(first_player.image, first_player_name)
                run = False

        pygame.display.update()


def showLeaderBoard():
    board = Leaderboard()
    Screen.blit(scores_background, (0, 0))
    board.getScores()
    board.draw()
    pygame.display.update()


def leaderBoard():
    run = True
    while run:
        pygame.display.set_caption("Main Menu")
        showLeaderBoard()
        back_button1 = AlternativeButton.MaliButton(32, 16, ok_img, 1)

        if back_button1.draw(Screen):
            main_menu(first_player_name, second_player_name)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def login():
    clock = pygame.time.Clock()
    input_box1 = InputBox(175, 150, 100, 32)
    input_box2 = InputBox(900, 150, 100, 32)
    input_boxes = [input_box1, input_box2]
    done = False
    Screen.blit(login_background, (0, 0))
    play_button = Button(image=pygame.image.load("assets/Buttons/PlayRect.png"), pos=(640, 500), text_input="PLAY",
                         font=getfont(75), base_color="#d7fcd4", hovering_color="White")
    while not done:

        my_font = getfont(40)
        player1 = my_font.render("First Player!", True, (53, 75, 39))
        Screen.blit(player1, (100, 50))

        player2 = my_font.render("Second Player!", True, (53, 75, 39))
        Screen.blit(player2, (800, 50))

        button_list = [play_button]

        for event in pygame.event.get():
            for box in input_boxes:
                box.handle_event(event)

            first_player_name = input_box1.text
            second_player_name = input_box2.text
            menu_mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and first_player_name != "" and second_player_name != "":

                if play_button.checkForInput(menu_mouse_position):
                    main_menu(first_player_name, second_player_name)

        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(Screen)

        menu_mouse_position = pygame.mouse.get_pos()
        for button in button_list:
            button.changeColor(menu_mouse_position)
            button.update(Screen)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(30)


login()
