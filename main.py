import pygame
import turing

# circles
circle = turing.Circle(250, 250, 50, "q0")
circle2 = turing.Circle(500, 250, 50, "q1")
# arrow to connect
arrow = turing.Line(0, 0, 0, 0)
# line that divide screen
divide_line = turing.Line(0, 0, 0, 0)
# head that is moving between areas
head = turing.Head(0, 510, 40, 510, 20, 530)
# on start calculate arrow to connect
arrow.calculate(circle.ret_rect(), circle.ret_r(), circle2.ret_rect(), circle2.ret_r())
# on start calculate line to divide
divide_line.calculate(pygame.Rect(0, 500, 0, 0), 0, pygame.Rect(1000, 500, 0, 0), 0)

vertical_divide_line = turing.Line(700, 0, 700, 500)

# areas
areas = []
# creating areas
for i in range(0, 25):
    areas.append(turing.Area(i * 40, i, 0))

textBox = turing.TextInput(pygame.Rect(100, 600, 200, 50), "Write")
button = turing.Button(pygame.Rect(100, 675, 20, 20), "+")

while turing.running:
    for event in pygame.event.get():
        # to quit event
        if event.type == pygame.QUIT:
            turing.running = False

        if event.type == pygame.KEYDOWN:
            # escape as quit
            if event.key == pygame.K_ESCAPE:
                turing.running = False
            textBox.write(event)

    # testing if mouse is in circle
    circle.mouse_in(pygame.mouse.get_pos())
    circle2.mouse_in(pygame.mouse.get_pos())
    textBox.mouse_in(pygame.mouse.get_pos())
    button.mouse_in(pygame.mouse.get_pos())

    # checking mouse keys
    click = pygame.mouse.get_pressed()
    circle.check_mouse(click)
    circle2.check_mouse(click)
    textBox.check_mouse(click)
    button.check_mouse(click)

    # moving circles and calculate line
    circle.move(pygame.mouse.get_pos(), circle2.ret_rect())
    circle2.move(pygame.mouse.get_pos(), circle.ret_rect())
    arrow.calculate(circle.ret_rect(), circle.ret_r(), circle2.ret_rect(), circle2.ret_r())

    # fill screen with black color
    turing.screen.fill((0, 0, 0))

    # drawing circles and line between
    circle.draw()
    circle2.draw()
    arrow.draw()

    # drawing divide line and head over areas
    divide_line.draw()
    head.draw()
    for a in areas:
        a.draw()
    vertical_divide_line.draw()

    textBox.draw()
    button.draw()
    # just display
    pygame.display.flip()
    # quit if running is False
pygame.quit()
