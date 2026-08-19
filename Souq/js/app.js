/* ============================================================
   موسوعة السوق — منطق التطبيق (PWA يعمل بدون إنترنت)
   يعرض كل فصول الموسوعة + قاعدة العبارات + النظرة العامة.
   ============================================================ */
(function(){
  'use strict';

  const $ = (s,el=document)=>el.querySelector(s);
  const $$ = (s,el=document)=>Array.from(el.querySelectorAll(s));
  const esc = s => String(s==null?'':s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const store = {
    get(k,d){ try{const v=localStorage.getItem(k); return v==null?d:JSON.parse(v);}catch(e){return d;} },
    set(k,v){ try{localStorage.setItem(k,JSON.stringify(v));}catch(e){} }
  };

  if(!window.matchMedia){ window.matchMedia = function(q){ return {matches:false,media:q,addListener(){},removeListener(){},addEventListener(){},removeEventListener(){},dispatchEvent(){return false;}}; }; }
  if(!window.scrollTo){ window.scrollTo = function(){}; }

  let currentRoute='home';
  let theme = store.get('souq_theme','light');
  let favorites = store.get('souq_favs',[]);
  let activeFunc='';
  let currentMlLang='';
  let currentMlQuery='';
  let currentDlgId='';
  let currentDlgLang='ar';
  let currentDlgRole='all';
  let currentSearchQ='';

  /* ---------- شاشة البداية ---------- */
  window.addEventListener('load', ()=>{
    const seen=store.get('souq_seen', false);
    const wait=seen?0:800;
    setTimeout(()=>{
      const sp=$('#splash');
      if(sp){ sp.classList.add('hide'); setTimeout(()=>{ sp.hidden=true; }, seen?0:400); }
      store.set('souq_seen', true);
      init();
    }, wait);
  });

  function init(){
    applyTheme();
    buildNav();
    buildBottomNav();
    bindEvents();
    registerSW();
    $('#appHeader').hidden=false;
    $('#content').hidden=false;
    $('#bottomNav').hidden=false;
    if(window.matchMedia('(min-width:900px)').matches){ $('#drawer').hidden=false; }
    if(window.speechSynthesis){ try{ speechSynthesis.getVoices(); speechSynthesis.addEventListener('voiceschanged', function(){}); }catch(e){} }
    route();
  }

  function applyTheme(){ document.documentElement.setAttribute('data-theme', theme); }

  /* ============================================================
     محرّك الماركدون (عربي) — يعرض كل المحتوى كما هو
     ============================================================ */
  const C0='\u0000';

  function plainSpeak(s){
    return String(s==null?'':s).replace(/[*_`#>]+/g,' ').replace(/\s+/g,' ').trim();
  }
  function isSpeakable(text){
    const tx=plainSpeak(text);
    if(tx.length<2 || tx.length>280) return false;
    if(/^[-–—\d\s.,:;!?/%()«»"']+$/.test(tx)) return false;
    return /[\u0600-\u06FFa-zA-Z\u0400-\u04FF]/.test(tx);
  }
  function guessLang(text, fallback){
    const tx=String(text||'');
    const ar=/[\u0600-\u06FF]/.test(tx);
    const cyr=/[\u0400-\u04FF]/.test(tx);
    const trc=/[çğıöşüÇĞİÖŞÜ]/.test(tx);
    const frc=/[àâäéèêëïîôùûüçœæÀÂÄÉÈÊËÏÎÔÙÛÜÇ]/.test(tx);
    const lat=/[A-Za-z]/.test(tx);
    if(cyr) return 'tg';
    if(trc) return 'tr';
    if(frc && !trc) return 'fr';
    if(ar && !lat && !cyr) return 'ar';
    if(lat) return (fallback && fallback!=='ar' && fallback!=='all') ? fallback : 'en';
    return fallback || 'ar';
  }
  function sayWrap(text, lang, innerHtml){
    const tx=plainSpeak(text);
    if(!isSpeakable(tx)) return innerHtml!=null?innerHtml:esc(String(text||''));
    return '<span class="say">'+speakBtn(tx, lang)+'<span class="say-txt" dir="auto">'+(innerHtml!=null?innerHtml:esc(tx))+'</span></span>';
  }
  function sayMany(text, lang){
    const raw=String(text||'').trim();
    const parts=raw.split(/\s*[·•]+|\s+\/\s+/).map(s=>s.trim()).filter(Boolean);
    if(parts.length>1 && parts.length<14 && parts.every(p=>p.length<48)){
      return parts.map(p=>sayWrap(p, lang)).join('<span class="say-sep"> · </span>');
    }
    return sayWrap(raw, lang);
  }
  function listenItem(raw, lang){
    const inner=inline(raw, lang);
    if(inner.indexOf('data-speak')>=0) return inner;
    const plain=plainSpeak(raw);
    if(isSpeakable(plain) && plain.length<=160) return sayWrap(plain, lang, inner);
    return inner;
  }

  function inline(raw, lang){
    const codes=[], links=[];
    let t = String(raw==null?'':raw);
    t = t.replace(/`([^`]+)`/g, (m,c)=>{ codes.push(c); return C0+'C'+(codes.length-1)+C0; });
    t = t.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m,txt,url)=>{ links.push([txt,url]); return C0+'L'+(links.length-1)+C0; });
    t = esc(t);
    t = t.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    t = t.replace(/<strong>([^<]+)<\/strong>/g, (m,x)=>{
      const plain=x.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
      if(isSpeakable(plain) && (guessLang(plain,lang)!=='ar' || plain.length<=90))
        return sayWrap(plain, lang, '<strong>'+x+'</strong>');
      return m;
    });
    t = t.replace(new RegExp(C0+'C(\\d+)'+C0,'g'), (m,n)=> '<code>'+sayMany(codes[+n], lang)+'</code>');
    t = t.replace(new RegExp(C0+'L(\\d+)'+C0,'g'), (m,n)=>{ const x=links[+n]; return '<a href="'+esc(x[1])+'" target="_blank" rel="noopener">'+esc(x[0])+'</a>'; });
    return t;
  }

  function renderTable(rows, lang){
    const cells = row => row.replace(/^\|/,'').replace(/\|$/,'').split('|').map(c=>c.trim());
    const header = cells(rows[0]);
    const body = rows.slice(2).map(r=>cells(r));
    const labels = header.map(h=>h.replace(/\*\*/g,'').trim());
    let html='<div class="table-wrap"><table><thead><tr>'+header.map(h=>'<th>'+inline(h)+'</th>').join('')+'</tr></thead><tbody>';
    body.forEach(r=>{
      html+='<tr>';
      labels.forEach((lab,i)=>{ html+='<td data-label="'+esc(lab)+'">'+listenItem(r[i]||'', lang)+'</td>'; });
      html+='</tr>';
    });
    html+='</tbody></table></div>';
    return html;
  }

  function mdRender(md, lang){
    const lines = String(md==null?'':md).replace(/\r\n/g,'\n').split('\n');
    let html='', i=0, secOpen=false;
    const closeSec=()=>{ if(secOpen){ html+='</section>'; secOpen=false; } };
    const isBlank = l=>/^\s*$/.test(l);
    const isH = l=>/^#{1,6}\s+/.test(l);
    const isHR = l=>/^---+\s*$/.test(l) || /^\*\*\*+\s*$/.test(l);
    const isQuote = l=>/^>\s?/.test(l);
    const isTable = l=>/^\|/.test(l);
    const isUL = l=>/^\s*[-*]\s+/.test(l);
    const isOL = l=>/^\s*\d+\.\s+/.test(l);
    const blockStart = l=> isBlank(l)||isH(l)||isHR(l)||isQuote(l)||isTable(l)||isUL(l)||isOL(l);

    while(i<lines.length){
      while(i<lines.length && isBlank(lines[i])) i++;
      if(i>=lines.length) break;
      let line=lines[i];
      let h=line.match(/^(#{1,6})\s+(.*)$/);
      if(h){
        const lvl=h[1].length; const txt=h[2].trim();
        if(lvl===2){ closeSec(); html+='<section class="md-sec">'; secOpen=true; }
        html+='<h'+lvl+' id="h'+i+'">'+inline(txt, lang)+'</h'+lvl+'>'; i++; continue;
      }
      if(isHR(line)){ html+='<hr>'; i++; continue; }
      if(isQuote(line)){
        let buf=[];
        while(i<lines.length && isQuote(lines[i])){ buf.push(lines[i].replace(/^>\s?/,'')); i++; }
        html+='<blockquote>'+mdRender(buf.join('\n'), lang)+'</blockquote>';
        continue;
      }
      if(isTable(line) && i+1<lines.length && /^\|[\s:|-]*\|?\s*$/.test(lines[i+1]) && lines[i+1].includes('-')){
        let tbuf=[];
        while(i<lines.length && isTable(lines[i])){ tbuf.push(lines[i]); i++; }
        html+=renderTable(tbuf, lang);
        continue;
      }
      if(isUL(line)){
        let items=[];
        while(i<lines.length){
          if(isUL(lines[i])){ items.push(lines[i].replace(/^\s*[-*]\s+/,'')); i++; }
          else if(!blockStart(lines[i])){ items[items.length-1]+=' '+lines[i].trim(); i++; }
          else break;
        }
        html+='<ul>'+items.map(li=>'<li>'+listenItem(li, lang)+'</li>').join('')+'</ul>';
        continue;
      }
      if(isOL(line)){
        let items=[];
        while(i<lines.length){
          if(isOL(lines[i])){ items.push(lines[i].replace(/^\s*\d+\.\s+/,'')); i++; }
          else if(!blockStart(lines[i])){ items[items.length-1]+=' '+lines[i].trim(); i++; }
          else break;
        }
        html+='<ol>'+items.map(li=>'<li>'+listenItem(li, lang)+'</li>').join('')+'</ol>';
        continue;
      }
      let buf=[];
      while(i<lines.length && !blockStart(lines[i])){ buf.push(lines[i]); i++; }
      html+='<p>'+listenItem(buf.join(' '), lang)+'</p>';
    }
    closeSec();
    return html;
  }

  function mdToc(md){
    const lines=String(md==null?'':md).replace(/\r\n/g,'\n').split('\n');
    let items=[];
    lines.forEach((l,idx)=>{
      const m=l.match(/^##\s+(.*)$/);
      if(m) items.push({id:'h'+idx, text:m[1].replace(/\*\*/g,'').trim()});
    });
    return items;
  }

  /* ============================================================
     القائمة الجانبية
     ============================================================ */
  function buildNav(){
    const list=$('#navList');
    let html='';
    html+=navItem('home','🏠','الرئيسية','c-teal');
    html+='<li class="nav-label">الأقسام</li>';
    CHAPTERS.forEach(c=>{
      html+='<li><button class="nav-item" data-route="'+c.id+'"><span class="ni-num">'+c.num+'</span><span>'+esc(c.label)+'</span></button></li>';
    });
    html+='<li class="nav-label">استكشاف</li>';
    html+=navItem('phrases','🔎','قاعدة العبارات','c-blue');
    html+=navItem('functions','🗂️','التصنيف الوظيفي','c-teal');
    html+=navItem('search','🔍','بحث شامل','c-purple');
    html+='<li class="nav-label">🌐 لغات متعددة</li>';
    html+=navItem('languages','🌐','بوابة اللغات','c-teal');
    ML_LANGS.forEach(l=>{
      const d=ML_DOCS.find(x=>x.lang===l.code && x.role==='main');
      if(d) html+='<li><button class="nav-item" data-route="'+d.id+'"><span class="ni-num '+l.color+'" style="color:#fff">'+l.flag+'</span><span>'+esc(l.name)+'</span></button></li>';
    });
    html+=navItem('mlphrases','🔎','عبارات متعددة اللغات','c-blue');
    html+=navItem('mlcompare','🔁','مقارنة الوظائف','c-purple');
    html+=navItem('mldialogues','💬','حوارات تفاعلية','c-rose');
    html+=navItem('ml-05-muqarana','📊','جداول المقارنة','c-slate');
    html+=navItem('ml-07-hiwarat','📄','نص الحوارات','c-slate');
    html+=navItem('ml-00-manhaj','🧭','المنهج','c-slate');
    html+=navItem('about','ℹ️','عن الموسوعة','c-teal');
    html+=navItem('favorites','⭐','المفضلة','c-amber');
    list.innerHTML=html;
    list.addEventListener('click', e=>{
      const btn=e.target.closest('.nav-item'); if(!btn) return;
      navigate(btn.dataset.route);
      closeDrawer();
    });
  }
  function navItem(id,icon,title,color){
    return '<li><button class="nav-item" data-route="'+id+'"><span class="ni-num '+color+'" style="color:#fff">'+icon+'</span><span>'+title+'</span></button></li>';
  }

  function buildBottomNav(){
    $$('.nav-tab').forEach(b=>b.addEventListener('click',()=>navigate(b.dataset.route)));
  }

  function bindEvents(){
    $('#menuBtn').addEventListener('click', openDrawer);
    $('#drawerOverlay').addEventListener('click', closeDrawer);
    $('#toTop').addEventListener('click', ()=>window.scrollTo({top:0,behavior:'smooth'}));
    window.addEventListener('scroll', ()=>{ $('#toTop').hidden = window.scrollY < 400; });

    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', e=>{
      e.preventDefault(); deferredPrompt=e;
      const ib=$('#installBtn'); ib.hidden=false;
      ib.addEventListener('click', async()=>{
        ib.hidden=true; deferredPrompt.prompt();
        await deferredPrompt.userChoice; deferredPrompt=null;
      },{once:true});
    });
    window.addEventListener('appinstalled', ()=>{ $('#installBtn').hidden=true; toast('تم تثبيت التطبيق بنجاح ✅'); });

    $('#resetFavs').addEventListener('click',()=>{
      if(confirm('مسح كل العبارات المحفوظة في المفضلة؟')){
        favorites=[]; store.set('souq_favs',[]); toast('تم مسح المفضلة');
        if(currentRoute==='favorites') render('favorites');
      }
    });
    $('#exportData')?.addEventListener('click', ()=>{
      const dataStr=JSON.stringify({favs:favorites});
      const blob=new Blob([dataStr],{type:'application/json'});
      const url=URL.createObjectURL(blob);
      const a=document.createElement('a'); a.href=url; a.download='souq-favorites.json'; a.click();
      URL.revokeObjectURL(url); toast('تم التصدير 📁'); closeDrawer();
    });

    $('#searchBtn')?.addEventListener('click', ()=>navigate('search'));
    $('#themeBtn')?.addEventListener('click', ()=>{
      theme = theme==='dark'?'light':'dark'; store.set('souq_theme',theme); applyTheme();
    });

    let textSizes=['normal','text-lg','text-sm'];
    let currSizeIdx=store.get('souq_text_size',0);
    const applyTextSize=()=>{ document.body.classList.remove('text-lg','text-sm'); if(textSizes[currSizeIdx]!=='normal') document.body.classList.add(textSizes[currSizeIdx]); };
    applyTextSize();
    $('#textSizeBtn')?.addEventListener('click', ()=>{
      currSizeIdx=(currSizeIdx+1)%textSizes.length; store.set('souq_text_size',currSizeIdx); applyTextSize();
      toast(currSizeIdx===0?'حجم الخط: عادي':currSizeIdx===1?'حجم الخط: كبير':'حجم الخط: صغير');
    });

    window.addEventListener('hashchange', route);
  }

  function openDrawer(){
    $('#drawer').hidden=false;
    requestAnimationFrame(()=>{ $('#drawer').classList.add('show'); $('#drawerOverlay').hidden=false; requestAnimationFrame(()=>$('#drawerOverlay').classList.add('show')); });
  }
  function closeDrawer(){
    if(window.matchMedia('(min-width:900px)').matches) return;
    $('#drawer').classList.remove('show');
    const ov=$('#drawerOverlay'); ov.classList.remove('show');
    setTimeout(()=>{ $('#drawer').hidden=true; ov.hidden=true; },320);
  }

  function navigate(route){ currentRoute=route; location.hash=route; }

  /* ============================================================
     التوجيه (Routing)
     ============================================================ */
  const ROUTES=['home','chapters','phrases','about','favorites','functions','search','languages','mlphrases','mlcompare','mldialogues'].concat(CHAPTERS.map(c=>c.id), ML_DOCS.map(d=>d.id));
  const isChapter = id => CHAPTERS.some(c=>c.id===id);

  function route(){
    const parts=(location.hash||'#home').slice(1).split('?');
    let clean=parts[0]||'home';
    const params=new URLSearchParams(parts[1]||'');
    currentRoute = ROUTES.includes(clean)?clean:'home';
    activeFunc = currentRoute==='phrases' ? (params.get('func')||'') : '';
    currentMlLang = currentRoute==='mlphrases' ? (params.get('lang')||'') : '';
    currentMlQuery = currentRoute==='mlphrases' ? (params.get('q')||'') : '';
    currentDlgId = currentRoute==='mldialogues' ? (params.get('id')||'') : '';
    currentDlgLang = currentRoute==='mldialogues' ? (params.get('lang')||currentDlgLang||'ar') : currentDlgLang;
    updateActiveNav();
    render(currentRoute);
    window.scrollTo({top:0});
    if(window.matchMedia('(max-width:899px)').matches) closeDrawer();
  }

  function updateActiveNav(){
    $$('.nav-item').forEach(b=>b.classList.toggle('active', b.dataset.route===currentRoute));
    const isMl = currentRoute==='languages'||currentRoute==='mlphrases'||currentRoute==='mlcompare'||currentRoute==='mldialogues'||String(currentRoute).indexOf('ml-')===0;
    let tab = currentRoute==='phrases'?'phrases':(currentRoute==='chapters'||isChapter(currentRoute))?'chapters':isMl?'languages':'home';
    $$('.nav-tab').forEach(b=>b.classList.toggle('active', b.dataset.route===tab));
    const map={home:SOUQ_META.appName, chapters:'أقسام الموسوعة', phrases:'قاعدة العبارات', about:'عن الموسوعة', favorites:'المفضلة', functions:'التصنيف الوظيفي', search:'البحث الشامل', languages:'بوابة اللغات', mlphrases:'عبارات متعددة اللغات', mlcompare:'مقارنة الوظائف', mldialogues:'حوارات تفاعلية'};
    let title=map[currentRoute];
    if(!title){ const ch=CHAPTERS.find(c=>c.id===currentRoute); title=ch?ch.label:SOUQ_META.appName; }
    if(!title){ const doc=ML_DOCS.find(d=>d.id===currentRoute); title=doc?doc.title:SOUQ_META.appName; }
    $('#sectionTitle').textContent=title;
  }

  function render(route){
    const c=$('#content');
    const map={home:renderHome, chapters:renderChapters, phrases:renderPhrases, about:renderAbout, favorites:renderFavorites, functions:renderFunctions, search:renderSearch, languages:renderLanguages, mlphrases:renderMlPhrases, mlcompare:renderMlCompare, mldialogues:renderDialogues};
    if(isChapter(route)){ c.innerHTML=renderChapter(route); }
    else if(ML_DOCS.some(d=>d.id===route)){ c.innerHTML=renderMlDoc(route); }
    else { c.innerHTML=(map[route]||renderHome)(); }
    if(route==='phrases') bindPhrases();
    if(route==='search') bindSearch();
    if(route==='home') bindHome();
    if(route==='mlphrases') bindMlPhrases();
    if(route==='mlcompare') bindMlCompare();
    if(route==='mldialogues') bindDialogues();
    bindReading();
  }

  /* ============================================================
     الشاشات
     ============================================================ */
  function chaptersGrid(){
    const tiles=CHAPTERS.map(c=>
      '<button class="section-tile" data-go="'+c.id+'">'+
        '<span class="ic '+c.color+'">'+c.icon+'</span>'+
        '<span class="t">'+esc(c.label)+'</span>'+
        '<span class="n">القسم '+c.num+'</span>'+
      '</button>').join('');
    return '<div class="section-grid">'+tiles+'</div>';
  }

  function renderHome(){
    const m=SOUQ_META;
    const gates=[
      {id:'chapters', ic:'📘', t:'الموسوعة العربية', n:m.chaptersCount+' قسماً و'+m.phrasesCount+' عبارة — جذب، تفاوض، لهجات'},
      {id:'languages', ic:'🌐', t:'لغات السوق', n:'تركية · إندونيسية · طاجيكية · فرنسية · إنجليزية — '+m.mlPhrasesCount+' عبارة'},
      {id:'search', ic:'🔍', t:'ابحث', n:'في الأقسام والعبارات والحوارات معاً'}
    ];
    const gateHtml=gates.map(g=>
      '<button class="gate" data-go="'+g.id+'"><span class="gate-ic">'+g.ic+'</span><span class="gate-t">'+esc(g.t)+'</span><span class="gate-n">'+esc(g.n)+'</span></button>'
    ).join('');
    const chips=[
      {id:'phrases', t:'عبارات عربية'},
      {id:'mldialogues', t:'حوارات'},
      {id:'mlcompare', t:'مقارنة'},
      {id:'favorites', t:'المفضلة'}
    ].map(c=>'<button class="chip" data-go="'+c.id+'">'+esc(c.t)+'</button>').join('');
    return ''+
      '<section class="hero">'+
        '<h1>'+esc(m.appName)+'</h1>'+
        '<p>كيف يتكلم بائع وزبون حقيقيان — بالعربية وخمس لغات.</p>'+
      '</section>'+
      '<div class="search-box home-search">'+
        '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M15.5 14h-.8l-.3-.3a6.5 6.5 0 10-.7.7l.3.3v.8l5 5 1.5-1.5-5-5zm-6 0A4.5 4.5 0 1114 9.5 4.5 4.5 0 019.5 14z"/></svg>'+
        '<input id="homeSearch" type="search" placeholder="ابحث: غالي، Hoş geldiniz، تفاوض...">'+
      '</div>'+
      '<div class="gate-list">'+gateHtml+'</div>'+
      '<div class="chip-row">'+chips+'</div>';
  }

  function bindHome(){
    const hs=$('#homeSearch'); if(!hs) return;
    hs.addEventListener('keydown', e=>{
      if(e.key!=='Enter') return;
      const q=hs.value.trim();
      navigate('search'+(q?('?q='+encodeURIComponent(q)):''));
    });
  }

  function renderChapters(){
    return '<div class="sec-intro">'+esc(SOUQ_META.appName)+' — '+esc(SOUQ_META.subtitle)+'. تصفّح '+SOUQ_META.chaptersCount+' قسماً منظّماً يغطي كل جوانب لغة السوق الحية.</div>'+chaptersGrid();
  }

  function renderChapter(id){
    const c=CHAPTERS.find(x=>x.id===id);
    if(!c) return renderHome();
    const toc=mdToc(c.raw);
    const tocHtml = toc.length>1 ? '<nav class="toc" aria-label="محتويات القسم"><div class="toc-title">📑 محتويات القسم</div>'+toc.map(t=>'<a data-anchor="'+t.id+'"><span class="dot"></span>'+esc(t.text)+'</a>').join('')+'</nav>' : '';
    const idx=CHAPTERS.findIndex(x=>x.id===id);
    const prev=idx>0?CHAPTERS[idx-1]:null;
    const next=idx<CHAPTERS.length-1?CHAPTERS[idx+1]:null;
    const nav='<div class="filter-row" style="margin-top:18px">'+(prev?'<button class="btn-primary ghost" data-go="'+prev.id+'" style="flex:1">→ '+esc(prev.label)+'</button>':'<span style="flex:1"></span>')+(next?'<button class="btn-primary ghost" data-go="'+next.id+'" style="flex:1">'+esc(next.label)+' ←</button>':'<span style="flex:1"></span>')+'</div>';
    return ''+
      '<div class="chapter-head">'+
        '<div style="display:flex;align-items:center">'+
          '<span class="ch-num">'+c.icon+'</span>'+
          '<div><h1>'+esc(c.title)+'</h1><p>القسم '+c.num+' من '+SOUQ_META.chaptersCount+'</p></div>'+
        '</div>'+
      '</div>'+
      '<div class="reading">'+
        tocHtml+
        '<div class="md-body">'+mdRender(c.raw, 'ar')+'</div>'+
      '</div>'+
      nav;
  }

  function renderAbout(){
    const a=ABOUT, m=SOUQ_META;
    return ''+
      '<div class="chapter-head"><div style="display:flex;align-items:center"><span class="ch-num">ℹ️</span><div><h1>'+esc(a.title)+'</h1><p>نظرة عامة ومنهجية الموسوعة</p></div></div></div>'+
      '<div class="about-card"><div class="about-meta">'+
        '<span class="badge gold">'+m.chaptersCount+' قسم</span>'+
        '<span class="badge teal">'+m.phrasesCount+' عبارة</span>'+
        '<span class="badge blue">'+m.countriesCount+' دولة/منطقة</span>'+
        '<span class="badge purple">'+m.dialectsCount+' لهجة</span>'+
        '<span class="badge rose">'+m.situationsCount+' موقف</span>'+
      '</div></div>'+
      mdRender(a.raw, 'ar');
  }

  /* ---------- قاعدة العبارات ---------- */
  function moreFold(inner, label){
    const html=String(inner||'');
    if(!html.trim()) return '';
    return '<details class="more"><summary>'+esc(label||'التفاصيل')+'</summary><div class="more-body">'+html+'</div></details>';
  }

  function phraseCard(p){
    const isFav=favorites.includes(p.id);
    const b=(t,cls)=> t?'<span class="badge '+(cls||'')+'">'+esc(t)+'</span>':'';
    const extra=
      '<div class="phrase-meta">'+
        b(p.func,'teal')+b(p.country,'gold')+b(p.dialect,'teal')+b(p.situation,'blue')+b(p.addressee,'purple')+b(p.formality)+b(p.familiarity)+b(p.frequency,'rose')+b(p.humor)+
      '</div>'+
      (p.notes?'<div class="phrase-notes"><b>ملاحظات:</b> '+esc(p.notes)+'</div>':'')+
      equivalentsBox(p.phrase, p.msa);
    return '<div class="phrase-card" data-pid="'+esc(p.id)+'">'+
      '<button class="fav-star '+(isFav?'on':'')+'" data-pid="'+esc(p.id)+'" aria-label="مفضلة">'+(isFav?'★':'☆')+'</button>'+
      '<div class="say say-block">'+speakBtn(p.phrase,'ar')+'<div class="phrase-main">«'+esc(p.phrase)+'»</div></div>'+
      (p.msa?'<div class="phrase-msa">'+esc(p.msa)+'</div>':'')+
      moreFold(extra, 'متى وأين تُقال')+
    '</div>';
  }

  function renderPhrases(){
    const m=SOUQ_META;
    const opt=arr=>'<option value="">الكل</option>'+arr.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join('');
      return funcBanner()+
      '<div class="sec-intro">قاعدة بيانات فيها <b>'+m.phrasesCount+'</b> عبارة وجملة من أسواق العربية، مع ترجمتها الفصحى ودولتها ولهجتها وموقفها. ابحث وصفِّ وفقاً لحاجتك.</div>'+
      '<div class="filter-bar">'+
        '<div class="search-box" style="margin-bottom:0">'+
          '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M15.5 14h-.8l-.3-.3a6.5 6.5 0 10-.7.7l.3.3v.8l5 5 1.5-1.5-5-5zm-6 0A4.5 4.5 0 1114 9.5 4.5 4.5 0 019.5 14z"/></svg>'+
          '<input id="phSearch" type="search" placeholder="ابحث في العبارات (العبارة، الفصحى، الملاحظات...)">'+
        '</div>'+
        '<div class="filter-row">'+
          '<select id="fCountry" class="filter-select">'+opt(m.countries)+'</select>'+
          '<select id="fDialect" class="filter-select">'+opt(m.dialects)+'</select>'+
          '<select id="fSituation" class="filter-select">'+opt(m.situations)+'</select>'+
          '<select id="fAddressee" class="filter-select">'+opt(m.addressees)+'</select>'+
        '</div>'+
        '<div class="filter-row">'+
          '<button id="fClear" class="btn-primary ghost" style="flex:0 0 auto;padding:10px 18px">مسح الفلاتر</button>'+
        '</div>'+
      '</div>'+
      '<div id="phCount" class="result-count"></div>'+
      '<div id="phResults"></div>';
  }

  function getFilteredPhrases(){
    const q=$('#phSearch')?$('#phSearch').value.trim().toLowerCase():'';
    const c=$('#fCountry')?$('#fCountry').value:'';
    const d=$('#fDialect')?$('#fDialect').value:'';
    const s=$('#fSituation')?$('#fSituation').value:'';
    const a=$('#fAddressee')?$('#fAddressee').value:'';
    return PHRASES.filter(p=>{
      if(activeFunc && p.func!==activeFunc) return false;
      if(c && p.country!==c) return false;
      if(d && p.dialect!==d) return false;
      if(s && p.situation!==s) return false;
      if(a && p.addressee!==a) return false;
      if(q){
        const hay=(p.phrase+' '+p.msa+' '+p.notes+' '+p.country+' '+p.dialect+' '+p.situation+' '+p.addressee).toLowerCase();
        if(!hay.includes(q)) return false;
      }
      return true;
    });
  }

  function renderPhrasesResults(){
    const list=getFilteredPhrases();
    const cnt=$('#phCount'); if(cnt) cnt.innerHTML=list.length+' نتيجة';
    const box=$('#phResults'); if(!box) return;
    if(!list.length){ box.innerHTML='<p style="text-align:center;color:var(--text-mute);padding:24px">لا توجد نتائج مطابقة.</p>'; return; }
    box.innerHTML=list.map(phraseCard).join('');
  }

  function bindPhrases(){
    ['#phSearch','#fCountry','#fDialect','#fSituation','#fAddressee'].forEach(sel=>{
      const el=$(sel); if(!el) return;
      el.addEventListener('input', renderPhrasesResults);
      if(sel!=='#phSearch') el.addEventListener('change', renderPhrasesResults);
    });
    const clr=$('#fClear'); if(clr) clr.addEventListener('click',()=>{
      if($('#phSearch'))$('#phSearch').value='';
      ['#fCountry','#fDialect','#fSituation','#fAddressee'].forEach(s=>{const e=$(s);if(e)e.value='';});
      renderPhrasesResults();
    });
    renderPhrasesResults();
  }

  function funcBanner(){
    if(!activeFunc) return '';
    const f=FUNCTIONS.find(x=>x.code===activeFunc);
    if(!f) return '';
    return '<div class="box tip" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'+
      '<div><span class="bt">عبارات الوظيفة '+esc(f.code)+'</span> '+esc(f.name)+' — '+f.count+' عبارة</div>'+
      '<button class="btn-primary ghost" data-go="phrases" style="flex:0 0 auto;padding:8px 14px">مسح التصفية</button>'+
    '</div>';
  }

  function renderFunctions(){
    const items=FUNCTIONS.map(f=>{
      const ch=f.chapterId?CHAPTERS.find(c=>c.id===f.chapterId):null;
      return '<div class="card">'+
        '<h2><span class="ic c-teal" style="width:34px;height:34px;border-radius:10px;font-size:16px;display:inline-flex;align-items:center;justify-content:center;color:#fff;margin-left:8px">'+esc(f.code)+'</span>'+esc(f.name)+'</h2>'+
        (f.examples?'<p style="color:var(--text-soft);font-size:14px">أمثلة: '+esc(f.examples)+'</p>':'')+
        '<div class="phrase-meta" style="margin-top:8px">'+
          '<span class="badge gold">'+f.count+' عبارة</span>'+
          (ch?'<span class="badge blue">'+esc(ch.label)+'</span>':'')+
        '</div>'+
        '<div class="filter-row" style="margin-top:12px">'+
          (f.count>0?'<button class="btn-primary ghost" data-go="phrases?func='+f.code+'" style="flex:1">عرض عبارات هذه الوظيفة</button>':'<span style="flex:1"></span>')+
          (ch?'<button class="btn-primary ghost" data-go="'+ch.id+'" style="flex:1">القسم المختص ←</button>':'<span hidden></span>')+
        '</div>'+
      '</div>';
    }).join('');
    return '<div class="sec-intro">التصنيف الوظيفي (A–K) هو العمود الفقري للموسوعة: كل عبارة تنتمي إلى وظيفة بيعية. اختر وظيفة لتصفّح عباراتها أو تنتقل إلى قسمها المختص.</div><div style="display:flex;flex-direction:column;gap:14px">'+items+'</div>';
  }

  function renderSearch(){
    return '<div class="sec-intro">بحث شامل في كل أقسام الموسوعة وقاعدة العبارات معاً.</div>'+
      '<div class="filter-bar">'+
        '<div class="search-box" style="margin-bottom:0">'+
          '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M15.5 14h-.8l-.3-.3a6.5 6.5 0 10-.7.7l.3.3v.8l5 5 1.5-1.5-5-5zm-6 0A4.5 4.5 0 1114 9.5 4.5 4.5 0 019.5 14z"/></svg>'+
          '<input id="gsSearch" type="search" placeholder="ابحث عن عبارة، موضوع، كلمة، أو موقف...">'+
        '</div>'+
        '<div class="filter-row">'+
          '<select id="gsScope" class="filter-select">'+
            '<option value="all">الكل (عربي + متعدد اللغات)</option>'+
            '<option value="chapters">الأقسام العربية فقط</option>'+
            '<option value="phrases">العبارات العربية فقط</option>'+
            '<option value="ml">متعدد اللغات فقط</option>'+
          '</select>'+
        '</div>'+
      '</div>'+
      '<div id="gsCount" class="result-count"></div>'+
      '<div id="gsResults"></div>';
  }

  function renderGlobalResults(){
    const q=$('#gsSearch')?$('#gsSearch').value.trim().toLowerCase():'';
    const scope=$('#gsScope')?$('#gsScope').value:'all';
    const box=$('#gsResults'); if(!box) return;
    if(!q){ box.innerHTML='<p style="text-align:center;color:var(--text-mute);padding:20px">اكتب كلمة للبحث في الموسوعة.</p>'; const c=$('#gsCount'); if(c)c.textContent=''; return; }
    let html=''; let total=0;
    if(scope!=='phrases' && scope!=='ml'){
      const chRes=CHAPTERS.map(c=>({c,idx:c.raw.toLowerCase().indexOf(q)})).filter(x=>x.idx>=0);
      if(chRes.length){
        total+=chRes.length;
        html+='<h3 style="margin:16px 0 8px;color:var(--teal-700)">📘 أقسام الموسوعة العربية ('+chRes.length+')</h3>';
        html+=chRes.slice(0,40).map(({c})=>{
          const idx=c.raw.toLowerCase().indexOf(q);
          const start=Math.max(0,idx-40);
          const snip=c.raw.substring(start,start+120).replace(/\n+/g,' ').replace(/\*\*/g,'').replace(/[#>*|]/g,'');
          return '<button class="section-tile" data-go="'+c.id+'" style="text-align:right;align-items:flex-start">'+
            '<span class="ic '+c.color+'">'+c.icon+'</span><span class="t">'+esc(c.label)+'</span><span class="n">…'+esc(snip)+'…</span></button>';
        }).join('');
      }
      const mlRes=ML_DOCS.map(d=>({d,idx:d.raw.toLowerCase().indexOf(q)})).filter(x=>x.idx>=0);
      if(mlRes.length){
        total+=mlRes.length;
        html+='<h3 style="margin:16px 0 8px;color:var(--teal-700)">🌐 الموسوعة متعددة اللغات ('+mlRes.length+')</h3>';
        html+=mlRes.slice(0,40).map(({d})=>{
          const idx=d.raw.toLowerCase().indexOf(q);
          const start=Math.max(0,idx-40);
          const snip=d.raw.substring(start,start+120).replace(/\n+/g,' ').replace(/\*\*/g,'').replace(/[#>*|]/g,'');
          return '<button class="section-tile" data-go="'+d.id+'" style="text-align:right;align-items:flex-start">'+
            '<span class="ic '+d.color+'">'+d.icon+'</span><span class="t">'+esc(d.label)+'</span><span class="n">…'+esc(snip)+'…</span></button>';
        }).join('');
      }
    }
    if(scope!=='chapters' && scope!=='ml'){
      const phRes=PHRASES.filter(p=>(p.phrase+' '+p.msa+' '+p.notes+' '+p.situation+' '+p.country+' '+p.dialect).toLowerCase().includes(q));
      if(phRes.length){
        total+=phRes.length;
        html+='<h3 style="margin:16px 0 8px;color:var(--teal-700)">🔤 العبارات العربية ('+phRes.length+')</h3>';
        html+=phRes.slice(0,40).map(phraseCard).join('');
      }
    }
    if(scope!=='chapters' && scope!=='phrases'){
      const mlpRes=ML_PHRASES.filter(p=>(p.originalText+' '+p.arabic+' '+p.arabicTranslation+' '+p.arabicPronunciation+' '+p.country+' '+p.situation+' '+p.category+' '+p.literalTranslation+' '+p.culturalNotes).toLowerCase().includes(q));
      if(mlpRes.length){
        total+=mlpRes.length;
        html+='<h3 style="margin:16px 0 8px;color:var(--teal-700)">🌐 العبارات المتعددة اللغات ('+mlpRes.length+')</h3>';
        html+=mlpRes.slice(0,40).map(mlPhraseCard).join('');
      }
    }
    const cnt=$('#gsCount'); if(cnt) cnt.textContent=total+' نتيجة لـ «'+q+'»';
    box.innerHTML = total ? html : '<p style="text-align:center;color:var(--text-mute);padding:24px">لا توجد نتائج مطابقة لـ «'+esc(q)+'».</p>';
  }

  function bindSearch(){
    const s=$('#gsSearch');
    if(s){
      if(currentSearchQ) s.value=currentSearchQ;
      s.addEventListener('input', renderGlobalResults);
      setTimeout(()=>s.focus(), 50);
    }
    const sc=$('#gsScope'); if(sc) sc.addEventListener('change', renderGlobalResults);
    renderGlobalResults();
  }

  function renderFavorites(){
    if(!favorites.length) return '<div class="sec-intro">عباراتك المفضلة تظهر هنا.</div><div class="card" style="text-align:center;color:var(--text-mute)">لم تضف أي عبارة للمفضلة بعد. اضغط ☆ على أي عبارة عربية أو متعددة اللغات.</div>';
    const ar=PHRASES.filter(p=>favorites.includes(p.id));
    const ml=ML_PHRASES.filter(p=>favorites.includes(p.id));
    if(!ar.length && !ml.length) return '<div class="card" style="text-align:center;color:var(--text-mute)">المفضلة تشير إلى عبارات لم تعد موجودة.</div>';
    let html='<div class="sec-intro">لديك <b>'+(ar.length+ml.length)+'</b> عبارة في المفضلة.</div>';
    if(ar.length) html+='<h3 style="margin:8px 0 10px;color:var(--teal-700)">العبارات العربية</h3>'+ar.map(phraseCard).join('');
    if(ml.length) html+='<h3 style="margin:16px 0 10px;color:var(--teal-700)">العبارات المتعددة اللغات</h3>'+ml.map(mlPhraseCard).join('');
    return html;
  }

  function toggleFav(star){
    const pid=star.dataset.pid;
    if(favorites.includes(pid)){
      favorites=favorites.filter(x=>x!==pid);
      star.classList.remove('on'); star.textContent='☆'; toast('أُزيلت من المفضلة');
    } else {
      favorites.push(pid);
      star.classList.add('on'); star.textContent='★'; toast('أُضيفت للمفضلة ⭐');
    }
    store.set('souq_favs',favorites);
    if(currentRoute==='favorites') render('favorites');
  }

  function toast(msg){
    const t=$('#toast'); if(!t) return;
    t.textContent=msg; t.hidden=false;
    clearTimeout(toast._t); toast._t=setTimeout(()=>t.hidden=true,2200);
  }

  /* ---------- تفويض النقر ---------- */
  document.addEventListener('click', e=>{
    const sp=e.target.closest('[data-speak]');
    if(sp){ e.preventDefault(); speak(decodeURIComponent(sp.dataset.speak), sp.dataset.lang); return; }
    const go=e.target.closest('[data-go]');
    if(go){ navigate(go.dataset.go); return; }
    const anc=e.target.closest('[data-anchor]');
    if(anc){ e.preventDefault(); const el=document.getElementById(anc.dataset.anchor); if(el) el.scrollIntoView({behavior:'smooth',block:'start'}); return; }
    const star=e.target.closest('.fav-star');
    if(star){ toggleFav(star); return; }
    const acc=e.target.closest('.acc-head');
    if(acc){ acc.parentElement.classList.toggle('open'); return; }
  });

  /* ============================================================
     القسم متعدد اللغات (Languages)
     ============================================================ */
  function renderLanguages(){
    const langCards = ML_LANGS.map(l=>{
      const doc = ML_DOCS.find(d=>d.lang===l.code && d.role==='main');
      const cnt = SOUQ_META.mlLangCounts[l.code]||0;
      return '<button class="section-tile" data-go="'+(doc?doc.id:'#')+'">'+
        '<span class="ic '+l.color+'">'+l.flag+'</span>'+
        '<span class="t">'+esc(l.name)+'</span>'+
        '<span class="n">'+cnt+' عبارة</span>'+
      '</button>';
    }).join('');
    const cross=[
      {id:'mlcompare', icon:'🔁', c:'c-purple', t:'مقارنة الوظائف', n:'عبر اللغات'},
      {id:'mldialogues', icon:'💬', c:'c-rose', t:'حوارات تفاعلية', n:'استمع ومثّل الدور'},
      {id:'mlphrases', icon:'🔎', c:'c-blue', t:'قاعدة العبارات المتعددة', n:SOUQ_META.mlPhrasesCount+' عبارة'},
      {id:'ml-05-muqarana', icon:'🔁', c:'c-slate', t:'جداول المقارنة', n:'الوظيفة × ٦ لغات'},
      {id:'ml-07-hiwarat', icon:'💬', c:'c-slate', t:'حوارات متعددة اللغات', n:'نفس الموقف'},
      {id:'ml-08-qamus', icon:'🔤', c:'c-slate', t:'قاموس مشترك', n:'كلمات وأنواع محلات'},
      {id:'ml-06-qawalib', icon:'📋', c:'c-slate', t:'قوالب جاهزة', n:'قابلة لإعادة الاستخدام'},
      {id:'ml-09-tahthir-wa-masadir', icon:'⚠️', c:'c-slate', t:'محاذير ومصادر', n:'ما يحتاج تحققاً'},
      {id:'ml-10-tadrib', icon:'🎯', c:'c-slate', t:'تمارين مواقف', n:'أدوار ولعب'},
      {id:'ml-00-manhaj', icon:'🧭', c:'c-slate', t:'المنهج', n:'سلّم الثقة والنطق'},
      {id:'ml-README', icon:'ℹ️', c:'c-slate', t:'عن الموسوعة الموازية', n:'المنهجية'}
    ];
    const crossHtml=cross.map(q=>'<button class="section-tile" data-go="'+q.id+'"><span class="ic '+q.c+'">'+q.icon+'</span><span class="t">'+esc(q.t)+'</span><span class="n">'+esc(q.n)+'</span></button>').join('');
    return '<div class="chapter-head"><div style="display:flex;align-items:center"><span class="ch-num">🌐</span><div><h1>بوابة اللغات</h1><p>كيف يتكلم بائع حقيقي — لا ترجمة حرفية</p></div></div></div>'+
      '<div class="card"><h2>كيف تُقرأ هذه الطبقة؟</h2><p style="color:var(--text-soft);font-size:14.5px">لا تبحث عن ترجمة «يا هلا وسهلا». ابحث: <b>ماذا يقول بائع حقيقي في هذا الموقف، في هذه الثقافة، لهذا المخاطَب؟</b> المسار: الموقف ← العبارة الأصلية ← النطق التقريبي ← المعنى بالعربية ← لمن ومتى تُقال.</p></div>'+
      '<div class="sec-intro">خمس لغات · '+SOUQ_META.mlPhrasesCount+' عبارة أصلية</div>'+
      '<div class="section-grid">'+langCards+'</div>'+
      '<div class="sec-intro">مواد مشتركة وأدوات</div>'+
      '<div class="section-grid">'+crossHtml+'</div>';
  }

  function renderMlDoc(id){
    const d=ML_DOCS.find(x=>x.id===id);
    if(!d) return renderLanguages();
    const lm = ML_LANGS.find(l=>l.code===d.lang);
    const toc=mdToc(d.raw);
    const tocHtml = toc.length>1 ? '<div class="toc"><div class="toc-title">📑 محتويات هذا الملف</div>'+toc.map(t=>'<a data-anchor="'+t.id+'"><span class="dot"></span>'+esc(t.text)+'</a>').join('')+'</div>' : '';
    const openBtn = (d.role==='main' && d.lang!=='all') ? '<div class="filter-row" style="margin-top:14px"><button class="btn-primary ghost" data-go="mlphrases?lang='+d.lang+'" style="flex:1">تصفّح عبارات '+esc(lm?lm.name:'هذه اللغة')+'</button><button class="btn-primary ghost" data-go="mlcompare" style="flex:1">قارن مع اللغات الأخرى</button></div>' : '';
    return '<div class="chapter-head"><div style="display:flex;align-items:center"><span class="ch-num">'+d.icon+'</span><div><h1>'+esc(d.title)+'</h1><p>'+ (lm?lm.flag+' '+esc(lm.name):'مادة مشتركة عبر اللغات') +'</p></div></div></div>'+
      '<div class="about-meta" style="margin-bottom:12px">'+
        (lm?'<span class="badge gold">'+lm.flag+' '+esc(lm.name)+'</span>':'<span class="badge teal">مشترك</span>')+
        '<span class="badge blue">موسوعة موازية</span>'+
      '</div>'+
      '<div class="reading">'+
        tocHtml+
        '<div class="md-body">'+mdRender(d.raw, (d.lang && d.lang!=='all')?d.lang:'')+'</div>'+
      '</div>'+
      openBtn;
  }

  function mlPhraseCard(p){
    const lm = ML_LANGS.find(l=>l.code===p.targetLanguage) || {flag:'🌐',name:''};
    const b=(t,cls)=> t? '<span class="badge '+(cls||'')+'">'+esc(t)+'</span>' : '';
    const isFav=favorites.includes(p.id);
    const arabicTxt = p.noDirectArabic==='yes' ? 'لا مقابل عربي مباشر' : (p.arabic||'');
    const showLiteral = p.literalTranslation && p.literalTranslation!==p.arabicTranslation && p.literalTranslation!==arabicTxt;
    const extra=
      (showLiteral? '<div class="phrase-msa"><b>حرفياً:</b> '+esc(p.literalTranslation)+'</div>' : '')+
      '<div class="phrase-meta">'+
        b(p.category,'teal')+b(p.subcategory,'blue')+b(p.situation,'purple')+b(p.register)+b(p.audience)+b(p.frequency,'rose')+b(p.confidence,'gold')+
        (p.noDirectArabic==='yes'?b('بلا مقابل عربي','amber'):'')+
      '</div>'+
      (p.usageNotes? '<div class="phrase-notes"><b>متى تُقال:</b> '+esc(p.usageNotes)+'</div>' : '')+
      (p.culturalNotes? '<div class="phrase-notes"><b>ملاحظة ثقافية:</b> '+esc(p.culturalNotes)+'</div>' : '')+
      (p.alternatives? '<div class="phrase-notes"><b>بدائل:</b> <span dir="auto">'+esc(p.alternatives)+'</span></div>' : '')+
      relatedLangsBox(p);
    return '<div class="phrase-card ml-card" data-pid="'+esc(p.id)+'">'+
      '<button class="fav-star '+(isFav?'on':'')+'" data-pid="'+esc(p.id)+'" aria-label="مفضلة">'+(isFav?'★':'☆')+'</button>'+
      '<div class="ml-langline">'+lm.flag+' '+esc(lm.name)+(p.country?' · '+esc(p.country):'')+'</div>'+
      '<div class="say say-block">'+speakBtn(p.originalText, p.targetLanguage)+'<div class="phrase-main ml-orig" dir="auto">'+esc(p.originalText)+'</div></div>'+
      (p.arabicPronunciation? '<div class="ml-pron">'+esc(p.arabicPronunciation)+'</div>' : '')+
      (arabicTxt? '<div class="say say-inline">'+speakBtn(p.noDirectArabic==='yes'?'':(p.arabic||''),'ar')+'<div class="phrase-msa">'+esc(arabicTxt)+'</div></div>' : '')+
      (p.arabicTranslation? '<div class="phrase-sense">'+esc(p.arabicTranslation)+'</div>' : '')+
      moreFold(extra, 'تفاصيل وملاحظات')+
    '</div>';
  }

  function renderMlPhrases(){
    const cats=[...new Set(ML_PHRASES.map(p=>p.category))].sort();
    const countries=[...new Set(ML_PHRASES.map(p=>p.country).filter(Boolean))].sort();
    const opt=arr=>'<option value="">الكل</option>'+arr.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join('');
    const langOpt='<option value="">كل اللغات</option>'+ML_LANGS.map(l=>'<option value="'+l.code+'">'+l.flag+' '+esc(l.name)+'</option>').join('');
    return '<div class="sec-intro">قاعدة بيانات متعددة اللغات فيها <b>'+SOUQ_META.mlPhrasesCount+'</b> عبارة أصلية ('+ML_LANGS.map(l=>l.flag+' '+esc(l.name)).join(' · ')+') مع المقابل العربي والمعنى الوظيفي والنطق التقريبي. ابحث وصفِّ حسب اللغة أو الوظيفة أو الدولة.</div>'+
      '<div class="filter-bar">'+
        '<div class="search-box" style="margin-bottom:0"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M15.5 14h-.8l-.3-.3a6.5 6.5 0 10-.7.7l.3.3v.8l5 5 1.5-1.5-5-5zm-6 0A4.5 4.5 0 1114 9.5 4.5 4.5 0 019.5 14z"/></svg><input id="mlSearch" type="search" placeholder="ابحث: Hoş geldiniz، غالي، son fiyat، mahal..."></div>'+
        '<div class="filter-row"><select id="mlLang" class="filter-select">'+langOpt+'</select><select id="mlCat" class="filter-select">'+opt(cats)+'</select></div>'+
        '<div class="filter-row"><select id="mlCountry" class="filter-select">'+opt(countries)+'</select><button id="mlClear" class="btn-primary ghost" style="flex:0 0 auto;padding:10px 18px">مسح الفلاتر</button></div>'+
      '</div>'+
      '<div id="mlCount" class="result-count"></div>'+
      '<div id="mlResults"></div>';
  }

  function getFilteredMlPhrases(){
    const q=$('#mlSearch')?$('#mlSearch').value.trim().toLowerCase():'';
    const lang=$('#mlLang')?$('#mlLang').value:'';
    const cat=$('#mlCat')?$('#mlCat').value:'';
    const country=$('#mlCountry')?$('#mlCountry').value:'';
    return ML_PHRASES.filter(p=>{
      if(lang && p.targetLanguage!==lang) return false;
      if(cat && p.category!==cat) return false;
      if(country && p.country!==country) return false;
      if(q){
        const hay=(p.originalText+' '+p.arabic+' '+p.arabicTranslation+' '+p.arabicPronunciation+' '+p.country+' '+p.situation+' '+p.category).toLowerCase();
        if(!hay.includes(q)) return false;
      }
      return true;
    });
  }

  function renderMlPhrasesResults(){
    const list=getFilteredMlPhrases();
    const cnt=$('#mlCount'); if(cnt) cnt.innerHTML=list.length+' نتيجة';
    const box=$('#mlResults'); if(!box) return;
    if(!list.length){ box.innerHTML='<p style="text-align:center;color:var(--text-mute);padding:24px">لا توجد نتائج مطابقة.</p>'; return; }
    box.innerHTML=list.map(mlPhraseCard).join('');
  }

  function bindMlPhrases(){
    const el=$('#mlLang'); if(el && currentMlLang) el.value=currentMlLang;
    const sq=$('#mlSearch'); if(sq && currentMlQuery) sq.value=currentMlQuery;
    ['#mlSearch','#mlLang','#mlCat','#mlCountry'].forEach(sel=>{
      const e=$(sel); if(!e) return;
      e.addEventListener('input', renderMlPhrasesResults);
      if(sel!=='#mlSearch') e.addEventListener('change', renderMlPhrasesResults);
    });
    const clr=$('#mlClear'); if(clr) clr.addEventListener('click',()=>{
      if($('#mlSearch')) $('#mlSearch').value='';
      ['#mlLang','#mlCat','#mlCountry'].forEach(s=>{const e=$(s); if(e) e.value='';});
      currentMlLang='';
      renderMlPhrasesResults();
    });
    renderMlPhrasesResults();
  }

  function renderMlCompare(){
    const cats=[...new Set(ML_PHRASES.map(p=>p.category))].sort();
    const opt=cats.map((c,i)=>'<option value="'+esc(c)+'"'+(i===0?' selected':'')+'>'+esc(c)+'</option>').join('');
    return '<div class="sec-intro">نفس الموقف الاجتماعي عبر اللغات الخمس: العبارة الأصلية ثم نطقها ثم معناها. هذا جدول معادل وظيفي، لا ترجمة كلمة بكلمة.</div>'+
      '<div class="filter-bar"><div class="filter-row"><select id="mcCat" class="filter-select" style="flex:1">'+opt+'</select></div></div>'+
      '<div id="mcResults"></div>';
  }

  function renderMlCompareResults(){
    const cat=$('#mcCat')?$('#mcCat').value:'';
    const box=$('#mcResults'); if(!box) return;
    if(!cat){ box.innerHTML='<p style="text-align:center;color:var(--text-mute);padding:20px">اختر وظيفة لعرض المقارنة.</p>'; return; }
    const rows=ML_PHRASES.filter(p=>p.category===cat);
    const subs=[...new Set(rows.map(p=>p.subcategory))];
    let html='<div class="compare-stack">';
    subs.forEach(sub=>{
      html+='<div class="card compare-card"><h2>'+esc(sub)+'</h2><div class="compare-grid">';
      ML_LANGS.forEach(l=>{
        const ps=rows.filter(p=>p.subcategory===sub && p.targetLanguage===l.code);
        if(!ps.length){ html+='<div class="compare-cell"><div class="ml-langline">'+l.flag+' '+esc(l.name)+'</div><div class="text-mute">—</div></div>'; return; }
        html+='<div class="compare-cell"><div class="ml-langline">'+l.flag+' '+esc(l.name)+'</div>'+
          ps.map(p=>'<div class="say say-block">'+speakBtn(p.originalText,l.code)+'<div class="ml-orig" dir="auto">'+esc(p.originalText)+'</div></div>'+
            (p.arabicPronunciation?'<div class="ml-pron">'+esc(p.arabicPronunciation)+'</div>':'')+
            (p.arabicTranslation?'<div class="phrase-msa">'+esc(p.arabicTranslation)+'</div>':'')
          ).join('')+'</div>';
      });
      html+='</div></div>';
    });
    html+='</div>';
    box.innerHTML=html;
  }

  function bindMlCompare(){
    const el=$('#mcCat'); if(el) el.addEventListener('change', renderMlCompareResults);
    renderMlCompareResults();
  }



  function bindReading(){
    const links=$$('.toc [data-anchor]');
    if(!links.length) return;
    const map={};
    links.forEach(a=>{ const el=document.getElementById(a.dataset.anchor); if(el) map[el.id]=a; });
    if(!window.IntersectionObserver) return;
    const obs=new IntersectionObserver(entries=>{
      entries.forEach(en=>{
        if(!en.isIntersecting) return;
        const a=map[en.target.id];
        if(!a) return;
        links.forEach(x=>x.classList.toggle('on', x===a));
      });
    },{rootMargin:'-18% 0px -70% 0px', threshold:0});
    Object.keys(map).forEach(id=>obs.observe(document.getElementById(id)));
  }

  /* ============================================================
     نطق + ربط العبارات + حوارات تفاعلية
     ============================================================ */
  const TTS_LANG = {ar:'ar-SA', tr:'tr-TR', id:'id-ID', tg:'ru-RU', fr:'fr-FR', en:'en-GB'};

  function speakBtn(text, lang){
    const tx=plainSpeak(text||String(text||'').trim());
    if(!tx) return '';
    const L=guessLang(tx, lang);
    return '<button type="button" class="speak-btn wide" data-speak="'+encodeURIComponent(tx)+'" data-lang="'+esc(L)+'" aria-label="استمع للنطق">🔊 استمع</button>';
  }

  function speak(text, lang){
    if(!text) return;
    const syn = window.speechSynthesis;
    if(!syn || typeof SpeechSynthesisUtterance==='undefined'){
      toast('النطق غير متاح في هذا المتصفح');
      return;
    }
    syn.cancel();
    const u = new SpeechSynthesisUtterance(text);
    const code = TTS_LANG[lang] || 'ar-SA';
    u.lang = code;
    u.rate = 0.92;
    toast('🔊 يقرأ الآن…');
    const pref = code.slice(0,2);
    const voices = syn.getVoices()||[];
    const v = voices.find(x=>x.lang && x.lang.toLowerCase().indexOf(pref)===0)
           || voices.find(x=>x.lang && x.lang.toLowerCase().indexOf(code.toLowerCase())===0);
    if(v) u.voice=v;
    if(lang==='tg' && !speak._tg){ speak._tg=1; toast('الطاجيكية تُقرأ بصوت قريب إن وُجد'); }
    syn.speak(u);
  }

  function normAr(s){
    return String(s||'').replace(/[^\u0600-\u06FFa-zA-Z0-9\s]/g,'').replace(/\s+/g,' ').trim().toLowerCase();
  }

  function findArPhrase(text){
    const n=normAr(text);
    if(!n || n.length<3) return null;
    return PHRASES.find(p=>normAr(p.phrase)===n || normAr(p.msa)===n)
        || PHRASES.find(p=>normAr(p.phrase).indexOf(n)>=0 || (normAr(p.msa)&&normAr(p.msa).indexOf(n)>=0));
  }

  function findMlByArabic(text){
    const n=normAr(text);
    if(!n) return [];
    const exact=ML_PHRASES.filter(p=>p.noDirectArabic!=='yes' && normAr(p.arabic)===n);
    if(exact.length) return exact;
    return ML_PHRASES.filter(p=>p.noDirectArabic!=='yes' && normAr(p.arabic).indexOf(n)>=0);
  }

  function equivalentsBox(phrase, msa){
    const list = findMlByArabic(phrase).concat(msa?findMlByArabic(msa):[]);
    const seen={}; const uniq=[];
    list.forEach(p=>{ if(!seen[p.id]){ seen[p.id]=1; uniq.push(p); } });
    if(!uniq.length) return '';
    const chips=uniq.slice(0,8).map(p=>{
      const lm=ML_LANGS.find(l=>l.code===p.targetLanguage)||{flag:'🌐'};
      return '<button class="eq-chip" data-go="mlphrases?lang='+p.targetLanguage+'&q='+encodeURIComponent(p.originalText)+'">'+lm.flag+' <span class="eq-txt" dir="auto">'+esc(p.originalText)+'</span></button>';
    }).join('');
    return '<div class="eq-box"><div class="eq-title">المقابل في اللغات الأخرى</div>'+chips+'</div>';
  }

  function relatedLangsBox(p){
    const sibs=ML_PHRASES.filter(x=>x.id!==p.id && x.subcategory && x.subcategory===p.subcategory);
    const byAr = (p.arabic && p.noDirectArabic!=='yes') ? ML_PHRASES.filter(x=>x.id!==p.id && normAr(x.arabic)===normAr(p.arabic)) : [];
    const all=[], seen={};
    byAr.concat(sibs).forEach(x=>{ if(!seen[x.targetLanguage]){ seen[x.targetLanguage]=1; all.push(x); } });
    const arHit = (p.arabic && p.noDirectArabic!=='yes') ? findArPhrase(p.arabic) : null;
    if(!all.length && !arHit) return '';
    let html='<div class="eq-box"><div class="eq-title">نفس الموقف في لغات أخرى</div>';
    if(arHit) html+='<button class="eq-chip" data-go="phrases">العربية: '+esc(arHit.phrase)+'</button>';
    all.slice(0,6).forEach(x=>{
      const lm=ML_LANGS.find(l=>l.code===x.targetLanguage)||{flag:'🌐'};
      html+='<button class="eq-chip" data-go="mlphrases?lang='+x.targetLanguage+'&q='+encodeURIComponent(x.originalText)+'">'+lm.flag+' <span class="eq-txt" dir="auto">'+esc(x.originalText)+'</span></button>';
    });
    html+='</div>';
    return html;
  }

  const DLG_LANG = [
    {code:'ar', re:/عربي/, name:'العربية', flag:'🇸🇦'},
    {code:'tr', re:/ترك/, name:'التركية', flag:'🇹🇷'},
    {code:'id', re:/إندونيس/, name:'الإندونيسية', flag:'🇮🇩'},
    {code:'tg', re:/طاجيك/, name:'الطاجيكية', flag:'🇹🇯'},
    {code:'fr', re:/فرنس/, name:'الفرنسية', flag:'🇫🇷'},
    {code:'en', re:/إنجليز/, name:'الإنجليزية', flag:'🇬🇧'}
  ];

  function parseRoleLine(line){
    const m=String(line||'').match(/^\*\*([بزعب])[:：]\*\*\s*(.+)$/);
    if(!m) return null;
    return {role: m[1]==='ز'?'customer':'seller', text:m[2].replace(/\*+/g,'').trim()};
  }

  function extractLines(block){
    const lines=[];
    String(block||'').split('\n').forEach(l=>{
      const r=parseRoleLine(l.trim());
      if(r) lines.push(r);
    });
    const ital=String(block||'').match(/\n\*([^*\n][^*]{8,}?)\*\s*(?:\n|$)/);
    return {lines, meaning: ital?ital[1].trim():''};
  }

  function parseDialogues(){
    if(parseDialogues._c) return parseDialogues._c;
    const doc=ML_DOCS.find(d=>d.id==='ml-07-hiwarat');
    const raw=doc?doc.raw:'';
    const parts=String(raw).replace(/\r\n/g,'\n').split(/\n(?=##\s+)/);
    const out=[];
    parts.forEach(block=>{
      const hm=block.match(/^##\s+(.+)/);
      if(!hm) return;
      const title=hm[1].replace(/\*+/g,'').trim();
      const langs={};
      const sub=block.split(/\n(?=###\s+)/);
      if(sub.length>1){
        sub.slice(1).forEach(sec=>{
          const sh=sec.match(/^###\s+(.+)/);
          if(!sh) return;
          const meta=DLG_LANG.find(x=>x.re.test(sh[1]));
          const code=meta?meta.code:'en';
          const got=extractLines(sec);
          if(got.lines.length) langs[code]=got;
        });
      }
      if(!Object.keys(langs).length){
        const chunks=block.split(/\n(?=\*\*(?:TR|ID|TJ|FR|EN|ع)[:：]?\*\*)/);
        chunks.forEach(ch=>{
          const tag=(ch.match(/^\*\*(TR|ID|TJ|FR|EN|ع)[:：]?\*\*/)||[])[1];
          if(!tag) return;
          const map={TR:'tr',ID:'id',TJ:'tg',FR:'fr',EN:'en','ع':'ar'};
          const got=extractLines(ch);
          if(!got.lines.length){
            const rest=ch.replace(/^\*\*(TR|ID|TJ|FR|EN|ع)[:：]?\*\*\s*/,'').trim();
            const quoted=rest.match(/`([^`]+)`/g);
            if(quoted){
              got.lines=quoted.map((q,i)=>({role:i%2?'customer':'seller', text:q.slice(1,-1)}));
            } else if(rest){
              const first=rest.split('\n')[0].replace(/\*+/g,'').trim();
              if(first) got.lines=[{role:'seller', text:first}];
            }
          }
          if(got.lines.length) langs[map[tag]]=got;
        });
      }
      if(Object.keys(langs).length){
        out.push({id:'d'+out.length, title, langs});
      }
    });
    parseDialogues._c=out;
    return out;
  }

  function renderDialogues(){
    const list=parseDialogues();
    if(currentDlgId){
      const d=list.find(x=>x.id===currentDlgId);
      if(d) return renderDialoguePlay(d);
    }
    const items=list.map(d=>{
      const n=Object.keys(d.langs).length;
      const flags=DLG_LANG.filter(l=>d.langs[l.code]).map(l=>l.flag).join(' ');
      return '<button class="dlg-item" data-go="mldialogues?id='+d.id+'&lang=ar"><div class="t">'+esc(d.title)+'</div><div class="n">'+flags+' · '+n+' لغات</div></button>';
    }).join('');
    return '<div class="chapter-head"><div style="display:flex;align-items:center"><span class="ch-num">💬</span><div><h1>حوارات تفاعلية</h1><p>نفس الموقف في لغات السوق — استمع أو مثّل دوراً</p></div></div></div>'+
      '<div class="sec-intro">حوارات حية من الموسوعة الموازية. اختر موقفاً، بدّل اللغة، واضغط 🔊 على أي سطر.</div>'+
      '<div class="dlg-list">'+items+'</div>'+
      '<div class="filter-row" style="margin-top:14px"><button class="btn-primary ghost" data-go="ml-07-hiwarat">اقرأ النص الكامل</button></div>';
  }

  function renderDialoguePlay(d){
    const available=DLG_LANG.filter(l=>d.langs[l.code]);
    if(!d.langs[currentDlgLang] && available[0]) currentDlgLang=available[0].code;
    const pack=d.langs[currentDlgLang]||{lines:[],meaning:''};
    const pills=available.map(l=>'<button class="lang-pill'+(currentDlgLang===l.code?' on':'')+'" data-dlg-lang="'+l.code+'">'+l.flag+' '+esc(l.name)+'</button>').join('');
    const bubbles=pack.lines.map(ln=>{
      const who=ln.role==='customer'?'الزبون':'البائع';
      const hide = currentDlgRole!=='all' && currentDlgRole!==ln.role;
      return '<div class="bubble '+ln.role+(hide?' hidden-role':'')+'">'+
        '<div class="who">'+who+'</div>'+
        '<div class="say say-block">'+speakBtn(ln.text, currentDlgLang)+'<div class="line" dir="auto">'+esc(ln.text)+'</div></div>'+
      '</div>';
    }).join('');
    const allText=pack.lines.map(x=>x.text).join('. ');
    return '<div class="filter-row" style="margin-bottom:10px"><button class="btn-primary ghost" data-go="mldialogues" style="flex:0 0 auto;padding:8px 14px">→ كل الحوارات</button></div>'+
      '<div class="chapter-head"><div style="display:flex;align-items:center"><span class="ch-num">💬</span><div><h1>'+esc(d.title)+'</h1><p>بدّل اللغة أو أخفِ دوراً لتمثيله</p></div></div></div>'+
      '<div class="lang-pills">'+pills+'</div>'+
      '<div class="role-bar">'+
        '<button class="lang-pill'+(currentDlgRole==='all'?' on':'')+'" data-dlg-role="all">الحوار كاملاً</button>'+
        '<button class="lang-pill'+(currentDlgRole==='seller'?' on':'')+'" data-dlg-role="seller">أنا البائع</button>'+
        '<button class="lang-pill'+(currentDlgRole==='customer'?' on':'')+'" data-dlg-role="customer">أنا الزبون</button>'+
        '<button class="speak-btn wide" data-speak="'+encodeURIComponent(allText)+'" data-lang="'+currentDlgLang+'">🔊 اسمع الحوار</button>'+
      '</div>'+
      (currentDlgRole!=='all'?'<div class="hint-note">السطور المطموسة هي دور الطرف الآخر — اضغط 🔊 لتسمعها بعد أن تقول ردّك.</div>':'')+
      '<div class="chat">'+bubbles+'</div>'+
      (pack.meaning?'<div class="phrase-notes"><b>المعنى الوظيفي:</b> '+esc(pack.meaning)+'</div>':'');
  }

  function bindDialogues(){
    document.querySelectorAll('[data-dlg-lang]').forEach(b=>b.addEventListener('click',()=>{
      currentDlgLang=b.dataset.dlgLang;
      const c=document.querySelector('#content'); if(c) c.innerHTML=renderDialogues();
      bindDialogues();
    }));
    document.querySelectorAll('[data-dlg-role]').forEach(b=>b.addEventListener('click',()=>{
      currentDlgRole=b.dataset.dlgRole;
      const c=document.querySelector('#content'); if(c) c.innerHTML=renderDialogues();
      bindDialogues();
    }));
  }


  /* ---------- Service Worker ---------- */
  function registerSW(){
    if('serviceWorker' in navigator){
      window.addEventListener('load',()=>{ navigator.serviceWorker.register('sw.js').catch(()=>{}); });
    }
  }

})();
