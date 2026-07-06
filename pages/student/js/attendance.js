/* ══════════════════════════════════════
   ATTENDANCE — Chart.js Donut Chart
   Requires: chart.js loaded before this file
   ══════════════════════════════════════ */

(function () {
  const ctx = document.getElementById('attChart').getContext('2d');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Present', 'Absent', 'Late'],
      datasets: [{
        data: [22, 2, 1],
        backgroundColor: ['#16a34a', '#ef4444', '#f59e0b'],
        borderWidth: 3,
        borderColor: '#ffffff',
        hoverOffset: 4,
        borderRadius: 4,
      }]
    },
    options: {
      cutout: '76%',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e3a8a',
          padding: 8,
          cornerRadius: 8,
          titleFont: { size: 11, weight: '700', family: 'Inter' },
          bodyFont:  { size: 11, family: 'Inter' },
        }
      },
      animation: {
        animateRotate: true,
        duration: 1000,
        easing: 'easeOutQuart',
      }
    }
  });
})();
