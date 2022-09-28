from __future__ import unicode_literals
import youtube_dl
import threading
from kivy.properties import ObjectProperty
from kivy.metrics import dp
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
from kivymd.uix.list import OneLineListItem, OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.uix.dropdownitem import MDDropDownItem
from recursos import HiloDescargador
from kivy.properties import ObjectProperty, ListProperty, StringProperty,BooleanProperty
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

class IconListItem(OneLineIconListItem):
    pass

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
    hilodescarga=ObjectProperty(None)
    lista_de_hilos=[]
    formato_convertir=StringProperty("")
    list_progreso_descarga=ListProperty([])



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
        lista_formatos=[
            'mp3',
            'mp4',
            'avi',
            'flv',
            'mkv',
            'ogg',
            'webm'
        ]
        menu_item_format=[
            {
                "viewclass": "IconListItem",
                'icon':"git",
                "text": f"{i}",
                "height":dp(56),
                "on_release": lambda x=f"{i}": self.seleccion_del_menu(x),
            } for i in lista_formatos
        ]
        self.menu_format=MDDropdownMenu(
            caller=self.ids.btn_formato_convertir,
            items=menu_item_format,
            position="center",
            width_mult=4
        )
        self.ids.btn_descargar.bind(on_release=self.add_new_descarga)
        self.ids.btn_listar_directorios.bind(on_release=self.on_listar_directorios)

        '''
        for name_tab in self.icons:
            tab=Tab(title="This is "+name_tab, icon=name_tab)
            self.ids.tabs.add_widget(tab)   
        '''
    def seleccion_del_menu(self, text_item):
        self.formato_convertir=text_item
        self.ids.lbl_muestra_format.text="Convertir a "+text_item
        print(text_item)
        self.menu_format.on_dismiss()
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

        #estas variables se modificaran segun el tipo de archivo que se desee
        ydl_opts={}
        if url!="" and ruta!="":
            if self.formato_convertir=="mp3":
                ydl_opts = {
                    'format': 'bestaudio/best,',
                    'nocheckcertificate': True,
                    # 'cachedir':False,
                    'outtmpl': ruta + '/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'logger': None,
                    'progress_hooks': None
                }
            elif self.formato_convertir=="mp4":
                ydl_opts = {
                    'format':'bestvideo+bestaudio',
                    'nocheckcertificate': True,
                    #'cachedir':False,
                    'outtmpl': ruta + '/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key':'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                    'logger': None,
                    'progress_hooks': None
                }
            elif self.formato_convertir=="avi":
                ydl_opts = {
                    'format':'bestvideo+bestaudio',
                    'nocheckcertificate': True,
                    #'cachedir':False,
                    'outtmpl': ruta + '/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key':'FFmpegVideoConvertor',
                        'preferedformat': 'avi',
                    }],
                    'logger': None,
                    'progress_hooks': None
                }
            elif self.formato_convertir=='mkv':
                ydl_opts = {
                    'format':'bestvideo+bestaudio',
                    'nocheckcertificate': True,
                    #'cachedir':False,
                    'outtmpl': ruta + '/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key':'FFmpegVideoConvertor',
                        'preferedformat': 'mkv',
                    }],
                    'logger': None,
                    'progress_hooks': None
                }
            elif self.formato_convertir=="flv":
                ydl_opts = {
                    'format':'bestvideo+bestaudio',
                    'nocheckcertificate': True,
                    #'cachedir':False,
                    'outtmpl': ruta + '/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key':'FFmpegVideoConvertor',
                        'preferedformat': 'flv',
                    }],
                    'logger': None,
                    'progress_hooks': None
                }
            elif self.formato_convertir=="ogg":
                ydl_opts = {
                    'format':'bestvideo+bestaudio',
                    'nocheckcertificate': True,
                    #'cachedir':False,
                    'outtmpl': ruta + '/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key':'FFmpegVideoConvertor',
                        'preferedformat': 'ogg',
                    }],
                    'logger': None,
                    'progress_hooks': None
                }
            elif self.formato_convertir=="webm":
                ydl_opts = {
                    'format':'bestvideo+bestaudio',
                    'nocheckcertificate': True,
                    #'cachedir':False,
                    'outtmpl': ruta + '/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key':'FFmpegVideoConvertor',
                        'preferedformat': 'webm',
                    }],
                    'logger': None,
                    'progress_hooks': None
                }
            existe_descarga=False#Variable que va servir para verificar si existe ya una descarga a nombre de la ruta indicada
            if len(self.list_progreso_descarga)>0:#primero se verifica si en la lista ya hay videos descargandose para verificar si hay videos del mismo descargandose
                for dic_url_descarga in self.list_progreso_descarga:
                    if url in dic_url_descarga:#validando que la url ya exista dentro de la lista de descargas
                        existe_descarga=True#si la url existe en la lista significa que existe


                if existe_descarga==True:#si existe cambia a True significa que no hay que agregar ninguna otra descarga
                    toast("Esta video ya se esta descargando porfavor, si desea descargarlo en otro formato cierre y ejecute esta app nuevamente",
                          duration=3.5)
                else:#si no existe entonces se agrega el nuevo hilo para descargar el video
                    descarga_item_list = ItemDescarga()
                    item = [descarga_item_list, descarga_item_list.ids.progres_download]
                    toast("Video descargando", duration=2.5)
                    self.list_progreso_descarga.append({url: item, 'formato': self.formato_convertir})
                    hilodescarga = HiloDescargador(url, url, ruta, ydl_opts, self.list_progreso_descarga, item,
                                                   contenedor_descarga, daemon=True, key_des=key_des)
                    hilodescarga.start()


            else:#de lo contrario si es igual a cero es porque no hay ningun elemento descargandose
                descarga_item_list = ItemDescarga()
                item = [descarga_item_list, descarga_item_list.ids.progres_download]
                toast("Video descargando", duration=2.5)
                self.list_progreso_descarga.append({url: item, 'formato': self.formato_convertir})
                hilodescarga = HiloDescargador(url, url, ruta, ydl_opts, self.list_progreso_descarga, item,
                                               contenedor_descarga, daemon=True, key_des=key_des)
                hilodescarga.start()
        else:
            toast("Debe de ingresar la URL del video puede ser de YouTube, Facebook o Vimeo ")















class ItemDescarga(OneLineListItem):
    pass





class VentanaApp(MDApp):


    def build(self):
        ventana=VentanaInicial()
        ventana.menu_format.background_color=self.theme_cls.primary_light
        self.theme_cls.colors=colors
        self.theme_cls.primary_palette="Red"
        self.theme_cls.accent_palette="Teal"
        return ventana


if __name__=="__main__":
    VentanaApp().run()


