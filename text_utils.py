import pygame

def create_outlined_text(text, font, text_color, outline_color):
    outline_surfaces = []
    offset = 2
    positions = [
        (-offset,-offset), (-offset, 0), (-offset,offset), 
        (0, -offset), (0, offset), 
        (offset,-offset), (offset, 0), (offset,offset)
    ]
    for dx, dy in positions:
        outline_surface = font.render(text, True, outline_color)
        outline_rect = outline_surface.get_rect()
        outline_rect.x = dx
        outline_rect.y = dy
        outline_surfaces.append((outline_surface, outline_rect))
    
    text_surface = font.render(text, True, text_color)
    return outline_surfaces, text_surface

def draw_outlined_text(screen, text, font, position, text_color="white", outline_color="black"):
    outline_surfaces, text_surface = create_outlined_text(text, font, text_color, outline_color)
    x, y = position
    for outline_surface, outline_rect in outline_surfaces:
        screen.blit(outline_surface, (x + outline_rect.x, y + outline_rect.y))
    screen.blit(text_surface, (x, y))

def draw_outlined_text_centered(screen, text, font, position, text_color="white", outline_color="black"):
    outline_surfaces, text_surface = create_outlined_text(text, font, text_color, outline_color)
    text_rect = text_surface.get_rect(center=position)    
    for outline_surface, outline_rect in outline_surfaces:
        new_rect = outline_surface.get_rect(center=position)
        new_rect.x += outline_rect.x
        new_rect.y += outline_rect.y
        screen.blit(outline_surface, new_rect)
    screen.blit(text_surface, text_rect)