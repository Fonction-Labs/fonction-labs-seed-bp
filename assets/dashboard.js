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

const GRID_COLOR = () => isDark() ? 'rgba(255,255,255,.07)' : 'rgba(0,0,0,.06)';
const TICK_COLOR = () => isDark() ? '#71717a' : '#a1a1aa';
const INDIGO     = () => isDark() ? '#818cf8' : '#4f46e5';
const DARK_BAR   = () => isDark() ? '#e4e4e7' : '#18181b';
const GRAY_BAR   = () => isDark() ? '#71717a' : '#a1a1aa';
const GREEN      = () => isDark() ? '#4ade80' : '#16a34a';
const AMBER      = () => isDark() ? '#fbbf24' : '#d97706';
const TEAL       = () => isDark() ? '#5eead4' : '#0d9488';
const ROSE       = () => isDark() ? '#fb7185' : '#e11d48';

const baseChartOpts = (yFmt) => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: isDark() ? '#18181b' : '#fff',
      titleColor: isDark() ? '#f4f4f5' : '#18181b',
      bodyColor: isDark() ? '#d4d4d8' : '#3f3f46',
      borderColor: isDark() ? '#3f3f46' : '#e4e4e7',
      borderWidth: 1, padding: 10,
      callbacks: { label: ctx => ` ${ctx.dataset.label}: ${yFmt(ctx.parsed.y)}` }
    }
  },
  scales: {
    x: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, font: { size: 11 } } },
    y: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, font: { size: 11 }, callback: yFmt }, border: { display: false } }
  }
});

// ─── Intro paragraphs ────────────────────────────────────────────────────────

function renderIntros() {
  const a = data.annual_summary || [];
  const y26 = a.find(r => r.year === 2026) || {};
  const y27 = a.find(r => r.year === 2027) || {};
  const y28 = a.find(r => r.year === 2028) || {};
  const mil27 = (data.year_end_milestones || []).find(r => r.year === 2027) || {};
  const cash = data.cash_monthly || [];
  const lastCash = cash[cash.length - 1] || {};
  const inv = (data.kpis || []).find(k => k.metric === 'Invoiced revenue H1 2026');

  const p = (id, text) => { const e = el(id); if (e) e.textContent = text; };

  p('kpisIntro',
    `En H1 2026, Fonction Labs a facturé ${inv ? fmt.eur(inv.value) : '—'} sans levée de fonds, ` +
    `validant la demande enterprise. Le modèle projette ${fmt.eur(y27.total_revenue)} de revenue en 2027 ` +
    `(×${y26.total_revenue ? (y27.total_revenue / y26.total_revenue).toFixed(1) : '—'}) ` +
    `et ${fmt.eur(y28.total_revenue)} en 2028, porté par la montée en puissance de l'abonnement plateforme.`
  );

  p('revenueIntro',
    `H1 2026 est intégralement basé sur des factures réelles (${inv ? fmt.eur(inv.value) : '—'}). ` +
    `À partir de juillet, le forecast modélise la signature de nouveaux comptes enterprise et l'expansion des use cases live. ` +
    `L'ARR passe de ${fmt.eur(y26.ending_arr)} fin 2026 à ${fmt.eur(mil27.ending_arr)} fin 2027, ` +
    `avec ${fmt.count(mil27.enterprise_accounts)} comptes et ${fmt.count(mil27.live_use_cases)} use cases live.`
  );

  p('marginsIntro',
    `La marge brute est calculée bottom-up : salaires FDE, freelances & partenaires, tokens clients et infra cloud. ` +
    `Elle progresse de ${fmt.pct(y26.gross_margin)} en 2026 à ${fmt.pct(y27.gross_margin)} en 2027 ` +
    `puis ${fmt.pct(y28.gross_margin)} en 2028, reflétant la montée du revenu plateforme à marge élevée dans le mix.`
  );

  const uof = data.use_of_funds || [];
  const seed = uof.reduce((s, f) => s + f.amount, 0);
  p('runwayIntro',
    `La levée seed de ${fmt.eur(seed)} finance 30+ mois d'exécution. ` +
    `Le cash reste positif sur tout l'horizon du plan — ` +
    `${fmt.eur(lastCash.ending_cash)} projeté en fin de période. ` +
    `L'allocation priorise la capacité de déploiement (FDE) et le développement produit, ` +
    `qui représentent ensemble 60% du budget.`
  );
}

