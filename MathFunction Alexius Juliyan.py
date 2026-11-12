"""MathFunction - Media pembelajaran interaktif Fungsi Kuadrat (SMA Kelas X, Fase E)
Modul Ajar: Alexius Juliyan Budiuntoro | Model PBL | 2 Pertemuan
Jalankan:  streamlit run app.py
"""
import math
import random
from fractions import Fraction

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="MathFunction - Fungsi Kuadrat", page_icon="📈", layout="wide")
S = st.session_state

# ───────────────────────── Tampilan ─────────────────────────
st.markdown("""
<style>
.hero{background:linear-gradient(120deg,#4f46e5,#06b6d4);color:#fff;padding:26px 30px;border-radius:18px;margin-bottom:18px}
.hero h1{margin:0;font-size:2.1rem;color:#fff}.hero p{margin:6px 0 0;opacity:.95;font-size:1.05rem}
.card{background:#f5f7ff;border-left:6px solid #4f46e5;padding:14px 18px;border-radius:12px;margin:10px 0;color:#1e1b4b}
.card.g{background:#ecfdf5;border-color:#10b981;color:#064e3b}
.card.o{background:#fff7ed;border-color:#f97316;color:#7c2d12}
.badge{display:inline-block;background:#4f46e5;color:#fff;padding:3px 12px;border-radius:20px;font-size:.85rem;margin:2px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#eef2ff,#ecfeff)}
</style>""", unsafe_allow_html=True)


_PN = [0]


def plot(fig):
    """Plotly dengan key unik otomatis (hindari duplikat ID)."""
    _PN[0] += 1
    st.plotly_chart(fig, key=f"plot{_PN[0]}")


def card(txt, kind=""):
    st.markdown(f'<div class="card {kind}">{txt}</div>', unsafe_allow_html=True)


# ───────────────────────── Util matematika ─────────────────────────
def Fr(x):
    return Fraction(str(x)).limit_denominator(1000)


