"""Génère les visuels des 11 publications de lancement Clic'Immo, par réseau."""
import base64, io, pathlib, sys
import qrcode
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(sys.argv[1])          # dossier visuels (contient fonts npm)
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

def font_b64(pkg, name):
    p = next(ROOT.glob(f"fontsource-{pkg}-*/files/{name}"))
    return base64.b64encode(p.read_bytes()).decode()

FONTS = "".join(
    f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(data:font/woff2;base64,{font_b64(pkg, f'{pkg}-latin-{w}-{st}.woff2')}) format('woff2');}}"
    for fam, pkg, w, st in [
        ("Jost", "jost", 400, "normal"), ("Jost", "jost", 500, "normal"), ("Jost", "jost", 600, "normal"),
        ("Cormorant Garamond", "cormorant-garamond", 500, "normal"),
        ("Cormorant Garamond", "cormorant-garamond", 600, "normal"),
        ("Cormorant Garamond", "cormorant-garamond", 500, "italic"),
    ])

def qr_data_uri(url):
    img = qrcode.make(url, border=1, box_size=12)
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# ── Formats par réseau ────────────────────────────────────────────────
FORMATS = {
    "instagram": dict(w=1080, h=1350, u=1.0,  layout="tall"),
    "facebook":  dict(w=1080, h=1080, u=0.86, layout="tall"),
    "linkedin":  dict(w=1200, h=627,  u=0.6,  layout="wide"),
    "google":    dict(w=1200, h=900,  u=0.78, layout="wide"),
}

# ── Composants visuels ────────────────────────────────────────────────
def mountains():
    return """<svg class="mount" viewBox="0 0 600 160" preserveAspectRatio="none">
<path d="M0 160 L0 110 L70 70 L120 95 L210 25 L265 70 L300 52 L370 105 L430 60 L520 110 L600 80 L600 160Z" fill="var(--acc)" opacity=".18"/>
<path d="M0 160 L0 130 L90 100 L160 120 L250 80 L330 118 L420 92 L510 126 L600 110 L600 160Z" fill="var(--acc)" opacity=".32"/>
<path d="M0 148 Q150 136 300 146 T600 140 L600 160 L0 160Z" fill="var(--acc)" opacity=".55"/></svg>"""

def bullets(items):
    return '<ul class="bul">' + "".join(f"<li><span>{a}</span>{b}</li>" for a, b in items) + "</ul>"

def stats(items):
    return '<div class="stats">' + "".join(f'<div class="st"><b>{n}</b><span>{t}</span></div>' for n, t in items) + "</div>"

def two_cols():
    return """<div class="cols">
<div class="col"><div class="ct">Formule<br><b>Accompagnée</b></div><div class="rate">4,17 %<small>TTC</small></div><p>Je m'occupe de tout, de l'estimation à l'acte authentique.</p></div>
<div class="col alt"><div class="ct">Formule<br><b>Autonome</b></div><div class="rate">2,04 %<small>TTC</small></div><p>Vous faites les visites, je sécurise dossier, offres et compromis.<br><em>Minimum 8 500 € TTC</em></p></div>
</div>"""

def tracker():
    steps = [("Mise en ligne", "done"), ("Visites & retours", "done"), ("Offres horodatées", "now"),
             ("Compromis", ""), ("Acte chez le notaire", "")]
    li = "".join(f'<li class="{c}"><i></i><span>{t}</span></li>' for t, c in steps)
    return f'<div class="track"><div class="th">Mon espace vendeur</div><ol>{li}</ol></div>'

def dpe():
    cols = [("A", "#2E8B57"), ("B", "#4FA05A"), ("C", "#9BC15A"), ("D", "#E8D24A"),
            ("E", "#F0A93C"), ("F", "#E46F35"), ("G", "#C9302C")]
    rows = "".join(
        f'<div class="dr{" hi" if l in "FG" else ""}" style="--c:{c};--w:{38 + i * 9}%"><b>{l}</b>{"<em>votre bien ?</em>" if l == "F" else ""}</div>'
        for i, (l, c) in enumerate(cols))
    return f'<div class="dpe">{rows}</div>'

def chips(items):
    return '<div class="chips">' + "".join(f"<span>{c}</span>" for c in items) + "</div>"

def stars():
    return '<div class="stars">★★★★★</div><div class="plat"><span>Immodvisor</span><span>Google</span></div>'

