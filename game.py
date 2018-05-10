import pygame
import spritesheet
import level

class Game:
    def __init__(self, sokoban):
        self.window = sokoban.window
        self.set_window = sokoban.set_window
        self.clock = pygame.time.Clock()
        self.sprites = spritesheet.Spritesheet("sprites.png")
        self.tiles = dict(zip(("#", "-", "_", ".", "$"),
                                 self.sprites.load_strip((0, 0, 32, 32), 5)))
        self.player_frames = [self.sprites.load_strip((0, i*32, 32, 32),
                               3, colorkey=(255, 0, 0)) for i in range(1, 5)]
        self.player_direction = 0
        self.player_frame = 1

    def move(self, movement):
        tile_map = self.level.tile_map
        boxes = self.level.boxes
        player_pos = self.level.player_pos
        new_pos = [sum(x) for x in zip(player_pos, movement)]

        if tile_map[new_pos[1]][new_pos[0]] == "#":
            return

        if boxes[new_pos[1]][new_pos[0]] == "$":
            box_pos = [sum(x) for x in zip(new_pos, movement)]

            if tile_map[box_pos[1]][box_pos[0]] == "#":
                return

            if boxes[box_pos[1]][box_pos[0]] == "$":
                return

            boxes[new_pos[1]][new_pos[0]] = " "
            boxes[box_pos[1]][box_pos[0]] = "$"
            self.window.blit(self.tiles["_"], (new_pos[0]*32,
                                                      new_pos[1]*32))
            self.window.blit(self.tiles["$"], (box_pos[0]*32,
                                                      box_pos[1]*32))

        self.window.blit(self.tiles[tile_map
                         [player_pos[1]][player_pos[0]]],
                          (player_pos[0]*32, player_pos[1]*32))
        self.window.blit(self.player_frames[self.player_direction][self.player_frame],
                                                     (new_pos[0]*32, 
                                                     new_pos[1]*32))
        self.level.player_pos = new_pos

        for goal in self.level.goals:
            if boxes[goal[1]][goal[0]] != "$":
                return

        self.finished = True

    def play(self, file_path):
        for self.level in level.collection(file_path):
            self.finished = False
            self.set_window(self.level.width*32, self.level.height*32,
                                    "Sokoban - "+self.level.name)
            for r, row in enumerate(self.level.tile_map):
                for c, col in enumerate(row):
                    self.window.blit(self.tiles[col], (c*32, r*32))

                    if col != "-" and self.level.boxes[r][c] != " ":
                        self.window.blit(self.tiles[
                                         self.level.boxes[r][c]], (c*32, r*32))

            self.window.blit(self.player_frames[self.player_direction][self.player_frame],
                             (self.level.player_pos[0]*32,
                              self.level.player_pos[1]*32))

            while not self.finished:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        movement = None

                        if event.key == pygame.K_DOWN:
                            movement = (0, 1)
                            direction = 0

                        elif event.key == pygame.K_UP:
                            movement = (0, -1)
                            direction = 1

                        elif event.key == pygame.K_RIGHT:
                            movement = (1, 0)
                            direction = 2

                        elif event.key == pygame.K_LEFT:
                            movement = (-1, 0)
                            direction = 3

                        if movement:
                            if self.player_direction != direction:
                                self.player_direction = direction
                                self.player_frame = 0

                            self.player_frame = (self.player_frame + 1) % 3
                            self.move(movement)

                    elif event.type == pygame.QUIT:
                        return

                pygame.display.update()
                self.clock.tick(60)

            pygame.time.delay(1000)

"""
import pygame

from level import collection
from spritesheet import Spritesheet

class Game:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.spritesheet = Spritesheet("spritesheet.png")
        self.tiles = dict(zip(("#", "-", "_", ".", "$"),
                     self.spritesheet.load_strip((0, 0, 32, 32), 5)))
        self.player_frames = [self.spritesheet.load_strip((0, i*32, 32, 32),
                       3, colorkey=(255, 0, 0)) for i in range(1, 4)]
    
    def move(self, level, movement):
        self.window.blit(self.tiles[level.tile_map
                    [level.player_pos[1]][level.player_pos[0]]],
                    (level.player_pos[0]*32, level.player_pos[1]*32))
        new_pos = [sum(x) for x in zip(level.player_pos, movement)]
        level.player_pos = new_pos
        self.window.blit(self.player_frames[0][1], (level.player_pos[0]*32,
                                                level.player_pos[1]*32))

    def run(self, file_path):
        for level in collection(file_path):
            self.window = pygame.display.set_mode((level.width*32,
                                              level.height*32))
            pygame.display.set_caption("Sokoban - "+level.name)

            for r, row in enumerate(level.tile_map):
                for c, col in enumerate(row):
                    self.window.blit(self.tiles[col], (c*32, r*32))

                    if col != "-" and level.boxes[r][c] != " ":
                        self.window.blit(self.tiles[level.boxes[r][c]],
                                    (c*32, r*32))

            self.window.blit(self.player_frames[0][1],
                            (level.player_pos[0]*32, level.player_pos[1]*32))

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        movement = {pygame.K_UP: (0, -1),
                                    pygame.K_DOWN: (0, 1),
                                    pygame.K_LEFT: (-1, 0),
                                    pygame.K_RIGHT: (1, 0)
                                   }.get(event.key, None)
                        self.move(level, movement)
                    
                    elif event.type == pygame.QUIT:
                        return

                pygame.display.update()
                self.clock.tick(60)
"""