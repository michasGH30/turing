import pygame

pygame.init()

screen = pygame.display.set_mode([1000, 700])
font = pygame.font.SysFont("comicsansms", 30)
font2 = pygame.font.SysFont("comicsansms", 60)

running = True


class Circle:
    def __init__(self, x, y, r, name):
        self.rect = pygame.Rect(x - r, y - r, 2 * r, 2 * r)
        self.pos = (x, y)
        self.r = r
        self.moving = False
        self.inside = False
        self.active = False
        self.name = name
        self.t = None
        self.to_render = None
        self.write_list = []
        self.move_list = []
        self.change_list = []
        self.write_textinput = TextInput(pygame.Rect(0, 600, 50, 50), "Write", False)
        self.move_textinput = TextInput(pygame.Rect(150, 600, 50, 50), "Move", False)
        self.change_state_textinput = TextInput(pygame.Rect(300, 600, 50, 50), "Change state", False)
        self.button = Button(pygame.Rect(550, 600, 50, 50), "+", 2)

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), self.pos, self.r)
        self.t = font.render(self.name, True, (255, 255, 255))
        screen.blit(self.t,
                    (self.rect.x + self.r - self.t.get_width() / 2, self.rect.y + self.r - self.t.get_height() / 2))
        if self.moving:
            pygame.draw.circle(screen, (255, 0, 0), self.pos, self.r, 10)
            self.write_textinput.draw()
            self.move_textinput.draw()
            self.change_state_textinput.draw()
            self.button.draw()
        elif not self.moving and self.active:
            pygame.draw.circle(screen, (255, 255, 0), self.pos, self.r, 10)
            self.write_textinput.draw()
            self.move_textinput.draw()
            self.change_state_textinput.draw()
            self.button.draw()

        if len(self.write_list) > 0 and (self.moving or (not self.moving and self.active)):
            for i in range(0, len(self.write_list)):
                self.to_render = font.render(
                    str(self.write_list[i] + ' ' + self.move_list[i] + ' ' + self.change_list[i]),
                    True, (255, 255, 255))
                screen.blit(self.to_render, (750, i * self.to_render.get_height() + 5))

    def ret_rect(self):
        return self.rect

    def ret_r(self):
        return self.r

    def collision(self, rect):
        inside = False
        where = 0
        if rect.x <= self.rect.x + self.rect.w <= rect.x + rect.w \
                and rect.y <= self.rect.y + self.rect.h <= rect.y + rect.h:
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

    def check_active(self, mpos, c):
        if self.rect.x < mpos[0] < self.rect.x + self.rect.w and self.rect.y < mpos[1] < self.rect.y + self.rect.h:
            if c == (1, 0, 0):
                self.moving = True
                self.active = True
            elif c == (0, 0, 1):
                self.moving = False
                self.active = False
            elif c == (0, 1, 0):
                self.active = True
        elif 0 < mpos[0] < 700 and 0 < mpos[1] < 500:
            if c == (1, 0, 0) or c == (0, 1, 0) or c == (0, 0, 1):
                self.active = False

    def text_box_and_button(self, mpos, c, e):
        self.write_textinput.check_active(mpos, c)
        self.write_textinput.write(e)

        self.move_textinput.check_active(mpos, c)
        self.move_textinput.write(e)

        self.change_state_textinput.check_active(mpos, c)
        self.change_state_textinput.write(e)

        if self.button.check_active(mpos, c):
            self.write_list.append(self.write_textinput.ret_text())
            self.move_list.append(self.move_textinput.ret_text())
            self.change_list.append(self.change_state_textinput.ret_text())

    def move(self, mouse_pos, rect):
        if self.moving:
            if mouse_pos[0] - self.r >= 0 and mouse_pos[0] + self.r <= 700 and mouse_pos[1] - self.r >= 0 \
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
            screen.blit(self.t,
                        (self.rect.x + 20 - (self.t.get_width() / 2), self.rect.y + 20 - (self.t.get_height() / 2)))


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

    def move(self, direction):
        if direction == 1 and self.x1 + 40 < 1000:
            self.x1 = self.x1 + 40
            self.x2 = self.x2 + 40
            self.x3 = self.x3 + 40
        elif direction == -1 and self.x1 - 40 >= 0:
            self.x1 = self.x1 - 40
            self.x2 = self.x2 - 40
            self.x3 = self.x3 - 40


class TextInput:
    def __init__(self, rect, label, start):
        self.rect = rect
        self.text = ''
        self.text_tex = font.render(self.text, True, (255, 255, 255))
        self.active = False
        self.label_tex = font.render(label, True, (255, 255, 255))
        self.start = start

    def check_active(self, mpos, c):
        if self.rect.x + self.label_tex.get_width() < mpos[0] < self.rect.x + self.label_tex.get_width() + self.rect.w \
                and self.rect.y < mpos[1] < self.rect.y + self.rect.h:
            if c == (1, 0, 0):
                if not self.active:
                    self.active = True
        else:
            if c == (1, 0, 0):
                if self.active:
                    self.active = False

    def start_menu_update(self):
        if self.start:
            if self.text_tex.get_width() + 10 >= self.rect.w - 28:
                self.rect.w = self.rect.w + 10

    def draw(self):
        screen.blit(self.label_tex, (self.rect.x, self.rect.y))
        if self.active:
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.rect.x + self.label_tex.get_width() + 10, self.rect.y, self.rect.w, self.rect.h), 1)
        elif not self.active:
            pygame.draw.rect(screen, (255, 255, 255),
                             (self.rect.x + self.label_tex.get_width() + 10, self.rect.y, self.rect.w, self.rect.h), 1)
        self.text_tex = font.render(self.text, True, (255, 255, 255))
        screen.blit(self.text_tex, (self.rect.x + 28 + self.label_tex.get_width(), self.rect.y + 1))

    def ret_text(self):
        return self.text

    def write(self, e):
        if self.active:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if not self.start:
                        if len(self.text) < 1:
                            self.text = self.text + e.unicode
                    else:
                        if len(self.text) < 23:
                            self.text = self.text + e.unicode


class Button:
    def __init__(self, rect, text, font_s):
        self.rect = rect
        self.text_tex = None
        self.active = False
        self.font_size = font_s
        if self.font_size == 1:
            self.text_tex = font.render(text, True, (0, 0, 0))
        elif self.font_size == 2:
            self.text_tex = font2.render(text, True, (0, 0, 0))

    def check_active(self, mpos, c):
        if self.rect.x < mpos[0] < self.rect.x + self.rect.w and self.rect.y < mpos[1] < self.rect.y + self.rect.h:
            self.active = True
            if c == (1, 0, 0):
                return True
            return False
        else:
            self.active = False
            return False

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 255)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 255)

        if self.font_size == 2:
            screen.blit(self.text_tex, (self.rect.x + self.text_tex.get_width() / 2.5,
                                        self.rect.y - self.text_tex.get_height() / 4))
        elif self.font_size == 1:
            screen.blit(self.text_tex, (self.rect.x + self.text_tex.get_width() / 2,
                                        self.rect.y + self.text_tex.get_height() / 10))


class StartMenu:
    def __init__(self):
        self.input_data = TextInput(pygame.Rect(0, 600, 200, 50), "Entry", True)
        self.start_button = Button(pygame.Rect(700, 600, 200, 50), "START", 1)

    def check_active(self, mpos, c):
        self.input_data.check_active(mpos, c)
        self.start_button.check_active(mpos, c)

    def write(self, e):
        self.input_data.write(e)

    def update(self):
        self.input_data.start_menu_update()

    def draw(self):
        self.input_data.draw()
        self.start_button.draw()