def L(x):
    """Pecahan -> LaTeX."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{'-' if x < 0 else ''}\\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def expr(pairs):
    """[(koef,'x^2'),(koef,'x'),(koef,'')] -> string LaTeX polinom."""
    s = ""
    for v, k in pairs:
        v = Fraction(v)
        if v == 0:
            continue
        m = abs(v)
        body = (L(m) if (m != 1 or k == "") else "") + k
        s += (("-" if v < 0 else "") + body) if not s else (f" {'-' if v < 0 else '+'} {body}")
    return s or "0"


def poly(a, b, c):
    return expr([(a, "x^2"), (b, "x"), (c, "")])


def coef(a):
    a = Fraction(a)
    return "" if a == 1 else ("-" if a == -1 else L(a))


def xm(r, var="x"):
    r = Fraction(r)
    return var if r == 0 else (f"({var}-{L(r)})" if r > 0 else f"({var}+{L(-r)})")


def fsqrt(x):
    x = Fraction(x)
    if x < 0:
        return None
    n, d = math.isqrt(x.numerator), math.isqrt(x.denominator)
    return Fraction(n, d) if n * n == x.numerator and d * d == x.denominator else None


def three_forms(a, b, c):
    """Tiga bentuk fungsi kuadrat (LaTeX)."""
    a, b, c = Fr(a), Fr(b), Fr(c)
    D = b * b - 4 * a * c
    p = -b / (2 * a)
    q = a * p * p + b * p + c
    std = f"f(x)={poly(a, b, c)}"
    vt = f"f(x)={coef(a)}{xm(p)}^2" + (f" {'+' if q > 0 else '-'} {L(abs(q))}" if q != 0 else "")
    if D < 0:
        fk = "\\text{tidak ada (D<0, tidak punya akar real)}"
    else:
        r = fsqrt(D)
        if r is not None:
            fk = f"f(x)={coef(a)}{xm((-b - r) / (2 * a))}{xm((-b + r) / (2 * a))}"
        else:
            s = math.sqrt(D)
            fk = f"f(x)={coef(a)}(x-({(-b - s) / (2 * a):.3f}))(x-({(-b + s) / (2 * a):.3f}))"
    return std, vt, fk


def parabola_fig(a, b, c, pts=None, height=420, title=None):
    a, b, c = float(a), float(b), float(c)
    xs0 = -b / (2 * a)
    q = a * xs0 ** 2 + b * xs0 + c
    D = b * b - 4 * a * c
    half = max(6.0, (math.sqrt(D) / (2 * abs(a)) + 3)) if D > 0 else 6.0
    lo, hi = min(xs0 - half, -1), max(xs0 + half, 1)
    if pts:
        lo, hi = min(lo, min(p[0] for p in pts) - 1), max(hi, max(p[0] for p in pts) + 1)
    x = np.linspace(lo, hi, 500)
    y = a * x ** 2 + b * x + c
    if a > 0:
        ylo = min(q, 0) - 2
        yhi = max(ylo + 10, min(y.max(), max(q, 0) + 25))
    else:
        yhi = max(q, 0) + 2
        ylo = min(yhi - 10, max(y.min(), min(q, 0) - 25))
    if pts:
        ylo, yhi = min(ylo, min(p[1] for p in pts) - 1), max(yhi, max(p[1] for p in pts) + 1)
    f = go.Figure()
    f.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Parabola", line=dict(color="#4f46e5", width=4)))
    f.add_trace(go.Scatter(x=[xs0, xs0], y=[ylo, yhi], mode="lines", name="Sumbu simetri",
                           line=dict(color="#94a3b8", dash="dash")))
    f.add_trace(go.Scatter(x=[xs0], y=[q], mode="markers+text", name="Titik puncak",
                           text=[f"({xs0:.2f}; {q:.2f})"], textposition="top center",
                           marker=dict(size=13, color="#ef4444")))
    f.add_trace(go.Scatter(x=[0], y=[c], mode="markers", name="Potong sumbu y",
                           marker=dict(size=11, color="#10b981", symbol="diamond")))
    if D >= 0:
        rs = sorted({(-b - math.sqrt(D)) / (2 * a), (-b + math.sqrt(D)) / (2 * a)})
        f.add_trace(go.Scatter(x=rs, y=[0] * len(rs), mode="markers", name="Potong sumbu x",
                               marker=dict(size=11, color="#f97316", symbol="square")))
    if pts:
        f.add_trace(go.Scatter(x=[p[0] for p in pts], y=[p[1] for p in pts], mode="markers+text",
                               text=[f"({p[0]:g}, {p[1]:g})" for p in pts], textposition="bottom right",
                               name="Titik diketahui", marker=dict(size=12, color="#0ea5e9", symbol="star")))
    f.update_layout(template="plotly_white", height=height, margin=dict(l=10, r=10, t=40 if title else 10, b=10),
                    title=title, legend=dict(orientation="h", y=-0.15), yaxis=dict(range=[ylo, yhi]),
                    xaxis=dict(range=[lo, hi]))
    return f


def steps(a, b, c):
    """Pembahasan langkah demi langkah (markdown + LaTeX)."""
    a, b, c = Fr(a), Fr(b), Fr(c)
    D = b * b - 4 * a * c
    xs = -b / (2 * a)
    ys = a * xs * xs + b * xs + c
    s = [f"**Langkah 1 - Arah bukaan.** Dari $f(x)={poly(a, b, c)}$ diperoleh $a={L(a)},\\ b={L(b)},\\ c={L(c)}$. "
         f"Karena $a{'>' if a > 0 else '<'}0$, grafik terbuka ke **{'atas' if a > 0 else 'bawah'}**, sehingga titik puncak "
         f"adalah titik **{'minimum' if a > 0 else 'maksimum'}**.",
         f"**Langkah 2 - Titik potong sumbu y.** Substitusi $x=0$: $f(0)=c={L(c)}$ → titik $(0,{L(c)})$.",
         f"**Langkah 3 - Diskriminan.** $D=b^2-4ac=({L(b)})^2-4({L(a)})({L(c)})={L(D)}$."]
    if D > 0:
        r = fsqrt(D)
        if r is not None:
            x1, x2 = sorted([(-b - r) / (2 * a), (-b + r) / (2 * a)])
            t = (f"Karena $D>0$ ada **dua** titik potong. $x_{{1,2}}=\\frac{{-b\\pm\\sqrt{{D}}}}{{2a}}"
                 f"=\\frac{{{L(-b)}\\pm {L(r)}}}{{{L(2 * a)}}}$ → $x_1={L(x1)}$ dan $x_2={L(x2)}$. "
                 f"Titik: $({L(x1)},0)$ dan $({L(x2)},0)$.")
        else:
            x1, x2 = sorted([(-float(b) - math.sqrt(D)) / (2 * float(a)), (-float(b) + math.sqrt(D)) / (2 * float(a))])
            t = f"Karena $D>0$ ada **dua** titik potong, $x_1\\approx{x1:.3f}$ dan $x_2\\approx{x2:.3f}$ (akar tidak rasional)."
    elif D == 0:
        t = f"Karena $D=0$ ada **satu** titik potong (grafik menyinggung sumbu x) di $({L(xs)},0)$."
    else:
        t = "Karena $D<0$ **tidak ada** titik potong dengan sumbu x (parabola tidak memotong sumbu x)."
    s.append("**Langkah 4 - Titik potong sumbu x.** " + t)
    s.append(f"**Langkah 5 - Sumbu simetri.** $x=-\\frac{{b}}{{2a}}=-\\frac{{{L(b)}}}{{2({L(a)})}}={L(xs)}$.")
    s.append(f"**Langkah 6 - Titik puncak.** $x_p={L(xs)}$, lalu $y_p=f({L(xs)})={L(ys)}$ "
             f"(cek: $y_p=-\\frac{{D}}{{4a}}={L(-D / (4 * a))}$). Titik puncak $({L(xs)},{L(ys)})$.")
    s.append(f"**Kesimpulan.** Nilai **{'minimum' if a > 0 else 'maksimum'}** fungsi adalah ${L(ys)}$ dicapai saat $x={L(xs)}$.")
    return s


def show_steps(a, b, c):
    for t in steps(a, b, c):
        st.markdown(t)
    std, vt, fk = three_forms(a, b, c)
    st.markdown("**Tiga bentuk fungsi:**")
    st.latex(std); st.latex(vt); st.latex(fk)


# ───────────────────────── Progres ─────────────────────────
S.setdefault("prog", {})
S.setdefault("refl", {})
ITEMS = {"diag": "Asesmen diagnostik", "p1_eks": "P1 - Eksplorasi grafik", "p1_lkpd": "P1 - LKPD 1",
         "p1_exit": "P1 - Kartu keluar", "p2_kuis": "P2 - Kuis apersepsi", "p2_kons": "P2 - Konstruksi fungsi",
         "p2_lkpd": "P2 - LKPD 2", "p2_exit": "P2 - Kartu keluar", "game1": "Game Tembak Bola Basket",
         "game2": "Game Kuis Kilat", "refleksi": "Refleksi siswa"}


def mark(key, score=100):
    S.prog[key] = max(S.prog.get(key, 0), score)


def pct():
    return int(sum(1 for k in ITEMS if S.prog.get(k, 0) > 0) / len(ITEMS) * 100)


def xp():
    return int(sum(S.prog.values()))


# ───────────────────────── Komponen kuis ─────────────────────────
def quiz(key, qs):
    """Kuis pilihan ganda dinilai otomatis. qs: [{q,o,a(index),e}]"""
    with st.form(key):
        ans = [st.radio(f"**{i + 1}.** {q['q']}", q["o"], index=None, key=f"{key}_{i}") for i, q in enumerate(qs)]
        ok = st.form_submit_button("✅ Kirim jawaban")
    if ok:
        if any(a is None for a in ans):
            st.warning("Jawab semua soal dulu ya.")
            return
        good = sum(1 for q, a in zip(qs, ans) if a == q["o"][q["a"]])
        sc = round(100 * good / len(qs))
        mark(key, sc)
        (st.success if sc >= 75 else st.warning)(f"Skor: **{sc}** ({good}/{len(qs)} benar)")
        for i, (q, a) in enumerate(zip(qs, ans)):
            with st.expander(f"{'✅' if a == q['o'][q['a']] else '❌'} Pembahasan soal {i + 1}"):
                st.markdown(f"Jawaban benar: **{q['o'][q['a']]}**\n\n{q['e']}")
        if sc == 100:
            st.balloons()


def check_form(key, items, per_row=4):
    """Isian bernilai otomatis. items: [{t, f:[(label, jawaban, opsi|None)], e}]"""
    with st.form(key):
        vals = []
        for i, it in enumerate(items):
            st.markdown(it["t"])
            row = []
            for j, (lab, ans, opt) in enumerate(it["f"]):
                if j % per_row == 0:
                    cols = st.columns(per_row)
                w = cols[j % per_row]
                row.append(w.selectbox(lab, ["-"] + opt, key=f"{key}{i}{j}") if opt
                           else w.number_input(lab, value=None, step=0.01, format="%g", key=f"{key}{i}{j}"))
            vals.append(row)
        ok = st.form_submit_button("✅ Periksa jawaban")
    if ok:
        tot = good = 0
        for i, (it, row) in enumerate(zip(items, vals)):
            res = []
            for (lab, ans, opt), v in zip(it["f"], row):
                c = (v == ans) if opt else (v is not None and abs(v - ans) < 0.02)
                res.append(c); tot += 1; good += c
            with st.expander(f"{'✅' if all(res) else '❌'} Soal {i + 1}: {sum(res)}/{len(res)} isian benar"):
                st.markdown(it["e"])
        sc = round(100 * good / tot)
        mark(key, sc)
        st.progress(sc / 100, text=f"Skor {sc} ({good}/{tot})")
        (st.success if sc >= 75 else st.info)("Mantap! Tujuan tercapai 🎉" if sc >= 75 else
                                               "Belum tercapai. Buka pembahasan lalu coba lagi.")
        if sc == 100:
            st.balloons()


# ───────────────────────── Bank soal ─────────────────────────
DIAG = [
    dict(q="Faktorkan $x^2-5x+6$.", o=["$(x-2)(x-3)$", "$(x+2)(x+3)$", "$(x-1)(x-6)$", "$(x+2)(x-3)$"], a=0,
         e="Cari dua bilangan hasil kali 6 dan jumlah −5 → −2 dan −3."),
    dict(q="Diskriminan dan jenis akar $2x^2-3x+5=0$ adalah ...",
         o=["$D=49$, dua akar real berbeda", "$D=-31$, tidak ada akar real", "$D=0$, dua akar real kembar",
            "$D=31$, dua akar real berbeda"], a=1, e="$D=(-3)^2-4(2)(5)=9-40=-31<0$ → tidak ada akar real."),
    dict(q="Jika $f(x)=2x-1$, maka $f(3)=$ ...", o=["6", "7", "5", "3"], a=2, e="$f(3)=2(3)-1=5$."),
    dict(q="Selesaikan $a+b=5$ dan $a-b=1$. Nilai $a$ dan $b$ adalah ...",
         o=["$a=2,\\ b=3$", "$a=3,\\ b=2$", "$a=4,\\ b=1$", "$a=5,\\ b=0$"], a=1,
         e="Jumlahkan: $2a=6\\Rightarrow a=3$, maka $b=2$."),
]
KUIS_P2 = [
    dict(q="Grafik $f(x)=-2x^2+4x+1$ terbuka ke ...", o=["atas", "bawah", "kanan", "kiri"], a=1,
         e="$a=-2<0$ sehingga terbuka ke bawah."),
    dict(q="Banyak titik potong $f(x)=x^2-6x+9$ dengan sumbu x adalah ...", o=["0", "1", "2", "3"], a=1,
         e="$D=36-36=0$ → satu titik potong (menyinggung)."),
    dict(q="Persamaan sumbu simetri $f(x)=x^2+8x+3$ adalah ...", o=["$x=4$", "$x=-4$", "$x=8$", "$x=-8$"], a=1,
         e="$x=-\\frac{b}{2a}=-\\frac{8}{2}=-4$."),
]
ARAH = ["Atas", "Bawah"]


def lkpd1_items():
    out = []
    for n, (a, b, c) in zip("fghk", [(1, -4, 3), (-1, 2, 3), (1, -4, 4), (1, 2, 5)]):
        A, B, C = Fr(a), Fr(b), Fr(c)
        D = B * B - 4 * A * C
        xs = -B / (2 * A)
        ys = A * xs * xs + B * xs + C
        out.append(dict(
            t=f"**Fungsi** ${n}(x)={poly(A, B, C)}$",
            f=[("Arah bukaan", "Atas" if a > 0 else "Bawah", ARAH), ("Titik potong y (0, ...)", float(C), None),
               ("Diskriminan D", float(D), None),
               ("Banyak titik potong sumbu x", "2" if D > 0 else ("1" if D == 0 else "0"), ["0", "1", "2"]),
               ("Sumbu simetri x =", float(xs), None), ("Titik puncak: x", float(xs), None),
               ("Titik puncak: y", float(ys), None)],
            e="\n\n".join(steps(a, b, c))))
    return out


EXIT1 = [dict(t="**Kartu keluar P1:** untuk $f(x)=x^2-6x+5$ tentukan:",
              f=[("Arah bukaan", "Atas", ARAH), ("Potong sumbu y (0, ...)", 5, None),
                 ("Potong sumbu x (terkecil)", 1, None), ("Potong sumbu x (terbesar)", 5, None),
                 ("Sumbu simetri x =", 3, None), ("Puncak: x", 3, None), ("Puncak: y", -4, None)],
              e="\n\n".join(steps(1, -6, 5)))]

LKPD2 = [
    dict(t="**1.** Fungsi kuadrat bentuk standar $f(x)=ax^2+bx+c$ melalui $P(0,5),\\ Q(1,2),\\ R(2,1)$.",
         f=[("a", 1, None), ("b", -4, None), ("c", 5, None)],
         e="$c=5$; $a+b+5=2\\Rightarrow a+b=-3$; $4a+2b+5=1\\Rightarrow 2a+b=-2$ → $a=1,\\ b=-4$. $f(x)=x^2-4x+5$."),
    dict(t="**2.** Grafik memotong sumbu x di $(-2,0)$ dan $(4,0)$ serta melalui $(0,-8)$. Tulis bentuk **standar**.",
         f=[("a", 1, None), ("b", -2, None), ("c", -8, None)],
         e="$f(x)=a(x+2)(x-4)$; $f(0)=-8a=-8\\Rightarrow a=1$. $f(x)=(x+2)(x-4)=x^2-2x-8$."),
    dict(t="**3.** Titik puncak $(3,-2)$ dan melalui $(1,6)$. Tulis bentuk **standar**.",
         f=[("a", 2, None), ("b", -12, None), ("c", 16, None)],
         e="$f(x)=a(x-3)^2-2$; $f(1)=4a-2=6\\Rightarrow a=2$. $f(x)=2(x-3)^2-2=2x^2-12x+16=2(x-2)(x-4)$."),
    dict(t="**4.** Bola dilempar dari ketinggian 2 m, mencapai tinggi maksimum 6 m pada $t=2$ detik. "
           "Tentukan $h(t)=at^2+bt+c$ dan waktu bola menyentuh tanah.",
         f=[("a", -1, None), ("b", 4, None), ("c", 2, None), ("Waktu mendarat (detik)", 4.45, None)],
         e="$h(t)=a(t-2)^2+6$; $h(0)=4a+6=2\\Rightarrow a=-1$. $h(t)=-t^2+4t+2$. $h=0\\Rightarrow (t-2)^2=6\\Rightarrow t=2+\\sqrt6\\approx4{,}45$ detik."),
    dict(t="**5. Tantangan:** mengapa bentuk faktor tidak dapat dipakai jika $D<0$?",
         f=[("Pilih jawaban", "Tidak ada akar real, grafik tidak memotong sumbu x",
             ["Grafik menjadi garis lurus", "Tidak ada akar real, grafik tidak memotong sumbu x", "Karena a = 0"])],
         e="Bentuk faktor memerlukan titik potong sumbu x ($x_1,x_2$ real). Jika $D<0$ akarnya tidak real."),
]
EXIT2 = [dict(t="**Kartu keluar P2:** fungsi kuadrat memotong sumbu x di $(1,0)$ dan $(3,0)$ serta melalui $(0,6)$. "
                "Tulis bentuk standar.",
              f=[("a", 2, None), ("b", -8, None), ("c", 6, None)],
              e="$f(x)=a(x-1)(x-3)$; $f(0)=3a=6\\Rightarrow a=2$. $f(x)=2(x-1)(x-3)=2x^2-8x+6$.")]


# ───────────────────────── Halaman ─────────────────────────
def hero(t, sub):
    st.markdown(f'<div class="hero"><h1>{t}</h1><p>{sub}</p></div>', unsafe_allow_html=True)


def goto(p):
    S.nav = p


def page_home():
    hero("📈 MathFunction", "Media pembelajaran interaktif · Persamaan &amp; Fungsi Kuadrat · Matematika Wajib Kelas X (Fase E)")
    c1, c2 = st.columns([3, 2])
    with c1:
        card("<b>Pertanyaan pemantik:</b> Mengapa lintasan bola basket berbentuk lengkungan, dan di titik mana bola "
             "mencapai tempat tertinggi? Bagaimana menemukan persamaan fungsinya hanya dari tiga titik?")
        st.markdown("### 🎯 Tujuan pembelajaran")
        st.markdown("""
