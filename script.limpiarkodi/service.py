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
import controlstartup as control
import coreapp

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

tempPath = translatePath('special://home/addons/temp/')
CacheRomdir   =  translatePath(os.path.join('special://home/addons/temp',''))
packagesdir   =  translatePath(os.path.join('special://home/addons/packages',''))
thumbnails    =  translatePath('special://home/userdata/Thumbnails')

setting = xbmcaddon.Addon().getSetting
iconpath = translatePath(os.path.join('special://home/addons/script.limpiarkodi','icon.png'))
filesize = int(setting('filesize_alert'))
filesize_thumb = int(setting('filesizethumb_alert'))
maxpackage_zips = int(setting('packagenumbers_alert'))

total_size2 = 0
total_size = 0
count = 0

for dirpath, dirnames, filenames in os.walk(packagesdir):
    count = 0
    for f in filenames:
        count += 1
        fp = os.path.join(dirpath, f)
        total_size += os.path.getsize(fp)
total_sizetext = "%.0f" % (total_size/1024000.0)

coreapp.delete_core_files()

if count > maxpackage_zips or int(total_sizetext) > filesize: 
        control.purgePackages()


if setting('autocore') == 'true':
    control.delete_core_files()

if setting('autoclean') == 'true':
    control.clearCache()

if setting('update') == 'true':
    control.update()

if setting('palantir') == 'true':
    control.palantir()

for dirpath2, dirnames2, filenames2 in os.walk(thumbnails):
    for f2 in filenames2:
        fp2 = os.path.join(dirpath2, f2)
        total_size2 += os.path.getsize(fp2)
total_sizetext2 = "%.0f" % (total_size2/1024000.0)

if int(total_sizetext2) > filesize_thumb:
    choice2 = xbmcgui.Dialog().yesno("[COLOR=red]AutoLimpiar[/COLOR]", 'La Carpeta Imagenes tiene [COLOR red]' + str(total_sizetext2) + ' MB   [/COLOR][CR]La carpeta se puede limpiar sin problemas para ahorrar espacio ...[CR]Desea Eliminarlas?', yeslabel='Si',nolabel='No')
    if choice2 == 1:
        control.deleteThumbnails()

xbmcgui.Dialog().notification('Limpiar Kodi',  'Packages: '+ str(total_sizetext) +  ' MB'  ' - Images: ' + str(total_sizetext2) + ' MB' , iconpath, 5000)