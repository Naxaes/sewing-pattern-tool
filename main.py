import csv
import pygame
pygame.init()

font = pygame.font.SysFont('Arial', 18)

BLACK = pygame.Color(0,     0,   0)
WHITE = pygame.Color(255, 255, 255)
PINK  = pygame.Color(255,   0, 255)


class Square:
    COLOR_CHOICES = {
        'BLANC': pygame.Color('#eff0f2'),
        '7715':  pygame.Color('#b8bcc8'),
        'Noir':  pygame.Color('#090a0c'),
        '7624':  pygame.Color('#302f35'),
        '7713':  pygame.Color('#2b333d'),
    }
    COLOR_LIST = tuple(COLOR_CHOICES.values())  # Guaranteed to be ordered in Python 3.6

    def __init__(self, id):
        self.id    = id
        self.color = Square.COLOR_LIST[id]


class Pattern:
    def __init__(self, squares):
        self.columns = len(squares[0])
        self.rows    = len(squares)
        self.square_width  = 5
        self.square_height = 5
        self.squares = squares
        self.surface = pygame.Surface((self.columns * self.square_width, self.rows * self.square_height))

    def position_to_tile_coordinates(self, x, y):
        x //= self.square_width
        y //= self.square_height
        return x, y

    def recolor(self, x, y, color):
        tile_x, tile_y = self.position_to_tile_coordinates(x, y)
        try:
            pressed_square = self.squares[tile_x][tile_y]
        except IndexError:
            return

        for i, row in enumerate(self.squares):
            for j, square in enumerate(row):
                if square.id == pressed_square.id:
                    square.color = color

    def draw(self):
        for i, row in enumerate(self.squares):
            for j, square in enumerate(row):
                position = (i * self.square_width, j * self.square_height)
                size     = (self.square_width, self.square_height)
                pygame.draw.rect(self.surface, square.color, (position, size))


def draw_palette(surface):
    for i, (name, color) in enumerate(Square.COLOR_CHOICES.items()):
        # Draw the color next to each other.
        size = (surface.get_width() // len(Square.COLOR_CHOICES), surface.get_height())
        position = (i * size[0], 0)
        pygame.draw.rect(surface, color, (position, size))

        # Draw and left-align text.
        text = font.render(name, True, BLACK)
        x = position[0] + 4  # Add some padding.
        y = (size[1] // 2 - text.get_height()  // 2)
        surface.blit(text, (x, y))

    # Draw a small line of white to separate the pattern from the palette.
    pygame.draw.line(surface, WHITE, (0, 0), (surface.get_width(), 0))


def draw_highlight(surface, i):
    size = (surface.get_width() // len(Square.COLOR_CHOICES), surface.get_height())
    position = (i * size[0], 0)
    pygame.draw.rect(surface, PINK, (position, size), 2)


def hovering_over_surface(surface):
    x, y = pygame.mouse.get_pos()



def main():
    # Create the pattern.
    with open('pattern.csv', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        values = list(reader)
    pattern = Pattern([[Square(id=int(value) - 1) for value in row] for row in values])

    # Create the palette.
    palette_surface = pygame.Surface((pattern.surface.get_width(), 50))
    draw_palette(palette_surface)
    draw_highlight(palette_surface, 0)

    # To showcase the selected color.
    selected_color = Square.COLOR_LIST[0]

    # Make the screen the size of the pattern and the palette.
    screen = pygame.display.set_mode((pattern.surface.get_width(), pattern.surface.get_height() + palette_surface.get_height()))
    clock  = pygame.time.Clock()

    # Main loop to keep the application running.
    running = True
    while running:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 0 <= x <= pattern.surface.get_width() and 0 <= y <= pattern.surface.get_height():
                    pattern.recolor(x, y, selected_color)
                elif 0 <= x <= palette_surface.get_width() and pattern.surface.get_height() <= y <= pattern.surface.get_height() + palette_surface.get_height():
                    x //= (palette_surface.get_width() // len(Square.COLOR_LIST))
                    try:
                        selected_color = Square.COLOR_LIST[x]
                        draw_palette(palette_surface)
                        draw_highlight(palette_surface, x)
                    except IndexError:
                        pass

        pattern.draw()
        screen.blit(pattern.surface, (0, 0))

        screen.blit(palette_surface, (0, pattern.surface.get_height()))
        pygame.display.update()


if __name__ == '__main__':
    main()