**Pertemuan 1 - Karakteristik fungsi kuadrat**
- Menentukan arah bukaan grafik serta peran koefisien $a$ dan titik potong sumbu y $(0,c)$.
- Menentukan banyak titik potong sumbu x berdasarkan diskriminan $D=b^2-4ac$.
- Menentukan sumbu simetri dan titik puncak (maksimum/minimum).

**Pertemuan 2 - Mengonstruksi fungsi kuadrat**
- Menyusun fungsi bentuk standar dari **tiga titik** (substitusi + SPL).
- Menyusun bentuk faktor dari **titik potong sumbu x** dan satu titik lain.
- Menyusun bentuk titik puncak dari **titik puncak** dan satu titik lain, lalu mengubah antarbentuk.
""")
        st.markdown("### 🧭 Alur Problem Based Learning (PBL)")
        st.table(pd.DataFrame({
            "Fase PBL": ["Orientasi pada masalah", "Mengorganisasi murid", "Membimbing penyelidikan",
                         "Mengembangkan & menyajikan hasil", "Menganalisis & mengevaluasi proses"],
            "Di aplikasi": ["Tab Orientasi (gambar & pemantik)", "Tab LKPD / petunjuk", "Eksplorasi interaktif & konstruktor",
                            "Isian LKPD dinilai otomatis", "Pembahasan langkah & kartu keluar"]}))
    with c2:
        st.markdown("### 🚀 Mulai belajar")
        st.button("🩺 Mulai dari Asesmen Diagnostik", on_click=goto, args=(NAV[1],))
        st.button("📘 Pertemuan 1", on_click=goto, args=(NAV[2],))
        st.button("📗 Pertemuan 2", on_click=goto, args=(NAV[3],))
        st.button("🎮 Main Game", on_click=goto, args=(NAV[5],))
        st.metric("Progres belajar", f"{pct()}%")
        st.progress(pct() / 100)
        card("Tips: kerjakan di buku berpetak lebih dulu, lalu <b>periksa dengan aplikasi ini</b> (seperti memeriksa dengan GeoGebra).", "g")


def page_diag():
    hero("🩺 Asesmen Diagnostik", "Pertemuan 1 · ± 10 menit · 4 soal prasyarat")
    card("Hasilnya dipakai untuk melihat bagian prasyarat yang perlu diperkuat: memfaktorkan, diskriminan, fungsi linear, dan SPLDV.")
    quiz("diag", DIAG)
    if S.prog.get("diag", 0) and S.prog["diag"] < 75:
        card("Skor di bawah 75: ulangi materi prasyarat (memfaktorkan, diskriminan, SPLDV) sebelum lanjut.", "o")


def explorer():
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("**Geser nilai koefisien:**")
        a = st.slider("a", -5.0, 5.0, 1.0, 0.5, key="ea")
        b = st.slider("b", -10.0, 10.0, -4.0, 0.5, key="eb")
        c = st.slider("c", -10.0, 10.0, 3.0, 0.5, key="ec")
        show_tab = st.checkbox("Tampilkan tabel nilai (x = -3 … 5)")
    if a == 0:
        c2.error("⚠️ a = 0 → fungsi menjadi **linear** (garis lurus), bukan fungsi kuadrat. Itulah mengapa $a\\neq0$.")
        return
    mark("p1_eks")
    A, B, C = Fr(a), Fr(b), Fr(c)
    D = B * B - 4 * A * C
    with c2:
        st.latex(f"f(x)={poly(A, B, C)}")
        plot(parabola_fig(a, b, c))
    m = st.columns(4)
    m[0].metric("Arah bukaan", "Atas ⬆️" if a > 0 else "Bawah ⬇️")
    m[1].metric("Potong sumbu y", f"(0, {c:g})")
    m[2].metric("D = b²−4ac", f"{float(D):g}", "2 titik potong x" if D > 0 else ("1 titik (menyinggung)" if D == 0 else "tidak ada titik potong x"))
    xs = -B / (2 * A)
    m[3].metric("Titik puncak", f"({float(xs):.2f}; {float(A * xs * xs + B * xs + C):.2f})")
    if show_tab:
        xv = list(range(-3, 6))
        st.dataframe(pd.DataFrame({"x": xv, "f(x)": [float(A * i * i + B * i + C) for i in xv]}).set_index("x").T)
    with st.expander("💡 Pertanyaan penuntun"):
        st.markdown("- Apa yang terjadi pada grafik jika tanda $a$ berubah?\n- Bagaimana hubungan $D$ dengan banyaknya titik potong sumbu x?\n"
                    "- Ubah $c$: titik mana yang ikut bergeser?\n- Ubah $b$: bagaimana letak sumbu simetri berubah?")


def page_p1():
    hero("📘 Pertemuan 1: Karakteristik Fungsi Kuadrat", "TP 1 · 2 JP (90 menit) · Problem Based Learning")
    t = st.tabs(["1️⃣ Orientasi", "2️⃣ Eksplorasi", "3️⃣ LKPD 1", "4️⃣ Pembahasan", "5️⃣ Kartu Keluar", "📖 Ringkasan"])
    with t[0]:
        st.markdown("#### Masalah: lintasan bola basket")
        plot(parabola_fig(-0.25, 2, 2, title="Lintasan bola basket (ilustrasi)"))
        card("<b>Masalah:</b> Apa saja ciri lengkungan tersebut dan bagaimana ciri itu dinyatakan secara matematis?")
        st.markdown("**Pertanyaan pemantik:** Mengapa lintasan bola berbentuk lengkungan? Apa perbedaan grafik fungsi linear dan kuadrat?")
        card("<b>Mengorganisasi:</b> siapkan buku garis berpetak, penggaris, pensil warna. Lanjut ke tab <b>Eksplorasi</b>.", "g")
    with t[1]:
        explorer()
    with t[2]:
        st.markdown("Lengkapi tabel karakteristik tiap fungsi (hitung dulu di buku, lalu isi). Boleh pakai desimal bila perlu.")
        check_form("p1_lkpd", lkpd1_items())
        with st.expander("Pertanyaan refleksi LKPD 1"):
            st.markdown("1. Hubungan tanda $a$ dan arah bukaan?\n2. Hubungan $c$ dan titik potong sumbu y?\n3. Hubungan $D$ dan titik potong sumbu x?\n"
                        "4. Cara menentukan sumbu simetri dan titik puncak tanpa menggambar?\n5. Mengapa $a\\neq0$?")
    with t[3]:
        st.markdown("#### Pembahasan langkah demi langkah")
        mode = st.radio("Pilih", ["Contoh dari LKPD", "Fungsi saya sendiri"], horizontal=True, key="p1m")
        if mode == "Contoh dari LKPD":
            n = st.selectbox("Fungsi", ["f(x)=x²−4x+3", "g(x)=−x²+2x+3", "h(x)=x²−4x+4", "k(x)=x²+2x+5"])
            abc = {"f": (1, -4, 3), "g": (-1, 2, 3), "h": (1, -4, 4), "k": (1, 2, 5)}[n[0]]
        else:
            q = st.columns(3)
            abc = (q[0].number_input("a", value=1.0, step=0.5, key="s1a"), q[1].number_input("b", value=-2.0, step=0.5, key="s1b"),
                   q[2].number_input("c", value=-3.0, step=0.5, key="s1c"))
        if abc[0] == 0:
            st.error("a tidak boleh 0.")
        else:
            show_steps(*abc)
            plot(parabola_fig(*abc))
    with t[4]:
        check_form("p1_exit", EXIT1)
    with t[5]:
        summary1()


def summary1():
    st.markdown("""
