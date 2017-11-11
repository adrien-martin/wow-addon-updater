import packages.requests as requests
from bs4 import BeautifulSoup


# Site splitter

def findZiploc(addonpage):
    # Curse
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return curse('https://www.curseforge.com/wow/addons/' + addonpage.split('/')[-1])
    if addonpage.startswith('https://www.curseforge.com/wow/addons/'):
        return curse(addonpage)

    # Tukui
    elif addonpage.startswith('http://git.tukui.org/'):
        return tukui(addonpage)

    # Wowinterface
    elif addonpage.startswith('http://www.wowinterface.com/'):
        return wowinterface(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')


def getCurrentVersion(addonpage):
    # Curse
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return getCurseVersion('https://www.curseforge.com/wow/addons/' + addonpage.split('/')[-1])
    if addonpage.startswith('https://www.curseforge.com/wow/addons/'):
        return getCurseVersion(addonpage)

    # Tukui
    elif addonpage.startswith('http://git.tukui.org/'):
        return getTukuiVersion(addonpage)

    # Wowinterface
    elif addonpage.startswith('http://www.wowinterface.com/'):
        return getWowinterfaceVersion(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')


# Curse

def curse(addonpage):
    try:
        page = requests.get(addonpage + '/download')
        html_parser = BeautifulSoup(page.content, 'html.parser')
        href = ''
        for download_link in html_parser.find_all(class_="download__link"):
            href = download_link['href']
        href_split = href.split('/')
        download_position = href_split.index('download')
        relative_url_array = href_split[download_position:]
        relative_path = '/' + '/'.join(relative_url_array)

        download_url = addonpage + relative_path
        return download_url
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''


def getCurseVersion(addonpage):
    try:
        page = requests.get(addonpage + '/files')
        html_parser = BeautifulSoup(page.content, 'html.parser')
        version = html_parser.find_all(class_="table__content file__name full")[0].text
        return version
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        return ''


# Tukui

def tukui(addonpage):
    print('Tukui is not supported yet.')
    return ''


def getTukuiVersion(addonpage):
    # print('Tukui is not supported yet.')
    return ''


# Wowinterface

def wowinterface(addonpage):
    downloadpage = addonpage.replace('info', 'download')
    try:
        page = requests.get(downloadpage + '/download')
        contentString = str(page.content)
        indexOfZiploc = contentString.find('Problems with the download? <a href="') + 37  # first char of the url
        endQuote = contentString.find('"', indexOfZiploc)  # ending quote after the url
        return contentString[indexOfZiploc:endQuote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''


def getWowinterfaceVersion(addonpage):
    try:
        page = requests.get(addonpage)
        contentString = str(page.content)
        indexOfVer = contentString.find('id="version"') + 22  # first char of the version string
        endTag = contentString.find('</div>', indexOfVer)  # ending tag after the version string
        return contentString[indexOfVer:endTag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        return ''