// ─── KPIs — 3 groupes narratifs ──────────────────────────────────────────────

function renderKpis() {
  function getKpi(name) { return data.kpis.find(k => k.metric === name); }
  function kpiVal(k) {
    if (!k) return '—';
    return k.unit === 'EUR' ? fmt.eur(k.value) : k.unit === 'pct' ? fmt.pct(k.value) : fmt.count(k.value);
  }

  const rev26 = getKpi('2026E revenue');
  const rev27 = getKpi('2027E revenue');
  const rev28 = getKpi('2028E revenue');
  const mil27 = data.year_end_milestones.find(r => r.year === 2027);
  const mil28 = data.year_end_milestones.find(r => r.year === 2028);

  const groups = [
    {
      label: 'Traction H1 2026',
      items: [
        { label: 'Revenue facturé H1', val: kpiVal(getKpi('Invoiced revenue H1 2026')), sub: 'Actuals sans levée de fonds' },
        { label: 'Seed raise', val: kpiVal(getKpi('Seed raise')), sub: 'Tour en cours' },
      ]
    },
    {
      label: 'Cible seed — 2027',
      accent: true,
      items: [
        { label: 'Revenue 2027E', val: kpiVal(rev27), sub: rev26 ? `×${(rev27.value/rev26.value).toFixed(1)} vs 2026` : '' },
        { label: 'ARR Dec-2027', val: kpiVal(getKpi('Ending ARR Dec-2027')), sub: `${mil27 ? fmt.count(mil27.enterprise_accounts) : '—'} comptes · ${mil27 ? fmt.count(mil27.live_use_cases) : '—'} UC live` },
        { label: 'Gross margin 2027', val: kpiVal(getKpi('Gross margin 2027')), sub: 'Bottom-up COGS' },
        { label: 'Cash Dec-2027', val: kpiVal(getKpi('Ending cash Dec-2027')), sub: '30+ mois runway' },
      ]
    },
    {
      label: 'Échelle — 2028',
      items: [
        { label: 'Revenue 2028E', val: kpiVal(rev28), sub: rev27 ? `×${(rev28.value/rev27.value).toFixed(1)} vs 2027` : '' },
        { label: 'ARR Dec-2028', val: mil28 ? fmt.eur(mil28.ending_arr) : '—', sub: `${mil28 ? fmt.count(mil28.enterprise_accounts) : '—'} comptes · ${mil28 ? fmt.count(mil28.live_use_cases) : '—'} UC live` },
      ]
    },
  ];

  setHTML('kpiGrid', groups.map(g => `
    <div class="mb-4">
      <div class="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2 px-1">${g.label}</div>
      <div class="grid grid-cols-2 sm:grid-cols-${g.items.length > 2 ? 4 : 2} divide-x divide-zinc-200 dark:divide-zinc-800 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden">
        ${g.items.map((item, i) => `
          <div class="px-5 py-4 ${g.accent ? (i === 0 ? 'bg-zinc-900 dark:bg-zinc-800' : 'bg-zinc-50 dark:bg-zinc-900/50') : 'bg-white dark:bg-zinc-950'}">
            <div class="text-xs text-zinc-500 ${g.accent && i === 0 ? 'text-zinc-400' : ''} mb-1.5 truncate">${item.label}</div>
            <div class="text-2xl font-bold tracking-tight leading-none ${g.accent && i === 0 ? 'text-white' : ''}">${item.val}</div>
            <div class="text-xs mt-2 text-zinc-400">${item.sub}</div>
          </div>`).join('')}
      </div>
    </div>`).join(''));
}

