"""
Multiverso Comic - Motion Graphic CTA Overlay Generator
Renderiza la animación HTML5 Canvas a video MOV transparente (QuickTime Animation / ProRes 4444)
con escala prudente (0.52x) y posicionamiento en la zona segura (Y=1420 en canvas 1080x1920).
"""

import http.server
import socketserver
import threading
import subprocess
import os
import shutil
import base64
import urllib.parse
from pathlib import Path

PORT = 8768
ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
FRAMES_DIR = ROOT_DIR / "temp_motion_cta_frames"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/fontsource/css/bangers@latest/index.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/fontsource/css/inter@latest/700.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/fontsource/css/inter@latest/800.css">
<style>
  * { margin: 0; padding: 0; }
  body { background: transparent; overflow: hidden; }
  canvas { display: block; }
</style>
</head>
<body>
<canvas id="cv" width="1080" height="1920"></canvas>
<script>
const cv  = document.getElementById('cv');
const ctx = cv.getContext('2d');
const DUR = 6000;

const clamp01 = p => p<0 ? 0 : p>1 ? 1 : p;
const seg = (t,a,b) => clamp01((t-a)/(b-a));
const eo  = p => 1-Math.pow(1-p,3);
const back = p => { const c=2.2; return 1 + (c+1)*Math.pow(p-1,3) + c*Math.pow(p-1,2); };

const TIKTOK_D = "M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z";
const FB_D = "M13.6 22v-8.1h2.72l.41-3.16H13.6V8.72c0-.91.25-1.53 1.56-1.53h1.66V4.36c-.29-.04-1.27-.12-2.42-.12-2.4 0-4.04 1.46-4.04 4.15v2.35H7.63v3.16h2.73V22z";
const pTiktok = new Path2D(TIKTOK_D);
const pFb     = new Path2D(FB_D);

let handleTxt = '@multiversocomic';

function star(c, cx, cy, spikes, R, r, rot){
  c.beginPath();
  for(let i=0;i<spikes*2;i++){
    const rad = (i%2===0)? R : r;
    const a = rot + i*Math.PI/spikes;
    const x = cx + Math.cos(a)*rad, y = cy + Math.sin(a)*rad;
    i===0 ? c.moveTo(x,y) : c.lineTo(x,y);
  }
  c.closePath();
}
function rr(c,x,y,w,h,r){
  c.beginPath();
  c.moveTo(x+r,y);
  c.arcTo(x+w,y,x+w,y+h,r);
  c.arcTo(x+w,y+h,x,y+h,r);
  c.arcTo(x,y+h,x,y,r);
  c.arcTo(x,y,x+w,y,r);
  c.closePath();
}
function comicText(c, txt, x, y, size, font, fill, strokeW, shadowCol, ox, oy){
  c.font = size + 'px ' + font;
  c.textAlign='center'; c.textBaseline='middle';
  c.lineJoin='round'; c.miterLimit=2;
  if(shadowCol){ c.fillStyle=shadowCol; c.fillText(txt, x+ox, y+oy); }
  c.lineWidth = strokeW; c.strokeStyle='#010101';
  c.strokeText(txt, x, y);
  c.fillStyle = fill; c.fillText(txt, x, y);
}

