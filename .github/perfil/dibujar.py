"""Dibuja la cabecera y la tarjeta de estado del perfil a partir de perfil.toml.

El texto va convertido en trazos con IBM Plex Sans, para que GitHub lo enseñe
igual en cualquier navegador. Las fechas se consultan en cada ejecución: la del
último commit si el proyecto tiene "repo" y la de la última entrada si tiene "rss".

Uso: python .github/perfil/dibujar.py
"""
import email.utils
import io
import json
import os
import sys
import time
import tomllib
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
MADRID = ZoneInfo("Europe/Madrid")

# Colores de la web (docs/diseno.md de jdsantana.com)
PINO = "#1c3b30"
LIQUEN = "#9fb8ac"
BANDA_CAJA = "#24483b"
BANDA_CAJA_LUZ = "#2f5e4c"
BANDA_BORDE = "#6f8f81"
BANDA_TEXTO = "#eef4f0"
BANDA_TEXTO_SUAVE = "#c9dcd2"

TEMAS = {
    "claro": dict(fondo="#f6f8f7", borde="#dde4e0", linea="#e4eae7", tinta="#1f2623",
                  suave="#56615c", ambar="#9a6400", musgo="#2d6a4f"),
    "oscuro": dict(fondo="#121a17", borde="#26342e", linea="#1e2a25", tinta="#e6eeea",
                   suave="#9aa8a2", ambar="#d9a441", musgo="#5fae86"),
}


def num(v):
    s = f"{v:.1f}"
    s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Fuente:
    def __init__(self, peso):
        tt = TTFont(AQUI / "fuentes" / f"plex-sans-{peso}.woff2")
        tt.flavor = None
        buf = io.BytesIO()
        tt.save(buf)
        datos = buf.getvalue()
        self.tt = TTFont(io.BytesIO(datos))
        self.glifos = self.tt.getGlyphSet()
        self.orden = self.tt.getGlyphOrder()
        self.upm = self.tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(datos))

    def _componer(self, texto):
        buf = hb.Buffer()
        buf.add_str(texto)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions

    def ancho(self, texto, tam):
        _, pos = self._componer(texto)
        return sum(p.x_advance for p in pos) * tam / self.upm

    def trazo(self, texto, x, y, tam, alinear="izq"):
        infos, pos = self._componer(texto)
        e = tam / self.upm
        if alinear == "der":
            x -= self.ancho(texto, tam)
        pen = SVGPathPen(self.glifos, ntos=num)
        avance = 0
        for info, p in zip(infos, pos):
            t = TransformPen(pen, (e, 0, 0, -e, x + (avance + p.x_offset) * e, y - p.y_offset * e))
            self.glifos[self.orden[info.codepoint]].draw(t)
            avance += p.x_advance
        return pen.getCommands()


F400, F500, F600 = Fuente(400), Fuente(500), Fuente(600)


def cabe(fuente, texto, tam, ancho, donde):
    if fuente.ancho(texto, tam) > ancho:
        raise SystemExit(f'"{texto}" no cabe en {donde}. Acórtalo en perfil.toml.')


def pedir(url, intentos=3):
    """Devuelve el contenido de url, o None si no existe o es privado (404)."""
    cabeceras = {"User-Agent": "perfil-Mafallout"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        cabeceras["Authorization"] = f"Bearer {token}"
        cabeceras["Accept"] = "application/vnd.github+json"
    for intento in range(intentos):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=cabeceras), timeout=20) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            error = e
        except (urllib.error.URLError, TimeoutError) as e:
            error = e
        time.sleep(5 * (intento + 1))
    # Mejor no tocar nada que dibujar una tarjeta sin fechas por un fallo pasajero
    raise SystemExit(f"No he podido leer {url}: {error}")


def fecha_repo(repo):
    datos = pedir(f"https://api.github.com/repos/{repo}/commits?per_page=1")
    commits = json.loads(datos) if datos else []
    if not commits:
        return None
    instante = datetime.fromisoformat(commits[0]["commit"]["committer"]["date"].replace("Z", "+00:00"))
    return instante.astimezone(MADRID)


def fecha_rss(url):
    datos = pedir(url)
    if not datos:
        return None
    fechas = [email.utils.parsedate_to_datetime(p.text) for p in ET.fromstring(datos).iter("pubDate")]
    return max(fechas).astimezone(MADRID) if fechas else None


