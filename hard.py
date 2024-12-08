import pygame, time, random, math, heapq
import numpy as np

_display = pygame.display
color_red = pygame.Color(255, 0, 0)
GAMEOVER = False
player_pos = [0]

class MainGame(object):
    
    screen_width = 900
    screen_height = 720
    tank_p1 = None
    window = None
    enemy_tank_list = []
    enemtank_count = 3
    bullet_list = []
    enemytank_bullet_list = []
    explode_list = []
    wall_list = []
    enemy_tank_counter = 0
    enemy_tank_killed = 0

    def startgame(self):

        pygame.display.init()
        MainGame.window = _display.set_mode([MainGame.screen_width, MainGame.screen_height])
        pygame.display.set_caption("DUCK ESCAPE")
        global player_pos
        self.create_my_duck()
        self.create_enemy_snake()
        self.create_walls()
        global GAMEOVER

        while not GAMEOVER:
            MainGame.window.fill(pygame.Color(0, 0, 0))
            self.get_event()
            self.blit_walls()
            if MainGame.tank_p1 and MainGame.tank_p1.alive:
                MainGame.tank_p1.display_tank()
            MainGame.window.blit(self.draw_text("Enemy Remains:%d" % len(MainGame.enemy_tank_list)), (7, 7))

            self.blit_walls()
            if MainGame.tank_p1 and MainGame.tank_p1.alive:
                MainGame.tank_p1.display_tank()

            self.blit_enemy_snake()

            if MainGame.tank_p1 and not MainGame.tank_p1.stop:
                MainGame.tank_p1.move()
                MainGame.tank_p1.hit_wall()
                MainGame.tank_p1.hit_enemy_snake()

            self.blit_enemy_bullet()
            self.blit_bullet()
            self.blit_explode()
            time.sleep(0.02)
            _display.update()
            self.blit_enemy_snake()

            if len(MainGame.enemy_tank_list) == 0 and MainGame.enemy_tank_counter == 2:
                GAMEOVER = True
                self.game_over("You Won!!!")
                pygame.quit()

        pygame.quit()

    def create_my_duck(self):
        MainGame.tank_p1 = MyDuck(420, 660, 0)
        global player_pos
        player_pos = [420, 660]

    def create_enemy_snake(self):
        top = 0

        for i in range(MainGame.enemtank_count):
            speed = random.randint(1, 3) #// 2
            odd_numbers = [x for x in range(0, 6) if x % 2 == 1]
            left = np.random.choice(odd_numbers)
            etank = EnemySnake(left * 60, top, speed, 1)
            MainGame.enemy_tank_list.append(etank)

    def create_walls(self):
        with open("world.txt", "r") as f:
            maze = [list(line.strip()) for line in f.readlines()]

        for row_index, row in enumerate(maze):
            for col_index, cell in enumerate(row):
                if cell == 'y':
                    wall = Wall(col_index * 60, row_index * 60)
                    MainGame.wall_list.append(wall)

    def blit_walls(self):
        for wall in MainGame.wall_list:
            if wall.live:
                wall.display_wall()
            else:
                MainGame.wall_list.remove(wall)

    def blit_enemy_snake(self):
        for etank in MainGame.enemy_tank_list:
            if etank.live:
                etank.display_tank()
                etank.direction = etank.next_direction()  # Update direction more frequently
                etank.move()
                etank.hit_wall()
                etank.hit_my_duck()
                ebullet = etank.shot()

                if ebullet:
                    MainGame.enemytank_bullet_list.append(ebullet)
            else:
                MainGame.enemy_tank_list.remove(etank)
                if MainGame.enemy_tank_counter < 2:
                    top = 0
                    speed = random.randint(1, 3)  # // 2
                    odd_numbers = [x for x in range(0, 6) if x % 2 == 1]
                    left = np.random.choice(odd_numbers)
                    new_etank = EnemySnake(left * 60, top, speed, 1)
                    MainGame.enemy_tank_list.append(new_etank)
                    MainGame.enemy_tank_counter += 1

    def blit_enemy_bullet(self):
        for ebullet in MainGame.enemytank_bullet_list:
            if ebullet.alive:
                ebullet.display_bullet()
                ebullet.bullet_move()
                ebullet.hit_walls()
                if MainGame.tank_p1.alive:
                    ebullet.hit_my_duck()
                else:
                    self.respawn_my_duck()
            else:
                MainGame.enemytank_bullet_list.remove(ebullet)

    def blit_bullet(self):
        for bullet in MainGame.bullet_list:
            if bullet.alive:
                bullet.display_bullet()
                bullet.bullet_move()
                bullet.hit_enemy_snake()
                bullet.hit_walls()
            else:
                MainGame.bullet_list.remove(bullet)

    def blit_explode(self):
        for explode in MainGame.explode_list:
            if explode.live:
                explode.display_explode()
            else:
                MainGame.explode_list.remove(explode)

    def draw_text(self, content):
        pygame.font.init()
        font = pygame.font.SysFont("kaiti", 18)
        text_sf = font.render(content, True, color_red)
        return text_sf
    
    def get_event(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                print("Quit")
                self.game_over()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if MainGame.tank_p1 and MainGame.tank_p1.alive:
                        MainGame.tank_p1.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Quit")
                    self.game_over()
                    #self.create_my_duck()

                if MainGame.tank_p1 and MainGame.tank_p1.alive:
                    if event.key == pygame.K_LEFT:
                        MainGame.tank_p1.direction = "l"
                        MainGame.tank_p1.stop = False

                    if event.key == pygame.K_RIGHT:
                        MainGame.tank_p1.direction = "r"
                        MainGame.tank_p1.stop = False

                    if event.key == pygame.K_UP:
                        MainGame.tank_p1.direction = "u"
                        MainGame.tank_p1.stop = False

                    if event.key == pygame.K_DOWN:
                        MainGame.tank_p1.direction = "d"
                        MainGame.tank_p1.stop = False

                    if event.key == pygame.K_SPACE:
                        if len(MainGame.bullet_list) < 3:
                            m = Bullet(MainGame.tank_p1)
                            MainGame.bullet_list.append(m)
    
    def respawn_my_duck(self):
        if not MainGame.tank_p1.alive:
            MainGame.tank_p1 = MyDuck(420, 660, 0)
            player_pos = [420, 660]

    def game_over(self, message):
        font = pygame.font.SysFont("arial", 48)
        text = font.render(message, True, color_red)
        text_rect = text.get_rect(center=(MainGame.screen_width // 2, MainGame.screen_height // 2))
        MainGame.window.blit(text, text_rect)
        pygame.display.update()
        time.sleep(3)  # Pause for 3 seconds to show the message 
        
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Tank(BaseItem):

    def __init__(self, left, top, determination):
        self.images = {
            "u": pygame.image.load("playerUp.png"),
            "d": pygame.image.load("playerDown.png"),
            "l": pygame.image.load("playerLeft.png"),
            "r": pygame.image.load("playerRight.png"),
        }
        self.isPlayer = determination
        self.direction = "u"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5
        self.stop = True
        self.oldtop = self.rect.top
        self.oldleft = self.rect.left

    def move(self):
        global player_pos
        self.oldtop = self.rect.top
        self.oldleft = self.rect.left
        if self.direction == "u":
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == "d":
            if self.rect.top < MainGame.screen_height - MainGame.tank_p1.rect.height:
                self.rect.top += self.speed
        elif self.direction == "l":
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == "r":
            if self.rect.left < MainGame.screen_width - MainGame.tank_p1.rect.width:
                self.rect.left += self.speed

        if self.isPlayer == 0:
            player_pos = (self.rect.left, self.rect.top)

    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop

    def hit_wall(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.stay()

    def shot(self):
        return Bullet(self)

    def display_tank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)

class MyDuck(Tank):
    def __init__(self, left, top, determination):
        super(MyDuck, self).__init__(left, top, determination)

    def hit_enemy_snake(self):
        for e_tank in MainGame.enemy_tank_list:
            if pygame.sprite.collide_rect(e_tank, self):
                self.stay()

class EnemySnake(Tank):

    def __init__(self, left, top, speed, determination):
        self.images = {
            "u": pygame.image.load("enemyUp.png"),
            "d": pygame.image.load("enemyDown.png"),
            "l": pygame.image.load("enemyLeft.png"),
            "r": pygame.image.load("enemyRight.png"),
        }
        global player_pos
        self.isPlayer = determination
        self.direction = "u"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.stop = True
        self.step = 1
        self.live = True
        
        self.direction = self.next_direction()
        self.shot_counter = 0
        self.shot_delay = random.randint(30, 100)
    
    def next_direction(self):

        direction = self.limited_a_star()
        if direction is None:
            if random.random() < 0.4:
                direction = self.charge()
            else:
                direction = self.jiggle()

        return direction
    
    def distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
    
    def get_neighbours(self, position):
        neighbours = []
        wall_padding = 30  # Half of the wall size (60 / 2)

        for dx, dy, direction in [(-1, 0, 'l'), (1, 0, 'r'), (0, -1, 'u'), (0, 1, 'd')]:
            new_x = position[0] + dx
            new_y = position[1] + dy

            if 0 <= new_x < MainGame.screen_width and 0 <= new_y < MainGame.screen_height:
                collide_with_wall = False
                for wall in MainGame.wall_list:
                    # Check if the new position is within the surrounding area of the wall
                    if wall.rect.inflate(wall_padding, wall_padding).collidepoint(new_x, new_y):
                        collide_with_wall = True
                        break
                if not collide_with_wall:
                    neighbours.append(((new_x, new_y), direction))

        return neighbours

    def limited_a_star(self):
        global player_pos
        start = (self.rect.x, self.rect.y)
        end = (player_pos[0], player_pos[1])

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = [(0, start, None)]
        closed_set = set()
        
        iterations = 0
        max_iterations = 1000

        while open_set:
            iterations += 1
            if iterations > max_iterations:
                break

            _, current, direction = heapq.heappop(open_set)

            if heuristic(current, end) < self.rect.width:
                if self.will_collide_with_wall_in_next_move(direction):
                    # Force algorithm: Move left or right by 60 units if there's a wall in front
                    if direction in ['l', 'r']:
                        new_direction = 'u' if self.rect.top > MainGame.tank_p1.rect.top else 'd'
                        new_pos = (self.rect.x, self.rect.y + (60 if new_direction == 'd' else -60))
                    else:  # direction in ['u', 'd']
                        new_direction = 'l' if self.rect.left > MainGame.tank_p1.rect.left else 'r'
                        new_pos = (self.rect.x + (60 if new_direction == 'r' else -60), self.rect.y)

                    if not self.will_collide_with_wall_in_next_move(new_direction):
                        return new_direction

                else:
                    return direction

            if current in closed_set:
                continue

            closed_set.add(current)

            for neighbour, next_direction in self.get_neighbours(current):
                if neighbour in closed_set:
                    continue

                tentative_g_score = heuristic(current, neighbour)
                f_score = tentative_g_score + heuristic(neighbour, end)
                heapq.heappush(open_set, (f_score, neighbour, next_direction if direction == '' else direction))

        return None

    def will_collide_with_wall_in_next_move(self, direction):
        future_rect = self.rect.copy()
        if direction == "u":
            future_rect.top -= self.speed
        elif direction == "d":
            future_rect.top += self.speed
        elif direction == "l":
            future_rect.left -= self.speed
        elif direction == "r":
            future_rect.left += self.speed

        for wall in MainGame.wall_list:
            if future_rect.colliderect(wall.rect):
                return True
        return False
    
    # Scripts
    def jiggle(self):

        global player_pos

        charge_probability = 0.5
        valid_directions = []

        for dx, dy, direction in [(-self.speed, 0, "l"), (self.speed, 0, "r"), (0, -self.speed, "u"), (0, self.speed, "d")]:
            new_x, new_y = self.rect.left + dx, self.rect.top + dy

            # Create a temporary rect to check for wall collisions
            temp_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)
            
            # Check if the new position would collide with any walls
            wall_collision = any([temp_rect.colliderect(wall.rect) for wall in MainGame.wall_list])

            # If the new position doesn't collide with any walls, add the direction to valid_directions
            if not wall_collision:
                valid_directions.append((new_x, new_y, direction))

        # Choose a random direction from valid_directions
        if valid_directions:
            chosen_direction = random.choice(valid_directions)
            chosen_new_x, chosen_new_y, chosen_new_direction = chosen_direction

            # Calculate the distance to the player's position
            dist_to_player = self.distance((chosen_new_x, chosen_new_y), player_pos)

            # Decide whether to charge or flank based on the charge_probability
            if random.random() < charge_probability:  # Charge towards the player
                min_distance = float("inf")
                for new_x, new_y, direction in valid_directions:
                    dist = self.distance((new_x, new_y), player_pos)
                    if dist < min_distance:
                        min_distance = dist
                        chosen_new_direction = direction
            else:  # Flanking behavior (chosen randomly)
                pass  # The chosen direction is already random

            return chosen_new_direction
        else:
            return self.direction
        
    def charge(self):

        global player_pos
        min_distance = float("inf")
        next_direction = self.direction

        for dx, dy, direction in [(-self.speed, 0, "l"), (self.speed, 0, "r"), (0, -self.speed, "u"), (0, self.speed, "d")]:
            new_x, new_y = self.rect.left + dx, self.rect.top + dy
            new_pos = (new_x, new_y)
            dist = self.distance(new_pos, player_pos)

            # Create a temporary rect to check for wall collisions
            temp_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)
            
            # Check if the new position would collide with any walls
            wall_collision = any([temp_rect.colliderect(wall.rect) for wall in MainGame.wall_list])

            # If the new position doesn't collide with any walls and has a smaller distance, update the direction
            if not wall_collision and dist < min_distance:
                min_distance = dist
                next_direction = direction

        return next_direction

    def shot(self):
        global player_pos
        self.shot_counter += 1

        # Check if the player is in sight
        player_in_sight = (abs(player_pos[0] - self.rect.left) < 30) or (abs(player_pos[1] - self.rect.top) < 30)

        # Shoot only if the player is in sight and the shot_counter has reached the shot_delay
        if player_in_sight and self.shot_counter >= self.shot_delay:
            self.shot_counter = 0
            self.shot_delay = random.randint(30, 100)  # Reset the shot delay with a new random value
            return Bullet(self)
    
        return None

    def hit_my_duck(self):
        if pygame.sprite.collide_rect(self, MainGame.tank_p1):
            self.stay()

class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load("bullet.png")
        self.direction = tank.direction
        self.speed = 10
        self.rect = self.image.get_rect()
        
        if self.direction == "u":
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == "d":
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == "l":
            self.rect.left = tank.rect.left - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == "r":
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        
        self.speed = 10
        self.alive = True

    def bullet_move(self):
        if self.direction == "u":
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.alive = False
        elif self.direction == "d":
            if self.rect.top < MainGame.screen_height - self.rect.height:
                self.rect.top += self.speed
            else:
                self.alive = False
        elif self.direction == "l":
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.alive = False
        elif self.direction == "r":
            if self.rect.left < MainGame.screen_width - self.rect.width:
                self.rect.left += self.speed
            else:
                self.alive = False

    def hit_enemy_snake(self):
        for e_tank in MainGame.enemy_tank_list:
            if pygame.sprite.collide_rect(e_tank, self) and self.alive:  
                explode = Explode(e_tank)
                MainGame.explode_list.append(explode)
                self.alive = False
                e_tank.live = False

    def hit_my_duck(self):
        if pygame.sprite.collide_rect(self, MainGame.tank_p1):
            explode = Explode(MainGame.tank_p1)
            MainGame.explode_list.append(explode)
            MainGame.tank_p1.alive = False
            self.alive = False

    def hit_walls(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.alive = False

    def display_bullet(self):
        MainGame.window.blit(self.image, self.rect)


class Explode:
    def __init__(self, tank):
        self.rect = tank.rect
        self.image = pygame.image.load("blast.png")
        self.live = True
        self.display_time = 10

    def display_explode(self):
        if self.display_time > 0:
            MainGame.window.blit(self.image, self.rect)
            self.display_time -= 1
        else:
            self.live = False

class Wall:
    def __init__(self,left,top):
        self.image = pygame.image.load("brick.png")
        self.rect = self.image.get_rect()
        
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 3
        
    def display_wall(self):
        MainGame.window.blit(self.image,self.rect)

class Waypoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

import heapq

class Node:
    def __init__(self, position):
        self.position = position

    def distance(self, other):
        # Assuming position is a tuple (x, y)
        return ((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2) ** 0.5

def a_star_pathfinding(start, end, waypoints):
    def heuristic(a, b):
        return a.distance(b)

    open_set = [(0, start, [])]  # (f_score, current_node, path)
    closed_set = set()

    while open_set:
        _, current, path = heapq.heappop(open_set)

        if current.position == end.position:
            return path + [current]  # Return the full path including the end node

        if current in closed_set:
            continue

        closed_set.add(current)

        for waypoint in waypoints:
            if waypoint in closed_set:
                continue

            tentative_g_score = current.distance(waypoint)  # Cost from current to waypoint
            f_score = tentative_g_score + heuristic(waypoint, end)  # Total cost

            heapq.heappush(open_set, (f_score, waypoint, path + [current]))

    return None  # No path found


# Call the startgame method
MainGame().startgame()