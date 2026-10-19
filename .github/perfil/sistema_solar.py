"""Cabecera del perfil: el sistema solar de Outer Wilds de mi esfera del reloj, en un bucle que acaba en supernova.

Las funciones de dibujo de uid a quantum son las de la esfera, sin cambios.
"""
import math
import random

CX, CY = 240, 346
# Tamaños de la versión final de la esfera
KS = {"timber": 0.95, "brittle": 1.36, "giant": 2.08, "bramble": 0.89}
COL = {"twins": "#e0883a", "timber": "#3b86a8", "brittle": "#9a8a94", "giant": "#3fae8f", "bramble": "#9a6a42"}
_n = [0]


def uid(p="u"):
    _n[0] += 1
    return f"{p}{_n[0]}"


def base(x, y, r, color):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}"/>'


def clipg(x, y, s, r, inner):
    i = uid("c")
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})"><clipPath id="{i}"><circle r="{r}"/></clipPath>'
            f'<g clip-path="url(#{i})">{inner}</g></g>')


def p_timber(x, y, s=1, sun=None):
    r = 10.5 * s
    out = base(x, y, r, "#3b86a8")
    out += clipg(x, y, s, 10.5,
        '<path d="M-8,-3 q4,-6 9,-3 q3,3 -1,6 q-4,3 -8,-3z" fill="#6bbf6e"/>'
        '<path d="M2,5 q5,-2 8,2 q-3,5 -8,1z" fill="#6bbf6e"/>'
        '<ellipse cx="0" cy="-10" rx="5" ry="2" fill="#eaf4f8" opacity=".85"/>')
    out += shade(x, y, r, sun)
    # Attlerock
    out += f'<circle cx="{x+15*s:.1f}" cy="{y-8*s:.1f}" r="{2.8*s:.1f}" fill="#b5a99a"/>'
    return out


def p_brittle(x, y, s=1, sun=None):
    r = 11 * s
    out = base(x, y, r, "#8a7d86")
    out += clipg(x, y, s, 11,
        '<ellipse cx="0" cy="-10.5" rx="8.4" ry="4.4" fill="#e9f1f8"/>'
        '<ellipse cx="0" cy="11" rx="5.6" ry="2.6" fill="#e9f1f8" opacity=".9"/>'
        '<path d="M-9,-2 L-4,0 L-6,4 L0,6 L-1,10" fill="none" stroke="#2b2330" stroke-width=".85" stroke-linejoin="round"/>'
        '<path d="M3,-6 L5,-1 L10,1" fill="none" stroke="#2b2330" stroke-width=".85" stroke-linejoin="round"/>'
        '<circle cx="-4" cy="0" r=".7" fill="#7cc4ff"/><circle cx="5" cy="-1" r=".7" fill="#7cc4ff"/>')
    out += shade(x, y, r, sun)
    # fragmentos de corteza cayendo
    out += (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})" fill="#8a7d86">'
            '<path d="M12.6,-3 L14.8,-4.2 L14.2,-1.6Z"/><path d="M-12.2,5.6 L-14,4.2 L-13.8,6.8Z"/></g>')
    # Hollow's Lantern
    lx, ly = x + 18 * s, y - 11 * s
    out += (f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{6.2*s:.1f}" fill="#ff7a2f" opacity=".3"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{3.2*s:.1f}" fill="#ff8a3a"/>'
            f'<circle cx="{lx-.8*s:.1f}" cy="{ly-.8*s:.1f}" r="{1.3*s:.1f}" fill="#ffd08a"/>')
    return out


def p_giant(x, y, s=1, sun=None):
    r = 13 * s
    out = base(x, y, r, "#3fae8f")
    out += clipg(x, y, s, 13,
        '<g fill="none" stroke-linecap="round">'
        '<path d="M-15,-5 q7,-4 15,-1 t15,-1" stroke="#9fe3c8" stroke-width="2.2" opacity=".8"/>'
        '<path d="M-15,3 q7,-4 15,-1 t15,-1" stroke="#2c8c74" stroke-width="2.6" opacity=".85"/>'
        '<path d="M-15,9 q7,-3 15,-1 t15,-1" stroke="#9fe3c8" stroke-width="1.8" opacity=".6"/></g>'
        '<ellipse cx="5" cy="8" rx="2.6" ry="1.2" fill="#e0cf9e"/>'
        '<circle cx="-4" cy="-8" r="2.2" fill="none" stroke="#e8fff6" stroke-width=".9" opacity=".8"/>')
    out += shade(x, y, r, sun)
    return out


def shard(cx, cy, ang, L, w, seed):
    r = random.Random(seed)
    j = lambda v: v * (1 + r.uniform(-.1, .1))
    H = [(0, -L/2), (j(w*.85), -L*.22), (j(w), L*.22), (0, L/2), (-j(w), L*.22), (-j(w*.85), -L*.22)]
    f = lambda pts: " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    left = [H[0], H[5], H[4], H[3], (0, -L*.05)]
    right = [H[0], H[1], H[2], H[3], (0, -L*.05)]
    top = [(0, -L/2), (-w*.4, -L*.3), (w*.3, -L*.3)]
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang})">'
            f'<polygon points="{f(left)}" fill="#a6dff6"/><polygon points="{f(right)}" fill="#4a9be0"/>'
            f'<polygon points="{f(top)}" fill="#e8f9ff" opacity=".85"/>'
            f'<polygon points="{f(H)}" fill="none" stroke="#2f6fb8" stroke-width=".7" stroke-linejoin="round"/></g>')


def p_bramble(x, y, s=1, sun=None):
    # (cx, cy, rot, L, w): losas de hielo irregulares alrededor de un nudo de lianas con chispas doradas
    SH = [(-19, -15, -40, 20, 7.5), (17, -19, 30, 13, 5.5), (-26, 3, 85, 12, 5), (23, 9, -25, 21, 8),
          (3, 26, 4, 22, 7.5), (-17, 19, 40, 18, 7.5), (2, -26, -12, 10, 4.2), (27, -4, 70, 9, 3.6)]
    rr = random.Random(4)
    g = ""
    for sx, sy, *_ in SH:
        mx, my = sx * .45 + sy * .25 + rr.uniform(-3, 3), sy * .45 - sx * .25 + rr.uniform(-3, 3)
        d = f"M0,0 Q{mx:.1f},{my:.1f} {sx*.78:.1f},{sy*.78:.1f}"
        g += f'<path d="{d}" fill="none" stroke="#231c12" stroke-width="2.6" stroke-linecap="round"/>'
        g += f'<path d="{d}" fill="none" stroke="#5c4d31" stroke-width="1.1" stroke-linecap="round"/>'
    for k, (sx, sy, a, L, w) in enumerate(SH):
        g += shard(sx, sy, a, L, w, k)
    g += '<circle r="8.5" fill="#231c12"/>'
    for d in ("M-7,-2 C-2,-8 3,6 7,1", "M-6,4 C-1,-1 4,9 8,-3", "M-3,-7 C-8,0 -2,7 3,8", "M2,-8 C8,-3 6,5 0,8",
              "M-8,1 C-3,4 2,-6 6,-5", "M-4,8 C0,2 5,2 8,5"):
        g += f'<path d="{d}" fill="none" stroke="#6e5c38" stroke-width="1.4" stroke-linecap="round"/>'
    for k in range(10):
        a = math.radians(k * 36 + rr.uniform(-8, 8))
        t0, t1 = a - .2, a + .2
        L_ = rr.uniform(8.5, 12)
        g += (f'<path d="M{5*math.cos(t0):.2f},{5*math.sin(t0):.2f} L{L_*math.cos(a):.2f},{L_*math.sin(a):.2f} '
              f'L{5*math.cos(t1):.2f},{5*math.sin(t1):.2f}Z" fill="#e8d28a" opacity=".85"/>')
    g += '<circle r="3.4" fill="#ffd36b" opacity=".35"/><circle r="1.5" fill="#fff1b8" opacity=".9"/>'
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">{g}</g>'


