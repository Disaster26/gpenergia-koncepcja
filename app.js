(function(){
  var top=document.getElementById('top'),burger=document.getElementById('burger'),menu=document.getElementById('menu');
  function cien(){top.classList.toggle('cien',window.scrollY>8)}
  cien();window.addEventListener('scroll',cien,{passive:true});
  function zamknij(){menu.classList.remove('otwarte');burger.setAttribute('aria-expanded','false');burger.setAttribute('aria-label','Otwórz menu');document.body.style.overflow=''}
  burger.addEventListener('click',function(){
    var o=!menu.classList.contains('otwarte');
    menu.classList.toggle('otwarte',o);burger.setAttribute('aria-expanded',String(o));
    burger.setAttribute('aria-label',o?'Zamknij menu':'Otwórz menu');document.body.style.overflow=o?'hidden':'';
  });
  menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',zamknij)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')zamknij()});

  // dolny pasek na telefonie: dopiero po przewinieciu za przyciski hero
  var mob=document.getElementById('mob'),cta=document.getElementById('heroCta'),kontakt=document.getElementById('kontakt');
  var zaHero=false,wKontakcie=false;
  function pasek(){var w=zaHero&&!wKontakcie;mob.classList.toggle('widac',w);mob.setAttribute('aria-hidden',String(!w));mob.querySelectorAll('a').forEach(function(a){a.tabIndex=w?0:-1})}
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(e){zaHero=!e[0].isIntersecting&&e[0].boundingClientRect.top<0;pasek()}).observe(cta);
    new IntersectionObserver(function(e){wKontakcie=e[0].isIntersecting;pasek()},{rootMargin:'0px 0px -40% 0px'}).observe(kontakt);
  }

  // formularz: bez backendu, podsumowanie + mailto
  var form=document.getElementById('form'),blad=document.getElementById('formBlad'),ok=document.getElementById('formOk');
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var f=form.elements,braki=[];
    [f.email,f.wiad].forEach(function(el){el.classList.remove('zle')});
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email.value.trim())){braki.push('e-mail');f.email.classList.add('zle')}
    if(f.wiad.value.trim().length<3){braki.push('listę produktów lub opis');f.wiad.classList.add('zle')}
    if(!f.zgoda.checked){braki.push('zgodę na przetwarzanie danych')}
    if(braki.length){blad.textContent='Uzupełnij: '+braki.join(', ')+'.';return}
    blad.textContent='';
    var plik=f.plik.files&&f.plik.files[0]?f.plik.files[0].name:'';
    var tresc='Rodzaj: '+f.typ.value+'\nFirma: '+(f.firma.value||'-')+'\nOsoba: '+(f.osoba.value||'-')+'\nE-mail: '+f.email.value+'\nTelefon: '+(f.tel.value||'-')+'\n\n'+f.wiad.value+(plik?'\n\n(Załączę plik: '+plik+')':'');
    document.getElementById('formPodsum').textContent=f.typ.value+(f.firma.value?' - '+f.firma.value:'')+(plik?', plik: '+plik:'')+'. Odpowiemy na adres '+f.email.value+'.';
    document.getElementById('formMail').href='mailto:il@gpenergia.com.pl?subject='+encodeURIComponent('Zapytanie ze strony: '+f.typ.value)+'&body='+encodeURIComponent(tresc);
    form.hidden=true;ok.hidden=false;ok.scrollIntoView({behavior:'smooth',block:'center'});
  });
})();