// ─── Business Model Phases + hypothèses par phase ────────────────────────────

const PHASE_ASSUMPTIONS = {
  current: {
    title: 'Hypothèses — Modèle actuel',
    groups: [
      {
        label: 'Pricing entrée',
        items: [
          { label: 'Workshop cadrage', key: 'workshop_fee', fmt: v => `${(v/1000).toFixed(0)}k€ / nouveau client` },
          { label: 'Déploiement 0→1', key: 'deployment_fee_per_uc', fmt: v => `${(v/1000).toFixed(0)}k€ / UC` },
          { label: 'Durée déploiement', key: 'deployment_duration_months', fmt: v => `${v} mois` },
        ]
      },
      {
        label: 'FDE & delivery',
        items: [
          { label: 'TJM FDE facturable', key: 'fde_billable_day_rate', fmt: v => `${v.toLocaleString('fr-FR')}€ /jour` },
          { label: 'Token cost / UC', key: 'avg_token_cost_per_uc', fmt: v => `${v}€ /mois` },
        ]
      },
    ]
  },
  transition: {
    title: 'Hypothèses — Modèle transitoire',
    groups: [
      {
        label: 'Abonnement per-UC',
        items: [
          { label: 'ETI (~100M CA)', key: 'seg_ETI', fmt: v => `${v.toLocaleString('fr-FR')}€ /UC/mois` },
          { label: 'Grand Compte (~1Md CA)', key: 'seg_GC', fmt: v => `${v.toLocaleString('fr-FR')}€ /UC/mois` },
          { label: 'TGC (~40Md CA)', key: 'seg_TGC', fmt: v => `${v.toLocaleString('fr-FR')}€ /UC/mois` },
        ]
      },
      {
        label: 'Objectifs intermédiaires',
        items: [
          { label: 'Comptes fin 2027', key: 'accounts_2027', fmt: v => `${v} comptes` },
          { label: 'UC live fin 2027', key: 'uc_2027', fmt: v => `${v} use cases` },
          { label: 'ARR cible Dec 2027', key: 'arr_2027', fmt: v => `${(v/1e6).toFixed(1)}M€` },
        ]
      },
    ]
  },
  target: {
    title: 'Hypothèses — Modèle cible',
    groups: [
      {
        label: 'Plateforme',
        items: [
          { label: 'Modèle facturation', key: null, static: 'Abonnement léger + crédits prépayés' },
          { label: 'NRR cible', key: null, static: '> 130%' },
          { label: 'Marge plateforme', key: null, static: '80%+ (SaaS pure)' },
        ]
      },
      {
        label: 'Échelle 2028',
        items: [
          { label: 'Comptes fin 2028', key: 'accounts_2028', fmt: v => `${v} comptes` },
          { label: 'UC live fin 2028', key: 'uc_2028', fmt: v => `${v} use cases` },
          { label: 'ARR cible Dec 2028', key: 'arr_2028', fmt: v => `${(v/1e6).toFixed(1)}M€` },
        ]
      },
    ]
  },
};

