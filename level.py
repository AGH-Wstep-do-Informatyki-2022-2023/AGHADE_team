import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from enemy import Enemy


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if cell == 'E':
                    enemy_sprite = Enemy((x, y))
                    self.enemy.add(enemy_sprite)

    def scroll_x(self):
        player = self.player.sprite
        enemy = self.enemy.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 6
            player.speed = 0
            enemy.rect.x += 6
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -6
            player.speed = 0
            enemy.rect.x -= 6
        else:
            self.world_shift = 0
            player.speed = 6
  

    def horizontal_collisions(self):
        player = self.player.sprite
        enemy = self.enemy.sprite
        player.rect.x += player.direction.x * player.speed
        enemy.rect.x += enemy.direction.x * enemy.speed
        

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(enemy.rect):
                if enemy.direction.x < 0:
                    enemy.rect.left = sprite.rect.right
                elif enemy.direction.x > 0:
                    enemy.rect.right = sprite.rect.left

    def vertical_collisions(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0.0000001
                    
    def following(self):
        player = self.player.sprite
        enemy = self.enemy.sprite
        enemy.rect.x += enemy.direction.x * enemy.speed
        if enemy.rect.x - player.rect.x < 300 and enemy.rect.x - player.rect.x > 0 and abs(enemy.rect.x - player.rect.x) > 32:
            enemy.direction.x = -1
        elif enemy.rect.x - player.rect.x > -300 and enemy.rect.x - player.rect.x < 0 and abs(enemy.rect.x - player.rect.x) > 32:
            enemy.direction.x = 1  
                            

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        self.player.update()
        self.horizontal_collisions()
        self.vertical_collisions()
        self.enemy.update()
        self.following()
        self.player.draw(self.display_surface)
        self.enemy.draw(self.display_surface)