def qr_block():
    return f'<div class="qr"><img src="{qr_data_uri("https://clic-immo.fr")}"><span>Scannez<br>pour estimer<br>votre bien</span></div>'

def quote():
    return '<div class="quote">« On ne vous appelle que<br>si vous l\'avez demandé. »</div>' + bullets([
        ("✓", "Votre accord est enregistré"), ("✓", "Limité dans le temps"), ("✓", "Retirable à tout moment")])

# ── Les 11 publications ───────────────────────────────────────────────
POSTS = [
    dict(n=1, slug="lancement", nets=["facebook", "instagram", "linkedin"], theme="dark",
         kicker="Nouvelle agence · Octobre 2026", title="Clic'Immo<br><em>est lancée</em>",
         sub="Votre agence de proximité à Larringes, sur le Plateau de Gavot.",
         comp=lambda: chips(["Thonon", "Évian", "Plateau de Gavot", "Annemasse"]) + mountains(),
         cta="Estimation gratuite · clic-immo.fr"),
    dict(n=2, slug="confiance", nets=["facebook", "linkedin"], theme="light",
         kicker="Pourquoi Clic'Immo ?", title="Une vente sécurisée<br><em>jusqu'à la signature</em>",
         sub="Le droit immobilier, je le pratique depuis bien avant d'être agent.",
         comp=lambda: stats([("2 ans", "en étude notariale"), ("10 ans", "clerc d'avocat, contentieux immobilier"),
                             ("7 ans", "agent immobilier dans le Chablais")]),
         cta="Agence à Larringes · clic-immo.fr"),
    dict(n=3, slug="formules", nets=["facebook", "instagram"], theme="light",
         kicker="Vendre avec Clic'Immo", title="Deux formules,<br><em>au choix</em>", sub="",
         comp=two_cols,
         foot="Honoraires à la charge du vendeur, calculés sur le prix net vendeur. Barème complet sur clic-immo.fr.",
         cta="Quelle formule vous ressemble ?"),
    dict(n=4, slug="estimation", nets=["facebook", "instagram", "google"], theme="terra",
         kicker="Estimation gratuite et sans engagement", title="Combien vaut<br><em>votre bien aujourd'hui ?</em>",
         sub="3 minutes en ligne. Vous choisissez si et quand je vous rappelle.",
         comp=qr_block, cta="clic-immo.fr · « Estimer mon bien »"),
    dict(n=5, slug="plateforme", nets=["facebook", "linkedin"], theme="light",
         kicker="La plateforme Clic'Immo", title="Suivez votre vente<br><em>comme un colis</em>",
         sub="Visites, retours des acheteurs, offres et documents : tout est visible, en temps réel.",
         comp=tracker, cta="Découvrez-la sur clic-immo.fr"),
    dict(n=6, slug="demarchage", nets=["facebook", "linkedin"], theme="dark",
         kicker="Depuis le 11 août 2026", title="Pas d'appel<br><em>sans votre accord</em>",
         sub="Le démarchage téléphonique sans consentement préalable est désormais interdit.",
         comp=quote, cta="C'est vous qui choisissez le moment · clic-immo.fr"),
    dict(n=7, slug="frontaliers", nets=["facebook", "linkedin", "instagram"], theme="light",
         kicker="Frontaliers", title="Travailler en Suisse,<br><em>vivre côté Léman</em>",
         sub="Acheter en Haute-Savoie quand on est frontalier, c'est courant. À condition d'anticiper :",
         comp=lambda: chips(["Financement", "Délais", "Compromis", "Frais de notaire"]) + mountains(),
         cta="De la recherche à la remise des clés · clic-immo.fr"),
    dict(n=8, slug="ancrage-local", nets=["facebook", "instagram", "google"], theme="terra",
         kicker="Larringes · Plateau de Gavot · Chablais", title="Ici, je connais<br><em>le vrai prix, rue par rue</em>",
         sub="Les hameaux, les écoles, les projets de la commune : une agence de proximité, c'est ça.",
         comp=lambda: '<div class="addr">☕ Passez me voir<br><b>19 route de la Touvière<br>74500 Larringes</b></div>' + mountains(),
         cta="clic-immo.fr"),
    dict(n=9, slug="dpe", nets=["facebook", "linkedin"], theme="light",
         kicker="Conseil vendeurs", title="Classé F ou G<br><em>au DPE ?</em>",
         sub="Il se vend, mais son prix en tient compte. Avant de choisir entre rénover et vendre, connaissez sa valeur actuelle.",
         comp=dpe, cta="Je vous aide à faire le calcul, gratuitement · clic-immo.fr"),
    dict(n=10, slug="avis-clients", nets=["facebook", "instagram", "linkedin"], theme="dark",
         kicker="Merci pour votre confiance", title="Vos avis sont<br><em>ma meilleure carte de visite</em>",
         sub="Nous avons travaillé ensemble ? Laissez votre avis en 1 minute.",
         comp=stars, cta="clic-immo.fr"),
    dict(n=11, slug="recrutement", nets=["linkedin", "facebook"], theme="terra",
         kicker="Clic'Immo s'agrandit", title="On recrute<br><em>des agents référents</em>",
         sub="Secteur Thonon · Bas-Chablais · Annemasse",
         comp=lambda: bullets([("→", "Contacts vendeurs apportés"), ("→", "Appui juridique au quotidien"),
                               ("→", "Outils modernes : visites tracées, offres en ligne"),
                               ("→", "Commission claire et écrite")]),
         cta="Écrivez-moi en message privé"),
]

