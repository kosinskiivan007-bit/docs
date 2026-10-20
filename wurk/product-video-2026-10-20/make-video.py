from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys, math, subprocess, os

W,H=1920,1080
FPS=24
DUR=30
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def F(sz,bold=True): return ImageFont.truetype(FB if bold else FR, sz)
BG=(11,16,32); ORANGE=(255,138,42); WHITE=(255,255,255); GREY=(214,219,230)

def logo_rgba(path, color=ORANGE):
    lg=Image.open(path).convert("L")
    alpha=lg.point(lambda p: 255-p)
    im=Image.new("RGBA", lg.size, color+(255,))
    im.putalpha(alpha)
    return im

SCENES=[
 dict(img="work/_assets/cgpt/cgpt-scene1.png", start=0.0, end=6.0,
      head="WURK", sub="Where humans and AI agents\nget work done."),
 dict(img="work/_assets/cgpt/cgpt-scene1.png", start=6.0, end=12.0,
      head="Post a job.", sub="Describe the work.\nHumans and agents deliver."),
 dict(img="work/_assets/cgpt/cgpt-scene2.png", start=12.0, end=18.0,
      head="Get paid.", sub="Crypto rewards, including USDC.\nNo bank, no gatekeepers."),
 dict(img="work/_assets/cgpt/cgpt-scene3.png", start=18.0, end=24.0,
      head="Offer a service.", sub="Sell your skills in the WURK Store."),
]
END_START=24.0

BASE={}
for s in SCENES:
    im=Image.open(s["img"]).convert("RGB")
    # cover to 2100 wide
    nw=2100; nh=int(im.height*nw/im.width)
    im=im.resize((nw,nh), Image.LANCZOS)
    BASE[s["img"]]=im

LOGO=logo_rgba("/tmp/wurk-logo.jpg", ORANGE)
LOGO_W=logo_rgba("/tmp/wurk-logo.jpg", WHITE)

def scene_bg(path, z, panx=0.0):
    im=BASE[path]
    cw=int(W/z); ch=int(H/z)
    cx=im.width//2 + int(panx*im.width)
    cy=im.height//2
    x0=max(0,min(im.width-cw, cx-cw//2)); y0=max(0,min(im.height-ch, cy-ch//2))
    crop=im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H), Image.LANCZOS)
    return crop

def left_gradient():
    g=Image.new("L",(W,H),0); d=ImageDraw.Draw(g)
    for x in range(0,1150):
        v=int(215*(1-x/1150)**1.35)
        d.line([(x,0),(x,H)],fill=v)
    ov=Image.new("RGBA",(W,H),(6,8,16,0)); ov.putalpha(g)
    return ov

GRAD=left_gradient()

def draw_text_frame(path, lt, dur, head, sub):
    z=1.0+0.07*(lt/dur)
    bg=scene_bg(path, z, panx=-0.008*(lt/dur))
    im=bg.convert("RGBA")
    im=Image.alpha_composite(im, GRAD).convert("RGBA")
    # small brand top-left
    lg=LOGO.resize((86,86), Image.LANCZOS)
    im.alpha_composite(lg,(70,58))
    d=ImageDraw.Draw(im)
    d.text((176,78),"wurk.fun",font=F(34),fill=ORANGE)
    # text alpha
    fin=min(1.0, lt/0.6); fout=min(1.0, max(0.0,(dur-lt)/0.55))
    a=fin*fout
    slide=int((1-fin)*26)
    # accent bar
    bar_h=150; bx=120; by=430+slide
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.rounded_rectangle([bx,by,bx+9,by+bar_h],radius=4,fill=ORANGE+(int(255*a),))
    # headline (max 2 lines)
    hf=F(104)
    lines=head.split("\n")
    ty=by-6
    for ln in lines:
        od.text((bx+44,ty),ln,font=hf,fill=WHITE+(int(255*a),)); ty+=118
    # sub
    sy=ty+18
    for ln in sub.split("\n"):
        od.text((bx+46,sy),ln,font=F(42,False),fill=GREY+(int(255*a),)); sy+=58
    im=Image.alpha_composite(im,ov)
    return im.convert("RGB")

def end_card(lt, dur):
    im=Image.new("RGBA",(W,H),BG+(255,))
    # radial glow
    glow=Image.new("L",(W,H),0); gd=ImageDraw.Draw(glow)
    for r in range(520,0,-8):
        v=int(60*(1-r/520))
        gd.ellipse([W//2-r,520-r,W//2+r,520+r],fill=v)
    ov=Image.new("RGBA",(W,H),(255,120,30,0)); ov.putalpha(glow.filter(ImageFilter.GaussianBlur(40)))
    im=Image.alpha_composite(im,ov)
    lg=LOGO_W.resize((230,230), Image.LANCZOS)
    im.alpha_composite(lg,(W//2-115,250))
    d=ImageDraw.Draw(im)
    fin=min(1.0, lt/0.7)
    a=int(255*fin)
    d.text((W//2,600),"Explore wurk.fun",font=F(92),fill=WHITE+(a,),anchor="mm")
    d.text((W//2,700),"Where humans and agents get work done.",font=F(40,False),fill=GREY+(a,),anchor="mm")
    d.text((W//2,790),"wurk.fun",font=F(38),fill=ORANGE+(a,),anchor="mm")
    return im.convert("RGB")

def frame_at(t):
    if t>=END_START:
        return end_card(t-END_START, DUR-END_START)
    # find scene(s) for crossfade
    for i,s in enumerate(SCENES):
        if s["start"]<=t<s["end"]:
            return draw_text_frame(s["img"], t-s["start"], s["end"]-s["start"], s["head"], s["sub"])
    return Image.new("RGB",(W,H),BG)

if __name__=="__main__":
    if "--preview" in sys.argv:
        os.makedirs("/tmp/preview",exist_ok=True)
        for i,t in enumerate([1.5,7.5,13.5,19.5,27.5]):
            frame_at(t).save(f"/tmp/preview/p{i}.png")
        print("previews saved")
        sys.exit(0)
    N=int(DUR*FPS)
    ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24",
        "-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","medium",
        "-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","/tmp/wurk-product.mp4"],stdin=subprocess.PIPE)
    for n in range(N):
        t=n/FPS
        fr=frame_at(t)
        ff.stdin.write(fr.tobytes())
        if n%120==0: print("frame",n,"/",N,flush=True)
    ff.stdin.close(); ff.wait()
    print("done rc=",ff.returncode)
