import pygame
import os

def create_icon():
    size = 1024
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colors
    KEY_BASE = (40, 44, 52)       # Dark Grey
    KEY_SHADOW = (30, 33, 39)     # Darker Shadow
    SWITCH_HOUSING = (20, 20, 20) # Black
    STEM_COLOR = (0, 122, 204)    # Blue (MX Blue)
    
    # 1. Draw Background (Transparent)
    surface.fill((0, 0, 0, 0))

    # Helper to draw rounded rect
    def draw_rounded_rect(surf, color, rect, radius):
        pygame.draw.rect(surf, color, (rect.x + radius, rect.y, rect.width - 2*radius, rect.height))
        pygame.draw.rect(surf, color, (rect.x, rect.y + radius, rect.width, rect.height - 2*radius))
        pygame.draw.circle(surf, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(surf, color, (rect.x + rect.width - radius, rect.y + radius), radius)
        pygame.draw.circle(surf, color, (rect.x + radius, rect.y + rect.height - radius), radius)
        pygame.draw.circle(surf, color, (rect.x + rect.width - radius, rect.y + rect.height - radius), radius)

    # 2. Keycap Base (Outer)
    margin = 64
    base_rect = pygame.Rect(margin, margin, size-2*margin, size-2*margin)
    draw_rounded_rect(surface, KEY_BASE, base_rect, 180)
    
    # 3. Inner Dish (Slightly concave look)
    dish_margin = 140
    dish_rect = pygame.Rect(dish_margin, dish_margin, size-2*dish_margin, size-2*dish_margin)
    draw_rounded_rect(surface, KEY_SHADOW, dish_rect, 150)

    # 4. Switch Mechanism (The "Stem")
    center = (size//2, size//2)
    
    # Housing Circle
    pygame.draw.circle(surface, SWITCH_HOUSING, center, 220)
    
    # The Cross (+)
    stem_thickness = 90
    stem_length = 280
    
    # Vertical bar
    v_rect = pygame.Rect(center[0] - stem_thickness//2, center[1] - stem_length//2, stem_thickness, stem_length)
    # Horizontal bar
    h_rect = pygame.Rect(center[0] - stem_length//2, center[1] - stem_thickness//2, stem_length, stem_thickness)
    
    pygame.draw.rect(surface, STEM_COLOR, v_rect)
    pygame.draw.rect(surface, STEM_COLOR, h_rect)
    
    pygame.image.save(surface, "MechKeys.png")
    print("Icon created: MechKeys.png")

if __name__ == "__main__":
    pygame.init()
    create_icon()
    pygame.quit()
