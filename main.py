# coding: utf-8

from kivymd.app import MDApp
from kivy_garden.mapview import MapView, MapMarker
from kivy.utils import platform
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from lib.filemanagment import FileManagment

userPosition = {'lat': -8.332996, 'lon': -36.416745}

class ScreenManagment(ScreenManager):
    pass


class LoginScreen(Screen):
    login = "italoph"
    password = "12345"

    fileManagment = FileManagment()

    def clickLogin(self):
        if self.ids.loginText.text == self.login and self.ids.passwordText.text == self.password:
            self.fileManagment.writeUserInfo(self.ids.loginText.text, self.ids.passwordText.text)
            self.manager.current = "mainscreen"


class MainScreen(Screen):

    def drawOnMap(self):
        pass

    def setStartPosition(self, dt):
        global userPosition
        self.ids.map.center_on(userPosition['lat'], userPosition['lon'])
        self.ids.localBus.lat = userPosition['lat']
        self.ids.localBus.lon = userPosition['lon']
        self.ids.map.zoom = 15

    def updatePosition(self, dt):
        global userPosition
        if platform == 'android':
            self.ids.localBus.lat = userPosition['lat']
            self.ids.localBus.lon = userPosition['lon']
        else:
            self.ids.localBus.lat = userPosition['lat']
            self.ids.localBus.lon = userPosition['lat']

    def addMarker(self, lat, lon, source):
        self.ids.map.add_widget(MapMarker(lat=lat, lon=lon, source=source))

    def multipleButtonsCall(self, instance):
        global userPosition
        if instance.icon == 'imgs/local.png':
            self.ids.map.center_on(userPosition['lat'], userPosition['lon'])
            self.ids.map.zoom = 16
        if instance.icon == 'imgs/log_out.png':
            self.manager.get_screen("loginscreen").fileManagment.deleteUserInfo()
            self.manager.current = "loginscreen"


class MapApp(MDApp):

    fileManagment = FileManagment()
    userInfo = fileManagment.getUserInfo()

    def on_loc_update(self, **kwargs):
        global userPosition
        userPosition['lat'] = float(kwargs['lat'])
        userPosition['lon'] = float(kwargs['lon'])
        print(kwargs.items())

    def on_start(self):
        if platform == 'android':
            from plyer import gps
            gps.configure(on_location=self.on_loc_update)
            gps.start()

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.title = 'Tela Inicial'

        screenManagment = ScreenManagment()

        if platform == 'android':
            Clock.schedule_interval(screenManagment.get_screen("mainscreen").updatePosition, 1)
            Clock.schedule_once(screenManagment.get_screen("mainscreen").setStartPosition)
        else:
            Clock.schedule_once(screenManagment.get_screen("mainscreen").setStartPosition)
        try:
            if self.userInfo["login"] == "italoph" and self.userInfo["password"] == "12345":
                screenManagment.current = "mainscreen"
        except:
            print("Login ou senha vazios ou incorretos!")

        return screenManagment


MapApp().run()
