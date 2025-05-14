import pygame

WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
FPS = 60

PALETTE = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 255), (255, 0, 255),
    (0, 0, 0)
]
PALETTE_RECT = pygame.Rect(0, 0, WIDTH, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Рисование и прямоугольники")
clock = pygame.time.Clock()

selected_color = (255, 0, 0)
circle_drawing = False
circle_points = []
rect_start = None
current_rect = None
rectangles = []

running = True
while running:
    screen.fill(WHITE)

    for i, color in enumerate(PALETTE):
        pygame.draw.rect(screen, color, (i * 50, 0, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if PALETTE_RECT.collidepoint(x, y):
                    selected_color = PALETTE[x // 50]
                else:
                    circle_drawing = True
                    circle_points.append((event.pos, selected_color))
            elif event.button == 3:
                rect_start = event.pos
                current_rect = pygame.Rect(rect_start[0], rect_start[1], 0, 0)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                circle_drawing = False
            elif event.button == 3 and current_rect:
                if abs(current_rect.width) > 5 and abs(current_rect.height) > 5:
                    rectangles.append((current_rect.copy(), selected_color))
                current_rect = None

        elif event.type == pygame.MOUSEMOTION and circle_drawing:
            x, y = event.pos
            if y > 50:
                circle_points.append(((x, y), selected_color))

    if pygame.mouse.get_pressed()[2] and rect_start:
        x, y = pygame.mouse.get_pos()
        width = x - rect_start[0]
        height = y - rect_start[1]
        current_rect.width = width
        current_rect.height = height

    for point, color in circle_points:
        pygame.draw.circle(screen, color, point, 10)

    for rect, color in rectangles:
        pygame.draw.rect(screen, color, rect, 2)

    if current_rect:
        pygame.draw.rect(screen, selected_color, current_rect, 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