function draw(t){
  const W=cv.width, H=cv.height;
  ctx.clearRect(0,0,W,H);

  const PRUDENT_SCALE = 0.52;
  const TARGET_X = W / 2;
  const TARGET_Y = 1420;

  const u = (Math.min(W,H)/1080) * PRUDENT_SCALE;

  let shX=0, shY=0;
  const w1 = seg(t,850,1150), w2 = seg(t,1150,1450);
  if(w1>0 && w1<1){ const a=14*u*(1-w1); shX=Math.sin(t*1.3)*a; shY=Math.cos(t*1.1)*a; }
  if(w2>0 && w2<1){ const a=9*u*(1-w2);  shX+=Math.sin(t*1.7)*a; shY+=Math.cos(t*1.4)*a; }

  let rot=0, mScale=1, ty=0;
  if(t>3600 && t<5400){ rot = Math.sin(t*0.004)*0.012; ty = Math.sin(t*0.002)*6*u; }
  const po = seg(t,5400,6000);
  if(po>0){ mScale = 1 - eo(po); rot += 0.35*eo(po); }

  ctx.save();
  ctx.translate(TARGET_X + shX, TARGET_Y + shY + ty);
  ctx.rotate(rot);
  ctx.scale(mScale, mScale);

  /* ---- explosión comic ---- */
  const bIn = back(seg(t,0,500));
  if(bIn>0){
    ctx.save();
    ctx.scale(bIn,bIn);
    ctx.rotate(t*0.00012);
    star(ctx,0,0,14,345*u,215*u, -0.2);
    ctx.fillStyle='#ffd400'; ctx.fill();
    ctx.lineWidth=12*u; ctx.lineJoin='round'; ctx.strokeStyle='#010101'; ctx.stroke();
    ctx.clip();
    ctx.fillStyle='rgba(214,41,118,.45)';
    const sp=30*u, off=(t*0.02)%sp;
    for(let yy=-360*u; yy<360*u; yy+=sp){
      for(let xx=-360*u; xx<360*u; xx+=sp){
        ctx.beginPath(); ctx.arc(xx+off, yy+off*0.5, 5*u, 0, 7); ctx.fill();
      }
    }
    ctx.restore();
  }

  /* ---- anillo de impacto ---- */
  const rp = seg(t,900,1450);
  if(rp>0 && rp<1){
    ctx.save(); ctx.globalAlpha=1-rp;
    ctx.beginPath(); ctx.arc(0,0,(200+340*eo(rp))*u,0,7);
    ctx.lineWidth=14*u*(1-rp)+2; ctx.strokeStyle='#ffffff'; ctx.stroke();
    ctx.restore();
  }

  /* ---- líneas de velocidad ---- */
  const sp2 = seg(t,1000,1650);
  if(sp2>0 && sp2<1){
    ctx.save(); ctx.globalAlpha=(1-sp2)*0.9;
    ctx.strokeStyle='#010101'; ctx.lineWidth=6*u; ctx.lineCap='round';
    for(let i=0;i<24;i++){
      const a=i*Math.PI/12 + 0.13;
      const r0=(380+120*eo(sp2))*u, r1=(500+160*eo(sp2))*u;
      ctx.beginPath();
      ctx.moveTo(Math.cos(a)*r0, Math.sin(a)*r0);
      ctx.lineTo(Math.cos(a)*r1, Math.sin(a)*r1);
      ctx.stroke();
    }
    ctx.restore();
  }

  /* ---- títulos ---- */
  const t1 = seg(t,350,850);
  if(t1>0){
    const s = 1 + (1-eo(t1))*1.9;
    ctx.save(); ctx.translate(0,-62*u); ctx.scale(s,s); ctx.rotate(-0.06*(1-eo(t1)));
    comicText(ctx,'MULTIVERSO',0,0,112*u,'"Bangers",cursive','#ffffff',16*u,'#7b2ff7',10*u,10*u);
    ctx.restore();
  }
  const t2 = seg(t,650,1150);
  if(t2>0){
    const s = 1 + (1-eo(t2))*2.2;
    ctx.save(); ctx.translate(0,82*u); ctx.scale(s,s); ctx.rotate(0.07*(1-eo(t2)));
    comicText(ctx,'COMIC',0,0,148*u,'"Bangers",cursive','#ffd400',18*u,'#d62976',11*u,11*u);
    ctx.restore();
  }

  /* ---- burbuja de diálogo con usuario ---- */
  const bb = back(seg(t,1500,2100));
  if(bb>0){
    ctx.save();
    ctx.translate(272*u,-332*u); ctx.scale(bb,bb);
    ctx.font='800 46px "Inter",sans-serif';
    const tw = ctx.measureText(handleTxt).width;
    const bw = tw+90*u, bh=96*u;
    ctx.beginPath();
    ctx.moveTo(-bw*0.28, bh*0.4);
    ctx.lineTo(-bw*0.05, bh*0.4);
    ctx.lineTo(-bw*0.55, bh*0.4+95*u);
    ctx.closePath();
    ctx.fillStyle='#ffffff'; ctx.fill();
    ctx.lineWidth=8*u; ctx.lineJoin='round'; ctx.strokeStyle='#010101'; ctx.stroke();
    rr(ctx,-bw/2,-bh/2,bw,bh,30*u);
    ctx.fillStyle='#ffffff'; ctx.fill();
    ctx.lineWidth=8*u; ctx.strokeStyle='#010101'; ctx.stroke();
    rr(ctx,-bw/2+6*u,-bh/2+6*u,bw-12*u,bh-12*u,24*u);
    ctx.fillStyle='#ffffff'; ctx.fill();
    ctx.fillStyle='#010101'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.font='800 46px "Inter",sans-serif';
    ctx.fillText(handleTxt,0,3*u);
    ctx.restore();
  }

  /* ---- cinta CTA ---- */
  const cb = back(seg(t,3000,3600));
  if(cb>0){
    ctx.save();
    ctx.translate(0,268*u); ctx.rotate(-0.05); ctx.scale(cb,cb);
    ctx.font='50px "Bangers",cursive';
    const ctaTxt='¡SÍGUENOS EN TODAS LAS REDES!';
    const tw=ctx.measureText(ctaTxt).width;
    const RW=tw+130*u, RH=92*u;
    ctx.fillStyle='#b02a37'; ctx.strokeStyle='#010101'; ctx.lineWidth=8*u; ctx.lineJoin='round';
    ctx.beginPath();
    ctx.moveTo(-RW/2+8*u,-RH/2-16*u); ctx.lineTo(-RW/2-48*u,-RH/2-16*u);
    ctx.lineTo(-RW/2-28*u,0); ctx.lineTo(-RW/2-48*u,RH/2+16*u); ctx.lineTo(-RW/2+8*u,RH/2+16*u);
    ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(RW/2-8*u,-RH/2-16*u); ctx.lineTo(RW/2+48*u,-RH/2-16*u);
    ctx.lineTo(RW/2+28*u,0); ctx.lineTo(RW/2+48*u,RH/2+16*u); ctx.lineTo(RW/2-8*u,RH/2+16*u);
    ctx.closePath(); ctx.fill(); ctx.stroke();
    rr(ctx,-RW/2,-RH/2,RW,RH,14*u);
    ctx.fillStyle='#e63946'; ctx.fill(); ctx.lineWidth=9*u; ctx.strokeStyle='#010101'; ctx.stroke();
    comicText(ctx,ctaTxt,0,4*u,50*u,'"Bangers",cursive','#ffffff',0,null,0,0);
    ctx.restore();
  }

  /* ---- iconos de redes ---- */
  const icons=[
    {c:'#ff0000', k:'yt'},
    {c:'#010101', k:'tt'},
    {c:'ig',      k:'ig'},
    {c:'#1877f2', k:'fb'}
  ];
  icons.forEach((ic,i)=>{
    const bx=(-225+i*150)*u, by=408*u, r=56*u;
    const st = back(seg(t,2150+i*150,2500+i*150));
    const pp = back(seg(t,2250+i*150,2650+i*150));
    if(st>0){
      ctx.save(); ctx.translate(bx,by); ctx.scale(st,st); ctx.rotate(0.3*(1-st));
      star(ctx,0,0,8,r*1.5,r*0.85,0.2);
      ctx.fillStyle= i%2 ? '#25f4ee' : '#ffd400'; ctx.fill();
      ctx.lineWidth=7*u; ctx.lineJoin='round'; ctx.strokeStyle='#010101'; ctx.stroke();
      ctx.restore();
    }
    if(pp>0){
      ctx.save(); ctx.translate(bx,by); ctx.scale(pp,pp);
      ctx.beginPath(); ctx.arc(0,0,r,0,7);
      if(ic.c==='ig'){
        const g=ctx.createLinearGradient(-r,-r,r,r);
        g.addColorStop(0,'#feda75'); g.addColorStop(.5,'#d62976'); g.addColorStop(1,'#4c5fd7');
        ctx.fillStyle=g;
      } else ctx.fillStyle=ic.c;
      ctx.fill();
      ctx.lineWidth=7*u; ctx.strokeStyle='#010101'; ctx.stroke();
      if(ic.k==='yt'){
        ctx.fillStyle='#ffffff'; rr(ctx,-r*0.66,-r*0.46,r*1.32,r*0.92,r*0.2); ctx.fill();
        ctx.fillStyle='#ff0000';
        ctx.beginPath();
        ctx.moveTo(-r*0.18,-r*0.26); ctx.lineTo(-r*0.18,r*0.26); ctx.lineTo(r*0.34,0);
        ctx.closePath(); ctx.fill();
      } else if(ic.k==='tt'){
        const s=r*1.25/24;
        const drawTT=(ox,oy,col)=>{ ctx.save(); ctx.translate(ox-r*0.6,oy-r*0.6); ctx.scale(s,s); ctx.fillStyle=col; ctx.fill(pTiktok); ctx.restore(); };
        drawTT(-3*u,-2*u,'#25f4ee'); drawTT(3*u,3*u,'#fe2c55'); drawTT(0,0,'#ffffff');
      } else if(ic.k==='ig'){
        ctx.strokeStyle='#ffffff'; ctx.lineWidth=r*0.16;
        rr(ctx,-r*0.6,-r*0.6,r*1.2,r*1.2,r*0.34); ctx.stroke();
        ctx.beginPath(); ctx.arc(0,0,r*0.32,0,7); ctx.stroke();
        ctx.fillStyle='#ffffff'; ctx.beginPath(); ctx.arc(r*0.38,-r*0.38,r*0.1,0,7); ctx.fill();
      } else {
        const s=r*1.35/24;
        ctx.save(); ctx.translate(-r*0.68,-r*0.68); ctx.scale(s,s);
        ctx.fillStyle='#ffffff'; ctx.fill(pFb); ctx.restore();
      }
      ctx.restore();
    }
  });

  /* ---- estrellas "pow" parpadeantes ---- */
  if(t>3600 && t<5400){
    const bl1=Math.abs(Math.sin(t*0.012)), bl2=Math.abs(Math.cos(t*0.012));
    ctx.save(); ctx.translate(-430*u,-290*u); ctx.scale(0.5+0.6*bl1,0.5+0.6*bl1); ctx.rotate(bl1);
    star(ctx,0,0,7,60*u,30*u,0); ctx.fillStyle='#25f4ee'; ctx.fill();
    ctx.lineWidth=7*u; ctx.strokeStyle='#010101'; ctx.stroke(); ctx.restore();
    ctx.save(); ctx.translate(438*u,-250*u); ctx.scale(0.5+0.6*bl2,0.5+0.6*bl2); ctx.rotate(-bl2);
    star(ctx,0,0,7,55*u,27*u,0); ctx.fillStyle='#d62976'; ctx.fill();
    ctx.lineWidth=7*u; ctx.strokeStyle='#010101'; ctx.stroke(); ctx.restore();
  }

  ctx.restore();
}

