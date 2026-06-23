const data = window.DASHBOARD_DATA;

const fmt = {
  eur(v) {
    const n = Number(v || 0);
    if (Math.abs(n) >= 1_000_000) return (n / 1_000_000).toFixed(1).replace('.0', '') + 'M€';
    if (Math.abs(n) >= 1_000) return Math.round(n / 1_000) + 'k€';
    return Math.round(n) + '€';
  },
  count(v) { return String(Math.round(Number(v || 0))); },
  pct(v) { return Math.round(Number(v || 0) * 100) + '%'; },
  monthLabel(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', { month: 'short' });
  },
  periodLabel(iso) {
    const d = new Date(iso);
    const mon = d.toLocaleDateString('en-US', { month: 'short' });
    const yr = String(d.getFullYear()).slice(2);
    return `${mon} '${yr}`;
  }
};

function getKpi(name) { return data.kpis.find(k => k.metric === name); }
function kpiValue(k) { return k.unit === 'EUR' ? fmt.eur(k.value) : fmt.count(k.value); }
function setHTML(id, html) { const el = document.getElementById(id); if (el) el.innerHTML = html; }
function svg(width, height, inner) { return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-hidden="true">${inner}</svg>`; }

function renderKpis() {
  const items = [
    { metric: 'Actual commercial revenue Jan-Jun 2026', sub: 'Chiffre d\'affaires commercial H1', dark: true },
    { metric: '2026E revenue',               sub: 'Revenu annuel total 2026E' },
    { metric: '2027E revenue',               sub: 'Services, déploiement et abonnement' },
    { metric: 'Ending ARR Dec-2027',         sub: 'Run-rate abonnement annualisé' },
    { metric: 'Enterprise accounts Dec-2027',sub: 'Comptes enterprise activés' },
    { metric: 'Live use cases Dec-2027',     sub: 'Use cases en abonnement' },
    { metric: '2028E revenue',               sub: 'Croissance par expansion compte', computed: true },
    { metric: 'Ending ARR Dec-2028',         sub: 'Run-rate abonnement annualisé', computed: true },
  ];
  setHTML('kpis', items.map(item => {
    let val;
    if (item.computed && item.metric === '2028E revenue') {
      const row = data.annual_summary.find(r => r.year === 2028);
      val = row ? fmt.eur(row.total_revenue) : '—';
    } else if (item.computed && item.metric === 'Ending ARR Dec-2028') {
      const row = data.year_end_milestones.find(r => r.year === 2028);
      val = row ? fmt.eur(row.ending_arr) : '—';
    } else {
      const k = getKpi(item.metric);
      val = k ? kpiValue(k) : '—';
    }
    return `<div class="kpi-card${item.dark ? ' feature' : ''}"><p>${item.metric}</p><strong>${val}</strong><span>${item.sub}</span></div>`;
  }).join(''));
}

function renderTrajectory() {
  setHTML('trajectoryCards', data.trajectory.map(t => `
    <article class="trajectory-card">
      <span class="year">${t.year}</span>
      <h3>${t.theme}</h3>
      <p>${t.text}</p>
    </article>`).join(''));
}

function renderMonthlyRevenue() {
  const months = data.revenue_monthly.filter(r => r.year === 2026);
  const max = Math.max(...months.map(r => r.total_revenue));
  const W = 760, H = 300, L = 42, R = 18, T = 20, B = 48;
  const chartW = W - L - R, chartH = H - T - B;
  const bw = chartW / months.length * 0.58;
  const gap = chartW / months.length;
  const y = v => T + chartH - (v / max) * chartH;
  const lines = [0, .25, .5, .75, 1].map(p => `<line class="grid-line" x1="${L}" x2="${W-R}" y1="${T + chartH - p*chartH}" y2="${T + chartH - p*chartH}"/>`).join('');
  const bars = months.map((m, i) => {
    const x = L + i * gap + (gap - bw) / 2;
    const yy = y(m.total_revenue);
    const h = T + chartH - yy;
    const actual = i < 6;
    return `<rect x="${x}" y="${yy}" width="${bw}" height="${h}" rx="7" fill="${actual ? '#111111' : '#9a958b'}"/>
      <text class="bar-label" x="${x + bw/2}" y="${H-22}" text-anchor="middle">${fmt.monthLabel(m.month)}</text>
      <text class="value-label" x="${x + bw/2}" y="${Math.max(12, yy-7)}" text-anchor="middle">${fmt.eur(m.total_revenue)}</text>`;
  }).join('');
  setHTML('monthlyRevenueChart', svg(W, H, lines + bars));

  const janJun = months.slice(0,6).reduce((s,r)=>s+r.total_revenue,0);
  const julDec = months.slice(6).reduce((s,r)=>s+r.total_revenue,0);
  const total = janJun + julDec;
  const svcH1 = months.slice(0,6).reduce((s,r)=>s+r.services_deployment_revenue,0);
  const svcH2 = months.slice(6).reduce((s,r)=>s+r.services_deployment_revenue,0);
  const subH1 = months.slice(0,6).reduce((s,r)=>s+r.platform_subscription_revenue,0);
  const subH2 = months.slice(6).reduce((s,r)=>s+r.platform_subscription_revenue,0);
  setHTML('revenue2026Table', `
    <table class="summary-table"><thead><tr><th>Metric</th><th>Jan–Jun</th><th>Jul–Dec</th><th>2026E</th></tr></thead><tbody>
      <tr><td>Commercial revenue</td><td>${fmt.eur(janJun)}</td><td>${fmt.eur(julDec)}</td><td>${fmt.eur(total)}</td></tr>
      <tr><td>Services &amp; deployment revenue</td><td>${fmt.eur(svcH1)}</td><td>${fmt.eur(svcH2)}</td><td>${fmt.eur(svcH1+svcH2)}</td></tr>
      <tr><td>Platform subscription revenue</td><td>${fmt.eur(subH1)}</td><td>${fmt.eur(subH2)}</td><td>${fmt.eur(subH1+subH2)}</td></tr>
    </tbody></table>`);
}

function renderUnitEconomics() {
  setHTML('unitEconomics', data.unit_economics.map(r => `
    <div class="phase-card">
      <span class="phase-label">${r.phase}</span>
      <strong>${r.assumption}</strong>
      <span>${r.driver} · ${r.timing}</span>
    </div>`).join(''));
}

function renderAccountsUseCases() {
  const rows = data.year_end_milestones;
  const max = Math.max(...rows.flatMap(r => [r.enterprise_accounts, r.live_use_cases]));
  const W=620,H=270,L=40,R=20,T=20,B=42, chartW=W-L-R, chartH=H-T-B;
  const gap = chartW / rows.length;
  const bw = gap * .22;
  const y = v => T + chartH - (v/max)*chartH;
  const grid = [0,.25,.5,.75,1].map(p=>`<line class="grid-line" x1="${L}" x2="${W-R}" y1="${T+chartH-p*chartH}" y2="${T+chartH-p*chartH}"/>`).join('');
  const bars = rows.map((r,i)=>{
    const base = L + i*gap + gap/2;
    const yA = y(r.enterprise_accounts), hA = T+chartH-yA;
    const yU = y(r.live_use_cases), hU = T+chartH-yU;
    return `<rect x="${base-bw-3}" y="${yA}" width="${bw}" height="${hA}" rx="6" fill="#111"/>
      <rect x="${base+3}" y="${yU}" width="${bw}" height="${hU}" rx="6" fill="#2f45ff"/>
      <text class="value-label" x="${base-bw/2-3}" y="${Math.max(12,yA-7)}" text-anchor="middle">${fmt.count(r.enterprise_accounts)}</text>
      <text class="value-label" x="${base+bw/2+3}" y="${Math.max(12,yU-7)}" text-anchor="middle">${fmt.count(r.live_use_cases)}</text>
      <text class="bar-label" x="${base}" y="${H-18}" text-anchor="middle">Dec ${r.year}</text>`;
  }).join('');
  const legend = `<text class="bar-label" x="${L}" y="${H-2}">● Enterprise accounts</text><text class="bar-label" x="${L+170}" y="${H-2}" fill="#2f45ff">● Live use cases</text>`;
  setHTML('accountsUsecasesChart', svg(W,H,grid+bars+legend));

  setHTML('milestonesTable', `<table class="summary-table"><thead><tr><th>Year-end</th><th>Accounts</th><th>Live use cases</th><th>Use cases / account</th><th>ARR</th></tr></thead><tbody>` +
    rows.map(r => `<tr><td>Dec ${r.year}</td><td>${fmt.count(r.enterprise_accounts)}</td><td>${fmt.count(r.live_use_cases)}</td><td>${Number(r.use_cases_per_account || 0).toFixed(1)}x</td><td>${fmt.eur(r.ending_arr)}</td></tr>`).join('') + `</tbody></table>`);
}

function renderRevenueMix() {
  const rows = data.annual_summary;
  const W=620,H=270,L=48,R=22,T=20,B=48, chartW=W-L-R, chartH=H-T-B;
  const max = Math.max(...rows.map(r=>r.total_revenue));
  const gap = chartW / rows.length;
  const bw = gap * .38;
  const y = v => T + chartH - (v/max)*chartH;
  const grid = [0,.25,.5,.75,1].map(p=>`<line class="grid-line" x1="${L}" x2="${W-R}" y1="${T+chartH-p*chartH}" y2="${T+chartH-p*chartH}"/>`).join('');
  const bars = rows.map((r,i)=>{
    const x = L + i*gap + (gap-bw)/2;
    const hSvc = (r.services_deployment_revenue/max)*chartH;
    const hSub = (r.platform_subscription_revenue/max)*chartH;
    const ySub = T + chartH - hSub;
    const ySvc = ySub - hSvc;
    return `<rect x="${x}" y="${ySvc}" width="${bw}" height="${hSvc}" rx="8" fill="#d0ccff"/>
      <rect x="${x}" y="${ySub}" width="${bw}" height="${hSub}" rx="8" fill="#2f45ff"/>
      <text class="value-label" x="${x+bw/2}" y="${Math.max(12,ySvc-8)}" text-anchor="middle">${fmt.eur(r.total_revenue)}</text>
      <text class="bar-label" x="${x+bw/2}" y="${H-20}" text-anchor="middle">${r.year}E</text>`;
  }).join('');
  const legend = `<text class="bar-label" x="${L}" y="${H-2}" fill="#7772d9">● Services &amp; deployment</text><text class="bar-label" x="${L+205}" y="${H-2}" fill="#2f45ff">● Platform subscription</text>`;
  setHTML('revenueMixChart', svg(W,H,grid+bars+legend));

  setHTML('annualTable', `<table class="summary-table"><thead><tr><th>Metric</th><th>2026E</th><th>2027E</th><th>2028E</th></tr></thead><tbody>
    <tr><td>Services &amp; deployment revenue</td>${rows.map(r=>`<td>${fmt.eur(r.services_deployment_revenue)}</td>`).join('')}</tr>
    <tr><td>Platform subscription revenue</td>${rows.map(r=>`<td>${fmt.eur(r.platform_subscription_revenue)}</td>`).join('')}</tr>
    <tr><td>Total revenue</td>${rows.map(r=>`<td>${fmt.eur(r.total_revenue)}</td>`).join('')}</tr>
    <tr><td>Ending ARR</td>${rows.map(r=>`<td>${fmt.eur(r.ending_arr)}</td>`).join('')}</tr>
    <tr><td>Recurring revenue share</td>${rows.map(r=>`<td>${fmt.pct(r.recurring_revenue_share)}</td>`).join('')}</tr>
    <tr><td>Gross margin</td>${rows.map(r=>`<td>${fmt.pct(r.gross_margin)}</td>`).join('')}</tr>
  </tbody></table>`);
}

function renderArr() {
  // Use monthly data directly to avoid the quarter labelling bug (Q5 = Dec alone)
  const ARR_POINTS = ['2026-12-01','2027-06-01','2027-12-01','2028-06-01','2028-12-01'];
  const LABELS     = ["Dec '26", "Jun '27", "Dec '27", "Jun '28", "Dec '28"];
  const rows = ARR_POINTS.map(m => data.revenue_monthly.find(r => r.month === m)).filter(Boolean);
  const W=620,H=270,L=48,R=20,T=20,B=46, chartW=W-L-R, chartH=H-T-B;
  const max = Math.max(...rows.map(r=>r.ending_arr));
  const x = i => L + i*(chartW/(rows.length-1));
  const y = v => T + chartH - (v/max)*chartH;
  const grid = [0,.25,.5,.75,1].map(p=>`<line class="grid-line" x1="${L}" x2="${W-R}" y1="${T+chartH-p*chartH}" y2="${T+chartH-p*chartH}"/>`).join('');
  const points = rows.map((r,i)=>`${x(i)},${y(r.ending_arr)}`).join(' ');
  const labels = rows.map((r,i)=>`<circle cx="${x(i)}" cy="${y(r.ending_arr)}" r="5" fill="#2f45ff"/><text class="bar-label" x="${x(i)}" y="${H-20}" text-anchor="middle">${LABELS[i]}</text><text class="value-label" x="${x(i)}" y="${Math.max(12,y(r.ending_arr)-10)}" text-anchor="middle">${fmt.eur(r.ending_arr)}</text>`).join('');
  setHTML('arrChart', svg(W,H,grid+`<polyline points="${points}" fill="none" stroke="#2f45ff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>`+labels));
}

