import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont("comicsansms", 30)
font2 = pygame.font.SysFont("comicsansms", 60)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

running = True


class Circle:
    def __init__(self, x, y, r, name):
        # circle init
        self.rect = pygame.Rect(x - r, y - r, 2 * r, 2 * r)
        self.pos = (x, y)
        self.r = r
        # animating and moving circle
        self.moving = False
        self.inside = False
        self.active = False
        # name on circle
        self.name = name
        self.t = None
        # lists of algorythm things
        self.to_render = None
        self.on_c_list = []
        self.write_list = []
        self.move_list = []
        self.change_list = []
        # UI
        self.on_c_textinput = TextInput(pygame.Rect(0, 600, 50, 50), "On", False)
        self.write_textinput = TextInput(pygame.Rect(110, 600, 50, 50), "Write", False)
        self.move_textinput = TextInput(pygame.Rect(260, 600, 50, 50), "Move", False)
        self.change_state_textinput = TextInput(pygame.Rect(410, 600, 50, 50), "Change state", False)
        self.button = Button(pygame.Rect(660, 600, 50, 50), "+", 2)
        self.input_error = font.render("Complete all fields", True, RED)
        # check all inputs is entered
        self.draw_error = False
        self.on_c_entered = False
        self.write_entered = False
        self.move_entered = False
        self.change_state_entered = False

    def ret_active(self):
        return self.active, self.moving

    def draw_UI(self):
        self.on_c_textinput.draw()
        self.write_textinput.draw()
        self.move_textinput.draw()
        self.change_state_textinput.draw()
        self.button.draw()
        if self.draw_error:
            screen.blit(self.input_error, (720, 600))

    def draw(self):
        pygame.draw.circle(screen, BLUE, self.pos, self.r)
        self.t = font.render(self.name, True, WHITE)
        screen.blit(self.t,
                    (self.rect.x + self.r - self.t.get_width() / 2, self.rect.y + self.r - self.t.get_height() / 2))
        if self.moving:
            pygame.draw.circle(screen, RED, self.pos, self.r, 10)
            self.draw_UI()
        elif not self.moving and self.active:
            pygame.draw.circle(screen, YELLOW, self.pos, self.r, 10)
            self.draw_UI()

        if len(self.write_list) > 0 and (self.moving or (not self.moving and self.active)) and not self.draw_error:
            for i in range(0, len(self.write_list)):
                self.to_render = font.render(
                    str('ON: ' + self.on_c_list[i] + ' W: ' + self.write_list[i] + ' M: ' + self.move_list[i] + ' S: ' +
                        self.change_list[i]), True, WHITE)
                screen.blit(self.to_render, (705, i * self.to_render.get_height() + 5))

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
        self.on_c_textinput.check_active(mpos, c)
        self.on_c_textinput.write(e)

        self.write_textinput.check_active(mpos, c)
        self.write_textinput.write(e)

        self.move_textinput.check_active(mpos, c)
        self.move_textinput.write(e)

        self.change_state_textinput.check_active(mpos, c)
        self.change_state_textinput.write(e)

        self.draw_error = False

        self.write_entered = False
        self.move_entered = False
        self.change_state_entered = False

        if self.button.check_active(mpos, c):
            if self.on_c_textinput.ret_len() > 0:
                self.on_c_entered = True
            if self.write_textinput.ret_len() > 0:
                self.write_entered = True
            if self.move_textinput.ret_len() > 0:
                self.move_entered = True
            if self.change_state_textinput.ret_len() > 0:
                self.change_state_entered = True

            if self.on_c_entered and self.write_entered and self.move_entered and self.change_state_entered:
                self.on_c_list.append(self.on_c_textinput.ret_text())
                self.write_list.append(self.write_textinput.ret_text())
                self.move_list.append(self.move_textinput.ret_text())
                self.change_list.append(self.change_state_textinput.ret_text())
            else:
                self.draw_error = True

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

    def ret_lists(self):
        return self.on_c_list, self.write_list, self.move_list, self.change_list


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.start_pos = (x1, y1)
        self.end_pos = (x2, y2)

    def calculate(self, rect1, r1, rect2, r2):
        self.start_pos = (rect1.x + rect1.w, rect1.y + r1)
        self.end_pos = (rect2.x, rect2.y + r2)

    def draw(self):
        pygame.draw.line(screen, WHITE, self.start_pos, self.end_pos, 5)


class Area:
    def __init__(self, x, id, num):
        self.t = None
        self.rect = pygame.Rect(x, 540, 40, 40)
        self.id = id
        self.num = num

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, 5)
        if self.id == 0 or self.id == 24:
            self.t = font.render("#", True, RED)
            screen.blit(self.t, (self.rect.x + self.t.get_width() / 3, 530 + self.t.get_height() / 5))
        else:
            self.t = font.render(str(self.num), True, RED)
            screen.blit(self.t,
                        (self.rect.x + 20 - (self.t.get_width() / 2), self.rect.y + 20 - (self.t.get_height() / 2)))

    def ret_c(self):
        return str(self.num)

    def set_c(self, c):
        self.num = c


class Head:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def draw(self):
        pygame.draw.polygon(screen, WHITE, ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)))

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
        self.text_tex = font.render(self.text, True, WHITE)
        self.active = False
        self.label_tex = font.render(label, True, WHITE)
        self.start = start
        self.color = None

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
            self.color = RED
        elif not self.active:
            self.color = WHITE

        pygame.draw.rect(screen, self.color, (self.rect.x + self.label_tex.get_width() + 10,
                                              self.rect.y, self.rect.w, self.rect.h), 1)
        self.text_tex = font.render(self.text, True, WHITE)
        screen.blit(self.text_tex, (self.rect.x + 28 + self.label_tex.get_width(), self.rect.y + 1))

    def ret_text(self):
        return self.text

    def ret_len(self):
        return len(self.text)

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
            self.text_tex = font.render(text, True, BLACK)
        elif self.font_size == 2:
            self.text_tex = font2.render(text, True, BLACK)

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
            pygame.draw.rect(screen, RED, self.rect, 255)
        else:
            pygame.draw.rect(screen, WHITE, self.rect, 255)

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
        self.to_draw = True

    def check_active(self, mpos, c):
        self.input_data.check_active(mpos, c)
        if self.start_button.check_active(mpos, c) and len(self.input_data.ret_text()) > 0:
            return True
        else:
            return False

    def write(self, e):
        self.input_data.write(e)

    def update(self):
        self.input_data.start_menu_update()

    def set_to_draw(self, s):
        self.to_draw = s

    def draw(self):
        if self.to_draw:
            self.input_data.draw()
            self.start_button.draw()

    def ret_input_data(self):
        return list(self.input_data.ret_text())


class Timer:
    def __init__(self, n):
        self.n = n
        self.tick_start = 0

    def start_timer(self):
        self.tick_start = pygame.time.get_ticks()

    def check(self):
        if pygame.time.get_ticks() - self.tick_start >= self.n:
            return True
        return False


class Algorithm:
    def __init__(self):
        self.timer = Timer(1000)
        self.start = False
        self.current_area_id = 1
        self.current_circle_id = 0

    def start_algorithm(self, areas_list, areas_entry):
        print(areas_entry)
        for i in range(0, len(areas_entry)):
            areas_list[i + 1].set_c(areas_entry[i])
        self.timer.start_timer()

    def do_algorithm(self, areas_list, circles_list):
        pass
        # print(areas_list[self.current_area_id].ret_c())
