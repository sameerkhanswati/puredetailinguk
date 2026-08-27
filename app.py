
"""
PURE DETAILING UK — Premium Automotive Detailing Website
Built with Streamlit for client preview / Streamlit Community Cloud deployment.

Run locally:
    streamlit run app.py

Website designed and developed by SamX Systems.
"""

import base64
import re
from pathlib import Path

import streamlit as st

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Pure Detailing UK | Premium Automotive Care",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# CONSTANTS — client info (do not change without client sign-off)
# --------------------------------------------------------------------------
BRAND_NAME = "PURE DETAILING UK"
PHONE_DISPLAY = "+44 7875 500935"
PHONE_WA = "447875500935"
EMAIL = "info@puredetailing.com"
HOURS_LINE1 = "Monday – Saturday"
HOURS_LINE2 = "09:00 – 18:00"
WHATSAPP_URL = f"https://wa.me/{PHONE_WA}"
DEVELOPER_CREDIT = "SamX Systems"

IMAGES_DIR = Path(__file__).parent / "images"

SERVICE_OPTIONS = [
    "Maintenance Wash",
    "Paint Correction",
    "Ceramic Coating",
    "Vehicle Wrapping",
    "Paint Protection Film",
    "Performance Tuning",
    "Not Sure – Need Advice",
]

# --------------------------------------------------------------------------
# IMAGE HANDLING — optimized, cached WebP data URIs
# --------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_image_b64(filename: str, max_width: int = 1800, quality: int = 78) -> str | None:
    """Load once, resize oversized files, and cache a compact WebP data URI."""
    path = IMAGES_DIR / filename
    try:
        from io import BytesIO
        from PIL import Image
        with Image.open(path) as image:
            image = image.convert("RGB")
            if image.width > max_width:
                ratio = max_width / image.width
                image = image.resize((max_width, max(1, int(image.height * ratio))), Image.Resampling.LANCZOS)
            output = BytesIO()
            image.save(output, format="WEBP", quality=quality, method=6)
            data = output.getvalue()
        return "data:image/webp;base64," + base64.b64encode(data).decode("ascii")
    except (FileNotFoundError, OSError, ValueError):
        return None

def bg_style(filename: str, fallback_gradient: str = "linear-gradient(160deg,#151515,#050505)") -> str:
    uri = load_image_b64(filename)
    return f"url('{uri}')" if uri else fallback_gradient

_IMAGE_FILES = {
    "hero":"hero-car.jpg", "intro":"home-detailing.jpg",
    "maintenance":"maintenance-wash.jpg", "correction":"paint-correction.jpg",
    "ceramic":"ceramic-coating.jpg", "wrap":"car-wrapping.jpg",
    "ppf":"ppf-installation.jpg", "tuning":"car-tuning.jpg",
    "water":"ceramic-water-beading.jpg", "ppf_close":"ppf-closeup.jpg",
    "engine":"engine-tuning.jpg", "workshop":"workshop.jpg", "detailer":"detailer-working.jpg",
}
_IMAGE_VARS = "\n".join(f"        --img-{k}:{bg_style(v)};" for k,v in _IMAGE_FILES.items())