**Bentuk umum:** $f(x)=ax^2+bx+c,\\ a\\neq0$ · grafik berbentuk **parabola**.
- $a>0$ terbuka ke atas (puncak = **minimum**); $a<0$ terbuka ke bawah (puncak = **maksimum**).
- Titik potong sumbu y: $(0,c)$.
- Titik potong sumbu x dari $ax^2+bx+c=0$: $D>0$ dua titik, $D=0$ satu titik (menyinggung), $D<0$ tidak ada.
- Sumbu simetri: $x=-\\frac{b}{2a}$. Titik puncak: $\\left(-\\frac{b}{2a},\\ f\\left(-\\frac{b}{2a}\\right)\\right)$.
""")


def page_p2():
    hero("📗 Pertemuan 2: Mengonstruksi Fungsi Kuadrat", "TP 2 · 2 JP (90 menit) · Problem Based Learning")
    t = st.tabs(["0️⃣ Kuis Apersepsi", "1️⃣ Orientasi", "2️⃣ Konstruktor", "3️⃣ LKPD 2", "4️⃣ Kartu Keluar", "📖 Ringkasan"])
    with t[0]:
        st.markdown("Kuis digital 3 soal tentang ciri grafik fungsi kuadrat (apersepsi).")
        quiz("p2_kuis", KUIS_P2)
    with t[1]:
        st.markdown("#### Masalah: busur panah")
        plot(parabola_fig(1, -2, -3, pts=[(-1, 0), (0, -3), (1, -4)], title="Tiga titik pada lengkungan"))
        card("<b>Masalah:</b> Tiga titik pada lengkungan diketahui. Bagaimana menemukan persamaan fungsi kuadratnya? "
             "Bagaimana jika yang diketahui titik puncak atau titik potong dengan sumbu x?")
        st.markdown("**Pertanyaan pemantik:** Jika hanya tiga titik pada lengkungan, dapatkah kita menemukan persamaannya?")
    with t[2]:
        constructor()
    with t[3]:
        check_form("p2_lkpd", LKPD2)
    with t[4]:
        check_form("p2_exit", EXIT2)
    with t[5]:
        st.markdown("""