def comet(hx, hy):
    dx, dy = hx - CX, hy - CY
    n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
    px, py = -dy, dx
    L = 40
    ex, ey = hx + dx * L, hy + dy * L
    i = uid("g")
    return (f'<linearGradient id="{i}" gradientUnits="userSpaceOnUse" x1="{hx}" y1="{hy}" x2="{ex:.1f}" y2="{ey:.1f}">'
            f'<stop offset="0" stop-color="#d4eaff" stop-opacity=".95"/><stop offset="1" stop-color="#86bcff" stop-opacity="0"/></linearGradient>'
            f'<path d="M{hx+px*2.6:.1f},{hy+py*2.6:.1f} L{ex:.1f},{ey:.1f} L{hx-px*2.6:.1f},{hy-py*2.6:.1f}Z" fill="url(#{i})"/>'
            f'<circle cx="{hx}" cy="{hy}" r="3" fill="#e2f0ff"/>')


def quantum(x, y):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="none" stroke="#cfc6ff" stroke-width=".8" opacity=".4" stroke-dasharray="1.5 1.5"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="#d9d2ff"/>')


def shade(*args, **kwargs):
    # La sombra va aparte, en un grupo que gira hacia el sol mientras el planeta orbita
    return ""


# El bucle dura 220 s (22 x 10): al final el sol explota y todo vuelve a empezar exactamente igual
BUCLE = 220
# Cuatro eclipses de 44 s, y los últimos 44 s son la gigante roja y la supernova
ECLIPSE = 44
DIA = ("#FFD9A0", "#FF9448", "#FF7A30")
TARDE = ("#FFC58F", "#FF7A3C", "#E8552B")
GIGANTE = ("#FFB98A", "#E8552B", "#A82E1A")
RX = {"twins": 120, "timber": 146, "brittle": 166, "giant": 184, "bramble": 232}
RADIO = {"timber": 10.5 * KS["timber"], "brittle": 11 * KS["brittle"], "giant": 13 * KS["giant"]}
# Movimiento de la esfera: ángulo = 360 * fract(f0 + m / T). Aquí un minuto de la esfera dura 7,5 s
# y se empieza en las 21:18, la colocación de la captura que compartí.
F0 = {"twins": 0.222, "timber": 0.722, "brittle": 0.208, "giant": 0.708, "bramble": 0.25}
T_ESFERA = {"twins": 8, "timber": 8, "brittle": 20, "giant": 20, "bramble": 38}
SEG_MIN, M0 = 7.5, 21 * 60 + 18
FASE0 = {k: (F0[k] + M0 / T_ESFERA[k]) % 1 for k in F0}
# Luna cuántica a r + 11 del planeta, o r + 26 en el Abismo para quedar por fuera del cañón
LUNA = {k: (r + d, -round(.35 * (r + d))) for k, r, d in (("timber", 10, 11), ("brittle", 15, 11), ("giant", 27, 26))}
# Interloper: elipse muy estirada con el sol en un foco. Pasa rozando el sol y se aleja más allá de Rama Oscura.
PERIHELIO, AFELIO, EJE, T_COMETA, PASO_COMETA = 40, 330, 160, 95, 60
# Espacio que ocupa cada cuerpo con sus lunas y piezas, para saber cuándo se pisan dos
HUECO = {"twins": 25, "timber": 24, "brittle": 37, "giant": 56, "bramble": 33, "comet": 10}
CUERPOS = ["twins", "timber", "brittle", "giant", "bramble", "comet"]
# Cañón orbital: (fase, rx, ry, escala) de cada pieza y dónde va cuando está montado, respecto al módulo
CANON = [(0.10, 40, 16, 1.0), (0.17, 43, 17, 1.0), (0.25, 37, 15, 0.7)]
MONTADO = [(0, 0, 0), (11, -0.4, 90), (19.5, -0.7, 90)]
DISPARO, ROTURA = 2.2, (2.4, 6.5)
# Viajeros tocando junto al fuego: cuerpo, sitio respecto a su centro (px de la esfera) y golpes dentro de 8,8 s
VIAJEROS = [
    ("twins", (-15, 2), (0, .5)),        # Chert, tambores, en Ember Twin
    ("timber", (14.25, -7.6), (1.76,)),  # Esker, silbido, en Attlerock
    ("brittle", (0, 0), (3.52,)),        # Riebeck, banjo, en Hondonada Frágil
    ("giant", (0, 0), (5.28,)),          # Gabbro, flauta, en el Abismo del Gigante
    ("bramble", (0, 0), (7.04,)),        # Feldspar, armónica, en Rama Oscura
]
# Llamaradas en el borde del sol: segundo del bucle y ángulo
LLAMARADAS = [(15, 205), (98, 330), (141, 70)]
DT = .1


