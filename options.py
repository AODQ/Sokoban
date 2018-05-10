import pygame

class Option:
    hovered = False

    def __init__(self, text, x, y, font):
        self.text = text
        self.pos = (x, y)
        self.font = font
        self.set_rect()

    def get_color(self):
        if self.hovered:
            return (124, 112, 218)
        else:
            return (65, 65, 65)

    def set_rend(self):
        self.rend = self.font.render(self.text, False, self.get_color())

    def draw(self, window):
        self.set_rend()
        window.blit(self.rend, self.rect)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect(center=self.pos)


def draw(window, options):
    for opt in options:
        opt.hovered = opt.rect.collidepoint(pygame.mouse.get_pos())
        opt.draw(window)

def choice(options):
    for opt in options:
        mouse_pos = pygame.mouse.get_pos()
        if opt.rect.collidepoint(mouse_pos):
            return opt.text
    return None