async function startBatchRender() {
  await Promise.all([
    document.fonts.load('100px "Bangers"'),
    document.fonts.load('800 46px "Inter"'),
    document.fonts.ready
  ]);

  const FPS = 30;
  const TOTAL_FRAMES = 180;
  
  for (let f = 0; f < TOTAL_FRAMES; f++) {
    const t = (f / FPS) * 1000;
    draw(t);
    const dataUrl = cv.toDataURL('image/png');
    await fetch('/frame?idx=' + f, { method: 'POST', body: dataUrl });
  }
  await fetch('/done', { method: 'POST' });
}

window.onload = () => {
  setTimeout(startBatchRender, 300);
};
</script>
</body>
</html>
"""

class FrameHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/render"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        if self.path.startswith("/frame"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            idx = int(params.get("idx", [0])[0])
            b64_data = post_data.split(",", 1)[1] if "," in post_data else post_data
            img_bytes = base64.b64decode(b64_data)
            
            frame_path = FRAMES_DIR / f"frame_{idx:04d}.png"
            with open(frame_path, "wb") as f:
                f.write(img_bytes)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        elif self.path == "/done":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"done")
            threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        pass

def generate_motion_cta():
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True)

    server = socketserver.TCPServer(("127.0.0.1", PORT), FrameHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f"[Motion CTA] Server iniciado en http://127.0.0.1:{PORT}")

    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "google-chrome",
        "chromium-browser"
    ]
    chrome_bin = next((c for c in chrome_candidates if shutil.which(c) or os.path.exists(c)), None)
    if not chrome_bin:
        raise RuntimeError("No se encontró Chrome o Edge para renderizar el motion graphic.")

    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--window-size=1080,1920",
        f"http://127.0.0.1:{PORT}/"
    ]
    print(f"[Motion CTA] Renderizando fotogramas con {chrome_bin}...")
    p = subprocess.Popen(cmd)
    
    server_thread.join(timeout=120)
    p.kill()
    server.server_close()
    
    num_frames = len(list(FRAMES_DIR.glob("frame_*.png")))
    print(f"[Motion CTA] Fotogramas renderizados: {num_frames}/180")

    if num_frames == 180:
        output_mov = ASSETS_DIR / "vertical_cta_multiversocomic_motion.mov"
        print(f"[Motion CTA] Codificando a QuickTime Animation transparente: {output_mov}...")
        cmd_ff = [
            "ffmpeg", "-y",
            "-framerate", "30",
            "-i", str(FRAMES_DIR / "frame_%04d.png"),
            "-c:v", "qtrle",
            str(output_mov)
        ]
        subprocess.run(cmd_ff, check=True)
        shutil.rmtree(FRAMES_DIR, ignore_errors=True)
        print(f"[Motion CTA] ¡Overlay generado con éxito! -> {output_mov} ({output_mov.stat().st_size // 1024} KB)")
        return str(output_mov)
    else:
        raise RuntimeError(f"Error renderizando overlay: solo se generaron {num_frames} de 180 fotogramas.")

if __name__ == "__main__":
    generate_motion_cta()
