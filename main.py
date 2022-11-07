import pygame
import cv2 
import numpy as np
import os
import camera

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

camera = camera.Camera(0, (1920, 1080), "RGB")

def main():
    print("neil")

if __name__ == '__main__':
    main()
