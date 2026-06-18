/* ============================================================
   SYTFIX — ROI CALCULATOR
   Industry data · Auto-fill · Live computation
   ============================================================ */

(function () {
  'use strict';

  /* ── INDUSTRY BASELINE DATA ── */
  const INDUSTRIES = {
    hvac: {
      label:          'HVAC',
      jobValue:       350,
      visitorsMonthly:820,
      currentConv:    2.1,
      industryConv:   4.9,
      lostLeads:      8,
      lindy:          44,
    },
    plumbing: {
      label:          'Plumbing',
      jobValue:       275,
      visitorsMonthly:710,
      currentConv:    1.9,
      industryConv:   5.2,
      lostLeads:      10,
      lindy:          41,
    },
    dental: {
      label:          'Dental Practice',
      jobValue:       1200,
      visitorsMonthly:590,
      currentConv:    1.4,
      industryConv:   3.8,
      lostLeads:      5,
      lindy:          52,
    },
    construction: {
      label:          'Construction / Remodeling',
      jobValue:       8500,
      visitorsMonthly:380,
      currentConv:    0.8,
      industryConv:   2.5,
      lostLeads:      3,
      lindy:          38,
    },
    roofing: {
      label:          'Roofing',
      jobValue:       6500,
      visitorsMonthly:510,
      currentConv:    1.2,
      industryConv:   3.5,
      lostLeads:      4,
      lindy:          40,
    },
    landscaping: {
      label:          'Landscaping',
      jobValue:       420,
      visitorsMonthly:650,
      currentConv:    2.3,
      industryConv:   5.0,
      lostLeads:      7,
      lindy:          45,
    },
    electrical: {
      label:          'Electrical',
      jobValue:       290,
      visitorsMonthly:760,
      currentConv:    2.0,
      industryConv:   4.6,
      lostLeads:      9,
      lindy:          43,
    },
    pest: {
      label:          'Pest Control',
      jobValue:       210,
      visitorsMonthly:680,
      currentConv:    1.7,
      industryConv:   4.3,
      lostLeads:      8,
      lindy:          42,
    },
    general: {
      label:          'Other Service Business',
      jobValue:       450,
      visitorsMonthly:620,
      currentConv:    1.8,
      industryConv:   4.2,
      lostLeads:      7,
      lindy:          44,
    },
  };

  /* ── DOM REFS ── */
  const industrySelect  = document.getElementById('calc-industry');
  const jobValueInput   = document.getElementById('calc-job-value');
  const visitorsInput   = document.getElementById('calc-visitors');
  const currentConvInput= document.getElementById('calc-current-conv');
  const industryConvInput= document.getElementById('calc-industry-conv');

  const resMonthly      = document.getElementById('res-monthly-loss');
  const resAnnual       = document.getElementById('res-annual-loss');
  const resPotential    = document.getElementById('res-potential');
  const resLindy        = document.getElementById('res-lindy');
  const resLindyBar     = document.getElementById('res-lindy-bar');
  const resLindyStatus  = document.getElementById('res-lindy-status');

  if (!industrySelect) return;

  /* ── AUTO-FILL ON INDUSTRY CHANGE ── */
  function fillFromIndustry(key) {
    const data = INDUSTRIES[key];
    if (!data) return;

    animateInput(jobValueInput,    data.jobValue);
    animateInput(visitorsInput,    data.visitorsMonthly);
    animateInput(currentConvInput, data.currentConv, 1);
    animateInput(industryConvInput,data.industryConv, 1);

    compute();
  }

  function animateInput(el, target, decimals) {
    if (!el) return;
    const dec      = decimals || 0;
    const start    = parseFloat(el.value) || 0;
    const duration = 500;
    const began    = performance.now();

    function step(now) {
      const progress = Math.min((now - began) / duration, 1);
      const eased    = 1 - Math.pow(1 - progress, 3);
      const value    = start + (target - start) * eased;
      el.value       = value.toFixed(dec);
      if (progress < 1) requestAnimationFrame(step);
      else el.value  = target.toFixed(dec);
    }
    requestAnimationFrame(step);
  }

  /* ── COMPUTE RESULTS ── */
  function compute() {
    const jobValue    = parseFloat(jobValueInput.value)    || 0;
    const visitors    = parseFloat(visitorsInput.value)    || 0;
    const currentConv = parseFloat(currentConvInput.value) || 0;
    const industConv  = parseFloat(industryConvInput.value)|| 0;

    const currentLeads  = visitors * (currentConv / 100);
    const potentialLeads= visitors * (industConv  / 100);
    const lostLeads     = Math.max(potentialLeads - currentLeads, 0);
    const monthlyLoss   = lostLeads * jobValue;
    const annualLoss    = monthlyLoss * 12;
    const potential     = potentialLeads * jobValue;

    const key    = industrySelect.value;
    const lindy  = INDUSTRIES[key] ? INDUSTRIES[key].lindy : 44;
    const afterLindy = Math.min(lindy + 38, 96);

    if (resMonthly) {
      resMonthly.textContent = formatCurrency(monthlyLoss);
      resMonthly.className   = 'calc-result-item__val calc-result-item__val--danger';
    }

    if (resAnnual) {
      resAnnual.textContent = formatCurrency(annualLoss);
      resAnnual.className   = 'calc-result-item__val calc-result-item__val--danger';
    }

    if (resPotential) {
      resPotential.textContent = formatCurrency(potential);
      resPotential.className   = 'calc-result-item__val calc-result-item__val--good';
    }

    if (resLindy) {
      resLindy.textContent = lindy + ' → ' + afterLindy;
    }

    if (resLindyBar) {
      resLindyBar.style.width = afterLindy + '%';
    }

    if (resLindyStatus) {
      if (lindy < 40) {
        resLindyStatus.textContent = 'Needs Urgent Work';
        resLindyStatus.style.color = '#ef4444';
      } else if (lindy < 65) {
        resLindyStatus.textContent = 'Below Industry Standard';
        resLindyStatus.style.color = '#f59e0b';
      } else {
        resLindyStatus.textContent = 'Performing Well';
        resLindyStatus.style.color = '#22c55e';
      }
    }

    updateSummary(monthlyLoss, annualLoss, lostLeads);
  }

  /* ── NARRATIVE SUMMARY ── */
  function updateSummary(monthly, annual, lostLeads) {
    const summary = document.getElementById('calc-summary');
    if (!summary) return;

    const industryLabel = INDUSTRIES[industrySelect.value]
      ? INDUSTRIES[industrySelect.value].label
      : 'your industry';
    const roundedLeads = Math.ceil(lostLeads);

    summary.innerHTML = 'Based on your inputs, your website is leaving approximately '
      + '<strong>' + roundedLeads + ' leads/month</strong> on the table — '
      + 'worth <strong>' + formatCurrency(monthly) + ' per month</strong> and '
      + '<strong>' + formatCurrency(annual) + ' per year</strong>. '
      + 'The average ' + industryLabel + ' website that goes through SytFix remediation '
      + 'improves its Lindy Score™ by 35–45 points within 30 days.';
  }

  /* ── CURRENCY FORMATTER ── */
  function formatCurrency(num) {
    if (num >= 1000000) return '$' + (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000)    return '$' + (num / 1000).toFixed(1)    + 'K';
    return '$' + Math.round(num).toLocaleString();
  }

  /* ── EVENT LISTENERS ── */
  industrySelect.addEventListener('change', function () {
    fillFromIndustry(this.value);
  });

  [jobValueInput, visitorsInput, currentConvInput, industryConvInput].forEach(function (el) {
    if (el) {
      el.addEventListener('input', compute);
      el.addEventListener('change', compute);
    }
  });

  /* ── INIT ── */
  fillFromIndustry(industrySelect.value || 'hvac');

  /* ── CTA SCROLL ── */
  const calcCta = document.getElementById('calc-cta');
  if (calcCta) {
    calcCta.addEventListener('click', function (e) {
      e.preventDefault();
      window.location.href = 'contact.html?source=calculator';
    });
  }

})();
