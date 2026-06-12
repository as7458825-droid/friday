import os
import tempfile


def generate(art_type: str = "particles") -> str:
    if art_type == "particles":
        html = _particle_html()
    elif art_type == "fractal":
        html = _fractal_html()
    elif art_type == "flow":
        html = _flow_field_html()
    else:
        html = _particle_html()
    path = os.path.join(tempfile.gettempdir(), f"friday_art_{art_type}.html")
    with open(path, "w") as f:
        f.write(html)
    os.startfile(path)
    return f"Art generated: {art_type}. Open the HTML file."


def _particle_html() -> str:
    return """<!DOCTYPE html><html><body><canvas id='c'></canvas><script>
const c=document.getElementById('c'),ctx=c.getContext('2d');
c.width=innerWidth;c.height=innerHeight;
const p=Array.from({length:200},()=>({x:Math.random()*c.width,y:Math.random()*c.height,vx:(Math.random()-0.5)*2,vy:(Math.random()-0.5)*2}));
function draw(){ctx.fillStyle='rgba(0,0,0,0.1)';ctx.fillRect(0,0,c.width,c.height);
p.forEach(q=>{q.x+=q.vx;q.y+=q.vy;if(q.x<0||q.x>c.width)q.vx*=-1;if(q.y<0||q.y>c.height)q.vy*=-1;
ctx.fillStyle='#00ff88';ctx.beginPath();ctx.arc(q.x,q.y,3,0,Math.PI*2);ctx.fill();});
requestAnimationFrame(draw);}draw();</script></body></html>"""


def _fractal_html() -> str:
    return """<!DOCTYPE html><html><body><canvas id='c'></canvas><script>
const c=document.getElementById('c'),ctx=c.getContext('2d');
c.width=innerWidth;c.height=innerHeight;
function draw(iter){for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++){
let a=(x-c.width/2)*4/c.width,b=(y-c.height/2)*4/c.height,r=a,i=b,n=0;
while(r*r+i*i<4&&n<iter){let t=r*r-i*i+a;i=2*r*i+b;r=t;n++;}
ctx.fillStyle=n===iter?'#000':`hsl(${n*10},100%,50%)`;ctx.fillRect(x,y,1,1);}}
draw(50);</script></body></html>"""


def _flow_field_html() -> str:
    return """<!DOCTYPE html><html><body><canvas id='c'></canvas><script>
const c=document.getElementById('c'),ctx=c.getContext('2d');
c.width=innerWidth;c.height=innerHeight;
const p=Array.from({length:500},()=>({x:Math.random()*c.width,y:Math.random()*c.height}));
function draw(){ctx.fillStyle='rgba(0,0,0,0.05)';ctx.fillRect(0,0,c.width,c.height);
p.forEach(q=>{const a=Math.sin(q.x*0.01)*Math.cos(q.y*0.01)*4;
q.x+=Math.cos(a);q.y+=Math.sin(a);
if(q.x<0||q.x>c.width||q.y<0||q.y>c.height){q.x=Math.random()*c.width;q.y=Math.random()*c.height;}
ctx.fillStyle='#00ff88';ctx.beginPath();ctx.arc(q.x,q.y,1,0,Math.PI*2);ctx.fill();});
requestAnimationFrame(draw);}draw();</script></body></html>"""


def list_types() -> str:
    return "Types: particles, fractal, flow"
