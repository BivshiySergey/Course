import pygame
import random
from cells import Cell
import tank
from sounds import Sounds


class Game:
    ###Chances of cells
    def __init__(self):
        self.battlefield = None
        self.field_of_view = None

    @staticmethod
    def randomCell(surface=(40, 40)):
        rand = random.randint(0, 99)
        if rand == 0:
            return Cell(6, surface)
        elif 0 < rand < 5:
            return Cell(5, surface)
        elif 4 < rand < 15:
            return Cell(4, surface)
        elif 14 < rand < 35:
            return Cell(3, surface)
        elif 34 < rand < 55:
            return Cell(2, surface)
        elif 54 < rand < 85:
            return Cell(1, surface)
        elif 84 < rand < 100:
            return Cell(0, surface)
        else:
            return Cell(0, surface)

    def createBattlefield(self, surface=(40, 40)):
        self.battlefield = []
        for line_number in range(10):
            line = []
            if line_number < 3 or line_number > 6:
                for cell_number in range(10):
                    if cell_number < 3 or cell_number > 6:
                        line.append(Game.randomCell(surface))
                    else:
                        line.append(Cell(0, surface))
            else:
                for cell_number in range(10):
                    line.append(Game.randomCell(surface))
            self.battlefield.append(line)
        return self.battlefield

    def set_battlefield(self, battlefield):
        self.battlefield = battlefield

    def get_battlefield(self):
        return self.battlefield

    def set_sounds(self, sounds):
        self.sounds = sounds

    def tankActions(self, tank, move):
        if tank.AP > 0:
            if not tank.pos[0] == move[0] or not tank.pos[1] == move[1]:
                for y in range(tank.pos[0] - 1, tank.pos[0] + 2):
                    for x in range(tank.pos[1] - 1, tank.pos[1] + 2):
                        if move[0] == y and move[1] == x:
                            if self.battlefield[move[0]][move[1]].get_type() > 0:
                                if self.battlefield[move[0]][move[1]].damaged(tank.damage):
                                    tank.upgrade(self.battlefield[move[0]][move[1]].get_buff())
                                tank.AP -= 2
                                self.sounds.play_shot()
                            else:
                                tank.pos = move
                                tank.AP -= 1
                                self.sounds.play_move()
                            pygame.time.delay(500)
                            return True
        return False

    def tankAI(self, tank):
        while tank.AP > 0:
            move = (-1, -1)
            while move[0] < 0 or move[1] < 0 or move[0] > 9 or move[1] > 9:
                move = (random.randint(tank.pos[0] - 1, tank.pos[0] + 2),
                        random.randint(tank.pos[1] - 1, tank.pos[1] + 2))
            move1 = move
            for y in range(tank.pos[0] - 1, tank.pos[0] + 2):
                for x in range(tank.pos[1] - 1, tank.pos[1] + 2):
                    if y == tank.pos[0] and x == tank.pos[1] or tank.AP < 0 \
                            or x < 0 or y < 0 or x > 9 or y > 9:
                        continue
                    elif self.battlefield[y][x].hp > 0 < 2 * tank.damage \
                            or (self.battlefield[y][x].type == 0 and tank.damage == 1):
                        move = (y, x)
                        break
                else:
                    continue
                break
            Game.tankActions(self, tank, move)
        return

    def is_visible(self, pos):
        return self.field_of_view[pos[0]][pos[1]]

    def create_FOV(self, player_tanks, player_towers):
        self.field_of_view = []
        for y in range(10):
            line_of_FOV = []
            for x in range(10):
                line_of_FOV.append(False)
                for player_tank in player_tanks:
                    if y > player_tank.pos[0] - 2 and y < player_tank.pos[0] + 2 \
                            and x > player_tank.pos[1] - 2 and x < player_tank.pos[1] + 2:
                        line_of_FOV.pop()
                        line_of_FOV.append(True)
                        break
                for player_tower in player_towers:
                    if y > player_tower.pos[0] - 2 and y < player_tower.pos[0] + 2 \
                            and x > player_tower.pos[1] - 2 and x < player_tower.pos[1] + 2:
                        line_of_FOV.pop()
                        line_of_FOV.append(True)
                        break
            self.field_of_view.append(line_of_FOV)
        return

    def tank_Fight(self, player_tanks, player_towers, enemy_tanks, enemy_towers):
        player_objects = player_tanks.copy()
        player_objects.extend(player_towers)
        enemy_objects = enemy_tanks.copy()
        enemy_objects.extend(enemy_towers)
        for player_object in player_objects:
            for enemy_object in enemy_objects:
                while player_object.pos[0] > enemy_object.pos[0] - 2 and player_object.pos[0] < enemy_object.pos[0] + 2 \
                        and player_object.pos[1] > enemy_object.pos[1] - 2 and player_object.pos[1] < enemy_object.pos[
                    1] + 2 \
                        and player_object.hp > 0 and enemy_object.hp > 0:
                    player_object.hp -= enemy_object.damage
                    enemy_object.hp -= player_object.damage
        self.chosen_tank = None
        return

    def get_type_battlefield(self):
        battlefield = []
        for line in self.battlefield:
            line_of_type = []
            for cell in line:
                line_of_type.append(cell.get_type())
            battlefield.append(line_of_type)
        return battlefield

    def set_battlefield_from_type(self, battlefield, surface=(40, 40)):
        self.battlefield = []
        for y in range(10):
            line = []
            for x in range(10):
                cell = Cell(battlefield[y][x], surface)
                line.append(cell)
            self.battlefield.append(line)