def num(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pc(t, periodo):
    return f"{100 * t / periodo:.4f}".rstrip("0").rstrip(".") + "%"


def seg(v):
    return f"{v:g}"


def suave(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def tramos(t, puntos):
    """Valor en t de una línea de puntos (segundo, valor), con transiciones suaves entre ellos."""
    if t <= puntos[0][0]:
        return puntos[0][1]
    for (t0, v0), (t1, v1) in zip(puntos, puntos[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * suave((t - t0) / (t1 - t0)) if t1 > t0 else v1
    return puntos[-1][1]


def continuos(grados):
    out = [grados[0]]
    for v in grados[1:]:
        while v - out[-1] > 180:
            v -= 360
        while v - out[-1] < -180:
            v += 360
        out.append(v)
    return out


def simplificar(m, tol):
    """Douglas-Peucker: deja solo los puntos que hacen falta para que la interpolación lineal no se aparte más de tol."""
    claves, pila = {0, len(m) - 1}, [(0, len(m) - 1)]
    while pila:
        i, j = pila.pop()
        (t0, a), (t1, b) = m[i], m[j]
        peor, kpeor = 1.0, None
        for k in range(i + 1, j):
            t, v = m[k]
            u = (t - t0) / (t1 - t0)
            e = max(abs(a[q] + (b[q] - a[q]) * u - v[q]) / tol[q] for q in range(len(tol)))
            if e > peor:
                peor, kpeor = e, k
        if kpeor is not None:
            claves.add(kpeor)
            pila += [(i, kpeor), (kpeor, j)]
    return [m[k] for k in sorted(claves)]


def tiempos(duracion=BUCLE):
    n = round(duracion / DT)
    return [duracion * k / n for k in range(n + 1)]


class Svg:
    def __init__(self, W, H, titulo):
        self.W, self.H, self.titulo = W, H, titulo
        self.css, self.defs, self.cuerpo = [], [], []

    def animar(self, nombre, valores, css, tol, duracion=BUCLE, base=None):
        """Keyframes a partir de valores muestreados cada DT segundos a lo largo de la duración."""
        n = len(valores) - 1
        m = simplificar([(duracion * k / n, v) for k, v in enumerate(valores)], tol)
        cuerpo = "".join(f"{pc(t, duracion)}{{{css(*v)}}}" for t, v in m)
        self.css += [f"@keyframes {nombre}{{{cuerpo}}}",
                     f".{nombre}{{{css(*valores[0]) if base is None else base};animation:{nombre} {seg(duracion)}s linear infinite}}"]

    def fin(self):
        return "\n".join([
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W} {self.H}" width="{self.W}" height="{self.H}" role="img" aria-labelledby="t">',
            f'<title id="t">{self.titulo}</title>',
            "<style>", *self.css, "@media (prefers-reduced-motion:reduce){*{animation:none!important}}", "</style>",
            "<defs>", f'<clipPath id="banda"><rect width="{self.W}" height="{self.H}" rx="14"/></clipPath>', *self.defs, "</defs>",
            '<g clip-path="url(#banda)">', *self.cuerpo, "</g>", "</svg>"]) + "\n"


def estrellas(s, semilla, n, evitar):
    rnd = random.Random(semilla)
    s.css += ["@keyframes tw{0%{opacity:1}50%{opacity:.25}100%{opacity:1}}", ".tw{animation:tw 4.4s ease-in-out infinite}"]
    k = 0
    while k < n:
        x, y = rnd.uniform(10, s.W - 10), rnd.uniform(8, s.H - 8)
        if evitar(x, y):
            continue
        r = rnd.choice([0.7, 0.9, 1.1, 1.4])
        c = rnd.choice(["#cfd6ff", "#cfd6ff", "#ffd9a8"])
        o = rnd.uniform(.25, .7)
        clase = f' class="tw" style="animation-delay:{-rnd.uniform(0, 4.4):.1f}s"' if k % 7 == 0 else ""
        s.cuerpo.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}" opacity="{o:.2f}"{clase}/>')
        k += 1


def estrellas_que_mueren(s, zonas, semilla=3, vidas=5, T=22):
    """Como en la esfera: cada estrella aparece, se hincha, estalla en un anillo y la siguiente sale en otro sitio."""
    rnd = random.Random(semilla)
    total = vidas * T
    for k in range(len(zonas)):
        desfase = -T * k / len(zonas)
        sitios = []
        for j in range(vidas):
            zx, zy, zw, zh = zonas[(k + j) % len(zonas)]
            sitios.append((zx + zw * rnd.random(), zy + zh * rnd.random()))
        nucleo, anillo = [], []
        for j, (x, y) in enumerate(sitios):
            t0 = j * T
            sitio = f"translate({x:.1f}px,{y:.1f}px)"
            nucleo += [f"{pc(t0, total)}{{transform:{sitio} scale(1);opacity:0}}",
                       f"{pc(t0 + .08 * T, total)}{{transform:{sitio} scale(1);opacity:1}}",
                       f"{pc(t0 + .78 * T, total)}{{transform:{sitio} scale(1);opacity:1}}",
                       f"{pc(t0 + .879 * T, total)}{{transform:{sitio} scale(2.1);opacity:1}}",
                       f"{pc(t0 + .88 * T, total)}{{transform:{sitio} scale(2.1);opacity:0}}"]
            anillo += [f"{pc(t0, total)},{pc(t0 + .86 * T, total)}{{transform:{sitio} scale(.15);opacity:0}}",
                       f"{pc(t0 + .861 * T, total)}{{transform:{sitio} scale(.15);opacity:.9}}",
                       f"{pc(t0 + .999 * T, total)}{{transform:{sitio} scale(1);opacity:0}}"]
        nucleo.append(f"100%{{transform:translate({sitios[0][0]:.1f}px,{sitios[0][1]:.1f}px) scale(1);opacity:0}}")
        s.css += [f"@keyframes nucleo{k}{{{''.join(nucleo)}}}", f"@keyframes anillo{k}{{{''.join(anillo)}}}",
                  f".nucleo{k}{{opacity:0;animation:nucleo{k} {total}s linear {desfase:.2f}s infinite}}",
                  f".anillo{k}{{opacity:0;animation:anillo{k} {total}s linear {desfase:.2f}s infinite}}"]
        s.cuerpo += [f'<circle class="nucleo{k}" r="1.6" fill="#E8EEFF"/>',
                     f'<circle class="anillo{k}" r="9" fill="none" stroke="#CFE3FF" stroke-width="1.2"/>']


def en_eclipse(t, plantilla, fuera):
    """Valor de una plantilla (fracción del eclipse, valor) en los cuatro primeros tramos de 44 s. En el último, fuera."""
    k = int(t // ECLIPSE)
    if k >= 4:
        return fuera
    return tramos(t - k * ECLIPSE, [(u * ECLIPSE, v) for u, v in plantilla])


def parpadeo(t, plantilla):
    """Como en_eclipse, pero con cambios bruscos: el parpadeo de la linterna al empezar la noche."""
    k = int(t // ECLIPSE)
    if k >= 4:
        return 0
    u = (t - k * ECLIPSE) / ECLIPSE
    if u <= plantilla[0][0] or u >= plantilla[-1][0]:
        return 0
    for (u0, v0), (u1, v1) in zip(plantilla, plantilla[1:]):
        if u <= u1:
            return v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return 0


def ojo_del_universo(semilla=22):
    """El Ojo del Universo con radio 1: mitad izquierda nomai (lavanda, laberinto angular) y derecha owlk (verde, raíces)."""
    rnd = random.Random(semilla)
    lavanda, verde, hueco = "#a196ff", "#3dfaa3", "#06071a"

    def pincho(ang, largo, ancho, color, r0=.19):
        a = math.radians(ang)
        ux, uy, px, py = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        bx, by = r0 * ux, r0 * uy
        return (f'<path d="M{bx + px * ancho:.3f},{by + py * ancho:.3f} L{largo * ux:.3f},{largo * uy:.3f} '
                f'L{bx - px * ancho:.3f},{by - py * ancho:.3f}Z" fill="{color}"/>')

    def espina(ang, largo, color):
        out = ""
        a = math.radians(ang)
        for _ in range(rnd.randint(1, 3)):
            d = largo * rnd.uniform(.35, .7)
            lado = rnd.choice((-1, 1))
            b = a + lado * math.radians(rnd.uniform(28, 50))
            x0, y0 = d * math.cos(a), d * math.sin(a)
            L = largo * rnd.uniform(.1, .2)
            px, py = -math.sin(a) * .012, math.cos(a) * .012
            out += (f'<path d="M{x0 + px:.3f},{y0 + py:.3f} L{x0 + L * math.cos(b):.3f},{y0 + L * math.sin(b):.3f} '
                    f'L{x0 - px:.3f},{y0 - py:.3f}Z" fill="{color}"/>')
        return out

    def muesca(ang, largo, color):
        # Los pinchos nomai llevan dientes en ángulo recto, no ramitas como los owlk
        a = math.radians(ang)
        ux, uy, px, py = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        lado = rnd.choice((-1, 1))
        d, w, h = largo * rnd.uniform(.45, .6), .022, .05
        x0, y0 = d * ux, d * uy
        return (f'<path d="M{x0:.3f},{y0:.3f} L{x0 + lado * px * h:.3f},{y0 + lado * py * h:.3f} '
                f'L{x0 + lado * px * h + ux * w:.3f},{y0 + lado * py * h + uy * w:.3f} L{x0 + ux * w * 2.4:.3f},{y0 + uy * w * 2.4:.3f}Z" fill="{color}"/>')

    p = ['<defs>'
         f'<radialGradient id="ojo-nomai" cx="-.18" cy="0" r=".62" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{lavanda}" stop-opacity=".42"/><stop offset="1" stop-color="{lavanda}" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="ojo-owlk" cx=".18" cy="0" r=".68" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{verde}" stop-opacity=".45"/><stop offset="1" stop-color="{verde}" stop-opacity="0"/></radialGradient>'
         '</defs>',
         '<circle cx="-.18" r=".62" fill="url(#ojo-nomai)"/>',
         '<circle cx=".18" r=".68" fill="url(#ojo-owlk)"/>']
    # Pinchos: largos y cortos alternados, como en el juego
    nomai = [(92, .78), (108, .32), (122, .5), (136, .62), (149, .3), (160, .44), (172, .38), (180, .98), (192, .3), (205, .4), (218, .55), (232, .3), (243, .82), (258, .36), (268, .8)]
    owlk = [(-86, .62), (-72, .34), (-58, .4), (-41, 1.0), (-28, .3), (-17, .55), (-4, .3), (2, 1.0), (14, .36), (27, .62), (33, .9), (46, .42), (58, .55), (66, .95), (80, .4)]
    for ang, largo in nomai:
        ang += rnd.uniform(-2, 2)
        p.append(pincho(ang, largo, rnd.uniform(.018, .032), lavanda))
        if largo > .45:
            p.append(muesca(ang, largo, lavanda))
    for ang, largo in owlk:
        ang += rnd.uniform(-2, 2)
        p.append(pincho(ang, largo, rnd.uniform(.02, .036), verde))
        p.append(espina(ang, largo, verde))
    # Centro: a la izquierda un laberinto de líneas rectas lavanda y a la derecha una maraña de raíces verdes
    r = .3
    p.append(f'<path d="M0,{-r} A{r},{r} 0 0 0 0,{r}Z" fill="{lavanda}" opacity=".12"/><path d="M0,{-r} A{r},{r} 0 0 1 0,{r}Z" fill="{verde}" opacity=".12"/>')
    laberinto = []
    for _ in range(64):
        x, y = rnd.uniform(-.28, -.02), rnd.uniform(-.27, .27)
        if x * x + y * y > (r - .02) ** 2:
            continue
        tramos_ = [(x, y)]
        dx, dy = rnd.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        for _ in range(rnd.randint(2, 6)):
            paso = rnd.choice((.025, .035, .05))
            nx, ny = x + dx * paso, y + dy * paso
            if nx > -.015 or nx * nx + ny * ny > (r - .02) ** 2:
                break
            x, y = nx, ny
            tramos_.append((x, y))
            dx, dy = (dy, dx) if rnd.random() < .5 else (-dy, -dx)
        if len(tramos_) > 1:
            laberinto.append("M" + " L".join(f"{a:.3f},{b:.3f}" for a, b in tramos_))
    p.append(f'<path d="{" ".join(laberinto)}" fill="none" stroke="{lavanda}" stroke-width=".02" stroke-linecap="square" stroke-linejoin="miter"/>')
    raices = []
    for _ in range(60):
        a0 = rnd.uniform(-1.45, 1.45)
        d0 = rnd.uniform(.03, .27)
        x0, y0 = max(.02, d0 * math.cos(a0)), d0 * math.sin(a0)
        x1, y1 = x0 + rnd.uniform(-.08, .08), y0 + rnd.uniform(-.08, .08)
        if x1 < .02 or x1 * x1 + y1 * y1 > (r - .01) ** 2:
            continue
        cx, cy = (x0 + x1) / 2 + rnd.uniform(-.05, .05), (y0 + y1) / 2 + rnd.uniform(-.05, .05)
        raices.append(f"M{x0:.3f},{y0:.3f} Q{max(.02, cx):.3f},{cy:.3f} {x1:.3f},{y1:.3f}")
    p.append(f'<path d="{" ".join(raices)}" fill="none" stroke="{verde}" stroke-width=".02" stroke-linecap="round"/>')
    # Bordes irregulares del disco owlk: raicillas que salen del centro
    for _ in range(18):
        a = math.radians(rnd.uniform(-85, 85))
        d, L = r - .01, rnd.uniform(.04, .1)
        b = a + math.radians(rnd.uniform(-35, 35))
        px, py = -math.sin(a) * .016, math.cos(a) * .016
        x0, y0 = d * math.cos(a), d * math.sin(a)
        p.append(f'<path d="M{x0 + px:.3f},{y0 + py:.3f} L{x0 + L * math.cos(b):.3f},{y0 + L * math.sin(b):.3f} L{x0 - px:.3f},{y0 - py:.3f}Z" fill="{verde}"/>')
    p.append(f'<circle r=".085" fill="{hueco}"/><circle r=".12" fill="none" stroke="{hueco}" stroke-width=".02" opacity=".35"/>')
    return "".join(p)


class Sistema:
    def __init__(self, s, sx, sy, g):
        self.s, self.sx, self.sy, self.g = s, sx, sy, g
        self.R = 26 * g

    # ---------------------------------------------------------------- posiciones
    def pos(self, nombre, t):
        """Posición en pantalla y escala de profundidad del cuerpo en el segundo t del bucle."""
        if nombre == "comet":
            return self.pos_cometa(t)
        a = 2 * math.pi * (FASE0[nombre] + t / (T_ESFERA[nombre] * SEG_MIN))
        rx = RX[nombre] * self.g
        return self.sx + rx * math.cos(a), self.sy + rx * .4 * math.sin(a), 1 + .18 * math.sin(a)

    def plano_cometa(self, t):
        # Ley de Kepler: el tiempo avanza igual en la anomalía media M, y E sale de M = E - e·sen(E)
        a, e = (PERIHELIO + AFELIO) / 2, (AFELIO - PERIHELIO) / (AFELIO + PERIHELIO)
        M = 2 * math.pi * (t - PASO_COMETA) / T_COMETA
        E = M
        for _ in range(30):
            E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        x, y = a * (math.cos(E) - e), a * math.sqrt(1 - e * e) * math.sin(E)
        w = math.radians(EJE)
        return x * math.cos(w) - y * math.sin(w), x * math.sin(w) + y * math.cos(w)

    def pos_cometa(self, t):
        X, Y = self.plano_cometa(t)
        return self.sx + X * self.g, self.sy + .4 * Y * self.g, 1 + .18 * Y / math.hypot(X, Y)

    def pos_canon(self, i, t):
        """Pieza i del cañón respecto al centro del Abismo, sin la escala de profundidad del planeta."""
        fase, rx, ry, _ = CANON[i]
        a = 2 * math.pi * (fase + t / 22)
        return rx * math.cos(a) * self.g, ry * math.sin(a) * self.g, a

    def montado(self, i):
        x0, y0, _ = self.pos_canon(0, 0)
        dx, dy, giro = MONTADO[i]
        return x0 + dx * self.g, y0 + dy * self.g, giro

    def boca(self):
        x0, y0, _ = self.pos_canon(0, 0)
        return x0 + 25 * self.g, y0 - .9 * self.g

    # ---------------------------------------------------------------- dibujo base
    def orbitas(self):
        for k, rx in RX.items():
            self.s.cuerpo.append(f'<ellipse cx="{self.sx}" cy="{self.sy}" rx="{rx * self.g:.1f}" ry="{rx * .4 * self.g:.1f}" fill="none" stroke="{COL[k]}" stroke-width="1.2" opacity=".5"/>')
        puntos = [self.pos_cometa(PASO_COMETA + T_COMETA * k / 180)[:2] for k in range(180)]
        self.s.cuerpo.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in puntos) + 'Z" fill="none" stroke="#bcdcff" stroke-width="1" stroke-dasharray="2 4" opacity=".22"/>')

    def arte(self):
        """Dibujo de cada cuerpo una sola vez. Las copias de cada ranura lo reutilizan con <use>."""
        g, s = self.g, self.s
        for nombre, dibujo in (("timber", p_timber), ("brittle", p_brittle), ("giant", p_giant)):
            s.defs.append(f'<g id="arte-{nombre}">{dibujo(0, 0, KS[nombre] * g)}</g>')
        s.defs.append(f'<g id="arte-bramble">{p_bramble(0, 0, KS["bramble"] * g)}</g>')
        s.defs.append(f'<g id="arte-ember">{base(0, 0, 8.3 * g, "#e0883a")}</g><g id="arte-ash">{base(0, 0, 7 * g, "#c9a574")}</g>')
        radios = dict({k: r * g for k, r in RADIO.items()}, ember=8.3 * g, ash=7 * g)
        for nombre, r in radios.items():
            s.defs.append(f'<mask id="sombra-{nombre}"><circle r="{r:.2f}" fill="#fff"/><circle cx="{r * .42:.2f}" r="{r:.2f}" fill="#000"/></mask>')
            s.defs.append(f'<circle id="oscuro-{nombre}" r="{r:.2f}" fill="#05071a" opacity=".5" mask="url(#sombra-{nombre})"/>')
        cobre, cobre_c, cobre_o = "#b87a47", "#d9a066", "#6b3f22"
        tubo = (f'<g fill="none" stroke="{cobre}" stroke-width=".8" stroke-linecap="round"><path d="M-3,-7 L-3,7 M3,-7 L3,4"/>'
                f'<path d="M-3,-7 L3,-1 M-3,-1 L3,5 M-3,5 L1,7 M3,-7 L-3,-1 M3,-1 L-3,5"/><path d="M-3,-7 H3" stroke="{cobre_c}"/></g>')
        modulo = (f'<g stroke="{cobre_o}" stroke-width=".5" stroke-linejoin="round"><path d="M-0.6,-8 L1.2,-8 L2.2,0.5 L8,2.4 L7.6,3.4 L1.6,3.2 L-2.4,5.2 L-6.5,5.6 L-1.6,1.4 Z" fill="{cobre}"/>'
                  f'<path d="M1.2,-8 L2.2,0.5 L8,2.4 L5,0.2 L2.4,-2 Z" fill="{cobre_c}" stroke="none"/><rect x="-4.8" y="-3.8" width="3.8" height="3.4" rx=".6" fill="#4f9d9a" stroke="#2f6665"/>'
                  '<circle cx="-4.4" cy="2.8" r="1.8" fill="#8d7bff" opacity=".8" stroke="none"/><circle cx="-4.4" cy="2.8" r=".7" fill="#e6e0ff" stroke="none"/></g>')
        s.defs += [f'<g id="pieza0">{modulo}</g>', f'<g id="pieza1">{tubo}</g>', f'<g id="pieza2">{tubo}</g>']
        # Interloper: núcleo de hielo azul con la cara rocosa hacia el sol, y cola azul y lavanda
        s.defs += [
            '<linearGradient id="cola-fuera"><stop offset="0" stop-color="#8fc4ff" stop-opacity=".55"/><stop offset=".5" stop-color="#7d8cff" stop-opacity=".25"/><stop offset="1" stop-color="#b6a8ff" stop-opacity="0"/></linearGradient>',
            '<radialGradient id="escarcha"><stop offset=".35" stop-color="#d8f1ff" stop-opacity=".7"/><stop offset="1" stop-color="#8fc4ff" stop-opacity="0"/></radialGradient>',
            '<linearGradient id="cola-dentro"><stop offset="0" stop-color="#eaf7ff" stop-opacity=".95"/><stop offset="1" stop-color="#6aaaff" stop-opacity="0"/></linearGradient>',
            f'<g id="arte-cola" transform="scale({g:.2f})"><path d="M0,-3.4 Q18,-8 40,-9 Q44,0 40,9 Q18,8 0,3.4Z" fill="url(#cola-fuera)"/><path d="M0,-1.9 Q20,-2.6 40,0 Q20,2.6 0,1.9Z" fill="url(#cola-dentro)"/></g>',
            f'<g id="arte-nucleo" transform="scale({g:.2f})"><circle r="3.6" fill="#9fd0ff"/><circle cx="-.9" cy="-.9" r="1.6" fill="#e6f6ff" opacity=".9"/>'
            '<path d="M0,-3.6 A3.6,3.6 0 0 1 0,3.6 A1.8,3.6 0 0 0 0,-3.6Z" fill="#6f625a"/><circle cx="2.3" cy=".6" r=".55" fill="#4f4640"/></g>',
        ]

    # ---------------------------------------------------------------- animaciones de los cuerpos
    def movimiento(self, nombre):
        """Órbita con su escala de profundidad y giro de la sombra hacia el sol, a lo largo del bucle."""
        ts = tiempos()
        P = [self.pos(nombre, t) for t in ts]
        giros = continuos([math.degrees(math.atan2(self.sy - y, self.sx - x)) for x, y, _ in P])
        self.s.animar(f"mov-{nombre}", P, lambda x, y, d: f"transform:translate({x:.1f}px,{y:.1f}px) scale({d:.3f})", (.45, .45, .005))
        self.s.animar(f"rot-{nombre}", [(v,) for v in giros], lambda v: f"transform:rotate({v:.1f}deg)", (2.5,))
        if nombre == "comet":
            # La cola sale del lado contrario al sol y se alarga cerca de él. El hielo se derrite deprisa al
            # acercarse y se vuelve a congelar despacio al alejarse (25 s tras el perihelio).
            cola, hielo = [], []
            for t, v in zip(ts, giros):
                X, Y = self.plano_cometa(t)
                r = math.hypot(X, Y)
                cerca = PERIHELIO / r
                u = min(1, ((t - PASO_COMETA) % T_COMETA) / 25)
                hielo.append((min(suave(u), max(0, min(1, (r - 45) / 65))),))
                cola.append((v + 180, (26 + 70 * cerca) / 40, .8 + .5 * cerca, .55 + .45 * cerca))
            self.s.animar("cola", cola, lambda a, sx, sy, o: f"transform:rotate({a:.1f}deg) scale({sx:.2f},{sy:.2f});opacity:{o:.2f}", (2.5, .03, .02, .02))
            self.s.animar("deshielo", [(.8 * (1 - h),) for h, in hielo], lambda o: f"opacity:{o:.2f}", (.02,))
            self.s.animar("escarcha", hielo, lambda o: f"opacity:{o:.2f}", (.02,))

    def gemelos(self):
        """La arena pasa de Ash, el clarito, a Ember, el naranja: Ash se vacía y Ember se llena durante el bucle."""
        g, s = self.g, self.s
        lleno = [min(1, t / 205) for t in tiempos()]
        s.animar("ember", [(1 + .1 * p,) for p in lleno], lambda e: f"transform:scale({e:.3f})", (.003,))
        s.animar("ash", [(1 - .36 * p,) for p in lleno], lambda e: f"transform:scale({e:.3f})", (.003,))
        s.css += [f"@keyframes grano{{0%{{transform:translate({15 * g:.1f}px,{-2 * g:.1f}px);opacity:0}}50%{{opacity:.9}}100%{{transform:translate({-15 * g:.1f}px,{2 * g:.1f}px);opacity:0}}}}",
                  ".grano{opacity:0;animation:grano 2.2s linear infinite}",
                  "@keyframes arena{from{stroke-dashoffset:0}to{stroke-dashoffset:-4}}",
                  ".arena{animation:arena 1.1s linear infinite}"]

    def canon_css(self):
        """El cañón empieza montado, dispara la sonda y se rompe en tres piezas que siguen orbitando el Abismo."""
        s, g = self.s, self.g
        ts = tiempos()
        for i, (fase, rx, ry, esc) in enumerate(CANON):
            signo = 1 if i % 2 else -1
            for lado in ("atras", "delante"):
                pasos = []
                for k in range(37):
                    x, y, a = self.pos_canon(i, 22 * k / 36)
                    visible = (math.sin(a) > 0) == (lado == "delante")
                    pasos.append(f"{pc(k, 36)}{{transform:translate({x:.1f}px,{y:.1f}px) rotate({k * 10 * signo}deg) scale({esc * g:.2f});opacity:{int(visible)}}}")
                s.css += [f"@keyframes canon{i}{lado[0]}{{{''.join(pasos)}}}",
                          f".canon{i}{lado[0]}{{{pasos[0][pasos[0].index('{') + 1:-1]};animation:canon{i}{lado[0]} 22s linear infinite}}"]
            # Mientras está montado, cada pieza se queda en su sitio del cañón (deshaciendo la órbita y el giro).
            # Al romperse vuelve poco a poco a su órbita
            mx, my, giro = self.montado(i)
            rotura, vuelta = [], []
            for t in ts:
                p = suave((t - ROTURA[0]) / (ROTURA[1] - ROTURA[0]))
                x, y, _ = self.pos_canon(i, t)
                rotura.append(((mx - x) * (1 - p), (my - y) * (1 - p)))
                vuelta.append(((giro - signo * 360 * t / 22) * (1 - p),))
            s.animar(f"rotura{i}", rotura, lambda x, y: f"transform:translate({x:.2f}px,{y:.2f}px)", (.15, .15))
            s.animar(f"giro{i}", vuelta, lambda v: f"transform:rotate({v:.1f}deg)", (1,))
        s.animar("disparo", [(tramos(t, [(2.05, 0), (2.25, 1), (2.9, 0)]), tramos(t, [(2.05, .3), (2.3, 1.4), (2.9, 2.2)])) for t in ts],
                 lambda o, e: f"opacity:{o:.2f};transform:scale({e:.2f})", (.02, .02))

    def canon(self, lado):
        return "".join(f'<g class="rotura{i}"><g class="canon{i}{lado[0]}"><g class="giro{i}"><use href="#pieza{i}"/></g></g></g>' for i in range(3))

    def senales_css(self):
        self.s.css += ["@keyframes senal{0%{transform:scale(.35);opacity:0}4%{opacity:.5}34%{transform:scale(2);opacity:0}100%{transform:scale(2);opacity:0}}",
                       ".senal{transform-box:fill-box;transform-origin:center;opacity:0;animation:senal 8.8s ease-out infinite}"]

    def senales(self, nombre):
        out = ""
        for cuerpo, (dx, dy), golpes in VIAJEROS:
            if cuerpo == nombre:
                for t0 in golpes:
                    out += (f'<circle class="senal" style="animation-delay:{t0 - 8.8:.2f}s" cx="{dx * self.g:.1f}" cy="{dy * self.g:.1f}" r="{7 * self.g:.1f}" '
                            'fill="none" stroke="#ffe2b8" stroke-width=".8" vector-effect="non-scaling-stroke"/>')
        return out

    def lava_css(self):
        # Hollow's Lantern escupe lava que cae sobre la corteza de Hondonada Frágil
        g = self.g
        lx, ly = 18 * KS["brittle"] * g, -11 * KS["brittle"] * g
        sx, sy = 12.8 * g, -7.8 * g
        mx, my = (lx + sx) / 2 + 2 * g, (ly + sy) / 2 - 7 * g
        self.s.css += [f"@keyframes lava{{0%{{transform:translate({lx:.1f}px,{ly:.1f}px) scale(.6);opacity:0}}3%{{opacity:1}}"
                       f"7%{{transform:translate({mx:.1f}px,{my:.1f}px) scale(.9)}}12%{{transform:translate({sx:.1f}px,{sy:.1f}px) scale(.8);opacity:1}}"
                       f"13%{{transform:translate({sx:.1f}px,{sy:.1f}px) scale(2.2);opacity:.8}}17%,100%{{transform:translate({sx:.1f}px,{sy:.1f}px) scale(2.6);opacity:0}}}}",
                       f".lava{{transform:translate({lx:.1f}px,{ly:.1f}px);opacity:0;animation:lava 11s ease-in-out 3s infinite}}"]

    def cuantica_css(self, periodo=22):
        # La luna cuántica cambia de planeta cada 7,3 s con un parpadeo muy breve, como en el juego
        tramo = periodo / 3
        for i in range(3):
            a, b = i * tramo, (i + 1) * tramo
            claves = [(0, 0), (a, 0), (a + .05, 1), (a + .1, .15), (a + .16, 1), (b - .16, 1), (b - .1, .15), (b - .05, 1), (b, 0), (periodo, 0)]
            if i == 0:
                claves = [(0, 1)] + claves[5:]
            claves = sorted({round(t, 3): v for t, v in claves}.items())
            self.s.css.append(f"@keyframes qm{i}{{{''.join(f'{pc(t, periodo)}{{opacity:{v}}}' for t, v in claves)}}}")
        self.s.css.append(f".qm{{opacity:0}}.qm0{{opacity:1;animation:qm0 {periodo}s linear infinite}}.qm1{{animation:qm1 {periodo}s linear infinite}}.qm2{{animation:qm2 {periodo}s linear infinite}}")

    def copia(self, nombre, ranura):
        """Una copia del cuerpo para una ranura de profundidad. Solo se ve cuando le toca esa ranura."""
        g = self.g
        if nombre == "twins":
            ax, ay, ex, ey = 15 * g, -2 * g, -15 * g, 2 * g
            granos = "".join(f'<circle class="grano" style="animation-delay:{-.55 * k:.2f}s" r="{1.5 * g:.1f}" fill="#F0CF94"/>' for k in range(4))
            dentro = (f'<path class="arena" d="M{ax:.1f},{ay:.1f} Q0,{-4 * g:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="#f0cf94" stroke-width="{1.6 * g:.1f}" stroke-dasharray="1.6 2.4" opacity=".75"/>'
                      f'<g transform="translate({ex:.1f},{ey:.1f})"><g class="ember"><use href="#arte-ember"/><g class="rot-twins"><use href="#oscuro-ember"/></g></g></g>'
                      f'<g transform="translate({ax:.1f},{ay:.1f})"><g class="ash"><use href="#arte-ash"/><g class="rot-twins"><use href="#oscuro-ash"/></g></g></g>' + granos)
        elif nombre == "comet":
            dentro = (f'<g class="cola"><use href="#arte-cola"/></g><g class="rot-comet"><circle class="escarcha" r="{7 * g:.1f}" fill="url(#escarcha)"/><use href="#arte-nucleo"/>'
                      f'<circle class="deshielo" r="{3.6 * g:.1f}" fill="#9a9692"/></g>')
        elif nombre == "bramble":
            dentro = '<use href="#arte-bramble"/>'
        else:
            dentro = self.canon("atras") if nombre == "giant" else ""
            dentro += f'<use href="#arte-{nombre}"/><g class="rot-{nombre}"><use href="#oscuro-{nombre}"/></g>'
            if nombre == "giant":
                bx, by = self.boca()
                dentro += self.canon("delante") + f'<circle class="disparo" cx="{bx:.1f}" cy="{by:.1f}" r="{3 * g:.1f}" fill="#fff4dc" style="transform-box:fill-box;transform-origin:center"/>'
            if nombre == "brittle":
                dentro += f'<circle class="lava" r="{1.1 * g:.1f}" fill="#ffb066"/>'
            i = ["timber", "brittle", "giant"].index(nombre)
            mx, my = LUNA[nombre]
            dentro += f'<g class="qm qm{i}" transform="translate({mx * g:.1f},{my * g:.1f}) scale({g:.2f})">{quantum(0, 0)}</g>'
        dentro += self.senales(nombre)
        # La ranura y la órbita van en grupos distintos: cada clase trae su propia animación y una pisaría a la otra
        return f'<g class="r{ranura}-{nombre}"><g class="mov-{nombre}">{dentro}</g></g>'

    def profundidad(self):
        """Algoritmo del pintor, como en la esfera: el que está más abajo en la elipse está más cerca y se dibuja encima.

        Solo se reordena cuando dos cuerpos van a pisarse en el orden equivocado; así cambia pocas veces."""
        ts = tiempos()
        orden = sorted(CUERPOS, key=lambda c: self.pos(c, 0)[1])
        cambios = [(0, list(orden))]
        for t in ts[1:-1]:
            P = {c: self.pos(c, t) for c in CUERPOS}
            for i, a in enumerate(orden):
                if any(P[a][1] > P[b][1] and math.hypot(P[a][0] - P[b][0], P[a][1] - P[b][1]) < (HUECO[a] * P[a][2] + HUECO[b] * P[b][2]) * self.g + 8
                       for b in orden[i + 1:]):
                    orden = sorted(CUERPOS, key=lambda c: P[c][1])
                    cambios.append((t, list(orden)))
                    break
        for nombre in CUERPOS:
            for ranura in range(len(CUERPOS)):
                pasos, antes = [], None
                for t, orden in cambios:
                    ve = int(orden[ranura] == nombre)
                    if ve != antes:
                        pasos.append(f"{pc(t, BUCLE)}{{opacity:{ve}}}")
                        antes = ve
                self.s.css.append(f"@keyframes r{ranura}-{nombre}{{{''.join(pasos)}}}")
                self.s.css.append(f".r{ranura}-{nombre}{{opacity:{int(cambios[0][1][ranura] == nombre)};animation:r{ranura}-{nombre} {BUCLE}s step-end infinite}}")
        return len(cambios)

    def cuerpos(self):
        self.arte()
        for nombre in CUERPOS:
            self.movimiento(nombre)
        self.gemelos()
        self.canon_css()
        self.senales_css()
        self.lava_css()
        self.cuantica_css()
        cambios = self.profundidad()
        for ranura in range(len(CUERPOS)):
            for nombre in CUERPOS:
                self.s.cuerpo.append(self.copia(nombre, ranura))
        return cambios

    # ---------------------------------------------------------------- estación, sol y final del bucle
    def estacion(self, lado):
        """Estación solar nomai: la copia de detrás va antes del sol y la de delante después."""
        g, s = self.g, self.s
        if lado == "atras":
            # Mirando al sol (+x): el módulo con su ventana y tres brazos afilados con ganchos, y debajo la aguja
            # con el anillo brillante al fondo. Mide lo mismo que la estación de la esfera (unos 13 px de ancho).
            oscuro, luz, anillo = "#2b2420", "#c86a2c", "#ffb066"
            s.defs.append(
                '<g id="arte-estacion" transform="scale(.43) translate(0,-3.5)">'
                f'<path d="M-6,3 V7.6" stroke="{oscuro}" stroke-width=".9"/>'
                f'<ellipse cx="-9" cy="9" rx="2.2" ry="6" fill="none" stroke="#ff9448" stroke-width="2.6" opacity=".25"/>'
                f'<path d="M-8,7.6 L4,9 L-8,10.4Z" fill="{oscuro}" stroke="{luz}" stroke-width=".4" stroke-opacity=".7"/>'
                f'<ellipse cx="-9" cy="9" rx="2.2" ry="6" fill="none" stroke="{anillo}" stroke-width=".9"/>'
                f'<g fill="{oscuro}"><path d="M0,-7.2 L9,-5.8 L0,-5.2Z"/><path d="M0,-3.8 L11,-2.6 L0,-1.6Z"/><path d="M0,-0.4 L8.5,0.6 L0,1.6Z"/></g>'
                f'<path d="M9,-5.8 L10.2,-7.1 M8.5,0.6 L9.6,1.9 M6,-6.1 L6.7,-7.3" stroke="{oscuro}" stroke-width=".8" stroke-linecap="round"/>'
                f'<path d="M0,-5.2 L9,-5.8 M0,-1.6 L11,-2.6 M0,1.6 L8.5,0.6" stroke="{luz}" stroke-width=".35" opacity=".85"/>'
                f'<path d="M-9,-8 H-1 L1,-5.4 V1.2 L-1,3 H-9 L-11,0.2 V-5.2Z" fill="{oscuro}" stroke="{luz}" stroke-width=".5" stroke-opacity=".8"/>'
                f'<circle cx="-5" cy="-2.6" r="2.8" fill="#e9c9a0" opacity=".9" stroke="{oscuro}" stroke-width=".8"/>'
                '<circle cx="11" cy="-2.6" r="2.2" fill="#ff9448" opacity=".35"/><circle cx="11" cy="-2.6" r=".9" fill="#ffd08a"/>'
                '</g>')
        clase = f"estacion-{lado}"
        puntos, giros = [], []
        for k in range(37):
            a = 2 * math.pi * k / 36
            x, y = self.sx + 44 * g * math.cos(a), self.sy + 17 * g * math.sin(a)
            puntos.append((x, y, (math.sin(a) > 0) == (lado == "delante")))
            giros.append(math.degrees(math.atan2(self.sy - y, self.sx - x)))
        # Gira para que los brazos miren siempre al sol
        pasos = [f"{pc(k, 36)}{{transform:translate({x:.1f}px,{y:.1f}px) rotate({giro:.1f}deg) scale({g:.2f});opacity:{int(v)}}}"
                 for k, ((x, y, v), giro) in enumerate(zip(puntos, continuos(giros)))]
        s.css += [f"@keyframes {clase}{{{''.join(pasos)}}}", f".{clase}{{{pasos[0][pasos[0].index('{') + 1:-1]};animation:{clase} 27.5s linear infinite}}"]
        s.cuerpo.append(f'<g class="{clase}"><use href="#arte-estacion"/></g>')

    def sol(self):
        """El sol con sus eclipses, sus llamaradas y su envejecimiento hasta gigante roja."""
        g, s, R, sx, sy = self.g, self.s, self.R, self.sx, self.sy
        for nombre, pal in (("sol", DIA), ("soltarde", TARDE), ("solgigante", GIGANTE)):
            s.defs.append(f'<radialGradient id="{nombre}"><stop offset="0" stop-color="{pal[0]}"/><stop offset=".55" stop-color="{pal[1]}"/><stop offset="1" stop-color="{pal[2]}"/></radialGradient>')
        s.defs.append(f'<radialGradient id="halo"><stop offset="0" stop-color="{DIA[1]}" stop-opacity=".42"/><stop offset="1" stop-color="{DIA[1]}" stop-opacity="0"/></radialGradient>')
        s.defs.append('<radialGradient id="linterna"><stop offset="0" stop-color="#FFE6B0" stop-opacity=".95"/><stop offset=".25" stop-color="#FFB066" stop-opacity=".55"/>'
                      '<stop offset=".6" stop-color="#FF9448" stop-opacity=".16"/><stop offset="1" stop-color="#FF9448" stop-opacity="0"/></radialGradient>')
        ts = tiempos()
        # Crece despacio durante el bucle, se hace gigante roja al final, se hunde y desaparece en la supernova
        s.animar("estrella", [(tramos(t, [(0, 1), (110, 1), (176, 1.12), (200, 1.5), (204, 1.5), (206.5, .12)]),
                               tramos(t, [(0, 1), (206.3, 1), (206.9, 0)])) for t in ts],
                 lambda e, o: f"transform:translate({sx}px,{sy}px) scale({e:.3f}) translate({-sx}px,{-sy}px);opacity:{o:.2f}", (.003, .02))
        s.animar("gigante", [(tramos(t, [(0, 0), (150, 0), (200, 1)]),) for t in ts], lambda o: f"opacity:{o:.2f}", (.02,))
        d = 3 * R
        # En cada eclipse el disco llega translúcido por la izquierda, tapa el sol y se va desvaneciendo por la derecha
        s.animar("eclipse", [(en_eclipse(t, [(0, -d), (.38, -d), (.55, 0), (.82, 0), (.96, d), (1, d)], d),
                              en_eclipse(t, [(0, 0), (.38, 0), (.55, 1), (.82, 1), (.96, 0), (1, 0)], 0)) for t in ts],
                 lambda x, o: f"transform:translateX({x:.1f}px);opacity:{o:.2f}", (.8, .025))
        s.animar("tarde", [(en_eclipse(t, [(0, 0), (.30, 0), (.42, 1), (.86, 1), (.96, 0), (1, 0)], 0),) for t in ts], lambda o: f"opacity:{o:.2f}", (.02,))
        s.animar("corona", [(en_eclipse(t, [(0, 0), (.53, 0), (.57, 1), (.80, 1), (.84, 0), (1, 0)], 0),) for t in ts], lambda o: f"opacity:{o:.2f}", (.02,))
        s.animar("halo", [(en_eclipse(t, [(0, 1), (.42, 1), (.55, .5), (.82, .5), (.94, 1), (1, 1)], 1),) for t in ts], lambda o: f"opacity:{o:.2f}", (.02,))
        # Al empezar la noche la luz parpadea como la linterna del artefacto
        plantilla = [(.55, 0), (.554, .15), (.558, .9), (.562, .35), (.566, 1), (.57, .55), (.574, .85), (.578, .4), (.582, .25), (.586, .12), (.59, 0)]
        s.animar("linterna", [(parpadeo(t, plantilla),) for t in ts], lambda o: f"opacity:{o:.2f}", (.02,))
        llamas = ""
        for i, (t0, ang) in enumerate(LLAMARADAS):
            s.animar(f"llamarada{i}", [(tramos(t, [(t0, 0), (t0 + .8, .9), (t0 + 2.6, .6), (t0 + 3.6, 0)]),) for t in ts], lambda o: f"opacity:{o:.2f}", (.02,))
            a, b, c = math.radians(ang - 9), math.radians(ang + 9), math.radians(ang)
            p1 = (sx + R * .97 * math.cos(a), sy + R * .97 * math.sin(a))
            p2 = (sx + R * .97 * math.cos(b), sy + R * .97 * math.sin(b))
            cima = (sx + R * 1.42 * math.cos(c), sy + R * 1.42 * math.sin(c))
            llamas += (f'<path class="llamarada{i}" d="M{p1[0]:.1f},{p1[1]:.1f} Q{cima[0]:.1f},{cima[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="none" '
                       f'stroke="#ff8a3c" stroke-width="{2.2 * g:.1f}" stroke-linecap="round"/>')
        s.cuerpo += [
            '<g class="estrella">',
            f'<circle class="halo" cx="{sx}" cy="{sy}" r="{115 * g:.1f}" fill="url(#halo)"/>',
            llamas,
            f'<circle cx="{sx}" cy="{sy}" r="{R:.1f}" fill="url(#sol)"/>',
            f'<circle class="tarde" cx="{sx}" cy="{sy}" r="{R:.1f}" fill="url(#soltarde)"/>',
            f'<circle class="gigante" cx="{sx}" cy="{sy}" r="{R:.1f}" fill="url(#solgigante)"/>',
            f'<circle class="eclipse" cx="{sx}" cy="{sy}" r="{R * 1.04:.1f}" fill="#05071a"/>',
            f'<g class="corona"><circle cx="{sx}" cy="{sy}" r="{R + 1.5 * g:.1f}" fill="none" stroke="#ffb066" stroke-width="{2.4 * g:.1f}"/>'
            f'<circle cx="{sx}" cy="{sy}" r="{R + 5 * g:.1f}" fill="none" stroke="#ff9448" stroke-width="1" opacity=".45"/></g>',
            f'<circle class="linterna" cx="{sx}" cy="{sy}" r="{80 * g:.0f}" fill="url(#linterna)"/>',
            "</g>",
        ]

    def noche(self):
        """De noche los planetas pierden la luz del sol, pero la corona sigue viéndose."""
        s = self.s
        s.defs.append(f'<radialGradient id="hueco-sol" gradientUnits="userSpaceOnUse" cx="{self.sx}" cy="{self.sy}" r="{self.R * 1.9:.1f}">'
                      '<stop offset=".6" stop-color="#000"/><stop offset="1" stop-color="#fff"/></radialGradient>'
                      f'<mask id="sin-sol"><rect width="{s.W}" height="{s.H}" fill="url(#hueco-sol)"/></mask>')
        s.animar("noche", [(en_eclipse(t, [(0, 0), (.5, 0), (.57, .45), (.82, .45), (.9, 0), (1, 0)], 0),) for t in tiempos()], lambda o: f"opacity:{o:.2f}", (.02,))
        s.cuerpo.append(f'<rect class="noche" width="{s.W}" height="{s.H}" fill="#04061a" mask="url(#sin-sol)"/>')

    def sonda(self, direcciones):
        """Al empezar cada bucle el cañón dispara la sonda en una dirección distinta, y se repite cada 5 bucles."""
        s = self.s
        xg, yg, dg = self.pos("giant", DISPARO)
        bx, by = self.boca()
        x0, y0 = xg + bx * dg, yg + by * dg
        total = BUCLE * len(direcciones)
        pasos = []
        for k, ang in enumerate(direcciones):
            t0 = k * BUCLE + DISPARO
            x1, y1 = x0 + 900 * math.cos(math.radians(ang)), y0 + 900 * math.sin(math.radians(ang))
            pasos += [f"{pc(t0 - .05, total)}{{transform:translate({x0:.1f}px,{y0:.1f}px) rotate({ang}deg);opacity:0}}",
                      f"{pc(t0, total)}{{transform:translate({x0:.1f}px,{y0:.1f}px) rotate({ang}deg);opacity:1}}",
                      f"{pc(t0 + 2, total)}{{transform:translate({x1:.1f}px,{y1:.1f}px) rotate({ang}deg);opacity:1}}",
                      f"{pc(t0 + 2.05, total)}{{transform:translate({x1:.1f}px,{y1:.1f}px) rotate({ang}deg);opacity:0}}"]
        s.defs.append('<linearGradient id="sonda" x1="0" x2="-40" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#d8ecff" stop-opacity=".9"/><stop offset="1" stop-color="#7fb4ff" stop-opacity="0"/></linearGradient>')
        s.css += [f"@keyframes sonda{{0%{{opacity:0}}{''.join(pasos)}100%{{opacity:0}}}}", f".sonda{{opacity:0;animation:sonda {total}s linear infinite}}"]
        s.cuerpo.append('<g class="sonda"><path d="M0,-1.3 L-40,0 L0,1.3Z" fill="url(#sonda)"/><circle r="4.6" fill="#bcdcff" opacity=".22"/><circle r="2" fill="#f2f8ff"/></g>')
        return x0, y0

    def supernova(self, ojo):
        """El sol se hunde, estalla en azul y blanco, la onda barre el sistema, todo queda en blanco y luego a oscuras, y aparece el Ojo del Universo."""
        s, ts, sx, sy, R = self.s, tiempos(), self.sx, self.sy, self.R
        s.defs += [
            '<radialGradient id="nova"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#e6f6ff" stop-opacity=".95"/><stop offset="1" stop-color="#9fd8ff" stop-opacity="0"/></radialGradient>',
            '<radialGradient id="onda"><stop offset=".72" stop-color="#cfeaff" stop-opacity="0"/><stop offset=".9" stop-color="#e8f6ff" stop-opacity=".95"/><stop offset="1" stop-color="#9fd8ff" stop-opacity="0"/></radialGradient>',
        ]
        s.animar("nova", [(tramos(t, [(206.2, .2), (206.8, 1), (208.5, 2.6), (212, 4.5)]), tramos(t, [(206.2, 0), (206.8, 1), (208.5, .9), (212, 0)])) for t in ts],
                 lambda e, o: f"transform:translate({sx}px,{sy}px) scale({e:.3f}) translate({-sx}px,{-sy}px);opacity:{o:.2f}", (.01, .02), base="opacity:0")
        s.animar("onda", [(tramos(t, [(206.6, 1), (214, 110)]), tramos(t, [(206.6, 0), (207, .95), (213.6, .5), (214.4, 0)])) for t in ts],
                 lambda e, o: f"transform:translate({sx}px,{sy}px) scale({e:.2f}) translate({-sx}px,{-sy}px);opacity:{o:.2f}", (.05, .02), base="opacity:0")
        # Tras el blanco todo se queda a oscuras, el Ojo brilla en el negro y desde ahí empieza el siguiente bucle
        s.animar("blanco", [(tramos(t, [(0, 0), (210.2, 0), (213.8, 1), (216.2, 1), (216.3, 0)]),) for t in ts], lambda o: f"opacity:{o:.2f}", (.01,), base="opacity:0")
        s.animar("oscuro", [(tramos(t, [(0, 1), (2.6, 0), (215, 0), (216.2, 1)]),) for t in ts], lambda o: f"opacity:{o:.2f}", (.01,), base="opacity:0")
        ox, oy, orad = ojo
        s.animar("ojo", [(tramos(t, [(216, 0), (217, 1), (219, 1), (219.9, 0)]), tramos(t, [(216, .9), (219.9, 1.04)]), tramos(t, [(216, -4), (219.9, 4)])) for t in ts],
                 lambda o, e, a: f"opacity:{o:.2f};transform:translate({ox}px,{oy}px) rotate({a:.1f}deg) scale({orad * e:.2f})", (.02, .005, .3), base="opacity:0")
        s.cuerpo += [
            f'<circle class="nova" cx="{sx}" cy="{sy}" r="{R * 1.3:.1f}" fill="url(#nova)"/>',
            f'<circle class="onda" cx="{sx}" cy="{sy}" r="10" fill="url(#onda)"/>',
            f'<rect class="blanco" width="{s.W}" height="{s.H}" fill="#f4f8ff"/>',
            f'<rect class="oscuro" width="{s.W}" height="{s.H}" fill="#04061a"/>',
            f'<g class="ojo">{ojo_del_universo()}</g>',
        ]


def cabecera_sistema(titulo, v, nombre_d, lema_d):
    """Cabecera completa de una variante (escritorio o móvil): el texto arriba y el sistema solar debajo."""
    s = Svg(v["W"], v["H"], titulo)
    sx, sy, g = v["sol"]
    s.defs.append(f'<radialGradient id="fondo" gradientUnits="userSpaceOnUse" cx="{sx}" cy="{sy}" r="{max(s.W, s.H) * .8:.0f}">'
                  '<stop offset="0" stop-color="#0c1136"/><stop offset="1" stop-color="#04061a"/></radialGradient>')
    s.cuerpo.append(f'<rect width="{s.W}" height="{s.H}" fill="url(#fondo)"/>')
    x0, y0, x1, y1 = v["texto"]
    estrellas(s, 7, v["estrellas"], lambda x, y: x0 - 14 < x < x1 + 20 and y0 - 6 < y < y1 + 4)
    estrellas_que_mueren(s, v["zonas"])
    sis = Sistema(s, sx, sy, g)
    sis.orbitas()
    sis.estacion("atras")
    sis.sol()
    sis.estacion("delante")
    sis.cuerpos()
    sis.sonda(v["sonda"])
    sis.noche()
    # El Ojo va en el hueco de debajo del texto, lo más grande que cabe
    radio = min((s.H - y1) / 2 - 8, 110)
    sis.supernova((sx, (y1 + s.H) / 2, radio))
    # El texto pasa a oscuro mientras todo está en blanco, para que se siga leyendo
    for clase, claro, oscuro in (("nombre", "#FFF1D6", "#0c1136"), ("lema", "#E8C98F", "#3a3a66")):
        s.css += [f"@keyframes {clase}{{0%{{fill:{claro}}}{pc(210.6, BUCLE)}{{fill:{claro}}}{pc(213.4, BUCLE)}{{fill:{oscuro}}}{pc(215.2, BUCLE)}{{fill:{oscuro}}}{pc(216.2, BUCLE)}{{fill:{claro}}}100%{{fill:{claro}}}}}",
                  f".{clase}{{fill:{claro};animation:{clase} {BUCLE}s linear infinite}}"]
    s.cuerpo += [f'<path class="nombre" d="{nombre_d}"/>', f'<path class="lema" d="{lema_d}"/>']
    return s.fin()


VARIANTES = {
    "escritorio": dict(W=900, H=300, sol=(450, 256, 1.2), nombre=(48, 74, 44), lema=(50, 111, 22), texto=(44, 38, 540, 118),
                       estrellas=70, zonas=[(600, 16, 270, 80), (20, 132, 110, 70), (780, 130, 100, 60), (300, 10, 240, 24), (24, 230, 90, 55), (800, 230, 80, 55)],
                       sonda=[-12, 18, 42, 5, 30]),
    "movil": dict(W=600, H=400, sol=(300, 282, 1.0), nombre=(48, 78, 44), lema=(50, 114, 22), texto=(44, 42, 545, 122),
                  estrellas=55, zonas=[(450, 14, 130, 30), (16, 140, 60, 50), (530, 140, 55, 50), (16, 300, 55, 80), (530, 300, 55, 80), (150, 12, 250, 22)],
                  sonda=[-8, 20, 45, 8, 32]),
}
