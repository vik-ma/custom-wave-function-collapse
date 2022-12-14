import pygame


class InfoText():
    def __init__(self, x, y, main_text, main_text_font, main_text_color, hover_box, hover_box_group):
        self.x = x
        self.y = y
        self.main_text = main_text
        self.main_text_font = main_text_font
        self.rect = pygame.Rect(self.x, self.y, self.main_text_font.size(main_text)[0], self.main_text_font.size(main_text)[1])
        self.render_main_text = self.main_text_font.render(main_text, True, main_text_color)
        self.hover_box = hover_box
        self.hover_box_group = hover_box_group
        self.is_showing_hover_box = False

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.render_main_text, (self.x, self.y))

        if self.rect.collidepoint(pos):
            self.hover_box.update_image(pos[0], pos[1])
            self.hover_box_group.add(self.hover_box)
            self.is_showing_hover_box = True
        else:
            if self.is_showing_hover_box:
                self.hover_box_group.remove(self.hover_box)
                self.is_showing_hover_box = False
