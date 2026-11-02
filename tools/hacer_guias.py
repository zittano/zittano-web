"""Genera las guías nuevas (fechas clave y preguntas frecuentes) con el mismo diseño que las existentes."""
import json, html, os

BASE = "https://www.zittano.com.ar"
ORG = {"@type": "ProfessionalService", "@id": BASE + "/#organizacion",
       "name": "Zittano · Gestoría de Ciudadanías", "url": BASE + "/",
       "logo": BASE + "/logo-zittano.png"}
WA = "https://wa.me/5491173674060?text=Hola%20Zittano%21%20Le%C3%AD%20una%20gu%C3%ADa%20en%20la%20web%20y%20quiero%20consultar%20por%20mi%20caso"

HEAD = open("guias/aranceles-ciudadania-italiana/index.html", encoding="utf-8").read()
HEADER = HEAD[HEAD.index("<body>"):HEAD.index("<main")]
FOOTER = HEAD[HEAD.index("</main>"):]


def page(slug, title, h1, desc, corto, article, faqs, rel):
    url = f"{BASE}/guias/{slug}/"
    graph = [
        {"@type": "Article", "headline": h1, "description": desc, "url": url,
         "mainEntityOfPage": url, "inLanguage": "es-AR",
         "datePublished": "2026-11-02", "dateModified": "2026-11-02",
         "image": BASE + "/og-image.jpg", "author": {"@id": BASE + "/#organizacion"},
         "publisher": ORG, "about": "Ciudadanía italiana"},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guías", "item": BASE + "/guias/"},
            {"@type": "ListItem", "position": 3, "name": h1, "item": url}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    e = html.escape
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)
    rel_html = "".join(f'<a class="card" href="{h}"><b>{e(t)}</b><span>{e(d)}</span></a>' for h, t, d in rel)
    out = f'''<!doctype html>
<html lang="es-AR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Zittano</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)} | Zittano"><meta property="og:description" content="{e(desc)}">
<meta property="og:locale" content="es_AR"><meta property="og:image" content="{BASE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#fdf8ef">
<link rel="icon" type="image/png" href="/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Fraunces:opsz,wght@9..144,400;9..144,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/guias/guias.css">
<script type="application/ld+json">
{ld}
</script>
</head>{HEADER}<main class="wrap"><div class="narrow">
<nav class="crumbs" aria-label="Migas"><a href="/">Inicio</a> › <a href="/guias/">Guías</a> › {e(h1)}</nav>
<div class="hero"><div class="eyebrow"><span class="flag"><i style="background:#0a8f4a"></i><i style="background:#fff"></i><i style="background:#c8262b"></i></span> Guía Zittano</div>
<h1>{e(h1)}</h1>
<p class="meta">Actualizado: 2 de noviembre de 2026 · Por el equipo de abogados y gestores de Zittano</p></div>
<div class="corto"><b>En corto</b>{corto}</div>
<article>
{article}
</article>
<section class="faq"><h2>Preguntas frecuentes</h2>{faq_html}</section>
<div class="cta"><div><h3>¿Querés que veamos tu caso?</h3><p>Desde 2014 acompañamos a más de 15.000 familias de todo el país. Te responde una persona del equipo, no un bot.</p></div>
<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">Consultar por WhatsApp</a></div>
<p class="disc">Esta guía es informativa y resume la normativa vigente al 2 de noviembre de 2026. Las reglas y los aranceles pueden cambiar; cada caso necesita un análisis particular.</p>
</div>
<section class="rel narrow" style="margin-top:36px"><h2>Seguí leyendo</h2><div class="grid">{rel_html}</div></section>
{FOOTER}'''
    os.makedirs(f"guias/{slug}", exist_ok=True)
    open(f"guias/{slug}/index.html", "w", encoding="utf-8").write(out)


