from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import time


class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)
    def updte(self):
        self.image.x -= 1 * params.scale
        self.image_dupe.x -= *

class HelloWorld(FloatLayout):
    def __init__(self, **kwargs):
        super(HelloWorld, self).__init__(**kwargs)

        btn1 = Button(text="START GAME", font_size=34, size_hint=(.2,.2), pos_hint={'x':.4,'y':.4})
        btn1.bind(on_press=self.hello)
        self.add_widget(btn1)


    def hello(self, obj):
        print("--> Hello at time %s" % time.ctime())
        self.sfx_intro = SoundLoader.load('sound/intro2.wav')
        self.sfx_intro.stop()
        self.sfx_intro.play()

class Game(FloatLayout):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        btn1 = Button(text="This Game is ON", font_size=24, size_hint=(.2,.2), pos_hint={'x':.4,'y':.4})
        btn1.bind(on_press=self.hello)
        self.add_widget(btn1)




class HelloWorldApp(App):
    def build(self):
        return HelloWorld()

if __name__ == "__main__":
    myApp = HelloWorldApp()
    print("myApp name is %s" % myApp.name)
    myApp.run()

'''
class IntroScreen(FloatLayout):
    startbutton = Button(text='Start Game', font_size = 14)



class BallGame(Widget):
    #start = IntroScreen()
    pass

class BallApp(App):
    def build(self):
        return IntroScreen()


if __name__ == '__main__':
    BallApp().run()

'''


