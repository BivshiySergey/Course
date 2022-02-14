import os
import random

import easygui
import pygame
import time

import config
import multiplayer
import singleplayer
import sounds
import tower
from tank import Tank


class Game:
    def __init__(self):
        self.mainmenu_Title = 'Super Chess Championships Action Tank Fighting'

        self.WIDTH = 1280
        self.HEIGHT = 500
        self.FPS = 15

        pygame.init()
        pygame.mixer.init()
        self.sounds = sounds.Sounds()
        auth = config.AUTH
        self.connect = multiplayer.Connection(auth)

        self.screen = pygame.display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("S C C A T F")
        pygame.display.set_icon(pygame.transform.scale(pygame.image.load(os.path.join("images", "player_tower.png")), (50, 50)))
        self.SETTINGS_ICON = pygame.transform.scale(pygame.image.load(os.path.join("images", "settings.png")), (50, 50))
        self.SETTINGS_RECT = self.SETTINGS_ICON.get_rect(topleft=(self.WIDTH - 70, 20))
        self.BACK_ICON = pygame.transform.scale(pygame.image.load(os.path.join("images", "arrow_back.png")), (50, 50))
        self.BACK_RECT = self.BACK_ICON.get_rect(bottomleft=(self.WIDTH - 70, self.HEIGHT - 20))

        self.clock = pygame.time.Clock()

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.backgroundCOLOR = self.WHITE

        self.MAIN_CYCLE = True
        self.MAIN_MENU = True
        self.SINGLE_GAME_ON = False
        self.SETTINGS_MENU = False
        self.MULTIPLAYER = False
        self.MULTIPLAYER_MENU = False
        self.CONNECTING = False

        self.chosen_tank = None
        self.player_turn = True
        self.GAME_STATUS = "START"
        self.battlefield = []
        self.moves = []
        self.first_tick = 0

    def game_reboot(self):
        if self.connect.lobby_id is not None:
            self.connect.delete_lobby()
        self.connect = multiplayer.Connection(self.connect.get_auth())
        self.MAIN_CYCLE = True
        self.MAIN_MENU = True
        self.SINGLE_GAME_ON = False
        self.SETTINGS_MENU = False
        self.MULTIPLAYER = False
        self.MULTIPLAYER_MENU = False
        self.CONNECTING = False

        self.chosen_tank = None
        self.player_turn = True
        self.GAME_STATUS = "START"
        self.battlefield = []
        self.moves = []
        self.first_tick = 0

    def main_cycle(self):
        while self.MAIN_CYCLE:
            self.WIDTH = self.screen.get_width()
            self.HEIGHT = self.screen.get_height()
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.MAIN_CYCLE = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.backgroundCOLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (0, 0))
                    if self.SETTINGS_RECT.contains(mouse_rect):
                        if self.SETTINGS_MENU:
                            self.SETTINGS_MENU = False
                        else:
                            self.SETTINGS_MENU = True
                    if self.BACK_RECT.contains(mouse_rect):
                        self.game_reboot()

            self.screen.fill(self.backgroundCOLOR)
            self.screen.blit(self.SETTINGS_ICON, self.SETTINGS_RECT)
            self.screen.blit(self.BACK_ICON, self.BACK_RECT)
            if self.SETTINGS_MENU:
                self.settings_Cycle()
            elif self.MAIN_MENU:
                self.mainmenu_Cycle()
            elif self.SINGLE_GAME_ON:
                self.singleGame_Cycle()
            elif self.MULTIPLAYER:
                self.multiplayer_Game_Cycle()
            self.clock.tick(self.FPS)

    def mainmenu_Cycle(self):
        if self.MAIN_MENU:
            # title
            f = pygame.font.SysFont('arial', 48)
            titletext_surf = f.render(self.mainmenu_Title, True, self.BLACK, self.WHITE)
            titletext_rect = titletext_surf.get_rect(center=(self.WIDTH // 2, 120))
            self.screen.blit(titletext_surf, titletext_rect)
            # main menu text
            f = pygame.font.SysFont('arial', 24)
            single_text = f.render('Одиночная игра', True, self.BLACK, self.WHITE)
            single_position = single_text.get_rect(center=(self.WIDTH // 2, 200))
            self.screen.blit(single_text, single_position)
            multi_text = f.render('Мультиплеер', True, self.BLACK, self.WHITE)
            multi_position = multi_text.get_rect(center=(self.WIDTH // 2, 240))
            self.screen.blit(multi_text, multi_position)
            exit_text = f.render('Выход', True, self.BLACK, self.WHITE)
            exit_position = exit_text.get_rect(center=(self.WIDTH // 2, 300))
            self.screen.blit(exit_text, exit_position)
            # main menu settings + questions

            # buttons
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_keys = pygame.mouse.get_pressed()
                    if mouse_keys[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if exit_position.topleft[0] < mouse_pos[0] < exit_position.bottomright[0] and \
                                exit_position.topleft[1] < mouse_pos[1] < exit_position.bottomright[1]:
                            pygame.draw.rect(self.screen, self.BLACK, exit_position, 2)
                            self.MAIN_CYCLE = False
                        elif single_position.topleft[0] < mouse_pos[0] < single_position.bottomright[0] and \
                                single_position.topleft[1] < mouse_pos[1] < single_position.bottomright[1]:
                            pygame.draw.rect(self.screen, self.BLACK, single_position, 2)
                            self.MAIN_MENU = False
                            self.SINGLE_GAME_ON = True
                            self.GAME_STATUS = "START"
                        elif multi_position.topleft[0] < mouse_pos[0] < multi_position.bottomright[0] and \
                                multi_position.topleft[1] < mouse_pos[1] < multi_position.bottomright[1]:
                            pygame.draw.rect(self.screen, self.BLACK, multi_position, 2)
                            self.MAIN_MENU = False
                            self.MULTIPLAYER = True
                            self.MULTIPLAYER_MENU = True
        pygame.display.update()

    def singleGame_Cycle(self):
        if self.SINGLE_GAME_ON:
            if self.GAME_STATUS == "START":
                self.battlefield = singleplayer.Game.createBattlefield(self, config.CELL_BODY)
                self.enemy_tanks = [Tank(config.TANK_STATS, (0, 5), surface=config.CELL_BODY, player=False),
                                    Tank(config.TANK_STATS, (0, 4), surface=config.CELL_BODY, player=False)]
                self.player_tanks = [Tank(config.TANK_STATS, (9, 5), surface=config.CELL_BODY),
                                     Tank(config.TANK_STATS, (9, 4), surface=config.CELL_BODY)]
                self.player_towers = [tower.Tower(config.TOWER_STATS, (8, 6), surface=config.CELL_BODY),
                                      tower.Tower(config.TOWER_STATS, (8, 3), surface=config.CELL_BODY)]
                self.enemy_towers = [tower.Tower(config.TOWER_STATS, (1, 6), surface=config.CELL_BODY, player=False),
                                     tower.Tower(config.TOWER_STATS, (1, 3), surface=config.CELL_BODY, player=False)]
                self.GAME_STATUS = "GOES"
            elif self.GAME_STATUS == "GOES":
                if len(self.player_tanks) == 0 or len(self.player_towers) == 0:
                    self.GAME_STATUS = "OVER"
                    self.game_reboot()
                    easygui.msgbox("К сожалению вы проиграли", "Поражение!")
                    self.connect.win()
                elif len(self.enemy_tanks) == 0 or len(self.enemy_towers) == 0:
                    self.GAME_STATUS = "OVER"
                    easygui.msgbox("Поздравляю вы выиграли!", "Победа!")
                    self.game_reboot()
                    print('lose')
                else:
                    singleplayer.Game.create_FOV(self, self.player_tanks, self.player_towers)
                    self.game_visualization()
                    if self.player_turn:
                        mouse_keys = pygame.mouse.get_pressed()
                        if mouse_keys[0]:
                            mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (0, 0))
                            y = 0
                            for line in self.battlefield:
                                x = 0
                                for cell in line:
                                    if cell.get_rect().contains(mouse_rect):
                                        move = (y, x)
                                        chosen_tank = 0
                                        ZeroAP_counter = 0
                                        for tank1 in self.player_tanks:
                                            if tank1.AP < 1:
                                                ZeroAP_counter += 1
                                            if tank1.pos[0] == y and tank1.pos[1] == x:
                                                self.chosen_tank = chosen_tank
                                            chosen_tank += 1
                                        if len(self.player_tanks) == ZeroAP_counter:
                                            self.player_turn = False
                                        if not self.chosen_tank == None:
                                            if singleplayer.Game.tankActions(self, self.player_tanks[self.chosen_tank],
                                                                             move):
                                                print(cell.type, cell.hp)
                                    x += 1
                                y += 1
                    else:
                        singleplayer.Game.tank_Fight(self, self.player_tanks, self.player_towers
                                                     , self.enemy_tanks, self.enemy_towers)
                        for tank1 in self.enemy_tanks:
                            tank1.AP = 2
                            singleplayer.Game.tankAI(self, tank1)
                        self.battlefield = singleplayer.Game.get_battlefield(self)
                        for tank1 in self.player_tanks:
                            tank1.AP = 2
                        self.player_turn = True
                        self.chosen_tank = None

            elif self.GAME_STATUS == "OVER":
                self.SINGLE_GAME_ON = False
                self.MAIN_MENU = True
        pygame.display.update()

    def game_visualization(self):
        self.battlefield = singleplayer.Game.get_battlefield(self)
        start_rect = pygame.Rect(0, 8, 0, 0)
        for line in range(10):
            CELL_IS_VISIBLE = singleplayer.Game.is_visible(self, (line, 0))
            rect = self.battlefield[line][0].get_image().get_rect(topright=(start_rect.bottomright[0],
                                                                            start_rect.bottomright[1] + 2))
            image = self.battlefield[line][0].get_image()
            if not CELL_IS_VISIBLE:
                image = image.copy()
                image.fill((0, 0, 0))
            self.screen.blit(image, rect)
            start_rect = rect
            prev_rect = rect
            for cell in range(10):
                image = self.battlefield[line][cell].get_image()
                CELL_IS_VISIBLE = singleplayer.Game.is_visible(self, (line, cell))
                if not CELL_IS_VISIBLE:
                    image = image.copy()
                    image.fill((0, 0, 0))
                rect = image.get_rect(topleft=(prev_rect.topright[0] + 2, prev_rect.topright[1]))
                self.screen.blit(image, rect)
                self.battlefield[line][cell].set_rect(rect)
                if self.chosen_tank != None:
                    if self.player_tanks[self.chosen_tank].pos[0] == line \
                            and self.player_tanks[self.chosen_tank].pos[1] == cell:
                        pygame.draw.rect(self.screen, self.BLACK, rect, 2)
                prev_rect = rect
                for tower1 in self.player_towers:
                    if tower1.is_Dead():
                        self.player_tanks.remove(tower1)
                    else:
                        if tower1.pos[0] == line and tower1.pos[1] == cell and CELL_IS_VISIBLE:
                            self.screen.blit(tower1.image, rect)
                for tower1 in self.enemy_towers:
                    if tower1.is_Dead():
                        self.player_tanks.remove(tower1)
                    else:
                        if tower1.pos[0] == line and tower1.pos[1] == cell and CELL_IS_VISIBLE:
                            self.screen.blit(tower1.image, rect)
                for tank1 in self.player_tanks:
                    if tank1.is_Dead():
                        self.player_tanks.remove(tank1)
                    else:
                        if tank1.pos[0] == line and tank1.pos[1] == cell and CELL_IS_VISIBLE:
                            self.screen.blit(tank1.image, rect)
                for tank1 in self.enemy_tanks:
                    if tank1.is_Dead():
                        self.enemy_tanks.remove(tank1)
                    else:
                        if tank1.pos[0] == line and tank1.pos[1] == cell and CELL_IS_VISIBLE:
                            self.screen.blit(tank1.image, rect)


    def multiplayer_Game_Cycle(self):
        if self.MULTIPLAYER:
            if self.MULTIPLAYER_MENU:

                f = pygame.font.SysFont('arial', 24)
                host_text = f.render('Создать игру', True, self.BLACK, self.WHITE)
                host_position = host_text.get_rect(center=(self.WIDTH // 2, 220))
                self.screen.blit(host_text, host_position)
                search_text = f.render('Поиск игры', True, self.BLACK, self.WHITE)
                search_position = search_text.get_rect(center=(self.WIDTH // 2, 260))
                self.screen.blit(search_text, search_position)
                reg_text = f.render('Регистрация', True, self.BLACK, self.WHITE)
                reg_position = reg_text.get_rect(center=(self.WIDTH // 2, 300))
                self.screen.blit(reg_text, reg_position)
                auth_text = f.render('Авторизация', True, self.BLACK, self.WHITE)
                auth_position = auth_text.get_rect(center=(self.WIDTH // 2, 340))
                self.screen.blit(auth_text, auth_position)
                for event in self.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_keys = pygame.mouse.get_pressed()
                        if mouse_keys[0]:
                            res = None
                            mouse_pos = pygame.mouse.get_pos()
                            if host_position.topleft[0] < mouse_pos[0] < host_position.bottomright[0] and \
                                    host_position.topleft[1] < mouse_pos[1] < host_position.bottomright[1]:
                                pygame.draw.rect(self.screen, self.BLACK, host_position, 2)
                                self.GAME_STATUS = "HOST"
                                self.MULTIPLAYER_MENU = False
                                self.CONNECTING = True
                            elif search_position.topleft[0] < mouse_pos[0] < search_position.bottomright[0] and \
                                    search_position.topleft[1] < mouse_pos[1] < search_position.bottomright[1]:
                                pygame.draw.rect(self.screen, self.BLACK, search_position, 2)
                                self.GAME_STATUS = "SEARCH"
                                self.MULTIPLAYER_MENU = False
                                self.CONNECTING = True
                            elif reg_position.topleft[0] < mouse_pos[0] < reg_position.bottomright[0] and \
                                    reg_position.topleft[1] < mouse_pos[1] < reg_position.bottomright[1]:
                                pygame.draw.rect(self.screen, self.BLACK, reg_position, 2)
                                input = easygui.multenterbox(title='Регистрация', fields=["Логин", "Пароль"])
                                if input is None:
                                    self.game_reboot()
                                    return
                                res = self.connect.registrtion(input)
                                if isinstance(res, str):
                                    easygui.msgbox(res)
                            elif auth_position.topleft[0] < mouse_pos[0] < auth_position.bottomright[0] and \
                                    auth_position.topleft[1] < mouse_pos[1] < auth_position.bottomright[1]:
                                pygame.draw.rect(self.screen, self.BLACK, auth_position, 2)
                                input = easygui.multenterbox(title='Авторизация', fields=["Логин", "Пароль"])
                                if input is None:
                                    self.game_reboot()
                                    return
                                res = self.connect.authorization(input)
                                if isinstance(res, str):
                                    easygui.msgbox(res)
            elif self.CONNECTING:
                f = pygame.font.SysFont('arial', 24)
                cancel_text = f.render('Отмена', True, self.BLACK, self.WHITE)
                cancel_position = cancel_text.get_rect(center=(self.WIDTH // 2, 340))
                self.screen.blit(cancel_text, cancel_position)
                host_text = f.render('Поиск противника ' + str(round(10 + self.first_tick - time.time())) + "...",
                                     True, self.BLACK, self.WHITE)
                host_position = host_text.get_rect(center=(self.WIDTH // 2, 290))
                self.screen.blit(host_text, host_position)
                for event in self.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_keys = pygame.mouse.get_pressed()
                        if mouse_keys[0]:
                            mouse_pos = pygame.mouse.get_pos()
                            if cancel_position.topleft[0] < mouse_pos[0] < cancel_position.bottomright[0] and \
                                    cancel_position.topleft[1] < mouse_pos[1] < cancel_position.bottomright[1]:
                                pygame.draw.rect(self.screen, self.BLACK, cancel_position, 2)
                                self.game_reboot()
                if self.GAME_STATUS == "HOST":
                    second_tick = time.time()
                    if second_tick - self.first_tick > 10:
                        self.first_tick = time.time()
                        singleplayer.Game.createBattlefield(self, config.CELL_BODY)
                        res = self.connect.set_new_game(singleplayer.Game.get_type_battlefield(self))
                        if isinstance(res, dict):
                            singleplayer.Game.set_battlefield_from_type(self, res["battlefield"], config.CELL_BODY)
                            print(res)
                            self.connect.js = res
                            self.connect.lobby_id = res["id"]
                            self.enemy_tanks = [Tank(config.TANK_STATS, (0, 5), surface=config.CELL_BODY, player=False),
                                                Tank(config.TANK_STATS, (0, 4), surface=config.CELL_BODY, player=False)]
                            self.player_tanks = [Tank(config.TANK_STATS, (9, 5), surface=config.CELL_BODY),
                                                 Tank(config.TANK_STATS, (9, 4), surface=config.CELL_BODY)]
                            self.player_towers = [tower.Tower(config.TOWER_STATS, (8, 6), surface=config.CELL_BODY),
                                                  tower.Tower(config.TOWER_STATS, (8, 3), surface=config.CELL_BODY)]
                            self.enemy_towers = [
                                tower.Tower(config.TOWER_STATS, (1, 6), surface=config.CELL_BODY, player=False),
                                tower.Tower(config.TOWER_STATS, (1, 3), surface=config.CELL_BODY, player=False)]

                            self.GAME_STATUS = "SET"
                            self.CONNECTING = False
                        elif res == 404:
                            self.game_reboot()
                elif self.GAME_STATUS == "SEARCH":
                    second_tick = time.time()
                    if second_tick - self.first_tick > 10:
                        self.first_tick = time.time()
                        search_name = easygui.enterbox("Name for searching")
                        if search_name is None:
                            self.game_reboot()
                            return
                        res = self.connect.get_new_game(search_name)
                        if isinstance(res, dict):
                            singleplayer.Game.set_battlefield_from_type(self, res["battlefield"], config.CELL_BODY)
                            self.connect.js = res
                            self.connect.lobby_id = res["id"]

                            self.player_tanks = [
                                Tank(config.TANK_STATS, (0, 5), surface=config.CELL_BODY, player=False),
                                Tank(config.TANK_STATS, (0, 4), surface=config.CELL_BODY, player=False)]
                            self.enemy_tanks = [Tank(config.TANK_STATS, (9, 5), surface=config.CELL_BODY),
                                                Tank(config.TANK_STATS, (9, 4), surface=config.CELL_BODY)]
                            self.enemy_towers = [tower.Tower(config.TOWER_STATS, (8, 6), surface=config.CELL_BODY),
                                                 tower.Tower(config.TOWER_STATS, (8, 3), surface=config.CELL_BODY)]
                            self.player_towers = [
                                tower.Tower(config.TOWER_STATS, (1, 6), surface=config.CELL_BODY, player=False),
                                tower.Tower(config.TOWER_STATS, (1, 3), surface=config.CELL_BODY, player=False)]
                            self.GAME_STATUS = "GET"
                            self.CONNECTING = False
                        elif res == 404:
                            self.GAME_STATUS = "MENU"
                            self.CONNECTING = False
            else:
                singleplayer.Game.create_FOV(self, self.player_tanks, self.player_towers)
                self.game_visualization()
                if self.GAME_STATUS == "SET":
                    if len(self.player_tanks) == 0 or len(self.player_towers) == 0:
                        self.game_reboot()
                        self.connect.win()
                        easygui.msgbox("Поздравляю вы выиграли!", "Победа!")
                        return
                    elif len(self.enemy_tanks) == 0 or len(self.enemy_towers) == 0:
                        self.game_reboot()
                        easygui.msgbox("К сожалению вы проиграли", "Поражение!")
                        return
                    else:
                        if self.player_turn:
                            mouse_keys = pygame.mouse.get_pressed()
                            if mouse_keys[0]:
                                mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (0, 0))
                                y = 0
                                for line in self.battlefield:
                                    x = 0
                                    for cell in line:
                                        if cell.get_rect().contains(mouse_rect):
                                            move = (y, x)
                                            chosen_tank = 0
                                            ZeroAP_counter = 0
                                            for tank1 in self.player_tanks:
                                                if tank1.AP <= 0:
                                                    ZeroAP_counter += 1
                                                if tank1.pos[0] == y and tank1.pos[1] == x:
                                                    self.chosen_tank = chosen_tank
                                                chosen_tank += 1
                                            if len(self.player_tanks) == ZeroAP_counter:
                                                self.player_turn = False
                                            elif self.chosen_tank is not None:
                                                if singleplayer.Game.tankActions(self,
                                                                                 self.player_tanks[self.chosen_tank],
                                                                                 move):
                                                    self.moves.append({"chosen_tank": self.chosen_tank, "move": move})

                                                    print(cell.type, cell.hp)

                                        x += 1
                                    y += 1

                        else:
                            singleplayer.Game.tank_Fight(self, self.player_tanks, self.player_towers
                                                         , self.enemy_tanks, self.enemy_towers)
                            second_tick = time.time()
                            if second_tick - self.first_tick > 10:
                                print("try to set ")
                                self.first_tick = time.time()
                                res = self.connect.set_game(self.moves)
                                if res == "game is set":
                                    self.moves.clear()
                                    self.GAME_STATUS = "GET"
                                    print("game is set")
                                elif res == 404:
                                    self.game_reboot()
                            else:
                                f = pygame.font.SysFont('arial', 24)
                                host_text = f.render(
                                    'Ожидайте противника ' + str(
                                        round(10 + self.first_tick - second_tick)) + " сек ...",
                                    True, self.BLACK, self.WHITE)
                                host_position = host_text.get_rect(center=(round(self.WIDTH * 0.75), self.HEIGHT // 2))
                                self.screen.blit(host_text, host_position)
                elif self.GAME_STATUS == "GET":
                    second_tick = time.time()
                    if second_tick - self.first_tick > 10:
                        self.first_tick = time.time()
                        res = self.connect.get_game()
                        if isinstance(res, dict):
                            for tank1 in self.player_tanks:
                                tank1.AP = 2
                            for tank1 in self.enemy_tanks:
                                tank1.AP = 2
                            moves = res["moves"]
                            for move in moves:
                                singleplayer.Game.tankActions(self, self.enemy_tanks[move["chosen_tank"]]
                                                              , move["move"])
                            singleplayer.Game.tank_Fight(self, self.player_tanks, self.player_towers
                                                         , self.enemy_tanks, self.enemy_towers)
                            self.player_turn = True
                            self.GAME_STATUS = "SET"
                        elif res == 404:
                            self.game_reboot()
                    else:
                        f = pygame.font.SysFont('arial', 24)
                        host_text = f.render(
                            'Ожидайте противника ' + str(round(10 + self.first_tick - second_tick)) + " сек ...",
                            True, self.BLACK, self.WHITE)
                        host_position = host_text.get_rect(center=(round(self.WIDTH * 0.75), self.HEIGHT // 2))
                        self.screen.blit(host_text, host_position)
        pygame.display.update()

    def settings_Cycle(self):
        if self.SETTINGS_MENU:
            f = pygame.font.SysFont('arial', 24)
            move_text = f.render('Звук хода', True, self.BLACK, self.WHITE)
            move_position = move_text.get_rect(center=(self.WIDTH // 2, 220))
            self.screen.blit(move_text, move_position)
            shot_text = f.render('Звук выстрела', True, self.BLACK, self.WHITE)
            shot_position = shot_text.get_rect(center=(self.WIDTH // 2, 260))
            f = pygame.font.SysFont('arial', 50)
            self.screen.blit(shot_text, shot_position)
            plus_text = f.render('+', True, self.BLACK, self.WHITE)
            plus_position = plus_text.get_rect(center=(self.WIDTH // 2 - 20, 320))
            self.screen.blit(plus_text, plus_position)
            minus_text = f.render('-', True, self.BLACK, self.WHITE)
            minus_position = minus_text.get_rect(center=(self.WIDTH // 2 + 20, 320))
            self.screen.blit(minus_text, minus_position)
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_keys = pygame.mouse.get_pressed()
                    if mouse_keys[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if move_position.topleft[0] < mouse_pos[0] < move_position.bottomright[0] and \
                                move_position.topleft[1] < mouse_pos[1] < move_position.bottomright[1]:
                            pygame.draw.rect(self.screen, self.BLACK, move_position, 2)
                            config.MOVE_SOUND = easygui.fileopenbox(filetypes=["*.mp3", "*.wav"])
                        elif shot_position.topleft[0] < mouse_pos[0] < shot_position.bottomright[0] and \
                                shot_position.topleft[1] < mouse_pos[1] < shot_position.bottomright[1]:
                            pygame.draw.rect(self.screen, self.BLACK, shot_position, 2)
                            config.SHOT_SOUND = easygui.fileopenbox(filetypes=["*.mp3", "*.wav"])
                        elif plus_position.topleft[0] < mouse_pos[0] < plus_position.bottomright[0] and \
                                plus_position.topleft[1] < mouse_pos[1] < plus_position.bottomright[1]:
                            pygame.draw.rect(self.screen, self.BLACK, plus_position, 2)
                            self.sounds.plus_volume()
                            singleplayer.Game.set_sounds(self, self.sounds)
                        elif minus_position.topleft[0] < mouse_pos[0] < minus_position.bottomright[0] and \
                                minus_position.topleft[1] < mouse_pos[1] < minus_position.bottomright[1]:
                            pygame.draw.rect(self.screen, self.BLACK, minus_position, 2)
                            self.sounds.minus_volume()
                            singleplayer.Game.set_sounds(self, self.sounds)
            pygame.display.update()


game = Game()
game.main_cycle()
