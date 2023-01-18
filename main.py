import pygame
import cv2 
import numpy as np
import os
import sys
import camera

os.environ['SDL_VIDEO_CENTERED'] = '1'

padding_x = 75
padding_y = 25

screen_size = (1280, 720) # 720p

pygame.init()

FPS_FONT = pygame.font.SysFont(None, 24)

camera = camera.Camera(1, screen_size, "RGB")
clock = pygame.time.Clock()

screen = pygame.display.set_mode(screen_size)


def main():
    camera.start()

    while True:
        # renders camera feed
        camera.get_surface(dest_surf=screen)

        clock.tick(30)
        fps_image = FPS_FONT.render("Fps: " + str(int(clock.get_fps())), True, "#000000")
        screen.blit(fps_image, (screen_size[0] - padding_x, padding_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                camera.stop()
                sys.exit()



if __name__ == '__main__':
    main()
