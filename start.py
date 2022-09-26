from __future__ import unicode_literals
import youtube_dl
import threading
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.bubble import Bubble
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import OneLineListItem
from kivymd.uix.filemanager import MDFileManager
from kivymd.icon_definitions import md_icons
import clipboard as cop #biblioteca para copiar y pegar
from recursos import  ContenedorRigidoDescargas
from kivymd.uix.list import OneLineListItem
from recursos import HiloDescargador

from recursos import CopyPasteUrl



colors={
    "Teal": {
        "200": "#BCAAA4",
        "500": "#212121",
        "700": "#212121",
    },
    "Red": {
        "200": "#C5E1A5",
        "500": "#795548",
        "700": "#5D4037",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#202020",
        "Background": "#E0E0E0",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
    },
}

class Tab(MDBoxLayout, MDTabsBase):
    icon = ObjectProperty()


class MyLogger(object):
    def debug(self, msg):
        print(msg)
    def warning(self, msg):
        print(msg)
    def error(self, msg):
        print(msg)

class VentanaInicial(MDBoxLayout):
    cuenta_item=0
    icons=list(md_icons.keys())[15:30]

    def __init__(self):
        super(VentanaInicial, self).__init__()
        Window.bind(on_keyboard=self.events_manager)
        self.abrir_manager=False
        self.ruta_manager=MDFileManager(
            exit_manager=self.salir_manager,
            select_path=self.seleccionar_ruta,
            preview=True
        )
        print(self.ids)
        self.ids.btn_descargar.bind(on_release=self.add_new_descarga)
        self.ids.btn_listar_directorios.bind(on_release=self.on_listar_directorios)
        '''
        for name_tab in self.icons:
            tab=Tab(title="This is "+name_tab, icon=name_tab)
            self.ids.tabs.add_widget(tab)   
        '''
    def seleccionar_ruta(self, path):
        self.ids.txt_ruta.text=path
        self.salir_manager()
        print(path)
        print(type(path))

    def salir_manager(self, *args):
        self.abrir_manager=False
        self.ruta_manager.close()

    def abrir_manejador_ruta(self):
        self.ruta_manager.show('/')
        self.abrir_manager=True

    #funcion llamada cuando se llama al boton de busqueda de ruta
    def events_manager(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.abrir_manager:
                self.abrir_manager.back()
        return True
    #agregando el cursor
    def on_seleccionar_cursor(self, pos):
        print("Cursor agregando")
        print("--------------------------------------------------")
        print(self.ids.txt_url.focus)
        print("--------------------------------------------------")
        if self.ids.txt_url.focus==True:

            self.copy_paste=copy_paste=CopyPasteUrl()

            self.ids.show_copypaste.add_widget(copy_paste)

        else:
            #enlanzando el boton con la funcion pegar que se hara para pegar la url en el textfield
            self.copy_paste.ids.btn_pegar.bind(on_release=self.pegar_url)
            self.copy_paste.ids.btn_copiar.bind(on_release=self.copiando_url)
            self.copy_paste.ids.btn_borrar.bind(on_release=self.borrar_url)
            self.ids.show_copypaste.remove_widget(self.copy_paste)
    #funcion que servira copiar y pegar la ruta de descarga
    def on_seleccionar_cursor_copypaste_ruta(self, pos):
        print("evento para  pegar la ruta de descarga")
        if self.ids.txt_ruta.focus==True:
            self.copy_paste = copy_paste=CopyPasteUrl()
            self.ids.show_copypaste2.add_widget(copy_paste)
        else:
            self.copy_paste.ids.btn_pegar.bind(on_release=self.pegar_ruta)
            self.copy_paste.ids.btn_copiar.bind(on_release=self.copiando_ruta)
            self.copy_paste.ids.btn_borrar.bind(on_release=self.borrar_ruta)
            self.ids.show_copypaste2.remove_widget(self.copy_paste)

    def pegar_url(self, pos):#copiando la url al campo
        url=cop.paste()
        print(url)
        self.ids.txt_url.text=url
    def copiando_url(self, pos):
        cop.copy(self.ids.txt_url.text)

    def pegar_ruta(self, pos):
        ruta=cop.paste()
        self.ids.txt_ruta.text=ruta

    def borrar_url(self, pos):
        self.ids.txt_url.text=''

    def borrar_ruta(self, pos):
        self.ids.txt_ruta.text=''

    def copiando_ruta(self, pos):
        cop.copy(self.ids.txt_ruta.text)

    def on_listar_directorios(self, pos):
        pass




    def add_new_descarga(self, pos):
        contenedor_descarga=self.ids.list_descargas
        url=self.ids.txt_url.text
        ruta=self.ids.txt_ruta.text
        key_des=0
        descarga_item_list=ItemDescarga()
        item=[descarga_item_list, descarga_item_list.ids.progres_download]


        hilodescarga=HiloDescargador(url,url, ruta, item,contenedor_descarga, daemon=True, key_des=key_des)
        hilodescarga.start()






class ItemDescarga(OneLineListItem):
    pass







class VentanaApp(MDApp):


    def build(self):
        self.theme_cls.colors=colors
        self.theme_cls.primary_palette="Red"
        self.theme_cls.accent_palette="Teal"
        return VentanaInicial()


if __name__=="__main__":
    VentanaApp().run()


