
#coding: utf-8

from kivymd.app import MDApp
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform
from kivy.clock import Clock

userPosition = {'lat': 0, 'lon': 0}

class MainScreen(FloatLayout):

    def drawOnMap(self):
        pass

    def setStartPosition(self):
        global userPosition
        self.ids.map.center_on(userPosition['lat'], userPosition['lon'])

    def updatePosition(self, dt):
        global userPosition
        if platform == 'android':
            self.ids.userLocal.lat = userPosition['lat']
            self.ids.userLocal.lon = userPosition['lon']
        else:
            userPosition['lat'] = -8.32985
            userPosition['lon'] = -36.4156
            self.ids.userLocal.lat = userPosition['lat']
            self.ids.userLocal.lon = userPosition['lon']

    def addMarker(self, lat, lon, source):
        self.ids.map.add_widget(MapMarker(lat=lat, lon=lon, source=source))

    def multipleButtonsCall(self, instance):
        global userPosition
        if instance.icon == 'imgs/local.png':
            self.ids.map.center_on(userPosition['lat'], userPosition['lon'])
            self.ids.map.zoom = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MapApp(MDApp):

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
        main_screen = MainScreen()
        Clock.schedule_interval(main_screen.updatePosition, 1)
        main_screen.setStartPosition()
        return main_screen

MapApp().run()