THEMES = {
    "light": "--bg:#F5EFE6;--bg2:#EAE0D2;--ink:#2E1F2E;--soft:#6B5A6B;--acc:#C4614A;--card:#fff;--line:#DDD3C5",
    "dark":  "--bg:#2E1F2E;--bg2:#4A3350;--ink:#F5EFE6;--soft:#CBBBC6;--acc:#E07A60;--card:#3B293D;--line:#5A4460",
    "terra": "--bg:#C4614A;--bg2:#B0533E;--ink:#FFF8F1;--soft:#FBE3D8;--acc:#2E1F2E;--card:#FFF8F1;--line:#E09A86",
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box;font-variant-numeric:lining-nums}
html,body{width:var(--W);height:var(--H);overflow:hidden}
body{background:var(--bg);color:var(--ink);font-family:'Jost',sans-serif;position:relative;
  font-size:calc(var(--u)*30px);-webkit-font-smoothing:antialiased}
.frame{position:absolute;inset:calc(var(--u)*34px);border:calc(var(--u)*2px) solid var(--line);border-radius:calc(var(--u)*6px)}
.wrap{position:absolute;inset:calc(var(--u)*80px);display:flex;flex-direction:column}
.brand{display:flex;align-items:baseline;gap:calc(var(--u)*14px)}
.logo{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:calc(var(--u)*50px);letter-spacing:.01em}
.logo span{color:var(--acc)}
.loc{font-size:calc(var(--u)*20px);letter-spacing:.18em;text-transform:uppercase;color:var(--soft)}
.kicker{margin-top:calc(var(--u)*56px);font-size:calc(var(--u)*24px);font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--acc)}
.title{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:calc(var(--u)*96px);line-height:1.0;margin-top:calc(var(--u)*18px)}
.title em{font-style:italic;font-weight:500;color:var(--acc)}
.sub{margin-top:calc(var(--u)*26px);font-size:calc(var(--u)*31px);line-height:1.4;color:var(--soft);max-width:30em}
.comp{flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;min-height:0}
.foot{font-size:calc(var(--u)*19px);color:var(--soft);line-height:1.4;margin-bottom:calc(var(--u)*18px)}
.cta{display:flex;justify-content:space-between;align-items:center;border-top:calc(var(--u)*2px) solid var(--line);
  padding-top:calc(var(--u)*24px);font-size:calc(var(--u)*27px);font-weight:500}
