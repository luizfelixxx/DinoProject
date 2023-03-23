import pygame

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self, screen):
		action = False
		position = pygame.mouse.get_pos()

		if self.rect.collidepoint(position):
			if pygame.mouse.get_pressed()[0] and self.clicked == False:
				self.clicked = True
				action = True

		if not pygame.mouse.get_pressed()[0]:
			self.clicked = False

		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action