function renderModelPhases() {
  const phases = data.business_model_phases;
  if (!phases) return;

  const a = data.key_assumptions || {};
  const seg = a.segment_pricing || {};
  const mil27 = (data.year_end_milestones || []).find(r => r.year === 2027) || {};
  const mil28 = (data.year_end_milestones || []).find(r => r.year === 2028) || {};

  const vals = {
    workshop_fee: a.workshop_fee,
    deployment_fee_per_uc: a.deployment_fee_per_uc,
    deployment_duration_months: a.deployment_duration_months,
    fde_billable_day_rate: a.fde_billable_day_rate,
    avg_token_cost_per_uc: a.avg_token_cost_per_uc,
    seg_ETI: seg.ETI,
    seg_GC: seg.GC,
    seg_TGC: seg.TGC,
    accounts_2027: mil27.enterprise_accounts,
    uc_2027: mil27.live_use_cases,
    arr_2027: mil27.ending_arr,
    accounts_2028: mil28.enterprise_accounts,
    uc_2028: mil28.live_use_cases,
    arr_2028: mil28.ending_arr,
  };

  const statusBadge = (s) => {
    const cls = s === 'active' ? 'phase-active' : s === 'next' ? 'phase-next' : 'phase-planned';
    const label = s === 'active' ? 'Actif' : s === 'next' ? 'En cours' : 'Cible';
    return `<span class="phase-badge ${cls}">${label}</span>`;
  };

  const renderAssumptionDrawer = (phaseId) => {
    const def = PHASE_ASSUMPTIONS[phaseId];
    if (!def) return '';
    const rows = def.groups.map(g => `
      <div>
        <div class="text-xs font-semibold uppercase tracking-wide text-zinc-400 dark:text-zinc-500 mb-2">${g.label}</div>
        <div class="space-y-1.5">
          ${g.items.map(item => {
            const v = item.static !== undefined ? item.static : (item.key && vals[item.key] != null ? item.fmt(vals[item.key]) : '—');
            return `<div class="flex justify-between items-baseline gap-4 text-sm">
              <span class="text-zinc-500 dark:text-zinc-400">${item.label}</span>
              <span class="font-medium text-zinc-900 dark:text-zinc-100 whitespace-nowrap">${v}</span>
            </div>`;
          }).join('')}
        </div>
      </div>`).join('');
    return `
      <div id="drawer-${phaseId}" class="hidden mt-4 pt-4 border-t border-zinc-200 dark:border-zinc-700">
        <div class="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">${def.title}</div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">${rows}</div>
      </div>`;
  };

  setHTML('modelPhases', phases.map(p => `
    <div class="stat-card cursor-pointer select-none" onclick="togglePhaseDrawer('${p.id}', this)">
      <div class="flex items-center gap-3 mb-3">
        ${statusBadge(p.status)}
        <h3 class="font-semibold text-base">${p.name}</h3>
        <span class="text-xs text-zinc-400 ml-auto mr-2">${p.period}</span>
        <span id="arrow-${p.id}" class="text-xs text-zinc-400 transition-transform">▸ Hypothèses</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
        <div>
          <div class="text-xs text-zinc-400 uppercase tracking-wide mb-1">Modèle de revenu</div>
          <div class="text-zinc-700 dark:text-zinc-300">${p.revenue_model}</div>
        </div>
        <div>
          <div class="text-xs text-zinc-400 uppercase tracking-wide mb-1">Pricing</div>
          <div class="text-zinc-700 dark:text-zinc-300 font-medium">${p.pricing}</div>
        </div>
        <div>
          <div class="text-xs text-zinc-400 uppercase tracking-wide mb-1">Profil de marge</div>
          <div class="text-zinc-700 dark:text-zinc-300">${p.margin_profile}</div>
        </div>
      </div>
      <div class="mt-3 text-xs text-zinc-500">KPI principal : ${p.key_metric}</div>
      ${renderAssumptionDrawer(p.id)}
    </div>`).join(''));
}

function togglePhaseDrawer(id, card) {
  const drawer = document.getElementById(`drawer-${id}`);
  const arrow = document.getElementById(`arrow-${id}`);
  if (!drawer) return;
  const open = !drawer.classList.contains('hidden');
  drawer.classList.toggle('hidden', open);
  if (arrow) arrow.textContent = open ? '▸ Hypothèses' : '▾ Hypothèses';
}

// ─── Revenue (unified section) ───────────────────────────────────────────────

