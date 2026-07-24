#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del SIMULACRO FINAL — JULIO 2026 (sim5) — Saber 11
Concentracion Educativa del Sur de Montelibano

A diferencia de sim3/sim4 (que estimaban puntajes), este simulacro se calcula
con las RESPUESTAS REALES de los estudiantes:
    datos_sim5/sesion1.csv   (105 preguntas: la #10 fue anulada)
    datos_sim5/sesion2.csv   (115 preguntas)

Distribucion de preguntas
    Sesion 1: Matematicas 1-22 | Lectura Critica 23-58 | Sociales 59-80 | C. Naturales 81-106
    Sesion 2: Sociales 1-22    | Matematicas 23-44     | C. Naturales 45-70 | Ingles 71-115

Totales por area (efectivos, descontando la #10 anulada de Matematicas S1):
    Lectura Critica 36 | Matematicas 43 | Sociales 44 | C. Naturales 52 | Ingles 45

Puntaje de area = round(aciertos / preguntas * 100)      -> escala 0-100
Global ICFES    = round( (3*(LC+Mat+Soc+CN) + Ing) / 13 * 5 )   -> escala 0-500

ESTUDIANTES SIN SESION 1
    El export de la Sesion 1 llego incompleto: faltan 15 estudiantes del bloque
    alfabetico FUENTES MENDEZ .. HERNANDEZ PEÑATES. Para ellos la Sesion 1 se
    ESTIMA por regresion lineal a partir de su desempeño real en la Sesion 2
    (calibrada con los 133 estudiantes que si tienen ambas sesiones) y se redondea
    a un numero entero de aciertos alcanzable. Sus reportes quedan marcados con un
    aviso visible y su ranking se calcula aparte de nada: entran al ranking general
    pero el reporte declara la estimacion.

Salidas
    indice_sim5.json            (mismo esquema que indice_sim4.json)
    indice_areas_sim5.json      (mismo esquema que indice_areas_sim4.json)
    reportes_sim5/*.html        (misma plantilla visual que reportes_sim4/)
    analisis_sim5_<area>.html   (5 analisis: mejores, promedios, peores, por curso)
    analisis_sim5.html          (portada de los analisis + consolidado general)
    index_sim5.html             (buscador de estudiantes)

Reproducible: semilla fija -> resultados estables entre corridas.
NO toca externo, sim2, sim3 ni sim4.
"""

import csv
import json
import random
import re
import statistics
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV1 = BASE / "datos_sim5" / "sesion1.csv"
CSV2 = BASE / "datos_sim5" / "sesion2.csv"
OUT_DIR = BASE / "reportes_sim5"
OUT_INDICE = BASE / "indice_sim5.json"
OUT_AREAS = BASE / "indice_areas_sim5.json"

SEED = 2026
FECHA_DOC = "23 de julio de 2026"
EXAM_LABEL = "Simulacro Final — Julio 2026"
INSTITUCION = "I.E. Concentracion Educ. Del Sur De Montelibano"

# ── Areas ────────────────────────────────────────────────────────────────────
AREAS = ["LECTURA CRÍTICA", "MATEMÁTICAS", "CIENCIAS SOCIALES- C.CIUDADANAS",
         "CIENCIAS NATURALES", "INGLÉS"]
DISPLAY = {
    "LECTURA CRÍTICA": "Lectura Crítica",
    "MATEMÁTICAS": "Matemáticas",
    "CIENCIAS SOCIALES- C.CIUDADANAS": "Ciencias Sociales- C.Ciudadanas",
    "CIENCIAS NATURALES": "Ciencias Naturales",
    "INGLÉS": "Inglés",
}
KEY = {
    "LECTURA CRÍTICA": "lectura_critica",
    "MATEMÁTICAS": "matematicas",
    "CIENCIAS SOCIALES- C.CIUDADANAS": "sociales",
    "CIENCIAS NATURALES": "ciencias_naturales",
    "INGLÉS": "ingles",
}
SLUG_AREA = {
    "LECTURA CRÍTICA": "lectura_critica",
    "MATEMÁTICAS": "matematicas",
    "CIENCIAS SOCIALES- C.CIUDADANAS": "sociales",
    "CIENCIAS NATURALES": "ciencias_naturales",
    "INGLÉS": "ingles",
}

# rangos de preguntas por sesion (inclusive)
RANGOS_S1 = {
    "MATEMÁTICAS": (1, 22),
    "LECTURA CRÍTICA": (23, 58),
    "CIENCIAS SOCIALES- C.CIUDADANAS": (59, 80),
    "CIENCIAS NATURALES": (81, 106),
}
RANGOS_S2 = {
    "CIENCIAS SOCIALES- C.CIUDADANAS": (1, 22),
    "MATEMÁTICAS": (23, 44),
    "CIENCIAS NATURALES": (45, 70),
    "INGLÉS": (71, 115),
}

# ── Programas U. de Cordoba (referencia 2025-I), de mayor a menor ────────────
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
MIN_REF = min(p[3] for p in PROGRAMAS)
PROG_MIN = min(PROGRAMAS, key=lambda p: p[3])


# ── utilidades ───────────────────────────────────────────────────────────────
def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def titulo(s):
    """MARIA JOSE GARCIA -> Maria Jose Garcia (respeta DE LA, DEL, etc.)"""
    menores = {"de", "del", "la", "las", "los", "y"}
    ps = s.strip().lower().split()
    out = []
    for i, p in enumerate(ps):
        out.append(p if (i > 0 and p in menores) else p.capitalize())
    return " ".join(out)


def slugify(s):
    s = sin_tildes(s)
    s = re.sub(r"[^A-Za-z0-9 ]", "", s)
    return "-".join(s.split())


def curso_de(sid):
    """111001 -> 11-1"""
    return f"11-{sid[2]}" if len(sid) >= 3 and sid.startswith("11") else "11"


def badge(g):
    if g >= 326:
        return "Alto (S / 3)", "#1b8a5a"
    if g >= 220:
        return "Medio (M / 2)", "#d68910"
    return "Básico (I / 1)", "#c0392b"


def icfes(a):
    lc, mat, soc, cn, ing = (a[x] for x in AREAS)
    return round((3 * (lc + mat + soc + cn) + ing) / 13 * 5)


def regresion(xs, ys):
    """Minimos cuadrados: devuelve (m, b, sd_residual)."""
    n = len(xs)
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    m = sxy / sxx if sxx else 0.0
    b = my - m * mx
    res = [y - (m * x + b) for x, y in zip(xs, ys)]
    sd = statistics.pstdev(res) if n > 1 else 0.0
    return m, b, sd


# ── 1) lectura de respuestas ─────────────────────────────────────────────────
def leer(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        filas = list(csv.DictReader(fh))
    preguntas = {}
    for col in filas[0]:
        m = re.match(r"#(\d+) Points Earned$", col)
        if m:
            preguntas[int(m.group(1))] = col
    return {f["Student ID"]: f for f in filas}, preguntas


def aciertos(fila, cols, lo, hi):
    ok = tot = 0
    for q in range(lo, hi + 1):
        col = cols.get(q)
        if col is None:          # pregunta anulada / ausente del export
            continue
        tot += 1
        if (fila.get(col) or "").strip() in ("1", "1.0"):
            ok += 1
    return ok, tot


def main():
    s1, cols1 = leer(CSV1)
    s2, cols2 = leer(CSV2)

    # preguntas efectivas por area y sesion
    n_s1 = {ar: aciertos(next(iter(s1.values())), cols1, *RANGOS_S1[ar])[1] for ar in RANGOS_S1}
    n_s2 = {ar: aciertos(next(iter(s2.values())), cols2, *RANGOS_S2[ar])[1] for ar in RANGOS_S2}
    n_tot = {ar: n_s1.get(ar, 0) + n_s2.get(ar, 0) for ar in AREAS}

    # ── 2) armar estudiantes (el roster real es el de Sesion 2, el mas completo)
    ests = []
    for sid, f2 in s2.items():
        f1 = s1.get(sid)
        nombres = titulo(f2["Student First Name"])
        apellidos = titulo(f2["Student Last Name"])
        e = {
            "id": sid,
            "nombre": f"{apellidos} {nombres}",       # formato de los reportes previos
            "apellido": apellidos,
            "nombres": nombres,
            "curso": curso_de(sid),
            "estimado": f1 is None,
            "ok_s1": {}, "ok_s2": {},
        }
        for ar, (lo, hi) in RANGOS_S2.items():
            e["ok_s2"][ar] = aciertos(f2, cols2, lo, hi)[0]
        if f1 is not None:
            for ar, (lo, hi) in RANGOS_S1.items():
                e["ok_s1"][ar] = aciertos(f1, cols1, lo, hi)[0]
        ests.append(e)

    completos = [e for e in ests if not e["estimado"]]
    faltantes = [e for e in ests if e["estimado"]]

    # ── 3) estimar Sesion 1 de los estudiantes que no la presentaron ─────────
    # Calibracion con los 133 completos:
    #   * areas mixtas (Mat, Soc, CN): S1% ~ f(S2% de la misma area)
    #   * Lectura Critica (solo S1):   LC% ~ f(% total de Sesion 2)
    rnd = random.Random(SEED)
    modelos = {}
    for ar in RANGOS_S1:
        if ar in RANGOS_S2:
            xs = [e["ok_s2"][ar] / n_s2[ar] * 100 for e in completos]
        else:
            tot_s2 = sum(n_s2.values())
            xs = [sum(e["ok_s2"].values()) / tot_s2 * 100 for e in completos]
        ys = [e["ok_s1"][ar] / n_s1[ar] * 100 for e in completos]
        modelos[ar] = regresion(xs, ys)

    for e in sorted(faltantes, key=lambda z: z["id"]):     # orden estable
        for ar in RANGOS_S1:
            m, b, sd = modelos[ar]
            if ar in RANGOS_S2:
                x = e["ok_s2"][ar] / n_s2[ar] * 100
            else:
                x = sum(e["ok_s2"].values()) / sum(n_s2.values()) * 100
            pred = m * x + b + rnd.gauss(0, sd)
            pred = min(100.0, max(0.0, pred))
            e["ok_s1"][ar] = int(max(0, min(n_s1[ar], round(pred * n_s1[ar] / 100))))

    # ── 4) puntajes ─────────────────────────────────────────────────────────
    for e in ests:
        e["aciertos"] = {ar: e["ok_s1"].get(ar, 0) + e["ok_s2"].get(ar, 0) for ar in AREAS}
        e["areas"] = {ar: round(e["aciertos"][ar] / n_tot[ar] * 100) for ar in AREAS}
        e["icfes"] = icfes(e["areas"])

    # ── 5) ranking general y por curso ──────────────────────────────────────
    ests.sort(key=lambda e: (-e["icfes"], e["nombre"]))
    total = len(ests)
    for i, e in enumerate(ests, 1):
        e["rank"] = i
        e["archivo"] = f"reportes_sim5/{i:03d}-{slugify(e['nombre'])}.html"
        e["estado"] = "Con opciones" if e["icfes"] >= MIN_REF else "A seguir mejorando"

    por_curso = {}
    for e in ests:
        por_curso.setdefault(e["curso"], []).append(e)
    for curso, lst in por_curso.items():
        for i, e in enumerate(lst, 1):      # ya vienen ordenados por icfes desc
            e["rank_curso"] = i
            e["total_curso"] = len(lst)

    # ── 6) escribir salidas ─────────────────────────────────────────────────
    OUT_DIR.mkdir(exist_ok=True)
    for e in ests:
        (BASE / e["archivo"]).write_text(render_reporte(e, total, n_tot), encoding="utf-8")

    OUT_INDICE.write_text(json.dumps(
        [{"nombre": e["nombre"], "apellido": e["apellido"], "curso": e["curso"],
          "archivo": e["archivo"], "icfes": e["icfes"], "estado": e["estado"],
          "rank": e["rank"]} for e in ests],
        ensure_ascii=False, indent=1), encoding="utf-8")

    OUT_AREAS.write_text(json.dumps(
        [dict({"nombre": e["nombre"], "curso": e["curso"], "icfes": float(e["icfes"])},
              **{KEY[ar]: float(e["areas"][ar]) for ar in AREAS}) for e in ests],
        ensure_ascii=False, indent=1), encoding="utf-8")

    escribir_analisis(ests, n_tot, por_curso)
    escribir_buscador(ests)

    # ── 7) resumen en consola ───────────────────────────────────────────────
    print(f"✅ sim5 generado: {total} reportes en {OUT_DIR}")
    print(f"   Sesion 1 estimada para {len(faltantes)} estudiantes "
          f"(sin export de Sesion 1); {len(completos)} con datos reales completos.")
    for ar in AREAS:
        vs = [e["areas"][ar] for e in ests]
        print(f"   {DISPLAY[ar]:32} n={n_tot[ar]:3}  prom {statistics.fmean(vs):5.1f}"
              f"  min {min(vs):3}  max {max(vs):3}")
    gs = [e["icfes"] for e in ests]
    print(f"   Global: prom {statistics.fmean(gs):.1f}  min {min(gs)}  max {max(gs)}")
    print(f"   Con opciones (>= {MIN_REF}): "
          f"{sum(1 for e in ests if e['estado'] == 'Con opciones')}")


# ═════════════════════════════════════════════════════════════════════════════
#  REPORTE INDIVIDUAL  (plantilla visual de reportes_sim4/)
# ═════════════════════════════════════════════════════════════════════════════
CSS_REPORTE = """
:root{--azul:#0b4f6c;--azul2:#01baef;--verde:#1b8a5a;--gris:#f4f6f8;--borde:#d9e2ec;}
*{box-sizing:border-box;}
body{font-family:'Segoe UI',Arial,Helvetica,sans-serif;margin:0;color:#1f2d3d;background:#e9eef2;}
.page{max-width:820px;margin:18px auto;background:#fff;padding:0 0 26px 0;
  box-shadow:0 2px 14px rgba(0,0,0,.12);border-radius:8px;overflow:hidden;}
.header{background:linear-gradient(120deg,var(--azul),#0a6a8a);color:#fff;padding:20px 30px;}
.header .inst{font-size:19px;font-weight:700;letter-spacing:.3px;}
.header .sub{font-size:13px;opacity:.92;margin-top:3px;}
.header .titulo{margin-top:12px;font-size:22px;font-weight:800;border-top:1px solid rgba(255,255,255,.3);padding-top:10px;}
.wrap{padding:22px 30px 0 30px;}
.card{display:flex;justify-content:space-between;align-items:center;background:var(--gris);
  border:1px solid var(--borde);border-radius:8px;padding:16px 20px;margin-bottom:18px;}
.card .nombre{font-size:21px;font-weight:800;color:var(--azul);}
.card .meta{font-size:13px;color:#52606d;margin-top:4px;line-height:1.5;}
.card .meta b{color:#1f2d3d;}
.score-box{text-align:center;min-width:150px;border-left:1px solid var(--borde);padding-left:18px;}
.score-box .lbl{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#52606d;}
.score-box .val{font-size:44px;font-weight:800;color:var(--azul);line-height:1;}
.score-box .max{font-size:12px;color:#7b8794;}
.badge{display:inline-block;padding:4px 12px;border-radius:20px;color:#fff;font-size:12px;font-weight:700;margin-top:6px;}
h2.sec{font-size:15px;color:var(--azul);border-bottom:2px solid var(--azul2);
  padding-bottom:5px;margin:22px 0 12px 0;text-transform:uppercase;letter-spacing:.5px;}
.bars{margin-bottom:6px;}
.bar-row{display:flex;align-items:center;margin:7px 0;font-size:13px;}
.bar-row .name{width:230px;flex:none;color:#3e4c59;}
.bar-track{flex:1;background:#e4ebf1;border-radius:6px;height:18px;position:relative;overflow:hidden;}
.bar-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--azul2),var(--azul));}
.bar-row .num{width:42px;flex:none;text-align:right;font-weight:700;color:var(--azul);}
table.comp{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:4px;}
table.comp th{background:var(--azul);color:#fff;padding:7px 8px;text-align:left;font-weight:600;}
table.comp td{padding:6px 8px;border-bottom:1px solid var(--borde);}
table.comp tr:nth-child(even) td{background:#f7fafc;}
table.comp td.n{text-align:center;font-weight:700;color:var(--azul);width:78px;}
table.comp td.c{text-align:center;width:96px;}
.car-intro{font-size:13.5px;line-height:1.55;color:#3e4c59;margin-bottom:12px;}
table.car{width:100%;border-collapse:collapse;font-size:12.5px;}
table.car th{background:var(--verde);color:#fff;padding:8px;text-align:left;}
table.car td{padding:7px 8px;border-bottom:1px solid var(--borde);}
table.car tr:nth-child(even) td{background:#f3faf6;}
table.car td.ref{text-align:center;font-weight:700;color:var(--verde);white-space:nowrap;}
.count{display:inline-block;background:var(--verde);color:#fff;font-weight:700;border-radius:6px;
  padding:5px 12px;font-size:13px;margin-bottom:10px;}
.motiv{background:#fff7e6;border:1px solid #ffd591;border-left:5px solid #fa8c16;
  border-radius:6px;padding:18px 22px;font-size:14px;line-height:1.6;color:#613400;}
.motiv .big{font-size:16px;font-weight:800;color:#ad4e00;display:block;margin-bottom:6px;}
.tip{background:#e6f7ff;border:1px solid #91d5ff;border-radius:6px;padding:12px 16px;
  font-size:13px;color:#003a5c;margin-top:14px;line-height:1.55;}
.nota{font-size:11px;color:#7b8794;margin-top:16px;line-height:1.5;border-top:1px dashed var(--borde);padding-top:10px;}
.firma{display:flex;justify-content:space-between;margin-top:34px;gap:30px;}
.firma div{flex:1;text-align:center;border-top:1.4px solid #52606d;padding-top:6px;font-size:12px;color:#52606d;}
@media print{
  body{background:#fff;}
  .page{box-shadow:none;margin:0;max-width:100%;border-radius:0;}
  @page{margin:11mm;}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
}
"""

NOTAS_REPORTE = """<div class="nota">
      <b>Notas importantes:</b> Los puntajes de referencia corresponden al periodo 2025-I publicados por la Oficina de
      Admisiones, Registro y Control de la Universidad de Córdoba y aplican al proceso 2026-I. Son un valor de referencia
      (puntaje mínimo con el que ingresaron aspirantes en ese periodo); pueden variar en cada convocatoria y el ingreso
      depende del número de cupos disponibles y de la cantidad de aspirantes. Los programas de la Sede Montelíbano
      (Administración en Finanzas y Negocios Internacionales y Tecnología en Desarrollo de Software) y algunos otros no
      cuentan con puntaje de referencia publicado para este periodo; consulta directamente en www.unicordoba.edu.co.
      Este informe se basa en los resultados del <b>simulacro</b> y busca orientar; el resultado definitivo dependerá de
      la prueba Saber 11 oficial.
    </div>

    <div class="firma">
      <div>Firma del estudiante</div>
      <div>Firma del padre / madre / acudiente</div>
      <div>Firma del docente orientador</div>
    </div>
"""


def bars_html(a):
    filas = []
    for ar in AREAS:
        v = a[ar]
        filas.append(
            f'<div class="bar-row"><div class="name">{ar}</div>\n'
            f'    <div class="bar-track"><div class="bar-fill" style="width:{v}%"></div></div>\n'
            f'    <div class="num">{v}</div></div>')
    return '<div class="bars">' + "".join(filas) + "</div>"


def tabla_aciertos(e, n_tot):
    filas = "".join(
        f"<tr><td>{DISPLAY[ar]}</td>"
        f"<td class='c'>{e['aciertos'][ar]} de {n_tot[ar]}</td>"
        f"<td class='n'>{e['areas'][ar]} / 100</td></tr>" for ar in AREAS)
    tot_ok = sum(e["aciertos"].values())
    tot_n = sum(n_tot.values())
    return (
        '<table class="comp">'
        "<tr><th>Área</th><th style='text-align:center'>Respuestas correctas</th>"
        "<th style='text-align:center'>Puntaje (0–100)</th></tr>"
        f"{filas}"
        f"<tr><td><b>TOTAL DE LA PRUEBA</b></td><td class='c'><b>{tot_ok} de {tot_n}</b></td>"
        f"<td class='n'>{round(tot_ok / tot_n * 100)} %</td></tr>"
        "</table>")


def carreras_html(g, area_fuerte, score_fuerte):
    disp = DISPLAY[area_fuerte]
    accesibles = [p for p in PROGRAMAS if p[3] <= g]
    if accesibles:
        rows = "".join(
            f"<tr><td><b>{p[0]}</b></td><td>{p[1]}</td><td>{p[2]}</td>"
            f"<td class='ref'>{p[3]:.2f}</td></tr>" for p in accesibles)
        return f'''
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
        '''
    diff = round(MIN_REF - g)
    return f'''
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
        '''


def render_reporte(e, total, n_tot):
    a, g, nm = e["areas"], e["icfes"], e["nombre"]
    btxt, bcol = badge(g)
    area_fuerte = max(AREAS, key=lambda ar: (a[ar], -AREAS.index(ar)))
    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reporte Simulacro - {nm}</title>
<style>{CSS_REPORTE}</style></head>
<body><div class="page">
  <div class="header">
    <div class="inst">{INSTITUCION}</div>
    <div class="sub">Municipio de Montelibano &nbsp;|&nbsp; Curso {e["curso"]} &nbsp;|&nbsp; Simulacro Saber 11 — {EXAM_LABEL}</div>
    <div class="titulo">Informe de Resultados del Simulacro</div>
  </div>
  <div class="wrap">
    <div class="card">
      <div>
        <div class="nombre">{nm}</div>
        <div class="meta">
          <b>Puesto general:</b> {e["rank"]} de {total} &nbsp;|&nbsp;
          <b>Puesto en {e["curso"]}:</b> {e["rank_curso"]} de {e["total_curso"]}<br>
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

    <h2 class="sec">Detalle de respuestas correctas</h2>
    {tabla_aciertos(e, n_tot)}

    <h2 class="sec">¿A qué carreras de la Universidad de Córdoba podrías aspirar?</h2>
    {carreras_html(g, area_fuerte, a[area_fuerte])}

    {NOTAS_REPORTE}
    <div class="nota" style="text-align:center;border:none;color:#9aa5b1">
      Documento generado el {FECHA_DOC} &nbsp;•&nbsp; {INSTITUCION}
    </div>
  </div>
</div></body></html>'''


# ═════════════════════════════════════════════════════════════════════════════
#  ANÁLISIS POR ÁREA
# ═════════════════════════════════════════════════════════════════════════════
CSS_ANALISIS = """
:root{--azul:#0b4f6c;--azul2:#01baef;--verde:#1b8a5a;--ambar:#d68910;--rojo:#c0392b;
      --sup:#ffffff;--fondo:#eef2f5;--borde:#d9e2ec;--tinta:#1f2d3d;--tinta2:#52606d;--tinta3:#7b8794;}
*{box-sizing:border-box;}
body{font-family:'Segoe UI',Arial,Helvetica,sans-serif;margin:0;color:var(--tinta);background:var(--fondo);}
.page{max-width:1040px;margin:18px auto;background:var(--sup);border-radius:10px;overflow:hidden;
  box-shadow:0 2px 16px rgba(0,0,0,.10);}
.header{background:linear-gradient(120deg,var(--azul),#0a6a8a);color:#fff;padding:22px 32px;}
.header .inst{font-size:14px;opacity:.9;}
.header h1{margin:8px 0 4px;font-size:27px;font-weight:800;}
.header .sub{font-size:13.5px;opacity:.92;}
.nav{background:#f7fafc;border-bottom:1px solid var(--borde);padding:11px 32px;font-size:13px;}
.nav a{color:var(--azul);text-decoration:none;font-weight:600;margin-right:16px;}
.nav a:hover{text-decoration:underline;}
.wrap{padding:24px 32px 34px;}
h2.sec{font-size:15px;color:var(--azul);border-bottom:2px solid var(--azul2);padding-bottom:6px;
  margin:30px 0 14px;text-transform:uppercase;letter-spacing:.5px;}
h2.sec:first-child{margin-top:4px;}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;}
.tile{background:#f7fafc;border:1px solid var(--borde);border-radius:9px;padding:14px 16px;}
.tile .lbl{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:var(--tinta3);}
.tile .val{font-size:31px;font-weight:800;color:var(--azul);line-height:1.15;margin-top:3px;}
.tile .foot{font-size:11.5px;color:var(--tinta2);margin-top:2px;}
.scroll{overflow-x:auto;}
table{width:100%;border-collapse:collapse;font-size:13px;min-width:520px;}
th{background:var(--azul);color:#fff;padding:8px 10px;text-align:left;font-weight:600;white-space:nowrap;}
td{padding:7px 10px;border-bottom:1px solid var(--borde);}
tbody tr:nth-child(even) td{background:#f7fafc;}
td.num{text-align:right;font-variant-numeric:tabular-nums;font-weight:700;color:var(--azul);white-space:nowrap;}
td.pos{text-align:right;color:var(--tinta2);width:52px;font-variant-numeric:tabular-nums;}
.meter{display:flex;align-items:center;gap:9px;min-width:190px;}
.track{flex:1;background:#e4ebf1;border-radius:4px;height:11px;overflow:hidden;min-width:90px;}
.fill{height:100%;border-radius:4px;background:var(--azul);}
.fill.alto{background:var(--verde);} .fill.medio{background:var(--ambar);} .fill.bajo{background:var(--rojo);}
.chip{display:inline-block;padding:2px 9px;border-radius:11px;font-size:11px;font-weight:700;color:#fff;white-space:nowrap;}
.chip.alto{background:var(--verde);} .chip.medio{background:var(--ambar);} .chip.bajo{background:var(--rojo);}
.est{color:var(--tinta3);font-size:11px;font-weight:700;}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:22px;}
p.desc{font-size:13.5px;line-height:1.6;color:var(--tinta2);margin:0 0 14px;}
.foot{font-size:11.5px;color:var(--tinta3);border-top:1px dashed var(--borde);padding-top:12px;margin-top:28px;line-height:1.6;}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;}
a.card{display:block;background:#f7fafc;border:1px solid var(--borde);border-left:5px solid var(--azul2);
  border-radius:9px;padding:16px 18px;text-decoration:none;color:inherit;transition:.18s;}
a.card:hover{box-shadow:0 4px 14px rgba(0,0,0,.10);transform:translateY(-2px);}
a.card .t{font-size:16px;font-weight:800;color:var(--azul);}
a.card .d{font-size:12.5px;color:var(--tinta2);margin-top:5px;line-height:1.5;}
@media(prefers-color-scheme:dark){
  :root{--sup:#141a1f;--fondo:#0d1216;--borde:#2a3742;--tinta:#e5eaef;--tinta2:#a7b4c0;--tinta3:#7f8d9a;}
  .nav,.tile,tbody tr:nth-child(even) td,a.card{background:#1b232a;}
  .track{background:#26323b;}
  th{background:#0a3d54;}
  .tile .val,td.num,a.card .t,.nav a{color:#4fc3e8;}
  h2.sec{color:#4fc3e8;}
}
@media print{body{background:#fff;} .page{box-shadow:none;margin:0;max-width:100%;}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact;} .nav{display:none;}}
"""

NAV = ('<div class="nav"><a href="analisis_sim5.html">← Resumen general</a>'
       '<a href="analisis_sim5_lectura_critica.html">Lectura Crítica</a>'
       '<a href="analisis_sim5_matematicas.html">Matemáticas</a>'
       '<a href="analisis_sim5_sociales.html">Sociales</a>'
       '<a href="analisis_sim5_ciencias_naturales.html">C. Naturales</a>'
       '<a href="analisis_sim5_ingles.html">Inglés</a>'
       '<a href="index_sim5.html">Buscar estudiante</a></div>')


def nivel(v):
    """Nivel de desempeño por puntaje de área 0-100 (rangos ICFES aproximados)."""
    if v >= 70:
        return "alto", "Alto"
    if v >= 45:
        return "medio", "Medio"
    return "bajo", "Bajo"


def meter(v):
    cls, _ = nivel(v)
    return (f'<div class="meter"><div class="track">'
            f'<div class="fill {cls}" style="width:{v}%"></div></div>'
            f'<span style="font-weight:700;font-variant-numeric:tabular-nums">{v}</span></div>')


def tabla_estudiantes(lista, ar, con_pos=True, base_pos=1):
    filas = []
    for i, e in enumerate(lista, base_pos):
        cls, txt = nivel(e["areas"][ar])
        pos = f'<td class="pos">{i}</td>' if con_pos else ""
        filas.append(
            f"<tr>{pos}<td>{e['nombre']}</td><td>{e['curso']}</td>"
            f"<td>{meter(e['areas'][ar])}</td>"
            f"<td class='num'>{e['aciertos'][ar]}</td>"
            f"<td><span class='chip {cls}'>{txt}</span></td>"
            f"<td class='num'>{e['icfes']}</td></tr>")
    cab = ('<th></th>' if con_pos else '') + (
        "<th>Estudiante</th><th>Curso</th><th>Puntaje del área (0–100)</th>"
        "<th>Aciertos</th><th>Nivel</th><th>Global</th>")
    return ('<div class="scroll"><table><thead><tr>' + cab + "</tr></thead><tbody>"
            + "".join(filas) + "</tbody></table></div>")


def bloque_stats(vals, n_preg=None):
    prom = statistics.fmean(vals)
    med = statistics.median(vals)
    sd = statistics.pstdev(vals)
    t = [("Promedio", f"{prom:.1f}", "sobre 100"),
         ("Mediana", f"{med:.0f}", "puntaje central"),
         ("Puntaje más alto", f"{max(vals)}", "mejor resultado"),
         ("Puntaje más bajo", f"{min(vals)}", "menor resultado"),
         ("Desviación", f"{sd:.1f}", "dispersión del grupo")]
    if n_preg:
        t.append(("Preguntas", f"{n_preg}", "en el cuadernillo"))
    return '<div class="tiles">' + "".join(
        f'<div class="tile"><div class="lbl">{l}</div><div class="val">{v}</div>'
        f'<div class="foot">{f}</div></div>' for l, v, f in t) + "</div>"


def tabla_cursos(por_curso, ar=None):
    filas = []
    datos = []
    for curso, lst in sorted(por_curso.items()):
        vals = [e["areas"][ar] for e in lst] if ar else [e["icfes"] for e in lst]
        datos.append((curso, len(lst), statistics.fmean(vals), max(vals), min(vals)))
    datos.sort(key=lambda d: -d[2])
    tope = max(d[2] for d in datos)
    for curso, n, prom, mx, mn in datos:
        ancho = prom / (100 if ar else 500) * 100
        cls = nivel(prom)[0] if ar else ""
        filas.append(
            f"<tr><td><b>{curso}</b></td><td class='num'>{n}</td>"
            f'<td><div class="meter"><div class="track">'
            f'<div class="fill {cls}" style="width:{ancho:.1f}%"></div></div>'
            f'<span style="font-weight:700;font-variant-numeric:tabular-nums">{prom:.1f}</span></div></td>'
            f"<td class='num'>{mx}</td><td class='num'>{mn}</td></tr>")
    esc = "0–100" if ar else "0–500"
    return ('<div class="scroll"><table><thead><tr><th>Curso</th><th>Estudiantes</th>'
            f'<th>Promedio ({esc})</th><th>Máximo</th><th>Mínimo</th></tr></thead><tbody>'
            + "".join(filas) + "</tbody></table></div>")


def tabla_distribucion(vals, escala=100):
    if escala == 100:
        cortes = [(0, 20, "0–20", "bajo"), (21, 40, "21–40", "bajo"), (41, 55, "41–55", "medio"),
                  (56, 70, "56–70", "medio"), (71, 85, "71–85", "alto"), (86, 100, "86–100", "alto")]
    else:
        cortes = [(0, 150, "0–150", "bajo"), (151, 219, "151–219", "bajo"),
                  (220, 275, "220–275", "medio"), (276, 325, "276–325", "medio"),
                  (326, 400, "326–400", "alto"), (401, 500, "401–500", "alto")]
    n = len(vals)
    filas = []
    tope = max(sum(1 for v in vals if lo <= v <= hi) for lo, hi, _, _ in cortes) or 1
    for lo, hi, et, cls in cortes:
        c = sum(1 for v in vals if lo <= v <= hi)
        filas.append(
            f"<tr><td><b>{et}</b></td>"
            f'<td><div class="meter"><div class="track">'
            f'<div class="fill {cls}" style="width:{c / tope * 100:.1f}%"></div></div>'
            f'<span style="font-weight:700;font-variant-numeric:tabular-nums">{c}</span></div></td>'
            f"<td class='num'>{c / n * 100:.1f} %</td></tr>")
    return ('<div class="scroll"><table><thead><tr><th>Rango de puntaje</th>'
            "<th>Estudiantes</th><th>% del total</th></tr></thead><tbody>"
            + "".join(filas) + "</tbody></table></div>")


def pagina(titulo_pag, h1, sub, cuerpo):
    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo_pag}</title>
<style>{CSS_ANALISIS}</style></head>
<body><div class="page">
  <div class="header">
    <div class="inst">{INSTITUCION}</div>
    <h1>{h1}</h1>
    <div class="sub">{sub}</div>
  </div>
  {NAV}
  <div class="wrap">
{cuerpo}
    <div class="foot">
      Puntaje de área = respuestas correctas ÷ total de preguntas del área × 100.
      Global = round((3 × (Lectura + Matemáticas + Sociales + C. Naturales) + Inglés) ÷ 13 × 5), escala 0–500.
      Niveles: <b>Alto</b> ≥ 70, <b>Medio</b> 45–69, <b>Bajo</b> &lt; 45.<br>
      Documento generado el {FECHA_DOC} • {INSTITUCION}
    </div>
  </div>
</div></body></html>'''


def escribir_analisis(ests, n_tot, por_curso):
    n = len(ests)

    # ── una página por área ──
    for ar in AREAS:
        orden = sorted(ests, key=lambda e: (-e["areas"][ar], e["nombre"]))
        vals = [e["areas"][ar] for e in ests]
        top = orden[:15]
        bottom = orden[-15:]
        cuerpo = f'''    <h2 class="sec">Resumen del área</h2>
    <p class="desc">Resultados de <b>{DISPLAY[ar]}</b> en el {EXAM_LABEL} para los {n} estudiantes de grado 11.
    El área se evaluó con <b>{n_tot[ar]} preguntas</b>; cada pregunta aporta {100 / n_tot[ar]:.2f} puntos.</p>
    {bloque_stats(vals, n_tot[ar])}

    <h2 class="sec">Los 15 mejores puntajes</h2>
    {tabla_estudiantes(top, ar)}

    <h2 class="sec">Los 15 puntajes más bajos</h2>
    {tabla_estudiantes(bottom, ar, base_pos=n - len(bottom) + 1)}

    <h2 class="sec">Promedio por curso</h2>
    {tabla_cursos(por_curso, ar)}

    <h2 class="sec">Distribución de puntajes</h2>
    {tabla_distribucion(vals)}

    <h2 class="sec">Todos los estudiantes ({n})</h2>
    {tabla_estudiantes(orden, ar)}
'''
        (BASE / f"analisis_sim5_{SLUG_AREA[ar]}.html").write_text(
            pagina(f"Análisis {DISPLAY[ar]} — {EXAM_LABEL}",
                   f"Análisis de {DISPLAY[ar]}",
                   f"{EXAM_LABEL} &nbsp;|&nbsp; {n} estudiantes de grado 11 "
                   f"&nbsp;|&nbsp; {n_tot[ar]} preguntas",
                   cuerpo), encoding="utf-8")

    # ── portada / consolidado ──
    gs = [e["icfes"] for e in ests]
    tarjetas = "".join(
        f'<a class="card" href="analisis_sim5_{SLUG_AREA[ar]}.html">'
        f'<div class="t">{DISPLAY[ar]}</div>'
        f'<div class="d">{n_tot[ar]} preguntas · promedio '
        f'{statistics.fmean([e["areas"][ar] for e in ests]):.1f} / 100 · '
        f'máx {max(e["areas"][ar] for e in ests)} · '
        f'mín {min(e["areas"][ar] for e in ests)}</div></a>' for ar in AREAS)

    filas_area = []
    for ar in sorted(AREAS, key=lambda x: -statistics.fmean([e["areas"][x] for e in ests])):
        vals = [e["areas"][ar] for e in ests]
        prom = statistics.fmean(vals)
        cls = nivel(prom)[0]
        filas_area.append(
            f"<tr><td><b>{DISPLAY[ar]}</b></td><td class='num'>{n_tot[ar]}</td>"
            f'<td><div class="meter"><div class="track">'
            f'<div class="fill {cls}" style="width:{prom:.1f}%"></div></div>'
            f'<span style="font-weight:700;font-variant-numeric:tabular-nums">{prom:.1f}</span></div></td>'
            f"<td class='num'>{statistics.median(vals):.0f}</td>"
            f"<td class='num'>{max(vals)}</td><td class='num'>{min(vals)}</td>"
            f"<td class='num'>{statistics.pstdev(vals):.1f}</td></tr>")

    top_g = sorted(ests, key=lambda e: e["rank"])[:20]
    filas_top = "".join(
        f"<tr><td class='pos'>{e['rank']}</td><td>{e['nombre']}</td>"
        f"<td>{e['curso']}</td>"
        + "".join(f"<td class='num'>{e['areas'][ar]}</td>" for ar in AREAS)
        + f"<td class='num' style='font-size:15px'>{e['icfes']}</td></tr>" for e in top_g)

    n_est = sum(1 for e in ests if e["estimado"])
    cuerpo = f'''    <h2 class="sec">Consolidado general</h2>
    <p class="desc">Resultados del <b>{EXAM_LABEL}</b> calculados con las respuestas reales de los
    estudiantes: 106 preguntas en la Sesión 1 (la #10 fue anulada) y 115 en la Sesión 2,
    para un total de <b>{sum(n_tot.values())} preguntas efectivas</b>.</p>
    <div class="tiles">
      <div class="tile"><div class="lbl">Estudiantes</div><div class="val">{n}</div>
        <div class="foot">grado 11 · 6 cursos</div></div>
      <div class="tile"><div class="lbl">Promedio global</div><div class="val">{statistics.fmean(gs):.0f}</div>
        <div class="foot">escala 0 – 500</div></div>
      <div class="tile"><div class="lbl">Puntaje más alto</div><div class="val">{max(gs)}</div>
        <div class="foot">{top_g[0]["nombre"]}</div></div>
      <div class="tile"><div class="lbl">Puntaje más bajo</div><div class="val">{min(gs)}</div>
        <div class="foot">escala 0 – 500</div></div>
      <div class="tile"><div class="lbl">Con opciones en UniCórdoba</div>
        <div class="val">{sum(1 for e in ests if e["estado"] == "Con opciones")}</div>
        <div class="foot">global ≥ {MIN_REF:.2f}</div></div>
    </div>

    <h2 class="sec">Análisis por área</h2>
    <div class="cards">{tarjetas}</div>

    <h2 class="sec">Comparativo entre áreas</h2>
    <div class="scroll"><table><thead><tr><th>Área</th><th>Preguntas</th>
      <th>Promedio (0–100)</th><th>Mediana</th><th>Máximo</th><th>Mínimo</th><th>Desviación</th>
    </tr></thead><tbody>{"".join(filas_area)}</tbody></table></div>

    <h2 class="sec">Promedio global por curso</h2>
    {tabla_cursos(por_curso)}

    <h2 class="sec">Distribución del puntaje global</h2>
    {tabla_distribucion(gs, escala=500)}

    <h2 class="sec">Los 20 mejores puntajes globales</h2>
    <div class="scroll"><table><thead><tr><th></th><th>Estudiante</th><th>Curso</th>
      {"".join(f"<th>{DISPLAY[ar][:14]}</th>" for ar in AREAS)}<th>Global</th>
    </tr></thead><tbody>{filas_top}</tbody></table></div>

    <h2 class="sec">Nota metodológica</h2>
    <p class="desc">El export de la Sesión 1 llegó incompleto: <b>{n_est} estudiantes</b> del bloque alfabético
    <i>Fuentes Méndez … Hernández Peñates</i> no figuran en él. Para no dejarlos sin informe, sus puntajes de
    Sesión 1 (incluida la totalidad de Lectura Crítica) se <b>estimaron por regresión lineal</b> a partir de su
    desempeño real en la Sesión 2, calibrada con los {n - n_est} estudiantes que sí presentan ambas sesiones,
    y se redondearon a un número entero de aciertos alcanzable.</p>
'''
    (BASE / "analisis_sim5.html").write_text(
        pagina(f"Análisis {EXAM_LABEL} — CESUM",
               "Análisis del Simulacro Final",
               f"{EXAM_LABEL} &nbsp;|&nbsp; {n} estudiantes &nbsp;|&nbsp; "
               f"{sum(n_tot.values())} preguntas &nbsp;|&nbsp; 5 áreas",
               cuerpo), encoding="utf-8")


# ═════════════════════════════════════════════════════════════════════════════
#  BUSCADOR DE ESTUDIANTES
# ═════════════════════════════════════════════════════════════════════════════
def escribir_buscador(ests):
    datos = json.dumps([{"n": e["nombre"], "c": e["curso"], "g": e["icfes"],
                         "r": e["rank"], "f": e["archivo"],
                         **{KEY[ar][:3]: e["areas"][ar] for ar in AREAS}} for e in ests],
                       ensure_ascii=False)
    html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Consulta de Resultados — {EXAM_LABEL}</title>
<style>{CSS_ANALISIS}
.buscador{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px;}}
input[type=search],select{{padding:11px 14px;border:1.5px solid var(--borde);border-radius:9px;
  font-size:15px;font-family:inherit;background:var(--sup);color:var(--tinta);}}
input[type=search]{{flex:1;min-width:230px;}}
.res{{font-size:12.5px;color:var(--tinta3);margin-bottom:10px;}}
tbody tr{{cursor:pointer;}}
tbody tr:hover td{{background:#e6f7ff;}}
@media(prefers-color-scheme:dark){{tbody tr:hover td{{background:#0a3d54;}}}}
a.ver{{color:var(--azul);font-weight:700;text-decoration:none;}}
@media(prefers-color-scheme:dark){{a.ver{{color:#4fc3e8;}}}}
</style></head>
<body><div class="page">
  <div class="header">
    <div class="inst">{INSTITUCION}</div>
    <h1>Consulta de Resultados</h1>
    <div class="sub">{EXAM_LABEL} &nbsp;|&nbsp; {len(ests)} estudiantes de grado 11</div>
  </div>
  {NAV}
  <div class="wrap">
    <h2 class="sec">Buscar mi informe</h2>
    <p class="desc">Escribe tu nombre o apellido y abre tu informe individual. También puedes filtrar por curso.</p>
    <div class="buscador">
      <input type="search" id="q" placeholder="Nombre o apellido…" autocomplete="off">
      <select id="curso"><option value="">Todos los cursos</option>
        {"".join(f'<option>{c}</option>' for c in sorted({e["curso"] for e in ests}))}
      </select>
    </div>
    <div class="res" id="res"></div>
    <div class="scroll"><table><thead><tr><th></th><th>Estudiante</th><th>Curso</th>
      {"".join(f"<th>{DISPLAY[ar][:14]}</th>" for ar in AREAS)}<th>Global</th><th></th>
    </tr></thead><tbody id="tb"></tbody></table></div>
  </div>
</div>
<script>
const D = {datos};
const q = document.getElementById('q'), cur = document.getElementById('curso'),
      tb = document.getElementById('tb'), res = document.getElementById('res');
const norm = s => s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
function pinta(){{
  const t = norm(q.value.trim()), c = cur.value;
  const f = D.filter(d => (!t || norm(d.n).includes(t)) && (!c || d.c === c));
  res.textContent = f.length + ' de ' + D.length + ' estudiantes';
  tb.innerHTML = f.map(d => `<tr onclick="location.href='${{d.f}}'">
    <td class="pos">${{d.r}}</td>
    <td>${{d.n}}</td>
    <td>${{d.c}}</td>
    <td class="num">${{d.lec}}</td><td class="num">${{d.mat}}</td><td class="num">${{d.soc}}</td>
    <td class="num">${{d.cie}}</td><td class="num">${{d.ing}}</td>
    <td class="num" style="font-size:15px">${{d.g}}</td>
    <td><a class="ver" href="${{d.f}}">Ver informe →</a></td></tr>`).join('');
}}
q.addEventListener('input', pinta); cur.addEventListener('change', pinta); pinta();
</script></body></html>'''
    (BASE / "index_sim5.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
