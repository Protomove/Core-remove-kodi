#   script.limpiarkodi
#   Copyright (C) 2020  Teco
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.



import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import re
import os
import sqlite3
import json

if sys.version_info.major==3:
    from urllib.request import urlopen, Request, HTTPError
    from six.moves import urllib
    from six.moves.urllib.parse import parse_qs, urlparse, quote_plus, unquote_plus
    from urllib.parse import urlparse
    translatePath = xbmcvfs.translatePath
    try:
        from urllib.parse import parse_qs
    except ImportError:
        from cgi import parse_qs
if sys.version_info.major==2:
    from six.moves import urllib
    from six.moves.urllib.parse import parse_qs, urlparse, quote_plus, unquote_plus
    from urllib2 import urlopen, Request, HTTPError
    from urlparse import urlparse
    from urlparse import parse_qs
    translatePath = xbmc.translatePath
addon_id = 'script.limpiarkodi'
fanart = translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
icon3 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'luar.png'))
icon4 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'icon2.png'))
icon2 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'indigo.png'))
icon5 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'bibloteca.png'))
icon6 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'ltemp.png'))
icon7 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'paque.png'))
icon8 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'update.png'))
icon9 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'image.png'))
icon10 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'depen.png'))
icon11 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'Ajustes.png'))
icon12 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'respaldo.png'))
icon13 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'herra.png'))
icon14 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'depenico.png'))
icon15 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'Mante.png'))
icon16 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'Mante.png'))
icon17 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'lupa.png'))
icon18 = translatePath(os.path.join('special://home/addons/script.limpiarkodi/media' , 'gdrive.png'))
thumbnailPath = translatePath('special://thumbnails');
cachePath = os.path.join(translatePath('special://home'), 'cache')
##cdmPath = os.path.join(translatePath('special://home'), 'cdm')
purgePath = os.path.join(translatePath('special://home/addons'), 'packages')
tempPath = translatePath('special://home/addons/temp/')
indigoPath = translatePath('special://home/addons/plugin.program.indigo')
gdrivePath = translatePath('special://home/addons/plugin.video.gdrive')
ltempPath = translatePath('special://home/temp')
addonPath = os.path.join(os.path.join(translatePath('special://home'), 'addons'),'script.limpiarkodi')
mediaPath = os.path.join(addonPath, 'media')
databasePath = translatePath('special://database')
unoxdosPath = translatePath('special://home/addons/script.limpiarkodi')
THUMBS = translatePath(os.path.join('special://home/userdata/Thumbnails',''))
addonName = xbmcaddon.Addon().getAddonInfo('name')

#######################################################################
#                       Menu                                          #
#######################################################################

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi



def mainMenu():
    addItem('  Limpiar Cache y Rom','url', 1,icon15)
    addItem('  Borrar Imagenes', 'url', 2,icon9)
    addItem('  Eliminar Temp', 'url', 3,icon6)
    addItem('  Eliminar Paquetes', 'url', 4,icon7)
def depe():
    addfolder('Dependencias','url', 17,icon14)

def herra():
    addfolder('Herramientas','url', 18,icon13)

    addItem('Buscador de Addons y Scripts','url', 16,icon17)
    addItem('Ajustes','url', 15,icon11)


#######################################################################
#                        Add Menu                               #
#######################################################################

def addLink(name,url,iconimage):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok


def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )

    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addItem(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name)#, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    #liz.setProperty('fanart_image', fanart)
    liz.setArt({'icon': 'DefaultFolder.png', 'thumb': iconimage, 'fanart': fanart})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)

def addfolder(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name)#, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    #liz.setProperty('fanart_image', fanart)
    liz.setArt({'icon': 'DefaultFolder.png', 'thumb': iconimage, 'fanart': fanart})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok


#######################################################################
#                        Parses Choice
#######################################################################
      
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                    params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                    splitparams={}
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]
    return param

