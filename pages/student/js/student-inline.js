// Promo Slideshow
(function () {
  var track  = document.getElementById('promoTrack');
  var dots   = document.querySelectorAll('#promoDots .promo-dot');
  var total  = document.querySelectorAll('.promo-slide').length;
  var cur    = 0, timer;

  function goTo(n) {
    cur = (n + total) % total;
    track.style.transform = 'translateX(-' + cur * 100 + '%)';
    dots.forEach(function(d, i) { d.classList.toggle('active', i === cur); });
  }

  function start() { timer = setInterval(function() { goTo(cur + 1); }, 6000); }
  function reset() { clearInterval(timer); start(); }

  document.getElementById('promoNext').addEventListener('click', function() { goTo(cur + 1); reset(); });
  document.getElementById('promoPrev').addEventListener('click', function() { goTo(cur - 1); reset(); });
  dots.forEach(function(d) {
    d.addEventListener('click', function() { goTo(+this.dataset.i); reset(); });
  });

  start();
})();

// Digital ID Modal
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

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
})();
