import kivy

from kivy.core.window import Config
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.metrics import Metrics


import random
import math

class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

class Menu(FloatLayout):
    def __init__(self):
        super(Menu, self).__init__()
        #self.add_widget(Background(source='images/backgrnd2.png'))
        self.canvas.add(Color(1,1,1,1))
        self.canvas.add(Rectangle(pos=((40),0),size=((1330),(800))))

        #self.size = self.children[0].size
        #btn1 = Button(text="START GAME", font_size=34, size_hint=(.2,.2), pos_hint={'x':.4,'y':.4})
        btn1 = Button(text="START GAME", font_size=(34), size=((400),(200)), pos=((500),(300)))
        btn1.bind(on_press=self.gotogame)
        self.add_widget(btn1)
        self.canvas.add(Color(1,0,0,1))
        self.canvas.add(Rectangle(pos=(0,0), size=((30),(Window.height))))
        self.canvas.add(Rectangle(pos=((1380),0), size=((30),(800))))

        self.size = self.children[0].size
        #self.add_widget(Blank(*params.blank_rect))
        self.sound = SoundLoader.load('audio/intro2.wav')
        self.sound.loop=True
        self.sound.volume = 1
        self.sound.play()
        


    def gotogame(self, *ignore):
        self.sound.stop()
        self.sound2 = SoundLoader.load('audio/bounce.wav')
        self.sound2.stop()
        self.sound2.play()
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Game())





class Background(Sprite):
    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        
        self.allow_stretch = True
        self.size = 1310, 800
        self.pos = 40,0


class Guy(Sprite):
    def __init__(self, pos):
        super(Guy, self).__init__(source='images/guyball.png', pos=pos)
        self.allow_stretch = True
        self.size = (48,48)
        self.speed = 4
        self.theta = random.uniform(3.3,4.3)
        self.xdir = math.cos(self.theta)
        self.ydir = math.sin(self.theta)
        self.velocity_y = self.ydir*self.speed
        self.velocity_x = self.xdir*self.speed
        self.rotdir = 1 
        self.thetad = self.theta+(self.rotdir*(3.14159/2))
        self.onball = False


    def update(self):
        self.velocity_y = self.speed*self.ydir
        self.velocity_x = self.speed*self.xdir
        self.y += self.velocity_y
        self.x += self.velocity_x

        if (self.y < 0):
            self.ydir *= -1
        if(self.top > 800):
            self.ydir *= -1

        if(self.x < 30):
            self.xdir *= -1
        if(self.right > 1380):
            self.xdir *= -1


        #self.theta = math.atan(self.ydir/self.xdir)


    def on_touch_down(self, *ignore):
        pass


class Ball(Sprite):
    def __init__(self, pos):
        super(Ball, self).__init__(source='images/normball.png', pos=pos)
        self.balcol = random.randrange(0,18)
        if self.balcol > 17:
            self.source='images/redball.png'
        if self.balcol < 2:
            self.source='images/greenball.png'
        self.allow_stretch = True
        self.size = (116, 116)
        self.speed = -2

    def update(self, speed):

        self.x += speed*-1
        self.y += random.randrange(-2,3)

        if self.right < -10:
            self.parent.remove_widget(self)

class Balls(Sprite):
    add_ball = 0

    def update(self, dt, speed):
        for child in list(self.children):
            child.update(speed)
        
        self.add_ball -= dt
        
        if self.add_ball < 0:
            y = (random.random()*650+25)
            self.add_widget(Ball(pos=(Window.width+50,y)))
            self.add_ball = 3/speed


class Ends(Widget):
    def __init__(self, pos):
        super(Ends, self).__init__(pos=pos)
        self.hits = 0

        self.canvas.add(Color(0,0,0,1))
        self.canvas.add(Rectangle(pos=pos, size=(30,800)))

        # rect = InstructionGroup()
        # rect.add(Color(1,1,0,1))
        # rect.add(Rectangle(pos=pos, size = (30,800)))
        # self.canvas.add(rect)


        # with self.canvas:
        #     self.col = Color(0, 0, 0, 1)
        #     self.rect = Rectangle(pos=pos, size = (30,800))

    def HitEnd(self):
        print("HIT END")
        self.hits += 1
        if self.hits == 1:
            self.canvas.add(Color(0,1,0,1))
            self.canvas.add(Rectangle(pos=self.pos, size=(30,800)))
            return False
        if self.hits == 2:
            self.canvas.add(Color(1,1,0,1))
            self.canvas.add(Rectangle(pos=self.pos, size=(30,800)))
            return False
        if self.hits == 3:
            self.canvas.add(Color(1,0,0,1))
            self.canvas.add(Rectangle(pos=self.pos, size=(30,800)))
            return False
        if self.hits == 4:
            return True

        #rect.add(Color(1,0,0,1))
        #self.canvas.add(Color(1,0,0,1))
        #self.canvas.add(Rectangle(pos=self.pos, size=(30,800)))




class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.size = (1400, 800)
        self.gamespeed = 1
        #self.add_widget(Background(source='images/backgrnd2.png'))
        self.canvas.add(Color(1,1,1,1))
        self.canvas.add(Rectangle(pos=(40,0),size=(self.width-70,self.height)))
        self.end1 = Ends(pos=(0,0))
        self.end2 = Ends(pos=(1380,0))
        self.add_widget(self.end1)
        self.add_widget(self.end2)
        self.balls = Balls(pos=(self.width+50, (random.randint(0,18)*40+10) ), speed = self.gamespeed)

        self.add_widget(self.balls)



        self.guy = Guy(pos=((random.randint(200,600)), (random.randint(200,600))))
        self.add_widget(self.guy)
        self.score = 0
        self.score_label = Label(pos=(200,10),opacity=1,text="[color=111111]SCORE:%s" % self.score, markup=True)
        self.add_widget(self.score_label)

        Clock.schedule_interval(self.update, 1.0/60.0)

        Clock.schedule_interval(self.speedincrease, 7.0)
        self.game_over = False

        if self.game_over == False:

            Clock.schedule_interval(self.scoreincrease, 0.1)
        



    def update(self, dt):
        if self.game_over:
            self.bind(on_touch_down=self._on_touch_down)


        self.guy.update()
        self.balls.update(dt, self.gamespeed)

        for ball in self.balls.children:
            if ball.collide_widget(self.guy):
                if math.sqrt((ball.center[0]-self.guy.center[0])**2+(ball.center[1]-self.guy.center[1])**2) < 76:
                    print("I've hit a ball")
                    if ball.source=='images/redball.png':
                        self.game_over = True
                    if ball.source=='images/greenball.png':
                        if max(abs(self.guy.xdir),abs(self.guy.ydir)) == self.guy.xdir:
                            self.guy.xdir *= -1
                        else:
                            self.guy.ydir *= -1
                else:
                    pass


        if self.guy.x < 30:
            self.game_over = self.end1.HitEnd()
        if self.guy.right > 1380:
            self.game_over = self.end2.HitEnd()

    def speedincrease(self, *ignore):
        self.gamespeed += .4
        
        self.guy.speed = self.gamespeed*2

    def scoreincrease(self, *ignore):
        self.score +=1
        self.score_label.text="[color=111111]SCORE:%s" % self.score

    def _on_touch_down(self, *ignore):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Menu())




class GameApp(App):
    def build(self):
        #params.init()

        top = Widget()
        top.add_widget(Menu())
        return top




if __name__ == '__main__':

    GameApp().run()
