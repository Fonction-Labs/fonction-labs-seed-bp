const data = window.DASHBOARD_DATA;

// ─── Helpers ────────────────────────────────────────────────────────────────

const fmt = {
  eur(v) {
    const n = Number(v || 0);
    if (Math.abs(n) >= 1_000_000) return (n / 1_000_000).toFixed(1).replace('.0', '') + 'M€';
    if (Math.abs(n) >= 1_000) return Math.round(n / 1_000) + 'k€';
    return Math.round(n) + '€';
  },
  count(v) { return String(Math.round(Number(v || 0))); },
  pct(v) { return Math.round(Number(v || 0) * 100) + '%'; },
};

function el(id) { return document.getElementById(id); }
function setHTML(id, html) { const e = el(id); if (e) e.innerHTML = html; }

function isDark() { return document.documentElement.classList.contains('dark'); }

const GRID_COLOR   = () => isDark() ? 'rgba(255,255,255,.07)' : 'rgba(0,0,0,.06)';
const TICK_COLOR   = () => isDark() ? '#71717a' : '#a1a1aa';
const TOOLTIP_BG   = () => isDark() ? '#18181b' : '#fff';
const TOOLTIP_BODY = () => isDark() ? '#d4d4d8' : '#3f3f46';
const TOOLTIP_TTL  = () => isDark() ? '#f4f4f5' : '#18181b';

const baseChartOpts = (yFmt) => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: TOOLTIP_BG,
      titleColor: TOOLTIP_TTL,
      bodyColor: TOOLTIP_BODY,
      borderColor: () => isDark() ? '#3f3f46' : '#e4e4e7',
      borderWidth: 1,
      padding: 10,
      callbacks: { label: ctx => ` ${ctx.dataset.label}: ${yFmt(ctx.parsed.y)}` }
    }
  },
  scales: {
    x: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, font: { size: 11 } } },
    y: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, font: { size: 11 }, callback: yFmt }, border: { display: false } }
  }
});

// ─── KPIs — stat row sans chrome ─────────────────────────────────────────────

function renderKpis() {
  function getKpi(name) { return data.kpis.find(k => k.metric === name); }
  function kpiVal(k) { return k.unit === 'EUR' ? fmt.eur(k.value) : fmt.count(k.value); }

  const row2028 = data.annual_summary.find(r => r.year === 2028);
  const mil2028 = data.year_end_milestones.find(r => r.year === 2028);

  // Two rows: actuals + 2026 / 2027 numbers / 2028 numbers
  const row1 = [
    { label: 'Revenue H1 2026*',        val: kpiVal(getKpi('Actual commercial revenue Jan-Jun 2026')), sub: 'Actuals Jan–Jun', accent: true },
    { label: '2026E revenue',            val: kpiVal(getKpi('2026E revenue')),                         sub: 'Full-year' },
    { label: '2027E revenue',            val: kpiVal(getKpi('2027E revenue')),                         sub: 'Services + abonnement' },
    { label: 'ARR Dec-2027',             val: kpiVal(getKpi('Ending ARR Dec-2027')),                   sub: 'Run-rate annualisé' },
  ];
  const row2 = [
    { label: 'Enterprise accounts 2027', val: kpiVal(getKpi('Enterprise accounts Dec-2027')),          sub: 'Comptes activés' },
    { label: 'Live use cases 2027',      val: kpiVal(getKpi('Live use cases Dec-2027')),               sub: 'Use cases live' },
    { label: '2028E revenue',            val: row2028 ? fmt.eur(row2028.total_revenue) : '—',          sub: 'Expansion comptes' },
    { label: 'ARR Dec-2028',             val: mil2028 ? fmt.eur(mil2028.ending_arr) : '—',            sub: 'Run-rate annualisé' },
  ];

  const renderRow = (items) => `
    <div class="grid grid-cols-2 sm:grid-cols-4 divide-x divide-zinc-200 dark:divide-zinc-800 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden mb-px">
      ${items.map(item => `
        <div class="px-5 py-4 ${item.accent ? 'bg-zinc-900 dark:bg-zinc-800' : 'bg-white dark:bg-zinc-950'}">
          <div class="text-xs text-${item.accent ? 'zinc-400' : 'zinc-500'} mb-1.5 truncate">${item.label}</div>
          <div class="text-2xl font-bold tracking-tight leading-none ${item.accent ? 'text-white' : ''}">${item.val}</div>
          <div class="text-xs mt-2 text-${item.accent ? 'zinc-400' : 'zinc-400'}">${item.sub}</div>
        </div>`).join('')}
    </div>`;

  setHTML('kpiGrid',
    renderRow(row1) + renderRow(row2) +
    `<p class="text-xs text-zinc-400 dark:text-zinc-500 mt-3 pl-1">* Chiffre d'affaires encaissé sur transactions Qonto classifiées. Facturé YTD : ~230k€.</p>`
  );
}