REL_LEY = ("/guias/requisitos-ciudadania-italiana/", "Quién puede tener la ciudadanía italiana en 2026", "La Ley 74/2025, sus excepciones y qué dijeron los tribunales.")
REL_MEN = ("/guias/hijos-menores-ciudadania-italiana/", "Hijos menores de italianos: qué dice la ley en 2026", "Plazos hasta 2029 y gratuidad desde 2026.")
REL_ARA = ("/guias/aranceles-ciudadania-italiana/", "Aranceles oficiales de la ciudadanía italiana en 2026", "600 euros por solicitante adulto.")
REL_FEC = ("/guias/fechas-clave-ciudadania-italiana/", "Fechas clave de la ciudadanía italiana", "Los plazos que vienen y las fechas que cambiaron las reglas.")
REL_FAQ = ("/guias/preguntas-frecuentes-ciudadania-italiana/", "Preguntas frecuentes sobre la ciudadanía italiana", "Las respuestas cortas a lo que más nos preguntan.")

# ---------- Fechas clave ----------
fechas_art = '''<h2>Los plazos que vienen</h2>
<table>
<thead><tr><th>Fecha</th><th>Qué pasa</th><th>Norma</th></tr></thead>
<tbody>
<tr><td><strong>31/12/2028</strong></td><td>Último día del período de transición: hasta entonces los consulados reciben una cantidad limitada de solicitudes de adultos por año.</td><td>Ley 11/2026</td></tr>
<tr><td><strong>1/1/2029</strong></td><td>El reconocimiento de adultos residentes en el exterior pasa a una oficina central del Ministerio de Asuntos Exteriores, en Roma.</td><td>Ley 11/2026</td></tr>
<tr><td><strong>31/5/2029</strong></td><td>Vence el plazo para la declaración de los hijos que eran menores de edad al 24 de mayo de 2025.</td><td>Ley 74/2025 (plazo prorrogado)</td></tr>
<tr><td><strong>3 años desde el nacimiento</strong></td><td>Plazo para la declaración de los hijos nacidos después del 24 de mayo de 2025.</td><td>Ley 74/2025</td></tr>
</tbody></table>

<h2>Las fechas que cambiaron las reglas</h2>
<table>
<thead><tr><th>Fecha</th><th>Qué pasó</th><th>Norma</th></tr></thead>
<tbody>
<tr><td>21/10/2026</td><td>Se publica en la Gaceta Oficial el nuevo planteo del Tribunal de Avellino contra la reforma.</td><td>Ordenanza del Tribunal de Avellino</td></tr>
<tr><td>10/8/2026</td><td>El Ministerio del Interior deja atrás el “minor issue” y habilita el reexamen de los rechazos.</td><td>Circular 65050/2026</td></tr>
<tr><td>26/7/2026</td><td>La Casación resuelve que el hijo con doble ciudadanía no perdió la italiana por la naturalización de su padre.</td><td>Sentencia 24045/2026</td></tr>
<tr><td>23/7/2026</td><td>La Corte Constitucional consulta al Tribunal de Justicia de la UE sobre la reforma.</td><td>Ordenanza 147/2026</td></tr>
<tr><td>Abril de 2026</td><td>La Corte Constitucional deja en pie la Ley 74/2025.</td><td>Sentencia 63/2026</td></tr>
<tr><td>19/1/2026</td><td>Se aprueba la centralización del reconocimiento de adultos en Roma desde 2029.</td><td>Ley 11/2026</td></tr>
<tr><td>1/1/2026</td><td>La declaración para hijos menores pasa a ser gratuita (antes, 250 euros).</td><td>Ley de Presupuesto italiana</td></tr>
<tr><td>24/5/2025</td><td>Fecha de referencia para el plazo de los hijos menores.</td><td>Ley 74/2025</td></tr>
<tr><td>27/3/2025, 23:59 (Roma)</td><td>Corte de la reforma: lo iniciado antes sigue con las reglas anteriores; lo posterior, con los límites del artículo 3-bis.</td><td>Decreto-ley 36/2025, Ley 74/2025</td></tr>
<tr><td>1/1/2025</td><td>El arancel del reconocimiento sube de 300 a 600 euros por solicitante adulto.</td><td>Ley de Presupuesto italiana 2025</td></tr>
<tr><td>3/10/2024</td><td>El Ministerio del Interior adopta el criterio del “minor issue” (hoy superado).</td><td>Circular 43347/2024</td></tr>
<tr><td>1/1/1948</td><td>Desde esta fecha las mujeres transmiten la ciudadanía a sus hijos; antes, solo por vía judicial.</td><td>Constitución italiana</td></tr>
</tbody></table>
<p>Para el detalle de cada cambio, mirá la <a href="/guias/requisitos-ciudadania-italiana/">guía de la ley vigente</a> y las <a href="/novedades/">novedades legales</a>.</p>'''