function renderCapacityAndCash() {
  const caps = data.delivery_capacity.filter(r => r.month.endsWith('-12-01') || ['2026-09-01','2027-06-01','2028-06-01'].includes(r.month));
  const W=620,H=270,L=48,R=20,T=20,B=46, chartW=W-L-R, chartH=H-T-B;
  const max = Math.max(...caps.flatMap(r=>[r.fde_capacity_active_use_cases, r.active_deployments]));
  const x = i => L + i*(chartW/(caps.length-1));
  const y = v => T + chartH - (v/max)*chartH;
  const grid = [0,.25,.5,.75,1].map(p=>`<line class="grid-line" x1="${L}" x2="${W-R}" y1="${T+chartH-p*chartH}" y2="${T+chartH-p*chartH}"/>`).join('');
  const capLine = caps.map((r,i)=>`${x(i)},${y(r.fde_capacity_active_use_cases)}`).join(' ');
  const depLine = caps.map((r,i)=>`${x(i)},${y(r.active_deployments)}`).join(' ');
  const labels = caps.map((r,i)=>{ const d=new Date(r.month); const label=`${d.toLocaleDateString('en-US',{month:'short'})} '${String(d.getFullYear()).slice(2)}`; return `<text class="bar-label" x="${x(i)}" y="${H-20}" text-anchor="middle">${label}</text>`}).join('');
  setHTML('capacityChart', svg(W,H,grid+`<polyline points="${capLine}" fill="none" stroke="#2f45ff" stroke-width="4" stroke-linecap="round"/><polyline points="${depLine}" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>`+caps.map((r,i)=>`<circle cx="${x(i)}" cy="${y(r.fde_capacity_active_use_cases)}" r="4" fill="#2f45ff"/><circle cx="${x(i)}" cy="${y(r.active_deployments)}" r="4" fill="#111"/>`).join('')+labels+`<text class="bar-label" x="${L}" y="${H-2}">● Active deployments</text><text class="bar-label" x="${L+160}" y="${H-2}" fill="#2f45ff">● FDE capacity</text>`));

  const capacityByYear = [2026,2027,2028].map(year => data.delivery_capacity.find(r => r.year === year && r.month.endsWith('-12-01')) || data.delivery_capacity.find(r => r.year === year));
  setHTML('capacityTable', `<h3>FDE leverage assumptions</h3><table class="summary-table"><thead><tr><th>Year</th><th>Capacity / FDE</th><th>Driver of improvement</th></tr></thead><tbody>` +
    capacityByYear.map(r => `<tr><td>${r.year}</td><td>${Number(r.use_cases_per_fde).toFixed(0)} active use cases</td><td>${r.year===2026?'Hands-on deployments':r.year===2027?'Reusable playbooks and internal tooling':'Progressive self-serve deployment capabilities'}</td></tr>`).join('') + `</tbody></table>`);

  const cash = data.cash_monthly.filter(r => r.month.endsWith('-12-01') || ['2026-09-01','2027-06-01','2028-06-01'].includes(r.month));
  const maxCash = Math.max(...cash.map(r=>r.ending_cash));
  const minCash = Math.min(0, ...cash.map(r=>r.ending_cash));
  const range = maxCash - minCash || 1;
  const yc = v => T + chartH - ((v-minCash)/range)*chartH;
  const xc = i => L + i*(chartW/(cash.length-1));
  const cashPoints = cash.map((r,i)=>`${xc(i)},${yc(r.ending_cash)}`).join(' ');
  const cashLabels = cash.map((r,i)=>{ const d=new Date(r.month); const label=`${d.toLocaleDateString('en-US',{month:'short'})} '${String(d.getFullYear()).slice(2)}`; return `<circle cx="${xc(i)}" cy="${yc(r.ending_cash)}" r="5" fill="#111"/><text class="bar-label" x="${xc(i)}" y="${H-20}" text-anchor="middle">${label}</text><text class="value-label" x="${xc(i)}" y="${Math.max(12,yc(r.ending_cash)-9)}" text-anchor="middle">${fmt.eur(r.ending_cash)}</text>`}).join('');
  setHTML('cashChart', svg(W,H,grid+`<polyline points="${cashPoints}" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>`+cashLabels));
}

function renderFunds() {
  setHTML('useOfFunds', `<h3>Seed allocation</h3><div class="fund-list">` + data.use_of_funds.map(f => `
    <div class="fund-item">
      <div class="fund-top"><span>${f.category}</span><span>${fmt.eur(f.amount)}</span></div>
      <div class="fund-purpose">${f.purpose} · ${fmt.pct(f.share)}</div>
      <div class="fund-bar"><div style="width:${Math.max(4, f.share*100)}%"></div></div>
    </div>`).join('') + `</div>`);
}

renderKpis();
renderTrajectory();
renderMonthlyRevenue();
renderUnitEconomics();
renderAccountsUseCases();
renderRevenueMix();
renderArr();
renderCapacityAndCash();
renderFunds();
