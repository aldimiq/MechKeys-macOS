import pygame
import os

def create_menubar_icon():
    # macOS menu bar icons are typically 22x22 points (so 44x44 pixels for retina)
    # But usually providing a larger one works fine as it scales down.
    # Let's target 44x44 pixels.
    size = 44
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Template icons should be black/alpha. The system tints them.
    # Actually, for "Template" images:
    # - Opaque areas are colored by the system (usually black in light mode, white in dark mode).
    # - Transparent areas remain transparent.
    # So we should draw in SOLID BLACK (or any solid color, but black is standard for "content").
    
    CONTENT_COLOR = (0, 0, 0, 255) # Solid Black
    
    # 1. Background is already transparent
    surface.fill((0, 0, 0, 0))

    # Helper for rounded rect
    def draw_rounded_rect(surf, color, rect, radius, width=0):
        # If width=0 (fill), we draw filled shapes
        # If width>0 (outline), we draw lines (pygame 2.0.0+ supports border_radius in draw.rect)
        pygame.draw.rect(surf, color, rect, width, border_radius=radius)

    # 2. Keycap Outline
    margin = 4
    rect = pygame.Rect(margin, margin, size-2*margin, size-2*margin)
    
    # Draw outline
    draw_rounded_rect(surface, CONTENT_COLOR, rect, 8, width=3)
    
    # 3. Small "Switch" in center (Cross)
    center = (size//2, size//2)
    stem_w = 4
    stem_h = 16
    
    # Vertical bar
    v_rect = pygame.Rect(center[0] - stem_w//2, center[1] - stem_h//2, stem_w, stem_h)
    pygame.draw.rect(surface, CONTENT_COLOR, v_rect)
    
    # Horizontal bar
    h_rect = pygame.Rect(center[0] - stem_h//2, center[1] - stem_w//2, stem_h, stem_w)
    pygame.draw.rect(surface, CONTENT_COLOR, h_rect)

    # Save as Template image
    filename = "menubar_icon_Template.png"
    pygame.image.save(surface, filename)
    print(f"Icon created: {filename}")

if __name__ == "__main__":
    pygame.init()
    create_menubar_icon()
    pygame.quit()