fechas_faq = [
    ("¿Hasta cuándo se puede pedir la ciudadanía italiana en el consulado?",
     "Hasta el 31 de diciembre de 2028 los consulados reciben una cantidad limitada de solicitudes de adultos por año. Desde el 1 de enero de 2029, según la Ley 11/2026, el reconocimiento de adultos que viven en el exterior lo resuelve una oficina central en Roma."),
    ("¿Cuál es la fecha de corte de la Ley 74/2025?",
     "Las 23:59 (hora de Roma) del 27 de marzo de 2025. Las solicitudes, turnos asignados o juicios anteriores siguen con las reglas anteriores."),
    ("¿Hasta cuándo pueden ser italianos mis hijos menores?",
     "Si tu hijo era menor de edad el 24 de mayo de 2025, hasta el 31 de mayo de 2029. Si nació después, tres años desde su nacimiento."),
]
page("fechas-clave-ciudadania-italiana",
     "Fechas clave de la ciudadanía italiana en 2026: plazos y cambios de ley",
     "Fechas clave de la ciudadanía italiana: los plazos que vienen",
     "Calendario de la ciudadanía italiana: el corte del 27 de marzo de 2025, el plazo de hijos menores hasta el 31 de mayo de 2029, la centralización en Roma desde 2029 y los fallos de 2026.",
     "Hay tres fechas que hoy importan: el <strong>27 de marzo de 2025</strong> (corte de la Ley 74/2025), el <strong>31 de diciembre de 2028</strong> (fin de la transición en los consulados) y el <strong>31 de mayo de 2029</strong> (plazo para los hijos que eran menores en mayo de 2025).",
     fechas_art, fechas_faq, [REL_LEY, REL_MEN, REL_FAQ])

