from PIL import Image, ImageDraw, ImageFilter
import math, sys, subprocess, os

W,H=1920,1080; FPS=24; T=20.0; N=int(T*FPS); SS=2
BG=(11,16,32); ORANGE=(255,138,42); TEAL=(70,211,196); WHITE=(240,244,252); DIM=(51,64,94); GOLD=(255,209,102)

def sc(v): return v*SS
def ellipse(d,cx,cy,r,**kw): d.ellipse([sc(cx-r),sc(cy-r),sc(cx+r),sc(cy+r)],**kw)
def line(d,pts,fill,width): d.line([(sc(x),sc(y)) for x,y in pts],fill=fill,width=int(sc(width)))

def gear(d,cx,cy,r,teeth,angle,color,hole=None,tl=None,tw=None):
    tl=tl or r*0.22; tw=tw or max(6,r*0.16)
    for i in range(teeth):
        a=angle+2*math.pi*i/teeth
        px,py=cx+math.cos(a)*(r+tl*0.35),cy+math.sin(a)*(r+tl*0.35)
        # tooth as rotated rectangle
        ca,sa=math.cos(a),math.sin(a)
        w2,h2=tw/2,tl/2
        pts=[]
        for dx,dy in [(-w2,-h2),(w2,-h2),(w2,h2),(-w2,h2)]:
            pts.append((px+dx*ca-dy*sa, py+dx*sa+dy*ca))
        d.polygon([(sc(x),sc(y)) for x,y in pts],fill=color)
    ellipse(d,cx,cy,r,fill=color)
    h=hole if hole is not None else r*0.30
    ellipse(d,cx,cy,h,fill=BG)
    ellipse(d,cx,cy,h*0.55,fill=color)

def frame_at(t):
    im=Image.new("RGB",(W*SS,H*SS),BG); d=ImageDraw.Draw(im,"RGBA")
    # radial glow
    gl=Image.new("L",(W*SS,H*SS),0); gd=ImageDraw.Draw(gl)
    for rr in range(sc(600),0,-sc(8)):
        v=int(46*(1-rr/sc(600)))
        gd.ellipse([sc(1260)-rr,sc(540)-rr,sc(1260)+rr,sc(540)+rr],fill=v)
    ov=Image.new("RGBA",(W*SS,H*SS),(255,120,30,0)); ov.putalpha(gl.filter(ImageFilter.GaussianBlur(sc(30))))
    im=Image.alpha_composite(im.convert("RGBA"),ov); d=ImageDraw.Draw(im,"RGBA")
    # faint grid
    for gx in range(0,W,80): d.line([(sc(gx),0),(sc(gx),H*SS)],fill=(255,255,255,8),width=1)
    for gy in range(0,H,80): d.line([(0,sc(gy)),(W*SS,sc(gy))],fill=(255,255,255,8),width=1)
    ph=2*math.pi*t/T
    cx,cy=1260,540
    # ring track
    ellipse(d,cx,cy,340,outline=(60,76,112,255),width=int(sc(10)))
    ellipse(d,cx,cy,318,outline=(35,45,70,255),width=int(sc(3)))
    # gears (periodic)
    gear(d,cx,cy,250,26,ph,ORANGE,hole=70)
    gear(d,cx-400,cy-90,150,16,-(250/150)*ph+0.3,TEAL,hole=42)
    gear(d,cx-251,cy+251,105,11,-(250/105)*ph+1.1,WHITE,hole=30)
    # balls on ring (3, evenly spaced)
    for k in range(3):
        a=ph+2*math.pi*k/3
        bx,by=cx+math.cos(a)*340,cy+math.sin(a)*340
        # trail
        for j in range(1,8):
            aa=a-0.03*j
            tx,ty=cx+math.cos(aa)*340,cy+math.sin(aa)*340
            ellipse(d,tx,ty,11-1.2*j,fill=(255,209,102,int(70*(1-j/8))))
        ellipse(d,bx,by,18,fill=GOLD); ellipse(d,bx-5,by-5,5,fill=(255,255,255,180))
    # pendulum (left)
    px,py=420,250; L=360; ang=0.55*math.sin(ph)
    ex,ey=px+L*math.sin(ang),py+L*math.cos(ang)
    line(d,[(px,py),(ex,ey)],(150,165,195,255),7)
    ellipse(d,px,py,16,fill=WHITE)
    ellipse(d,ex,ey,38,fill=TEAL); ellipse(d,ex-10,ey-10,10,fill=(255,255,255,160))
    # piston (left-bottom) - 2 cycles
    pist=60*math.sin(2*ph)
    line(d,[(760,960),(760,760+pist)],(120,135,165,255),34)
    ellipse(d,760,720+pist,34,fill=ORANGE); ellipse(d,760,720+pist,14,fill=BG)
    # small sparkles at ring
    for k in range(6):
        a=ph*2+2*math.pi*k/6; sx,sy=cx+math.cos(a)*400,cy+math.sin(a)*400
        ellipse(d,sx,sy,3+(2 if k%2 else 0),fill=(255,255,255,120))
    # vignette
    vg=Image.new("L",(W*SS,H*SS),0); vd=ImageDraw.Draw(vg)
    vd.ellipse([-sc(200),-sc(200),W*SS+sc(200),H*SS+sc(200)],fill=255)
    vg=vg.filter(ImageFilter.GaussianBlur(sc(120)))
    dark=Image.new("RGBA",(W*SS,H*SS),(0,0,0,0)); dark.putalpha(Image.eval(vg,lambda v:0 if v>128 else int((128-v)*0.9)))
    im=Image.alpha_composite(im,dark)
    out=im.convert("RGB").resize((W,H),Image.LANCZOS)
    dd=ImageDraw.Draw(out)
    dd.text((W-40,H-34),"wurk.fun",font=None,fill=(120,132,160),anchor="rs")
    return out

if __name__=="__main__":
    if "--preview" in sys.argv:
        os.makedirs("/tmp/mprev",exist_ok=True)
        for i,t in enumerate([0,4,8,12,16]):
            frame_at(t).save(f"/tmp/mprev/m{i}.png")
        print("ok"); sys.exit(0)
    ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","/tmp/wurk-machine.mp4"],stdin=subprocess.PIPE)
    for n in range(N):
        ff.stdin.write(frame_at(n/FPS).tobytes())
        if n%120==0: print("frame",n,flush=True)
    ff.stdin.close(); ff.wait(); print("done",ff.returncode)
