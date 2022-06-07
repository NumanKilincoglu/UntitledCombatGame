import pygame, sys

from Button import Button


pygame.init()

Screen = pygame.display.set_mode((1280, 720))
back_ground = pygame.image.load("assets/Backgrounds/menu.jpg")


def getfont(size):
    return pygame.font.Font("assets/fonts/pixelart.ttf", size)

def play():
    while True:
        Screen.blit(back_ground, ((0, 0)))
        pygame.display.set_caption("Main Menu")

        # print(menu_mouse_position)
        menu_text = getfont(100).render("Main Menu", True, "#000000")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load("assets/Buttons/PlayRect.png"), pos=(640, 250), text_input="PLAY",
                             font=getfont(75), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=pygame.image.load("assets/Buttons/OptionsRect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=getfont(75), base_color="#d7fcd4", hovering_color="White")
        # leader_board_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),text_input="QUIT", font=getfont(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Buttons/QuitRect.png"), pos=(640, 550), text_input="QUIT",
                             font=getfont(75), base_color="#d7fcd4", hovering_color="White")

        Screen.blit(menu_text, menu_rect)
        button_list = [play_button, options_button, quit_button]

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
                    play()
                if options_button.checkForInput(menu_mouse_position):
                    print('opts')
                if quit_button.checkForInput(menu_mouse_position):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()