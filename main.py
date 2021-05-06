from pygame import *
from random import randint

mixer.init()
font.init()
font1 = font.SysFont('Arial', 50)
font2 = font.SysFont('Arial', 70)

win_width = 1024
win_height = 800

x1 = 512
y1 = 650

score = 0 
lost = 0

Next = False

window = display.set_mode((win_width,win_height))
display.set_caption('Космос')
background = transform.scale(image.load('bin/galaxy.jpg'),(win_width,win_height))

mixer.music.load('bin/space.ogg')
#mixer.music.play()

game = True
finish = False


clock  = time.Clock()

class GameSprite(sprite.Sprite):
	def __init__(self,image_player,player_x,player_y,player_speed):
		super().__init__()
		self.image = transform.scale(image.load(image_player),(100,100))
		self.speed = player_speed
		self.rect = self.image.get_rect()
		self.rect.x = player_x
		self.rect.y = player_y


	def reset(self):
		window.blit(self.image, (self.rect.x , self.rect.y))

class Hero(GameSprite):
	def update(self):
		global x1
		keys = key.get_pressed()
		if keys[K_a] and self.rect.x >= 5:
			self.rect.x -= self.speed
		elif keys[K_d] and self.rect.x <= win_width-80:
			self.rect.x += self.speed

		x1 = self.rect.x

class Enemy(GameSprite):
	derection = 'down'
	def update(self):
		global score , lost
		if self.rect.y < 500:
			self.derection = 'down'

		if self.rect.y > win_height:
			self.derection = 'up'
			lost += 1

		if self.derection == 'up':
			self.rect.y = 0 
			self.rect.x = randint(50,970)
			self.speed = randint(2,5)
		else:
			self.rect.y += self.speed

class Bullet(sprite.Sprite):
	def __init__(self,image_player,player_x,player_y,player_speed):
		super().__init__()
		self.image = transform.scale(image.load(image_player),(30,30))
		self.speed = player_speed
		self.rect = self.image.get_rect()
		self.rect.x = player_x
		self.rect.y = player_y
	
	def update(self):
		self.rect.y -= self.speed

	def draw(self):
		window.blit(self.image,(self.rect.x,self.rect.y),self.speed)

hero = Hero('bin/rocket.png',x1,y1,10)

monsters = sprite.Group()

for i in range(6):
	enemy = Enemy('bin/ufo.png',randint(50,970),10,randint(2,5))
	monsters.add(enemy)

bullets = sprite.Group()

while game:
	clock.tick(60)

	for e in event.get():
		if e.type == QUIT:
			game = False
		if e.type == KEYDOWN:
			if e.key == K_r:
				finish = False
				hero.rect.x = 512
				hero.rect.y = 650
				for i in monsters:
					i.kill()
				lost = 0
				score = 0
			if Next == True:
				if e.key == K_o:
					import lvl2
					lvl2.start()

	if finish != True:
		window.blit(background,(0,0))

		hero.reset()
		hero.update()

		monsters.draw(window)
		monsters.update()

		bullets.draw(window)
		bullets.update()

		for bullet in bullets:

			if bullet.rect.y > win_width:
				bullets.pop(bullets.index(bullet))


		keys = key.get_pressed()

		if keys[K_SPACE]:

			bullets.add(Bullet('bin/bullet.png',x1,y1,5))


		text_score = font1.render("Счёт: "+str(score),True,(255,0,0))
		text_lost = font1.render("Пропущено: "+str(lost),True,(255,0,0))

		window.blit(text_score, [20,20])
		window.blit(text_lost, [20,60])

		if sprite.groupcollide(bullets,monsters,True,True):
			score += 1
			text_score = font1.render("Счёт: "+str(score),True,(255,0,0))

		if len(monsters) < 6:

			enemy = Enemy('bin/ufo.png',randint(50,970),10,randint(2,5))
			monsters.add(enemy)

		if score == 30:
			win = font2.render("Первый уровень пройден!",True,(255,0,0))
			window.blit(win, [250,300])
			win3 = font2.render("Нажмите O что бы продолжить.",True,(255,0,0))
			window.blit(win3, [180,400])
			finish = True
			hero.rect.x = 512
			hero.rect.y = 650
			for i in monsters:
				i.kill()
			lost = 0
			score = 0
			Next = True


		if lost >= 3:
			win = font2.render("ВЫ ПРОИГРАЛИ",True,(255,0,0))
			win3 = font2.render("Нажмите R что бы начать заново.",True,(255,0,0))
			window.blit(win3, [200,400])
			window.blit(win, [250,300])
			finish = True

	display.update()
