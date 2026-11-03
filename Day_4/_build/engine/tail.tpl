<div id="notesPanel"></div>
<div id="blank"></div>
<div id="help"><div>
  <b style="font-size:22px">Keyboard shortcuts</b><br>
  <kbd>→</kbd><kbd>Space</kbd> Next step / slide<br>
  <kbd>←</kbd> Previous<br>
  <kbd>Home</kbd><kbd>End</kbd> First / last slide<br>
  <kbd>F</kbd> Fullscreen<br>
  <kbd>T</kbd> Light / dark theme<br>
  <kbd>P</kbd> Presenter window (notes, next slide, timer)<br>
  <kbd>N</kbd> Show notes on this screen<br>
  <kbd>B</kbd> Black screen (pause)<br>
  <kbd>K</kbd> Check that every slide fits the screen<br>
  <kbd>?</kbd> Toggle this help
</div></div>

<script>
const deck=document.getElementById('deck');
const slides=[...document.querySelectorAll('.slide')];
const root=document.documentElement;
let cur=0, pw=null, t0=null;

// theme
root.dataset.theme=localStorage.getItem('{{THEME_KEY}}')||'{{DEFAULT_THEME}}';

function fit(){const s=Math.min(innerWidth/1600,innerHeight/900);deck.style.transform=`translate(-50%,-50%) scale(${s})`;}
addEventListener('resize',fit);fit();

const frags=s=>[...s.querySelectorAll('.f')];
const titleOf=s=>(s.querySelector('h1,h2,.quote,.statement')||{}).textContent?.trim().replace(/\s+/g,' ')||'';

function go(i,allOn=false){
  i=Math.max(0,Math.min(slides.length-1,i));
  slides[cur].classList.remove('active');
  cur=i;
  frags(slides[cur]).forEach(f=>f.classList.toggle('on',allOn));
  slides[cur].classList.add('active');
  history.replaceState(null,'','#'+(cur+1));
  render();
}
function next(){
  const hidden=frags(slides[cur]).filter(f=>!f.classList.contains('on'));
  if(hidden.length){hidden[0].classList.add('on');render();}
  else if(cur<slides.length-1) go(cur+1);
}
function prev(){
  const on=frags(slides[cur]).filter(f=>f.classList.contains('on'));
  if(on.length){on[on.length-1].classList.remove('on');render();}
  else if(cur>0) go(cur-1,true);
}
function render(){
  document.getElementById('progress').style.width=((cur+1)/slides.length*100)+'%';
  document.getElementById('num').textContent=`${cur+1} / ${slides.length}`;
  document.getElementById('sec').textContent='{{LABEL}} · '+(slides[cur].dataset.section||'');
  const n=slides[cur].querySelector('.notes');
  document.getElementById('notesPanel').innerHTML=`<b>Slide ${cur+1}: ${titleOf(slides[cur])}</b><br>${n?n.innerHTML:'(no notes)'}`;
  syncPresenter();
}

