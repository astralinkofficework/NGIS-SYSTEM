/* Promo Slideshow */
(function () {
  var track  = document.getElementById('promoTrack');
  var dots   = document.querySelectorAll('#promoDots .promo-dot');
  var total  = document.querySelectorAll('.promo-slide').length;
  var cur    = 0, timer;

  function show(idx) {
    track.style.transform = 'translateX(-' + (idx * 100) + '%)';
    dots.forEach(function(d, i) {
      d.classList.toggle('active', i === idx);
    });
    cur = idx;
  }

  function next() {
    show((cur + 1) % total);
  }

  function start() {
    timer = setInterval(next, 4000);
  }

  function stop() {
    clearInterval(timer);
  }

  dots.forEach(function(d, i) {
    d.addEventListener('click', function() {
      stop();
      show(i);
      start();
    });
  });

  start();
})();

/* Digital Student ID Card Modal */
(function() {
  const modal = document.getElementById('idModal');
  const openBtn = document.getElementById('viewIdBtn');
  const openBtnTop = document.getElementById('viewIdBtnTop');
  const closeBtn = document.getElementById('idCloseBtn');
  const cardWrap = document.getElementById('idCardWrap');

  function openModal() {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.remove('show');
    document.body.style.overflow = '';
    cardWrap.classList.remove('flipped');
  }

  if (openBtn) openBtn.addEventListener('click', openModal);
  if (openBtnTop) openBtnTop.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (cardWrap) cardWrap.addEventListener('click', () => cardWrap.classList.toggle('flipped'));

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
})();
