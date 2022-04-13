import pygame
pygame.init()

screen = pygame.display.set_mode([1000, 700])
font = pygame.font.SysFont("comicsansms", 30)

running = True


class Circle:
    def __init__(self, x, y, r, name):
        self.rect = pygame.Rect(x - r, y - r, 2 * r, 2 * r)
        self.pos = (x, y)
        self.r = r
        self.moving = False
        self.inside = False
        self.name = name
        self.t = None

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), self.pos, self.r)
        self.t = font.render(self.name, True, (255, 255, 255))
        screen.blit(self.t, (self.rect.x + self.r - self.t.get_width()/2, self.rect.y + self.r - self.t.get_height()/2))
        if self.moving:
            pygame.draw.circle(screen, (255, 0, 0), self.pos, self.r, 10)

    def ret_rect(self):
        return self.rect

    def ret_r(self):
        return self.r

    def collision(self, rect):
        inside = False
        where = 0
        if rect.x <= self.rect.x + self.rect.w <= rect.x + rect.w and rect.y <= self.rect.y + self.rect.h <= rect.y + rect.h:
            inside = True
            where = -1
        if rect.x <= self.rect.x + self.rect.w <= rect.x + rect.w and rect.y <= self.rect.y <= rect.y + rect.h:
            inside = True
            where = -2
        if rect.x <= self.rect.x <= rect.x + rect.w and rect.y <= self.rect.y + self.rect.h <= rect.y + rect.h:
            inside = True
            where = 1
        if rect.x <= self.rect.x <= rect.x + rect.w and rect.y <= self.rect.y <= rect.y + rect.h:
            inside = True
            where = 2
        return inside, where

    def mouse_in(self, mouse_pos):
        if self.rect.x <= mouse_pos[0] <= self.rect.x + self.rect.h and self.rect.y <= mouse_pos[1] <= self.rect.y + self.rect.w:
            self.inside = True
        else:
            self.inside = False

    def check_mouse(self, c):
        if c == (1, 0, 0) and self.inside:
            self.moving = True
        if c == (0, 0, 1) and self.inside:
            self.moving = False

    def move(self, mouse_pos, rect):
        if self.moving:
            if mouse_pos[0] - self.r >= 0 and mouse_pos[0] + self.r <= 1000 and mouse_pos[1] - self.r >= 0 \
                    and mouse_pos[1] + self.r <= 500:
                check = self.collision(rect)
                if not check[0]:
                    self.pos = mouse_pos
                    self.rect.x = self.pos[0] - self.r
                    self.rect.y = self.pos[1] - self.r
                else:
                    if check[1] == -1:
                        self.pos = (mouse_pos[0] - 5, mouse_pos[1] - 5)
                        self.rect.x = self.pos[0] - self.r
                        self.rect.y = self.pos[1] - self.r
                        pygame.mouse.set_pos(mouse_pos[0] - 5, mouse_pos[1] - 5)
                    elif check[1] == -2:
                        self.pos = (mouse_pos[0] - 5, mouse_pos[1] + 5)
                        self.rect.x = self.pos[0] - self.r
                        self.rect.y = self.pos[1] - self.r
                        pygame.mouse.set_pos(mouse_pos[0] - 5, mouse_pos[1] + 5)
                    elif check[1] == 1:
                        self.pos = (mouse_pos[0] + 5, mouse_pos[1] - 5)
                        self.rect.x = self.pos[0] - self.r
                        self.rect.y = self.pos[1] - self.r
                        pygame.mouse.set_pos(mouse_pos[0] + 5, mouse_pos[1] - 5)
                    elif check[1] == 2:
                        self.pos = (mouse_pos[0] + 5, mouse_pos[1] + 5)
                        self.rect.x = self.pos[0] - self.r
                        self.rect.y = self.pos[1] - self.r
                        pygame.mouse.set_pos(mouse_pos[0] + 5, mouse_pos[1] + 5)


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.start_pos = (x1, y1)
        self.end_pos = (x2, y2)

    def calculate(self, rect1, r1, rect2, r2):
        self.start_pos = (rect1.x + rect1.w, rect1.y + r1)
        self.end_pos = (rect2.x, rect2.y + r2)

    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), self.start_pos, self.end_pos, 5)


class Area:
    def __init__(self, x, id, num):
        self.t = None
        self.rect = pygame.Rect(x, 540, 40, 40)
        self.id = id
        self.num = num

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 5)
        if self.id == 0 or self.id == 24:
            self.t = font.render("#", True, (255, 0, 0))
            screen.blit(self.t, (self.rect.x + self.t.get_width() / 3, 530 + self.t.get_height() / 5))
        else:
            self.t = font.render(str(self.num), True, (255, 0, 0))
            if self.num == 1:
                screen.blit(self.t, (self.rect.x + self.t.get_width(), 530 + self.t.get_height() / 5))
            elif self.num == 0:
                screen.blit(self.t, (self.rect.x + self.t.get_width()/1.5, 530 + self.t.get_height() / 5))


class Head:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def draw(self):
        pygame.draw.polygon(screen, (255, 255, 255), ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)))

    def move(self, dir):
        if dir == 1 and self.x1 + 40 < 1000:
            self.x1 = self.x1 + 40
            self.x2 = self.x2 + 40
            self.x3 = self.x3 + 40
        elif dir == -1 and self.x1 - 40 >= 0:
            self.x1 = self.x1 - 40
            self.x2 = self.x2 - 40
            self.x3 = self.x3 - 40