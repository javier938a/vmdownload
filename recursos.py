from __future__ import  unicode_literals
import youtube_dl
import threading
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivy.uix.bubble import Bubble
from kivymd.uix.progressbar import  MDProgressBar
from kivymd.uix.list import OneLineListItem


class CopyPasteUrl(Bubble):
    pass

class ContenedorRigidoDescargas(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

class MyLogger(object):
    def debug(self, msg):
        pass#print(msg)
    def warning(self, msg):
        pass#print(msg)
    def error(self, msg):
        pass#print(msg)

class HiloDescargador(threading.Thread):
    list_progreso_descarga = []

    def __init__(self, nombre_hilo, url, ruta,item, contendor_descarga,daemon=None, key_des=None):
        threading.Thread.__init__(self, name=nombre_hilo, target=HiloDescargador.run, daemon=daemon)
        self.url=url
        self.ruta=ruta
        self.descargas={}
        self.contenedor_descarga=contendor_descarga

        self.list_progreso_descarga.append({nombre_hilo: item})  # agrego un diccionario de progreos a una lista global para ir viendo los prograsos independiente


        self.contenedor_descarga.add_widget(item[0])


            #print(item_progres)




    def progreso_descarga(self, d):
        total_descarga = int(d['total_bytes'])
        descargando = int(d['downloaded_bytes'])
        porcentaje=round(float((descargando/total_descarga)*100), 2)
        #print(self.list_progreso_descarga)
        #print(d)
        print("Hola: "+str(self.name))
        for progreso in self.list_progreso_descarga:
            if self.name in progreso:
                #print("Nombre del Hilo")
                #print(progreso[self.name][1])
                if d['status']=='downloading':
                    lista_de_divicion_de_ruta=d['tmpfilename'].split("/")
                    nombre_media_con_extension=lista_de_divicion_de_ruta[len(lista_de_divicion_de_ruta)-1]
                    lista_nombre_media_con_extencion=nombre_media_con_extension.split('.')
                    nombre_media=lista_nombre_media_con_extencion[0]

                    progreso[self.name][0].ids.lbl_porcentaje.text=str(porcentaje)+"% velocidad "+str(d['_speed_str'])
                    progreso[self.name][0].ids.lbl_ubicacion.text="Descargando: [size=11]"+nombre_media+"[/size]"
                    progreso[self.name][1].value=porcentaje
                    #print(d)



        print("Porcentaje: "+str(porcentaje))

        if d['status'] == 'finished':
            print('descarga finalizada, convertido')


    def run(self):
        url_descarga = self.url
        ydl_opts = {
            #'format': 'bestaudio/best,'
            'format':'bestvideo+bestaudio',
            'nocheckcertificate': True,
            #'cachedir':False,
            'outtmpl': self.ruta + '/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'postprocessors': [{
                #'key': 'FFmpegExtractAudio',
                'key':'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
                #'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.progreso_descarga]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_descarga])


