import pygame, sys
from Player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser

class Game:
    def __init__(self):
        # player_setup
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # obstacle_setup
        self.shape =obstacle.shape
        self.block_size = 8
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 3
        self.obstacle_x_position = [num * (screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_position, x_start=screen_width/20, y_start=400)

        #alien_setup

        self.alien = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()

        self.alien_setup(rows=6, cols=8)
        self.alien_direction = -1
        #extra_setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time  = randint(400, 800)

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'X':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,'grey', x, y)
                    self.blocks.add(block)
    def create_multiple_obstacle(self, *offset,  x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset=70, y_offset = 48):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance +x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:

                   alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.alien.add(alien_sprite)
    def alien_pos_checker(self):
        all_aliens = self.alien.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)
    def alien_move_down(self,distance):
        if self.alien:

            for alien in self.alien.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.alien.sprites():
            random_alien =choice(self.alien.sprites())
            laser_sprite = Laser(random_alien.rect.center,screen_height, 8)
            self.alien_lasers.add(laser_sprite)
    def extra_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def collison_check(self):
        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisons
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # alien collsion
                alien_hit = pygame.sprite.spritecollide(laser, self.alien, True)
                if alien_hit:
                    for alien in alien_hit:
                        self.score += alien.value
                    laser.kill()
                # extra
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    laser.kill()
                    self.score += 500

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        #alien
        if self.alien:
            for alien in self.alien:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player,False):
                    pygame.quit()
                    sys.exit()
    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))
    def display_score(self):
        score_surf = self.font.render(f'score : {self.score}', False, 'White')
        score_rect =score_surf.get_rect(topleft= (10, 0))
        screen.blit(score_surf, score_rect)


    def run(self):
        self.player.draw(screen)
        self.alien.update(self.alien_direction)
        self.alien_pos_checker()
        self.alien_lasers.update()
        self.extra_timer()
        self.extra.update()
        self.collison_check()
        self.display_lives()

        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.extra.draw(screen)


        self.blocks.draw(screen)
        self.alien.draw(screen)
        self.alien_lasers.draw(screen)
        self.display_lives()
        self.display_score()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALienlaser = pygame.USEREVENT
    pygame.time.set_timer(ALienlaser, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALienlaser:
                game.alien_shoot()
        screen.fill((50, 40, 40))
        game.run()
        pygame.display.flip()
        clock.tick(60)