.cta .dot{width:calc(var(--u)*16px);height:calc(var(--u)*16px);border-radius:50%;background:var(--acc)}
/* wide */
.wide .wrap{inset:calc(var(--u)*80px) calc(var(--u)*90px)}
.wide .main{flex:1;display:grid;grid-template-columns:1.08fr 1fr;gap:calc(var(--u)*70px);min-height:0}
.wide .txt{display:flex;flex-direction:column;justify-content:center}
.wide .kicker{margin-top:0}
.tall .main{flex:1;display:flex;flex-direction:column;min-height:0}
.tall .comp{padding:calc(var(--u)*40px) 0 calc(var(--u)*30px)}
.wide .title{font-size:calc(var(--u)*84px)}
/* components */
.mount{position:absolute;left:calc(var(--u)*-80px);right:calc(var(--u)*-80px);bottom:calc(var(--u)*22px);height:calc(var(--u)*170px);width:calc(100% + var(--u)*160px)}
.wide .mount{display:none}
.chips{display:flex;flex-wrap:wrap;gap:calc(var(--u)*16px);position:relative;z-index:1}
.chips span{border:calc(var(--u)*2px) solid var(--acc);color:var(--ink);border-radius:999px;padding:calc(var(--u)*14px) calc(var(--u)*30px);font-size:calc(var(--u)*30px);font-weight:500}
.tall .chips{margin-bottom:calc(var(--u)*130px)}
.bul{list-style:none;display:flex;flex-direction:column;gap:calc(var(--u)*22px)}
.bul li{display:flex;gap:calc(var(--u)*20px);font-size:calc(var(--u)*33px);line-height:1.3;align-items:baseline}
.bul li span{color:var(--acc);font-weight:600;flex:none}
.stats{display:flex;flex-direction:column;gap:calc(var(--u)*20px)}
.st{display:flex;align-items:center;gap:calc(var(--u)*30px);background:var(--card);border-radius:calc(var(--u)*14px);padding:calc(var(--u)*24px) calc(var(--u)*34px)}
.st b{font-family:'Cormorant Garamond',serif;font-size:calc(var(--u)*72px);color:var(--acc);font-weight:600;min-width:3.4em;line-height:1}
.st span{font-size:calc(var(--u)*30px);line-height:1.3}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:calc(var(--u)*24px)}
.col{background:var(--card);border-radius:calc(var(--u)*16px);padding:calc(var(--u)*36px) calc(var(--u)*32px)}
.col.alt{background:#2E1F2E;color:#F5EFE6}
.ct{font-size:calc(var(--u)*24px);text-transform:uppercase;letter-spacing:.12em;color:var(--soft);line-height:1.5}
.col.alt .ct{color:#CBBBC6}
.ct b{font-family:'Cormorant Garamond',serif;font-size:calc(var(--u)*46px);text-transform:none;letter-spacing:0;color:inherit;font-weight:600}
.col .ct b{color:#2E1F2E}.col.alt .ct b{color:#F5EFE6}
.rate{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:calc(var(--u)*92px);color:#C4614A;margin:calc(var(--u)*18px) 0 calc(var(--u)*12px);line-height:1}
.col.alt .rate{color:#E07A60}
.rate small{font-family:'Jost';font-size:calc(var(--u)*24px);margin-left:calc(var(--u)*8px);font-weight:500}
.col p{font-size:calc(var(--u)*27px);line-height:1.4}
.col p em{display:block;margin-top:calc(var(--u)*12px);font-style:normal;font-weight:600;color:#E07A60}
.track{background:var(--card);border-radius:calc(var(--u)*18px);padding:calc(var(--u)*36px) calc(var(--u)*40px);box-shadow:0 calc(var(--u)*14px) calc(var(--u)*40px) rgba(46,31,46,.10)}
.th{font-size:calc(var(--u)*22px);letter-spacing:.14em;text-transform:uppercase;color:var(--soft);margin-bottom:calc(var(--u)*22px)}
.track ol{list-style:none;position:relative}
.track li{display:flex;align-items:center;gap:calc(var(--u)*24px);padding:calc(var(--u)*13px) 0;font-size:calc(var(--u)*32px);position:relative;color:var(--soft)}
.track li:not(:last-child)::after{content:"";position:absolute;left:calc(var(--u)*15px);top:calc(50% + var(--u)*18px);height:calc(100% - var(--u)*36px);width:calc(var(--u)*3px);background:var(--line)}
.track i{width:calc(var(--u)*33px);height:calc(var(--u)*33px);border-radius:50%;border:calc(var(--u)*3px) solid var(--line);flex:none;background:var(--card)}
.track li.done{color:var(--ink)}.track li.done i{background:#4A7A59;border-color:#4A7A59}
.track li.done i::after{content:"✓";color:#fff;display:block;text-align:center;font-size:calc(var(--u)*20px);line-height:calc(var(--u)*27px);font-style:normal}
.track li.now{color:var(--ink);font-weight:600}.track li.now i{border-color:var(--acc);box-shadow:inset 0 0 0 calc(var(--u)*6px) var(--card);background:var(--acc)}
.dpe{display:flex;flex-direction:column;gap:calc(var(--u)*10px)}
.dr{width:var(--w);background:var(--c);color:#fff;height:calc(var(--u)*62px);display:flex;align-items:center;justify-content:space-between;
  padding:0 calc(var(--u)*24px);clip-path:polygon(0 0,calc(100% - var(--u)*30px) 0,100% 50%,calc(100% - var(--u)*30px) 100%,0 100%);opacity:.45}
.dr b{font-size:calc(var(--u)*36px);font-weight:600}
.dr.hi{opacity:1;height:calc(var(--u)*76px)}
.dr em{font-style:normal;font-size:calc(var(--u)*24px);font-weight:500;margin-right:calc(var(--u)*30px)}
.qr{display:flex;align-items:center;gap:calc(var(--u)*40px)}
.qr img{width:calc(var(--u)*300px);height:calc(var(--u)*300px);background:#fff;padding:calc(var(--u)*16px);border-radius:calc(var(--u)*16px)}
.qr span{font-family:'Cormorant Garamond',serif;font-size:calc(var(--u)*50px);line-height:1.1;font-weight:500;font-style:italic}
.quote{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:calc(var(--u)*50px);line-height:1.15;margin-bottom:calc(var(--u)*34px);color:var(--ink)}
.addr{font-size:calc(var(--u)*32px);line-height:1.45;position:relative;z-index:1}
.addr b{font-family:'Cormorant Garamond',serif;font-size:calc(var(--u)*50px);font-weight:600;line-height:1.1;display:block;margin-top:calc(var(--u)*10px)}
.tall .addr{margin-bottom:calc(var(--u)*120px)}
.stars{font-size:calc(var(--u)*92px);color:var(--acc);letter-spacing:.08em;line-height:1}
.plat{display:flex;gap:calc(var(--u)*16px);margin-top:calc(var(--u)*30px)}
.plat span{background:var(--card);border-radius:999px;padding:calc(var(--u)*14px) calc(var(--u)*32px);font-size:calc(var(--u)*30px);font-weight:500}
"""

def page(post, fmt):
    f = FORMATS[fmt]
    head = '<div class="brand"><div class="logo">Clic<span>\'</span>Immo</div><div class="loc">Larringes · Chablais</div></div>'
    txt = f'<div class="kicker">{post["kicker"]}</div><div class="title">{post["title"]}</div>' + (
        f'<div class="sub">{post["sub"]}</div>' if post["sub"] else "")
    comp = f'<div class="comp">{post["comp"]()}</div>'
    main = (f'<div class="main"><div class="txt">{txt}</div>{comp}</div>' if f["layout"] == "wide"
            else f'<div class="main">{txt}{comp}</div>')
    foot = f'<div class="foot">{post["foot"]}</div>' if post.get("foot") else ""
    cta = f'<div class="cta"><span>{post["cta"]}</span><span class="dot"></span></div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
:root{{--W:{f['w']}px;--H:{f['h']}px;--u:{f['u']};{THEMES[post['theme']]}}}{CSS}</style></head>
<body class="{f['layout']}"><div class="frame"></div><div class="wrap">{head}{main}{foot}{cta}</div></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    for post in POSTS:
        for net in post["nets"]:
            f = FORMATS[net]
            pg = b.new_page(viewport={"width": f["w"], "height": f["h"]})
            pg.set_content(page(post, net)); pg.wait_for_timeout(150)
            # alerte si le contenu déborde
            over = pg.evaluate("""() => { const m=document.querySelector('.main'); return m.scrollHeight - m.clientHeight }""")
            name = f"{post['n']:02d}_{post['slug']}_{net}.png"
            pg.screenshot(path=str(OUT / name)); pg.close()
            print(name, f"{f['w']}x{f['h']}", "DEBORDE %dpx" % over if over > 2 else "ok")
    b.close()

# ── PDF modifiables pour Canva : un PDF par réseau, une page par publication ──
if len(sys.argv) > 3:
    from pypdf import PdfWriter
    PDF = pathlib.Path(sys.argv[3]); PDF.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for net, f in FORMATS.items():
            w = PdfWriter(); tmp = []
            for post in POSTS:
                if net not in post["nets"]:
                    continue
                pg = b.new_page(viewport={"width": f["w"], "height": f["h"]})
                pg.set_content(page(post, net)); pg.wait_for_timeout(150)
                t = PDF / f"_tmp_{post['n']:02d}.pdf"
                pg.pdf(path=str(t), width=f"{f['w']}px", height=f"{f['h']}px", print_background=True,
                       margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, page_ranges="1")
                pg.close(); w.append(str(t)); tmp.append(t)
            w.write(str(PDF / f"ClicImmo_lancement_{net}.pdf"))
            for t in tmp: t.unlink()
            print(net, len(tmp), "pages")
        b.close()
