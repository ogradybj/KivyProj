from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class OrbitBall(Widget):
    def __init__(self, **kwargs):
        super(OrbitBall, self).__init__(**kwargs)
        self.counter = NumericProperty(0)
        self.speed = NumericProperty(1)
        self.velocity_x = NumericProperty(0)
        self.velocity_y = NumericProperty(0)
        self.velocity = ReferenceListProperty(self.velocity_x, self.velocity_y)
        with self.canvas.after:
            self.color(.1,.1,.9,1)
            self.Ellipse(pos=self.pos, size=self.size)

    def move(self):
        self.counter += 1
        # if self.counter % 1200 == 0:
        #     self.speed += 1


        self.velocity.velocity_y = randint(-3,3)*self.speed
        self.velocity.velocity_x = self.speed*-1
        self.pos = Vector(*self.velocity) + self.pos
        print(self.pos)




class GuyBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    counter = NumericProperty(0)
    score = NumericProperty(0)
    speed = NumericProperty(1)


    def move(self):

        self.counter += 1
        if self.counter % 10 == 0:
            self.score += 1
        if self.counter % 100 == 0:
            self.speed += 1

        self.pos = Vector(*self.velocity)*self.speed + self.pos

#class mainMenu(Widget):
#
#    def __init__(self, app):
#        


class TangentGame(Widget):
    ball = GuyBall()#ObjectProperty(None)
    ballList = []

    for i in range(2):
        tempBall = OrbitBall()
        tempBall.center_x = i*100+400
        tempBall.center_y = randint(1,10)*10
        ballList.append(tempBall)
        
    # orbitball1 = ObjectProperty(None)
    # orbitball2 = ObjectProperty(None)
    # orbitball3 = ObjectProperty(None)

    def start_ball(self):#, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(4,0).rotate(randint(190,240))
        for i in range(len(self.ballList)):
            self.ballList[i].velocity = Vector(-3,0)
        # self.orbitball1.velocity = Vector(-3,0)
        # self.orbitball2.velocity = Vector(-3,0)

    def update(self, dt):
        self.ball.move()
        for i in range(len(self.ballList)):
            self.ballList[i].move()
        # self.orbitball1.move()
        # self.orbitball2.move()

        #self.ball.score += 1

        # bounce of paddles
        #self.player1.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if(self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        for i in range(len(self.ballList)):
            if(self.ballList[i].center_x < -100):
                self.ballList[i].center_x = 500
                self.ballList[i].center_y = randint(1,10)*10



        # went of to a side to score point?
        # if self.ball.x < self.x:
        #     self.player2.score += 1
        #     self.serve_ball(vel=(4, 0))
        # if self.ball.x > self.width:
        #     self.player1.score += 1
        #     self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        # if touch.x < self.width / 3:
        #     self.player1.center_y = touch.y
        # if touch.x > self.width - self.width / 3:
        #     self.player2.center_y = touch.y
        pass


class BallApp(App):
    def build(self):
        game = TangentGame()
        game.start_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    BallApp().run()



