(function () {
  var d = document;
  // menu
  var burger = d.getElementById('burger'), menu = d.getElementById('menu');
  function close() {
    if (!menu.classList.contains('open')) return;
    menu.classList.remove('open'); burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', burger.dataset.open); d.body.style.overflow = '';
  }
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var o = !menu.classList.contains('open');
      menu.classList.toggle('open', o); burger.setAttribute('aria-expanded', String(o));
      burger.setAttribute('aria-label', o ? burger.dataset.close : burger.dataset.open);
      d.body.style.overflow = o ? 'hidden' : '';
    });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) close(); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { close(); } });
    window.matchMedia('(min-width:1100px)').addEventListener('change', close);
  }

  // mobile action bar: only after the main CTA (hero / page head) is out of view, hidden over the form and footer
  var mob = d.getElementById('mob');
  var trigger = d.getElementById('heroCta') || d.querySelector('.phead, .art-head');
  var hideOver = d.querySelectorAll('#rfq, .ctaband, .foot');
  if (mob && trigger && 'IntersectionObserver' in window) {
    var past = false, over = 0;
    var set = function () {
      var on = past && over === 0;
      mob.classList.toggle('on', on); mob.setAttribute('aria-hidden', String(!on));
      mob.querySelectorAll('a').forEach(function (a) { a.tabIndex = on ? 0 : -1; });
    };
    new IntersectionObserver(function (es) {
      var e = es[0]; past = !e.isIntersecting && e.boundingClientRect.top < 0; set();
    }).observe(trigger);
    var seen = new Set();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) seen.add(e.target); else seen.delete(e.target); });
      over = seen.size; set();
    });
    hideOver.forEach(function (el) { io.observe(el); });
  }

  // RFQ form
  var form = d.getElementById('rfqForm');
  if (!form) return;
  var EN = form.dataset.lang === 'en';
  var T = EN ? { fill: 'Please complete: ', company: 'company', email: 'a valid e-mail', msg: 'part numbers or message', consent: 'consent', big: 'The file is larger than 10 MB.', type: 'Allowed files: xlsx, xls, csv, pdf.', sent: 'Sending...', fail: 'The enquiry could not be sent. Please e-mail info@gpenergia.com.pl.', sum: 'Summary: ', file: 'file' }
               : { fill: 'Uzupełnij: ', company: 'firmę', email: 'poprawny e-mail', msg: 'kody produktów lub wiadomość', consent: 'zgodę', big: 'Plik jest większy niż 10 MB.', type: 'Dozwolone pliki: xlsx, xls, csv, pdf.', sent: 'Wysyłanie...', fail: 'Nie udało się wysłać zapytania. Prosimy o e-mail na info@gpenergia.com.pl.', sum: 'Podsumowanie: ', file: 'plik' };
  var f = form.elements, err = d.getElementById('f-err'), ok = d.getElementById('rfqOk');
  var t0 = Date.now(); d.getElementById('f-t').value = String(t0);
  var fileIn = d.getElementById('f-file'), fileName = d.getElementById('f-file-name');
  function fileCheck() {
    var file = fileIn.files && fileIn.files[0];
    fileName.textContent = file ? file.name + ' (' + Math.max(1, Math.round(file.size / 1024)) + ' KB)' : fileName.dataset.none;
    if (!file) return '';
    if (!/\.(xlsx|xls|csv|pdf)$/i.test(file.name)) return T.type;
    if (file.size > 10 * 1024 * 1024) return T.big;
    return '';
  }
  fileIn.addEventListener('change', function () { err.textContent = fileCheck(); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var miss = [], first = null;
    [f.company, f.email, f.message].forEach(function (el) { el.classList.remove('bad'); el.removeAttribute('aria-invalid'); });
    function bad(el, label) { el.classList.add('bad'); el.setAttribute('aria-invalid', 'true'); miss.push(label); first = first || el; }
    if (!f.company.value.trim()) bad(f.company, T.company);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.email.value.trim())) bad(f.email, T.email);
    if (f.message.value.trim().length < 3) bad(f.message, T.msg);
    if (!f.consent.checked) { miss.push(T.consent); first = first || f.consent; }
    var fe = fileCheck();
    if (miss.length || fe) { err.textContent = miss.length ? T.fill + miss.join(', ') + '.' + (fe ? ' ' + fe : '') : fe; if (first) first.focus(); return; }
    err.textContent = '';
    if (f.website.value) return; // honeypot
    var ep = form.dataset.endpoint;
    var file = fileIn.files && fileIn.files[0];
    var summary = f.subject.value + ' - ' + f.company.value.trim() + ' - ' + f.email.value.trim() + (file ? ' - ' + T.file + ': ' + file.name : '');
    if (!ep) { // preview: no backend yet
      d.getElementById('rfqSum').textContent = T.sum + summary;
      form.hidden = true; ok.hidden = false; ok.focus(); return;
    }
    var btn = form.querySelector('button[type=submit]'); btn.disabled = true; btn.textContent = T.sent;
    fetch(ep, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); d.getElementById('rfqSum').textContent = T.sum + summary; form.hidden = true; ok.hidden = false; ok.focus(); })
      .catch(function () { err.textContent = T.fail; btn.disabled = false; btn.textContent = btn.dataset.label || btn.textContent; });
  });
})();
