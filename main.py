# coding: utf-8

from kivymd.app import MDApp
from kivy_garden.mapview import MapView, MapMarker
from kivy.utils import platform
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock, mainthread
from lib.filemanagment import FileManagment
import requests
from plyer import gps

userPosition = {'id': 0, 'lat': 0, 'lon': 0}
sendData = False

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

    markerList = [MapMarker(), MapMarker()]

    def drawOnMap(self):
        pass

    @mainthread
    def updatePosition(self, dt):
        global userPosition
        global sendData
        if platform == 'android':
            self.markerList[0] = self.markerList[1]
            self.markerList[1] = self.addMarker(userPosition['lat'], userPosition['lon'], source="imgs/onibus_local.png")
            self.ids.map.center_on(userPosition['lat'], userPosition['lon'])
            self.ids.map.zoom = 18
            self.ids.map.add_marker(self.markerList[1])
            self.ids.map.remove_marker(self.markerList[0])
            print(userPosition)
            if sendData == True:
                try:
                    requests.post("https://Aplicativo-Onibus.italopimentel.repl.co/routers", json=userPosition)
                except:
                    print("Não foi possível enviar a rota, ocorreu algum erro")

    def addMarker(self, lat, lon, source):
        return MapMarker(lat=lat, lon=lon, source=source)

    def multipleButtonsCall(self, instance):
        global userPosition
        if instance.icon == 'imgs/local.png':
            self.ids.map.center_on(userPosition['lat'], userPosition['lon'])
            self.ids.map.zoom = 16
        if instance.icon == 'imgs/log_out.png':
            self.manager.get_screen("loginscreen").fileManagment.deleteUserInfo()
            self.manager.current = "loginscreen"

    def startService(self):
        global sendData
        if sendData == False:
            sendData = True
            self.ids.btnStart.text = "Parar"
            self.ids.btnStart.color = "red"
            print("O valor foi mudado para {}".format(sendData))
        elif sendData == True:
            sendData = False
            self.ids.btnStart.text = "Iniciar"
            self.ids.btnStart.color = "blue"
            print("O valor foi mudado para {}".format(sendData))

class MapApp(MDApp):

    fileManagment = FileManagment()
    userInfo = fileManagment.getUserInfo()

    def on_loc_update(self, **kwargs):
        global userPosition
        userPosition['lat'] = float(kwargs['lat'])
        userPosition['lon'] = float(kwargs['lon'])
        print(kwargs.items())

    def on_start(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.title = 'Tela Inicial'

        if platform == 'android':
            gps.configure(on_location=self.on_loc_update)
            gps.start(minTime=3000, minDistance=0)

    def build(self):
        screenManagment = ScreenManagment()
        Clock.schedule_interval(screenManagment.get_screen("mainscreen").updatePosition, 3)
        try:
            if self.userInfo["login"] == "italoph" and self.userInfo["password"] == "12345":
                screenManagment.current = "mainscreen"
        except:
            print("Login ou senha vazios ou incorretos!")

        return screenManagment

app = MapApp().run()
