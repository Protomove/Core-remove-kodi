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

        delete_core_files()