def cabecera(datos):
    W, H = 900, 278
    nombre, lema, cajas = datos["nombre"], datos["lema"], datos["caja"]
    if len(cajas) != 3:
        raise SystemExit("La cabecera necesita exactamente tres cajas en perfil.toml.")
    cx = [48, 350, 652]
    cy, cw, ch = 152, 200, 84
    ly = cy + ch / 2
    cabe(F600, nombre, 46, W - 96, "el nombre de la cabecera")
    cabe(F400, lema, 23, W - 96, "el lema de la cabecera")
    for caja in cajas:
        cabe(F600, caja["titulo"], 25, cw - 40, "una caja de la cabecera")
        cabe(F400, caja["detalle"], 19, cw - 40, "una caja de la cabecera")

    camino = ", ".join(c["titulo"] for c in cajas)
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">',
        f"<title id=\"t\">{nombre}. {lema}. Esquema: {camino}.</title>",
        # Ciclo de 8,5 s: el punto sale de la primera caja, entra en la segunda,
        # que se ilumina, sigue hasta la tercera y descansa unos 5 s.
        "<style>",
        ".bx{animation:on .45s ease-out both}",
        ".ln{stroke-dasharray:100;animation:draw .45s cubic-bezier(.45,0,.2,1) both}",
        ".ah{animation:on .2s ease-out both}",
        ".pt,.luz{opacity:0;animation:8.5s linear 2s infinite}",
        ".pt1{animation-name:pt1}.pt2{animation-name:pt2}",
        ".luz0{animation-name:luz0}.luz1{animation-name:luz1}.luz2{animation-name:luz2}",
        "@keyframes on{from{opacity:0}to{opacity:1}}",
        "@keyframes draw{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}",
        "@keyframes luz0{0%{opacity:0}2%,7%{opacity:1}11%,100%{opacity:0}}",
        "@keyframes pt1{0%,4%{transform:translateX(0);opacity:0}5.5%{opacity:1}14%{transform:translateX(96px);opacity:1}15%,100%{transform:translateX(96px);opacity:0}}",
        "@keyframes luz1{0%,14%{opacity:0}16%,22%{opacity:1}26%,100%{opacity:0}}",
        "@keyframes pt2{0%,22%{transform:translateX(0);opacity:0}23.5%{opacity:1}32%{transform:translateX(96px);opacity:1}33%,100%{transform:translateX(96px);opacity:0}}",
        "@keyframes luz2{0%,32%{opacity:0}34%,40%{opacity:1}44%,100%{opacity:0}}",
        "@media (prefers-reduced-motion:reduce){.bx,.ln,.ah{animation:none}.pt,.luz{animation:none;opacity:0}}",
        "</style>",
        f'<rect width="{W}" height="{H}" rx="14" fill="{PINO}"/>',
        f'<path fill="{BANDA_TEXTO}" d="{F600.trazo(nombre, 47, 82, 46)}"/>',
        f'<path fill="{BANDA_TEXTO_SUAVE}" d="{F400.trazo(lema, 49, 119, 23)}"/>',
    ]
    # Conexiones de borde a borde, con la flecha hacia donde va la consulta
    for i, retraso in enumerate((0.55, 0.95)):
        x1, x2 = cx[i] + cw + 1, cx[i + 1] - 1
        p.append(f'<line class="ln" style="animation-delay:{retraso}s" x1="{num(x1)}" y1="{num(ly)}" x2="{num(x2 - 1)}" y2="{num(ly)}" stroke="{LIQUEN}" stroke-width="1.6"/>')
        p.append(f'<path class="ah" style="animation-delay:{retraso + 0.4:.2f}s" d="M{num(x2 - 9)} {num(ly - 6)}L{num(x2 - 1.5)} {num(ly)}L{num(x2 - 9)} {num(ly + 6)}" fill="none" stroke="{LIQUEN}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, (caja, retraso) in enumerate(zip(cajas, (0.2, 0.6, 1.0))):
        x = cx[i]
        p.append(f'<g class="bx" style="animation-delay:{retraso}s">')
        p.append(f'<rect x="{x}" y="{cy}" width="{cw}" height="{ch}" rx="10" fill="{BANDA_CAJA}" stroke="{BANDA_BORDE}" stroke-width="1.5"/>')
        p.append(f'<rect class="luz luz{i}" x="{x + 0.75}" y="{cy + 0.75}" width="{cw - 1.5}" height="{ch - 1.5}" rx="9.3" fill="{BANDA_CAJA_LUZ}"/>')
        p.append(f'<path fill="{BANDA_TEXTO}" d="{F600.trazo(caja["titulo"], x + 20, cy + 37, 25)}"/>')
        p.append(f'<path fill="{BANDA_TEXTO_SUAVE}" d="{F400.trazo(caja["detalle"], x + 20, cy + 66, 19)}"/>')
        p.append("</g>")
    for i in range(2):
        p.append(f'<circle class="pt pt{i + 1}" cx="{num(cx[i] + cw + 2)}" cy="{num(ly)}" r="4.5" fill="{BANDA_TEXTO}"/>')
    p.append("</svg>")
    return "\n".join(p) + "\n"


def estado(proyectos, tema):
    c = TEMAS[tema]
    W = 820
    filas = []
    for pr in proyectos:
        filas.append((pr, 80 if pr.get("fecha_texto") else 62))
    H = sum(alto for _, alto in filas)

    resumen = "; ".join(
        f'{pr["nombre"]} {pr["texto"].lower()}' + (f', {pr["fecha_texto"].lower()}' if pr.get("fecha_texto") else "")
        for pr, _ in filas
    )
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">',
        f'<title id="t">Estado: {resumen}.</title>',
        "<style>",
        ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.8s ease-out infinite}",
        "@keyframes pulse{0%{transform:scale(1);opacity:.55}70%,100%{transform:scale(2.6);opacity:0}}",
        "@media (prefers-reduced-motion:reduce){.pulse{animation:none;opacity:0}}",
        "</style>",
        f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="12" fill="{c["fondo"]}" stroke="{c["borde"]}" stroke-width="1.5"/>',
    ]
    y = 0
    latido = 0
    for i, (pr, alto) in enumerate(filas):
        if i:
            p.append(f'<line x1="24" y1="{y}" x2="796" y2="{y}" stroke="{c["linea"]}" stroke-width="1.5"/>')
        centro = y + (29 if pr.get("fecha_texto") else alto / 2)
        if pr["estado"] == "en-construccion":
            color = c["ambar"]
            p.append(f'<circle cx="44" cy="{num(centro)}" r="5.5" fill="none" stroke="{color}" stroke-width="2.2"/>')
        else:
            color = c["musgo"]
            p.append(f'<circle class="pulse" style="animation-delay:{latido * 0.7:.1f}s" cx="44" cy="{num(centro)}" r="6" fill="none" stroke="{color}" stroke-width="2"/>')
            p.append(f'<circle cx="44" cy="{num(centro)}" r="6" fill="{color}"/>')
            latido += 1
        p.append(f'<path fill="{c["tinta"]}" d="{F600.trazo(pr["nombre"], 70, centro + 7.7, 22)}"/>')
        p.append(f'<path fill="{color}" d="{F500.trazo(pr["texto"], 790, centro + 6.6, 19, alinear="der")}"/>')
        if pr.get("fecha_texto"):
            p.append(f'<path fill="{c["suave"]}" d="{F400.trazo(pr["fecha_texto"], 70, y + 60, 16)}"/>')
        y += alto
    p.append("</svg>")
    return "\n".join(p) + "\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    datos = tomllib.loads((RAIZ / "perfil.toml").read_text(encoding="utf-8"))
    proyectos = datos["proyecto"]
    for pr in proyectos:
        if pr["estado"] not in ("funciona", "en-construccion"):
            raise SystemExit(f'Estado desconocido en "{pr["nombre"]}": usa "funciona" o "en-construccion".')
        cabe(F600, pr["nombre"], 22, 440, "una fila de la tarjeta")
        cabe(F500, pr["texto"], 19, 260, "una fila de la tarjeta")
        if pr.get("repo"):
            fecha = fecha_repo(pr["repo"])
            pr["fecha_texto"] = fecha and f"Último cambio: {fecha:%d/%m/%Y}"
        elif pr.get("rss"):
            fecha = fecha_rss(pr["rss"])
            pr["fecha_texto"] = fecha and f"Última entrada: {fecha:%d/%m/%Y}"

    assets = RAIZ / "assets"
    (assets / "cabecera.svg").write_text(cabecera(datos["cabecera"]), encoding="utf-8", newline="\n")
    for tema in TEMAS:
        (assets / f"estado-{tema}.svg").write_text(estado(proyectos, tema), encoding="utf-8", newline="\n")
    for pr in proyectos:
        print(f'{pr["nombre"]}: {pr["texto"]}' + (f' ({pr["fecha_texto"]})' if pr.get("fecha_texto") else ""))


if __name__ == "__main__":
    main()