# --------------------------------------------------------------------------
# GLOBAL CSS
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Oswald:wght@400;500;600;700&display=swap');

    :root{
        --pd-ink:#171717;
        --pd-ink-2:#222222;
        --pd-cream:#F5F2EC;
        --pd-white:#FFFFFF;
        --pd-soft:#ECE7DE;
        --pd-gold:#B58A3A;
        --pd-gold-light:#D7B66A;
        --pd-gold-dark:#8B682C;
        --pd-body:#4E4E4E;
        --pd-muted:#6D6D6D;
        --pd-line:#DED8CE;
        --pd-dark-line:rgba(255,255,255,.14);
    }

    html, body, #root, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"]{
        background:var(--pd-cream) !important;
        color:var(--pd-ink) !important;
    }

    #MainMenu, footer,
    header,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    section[data-testid="stSidebar"]{
        display:none !important;
    }

    .block-container{
        padding:0 !important;
        max-width:none !important;
    }

    *{box-sizing:border-box;}
    html{scroll-behavior:smooth;}
    body{margin:0;overflow-x:hidden;font-family:'DM Sans',Arial,sans-serif;}
    a{text-decoration:none !important;color:inherit;}
    ::selection{background:var(--pd-gold);color:#fff;}

    .pd-section h1,.pd-section h2,.pd-section h3,
    .pd-hero h1,.pd-feature h2,
    .pd-heading{
        font-family:'Oswald',Arial,sans-serif !important;
        color:var(--pd-ink) !important;
        text-transform:uppercase;
        letter-spacing:.02em;
        line-height:.96;
        margin:0;
    }

    .pd-label{
        display:block;
        margin-bottom:18px;
        color:var(--pd-gold-dark) !important;
        font-size:.72rem !important;
        line-height:1.2;
        font-weight:700 !important;
        letter-spacing:3px !important;
        text-transform:uppercase;
    }

    .pd-label::before{
        content:"";
        display:inline-block;
        width:34px;
        height:2px;
        margin:0 11px 3px 0;
        background:var(--pd-gold);
    }

    .pd-muted{
        color:var(--pd-body) !important;
        font-size:1rem;
        font-weight:400;
        line-height:1.85;
    }

    @keyframes pdFadeUp{
        from{opacity:0;transform:translateY(30px)}
        to{opacity:1;transform:translateY(0)}
    }
    @keyframes pdShine{
        0%{transform:translateX(-150%) skewX(-18deg)}
        45%,100%{transform:translateX(280%) skewX(-18deg)}
    }
    @keyframes pdGoldPulse{
        0%,100%{box-shadow:0 0 0 rgba(181,138,58,0)}
        50%{box-shadow:0 0 34px rgba(181,138,58,.16)}
    }
    @keyframes pdLine{
        from{transform:scaleX(0);transform-origin:left}
        to{transform:scaleX(1);transform-origin:left}
    }
    .pd-fade{animation:pdFadeUp .8s cubic-bezier(.22,1,.36,1) both;}

    .pd-nav{
        position:fixed;
        inset:0 0 auto 0;
        z-index:9999;
        min-height:82px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:28px;
        padding:0 5.5%;
        background:rgba(20,20,20,.96) !important;
        border-bottom:1px solid rgba(255,255,255,.10);
        box-shadow:0 10px 40px rgba(0,0,0,.18);
    }

    .pd-logo{
        flex:0 0 auto;
        font-family:'Oswald',sans-serif !important;
        font-size:1.45rem !important;
        font-weight:600 !important;
        letter-spacing:2px !important;
        color:#fff !important;
        white-space:nowrap;
    }
    .pd-logo span{color:var(--pd-gold-light) !important;}
    .pd-logo b{
        margin-left:5px;
        color:#BDBDBD !important;
        font-size:.58em;
        letter-spacing:3px;
    }

    .pd-nav-links{
        display:flex;
        align-items:center;
        justify-content:center;
        gap:30px;
        flex:1;
    }
    .pd-nav-links a{
        color:#F5F5F5 !important;
        font-size:.72rem !important;
        font-weight:700 !important;
        letter-spacing:1.8px !important;
        transition:color .25s ease,transform .25s ease;
    }
    .pd-nav-links a:hover{
        color:var(--pd-gold-light) !important;
        transform:translateY(-1px);
    }

    .pd-cta-btn{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        min-height:46px;
        padding:0 22px;
        border:1px solid var(--pd-gold-light) !important;
        color:var(--pd-gold-light) !important;
        background:transparent !important;
        font-size:.69rem !important;
        font-weight:700 !important;
        letter-spacing:1.8px !important;
        white-space:nowrap;
        transition:background .25s ease,color .25s ease,transform .25s ease;
    }
    .pd-cta-btn:hover{
        background:var(--pd-gold-light) !important;
        color:#151515 !important;
        transform:translateY(-2px);
    }

    .pd-hero{
        position:relative;
        min-height:760px;
        height:100vh;
        display:flex;
        align-items:flex-end;
        padding:0 6% 92px;
        overflow:hidden;
        isolation:isolate;
        background-color:#101010 !important;
        background-size:cover;
        background-position:center;
    }

    .pd-hero::before{
        content:"";
        position:absolute;
        inset:0;
        z-index:-1;
        background:
            linear-gradient(90deg,rgba(8,8,8,.92) 0%,rgba(8,8,8,.68) 42%,rgba(8,8,8,.18) 78%),
            linear-gradient(0deg,rgba(8,8,8,.94) 0%,rgba(8,8,8,.16) 62%,rgba(8,8,8,.35) 100%);
    }
    .pd-hero::after{
        content:"";
        position:absolute;
        inset:auto 0 0;
        height:3px;
        background:linear-gradient(90deg,transparent,var(--pd-gold-light),transparent);
        animation:pdLine 1.4s ease both;
    }

    .pd-hero-inner{
        position:relative;
        z-index:2;
        max-width:800px;
        animation:pdFadeUp 1s cubic-bezier(.22,1,.36,1) both;
    }

    .pd-hero .pd-label{color:var(--pd-gold-light) !important;}
    .pd-hero .pd-label::before{background:var(--pd-gold-light);}

    .pd-hero h1{
        max-width:800px;
        font-size:clamp(4rem,8vw,7.6rem) !important;
        font-weight:600 !important;
        color:#FFFFFF !important;
        text-shadow:0 8px 30px rgba(0,0,0,.35);
        margin-bottom:26px !important;
    }

    .pd-hero .pd-muted{
        max-width:610px;
        color:rgba(255,255,255,.84) !important;
        font-size:1.05rem;
    }

    .pd-hero-btns{
        display:flex;
        gap:14px;
        flex-wrap:wrap;
        margin-top:34px;
    }

    .pd-btn-primary,.pd-btn-outline{
        position:relative;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        min-height:54px;
        padding:0 28px;
        font-size:.72rem !important;
        font-weight:700 !important;
        letter-spacing:1.8px !important;
        text-transform:uppercase;
        overflow:hidden;
        transition:transform .25s ease,background .25s ease,color .25s ease,border-color .25s ease;
    }

    .pd-btn-primary{
        background:var(--pd-gold-light) !important;
        color:#171717 !important;
        animation:pdGoldPulse 3.5s ease-in-out infinite;
    }
    .pd-btn-primary::after{
        content:"";
        position:absolute;
        inset:0;
        width:35%;
        background:rgba(255,255,255,.30);
        transform:translateX(-150%) skewX(-18deg);
        animation:pdShine 5s ease-in-out infinite;
    }
    .pd-btn-primary:hover{
        transform:translateY(-3px);
        background:#E2C37C !important;
        color:#111 !important;
    }

    .pd-btn-outline{
        border:1px solid rgba(255,255,255,.55) !important;
        color:#FFFFFF !important;
        background:rgba(255,255,255,.04) !important;
    }
    .pd-btn-outline:hover{
        border-color:var(--pd-gold-light) !important;
        color:var(--pd-gold-light) !important;
        background:rgba(181,138,58,.10) !important;
        transform:translateY(-3px);
    }

    .pd-section{
        position:relative;
        padding:110px 6%;
        background:var(--pd-cream) !important;
        color:var(--pd-ink) !important;
    }
    .pd-section-alt{
        background:var(--pd-ink) !important;
        color:#fff !important;
    }
    .pd-section-alt h1,.pd-section-alt h2,.pd-section-alt h3{
        color:#FFFFFF !important;
    }
    .pd-section-alt .pd-muted{color:#C8C8C8 !important;}
    .pd-section-alt .pd-label{color:var(--pd-gold-light) !important;}
    .pd-section-alt .pd-label::before{background:var(--pd-gold-light);}

    .pd-section::after{
        content:"";
        position:absolute;
        left:6%;
        right:6%;
        bottom:0;
        height:1px;
        background:var(--pd-line);
    }
    .pd-section-alt::after{background:var(--pd-dark-line);}

    .pd-split{
        display:flex;
        align-items:center;
        gap:78px;
        max-width:1420px;
        margin:0 auto;
    }
    .pd-split-img{
        flex:1 1 50%;
        min-height:520px;
        border-radius:4px;
        background-size:cover;
        background-position:center;
        box-shadow:0 28px 70px rgba(25,25,25,.16);
    }
    .pd-split-text{
        flex:1 1 50%;
        min-width:0;
    }
    .pd-split-text h2{
        font-size:clamp(2.7rem,4vw,4.4rem) !important;
        margin-bottom:26px !important;
    }
    .pd-split-text ul{
        list-style:none;
        padding:0;
        margin:30px 0 0;
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:0 28px;
    }
    .pd-split-text li{
        padding:14px 0;
        border-bottom:1px solid var(--pd-line);
        color:#353535 !important;
        font-size:.9rem;
        font-weight:600;
    }
    .pd-split-text li::before{
        content:"";
        display:inline-block;
        width:7px;
        height:7px;
        margin:0 11px 1px 0;
        background:var(--pd-gold);
        border-radius:50%;
    }

    .pd-services-head{
        max-width:720px;
        margin:0 auto 52px;
        text-align:left;
    }
    .pd-services-head h2{
        font-size:clamp(2.8rem,4.5vw,5rem) !important;
    }

    .pd-grid{
        max-width:1420px;
        margin:0 auto;
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:18px;
    }

    .pd-card{
        position:relative;
        min-height:420px;
        overflow:hidden;
        border:1px solid rgba(255,255,255,.12);
        background:#111 !important;
        transition:transform .45s cubic-bezier(.22,1,.36,1),box-shadow .45s ease,border-color .3s ease;
    }
    .pd-card:hover{
        transform:translateY(-8px);
        border-color:rgba(215,182,106,.55);
        box-shadow:0 25px 60px rgba(0,0,0,.36);
    }
    .pd-card-img{
        position:absolute;
        inset:0;
        background-size:cover;
        background-position:center;
        transition:transform .7s cubic-bezier(.22,1,.36,1);
    }
    .pd-card:hover .pd-card-img{transform:scale(1.075);}
    .pd-card::after{
        content:"";
        position:absolute;
        inset:0;
        background:
            linear-gradient(180deg,rgba(0,0,0,.04) 20%,rgba(0,0,0,.30) 48%,rgba(0,0,0,.94) 100%);
    }
    .pd-card-content{
        position:absolute;
        left:0;
        right:0;
        bottom:0;
        z-index:2;
        padding:30px;
    }
    .pd-card-num{
        display:block;
        margin-bottom:8px;
        color:var(--pd-gold-light) !important;
        font-family:'Oswald',sans-serif !important;
        font-size:.95rem !important;
        font-weight:600 !important;
        letter-spacing:2px;
    }
    .pd-card-content h3{
        color:#FFFFFF !important;
        font-size:1.7rem !important;
        margin-bottom:10px !important;
    }
    .pd-card-content p{
        max-width:360px;
        color:rgba(255,255,255,.76) !important;
        font-size:.84rem !important;
        line-height:1.7;
        margin:0;
    }

    .pd-feature{
        display:flex;
        min-height:570px;
        background:var(--pd-cream) !important;
    }
    .pd-feature.reverse{flex-direction:row-reverse;}
    .pd-feature-img{
        flex:1.15;
        min-height:570px;
        background-size:cover;
        background-position:center;
    }
    .pd-feature-text{
        flex:1;
        display:flex;
        flex-direction:column;
        justify-content:center;
        padding:80px 7%;
        background:var(--pd-cream) !important;
        color:var(--pd-ink) !important;
    }
    .pd-feature-text h2{
        font-size:clamp(3rem,4.6vw,5.2rem) !important;
        margin-bottom:24px !important;
    }
    .pd-feature-text .pd-muted{max-width:560px;}
    .pd-feature-list{
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:15px 30px;
        margin-top:30px;
    }
    .pd-feature-list div{
        padding:12px 0 12px 15px;
        border-left:2px solid var(--pd-gold);
        color:#292929 !important;
        font-size:.86rem;
        font-weight:700;
    }

    .pd-gallery{
        max-width:1420px;
        margin:0 auto;
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:16px;
    }
    .pd-gallery-item{
        position:relative;
        height:350px;
        overflow:hidden;
        background:#111 !important;
        border-radius:3px;
    }
    .pd-gallery-item .pd-g-img{
        position:absolute;
        inset:0;
        background-size:cover;
        background-position:center;
        transition:transform .7s cubic-bezier(.22,1,.36,1);
    }
    .pd-gallery-item:hover .pd-g-img{transform:scale(1.08);}
    .pd-gallery-item::after{
        content:"";
        position:absolute;
        inset:0;
        background:linear-gradient(180deg,transparent 40%,rgba(0,0,0,.86) 100%);
    }
    .pd-gallery-cap{
        position:absolute;
        left:22px;
        right:22px;
        bottom:20px;
        z-index:2;
        color:#fff !important;
        font-size:.72rem !important;
        font-weight:700 !important;
        letter-spacing:2px !important;
    }

    .pd-why-grid,.pd-process-grid{
        max-width:1420px;
        margin:0 auto;
        display:grid;
        grid-template-columns:repeat(4,minmax(0,1fr));
        gap:34px;
    }
    .pd-why-item .num,.pd-process-item .num{
        display:block;
        color:var(--pd-gold-light) !important;
        font-family:'Oswald',sans-serif !important;
        font-size:3.4rem !important;
        line-height:1 !important;
        margin-bottom:14px;
    }
    .pd-why-item h3,.pd-process-item h3{
        color:#fff !important;
        font-size:1.12rem !important;
        margin-bottom:10px !important;
        letter-spacing:1px;
    }
    .pd-why-item p,.pd-process-item p{
        color:#BDBDBD !important;
        font-size:.88rem !important;
        line-height:1.7;
        margin:0;
    }
    .pd-process-item{
        border-top:1px solid rgba(255,255,255,.18);
        padding-top:22px;
    }

    .pd-about-imgs{
        display:grid;
        grid-template-columns:1.2fr .8fr;
        gap:14px;
        height:540px;
    }
    .pd-about-imgs div{
        background-size:cover;
        background-position:center;
        border-radius:3px;
    }

    .pd-review-grid{
        max-width:1420px;
        margin:0 auto;
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:18px;
    }
    .pd-review-card{
        background:#FFFFFF !important;
        border:1px solid var(--pd-line);
        padding:32px;
        box-shadow:0 12px 35px rgba(20,20,20,.06);
    }
    .pd-review-tag{
        display:inline-block;
        margin-bottom:18px;
        padding:5px 10px;
        background:var(--pd-gold) !important;
        color:#fff !important;
        font-size:.62rem !important;
        font-weight:700 !important;
        letter-spacing:1.8px;
    }
    .pd-review-card p{
        color:#2F2F2F !important;
        font-size:.94rem !important;
        line-height:1.8;
        font-style:italic;
        margin:0;
    }
    .pd-review-name{
        margin-top:20px;
        color:#777 !important;
        font-size:.76rem !important;
        letter-spacing:1px;
    }

    .pd-contact-grid{
        max-width:1420px;
        margin:0 auto;
        display:grid;
        grid-template-columns:.85fr 1.15fr;
        gap:80px;
        align-items:start;
    }
    .pd-contact-heading h2{
        font-size:clamp(3rem,4.7vw,5.3rem) !important;
        margin-bottom:32px !important;
    }
    .pd-contact-item{margin-bottom:27px;}
    .pd-contact-item .lbl{
        display:block;
        margin-bottom:7px;
        color:var(--pd-gold-dark) !important;
        font-size:.68rem !important;
        font-weight:700 !important;
        letter-spacing:2px;
    }
    .pd-contact-item .val{
        color:#242424 !important;
        font-size:1.05rem !important;
        line-height:1.6;
    }
    .pd-wa-btn{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        min-height:50px;
        margin-top:5px;
        padding:0 24px;
        background:#1F9D55 !important;
        color:#fff !important;
        font-size:.72rem !important;
        font-weight:700 !important;
        letter-spacing:1.7px;
        transition:transform .25s ease,filter .25s ease;
    }
    .pd-wa-btn:hover{transform:translateY(-3px);filter:brightness(1.08);}

    .pd-contact-panel{
        padding:0 !important;
    }
    div[data-testid="stForm"]{
        background:#191919 !important;
        border:1px solid rgba(215,182,106,.32) !important;
        border-radius:5px !important;
        padding:38px !important;
        box-shadow:0 28px 70px rgba(0,0,0,.18) !important;
    }
    div[data-testid="stForm"] *,
    div[data-testid="stForm"] p,
    div[data-testid="stForm"] label,
    div[data-testid="stForm"] span{
        color:#F5F5F5 !important;
    }
    div[data-testid="stForm"] label p,
    div[data-testid="stForm"] label{
        color:#BEBEBE !important;
        font-size:.69rem !important;
        font-weight:700 !important;
        letter-spacing:1.5px !important;
        text-transform:uppercase;
    }
    div[data-testid="stForm"] input,
    div[data-testid="stForm"] textarea{
        min-height:48px;
        background:#0F0F0F !important;
        color:#FFFFFF !important;
        -webkit-text-fill-color:#FFFFFF !important;
        border:1px solid #4A4A4A !important;
        border-radius:3px !important;
        box-shadow:none !important;
    }
    div[data-testid="stForm"] input:focus,
    div[data-testid="stForm"] textarea:focus{
        border-color:var(--pd-gold-light) !important;
        box-shadow:0 0 0 1px var(--pd-gold-light) !important;
    }
    div[data-testid="stForm"] input::placeholder,
    div[data-testid="stForm"] textarea::placeholder{
        color:#777 !important;
        -webkit-text-fill-color:#777 !important;
    }
    div[data-testid="stForm"] div[data-baseweb="select"] > div{
        min-height:48px;
        background:#0F0F0F !important;
        border:1px solid #4A4A4A !important;
        border-radius:3px !important;
    }
    div[data-testid="stForm"] div[data-baseweb="select"] *,
    div[data-testid="stForm"] div[data-baseweb="select"] input{
        color:#FFFFFF !important;
        -webkit-text-fill-color:#FFFFFF !important;
    }
    div[role="listbox"]{
        background:#191919 !important;
        border:1px solid #555 !important;
    }
    div[role="option"]{
        background:#191919 !important;
        color:#FFFFFF !important;
    }
    div[role="option"]:hover{
        background:#2B2B2B !important;
    }
    div[data-testid="stForm"] button{
        min-height:52px !important;
        background:var(--pd-gold-light) !important;
        color:#171717 !important;
        border:0 !important;
        border-radius:3px !important;
        font-size:.72rem !important;
        font-weight:800 !important;
        letter-spacing:1.8px !important;
        text-transform:uppercase;
        transition:transform .25s ease,filter .25s ease;
    }
    div[data-testid="stForm"] button:hover{
        transform:translateY(-2px);
        filter:brightness(1.05);
    }
    div[data-testid="stForm"] [data-testid="stDateInput"] input{
        color:#FFFFFF !important;
    }
    div[data-testid="stForm"] [data-testid="stFormSubmitButton"]{
        margin-top:8px;
    }

    .pd-footer{
        padding:64px 6% 28px;
        background:#151515 !important;
        color:#fff !important;
    }
    .pd-footer-top{
        max-width:1420px;
        margin:0 auto 42px;
        display:flex;
        justify-content:space-between;
        gap:30px;
        flex-wrap:wrap;
    }
    .pd-footer-logo{
        font-family:'Oswald',sans-serif !important;
        font-size:1.8rem !important;
        letter-spacing:2px;
        color:#fff !important;
    }
    .pd-footer-logo span{color:var(--pd-gold-light) !important;}
    .pd-footer-logo b{color:#AAA !important;font-size:.6em;letter-spacing:3px;margin-left:4px;}
    .pd-footer-tag{
        margin-top:7px;
        color:#999 !important;
        font-size:.84rem !important;
    }
    .pd-footer-links{
        display:flex;
        gap:25px;
        flex-wrap:wrap;
    }
    .pd-footer-links a{
        color:#DDD !important;
        font-size:.7rem !important;
        font-weight:700 !important;
        letter-spacing:1.4px;
    }
    .pd-footer-links a:hover{color:var(--pd-gold-light) !important;}
    .pd-footer-bottom{
        max-width:1420px;
        margin:0 auto;
        padding-top:22px;
        border-top:1px solid rgba(255,255,255,.12);
        display:flex;
        justify-content:space-between;
        gap:15px;
        flex-wrap:wrap;
        color:#8E8E8E !important;
        font-size:.72rem !important;
    }

    .pd-contact-panel{
        background:var(--pd-cream) !important;
        color:var(--pd-ink) !important;
        padding:78px 8% !important;
        border:1px solid var(--pd-line) !important;
        border-radius:4px !important;
        box-shadow:0 20px 55px rgba(20,20,20,.08);
    }
    .pd-contact-panel h2{
        color:var(--pd-ink) !important;
        font-family:'Oswald',Arial,sans-serif !important;
        font-size:clamp(2.8rem,4.2vw,4.8rem) !important;
        line-height:.98 !important;
        margin:0 0 32px !important;
    }
    .pd-contact-panel .pd-label{
        color:var(--pd-gold-dark) !important;
    }
    .pd-contact-panel .pd-label::before{
        background:var(--pd-gold) !important;
    }
    .pd-contact-panel .pd-contact-item .lbl{
        color:var(--pd-gold-dark) !important;
    }
    .pd-contact-panel .pd-contact-item .val{
        color:#222222 !important;
        -webkit-text-fill-color:#222222 !important;
    }
    .pd-contact-panel .pd-contact-item a{
        color:#222222 !important;
    }

    .pd-section:not(.pd-section-alt) h1,
    .pd-section:not(.pd-section-alt) h2,
    .pd-section:not(.pd-section-alt) h3,
    .pd-section:not(.pd-section-alt) p,
    .pd-section:not(.pd-section-alt) li{
        color:inherit;
    }

    @media (max-width:1100px){
        .pd-nav{padding:0 4%;}
        .pd-nav-links{gap:18px;}
        .pd-grid{grid-template-columns:repeat(2,minmax(0,1fr));}
        .pd-why-grid,.pd-process-grid{grid-template-columns:1fr 1fr;}
        .pd-contact-grid{gap:45px;}
    }

    @media (max-width:900px){
        .pd-nav{min-height:72px;}
        .pd-nav-links{display:none;}
        .pd-logo{font-size:1.2rem !important;}
        .pd-hero{min-height:700px;padding:0 7% 65px;}
        .pd-hero h1{font-size:clamp(3.7rem,12vw,6rem) !important;}
        .pd-section{padding:78px 7%;}
        .pd-split{flex-direction:column;gap:45px;}
        .pd-split-img{width:100%;min-height:390px;}
        .pd-split-text{width:100%;}
        .pd-feature,.pd-feature.reverse{flex-direction:column;}
        .pd-feature-img{min-height:360px;}
        .pd-feature-text{padding:65px 7%;}
        .pd-gallery{grid-template-columns:1fr 1fr;}
        .pd-about-imgs{height:auto;grid-template-columns:1fr 1fr;}
        .pd-contact-grid{grid-template-columns:1fr;}
        .pd-contact-form-wrap{width:100%;}
    }

    @media (max-width:650px){
        .pd-cta-btn{padding:0 13px;font-size:.62rem !important;}
        .pd-hero{min-height:650px;}
        .pd-hero h1{font-size:3.55rem !important;}
        .pd-hero-btns{flex-direction:column;align-items:stretch;}
        .pd-btn-primary,.pd-btn-outline{width:100%;}
        .pd-split-text ul{grid-template-columns:1fr;}
        .pd-grid,.pd-gallery,.pd-review-grid{grid-template-columns:1fr;}
        .pd-card{min-height:390px;}
        .pd-about-imgs{grid-template-columns:1fr;}
        .pd-about-imgs div{height:300px;}
        .pd-feature-list{grid-template-columns:1fr;}
        .pd-why-grid,.pd-process-grid{grid-template-columns:1fr;}
        div[data-testid="stForm"]{padding:25px !important;}
        .pd-footer-links{gap:15px;}
    }

    @media (prefers-reduced-motion:reduce){
        html{scroll-behavior:auto;}
        *,*::before,*::after{
            animation-duration:.01ms !important;
            animation-iteration-count:1 !important;
            transition-duration:.01ms !important;
        }
    }
    /* ============================================================
   STREAMLIT CLOUD — DATE PICKER FIX
   ============================================================ */

    div[data-baseweb="calendar"] {
        background: #191919 !important;
        color: #FFFFFF !important;
        border: 1px solid #4A4A4A !important;
    }

    div[data-baseweb="calendar"] * {
        color: #FFFFFF !important;
    }

    div[data-baseweb="calendar"] button {
        background: #191919 !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="calendar"] button:hover {
        background: #2B2B2B !important;
        color: #D7B66A !important;
    }

    div[data-baseweb="calendar"] button[aria-selected="true"] {
        background: #D7B66A !important;
        color: #171717 !important;
    }

    div[data-baseweb="calendar"] svg {
        fill: #FFFFFF !important;
    }

    div[data-baseweb="popover"] {
        background: #191919 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<style>:root{" + _IMAGE_VARS + "}</style>",
    unsafe_allow_html=True,
)

def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

st.markdown(
    f"""
    <div class="pd-nav">
        <div class="pd-logo"><span>PURE</span> DETAILING <b>UK</b></div>
        <div class="pd-nav-links">
            <a href="#home">HOME</a>
            <a href="#services">SERVICES</a>
            <a href="#work">OUR WORK</a>
            <a href="#about">ABOUT</a>
            <a href="#reviews">REVIEWS</a>
            <a href="#contact">CONTACT</a>
        </div>
        <a href="#contact" class="pd-cta-btn">BOOK YOUR DETAIL</a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div id="home" class="pd-hero" style="background-image:var(--img-hero);">
        <div class="pd-hero-inner">
            <span class="pd-label">PREMIUM AUTOMOTIVE CARE</span>
            <h1>DETAILING<br>WITHOUT<br>COMPROMISE</h1>
            <p class="pd-muted">Precision detailing, advanced paint protection and performance
            enhancement for vehicles that deserve more.</p>
            <div class="pd-hero-btns">
                <a href="#contact" class="pd-btn-primary">BOOK A SERVICE</a>
                <a href="#services" class="pd-btn-outline">EXPLORE SERVICES</a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="pd-section">
        <div class="pd-split">
            <div class="pd-split-img pd-fade" style="background-image:var(--img-intro);"></div>
            <div class="pd-split-text pd-fade">
                <span class="pd-label">OUR APPROACH</span>
                <h2>ENGINEERED<br>FOR PERFECTION.</h2>
                <p class="pd-muted">Pure Detailing UK provides a complete range of professional
                automotive care services — from routine maintenance to advanced protection and
                performance enhancement — each carried out with precision and premium products.</p>
                <ul>
                    <li>Maintenance Washes</li>
                    <li>Paint Correction</li>
                    <li>Ceramic Coating</li>
                    <li>Paint Protection Film</li>
                    <li>Vehicle Wrapping</li>
                    <li>Performance Tuning</li>
                </ul>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

services = [
    ("01", "Maintenance Wash", "Professional maintenance washing designed to safely remove dirt and contamination while preserving the vehicle's finish.", "maintenance-wash.jpg"),
    ("02", "Paint Correction", "Machine polishing and correction techniques designed to reduce visible imperfections and restore clarity and gloss.", "paint-correction.jpg"),
    ("03", "Ceramic Coating", "Advanced ceramic protection designed to enhance gloss, hydrophobic performance and easier maintenance.", "ceramic-coating.jpg"),
    ("04", "Vehicle Wrapping", "Premium vinyl wrapping, colour changes and styling enhancements professionally installed.", "car-wrapping.jpg"),
    ("05", "Paint Protection Film", "Professional PPF installation designed to help protect vulnerable painted surfaces from everyday road debris and wear.", "ppf-installation.jpg"),
    ("06", "Performance Tuning", "Professional performance enhancement solutions tailored to the vehicle and driving requirements.", "car-tuning.jpg"),
]

def image_var(filename: str) -> str:
    return {
        "maintenance-wash.jpg":"var(--img-maintenance)",
        "paint-correction.jpg":"var(--img-correction)",
        "ceramic-coating.jpg":"var(--img-ceramic)",
        "car-wrapping.jpg":"var(--img-wrap)",
        "ppf-installation.jpg":"var(--img-ppf)",
        "car-tuning.jpg":"var(--img-tuning)",
    }.get(filename, "linear-gradient(160deg,#151515,#050505)")

cards_html = "".join(
    f"""
    <article class="pd-card">
        <span class="pd-card-img" style="background-image:{image_var(img)};"></span>
        <div class="pd-card-content">
            <span class="pd-card-num">{num}</span>
            <h3>{esc(name)}</h3>
            <p>{esc(desc)}</p>
        </div>
    </article>
    """
    for num, name, desc, img in services
)

st.markdown(
    f"""
    <section id="services" class="pd-section pd-section-alt">
        <div class="pd-services-head">
            <span class="pd-label">WHAT WE DO</span>
            <h2>OUR SERVICES.</h2>
        </div>
        <div class="pd-grid">
            {cards_html}
        
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="pd-feature">
        <div class="pd-feature-img" style="background-image:var(--img-water);"></div>
        <div class="pd-feature-text">
            <span class="pd-label">CERAMIC COATING</span>
            <h2>PROTECTION<br>THAT PERFORMS.</h2>
            <p class="pd-muted">A durable ceramic layer engineered to enhance gloss and shield
            your paintwork from everyday contamination.</p>
            <div class="pd-feature-list">
                <div>Enhanced Gloss</div>
                <div>Hydrophobic Surface</div>
                <div>Easier Maintenance</div>
                <div>Long-Term Protection</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="pd-feature reverse">
        <div class="pd-feature-img" style="background-image:var(--img-ppf_close);"></div>
        <div class="pd-feature-text">
            <span class="pd-label">PAINT PROTECTION FILM</span>
            <h2>INVISIBLE<br>PROTECTION.</h2>
            <p class="pd-muted">Professionally installed PPF helps shield vulnerable panels from
            stone chips, road debris and everyday wear, while preserving the factory finish
            underneath. Our team fits film with precision, keeping the result virtually undetectable.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="pd-feature">
        <div class="pd-feature-img" style="background-image:var(--img-engine);"></div>
        <div class="pd-feature-text">
            <span class="pd-label">PERFORMANCE TUNING</span>
            <h2>UNLOCK YOUR<br>VEHICLE'S<br>POTENTIAL.</h2>
            <p class="pd-muted">Our tuning specialists tailor performance solutions to your
            vehicle and driving requirements, carried out with the same precision applied to
            every service we offer.</p>
            <a href="#contact" class="pd-btn-primary" style="margin-top:10px;">ENQUIRE ABOUT TUNING</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

gallery_items = [
    ("maintenance-wash.jpg", "MAINTENANCE WASH"),
    ("paint-correction.jpg", "PAINT CORRECTION"),
    ("ceramic-coating.jpg", "CERAMIC COATING"),
    ("car-wrapping.jpg", "VEHICLE WRAPPING"),
    ("ppf-installation.jpg", "PAINT PROTECTION FILM"),
    ("car-tuning.jpg", "PERFORMANCE TUNING"),
]
gallery_html = "".join(
    f"""
    <figure class="pd-gallery-item">
        <span class="pd-g-img" style="background-image:{image_var(img)};"></span>
        <figcaption class="pd-gallery-cap">{cap}</figcaption>
    </figure>
    """
    for img, cap in gallery_items
)
st.markdown(
    f"""
    <section id="work" class="pd-section">
        <div class="pd-services-head">
            <span class="pd-label">OUR WORK</span>
            <h2>PRECISION IN EVERY DETAIL.</h2>
        </div>
        <div class="pd-gallery">
            {gallery_html}
        
    </section>
    """,
    unsafe_allow_html=True,
)

why_items = [
    ("01", "PRECISION CRAFTSMANSHIP", "Every vehicle is treated with exceptional attention to detail."),
    ("02", "PREMIUM PRODUCTS", "Professional-grade products and proven detailing techniques."),
    ("03", "PASSION FOR PERFECTION", "No shortcuts. Every stage is approached with care and precision."),
    ("04", "TAILORED SOLUTIONS", "Every vehicle and client receives the appropriate treatment for their requirements."),
]
why_html = "".join(
    f"""
    <div class="pd-why-item">
        <span class="num">{num}</span>
        <h3>{title}</h3>
        <p>{desc}</p>
    </div>
    """
    for num, title, desc in why_items
)
st.markdown(
    f"""
    <div class="pd-section pd-section-alt">
        <div class="pd-why-grid">
            {why_html}
        
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div id="about" class="pd-section">
        <div class="pd-split">
            <div class="pd-about-imgs pd-fade">
                <div style="background-image:var(--img-workshop);"></div>
                <div style="background-image:var(--img-detailer);"></div>
            </div>
            <div class="pd-split-text pd-fade">
                <span class="pd-label">ABOUT US</span>
                <h2>PASSION. PRECISION.<br>PURE DETAILING.</h2>
                <p class="pd-muted">Pure Detailing UK is built around a simple principle: every
                vehicle deserves careful, considered attention. We use premium products and
                proven techniques, tailoring each service to the individual car and the client's
                requirements — with no shortcuts along the way.</p>
                <h2 style="font-size:1.8rem; margin-top:30px;">CARE WITHOUT<br>SHORTCUTS.</h2>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

process_items = [
    ("01", "ENQUIRE", "Tell us about your vehicle and what you need."),
    ("02", "CONSULT", "We discuss the right treatment and solution."),
    ("03", "TRANSFORM", "Our specialists carry out the service with precision."),
    ("04", "ENJOY", "Drive away with a vehicle that looks and feels exceptional."),
]
process_html = "".join(
    f"""
    <div class="pd-process-item">
        <span class="num">{num}</span>
        <h3>{title}</h3>
        <p>{desc}</p>
    </div>
    """
    for num, title, desc in process_items
)
st.markdown(
    f"""
    <div class="pd-section pd-section-alt">
        <div class="pd-services-head">
            <span class="pd-label">HOW IT WORKS</span>
            <h2>OUR PROCESS.</h2>
        </div>
        <div class="pd-process-grid">
            {process_html}
        
    </div>
    """,
    unsafe_allow_html=True,
)

demo_reviews = [
    ("The ceramic coating result was fantastic — the finish looked incredible.", "— Demo Client"),
    ("Booked a maintenance wash and the attention to detail was excellent.", "— Demo Client"),
    ("Professional from start to finish, would recommend to anyone in the area.", "— Demo Client"),
]
reviews_html = "".join(
    f"""
    <article class="pd-review-card">
        <span class="pd-review-tag">DEMO REVIEW</span>
        <p>"{quote}"</p>
        <span class="pd-review-name">{name}</span>
    </article>
    """
    for quote, name in demo_reviews
)
st.markdown(
    f"""
    <section id="reviews" class="pd-section">
        <div class="pd-services-head">
            <span class="pd-label">CLIENT FEEDBACK</span>
            <h2>WHAT CLIENTS SAY.</h2>
        </div>
        <p class="pd-muted" style="max-width:620px; margin-bottom:40px;">
            The reviews below are placeholder demo content for this preview and can be replaced
            with real Google reviews or client testimonials before launch.
        </p>
        <div class="pd-review-grid">
            {reviews_html}
    
    </section>
    """,
    unsafe_allow_html=True,
)

contact_left, contact_right = st.columns([1, 1], gap="large")

with contact_left:
    st.markdown(
        f"""
        <section id="contact" class="pd-contact-panel">
            <span class="pd-label">GET IN TOUCH</span>
            <h2>READY TO<br>TRANSFORM<br>YOUR CAR?</h2>
            <div style="margin-top:40px;">
                <div class="pd-contact-item">
                    <span class="lbl">PHONE / WHATSAPP</span>
                    <span class="val">{PHONE_DISPLAY}</span>
                </div>
                <div class="pd-contact-item">
                    <span class="lbl">EMAIL</span>
                    <span class="val">{EMAIL}</span>
                </div>
                <div class="pd-contact-item">
                    <span class="lbl">OPENING HOURS</span>
                    <span class="val">{HOURS_LINE1}<br>{HOURS_LINE2}</span>
                </div>
                <a href="{WHATSAPP_URL}" target="_blank" class="pd-wa-btn">WHATSAPP US</a>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

with contact_right:
    with st.form("booking_form", clear_on_submit=False):
        st.markdown('<span class="pd-label">REQUEST A QUOTE</span>', unsafe_allow_html=True)
        full_name = st.text_input("Full Name")
        c1, c2 = st.columns(2)
        with c1:
            email_input = st.text_input("Email Address")
        with c2:
            phone_input = st.text_input("Phone Number")
        vehicle = st.text_input("Vehicle Make & Model")
        service = st.selectbox("Select Service", SERVICE_OPTIONS)
        preferred_date = st.date_input("Preferred Date")
        message = st.text_area("Message", height=110)
        submitted = st.form_submit_button("REQUEST A QUOTE")

        if submitted:
            errors = []
            if not full_name.strip():
                errors.append("Full Name is required.")
            if not email_input.strip() or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_input.strip()):
                errors.append("A valid Email Address is required.")
            if not phone_input.strip():
                errors.append("Phone Number is required.")
            if not vehicle.strip():
                errors.append("Vehicle Make & Model is required.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.success(
                    "Thank you — your enquiry has been received. "
                    "Our team will be in touch shortly to confirm the details."
                )

st.markdown(
    f"""
    <div class="pd-footer">
        <div class="pd-footer-top">
            <div>
                <div class="pd-footer-logo"><span>PURE</span> DETAILING <b>UK</b></div>
                <div class="pd-footer-tag">Premium Automotive Care</div>
            </div>
            <div class="pd-footer-links">
                <a href="#home">HOME</a>
                <a href="#services">SERVICES</a>
                <a href="#work">OUR WORK</a>
                <a href="#about">ABOUT</a>
                <a href="#reviews">REVIEWS</a>
                <a href="#contact">CONTACT</a>
            </div>
        </div>
        <div class="pd-footer-bottom">
            <span>\u00a9 2026 {BRAND_NAME}. All Rights Reserved.</span>
            <span>Website designed and developed by {DEVELOPER_CREDIT}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)