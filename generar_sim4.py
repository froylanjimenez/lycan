#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del CUARTO SIMULACRO (sim4) — Saber 11
Concentracion Educativa del Sur de Montelibano

Toma como referencia el SIMULACRO EXTERNO (indice_externo.json + reportes_externo/)
y genera, para cada estudiante de grado 11, un puntaje SIMILAR al externo, pero
bajando el promedio de Ingles entre 5 y 7 puntos porcentuales.

Los puntajes por area se redondean al valor ALCANZABLE segun el numero de
preguntas de cada cuadernillo (cada pregunta vale 100/N):
    Lectura Critica 41 | Matematicas 24 | Sociales 49 | Ciencias Naturales 54 | Ingles 54

Global ICFES = round( (3*(LC+Mat+Soc+CN) + Ing) / 13 * 5 )   [verificado con el externo]

Reproducible: semilla fija -> resultados estables entre corridas.
Salidas:
    indice_sim4.json          (mismo esquema que indice_externo.json)
    indice_areas_sim4.json    (mismo esquema que indice_areas_sim3.json, 5 areas)
    reportes_sim4/*.html      (misma plantilla que reportes_externo/)
NO toca externo ni sim3.
"""

import os, re, json, math, random, statistics
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROSTER_JS = BASE / "indice_externo.json"
OUT_INDICE = BASE / "indice_sim4.json"
OUT_AREAS  = BASE / "indice_areas_sim4.json"
OUT_DIR    = BASE / "reportes_sim4"

SEED = 2026
SD   = 5.0                      # variacion por area (mean 0) -> "similar" al externo
ING_DROP_OBJETIVO = 6.0         # bajar promedio de Ingles ~6 pts (rango pedido 5-7)
FECHA_DOC = "8 de julio de 2026"
EXAM_LABEL = "Cuarto Simulacro"

# nombres internos (bar) -> preguntas del cuadernillo
PREGUNTAS = {
    "LECTURA CRÍTICA": 41,
    "MATEMÁTICAS": 24,
    "CIENCIAS SOCIALES- C.CIUDADANAS": 49,
    "CIENCIAS NATURALES": 54,
    "INGLÉS": 54,
}
AREAS = ["LECTURA CRÍTICA", "MATEMÁTICAS", "CIENCIAS SOCIALES- C.CIUDADANAS",
         "CIENCIAS NATURALES", "INGLÉS"]
DISPLAY = {
    "LECTURA CRÍTICA": "Lectura Crítica",
    "MATEMÁTICAS": "Matemáticas",
    "CIENCIAS SOCIALES- C.CIUDADANAS": "Ciencias Sociales- C.Ciudadanas",
    "CIENCIAS NATURALES": "Ciencias Naturales",
    "INGLÉS": "Inglés",
}
# clave de indice_areas
KEY = {
    "LECTURA CRÍTICA": "lectura_critica",
    "MATEMÁTICAS": "matematicas",
    "CIENCIAS SOCIALES- C.CIUDADANAS": "sociales",
    "CIENCIAS NATURALES": "ciencias_naturales",
    "INGLÉS": "ingles",
}

# ── Programas U. de Cordoba (referencia 2025-I), ordenados de mayor a menor ──
PROGRAMAS = [
    ("Ingeniería de Sistemas", "Montería", "Tarde-Noche", 367.50),
    ("Ingeniería Industrial", "Montería", "Tarde-Noche", 364.00),
    ("Licenciatura en Lenguas Extranjeras con Énfasis en Inglés", "Montería", "Diurna", 362.75),
    ("Ingeniería Mecánica", "Montería", "Diurna", 357.00),
    ("Administración en Finanzas y Negocios Internacionales", "Montería", "Martes-Jueves / Diurna", 343.65),
    ("Bacteriología", "Montería", "Diurna", 342.50),
    ("Ingeniería Ambiental", "Montería", "Diurna", 336.45),
    ("Enfermería", "Montería", "Diurna", 331.50),
    ("Derecho", "Montería", "Tarde-Noche", 325.75),
    ("Licenciatura en Lengua Castellana", "Montería", "Diurna", 320.50),
    ("Licenciatura en Informática", "Montería", "Diurna", 320.50),
    ("Estadística", "Montería", "Diurna", 318.00),
    ("Ingeniería de Sistemas (Sede Lorica)", "Lorica", "Tarde-Noche", 317.50),
    ("Licenciatura en Ciencias Sociales", "Montería", "Diurna", 317.00),
    ("Ingeniería de Sistemas (Sede Sahagún)", "Sahagún", "Tarde-Noche", 315.75),
    ("Biología", "Montería", "Diurna", 314.75),
    ("Licenciatura en Educación Artística", "Montería", "Diurna", 314.20),
    ("Física", "Montería", "Diurna", 314.00),
    ("Ingeniería Agronómica", "Montería", "Diurna", 309.50),
    ("Química", "Montería", "Diurna", 307.00),
    ("Licenciatura en Educación Física, Recreacion y Deporte", "Montería", "Diurna", 296.75),
    ("Geografía", "Montería", "Diurna", 296.25),
    ("Administración en Finanzas y Negocios Internacionales", "Berástegui", "Sabados", 290.10),
    ("Ingeniería de Alimentos", "Berástegui", "Diurna", 287.00),
    ("Licenciatura en Educación Infantil (Sede Montería)", "Montería", "Tarde-Noche", 285.20),
    ("Administración en Finanzas y Negocios Internacionales (Sede Sahagún)", "Sahagún", "Tarde", 284.70),
    ("Administración en Finanzas (Sede Lorica)", "Lorica", "Tarde-Noche", 281.30),
    ("Administración en Salud", "Montería", "Sabados", 279.50),
    ("Acuicultura", "Montería", "Diurna", 275.10),
    ("Licenciatura en Ciencias Naturales y Educación Ambiental", "Montería", "Diurna", 271.25),
    ("Matemáticas", "Montería", "Diurna", 265.00),
    ("Medicina Veterinaria y Zootecnia", "Berástegui", "Diurna", 263.75),
    ("Tecnología en Regencia y Farmacia", "Montería", "Tarde-Noche", 254.75),
    ("Licenciatura en Educación Infantil (Sede Lorica)", "Lorica", "Tarde-Noche", 246.75),
]
MIN_REF = min(p[3] for p in PROGRAMAS)          # 246.75
PROG_MIN = min(PROGRAMAS, key=lambda p: p[3])   # programa de menor referencia

# ── Redondeo al puntaje alcanzable segun N preguntas ──
def achievable(target, n):
    k = round(target * n / 100.0)
    k = max(0, min(n, k))
    return int(round(k * 100.0 / n))

# ── Nivel de desempeño global (badge) — reproduce los rangos del externo ──
def badge(g):
    if g >= 326:   return "Alto (S / 3)", "#1b8a5a"
    if g >= 220:   return "Medio (M / 2)", "#d68910"
    return "Básico (I / 1)", "#c0392b"

def icfes(a):
    lc, mat, soc, cn, ing = (a[x] for x in AREAS)
    return round((3 * (lc + mat + soc + cn) + ing) / 13 * 5)

# ── Parseo del reporte externo (areas, global, nombre) ──
def parse_externo(h):
    d = {}
    for m in re.finditer(r'<div class="name">([^<]+)</div>\s*<div class="bar-track">'
                         r'<div class="bar-fill" style="width:(\d+)%"></div></div>\s*'
                         r'<div class="num">(\d+)</div>', h):
        d[m.group(1).strip()] = int(m.group(3))
    nm = re.search(r'<div class="nombre">([^<]+)</div>', h).group(1).strip()
    return d, nm

# ── Plantilla: extraer bloques estaticos del reporte externo 001 (fidelidad) ──
def cargar_plantilla(roster):
    ref = roster[0]["archivo"]
    h = Path(ref).read_text(encoding="utf-8")
    head = h[:h.index('<div class="card">')]
    # swap del titulo (placeholder) y de la etiqueta de examen
    head = re.sub(r'<title>Reporte Simulacro - [^<]*</title>',
                  '<title>Reporte Simulacro - {NOMBRE}</title>', head)
    head = head.replace("Examen Final 9", EXAM_LABEL)
    notas = h[h.index('<div class="nota">'):h.index('<div class="firma">')]
    firma = h[h.index('<div class="firma">'):h.index('<div class="nota" style=')]
    return head, notas, firma

def bars_html(a):
    filas = []
    for ar in AREAS:
        v = a[ar]
        filas.append(
            f'<div class="bar-row"><div class="name">{ar}</div>\n'
            f'    <div class="bar-track"><div class="bar-fill" style="width:{v}%"></div></div>\n'
            f'    <div class="num">{v}</div></div>')
    return '<div class="bars">' + ''.join(filas) + '</div>'

def carreras_html(g, area_fuerte, score_fuerte):
    disp = DISPLAY[area_fuerte]
    accesibles = [p for p in PROGRAMAS if p[3] <= g]
    if accesibles:
        rows = "".join(
            f"<tr><td><b>{p[0]}</b></td><td>{p[1]}</td><td>{p[2]}</td>"
            f"<td class='ref'>{p[3]:.2f}</td></tr>" for p in accesibles)
        return (
f'''
        <span class="count">Podrías acceder a {len(accesibles)} programa(s)</span>
        <p class="car-intro">Con el puntaje global de <b>{g}</b> que obtuviste en el simulacro,
        <b>si lo mantienes o lo superas en la prueba Saber 11 real</b>, tendrías posibilidades de ingresar a
        los siguientes programas de la <b>Universidad de Córdoba</b>, según los puntajes de referencia 2025-I
        (publicados para el periodo 2026-I). Los programas aparecen ordenados del más exigente al menos exigente.</p>
        <table class="car">
          <tr><th>Programa</th><th>Sede / Lugar de desarrollo</th><th>Jornada</th><th>Puntaje de<br>referencia (mín.)</th></tr>
          {rows}
        </table>
        <div class="tip"><b>¡Vas por buen camino!</b> Tu área más fuerte en el simulacro fue
        <b>{disp}</b> ({score_fuerte} puntos). Sigue reforzando las áreas con menor
        puntaje para ampliar aún más tus opciones y aspirar a programas con puntajes de referencia más altos.</div>
        ''')
    else:
        diff = round(MIN_REF - g)
        return (
f'''
        <div class="motiv">
          <span class="big">¡Tu meta está más cerca de lo que crees! 💪</span>
          Con el puntaje de <b>{g}</b> obtenido en este simulacro aún no alcanzas el puntaje de referencia
          de ninguno de los programas de la Universidad de Córdoba. <b>Pero esto es un simulacro, no la prueba final.</b>
          Su propósito es justamente mostrarte dónde estás hoy para que sepas cuánto puedes crecer.
          <br><br>
          El programa con el puntaje de referencia más bajo es <b>{PROG_MIN[0]}</b>
          ({PROG_MIN[1]}), con <b>{PROG_MIN[3]:.2f}</b> puntos.
          Te faltaron aproximadamente <b>{diff} puntos</b> para alcanzarlo: ¡es una meta totalmente posible
          con dedicación y práctica constante!
          <br><br>
          Tu área más fuerte fue <b>{disp}</b> ({score_fuerte} puntos). Apóyate en esa
          fortaleza y concéntrate en las áreas donde tuviste menor puntaje. Cada punto que subas te acerca a tu sueño.
          <b>¡Sigue mejorando, tú puedes lograrlo!</b>
        </div>
        ''')

def render(est, head, notas, firma, total):
    a = est["areas"]; g = est["icfes"]; nm = est["nombre"]
    btxt, bcol = badge(g)
    # area mas fuerte (empate: orden canonico)
    area_fuerte = max(AREAS, key=lambda ar: (a[ar], -AREAS.index(ar)))
    head_i = head.replace("{NOMBRE}", nm)
    card = (
f'''    <div class="card">
      <div>
        <div class="nombre">{nm}</div>
        <div class="meta">
          <b>Puesto:</b> {est["rank"]} de {total} &nbsp;|&nbsp; Estudiante de grado 11<br>
          Nivel de desempeño global:
          <span class="badge" style="background:{bcol}">{btxt}</span>
        </div>
      </div>
      <div class="score-box">
        <div class="lbl">Puntaje Global</div>
        <div class="val">{g}</div>
        <div class="max">escala 0 – 500</div>
      </div>
    </div>

    <h2 class="sec">Resultados del simulacro por áreas (0 – 100)</h2>
    {bars_html(a)}

    <h2 class="sec">¿A qué carreras de la Universidad de Córdoba podrías aspirar?</h2>
    {carreras_html(g, area_fuerte, a[area_fuerte])}

    ''')
    footer = (
f'''<div class="nota" style="text-align:center;border:none;color:#9aa5b1">
      Documento generado el {FECHA_DOC} &nbsp;•&nbsp; I.E. Concentracion Educ. Del Sur De Montelibano
    </div>
  </div>
</div></body></html>''')
    return head_i + card + notas + firma + footer

def main():
    roster = json.loads(ROSTER_JS.read_text(encoding="utf-8"))
    total = len(roster)
    head, notas, firma = cargar_plantilla(roster)
    rnd = random.Random(SEED)

    # 1) leer base externo por estudiante
    base = []
    for e in roster:
        h = Path(e["archivo"]).read_text(encoding="utf-8")
        d, nm = parse_externo(h)
        slug = re.sub(r'^\d+-', '', os.path.basename(e["archivo"]))
        base.append({"nombre": nm, "apellido": e.get("apellido", nm),
                     "ext": d, "slug": slug})

    # 2) generar areas sim4 (semilla fija). Ingles: bajar el promedio ~ING_DROP_OBJETIVO
    def generar(offset):
        r = random.Random(SEED)
        out = []
        for b in base:
            a = {}
            for ar in AREAS:
                base_v = b["ext"][ar]
                tgt = base_v + r.gauss(0, SD)
                if ar == "INGLÉS":
                    tgt -= offset
                tgt = min(100.0, max(0.0, tgt))
                a[ar] = achievable(tgt, PREGUNTAS[ar])
            out.append(a)
        return out

    ext_ing_avg = statistics.fmean(b["ext"]["INGLÉS"] for b in base)
    # auto-ajuste del offset para que la caida de Ingles quede en [5,7] ~ objetivo
    best = None
    for off in [x / 2 for x in range(6, 30)]:      # 3.0 .. 14.5
        areas_try = generar(off)
        ing_avg = statistics.fmean(a["INGLÉS"] for a in areas_try)
        drop = ext_ing_avg - ing_avg
        score = abs(drop - ING_DROP_OBJETIVO)
        if best is None or score < best[0]:
            best = (score, off, drop, ing_avg, areas_try)
    _, off, drop, ing_avg, areas_final = best

    estudiantes = []
    for b, a in zip(base, areas_final):
        estudiantes.append({"nombre": b["nombre"], "apellido": b["apellido"],
                            "slug": b["slug"], "areas": a, "icfes": icfes(a)})

    # 3) ranking por global (desc); desempate estable por nombre
    estudiantes.sort(key=lambda e: (-e["icfes"], e["nombre"]))
    for i, e in enumerate(estudiantes, 1):
        e["rank"] = i
        e["archivo"] = f"reportes_sim4/{i:03d}-{e['slug']}"
        e["estado"] = "Con opciones" if e["icfes"] >= MIN_REF else "A seguir mejorando"

    # 4) escribir reportes
    OUT_DIR.mkdir(exist_ok=True)
    for e in estudiantes:
        (BASE / e["archivo"]).write_text(render(e, head, notas, firma, total),
                                         encoding="utf-8")

    # 5) indices
    indice = [{"nombre": e["nombre"], "apellido": e["apellido"], "archivo": e["archivo"],
               "icfes": e["icfes"], "estado": e["estado"], "rank": e["rank"]}
              for e in estudiantes]
    OUT_INDICE.write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")

    areas_idx = []
    for e in estudiantes:
        row = {"nombre": e["nombre"], "icfes": float(e["icfes"])}
        for ar in AREAS:
            row[KEY[ar]] = float(e["areas"][ar])
        areas_idx.append(row)
    OUT_AREAS.write_text(json.dumps(areas_idx, ensure_ascii=False, indent=1), encoding="utf-8")

    # 6) resumen
    print(f"✅ sim4 generado: {len(estudiantes)} estudiantes en {OUT_DIR}")
    print(f"   Ingles: promedio externo {ext_ing_avg:.2f} -> sim4 {ing_avg:.2f} "
          f"(caida {drop:.2f} pts, offset {off})")
    for ar in AREAS:
        ea = statistics.fmean(b['ext'][ar] for b in base)
        sa = statistics.fmean(e['areas'][ar] for e in estudiantes)
        print(f"   {DISPLAY[ar]:32} externo {ea:5.1f}  sim4 {sa:5.1f}")
    gs = [e["icfes"] for e in estudiantes]
    print(f"   Global sim4: min {min(gs)}  max {max(gs)}  prom {statistics.fmean(gs):.1f}")
    print(f"   Con opciones: {sum(1 for e in estudiantes if e['estado']=='Con opciones')}")

if __name__ == "__main__":
    main()
