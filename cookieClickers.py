
#cookie clickers
#by: emre cagin
import pygame
import sys
from pygame.locals import *
import time
from threading import Thread, Event
import math

class Cookie:

    x = 700
    
    def __init__(self, price, owned, cps, y_position, base_price):
        self.price = price
        self.owned = owned
        self.cps = cps
        self.y = y_position
        self.base_price = base_price

class CookieClickers:
		
	def __init__(self):
		pygame.init()
		pygame.font.init()
		pygame.display.set_caption("Cookie Clickers")
		
		self.bg_color = (255,255,255)
		self.brown = (255,222,173)
		red = (255,0,0)
		self.black = (0,0,0)
		self.white = (255,255,255)
		
		self.cookies = [Cookie(15,0,0.1,150,15), Cookie(100,0,1,170,100), Cookie(1100,0,8,190,1100), Cookie(12000,0,47,210,12000), Cookie(130000,0,260,230,130000)]
		
		self.cookie_wrapper = [] 
		self.cookie_wrapper.append(0)  # cookie number
		self.cookie_wrapper.append(0) # cookie per second increment
		
		self.quit_event = Event()
		self.thread = Thread(target = self.threaded_function, args = (self.cookie_wrapper, self.quit_event))
		self.thread.start()
		
	def threaded_function(self, cookie_wrapper, quit_event):
		while True:
			if quit_event.wait(0):
				break
			cookie_wrapper[0] += cookie_wrapper[1]
			time.sleep(1)
	        
	def dec_cookie_cnt(self, count):
		self.cookie_wrapper[0] -= count

	def inc_cookie_cnt(self, count):
		self.cookie_wrapper[0] += count

	def inc_cookie_per_sec_cnt(self, count):
		self.cookie_wrapper[1] += count
	
	def display_shop_content(self, visible):
		my_font = pygame.font.SysFont("comicsans", 30)
		label = []
		x_back = 1050
		y_back = 700
		
		if not visible:
			for c in range(0, 5):
				label.append(my_font.render(" ", 1, self.white))
			self.backImage.set_alpha(0)
		else:
			for c in range(0, 5):
				label.append(my_font.render(str("CPS + "+ str(self.cookies[c].cps)+ " PRICE: " + str("%1.f" % self.cookies[c].price + str(" No of items: " + str(self.cookies[c].owned)))), 1, self.black))
				self.screen.blit(label[c], (self.cookies[c].x, self.cookies[c].y))
			self.backImage.set_alpha(255)

		self.screen.blit(self.backImage,(x_back,y_back))			
	
	def adjust_cookie_values(self, seq):
		self.inc_cookie_per_sec_cnt(self.cookies[seq].cps)
		self.cookies[seq].owned += 1
		self.dec_cookie_cnt(self.cookies[seq].price)
		self.cookies[seq].price += self.cookies[seq].base_price * (1.15 ** self.cookies[seq].owned) - self.cookies[seq].price
	
	def run(self):	
		shop_visible = False
		my_font = pygame.font.SysFont("comicsans", 30)
		w = 1200
		h = 800 
		x_cookie = 300
		y_cookie = 200
		x_shop = 600
		y_shop = 600
		
		
		self.screen = pygame.display.set_mode((w, h))
		self.backImage = pygame.image.load("back button.jpeg").convert()
		cookieImage = pygame.image.load("cookie.png").convert()
		shopImage = pygame.image.load("shop image.png").convert()
		self.backImage.set_colorkey(self.white)
		cookieImage.set_colorkey(self.white)
		shopImage.set_colorkey(self.white)
				
		
		while True:
		    
			self.screen.fill(self.white)
			self.screen.blit(cookieImage,(x_cookie,y_cookie))
			self.screen.blit(shopImage,(x_shop,y_shop))
			self.display_shop_content(shop_visible)                                    
			label = my_font.render(str("Cookies: " + str("%.1f"% self.cookie_wrapper[0])),1,(0,0,0))
			label_cps = my_font.render(str("CPS: " + str("%.1f"% self.cookie_wrapper[1])),1,(0,0,0))
			self.screen.blit(label,(350,50))
			self.screen.blit(label_cps,(350,75))					
			pygame.display.update()

			pos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit_event.set()
					self.thread.join()
					pygame.quit()
					quit()
		            
				if event.type == pygame.MOUSEBUTTONUP:
					if pos[0] > 300 and pos[0] < 500 and pos[1] > 200 and pos[1] < 400:
						self.inc_cookie_cnt(1)
					elif pos [0] > 640 and pos[0] < 820 and pos[1] > 635 and pos[1] < 760:
						shop_visible = True
					elif shop_visible:
						if pos[0] > 1050 and pos[0] < 1150 and pos[1] > 700 and pos[1] < 775:
							shop_visible = False
						if pos[0] > 700 and pos[0] < 980 and pos[1] > 150 and pos[1] < 165 and self.cookie_wrapper[0] >= self.cookies[0].price:
							self.adjust_cookie_values(0)
						elif pos[0] > 700 and pos[0] < 980 and pos[1] > 170 and pos[1] < 185 and self.cookie_wrapper[0] >= self.cookies[1].price:
							self.adjust_cookie_values(1)
						elif pos[0] > 700 and pos[0] < 980 and pos[1] > 190 and pos[1] < 205 and self.cookie_wrapper[0] >= self.cookies[2].price:
							self.adjust_cookie_values(2)
						elif pos[0] > 700 and pos[0] < 980 and pos[1] > 210 and pos[1] < 225 and self.cookie_wrapper[0] >= self.cookies[3].price:
							self.adjust_cookie_values(3)
						elif pos[0] > 700 and pos[0] < 980 and pos[1] > 230 and pos[1] < 245 and self.cookie_wrapper[0] >= self.cookies[4].price:
							self.adjust_cookie_values(4)
		
 
if  __name__ == "__main__": 
	cookie_game = CookieClickers()
	cookie_game.run()