# ---------- Preguntas frecuentes ----------
faq_groups = [
    ("Quién puede ser italiano", [
        ("¿Quién puede tener la ciudadanía italiana en 2026?",
         "Desde la Ley 74/2025, quien nació fuera de Italia y tiene otra ciudadanía es reconocido como italiano en casos puntuales. El más común: tener un padre, madre, abuelo o abuela con ciudadanía italiana exclusiva. También quien tiene un padre o madre que vivió dos años seguidos en Italia antes de su nacimiento."),
        ("¿Los bisnietos de italianos pueden tener la ciudadanía?",
         "En principio no, salvo que el caso entre en alguna excepción de la Ley 74/2025 o se haya iniciado antes del 27 de marzo de 2025."),
        ("Mi abuelo nació en Italia, ¿me corresponde?",
         "Depende de si tu abuelo tuvo otra ciudadanía. La ley exige que haya tenido, o tuviera al morir, solamente la italiana."),
        ("¿Qué pasa con los casos iniciados antes de marzo de 2025?",
         "Las solicitudes, turnos asignados o juicios anteriores a las 23:59 (hora de Roma) del 27 de marzo de 2025 siguen con las reglas anteriores."),
        ("¿Se transmite la ciudadanía por línea materna?",
         "Desde el 1 de enero de 1948, sí. Los casos de mujeres que tuvieron hijos antes de esa fecha siempre fueron por vía judicial, y a las demandas nuevas también se les aplica la reforma de 2025."),
    ]),
    ("Fallos y cambios recientes", [
        ("¿La Ley 74/2025 está vigente?",
         "Sí. En abril de 2026 la Corte Constitucional la validó (Sentencia 63/2026) y en julio consultó al Tribunal de Justicia de la UE (Ordenanza 147/2026), pero ninguna de esas decisiones la suspende."),
        ("¿Qué es el “minor issue” y en qué quedó?",
         "Era el criterio por el que se rechazaban casos de antepasados que se naturalizaron cuando su hijo era menor. La Casación lo dejó atrás con la Sentencia 24045/2026 y la circular 65050/2026 permite pedir el reexamen de los rechazos basados solo en ese motivo."),
        ("¿Qué cambia en 2029?",
         "Desde el 1 de enero de 2029, por la Ley 11/2026, el reconocimiento de adultos que viven en el exterior lo resuelve una oficina central en Roma y no cada consulado. No cambia quién tiene derecho."),
    ]),
    ("Hijos menores", [
        ("¿Mis hijos menores son italianos automáticamente?",
         "Ya no. Desde la Ley 74/2025, los hijos menores nacidos en el exterior de un italiano por nacimiento adquieren la ciudadanía por una declaración de voluntad de los padres."),
        ("¿Hasta cuándo hay plazo para los hijos menores?",
         "Si eran menores el 24 de mayo de 2025, hasta el 31 de mayo de 2029. Si nacieron después, tres años desde el nacimiento."),
    ]),
    ("Costos", [
        ("¿Cuánto cuesta el arancel oficial?",
         "600 euros por cada solicitante mayor de edad desde el 1 de enero de 2025. En Argentina se paga en pesos al tipo de cambio consular del trimestre y no se devuelve si la ciudadanía no se reconoce."),
        ("¿La declaración de hijos menores tiene costo?",
         "No. Desde el 1 de enero de 2026 es gratuita: se eliminó la tasa de 250 euros."),
        ("¿Cuánto cobra Zittano?",
         "Depende de cada caso. Después de la consulta te damos un presupuesto claro y los honorarios se pagan por etapas."),
    ]),
]
faq_art = ""
all_faq = []
for titulo, qs in faq_groups:
    faq_art += f"<h2>{html.escape(titulo)}</h2>\n"
    for q, a in qs:
        faq_art += f"<h3 style=\"font-size:1.08rem;color:var(--ink);margin:22px 0 6px\">{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>\n"
        all_faq.append((q, a))
faq_art += '<p>¿No encontraste tu pregunta? Probá el <a href="/test.html">Tanómetro</a>, nuestro test gratis, o escribinos.</p>'

page("preguntas-frecuentes-ciudadania-italiana",
     "Preguntas frecuentes sobre la ciudadanía italiana en 2026",
     "Preguntas frecuentes sobre la ciudadanía italiana",
     "Respuestas cortas y actualizadas: quién puede ser italiano con la Ley 74/2025, bisnietos, línea materna, minor issue, hijos menores, centralización en Roma y aranceles oficiales.",
     "Las preguntas que más recibimos por WhatsApp e Instagram, respondidas en dos o tres líneas y con la norma que corresponde. Actualizado con la Ley 74/2025, la Ley 11/2026 y los fallos de 2026.",
     faq_art, [], [REL_LEY, REL_FEC, REL_ARA])

# La página de preguntas lleva todas sus preguntas en el schema, sin repetir el bloque desplegable.
p = "guias/preguntas-frecuentes-ciudadania-italiana/index.html"
s = open(p, encoding="utf-8").read()
s = s.replace('<section class="faq"><h2>Preguntas frecuentes</h2></section>\n', "")
s = s.replace('"mainEntity": []', '"mainEntity": ' + json.dumps(
    [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in all_faq],
    ensure_ascii=False))
open(p, "w", encoding="utf-8").write(s)
print("ok")
