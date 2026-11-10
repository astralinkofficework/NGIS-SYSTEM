/**
 * NGIS Dashboard CMS Client Loader
 * Dynamically connects published CMS configuration (Hero & Banners)
 * to live Student, Teacher, Principal, and Admin dashboards with graceful fallbacks.
 */

(function () {
  'use strict';

  function resolvePortal() {
    var p = (window.location.pathname || '').toLowerCase();
    if (p.indexOf('/pages/admin/') !== -1 || p.indexOf('/admin') !== -1) return 'admin';
    if (p.indexOf('/pages/teacher/') !== -1 || p.indexOf('/teacher') !== -1) return 'teacher';
    if (p.indexOf('/pages/principal/') !== -1 || p.indexOf('/principal') !== -1) return 'principal';
    if (p.indexOf('/pages/student/') !== -1 || p.indexOf('/student') !== -1) return 'student';
    return document.body.getAttribute('data-role') || 'student';
  }

  function hydrateDashboard() {
    var portal = resolvePortal();
    var campus = 'all';

    fetch('/api/cms/dashboard/content?portal=' + portal + '&campus=' + campus + '&mode=published')
      .then(function (res) { return res.json(); })
      .then(function (res) {
        if (!res.success || !res.data) return;
        var data = res.data;

        // 1. Hydrate Hero Section
        if (data.hero) {
          var heroTitle = document.querySelector('.hero-title');
          if (heroTitle && data.hero.title) heroTitle.textContent = data.hero.title;

          var heroGreeting = document.querySelector('.hero-greeting');
          if (heroGreeting && data.hero.greeting) heroGreeting.textContent = data.hero.greeting;

          var heroDate = document.querySelector('.hero-date');
          if (heroDate) {
            if (data.hero.date_visible === false) heroDate.style.display = 'none';
            else if (data.hero.date) heroDate.textContent = data.hero.date;
          }
        }

        // 2. Hydrate Banner Section
        var bannerSec = document.querySelector('.dash-banner-section');
        var sectionCfg = (data.page_sections || []).find(function (s) { return s.id === 'sec-banner'; });
        if (bannerSec && sectionCfg && sectionCfg.visible === false) {
          bannerSec.style.display = 'none';
        } else if (bannerSec && data.banners && data.banners.length > 0) {
          bannerSec.style.display = 'block';

          // Update slides in promo-track
          var track = document.getElementById('promoTrack');
          var dotsWrap = document.getElementById('promoDots');

          if (track) {
            var slidesHtml = '';
            var dotsHtml = '';
            data.banners.forEach(function (b, i) {
              slidesHtml += '<div class="promo-slide" data-idx="' + i + '"><img src="' + b.image_url + '" alt="' + (b.alt_text || 'Banner') + '"></div>';
              dotsHtml += '<button type="button" class="promo-dot' + (i === 0 ? ' active' : '') + '" data-i="' + i + '" aria-label="Slide ' + (i + 1) + '"></button>';
            });
            track.innerHTML = slidesHtml;
            if (dotsWrap) dotsWrap.innerHTML = dotsHtml;

            // Update first slide text
            var titleEl = document.querySelector('.promo-left-title');
            var subEl = document.querySelector('.promo-left-sub');
            if (titleEl && data.banners[0].heading) titleEl.innerHTML = data.banners[0].heading;
            if (subEl && data.banners[0].subtitle) subEl.textContent = data.banners[0].subtitle;

            // Wire reactive slide text transition
            window.NGIS_CMS_BANNERS = data.banners;
          }
        }
      })
      .catch(function (err) {
        // Graceful silent fallback to hardcoded template
        console.warn('[CMS Client] Notice: Live CMS hydration deferred:', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydrateDashboard);
  } else {
    hydrateDashboard();
  }
})();

