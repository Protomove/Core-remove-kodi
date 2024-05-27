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
thumbnailPath = translatePath('special://thumbnails');
cachePath = os.path.join(translatePath('special://home'), 'cache')
##cdmPath = os.path.join(translatePath('special://home'), 'cdm')
purgePath = os.path.join(translatePath('special://home/addons'), 'packages')
ltempPath = translatePath('special://home/temp')
torrentsdir = translatePath(os.path.join('special://cache'))
tempPath = translatePath('special://home/addons/temp/')
addonPath = os.path.join(os.path.join(translatePath('special://home'), 'addons'),'script.limpiarkodi')
unoxdosPath = translatePath('special://home/addons/plugin.video.1x2')
mediaPath = os.path.join(addonPath, 'media')
databasePath = translatePath('special://database')
THUMBS    =  translatePath(os.path.join('special://home/userdata/Thumbnails',''))

addon_id = 'script.limpiarkodi'
fanart = translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
iconpath = translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi

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

                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log"): continue
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

                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log"): continue
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
    if os.path.exists(ltempPath)==True:    
        for root, dirs, files in os.walk(ltempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                    for f in files:
                        try:
                            if (f == "*.*" or f == "*.*.*"): continue
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
##    if os.path.exists(cdmPath)==True:    
##        for root, dirs, files in os.walk(cdmPath):
##            file_count = 0
##            file_count += len(files)
##            if file_count > 0:
##                    for f in files:
##                        try:
##                            if (f == "*.dmp" or f == "*.txt"): continue
##                            os.unlink(os.path.join(root, f))
##                        except:
##                            pass
##                    for d in dirs:
##                        try:
##                            shutil.rmtree(os.path.join(root, d))
##                        except:
##                            pass
##                        
##            else:
##                pass
    if os.path.exists(purgePath)==True:
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                
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


                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass

    try:
        test = os.path.join(unoxdosPath,"test.py")
        os.unlink(test)
    except:
        pass


    xbmcgui.Dialog().notification('Limpia tu Kodi' , 'Auto Limpieza[COLOR blue] Completada[/COLOR]' , iconpath, 3000)

def Cacherom():

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log"): continue
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


                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass

    xbmcgui.Dialog().notification('Limpia tu Kodi' , 'Auto Limpieza[COLOR blue] Completada[/COLOR]' , iconpath, 3000)


def deleteThumbnails():

    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Borrar Imagenes", "Esta opcion eliminara todas las Imagenes[CR]Desea continuar?"):
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass                


    if os.path.exists(THUMBS):
        try:    
            for root, dirs, files in os.walk(THUMBS):
                file_count = 0
                file_count += len(files)
                # Count files and give option to delete
                if file_count > 0:
                        for f in files:    os.unlink(os.path.join(root, f))
                        for d in dirs: shutil.rmtree(os.path.join(root, d))
        except:
            pass
            
    try:
        text13 = os.path.join(databasePath,"Textures13.db")
        os.unlink(text13)
    except:
        pass
    dialog.ok("[COLOR=red]Atencion[/COLOR]", "Debe Reiniciar Kodi Para Aplicar los Cambios")


def purgePackages():

    purgePath = translatePath('special://home/addons/packages')
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

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
    xbmcgui.Dialog().notification('Limpia tu Kodi' , 'Auto Limpieza[COLOR blue] Completada[/COLOR]', iconpath, 3000)


def update():

        xbmc.executebuiltin('UpdateAddonRepos()')
        xbmc.executebuiltin('UpdateLocalAddons()')
        xbmcgui.Dialog().notification('Limpia Tu Kodi', "Repositorios & Addons[COLOR green]Actualizados[/COLOR]")
        try:
            test = os.path.join(unoxdosPath,"test.py")
            os.unlink(test)
        except:
            pass

def palantir():
        xbmc.executebuiltin('RunAddon(plugin.video.palantir3)')
        xbmc.executebuiltin("ActivateWindow(home)")
        xbmc.executebuiltin("ReloadSkin()")



def purgeCacheRom():

    tempPath = translatePath('special://home/addons/temp')
    paths = []
    if os.path.isdir(path_temp):
        paths = os.listdir(path_temp)

    else:
        e = t = 0
        for p in paths:
            p1 = os.path.join(path_temp,p)
            try:
                if os.path.isfile(p1):
                    os.unlink(p1)
                elif os.path.isdir(p1):
                    rmtree(p1)
                t += 1
            except:
                pass
