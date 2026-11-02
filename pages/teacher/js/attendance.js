/* ══════════════════════════════════════
   ATTENDANCE — Chart.js Donut Chart (Teacher Portal)
   Requires: chart.js loaded before this file
   ══════════════════════════════════════ */

(function () {
  const canvas = document.getElementById('attChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Present', 'Absent', 'Late'],
      datasets: [{
        data: [78, 2, 4],
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
          backgroundColor: '#2455D6',
          padding: 8,
          cornerRadius: 8,
          titleFont: { size: 11, weight: '500', family: 'Inter' },
          bodyFont:  { size: 11, weight: '400', family: 'Inter' },
          callbacks: {
            label: function(context) {
              const total = 84;
              const val = context.raw;
              const pct = ((val / total) * 100).toFixed(1);
              return `${context.label}: ${val} students (${pct}%)`;
            }
          }
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