// ─── Trajectory — timeline table ─────────────────────────────────────────────

function renderTrajectory() {
  const years = data.annual_summary;    // 2026, 2027, 2028
  const milestones = data.year_end_milestones;
  const themes = data.trajectory;

  // Rows: theme, revenue, ARR, use cases, description
  const get = (year) => ({
    theme:    themes.find(t => t.year === year),
    summary:  years.find(r => r.year === year),
    mile:     milestones.find(r => r.year === year),
  });

  const cols = [2026, 2027, 2028].map(get);

  const borderCls = 'border-t border-zinc-200 dark:border-zinc-800';
  const labelCls  = 'text-xs font-medium text-zinc-400 dark:text-zinc-500 uppercase tracking-wide py-3 pr-4 whitespace-nowrap';
  const cellCls   = 'py-3 px-4 text-sm';

  setHTML('trajectoryTable', `
    <table class="w-full text-sm border-collapse">
      <thead>
        <tr>
          <th class="text-left ${labelCls} w-28"></th>
          ${cols.map(c => `<th class="text-left px-4 py-3 border-l border-zinc-200 dark:border-zinc-800">
            <span class="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">${c.theme.year}</span>
            <div class="text-base font-semibold text-zinc-900 dark:text-zinc-100 mt-1">${c.theme.theme}</div>
          </th>`).join('')}
        </tr>
      </thead>
      <tbody>
        <tr class="${borderCls}">
          <td class="${labelCls}">Revenue</td>
          ${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800 font-semibold">${fmt.eur(c.summary.total_revenue)}</td>`).join('')}
        </tr>
        <tr class="${borderCls}">
          <td class="${labelCls}">Ending ARR</td>
          ${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800 font-semibold">${fmt.eur(c.mile.ending_arr)}</td>`).join('')}
        </tr>
        <tr class="${borderCls}">
          <td class="${labelCls}">Live use cases</td>
          ${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800">${fmt.count(c.mile.live_use_cases)}</td>`).join('')}
        </tr>
        <tr class="${borderCls}">
          <td class="${labelCls}">Comptes</td>
          ${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800">${fmt.count(c.mile.enterprise_accounts)}</td>`).join('')}
        </tr>
        <tr class="${borderCls}">
          <td class="${labelCls}">Récurrent</td>
          ${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800 text-zinc-500">${fmt.pct(c.summary.recurring_revenue_share)}</td>`).join('')}
        </tr>
        <tr class="${borderCls}">
          <td class="${labelCls}"></td>
          ${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800 text-zinc-500 dark:text-zinc-400 leading-relaxed">${c.theme.text}</td>`).join('')}
        </tr>
      </tbody>
    </table>`);
}

// ─── Monthly revenue 2026 ────────────────────────────────────────────────────

function renderMonthlyRevenue() {
  const months = data.revenue_monthly.filter(r => r.year === 2026);
  const labels = months.map(m => new Date(m.month).toLocaleDateString('fr-FR', { month: 'short' }));

  // Derive the actuals boundary from metadata so it follows vc_case.yaml automatically
  const actualsEnd = new Date(data.metadata.actuals_end_month || '2099-01-01');
  const actualsEndIdx = months.findIndex(m => new Date(m.month) >= actualsEnd);
  const splitIdx = actualsEndIdx === -1 ? months.length : actualsEndIdx;

  // The split month is partially actual, rest is forecast (pro-rated from today if we're in that month)
  const splitRow = months[splitIdx];
  const splitActual = splitRow ? splitRow.actual_commercial_revenue : 0;

  const today = new Date();
  const splitDate = splitRow ? new Date(splitRow.month) : null;
  const isCurrentMonth = splitDate && today.getFullYear() === splitDate.getFullYear() && today.getMonth() === splitDate.getMonth();
  const dayElapsed = isCurrentMonth ? today.getDate() : 30;
  const dayRemaining = Math.max(0, 30 - dayElapsed);
  const splitForecast = (splitRow && dayRemaining > 0) ? (splitActual / dayElapsed) * dayRemaining : 0;

  const actualVals   = months.map((m, i) => i < splitIdx ? m.total_revenue : i === splitIdx ? splitActual : 0);
  const forecastVals = months.map((m, i) => i < splitIdx ? 0 : i === splitIdx ? splitForecast : m.total_revenue);

  const darkColor = isDark() ? '#e4e4e7' : '#18181b';
  const grayColor = isDark() ? '#71717a' : '#a1a1aa';

  new Chart(el('monthlyRevenueChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Actuel',   data: actualVals,   backgroundColor: darkColor, borderRadius: 6 },
        { label: 'Forecast', data: forecastVals, backgroundColor: grayColor, borderRadius: 6 },
      ]
    },
    options: {
      ...baseChartOpts(fmt.eur),
      scales: {
        ...baseChartOpts(fmt.eur).scales,
        x: { ...baseChartOpts(fmt.eur).scales.x, stacked: true },
        y: { ...baseChartOpts(fmt.eur).scales.y, stacked: true },
      },
      plugins: {
        ...baseChartOpts(fmt.eur).plugins,
        legend: { display: false },
        tooltip: {
          ...baseChartOpts(fmt.eur).plugins.tooltip,
          filter: (item) => item.parsed.y > 0,
        }
      }
    }
  });

  const janJun = months.slice(0, 6).reduce((s, r) => s + r.total_revenue, 0);
  const julDec = months.slice(6).reduce((s, r) => s + r.total_revenue, 0);
  const svcH1 = months.slice(0, 6).reduce((s, r) => s + r.services_deployment_revenue, 0);
  const svcH2 = months.slice(6).reduce((s, r) => s + r.services_deployment_revenue, 0);
  const subH1 = months.slice(0, 6).reduce((s, r) => s + r.platform_subscription_revenue, 0);
  const subH2 = months.slice(6).reduce((s, r) => s + r.platform_subscription_revenue, 0);

  const rows = [
    ['Commercial revenue',          janJun,      julDec,      janJun + julDec],
    ['Services & deployment',       svcH1,       svcH2,       svcH1 + svcH2],
    ['Platform subscription',       subH1,       subH2,       subH1 + subH2],
  ];
  setHTML('revenue2026Rows', rows.map(([label, h1, h2, total]) => `
    <tr>
      <td class="px-4 py-3 text-zinc-700 dark:text-zinc-300">${label}</td>
      <td class="px-4 py-3 text-right">${fmt.eur(h1)}</td>
      <td class="px-4 py-3 text-right">${fmt.eur(h2)}</td>
      <td class="px-4 py-3 text-right font-semibold">${fmt.eur(total)}</td>
    </tr>`).join(''));
}

// ─── Phase cards ─────────────────────────────────────────────────────────────

function renderPhaseCards() {
  setHTML('phaseCards', data.unit_economics.map(r => `
    <div class="stat-card">
      <div class="text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-3">${r.phase}</div>
      <div class="text-xl font-bold tracking-tight mb-2">${r.assumption}</div>
      <div class="text-sm text-zinc-500 dark:text-zinc-400">${r.driver}</div>
      <div class="text-xs text-zinc-400 mt-1">${r.timing}</div>
    </div>`).join(''));
}

// ─── Accounts & use cases ────────────────────────────────────────────────────

function renderGrowth() {
  const rows = data.year_end_milestones;
  const labels = rows.map(r => `Dec ${r.year}`);

  new Chart(el('accountsChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Enterprise accounts', data: rows.map(r => r.enterprise_accounts), backgroundColor: isDark() ? '#e4e4e7' : '#3f3f46', borderRadius: 6 },
        { label: 'Live use cases',      data: rows.map(r => r.live_use_cases),      backgroundColor: isDark() ? '#6366f1' : '#4f46e5', borderRadius: 6 },
      ]
    },
    options: {
      ...baseChartOpts(fmt.count),
      plugins: {
        ...baseChartOpts(fmt.count).plugins,
        legend: {
          display: true,
          labels: { color: TICK_COLOR(), boxWidth: 12, boxHeight: 12, useBorderRadius: true, borderRadius: 3, font: { size: 11 } }
        }
      }
    }
  });

  setHTML('milestonesRows', rows.map(r => `
    <tr>
      <td class="py-3 text-zinc-700 dark:text-zinc-300">Dec ${r.year}</td>
      <td class="py-3 text-right">${fmt.count(r.enterprise_accounts)}</td>
      <td class="py-3 text-right">${fmt.count(r.live_use_cases)}</td>
      <td class="py-3 text-right font-semibold">${fmt.eur(r.ending_arr)}</td>
    </tr>`).join(''));
}

// ─── Revenue mix & ARR ───────────────────────────────────────────────────────

function renderMix() {
  const rows = data.annual_summary;
  const labels = rows.map(r => `${r.year}E`);

  new Chart(el('revenueMixChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Services & déploiement',  data: rows.map(r => r.services_deployment_revenue),  backgroundColor: isDark() ? '#a1a1aa' : '#d4d4d8', borderRadius: 4 },
        { label: 'Abonnement plateforme',   data: rows.map(r => r.platform_subscription_revenue), backgroundColor: isDark() ? '#6366f1' : '#4f46e5', borderRadius: 4 },
      ]
    },
    options: {
      ...baseChartOpts(fmt.eur),
      scales: {
        ...baseChartOpts(fmt.eur).scales,
        x: { ...baseChartOpts(fmt.eur).scales.x, stacked: true },
        y: { ...baseChartOpts(fmt.eur).scales.y, stacked: true },
      },
      plugins: {
        ...baseChartOpts(fmt.eur).plugins,
        legend: {
          display: true, position: 'bottom',
          labels: { color: TICK_COLOR(), boxWidth: 12, boxHeight: 12, useBorderRadius: true, borderRadius: 3, font: { size: 11 } }
        }
      }
    }
  });

  // ARR line chart — fixed points from revenue_monthly to avoid quarter bug
  const ARR_MONTHS  = ['2026-12-01','2027-06-01','2027-12-01','2028-06-01','2028-12-01'];
  const ARR_LABELS  = ["Dec '26", "Jun '27", "Dec '27", "Jun '28", "Dec '28"];
  const arrRows = ARR_MONTHS.map(m => data.revenue_monthly.find(r => r.month === m)).filter(Boolean);

  new Chart(el('arrChart'), {
    type: 'line',
    data: {
      labels: ARR_LABELS,
      datasets: [{
        label: 'Ending ARR',
        data: arrRows.map(r => r.ending_arr),
        borderColor: isDark() ? '#818cf8' : '#4f46e5',
        backgroundColor: isDark() ? 'rgba(129,140,248,.12)' : 'rgba(79,70,229,.08)',
        borderWidth: 2.5,
        pointBackgroundColor: isDark() ? '#818cf8' : '#4f46e5',
        pointRadius: 5,
        tension: 0.35,
        fill: true,
      }]
    },
    options: baseChartOpts(fmt.eur)
  });

  // Annual table with YoY growth columns
  const fmtMultiple = (a, b) => {
    if (!a || !b || a <= 0) return '—';
    return (b / a).toFixed(1) + '×';
  };
  const metrics = [
    { label: 'Services & déploiement',  fn: r => r.services_deployment_revenue, bold: false },
    { label: 'Abonnement plateforme',   fn: r => r.platform_subscription_revenue, bold: false },
    { label: 'Total revenue',           fn: r => r.total_revenue, bold: true },
    { label: 'Ending ARR',              fn: r => r.ending_arr, bold: false },
    { label: 'Recurring revenue share', fn: r => fmt.pct(r.recurring_revenue_share), bold: false, isStr: true },
    { label: 'Gross margin',            fn: r => fmt.pct(r.gross_margin), bold: false, isStr: true },
  ];
  const mutedCls = 'text-zinc-400 dark:text-zinc-500';
  setHTML('annualRows', metrics.map(({ label, fn, bold, isStr }) => {
    const vals = rows.map(r => fn(r));
    const cells = rows.map((r, i) => {
      const v = vals[i];
      const cell = `<td class="px-4 py-3 text-right font-${bold ? 'semibold' : 'normal'}">${isStr ? v : fmt.eur(v)}</td>`;
      const yoy = (i > 0 && !isStr)
        ? `<td class="px-4 py-3 text-right text-xs ${mutedCls}">${fmtMultiple(vals[i-1], v)}</td>`
        : (i > 0 ? `<td class="px-4 py-3 text-right text-xs ${mutedCls}">—</td>` : '');
      return cell + yoy;
    }).join('');
    return `<tr><td class="px-4 py-3 text-zinc-700 dark:text-zinc-300">${label}</td>${cells}</tr>`;
  }).join(''));
}

// ─── Capacity & cash ─────────────────────────────────────────────────────────

function renderRunway() {
  const caps = data.delivery_capacity.filter(r =>
    r.month.endsWith('-12-01') || ['2026-09-01','2027-06-01','2028-06-01'].includes(r.month));
  const capLabels = caps.map(r => {
    const d = new Date(r.month);
    return `${d.toLocaleDateString('en-US', { month: 'short' })} '${String(d.getFullYear()).slice(2)}`;
  });

  new Chart(el('capacityChart'), {
    type: 'line',
    data: {
      labels: capLabels,
      datasets: [
        {
          label: 'FDE capacity',
          data: caps.map(r => r.fde_capacity_active_use_cases),
          borderColor: isDark() ? '#818cf8' : '#4f46e5',
          backgroundColor: 'transparent',
          borderWidth: 2.5,
          pointRadius: 4,
          tension: 0.3,
        },
        {
          label: 'Active deployments',
          data: caps.map(r => r.active_deployments),
          borderColor: isDark() ? '#e4e4e7' : '#3f3f46',
          backgroundColor: 'transparent',
          borderWidth: 2,
          pointRadius: 4,
          borderDash: [4, 3],
          tension: 0.3,
        }
      ]
    },
    options: {
      ...baseChartOpts(fmt.count),
      plugins: {
        ...baseChartOpts(fmt.count).plugins,
        legend: {
          display: true, position: 'bottom',
          labels: { color: TICK_COLOR(), boxWidth: 12, boxHeight: 12, font: { size: 11 } }
        }
      }
    }
  });

  const cash = data.cash_monthly.filter(r =>
    r.month.endsWith('-12-01') || ['2026-09-01','2027-06-01','2028-06-01'].includes(r.month));
  const cashLabels = cash.map(r => {
    const d = new Date(r.month);
    return `${d.toLocaleDateString('en-US', { month: 'short' })} '${String(d.getFullYear()).slice(2)}`;
  });

  new Chart(el('cashChart'), {
    type: 'line',
    data: {
      labels: cashLabels,
      datasets: [{
        label: 'Ending cash',
        data: cash.map(r => r.ending_cash),
        borderColor: isDark() ? '#e4e4e7' : '#3f3f46',
        backgroundColor: isDark() ? 'rgba(228,228,231,.08)' : 'rgba(63,63,70,.06)',
        borderWidth: 2.5,
        pointBackgroundColor: isDark() ? '#e4e4e7' : '#3f3f46',
        pointRadius: 5,
        tension: 0.35,
        fill: true,
      }]
    },
    options: baseChartOpts(fmt.eur)
  });

  // FDE table
  const capByYear = [2026, 2027, 2028].map(y =>
    data.delivery_capacity.find(r => r.year === y && r.month.endsWith('-12-01')) ||
    data.delivery_capacity.find(r => r.year === y));
  const drivers = { 2026: 'Hands-on deployments', 2027: 'Playbooks & tooling', 2028: 'Self-serve progressif' };
  setHTML('capacityRows', capByYear.map(r => `
    <tr>
      <td class="py-3 text-zinc-700 dark:text-zinc-300">${r.year}</td>
      <td class="py-3 text-right">${Number(r.use_cases_per_fde).toFixed(0)} use cases</td>
      <td class="py-3 text-right text-zinc-500">${drivers[r.year]}</td>
    </tr>`).join(''));

  // Seed allocation
  setHTML('fundsGrid', data.use_of_funds.map(f => `
    <div>
      <div class="flex justify-between text-sm mb-1.5">
        <span class="font-medium">${f.category}</span>
        <span class="text-zinc-500">${fmt.eur(f.amount)} · ${fmt.pct(f.share)}</span>
      </div>
      <div class="h-1.5 rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden">
        <div class="h-full rounded-full bg-zinc-800 dark:bg-zinc-300" style="width:${Math.max(4, f.share * 100)}%"></div>
      </div>
      <div class="text-xs text-zinc-400 mt-1">${f.purpose}</div>
    </div>`).join(''));
}

// ─── TOC active state ────────────────────────────────────────────────────────

function initToc() {
  const links = document.querySelectorAll('.toc a');
  const ids   = [...links].map(a => a.getAttribute('href').slice(1));
  const sections = ids.map(id => document.getElementById(id)).filter(Boolean);

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const link = document.querySelector(`.toc a[href="#${e.target.id}"]`);
        if (link) link.classList.add('active');
      }
    });
  }, { rootMargin: '-30% 0px -60% 0px' });

  sections.forEach(s => obs.observe(s));
}

// ─── Dark mode toggle ────────────────────────────────────────────────────────

el('theme-toggle').addEventListener('click', () => {
  const isDk = document.documentElement.classList.toggle('dark');
  localStorage.theme = isDk ? 'dark' : 'light';
  // Charts don't auto-recolor — simplest UX is to reload
  location.reload();
});

// ─── Init ────────────────────────────────────────────────────────────────────

renderKpis();
renderTrajectory();
renderMonthlyRevenue();

renderPhaseCards();
renderGrowth();
renderMix();
renderRunway();
initToc();