function renderRevenue() {
  const years = data.annual_summary;
  const milestones = data.year_end_milestones;
  const themes = data.trajectory;

  const get = (year) => ({
    theme:   themes.find(t => t.year === year),
    summary: years.find(r => r.year === year),
    mile:    milestones.find(r => r.year === year),
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
        <tr class="${borderCls}"><td class="${labelCls}">Revenue</td>${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800 font-semibold">${fmt.eur(c.summary.total_revenue)}</td>`).join('')}</tr>
        <tr class="${borderCls}"><td class="${labelCls}">Ending ARR</td>${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800 font-semibold">${fmt.eur(c.mile.ending_arr)}</td>`).join('')}</tr>
        <tr class="${borderCls}"><td class="${labelCls}">Comptes</td>${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800">${fmt.count(c.mile.enterprise_accounts)}</td>`).join('')}</tr>
        <tr class="${borderCls}"><td class="${labelCls}">Use cases live</td>${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800">${fmt.count(c.mile.live_use_cases)}</td>`).join('')}</tr>
        <tr class="${borderCls}"><td class="${labelCls}">Gross margin</td>${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800">${fmt.pct(c.summary.gross_margin)}</td>`).join('')}</tr>
        <tr class="${borderCls}"><td class="${labelCls}"></td>${cols.map(c => `<td class="${cellCls} border-l border-zinc-200 dark:border-zinc-800 text-zinc-500 dark:text-zinc-400 text-xs leading-relaxed">${c.theme.text}</td>`).join('')}</tr>
      </tbody>
    </table>`);

  // Monthly revenue chart — all 36 months
  const months = data.revenue_monthly;
  const labels = months.map(m => {
    const d = new Date(m.month);
    return d.getMonth() === 0 ? d.getFullYear().toString() : d.toLocaleDateString('fr-FR', { month: 'short' });
  });

  const actualVals   = months.map(m => m.actual_services_revenue   || 0);
  const forecastVals = months.map(m => m.forecast_services_revenue || 0);
  const platformVals = months.map(m => m.platform_subscription_revenue || 0);

  new Chart(el('revenueChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Actuals (facturé)', data: actualVals,   backgroundColor: DARK_BAR(), borderRadius: 3 },
        { label: 'Forecast',          data: forecastVals, backgroundColor: GRAY_BAR(), borderRadius: 3 },
        { label: 'Plateforme',        data: platformVals, backgroundColor: INDIGO(),   borderRadius: 3 },
      ]
    },
    options: {
      ...baseChartOpts(fmt.eur),
      scales: {
        ...baseChartOpts(fmt.eur).scales,
        x: { ...baseChartOpts(fmt.eur).scales.x, stacked: true, ticks: { ...baseChartOpts(fmt.eur).scales.x.ticks, maxRotation: 0 } },
        y: { ...baseChartOpts(fmt.eur).scales.y, stacked: true },
      },
      plugins: {
        ...baseChartOpts(fmt.eur).plugins,
        legend: { display: true, position: 'bottom', labels: { color: TICK_COLOR(), boxWidth: 12, boxHeight: 12, useBorderRadius: true, borderRadius: 3, font: { size: 11 } } },
        tooltip: { ...baseChartOpts(fmt.eur).plugins.tooltip, filter: (item) => item.parsed.y > 0 }
      }
    }
  });

  // ARR line chart
  const ARR_MONTHS = ['2026-12-01','2027-06-01','2027-12-01','2028-06-01','2028-12-01'];
  const ARR_LABELS = ["Dec '26", "Jun '27", "Dec '27", "Jun '28", "Dec '28"];
  const arrRows = ARR_MONTHS.map(m => months.find(r => r.month === m)).filter(Boolean);

  new Chart(el('arrChart'), {
    type: 'line',
    data: {
      labels: ARR_LABELS,
      datasets: [{
        label: 'Ending ARR',
        data: arrRows.map(r => r.ending_arr),
        borderColor: INDIGO(),
        backgroundColor: isDark() ? 'rgba(129,140,248,.12)' : 'rgba(79,70,229,.08)',
        borderWidth: 2.5, pointBackgroundColor: INDIGO(), pointRadius: 5, tension: 0.35, fill: true,
      }]
    },
    options: baseChartOpts(fmt.eur)
  });

  // Revenue mix stacked
  new Chart(el('revenueMixChart'), {
    type: 'bar',
    data: {
      labels: years.map(r => `${r.year}E`),
      datasets: [
        { label: 'Services & déploiement', data: years.map(r => r.services_deployment_revenue), backgroundColor: GRAY_BAR(), borderRadius: 4 },
        { label: 'Abonnement plateforme',  data: years.map(r => r.platform_subscription_revenue), backgroundColor: INDIGO(), borderRadius: 4 },
      ]
    },
    options: {
      ...baseChartOpts(fmt.eur),
      scales: { ...baseChartOpts(fmt.eur).scales, x: { ...baseChartOpts(fmt.eur).scales.x, stacked: true }, y: { ...baseChartOpts(fmt.eur).scales.y, stacked: true } },
      plugins: { ...baseChartOpts(fmt.eur).plugins, legend: { display: true, position: 'bottom', labels: { color: TICK_COLOR(), boxWidth: 12, boxHeight: 12, useBorderRadius: true, borderRadius: 3, font: { size: 11 } } } }
    }
  });

  // Annual table
  const fmtMultiple = (a, b) => (!a || !b || a <= 0) ? '—' : (b / a).toFixed(1) + '×';
  const metrics = [
    { label: 'Services & déploiement', fn: r => r.services_deployment_revenue },
    { label: 'Abonnement plateforme',  fn: r => r.platform_subscription_revenue },
    { label: 'Total revenue',          fn: r => r.total_revenue, bold: true },
    { label: 'Ending ARR',             fn: r => r.ending_arr },
    { label: 'Enterprise accounts',    fn: r => r.enterprise_accounts_end, isCount: true },
    { label: 'Live use cases',         fn: r => r.live_use_cases, isCount: true },
    { label: 'Recurring share',        fn: r => fmt.pct(r.recurring_revenue_share), isStr: true },
    { label: 'Gross margin',           fn: r => fmt.pct(r.gross_margin), isStr: true },
  ];
  const mutedCls = 'text-zinc-400 dark:text-zinc-500';
  setHTML('annualRows', metrics.map(({ label, fn, bold, isStr, isCount }) => {
    const vals = years.map(r => fn(r));
    const cells = years.map((r, i) => {
      const v = vals[i];
      const display = isStr ? v : isCount ? fmt.count(v) : fmt.eur(v);
      const cell = `<td class="px-4 py-3 text-right ${bold ? 'font-semibold' : ''}">${display}</td>`;
      const yoy = (i > 0 && !isStr && !isCount)
        ? `<td class="px-4 py-3 text-right text-xs ${mutedCls}">${fmtMultiple(vals[i-1], v)}</td>`
        : (i > 0 ? `<td class="px-4 py-3 text-right text-xs ${mutedCls}">—</td>` : '');
      return cell + yoy;
    }).join('');
    return `<tr><td class="px-4 py-3 text-zinc-700 dark:text-zinc-300">${label}</td>${cells}</tr>`;
  }).join(''));
}

// ─── Margins & COGS ──────────────────────────────────────────────────────────

function renderMargins() {
  const gm = data.gross_margin_monthly || [];
  const qLabels = [], qGM = [];
  for (const year of [2026, 2027, 2028]) {
    for (const q of [1, 2, 3, 4]) {
      const qMonths = gm.filter(r => r.year === year && Math.floor((new Date(r.month).getMonth()) / 3) + 1 === q);
      if (!qMonths.length) continue;
      const rev = qMonths.reduce((s, r) => s + (r.total_revenue || 0), 0);
      const cogs = qMonths.reduce((s, r) => s + (r.total_cogs || 0), 0);
      if (rev > 0) { qLabels.push(`Q${q} '${String(year).slice(2)}`); qGM.push((rev - cogs) / rev); }
    }
  }

  new Chart(el('grossMarginChart'), {
    type: 'line',
    data: {
      labels: qLabels,
      datasets: [{
        label: 'Gross Margin',
        data: qGM,
        borderColor: GREEN(), backgroundColor: isDark() ? 'rgba(74,222,128,.1)' : 'rgba(22,163,74,.08)',
        borderWidth: 2.5, pointBackgroundColor: GREEN(), pointRadius: 4, tension: 0.3, fill: true,
      }]
    },
    options: { ...baseChartOpts(fmt.pct), scales: { ...baseChartOpts(fmt.pct).scales, y: { ...baseChartOpts(fmt.pct).scales.y, min: 0, max: 1 } } }
  });

  // COGS stacked bar — freelance_cost + service_continuity_cogs fusionnés en "Freelance & partenaires"
  const cogsData = data.cogs_monthly || [];
  const cogsYears = [2026, 2027, 2028];
  const cogsByYear = cogsYears.map(y => {
    const rows = cogsData.filter(r => r.year === y);
    return {
      fde:       rows.reduce((s, r) => s + (r.fde_cost || 0), 0),
      freelance: rows.reduce((s, r) => s + (r.freelance_cost || 0) + (r.service_continuity_cogs || 0), 0),
      tokens:    rows.reduce((s, r) => s + (r.token_cost || 0), 0),
      infra:     rows.reduce((s, r) => s + (r.infra_cloud_cost || 0), 0),
    };
  });

  new Chart(el('cogsChart'), {
    type: 'bar',
    data: {
      labels: cogsYears.map(y => `${y}E`),
      datasets: [
        { label: 'FDE (salaires)',          data: cogsByYear.map(c => c.fde),       backgroundColor: DARK_BAR(), borderRadius: 3 },
        { label: 'Freelance & partenaires', data: cogsByYear.map(c => c.freelance), backgroundColor: AMBER(),    borderRadius: 3 },
        { label: 'Infra cloud',             data: cogsByYear.map(c => c.infra),     backgroundColor: INDIGO(),   borderRadius: 3 },
        { label: 'Tokens clients',          data: cogsByYear.map(c => c.tokens),    backgroundColor: TEAL(),     borderRadius: 3 },
      ]
    },
    options: {
      ...baseChartOpts(fmt.eur),
      scales: { ...baseChartOpts(fmt.eur).scales, x: { ...baseChartOpts(fmt.eur).scales.x, stacked: true }, y: { ...baseChartOpts(fmt.eur).scales.y, stacked: true } },
      plugins: { ...baseChartOpts(fmt.eur).plugins, legend: { display: true, position: 'bottom', labels: { color: TICK_COLOR(), boxWidth: 12, boxHeight: 12, useBorderRadius: true, borderRadius: 3, font: { size: 11 } } } }
    }
  });

  // Margins table
  const annual = data.annual_summary;
  const marginRows = [
    { label: 'Revenue', fn: r => r.total_revenue, bold: true },
    { label: 'Total COGS', fn: r => r.total_cogs },
    { label: 'Gross Profit', fn: r => r.gross_profit, bold: true },
    { label: 'Gross Margin', fn: r => fmt.pct(r.gross_margin), isStr: true },
  ];
  setHTML('marginsRows', marginRows.map(({ label, fn, bold, isStr }) => {
    const cells = annual.map(r => `<td class="px-4 py-3 text-right ${bold ? 'font-semibold' : ''}">${isStr ? fn(r) : fmt.eur(fn(r))}</td>`).join('');
    return `<tr><td class="px-4 py-3 text-zinc-700 dark:text-zinc-300">${label}</td>${cells}</tr>`;
  }).join(''));
}

// ─── Runway & team ───────────────────────────────────────────────────────────

function renderRunway() {
  // Cash — tous les mois
  const cash = data.cash_monthly;
  const cashLabels = cash.map(r => {
    const d = new Date(r.month);
    return d.getMonth() === 0
      ? d.getFullYear().toString()
      : d.toLocaleDateString('fr-FR', { month: 'short' });
  });

  new Chart(el('cashChart'), {
    type: 'line',
    data: {
      labels: cashLabels,
      datasets: [{
        label: 'Cash disponible',
        data: cash.map(r => r.ending_cash),
        borderColor: DARK_BAR(),
        backgroundColor: isDark() ? 'rgba(228,228,231,.08)' : 'rgba(63,63,70,.06)',
        borderWidth: 2, pointRadius: 0, pointHoverRadius: 4, tension: 0.3, fill: true,
      }]
    },
    options: {
      ...baseChartOpts(fmt.eur),
      scales: {
        ...baseChartOpts(fmt.eur).scales,
        x: { ...baseChartOpts(fmt.eur).scales.x, ticks: { ...baseChartOpts(fmt.eur).scales.x.ticks, maxRotation: 0, maxTicksLimit: 12 } },
      }
    }
  });

  // Headcount — stacked bar par fonction, tous les mois
  const hcFn = data.headcount_by_function_monthly || [];
  const hcLabels = hcFn.map(r => {
    const d = new Date(r.month);
    return d.getMonth() === 0
      ? d.getFullYear().toString()
      : d.toLocaleDateString('fr-FR', { month: 'short' });
  });

  const fnColors = {
    founders:            DARK_BAR(),
    product_engineering: INDIGO(),
    fde:                 TEAL(),
    sales_gtm:           AMBER(),
    ops:                 ROSE(),
  };
  const fnLabels = {
    founders:            'Fondateurs',
    product_engineering: 'Product & Engineering',
    fde:                 'Forward-Deployed Engineering',
    sales_gtm:           'Sales & GTM',
    ops:                 'Ops',
  };

  if (el('headcountChart') && hcFn.length > 0) {
    new Chart(el('headcountChart'), {
      type: 'bar',
      data: {
        labels: hcLabels,
        datasets: Object.keys(fnColors).map(key => ({
          label: fnLabels[key],
          data: hcFn.map(r => r[key] || 0),
          backgroundColor: fnColors[key],
          borderRadius: 2,
        }))
      },
      options: {
        ...baseChartOpts(fmt.count),
        scales: {
          ...baseChartOpts(fmt.count).scales,
          x: { ...baseChartOpts(fmt.count).scales.x, stacked: true, ticks: { ...baseChartOpts(fmt.count).scales.x.ticks, maxRotation: 0, maxTicksLimit: 12 } },
          y: { ...baseChartOpts(fmt.count).scales.y, stacked: true },
        },
        plugins: {
          ...baseChartOpts(fmt.count).plugins,
          legend: { display: true, position: 'bottom', labels: { color: TICK_COLOR(), boxWidth: 12, boxHeight: 12, useBorderRadius: true, borderRadius: 3, font: { size: 11 } } },
        }
      }
    });
  }

  // Seed allocation
  setHTML('fundsGrid', data.use_of_funds.map(f => `
    <div>
      <div class="flex items-baseline justify-between gap-4 mb-1.5">
        <span class="text-sm font-medium">${f.category}</span>
        <span class="text-sm font-semibold tabular-nums">${fmt.eur(f.amount)}</span>
      </div>
      <div class="h-2 rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden mb-1">
        <div class="h-full rounded-full bg-zinc-800 dark:bg-zinc-300 transition-all" style="width:${Math.max(4, Math.round(f.share * 100))}%"></div>
      </div>
      <div class="flex justify-between text-xs text-zinc-400">
        <span>${f.purpose}</span>
        <span>${Math.round(f.share * 100)}%</span>
      </div>
    </div>`).join(''));
}

// ─── TOC ─────────────────────────────────────────────────────────────────────

function initToc() {
  const links = document.querySelectorAll('.toc a');
  const ids = [...links].map(a => a.getAttribute('href').slice(1));
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
  document.documentElement.classList.toggle('dark');
  localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  location.reload();
});

// ─── Init ────────────────────────────────────────────────────────────────────

renderIntros();
renderKpis();
renderModelPhases();
renderRevenue();
renderMargins();
renderRunway();
initToc();