// presenter window
function openPresenter(){
  pw=window.open('','deckPresenter','width=1200,height=760');
  if(!pw){alert('Please allow pop-ups to open the presenter view.');return;}
  const css=document.querySelector('style').textContent;
  pw.document.open();
  pw.document.write(`<!DOCTYPE html><html data-theme="${root.dataset.theme}"><head><title>Presenter · {{LABEL}}</title><style>${css}
  html,body{overflow:auto;background:#0c0e13;color:#eef0f5}
  .pv{display:grid;grid-template-columns:1.25fr 1fr;grid-template-rows:auto 1fr;gap:20px;padding:20px;height:100vh;box-sizing:border-box}
  .box2{background:#151922;border-radius:16px;padding:16px;overflow:hidden}
  .lab{font:700 13px -apple-system,sans-serif;letter-spacing:2px;text-transform:uppercase;color:#5aa9ff;margin-bottom:10px}
  .mini{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:10px}
  .mini .stage{position:absolute;left:0;top:0;width:1600px;height:900px;transform-origin:0 0;background:var(--bg);color:var(--text)}
  .mini .slide{display:flex!important;animation:none}
  #pnotes{font:20px/1.6 -apple-system,sans-serif;grid-column:1/3;overflow:auto}
  #pnotes b{color:#5aa9ff}
  .top{display:flex;justify-content:space-between;align-items:center;font:600 22px -apple-system,sans-serif}
  #ptimer{font:800 40px Menlo,monospace;color:#4fd1a1}
  button{background:#2a3142;color:#fff;border:0;border-radius:10px;padding:10px 18px;font-size:16px;margin-left:8px;cursor:pointer}
  </style></head><body><div class="pv">
   <div class="box2"><div class="top"><span class="lab">Now · <span id="pnum"></span></span><span><button id="bp">◀ Prev</button><button id="bn">Next ▶</button></span></div><div class="mini"><div class="stage" id="pcur"></div></div></div>
   <div class="box2"><div class="top"><span class="lab">Next</span><span id="ptimer">00:00</span></div><div class="mini"><div class="stage" id="pnext"></div></div><button id="br" style="margin:12px 0 0">Reset timer</button></div>
   <div class="box2" id="pnotes"></div>
  </div></body></html>`);
  pw.document.close();
  t0=Date.now();
  pw.document.addEventListener('keydown',onKey);
  pw.document.getElementById('bn').onclick=()=>next();
  pw.document.getElementById('bp').onclick=()=>prev();
  pw.document.getElementById('br').onclick=()=>{t0=Date.now();};
  pw.addEventListener('resize',syncPresenter);
  syncPresenter();
}
function syncPresenter(){
  if(!pw||pw.closed) return;
  const d=pw.document; d.documentElement.dataset.theme=root.dataset.theme;
  const put=(id,s)=>{const st=d.getElementById(id); if(!st) return; st.innerHTML=''; if(!s){st.innerHTML='<div style="padding:60px;font-size:60px">End of deck</div>';} else {const c=s.cloneNode(true);c.classList.add('active');st.appendChild(c);} const w=st.parentElement.clientWidth; st.style.transform=`scale(${w/1600})`;};
  put('pcur',slides[cur]);
  const nx=slides[cur+1]?slides[cur+1].cloneNode(true):null; if(nx) nx.querySelectorAll('.f').forEach(f=>f.classList.add('on'));
  put('pnext',nx);
  const remaining=frags(slides[cur]).filter(f=>!f.classList.contains('on')).length;
  d.getElementById('pnum').textContent=`Slide ${cur+1} / ${slides.length}${remaining?` · ${remaining} step(s) left`:''}`;
  const n=slides[cur].querySelector('.notes');
  d.getElementById('pnotes').innerHTML=`<div class="lab">Speaker notes</div><b>${titleOf(slides[cur])}</b><br>${n?n.innerHTML:'(no notes)'}`;
}
setInterval(()=>{if(pw&&!pw.closed&&t0){const s=Math.floor((Date.now()-t0)/1000);pw.document.getElementById('ptimer').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}},1000);

function onKey(e){
  const k=e.key;
  if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].includes(k)){e.preventDefault();next();}
  else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(k)){e.preventDefault();prev();}
  else if(k==='Home') go(0);
  else if(k==='End') go(slides.length-1,true);
  else if(k==='f'||k==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}
  else if(k==='t'||k==='T'){root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localStorage.setItem('{{THEME_KEY}}',root.dataset.theme);syncPresenter();}
  else if(k==='n'||k==='N'){const p=document.getElementById('notesPanel');p.style.display=p.style.display==='block'?'none':'block';}
  else if(k==='p'||k==='P') openPresenter();
  else if(k==='b'||k==='B'||k==='.'){const b=document.getElementById('blank');b.style.display=b.style.display==='block'?'none':'block';}
  else if(k==='k'||k==='K') checkFit();
  else if(k==='?'){const h=document.getElementById('help');h.style.display=h.style.display==='flex'?'none':'flex';}
  else if(k==='Escape'){document.getElementById('help').style.display='none';document.getElementById('blank').style.display='none';}
}
document.addEventListener('keydown',onKey);
deck.addEventListener('click',e=>{if(e.target.closest('a,button'))return; (e.clientX<innerWidth*0.25)?prev():next();});
let tx=null;
addEventListener('touchstart',e=>tx=e.touches[0].clientX);
addEventListener('touchend',e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)(dx<0?next:prev)();tx=null;});


function checkFit(){
  const keep=cur, rep=[]; const dr=deck.getBoundingClientRect(), sc=dr.width/1600;
  slides.forEach((s,i)=>{
    slides.forEach(x=>x.classList.remove('active'));
    s.style.animation='none'; s.classList.add('active');
    frags(s).forEach(f=>{f.style.transition='none';f.classList.add('on');});
    let mb=0, mr=0;
    s.querySelectorAll('*').forEach(e=>{
      if(e.closest('.notes,.shell,.hint,.termtag')||getComputedStyle(e).position==='absolute') return;
      const r=e.getBoundingClientRect(); if(!r.width||!r.height) return;
      mb=Math.max(mb,(r.bottom-dr.top)/sc); mr=Math.max(mr,(r.right-dr.left)/sc);
    });
    if(mb>835||mr>1500) rep.push('Slide '+(i+1)+': bottom '+Math.round(mb)+'px, right '+Math.round(mr)+'px');
    s.style.animation=''; frags(s).forEach(f=>{f.style.transition='';});
  });
  go(keep);
  alert(rep.length?('These slides run past the safe area (limit: bottom 835, right 1500):\n\n'+rep.join('\n')):'All '+slides.length+' slides fit.');
}

const start=parseInt(location.hash.slice(1));
slides[0].classList.add('active');
go(isNaN(start)?0:start-1);
</script>
</body>
</html>
