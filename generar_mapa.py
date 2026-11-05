"""Regenera el mapa base de la SNGR (una vez cada 3 a 6 meses).

Requisitos: Windows o Linux con Python 3 y conexión a internet. No necesita librerías adicionales.
Uso:  python generar_mapa.py
Resultado: carpeta AAAAMMDD/ con un archivo .pmtiles por provincia (zooms 0 a 15) y pais.pmtiles (zooms 0 a 9),
           e indice.json actualizado. Luego se publica todo en el repositorio mapa-base-sngr (ver README).
Los datos vienen de OpenStreetMap a través de la compilación diaria pública de Protomaps.
"""
import json, os, platform, subprocess, urllib.request, zipfile, io

AQUI = os.path.dirname(os.path.abspath(__file__))
IND = json.load(open(os.path.join(AQUI, 'indice.json'), encoding='utf-8'))

def obtener_pmtiles():
    exe = os.path.join(AQUI, 'pmtiles.exe' if os.name == 'nt' else 'pmtiles')
    if os.path.exists(exe):
        return exe
    rel = json.loads(urllib.request.urlopen('https://api.github.com/repos/protomaps/go-pmtiles/releases/latest').read())
    clave = 'Windows_x86_64.zip' if os.name == 'nt' else 'Linux_x86_64.tar.gz'
    url = [a['browser_download_url'] for a in rel['assets'] if a['name'].endswith(clave)][0]
    datos = urllib.request.urlopen(url).read()
    if url.endswith('.zip'):
        zipfile.ZipFile(io.BytesIO(datos)).extract('pmtiles.exe', AQUI)
    else:
        import tarfile
        tarfile.open(fileobj=io.BytesIO(datos)).extract('pmtiles', AQUI)
        os.chmod(exe, 0o755)
    return exe

def ultima_compilacion():
    b = json.loads(urllib.request.urlopen('https://build-metadata.protomaps.dev/builds.json').read())
    return b[-1]['key'].replace('.pmtiles', '')

def extraer(exe, fuente, destino, caja, zmax):
    subprocess.run([exe, 'extract', fuente, destino, '--bbox=%s,%s,%s,%s' % tuple(caja), '--maxzoom=%d' % zmax], check=True)

if __name__ == '__main__':
    exe = obtener_pmtiles()
    version = ultima_compilacion()
    fuente = 'https://build.protomaps.com/%s.pmtiles' % version
    carpeta = os.path.join(AQUI, version)
    os.makedirs(carpeta, exist_ok=True)
    extraer(exe, fuente, os.path.join(carpeta, 'pais.pmtiles'), [-92.2, -5.2, -75.0, 1.9], 9)
    for cod, p in sorted(IND['provincias'].items()):
        print('Provincia', cod, p['nombre'])
        destino = os.path.join(carpeta, cod + '.pmtiles')
        extraer(exe, fuente, destino, p['caja'], 15)
        p['mb'] = round(os.path.getsize(destino) / 1e6, 1)
    IND['version'] = version
    IND['fecha'] = '%s-%s-%s' % (version[:4], version[4:6], version[6:])
    IND['fuente'] = 'Protomaps (build %s) con datos de OpenStreetMap; recorte por provincia en zooms 0 a 15 y archivo nacional en zooms 0 a 9' % version
    json.dump(IND, open(os.path.join(AQUI, 'indice.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Listo. Versión', version, 'en', carpeta)