#######################################################################
#                       Funciones                                     #
#######################################################################
def setupCacheEntries():
    entries = 21 #make sure this refelcts the amount of entries you have
    dialogName = [" YouTube", " UrlResolve", " Simple Cacher", " Simple Downloader", " Metadatautils", " Streamlink", " Tvalacarta", " Resolveurl", " Alfa Downloads", " Metahandler", " Youtube.dl", " Extendedinfo", " TheMovieDB", " Extendedinfo/YouTube", " Autocompletion/Google", " Autocompletion/Bing", " Universalscrapers", " Torrents Alfa", " MediaExplorer Downloads", " Balandro Downloads", " MediaExplorer Torrent"]
    pathName = ["special://profile/addon_data/plugin.video.youtube/kodion", "special://profile/addon_data/script.module.urlresolve/cache",
                    "special://profile/addon_data/script.module.simplecache", "special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/script.module.metadatautils/animatedgifs", "special://profile/addon_data/script.module.streamlink/base","special://profile/addon_data/plugin.video.tvalacarta/downloads", "special://profile/addon_data/script.module.resolveurl/cache", "special://profile/addon_data/plugin.video.alfa/downloads", "special://profile/addon_data/script.module.metahandler/meta_cache", "special://profile/addon_data/script.module.youtube.dl/tmp", "special://profile/addon_data/script.extendedinfo/images", "special://profile/addon_data/script.extendedinfo/TheMovieDB", "special://profile/addon_data/script.extendedinfo/YouTube", "special://profile/addon_data/plugin.program.autocompletion/Google", "special://profile/addon_data/plugin.program.autocompletion/Bing", "special://profile/addon_data/script.module.universalscrapers", "special://profile/addon_data/plugin.video.alfa/videolibrary/temp_torrents_Alfa", "special://profile/addon_data/plugin.video.mediaexplorer/downloads", "special://profile/addon_data/plugin.video.balandro/downloads", "special://profile/addon_data/plugin.video.mediaexplorer/torrent"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

def delete_core_files():
    home_path = translatePath('special://xbmc')
    dialog = xbmcgui.Dialog()

    # Verificar si el directorio existe
    if os.path.exists(home_path):
        file_count = 0
        # Obtener la lista de archivos en el directorio principal
        files = [f for f in os.listdir(home_path) if os.path.isfile(os.path.join(home_path, f))]
        # Contar los archivos cuyos nombres empiezan con "core."
        file_count += sum(1 for f in files if f.startswith("core."))

        if file_count > 0:
            for f in files:
                try:
                    if f.startswith("core."):
                        os.unlink(os.path.join(home_path, f))
                except Exception as e:
                    xbmcgui.Dialog().notification('Error', str(e))
            xbmcgui.Dialog().notification('Limpia Tu Kodi', "Archivos core eliminados correctamente")
        else:
            xbmcgui.Dialog().notification('Limpia Tu Kodi', "No se encontraron archivos core")
    else:
        xbmcgui.Dialog().notification('Error', "El directorio home no fue encontrado")

def clearCache():

    if os.path.exists(cachePath)==True:
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Borrar Cache", str(file_count) + " Archivos Encontrados[CR]Desea Eliminarlos?"):
                
                    for f in files:
                        try:
                            if (f == "*.log" or f == "*.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Borrar Archivos en ROM Cache", str(file_count) + " Archivos Encontrados[CR]Desea Eliminarlos?"):
                    for g in files:
                        try:
                            if (g == "*.log" or f == "*.old.log"): continue
                            os.unlink(os.path.join(root, g))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    ##if os.path.exists(cdmPath)==True:    
      ##  for root, dirs, files in os.walk(cdmPath):
        ##    file_count = 0
          ##  file_count += len(files)
            ##if file_count > 0:
               ## dialog = xbmcgui.Dialog()
                ##if dialog.yesno("Borrar Archivos en CDM", str(file_count) + " Archivos Encontrados", "Desea Eliminarlos?"):
                  ##  for h in files:
                    ##    try:
                      ##      if (h == "*.dmp" or f == "*.txt"): continue
                        ##    os.unlink(os.path.join(root, h))
                        ##except:
                          ##  pass
                    ##for d in dirs:
                      ##  try:
                        ##    shutil.rmtree(os.path.join(root, d))
                       ## except:
                         ##   pass
                        
            ##else:
              ##  pass
    if os.path.exists(purgePath)==True:
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Borrar Cache", str(file_count) + " Archivos Encontrados[CR]Desea Eliminarlos?"):
                
                    for f in files:
                        try:
                            if (f == "*.*" or f == "*.*"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Borra ATV2 Cache ", str(file_count) + " Archivos Encontrados 'Otros'[CR]Desea Eliminarlo?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Borra ATV2 Cache ", str(file_count) + " Archivos Encontrados 'LocalAndRental'[CR]Desea Eliminarlos?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass

    cacheEntries = setupCacheEntries()

    for entry in cacheEntries:
        clear_cache_path = translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno("Limpia tu Kodi",str(file_count) + "%s Archivos Cache Encontrados[CR]Desea Eliminarlos?" %(entry.name)):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass


    dialog = xbmcgui.Dialog()
    dialog.ok("Limpia tu Kodi", "Todos los Archivos se Limpiaron con Exito")


def deleteThumbnails():

    if os.path.exists(thumbnailPath)==True:

            dialog = xbmcgui.Dialog()
            choice1 =dialog.yesno("Borrar Imagenes", "Desea eliminar todas las Imagenes?")
            if choice1 == 1:
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:
                        for f in files:
                            try:
                               os.unlink(os.path.join(root, f))
                            except:
                                pass
            
                choice2 =dialog.yesno("Limpia Tu Kodi", "Desea reiniciar Kodi ahora para terminar el proceso")
                if choice2 == 1:
                   xbmc.executebuiltin("RestartApp")()

    try:
        text13 = os.path.join(databasePath,"Textures13.db")
        os.unlink(text13)

    except:
        pass



def purgeCacheRom():

    tempPath = translatePath('special://home/addons/temp')
    dialog = xbmcgui.Dialog()
    for root, dirs, folders in os.walk(tempPath):
            file_count = 0
            file_count += len(folders)
    if os.path.exists(tempPath)==True:
        for root, dirs, folders in os.walk(tempPath):
            file_count = 0
            file_count += len(folders)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Borrar Archivos en Temp", str(file_count) + " Archivos Encontrados[CR]Desea Eliminarlos?"):

                    for f in folders:
                        try:
                            if (f == "*.*" or f == "*.*"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
        xbmcgui.Dialog().notification('Limpia Tu Kodi', "Archivos Temp Eliminados")


def purgePackages():

    purgePath = translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    if dialog.yesno("Borrar contenido en Paquetes", "%d Paquetes Encontrados.[CR]Desea Eliminarlos?" %file_count):
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                dialog = xbmcgui.Dialog()
                dialog.ok("Limpia tu Kodi", "Borrar todo el contenido de Paquetes")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Limpia tu Kodi", "Eliminados Paquetes")


def update():

        xbmc.executebuiltin('UpdateAddonRepos()')
        xbmc.executebuiltin('UpdateLocalAddons()')
        xbmc.executebuiltin('RunAddon(plugin.video.palantir2)')
        xbmc.executebuiltin("ActivateWindow(home)")
        xbmc.executebuiltin("ReloadSkin()")
        xbmcgui.Dialog().notification('Limpia Tu Kodi', "Repositorios & Addons[COLOR green]Actualizados[/COLOR]")
        try:
            test = os.path.join(unoxdosPath,"test.py")
            os.unlink(test)
        except:
            pass

def depen():

        xbmc.executebuiltin('ActivateWindow(10025,addons://dependencies/&quot;)')

def bibloteca():

        xbmc.executebuiltin('CleanLibrary(video,true)')


def deleteindigo():

    indigoPath = translatePath('special://home/addons/plugin.program.indigo')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(indigoPath):
            file_count = 0
            file_count += len(files)
    if os.path.exists(indigoPath)==True:    
        for root, dirs, files in os.walk(indigoPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Este Proceso Desinstala Indigo", str() + "Despues de desinstalar Indigo Kodi se  [COLOR red]reiniciara[/COLOR][CR]Esta seguro de que desea eliminar Indigo?"):

                    for f in files:
                        try:
                            if (f == "*.*" or f == "*.*"): continue
                            os.unlink(os.path.join(root, f))
                            xbmc.executebuiltin("RestartApp")()
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                xbmcgui.Dialog().notification('Limpia Tu Kodi', "Indigo [COLOR green] Desinstalado[/COLOR]")
                pass

def deletegdrive():

    gdrivePath = translatePath('special://home/addons/plugin.video.gdrive')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(gdrivePath):
            file_count = 0
            file_count += len(files)
    if os.path.exists(gdrivePath)==True:    
        for root, dirs, files in os.walk(gdrivePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Este Proceso Desinstala gdrive", str() + "Despues de desinstalar gdrive Kodi se  [COLOR red]reiniciara[/COLOR][CR]Esta seguro de que desea eliminar gdrive?"):

                    for f in files:
                        try:
                            if (f == "*.*" or f == "*.*"): continue
                            os.unlink(os.path.join(root, f))
                            xbmc.executebuiltin("RestartApp")()
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                xbmcgui.Dialog().notification('Limpia Tu Kodi', "gdrive [COLOR green] Desinstalado[/COLOR]")
                pass

def luar():

        xbmc.executebuiltin('InstallAddon(script.luar)')
        xbmc.executebuiltin('RunAddon(script.luar)')


def enableadaptive():

        xbmc.executebuiltin('InstallAddon(inputstream.adaptive)')
        xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % ('Limpia tu Kodi' , 'Input Stream Adaptative[COLOR green] Instalado[/COLOR]' , '3000', icon))




def enablertmp():

        xbmc.executebuiltin('InstallAddon(inputstream.rtmp)')
        xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % ('Limpia tu Kodi' , 'InputStream RTMP[COLOR green] Instalado[/COLOR]' , '3000', icon))



def compactDB():
    conn = sqlite3.connect(translatePath("special://home/userdata/Database/Addons27.db"))
    size1 = size2 = 0
    databasePath = translatePath('special://database')
    if os.path.exists(databasePath):
        files = ([f for f in os.listdir(databasePath) if f.endswith('.db') and os.path.isfile(os.path.join(databasePath, f))])
        d = xbmcgui.DialogProgress()
        d.create('Limpia Tu Kodi', "Iniciando... ")
        total = len(files)

        for n, f in enumerate(files):
            size1 += os.path.getsize(os.path.join(databasePath, f))
            d.update(int(n * 100 / total), 'Compactando ' + f)
            try:
                conn = sqlite3.connect(os.path.join(databasePath, f))
                conn.execute("VACUUM")
            except:
                logger("Error al compactar %s" % f)
            finally:
                conn.close()
                size2 += os.path.getsize(os.path.join(databasePath, f))

        d.close()

        size = size1 - size2
        if size > 1048576:
            msg = "Bases de datos compactadas: %0.2fMB" % (size / 1048576.0)
        elif size > 1024:
            msg = "Bases de datos compactadas: %0.2fKB" % (size / 1024.0)
        elif size == 0:
            msg = "Las bases de datos ya estaban compactadas"
        else:
            msg = "Bases de datos compactadas: %s bytes" % size

    else:
        msg = "Se ha producido un error al compactar las  bases de datos.\n" \
              "Reinicie Kodi y vuelva a probar"
        logger(msg)

    xbmcgui.Dialog().ok('Limpia Tu Kodi', msg)
    return

def exec_sql(command, database='Addons27.db'):
    res = None
    conn = sqlite3.connect(translatePath("special://home/userdata/Database/" + database))
    try:
        cur = conn.cursor()
        cur.execute(command)
        if 'SELECT' in command.upper():
            res = cur.fetchall()
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger('SQL EXCEPTION: %s' % str(e), 'error')
        xbmc.executebuiltin('Notification(%s, %s)' % ('ERROR:', str(e)))
    finally:
        conn.close()

    return res

def del_addon(id, repo=False):
    command = {
        "jsonrpc": "2.0",
        "method": "Addons.GetAddonDetails",
        "params": {"addonid": id, "properties": ['path']},
        "id": 1}
    res = json.loads(xbmc.executeJSONRPC(json.dumps(command)))
    path = res.get('result', {}).get('addon', {}).get('path')

    if path:
        # Eliminar carpeta local
        shutil.rmtree(path)
        # Eliminar de la BBDD
        exec_sql("DELETE FROM installed WHERE addonID = " + chr(34) + id + chr(34))
        if repo:
            exec_sql("DELETE FROM repo WHERE addonID = " + chr(34) + id + chr(34))

def analizar_repositorios(l_repos=None):
    ret = {}
    if not l_repos:
        l_repos = [a[0] for a in exec_sql("SELECT addonID FROM repo")]
    elif not isinstance(l_repos, list):
        l_repos = [l_repos]

    for repo in l_repos:
        addons_in_repo = [a[0] for a in exec_sql("SELECT addons.addonID FROM addonlinkrepo "
                                                 "JOIN addons ON addonlinkrepo.idAddon = addons.id "
                                                 "JOIN repo ON addonlinkrepo.idRepo = repo.id "
                                                 "WHERE  addons.addonID != repo.addonID AND "
                                                 "repo.addonID = " + chr(34) + repo + chr(34))]

        addons_installed_in_repo = [a[0] for a in exec_sql("SELECT addonID FROM installed") if a[0] in addons_in_repo]
        ret[repo] = {'alls': addons_in_repo, "installs": addons_installed_in_repo}

    return ret

def huerfa():
    c = 0
    r = analizar_repositorios()
    for k, v in r.items():
        if v['alls'] and not v['installs']:
            del_addon(k, True)
            c += 1

    if c == 0:
        xbmcgui.Dialog().ok(addonName, "No existen repositorios huerfanos.")
    elif c == 1:
        xbmcgui.Dialog().ok(addonName, "Se ha eliminado un repositorio huerfano correctamente.")
    else:
        xbmcgui.Dialog().ok(addonName, "Se han eliminado %s repositorios huerfanos correctamente.",
                            '' % c)

def dependencias_huerfanas():
    excluidos = ['script.module.beautifulsoup4', 'script.module.pil', 'script.module.pycryptodome', 'script.module.six']
    l_addons = [a[0] for a in exec_sql(
        "SELECT addonID FROM installed WHERE addonID LIKE " + chr(34) + "script.module.%" + chr(
            34) + " OR addonID LIKE " + chr(34) + "metadata.common.%" + chr(34))]

    l_inc = []
    for addon in [a for a in
                  exec_sql("SELECT metadata FROM addons INNER JOIN installed ON addons.addonID = installed.addonID")]:
        depen_by_addon = re.findall('"dependencies"\s*:\s*(\[[^\]]+\])', addon[0])
        if depen_by_addon:
            l_inc.extend(re.findall('"addonId"\s*:\s*"([^"]+)"', depen_by_addon[0]))

    return list((set(l_addons) - set(l_inc)) - set(excluidos))

def del_huerfanas():
    c = 0
    while True:
        huerfanas = dependencias_huerfanas()
        if huerfanas:
            for b in huerfanas:
                del_addon(b)
                c += 1
        else:
            break
    if del_huerfanas:
        if c == 0:
            xbmcgui.Dialog().ok(addonName, "No existen dependencias huerfanas.")
        elif c == 1:
            xbmcgui.Dialog().ok(addonName, "Se ha eliminado una dependencia huerfana correctamente.")
        else:
            xbmcgui.Dialog().ok(addonName, "Se han eliminado %s dependencias huerfanas correctamente."
                                '' % c)


def ajustes():

        xbmcaddon.Addon(id=sys.argv[0][9:-1]).openSettings()

def buscar():
        xbmc.executebuiltin('ActivateWindow(10040,addons://search)')

#######################################################################
#                       subs                                       #
#######################################################################

def depenm():

    addItem('  Mostrar Dependencias', 'url', 19,icon10)
    ##addItem('  Eliminar Repositorios Huerfanos', 'url', 9,icon10)
    ##addItem('  Eliminar Depenpencias Huerfanas', 'url', 14,icon10)



def herram():

    addItem('  Luar', 'url', 6,icon3)
    addItem('  Actualizar Addons y Repositorios', 'url', 5,icon8)
    addItem('  Compactar Base de Datos', 'url', 13,icon12)
    addItem('  Eliminar Indigo', 'url', 7,icon2)
    addItem('  Eliminar Gdrive', 'url', 20,icon18)
    addItem('  Activar InputStream Adaptive', 'url', 10,icon4)
    addItem('  Activar RTMP Input', 'url', 11,icon4)
    addItem('  Limpiar Bibloteca Kodi', 'url', 12,icon5)
    addItem('  Eliminar Archivos Core', 'url', 21, icon6)  # Añadir esta línea


#######################################################################
#                       Soporte                                       #
#######################################################################


params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.parse.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.parse.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

if mode==None or url==None or len(url)<1:
        mainMenu()

if mode==None or url==None or len(url)<1:
        depe()

if mode==None or url==None or len(url)<1:
        herra()

elif mode==1:
        clearCache()
        
elif mode==2:
        deleteThumbnails()

elif mode==3:
        purgeCacheRom()

elif mode==4:
        purgePackages()

elif mode==5:
        update()

elif mode==6:
        luar()

elif mode==7:
        deleteindigo()

elif mode==8:
        depenm()

elif mode==9:
        huerfa()

elif mode==10:
        enableadaptive()

elif mode==11:
        enablertmp()

elif mode==12:
        bibloteca()

elif mode==13:
        compactDB()

elif mode==14:
        del_huerfanas()

elif mode==15:
        ajustes()

elif mode==16:
        buscar()

elif mode==17:
        depenm()

elif mode==19:
        depen()

elif mode==18:
        herram()
		
elif mode==20:
        deletegdrive()
        
elif mode == 21:
        delete_core_files()
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))