**Tiga bentuk fungsi kuadrat**

| Bentuk | Rumus | Dipakai jika diketahui |
|---|---|---|
| Standar | $f(x)=ax^2+bx+c$ | tiga titik sembarang |
| Faktor | $f(x)=a(x-x_1)(x-x_2)$ | titik potong sumbu x + satu titik lain |
| Titik puncak | $f(x)=a(x-p)^2+q$ | titik puncak $(p,q)$ + satu titik lain |

Nilai maksimum/minimum adalah $q$, dicapai saat $x=p$. Bentuk faktor hanya ada jika $D\\ge0$.
""")


def constructor():
    st.markdown("Pilih informasi yang diketahui, isi nilainya, lalu lihat penyelesaian langkah demi langkah dan grafiknya.")
    mode = st.radio("Diketahui:", ["Tiga titik", "Titik potong sumbu x + satu titik", "Titik puncak + satu titik"], horizontal=True)
    if mode == "Tiga titik":
        d = [(-1, 0), (0, -3), (1, -4)]
        P = []
        for i in range(3):
            c1, c2 = st.columns(2)
            P.append((Fr(c1.number_input(f"x{i + 1}", value=float(d[i][0]), step=1.0, key=f"t{i}x")),
                      Fr(c2.number_input(f"y{i + 1}", value=float(d[i][1]), step=1.0, key=f"t{i}y"))))
        if len({p[0] for p in P}) < 3:
            st.error("Ketiga titik harus punya x berbeda.")
            return
        (x1, y1), (x2, y2), (x3, y3) = P
        A1, B1, R1 = x2 * x2 - x1 * x1, x2 - x1, y2 - y1
        A2, B2, R2 = x3 * x3 - x1 * x1, x3 - x1, y3 - y1
        det = A1 * B2 - A2 * B1
        a = (R1 * B2 - R2 * B1) / det
        b = (A1 * R2 - A2 * R1) / det
        c = y1 - a * x1 * x1 - b * x1
        st.markdown("**Langkah 1 - Substitusi** tiap titik ke $f(x)=ax^2+bx+c$:")
        for i, (x, y) in enumerate(P, 1):
            st.latex(f"({i})\\quad {expr([(x * x, 'a'), (x, 'b'), (1, 'c')])} = {L(y)}")
        st.markdown("**Langkah 2 - Eliminasi $c$:** (2)−(1) dan (3)−(1):")
        st.latex(f"{expr([(A1, 'a'), (B1, 'b')])}={L(R1)}")
        st.latex(f"{expr([(A2, 'a'), (B2, 'b')])}={L(R2)}")
        st.markdown(f"**Langkah 3 - Selesaikan SPLDV** → $a={L(a)}$, $b={L(b)}$. **Langkah 4 -** substitusi ke (1): $c={L(c)}$.")
        pts = [(float(x), float(y)) for x, y in P]
    elif mode.startswith("Titik potong"):
        c1, c2, c3, c4 = st.columns(4)
        r1, r2 = Fr(c1.number_input("x₁", value=1.0, step=1.0)), Fr(c2.number_input("x₂", value=3.0, step=1.0))
        x0, y0 = Fr(c3.number_input("titik x", value=0.0, step=1.0)), Fr(c4.number_input("titik y", value=6.0, step=1.0))
        if x0 in (r1, r2):
            st.error("Titik lain tidak boleh berada di titik potong sumbu x.")
            return
        a = y0 / ((x0 - r1) * (x0 - r2))
        b, c = -a * (r1 + r2), a * r1 * r2
        st.markdown(f"**Langkah 1 -** bentuk faktor: $f(x)=a{xm(r1)}{xm(r2)}$.")
        st.markdown(f"**Langkah 2 -** substitusi $({L(x0)},{L(y0)})$: ${L(y0)}=a({L(x0 - r1)})({L(x0 - r2)})\\Rightarrow a={L(a)}$.")
        st.markdown(f"**Langkah 3 -** jabarkan: $f(x)={coef(a)}{xm(r1)}{xm(r2)}={poly(a, b, c)}$.")
        pts = [(float(r1), 0.0), (float(r2), 0.0), (float(x0), float(y0))]
    else:
        c1, c2, c3, c4 = st.columns(4)
        p, q = Fr(c1.number_input("p", value=3.0, step=1.0)), Fr(c2.number_input("q", value=-2.0, step=1.0))
        x0, y0 = Fr(c3.number_input("titik x", value=1.0, step=1.0)), Fr(c4.number_input("titik y", value=6.0, step=1.0))
        if x0 == p:
            st.error("Titik lain tidak boleh memiliki x yang sama dengan titik puncak.")
            return
        a = (y0 - q) / (x0 - p) ** 2
        b, c = -2 * a * p, a * p * p + q
        st.markdown(f"**Langkah 1 -** bentuk titik puncak: $f(x)=a(x-({L(p)}))^2+({L(q)})$.")
        st.markdown(f"**Langkah 2 -** substitusi $({L(x0)},{L(y0)})$: ${L(y0)}=a({L(x0 - p)})^2+({L(q)})\\Rightarrow a={L(a)}$.")
        st.markdown(f"**Langkah 3 -** jabarkan ke bentuk standar: $f(x)={poly(a, b, c)}$.")
        pts = [(float(p), float(q)), (float(x0), float(y0))]
    std, vt, fk = three_forms(a, b, c)
    st.success("Hasil - tiga bentuk fungsi:")
    st.latex(std); st.latex(vt); st.latex(fk)
    plot(parabola_fig(a, b, c, pts=pts))
    mark("p2_kons")


def page_solver():
    hero("🧮 Pembahasan Langkah demi Langkah", "Masukkan fungsi apa saja, aplikasi menganalisis & menjelaskan langkahnya")
    q = st.columns(3)
    a, b, c = (q[0].number_input("a", value=2.0, step=0.5), q[1].number_input("b", value=-8.0, step=0.5),
               q[2].number_input("c", value=6.0, step=0.5))
    if a == 0:
        st.error("a = 0: ini fungsi linear, bukan fungsi kuadrat.")
        return
    st.latex(f"f(x)={poly(Fr(a), Fr(b), Fr(c))}")
    l, r = st.columns(2)
    with l:
        show_steps(a, b, c)
    with r:
        plot(parabola_fig(a, b, c))


# ───────────────────────── Game ─────────────────────────
HOOPS = [(6, 3.05), (7, 3.5), (8, 3.0), (9, 4.0), (10, 3.05)]


def game1():
    st.markdown("### 🏀 Tembak Bola Basket")
    card("Bola dilempar dari $(0,2)$. Atur <b>titik puncak</b> lintasan $(p,q)$ agar bola masuk ke ring (⭕) dari atas. "
         "Bentuk fungsinya $f(x)=a(x-p)^2+q$ dengan $a$ dihitung otomatis dari titik $(0,2)$.")
    g = S.setdefault("g1", dict(lv=0, score=0, tries=0, msg=""))
    if g["lv"] >= len(HOOPS):
        st.success(f"🏆 Selesai! Skor akhir: **{g['score']} / {len(HOOPS) * 100}**")
        if st.button("Main lagi", key="g1r"):
            S.g1 = dict(lv=0, score=0, tries=0, msg="")
            st.rerun()
        return
    hx, hy = HOOPS[g["lv"]]
    st.markdown(f"**Level {g['lv'] + 1}/{len(HOOPS)}** · Ring di $({hx},{hy})$ · Skor: {g['score']}")
    c1, c2 = st.columns([1, 2])
    p = c1.slider("p (jarak titik tertinggi)", 1.0, 9.5, 4.0, 0.1, key=f"p{g['lv']}")
    q = c1.slider("q (tinggi maksimum)", 2.5, 12.0, 5.0, 0.1, key=f"q{g['lv']}")
    a = (2 - q) / p ** 2
    c1.latex(f"a={a:.3f}")
    c1.latex(f"f(x)={a:.3f}(x-{p:.1f})^2+{q:.1f}")
    x = np.linspace(0, hx + 2, 200)
    y = a * (x - p) ** 2 + q
    f = go.Figure()
    f.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#f97316", width=4), name="Lintasan"))
    f.add_trace(go.Scatter(x=[0], y=[2], mode="markers+text", text=["🏀"], textposition="top center", marker=dict(size=14, color="#f97316"), name="Bola"))
    f.add_trace(go.Scatter(x=[hx], y=[hy], mode="markers+text", text=["⭕ ring"], textposition="top right",
                           marker=dict(size=18, color="#ef4444", symbol="circle-open", line=dict(width=4)), name="Ring"))
    f.add_trace(go.Scatter(x=[p], y=[q], mode="markers", marker=dict(size=10, color="#4f46e5"), name="Puncak"))
    f.update_layout(template="plotly_white", height=380, margin=dict(l=10, r=10, t=10, b=10),
                    yaxis=dict(range=[0, 13]), xaxis=dict(range=[0, hx + 2]), legend=dict(orientation="h", y=-0.15))
    plot(f)
    if c1.button("🏀 Tembak!", key=f"shoot{g['lv']}"):
        g["tries"] += 1
        fy = a * (hx - p) ** 2 + q
        if hx <= p:
            g["msg"] = "❌ Bola mengenai ring saat masih naik. Geser titik puncak (p) lebih dekat ke pelempar."
        elif abs(fy - hy) <= 0.25:
            pts = max(20, 100 - 20 * (g["tries"] - 1))
            g["score"] += pts
            g["lv"] += 1
            g["tries"] = 0
            g["msg"] = f"✅ MASUK! +{pts} poin (f({hx}) = {fy:.2f})"
            mark("game1", round(100 * g["score"] / (len(HOOPS) * 100)))
        else:
            g["msg"] = f"❌ Meleset: pada x = {hx} tinggi bola {fy:.2f}, ring di {hy}. {'Naikkan' if fy < hy else 'Turunkan'} lintasan."
        st.rerun()
    if g["msg"]:
        (st.success if g["msg"].startswith("✅") else st.error)(g["msg"])


def gen_q():
    t = random.randint(1, 5)
    if t == 5:
        a, b, c = random.choice([-2, -1, 1, 2]), random.randint(-6, 6), random.randint(-6, 6)
    else:
        a, x1, x2 = random.choice([-3, -2, -1, 1, 2, 3]), random.randint(-5, 5), random.randint(-5, 5)
        b, c = -a * (x1 + x2), a * x1 * x2
    A, B, C = Fr(a), Fr(b), Fr(c)
    D = B * B - 4 * A * C
    xs = -B / (2 * A)
    ys = A * xs * xs + B * xs + C
    Q = {1: ("Tentukan **sumbu simetri** $x=\\ ?$", float(xs), None),
         2: ("Tentukan **diskriminan** $D$.", float(D), None),
         3: ("Tentukan **titik potong sumbu y**, yaitu $(0,\\ ?)$", float(C), None),
         4: (f"Tentukan **nilai {'minimum' if a > 0 else 'maksimum'}** fungsi.", float(ys), None),
         5: ("Berapa **banyak titik potong** dengan sumbu x?", "2" if D > 0 else ("1" if D == 0 else "0"), ["0", "1", "2"])}[t]
    return dict(a=a, b=b, c=c, q=Q[0], ans=Q[1], opt=Q[2])


def game2():
    st.markdown("### ⚡ Kuis Kilat Parabola")
    card("10 soal acak, jawab sebanyak mungkin dengan benar. Streak (benar berturut-turut) memberi <b>bonus poin</b>!")
    g = S.setdefault("g2", dict(i=0, ok=0, streak=0, pts=0, q=gen_q(), fb=""))
    if g["i"] >= 10:
        st.success(f"🏁 Selesai! Benar {g['ok']}/10 · Poin {g['pts']}")
        if st.button("Main lagi", key="g2r"):
            S.g2 = dict(i=0, ok=0, streak=0, pts=0, q=gen_q(), fb="")
            st.rerun()
        return
    if g["fb"]:
        (st.success if g["fb"].startswith("✅") else st.error)(g["fb"])
    q = g["q"]
    st.markdown(f"**Soal {g['i'] + 1}/10** · 🔥 Streak {g['streak']} · Poin {g['pts']}")
    st.latex(f"f(x)={poly(q['a'], q['b'], q['c'])}")
    with st.form("g2f"):
        st.markdown(q["q"])
        v = st.selectbox("Jawaban", ["-"] + q["opt"]) if q["opt"] else st.number_input("Jawaban", value=None, step=0.5, format="%g")
        go_ = st.form_submit_button("Jawab ➜")
    if go_:
        good = (v == q["ans"]) if q["opt"] else (v is not None and abs(v - q["ans"]) < 0.02)
        if good:
            g["ok"] += 1; g["streak"] += 1
            g["pts"] += 10 + 5 * min(g["streak"] - 1, 4)
            g["fb"] = f"✅ Benar! Jawaban: {q['ans']:g}" if not q["opt"] else f"✅ Benar! Jawaban: {q['ans']}"
        else:
            g["streak"] = 0
            g["fb"] = f"❌ Kurang tepat. Jawaban benar: {q['ans'] if q['opt'] else format(q['ans'], 'g')}"
        g["i"] += 1
        g["q"] = gen_q()
        if g["i"] >= 10:
            mark("game2", g["ok"] * 10)
        st.rerun()


def page_game():
    hero("🎮 Game Edukasi", "Belajar sambil bermain: terapkan konsep titik puncak, diskriminan, dan sumbu simetri")
    t = st.tabs(["🏀 Tembak Bola Basket", "⚡ Kuis Kilat"])
    with t[0]:
        game1()
    with t[1]:
        game2()


# ───────────────────────── Progres & Refleksi ─────────────────────────
def page_progress():
    hero("📊 Progres Belajar & Refleksi", "Pantau capaianmu dan isi lembar refleksi (Ayo, Berefleksi)")
    m = st.columns(3)
    m[0].metric("Aktivitas selesai", f"{sum(1 for k in ITEMS if S.prog.get(k, 0) > 0)}/{len(ITEMS)}")
    m[1].metric("Total XP", xp())
    lvl = "🌱 Pemula" if xp() < 300 else "🚀 Penjelajah" if xp() < 700 else "🏆 Master Parabola"
    m[2].metric("Level", lvl)
    st.progress(pct() / 100, text=f"{pct()}% selesai")
    df = pd.DataFrame([{"Aktivitas": v, "Status": "✅ Selesai" if S.prog.get(k, 0) > 0 else "⬜ Belum",
                        "Skor terbaik": S.prog.get(k, 0)} for k, v in ITEMS.items()])
    st.dataframe(df, hide_index=True)
    st.download_button("⬇️ Unduh rekap (CSV)", df.to_csv(index=False).encode("utf-8"), "rekap_progres.csv", "text/csv")
    nilai = [S.prog[k] for k in ("diag", "p1_lkpd", "p1_exit", "p2_kuis", "p2_lkpd", "p2_exit") if k in S.prog]
    if nilai:
        st.info(f"Rata-rata nilai asesmen: **{sum(nilai) / len(nilai):.1f}** · "
                f"{'Tuntas, coba pengayaan!' if sum(nilai) / len(nilai) >= 75 else 'Perlu penguatan, ulangi bagian yang masih sulit.'}")
    st.markdown("### 📝 Refleksi siswa")
    with st.form("refl"):
        qs = ["Saya tertarik ketika pembelajaran dimulai dengan gambar lintasan bola basket dan masalah sehari-hari.",
              "Saya lebih mudah memahami karakteristik grafik dengan bantuan visualisasi interaktif.",
              "Saya mudah memahami cara menyusun fungsi kuadrat ketika berdiskusi dengan teman.",
              "Saya dapat menentukan titik puncak serta nilai maksimum atau minimum suatu fungsi kuadrat."]
        r = [(st.radio(q, ["Ya", "Belum"], horizontal=True, index=None, key=f"r{i}"),
              st.text_input("Alasan singkat", key=f"ra{i}")) for i, q in enumerate(qs)]
        sulit = st.text_area("Bagian materi yang masih sulit bagi saya adalah ...")
        if st.form_submit_button("Simpan refleksi"):
            S.refl = {"jawaban": r, "sulit": sulit}
            mark("refleksi")
            st.success("Refleksi tersimpan. Terima kasih! 🙌")
    if st.button("🗑️ Reset semua progres"):
        for k in list(S.keys()):
            del S[k]
        st.rerun()


# ───────────────────────── Navigasi ─────────────────────────
NAV = ["🏠 Beranda", "🩺 Asesmen Diagnostik", "📘 Pertemuan 1: Karakteristik", "📗 Pertemuan 2: Mengonstruksi",
       "🧮 Pembahasan Langkah", "🎮 Game Edukasi", "📊 Progres & Refleksi"]
PAGES = dict(zip(NAV, [page_home, page_diag, page_p1, page_p2, page_solver, page_game, page_progress]))

with st.sidebar:
    st.markdown("## 📈 MathFunction")
    st.caption("Fungsi Kuadrat · SMA Kelas X (Fase E)")
    st.radio("Menu", NAV, key="nav", label_visibility="collapsed")
    st.progress(pct() / 100, text=f"Progres {pct()}%")
    st.markdown(f'<span class="badge">XP {xp()}</span>', unsafe_allow_html=True)
    st.caption("Modul Ajar: Alexius Juliyan Budiuntoro")

PAGES[S.nav]()
