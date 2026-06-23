from __future__ import annotations
import shutil
from pathlib import Path

from fonction_bp.config import Paths

HTML = r'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Fonction Labs — BP Dashboard</title>
  <link rel="stylesheet" href="assets/style.css" />
</head>
<body>
  <header class="topbar">
    <a class="brand" href="#top">fonction</a>
    <nav>
      <a href="#trajectory">Trajectoire</a>
      <a href="#traction">Traction</a>
      <a href="#model">Modèle</a>
      <a href="#growth">Croissance</a>
      <a href="#runway">Runway</a>
      <a class="nav-download" href="downloads/Fonction_Labs_BP_Seed_2026_2028_full_pipeline_v2.xlsx">Excel</a>
    </nav>
  </header>

  <main id="top">
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Annexe BP · VC case</p>
        <h1>Fonction Labs — BP dashboard</h1>
        <p class="lead">Vue synthétique du modèle seed 2026–2028 : traction commerciale, passage vers l'abonnement plateforme, expansion par use case et usage des fonds.</p>
        <div class="meta">
          <span class="pill">Levée modélisée : 2,5M€ net</span>
          <span class="pill">Closing : septembre 2026</span>
          <span class="pill">Modèle : VC case</span>
          <span class="pill">Devise : k€ HT</span>
        </div>
        <div class="hero-actions">
          <a class="button primary" href="downloads/Fonction_Labs_BP_Seed_2026_2028_full_pipeline_v2.xlsx">Télécharger le BP complet</a>
          <a class="button secondary" href="downloads/Fonction_Labs_BP_Seed_2026_2028_simplified_pipeline_v2.xlsx">BP simplifié</a>
        </div>
      </div>
      <aside class="hero-panel">
        <span class="panel-label">Source du modèle</span>
        <strong>Pipeline v2</strong>
        <p>Dashboard, Excel complet et Excel simplifié sont générés depuis les mêmes tables DuckDB.</p>
      </aside>
    </section>

    <section class="kpi-band" id="kpis" aria-label="KPIs"></section>

    <section id="trajectory" class="section trajectory-section">
      <div class="section-intro">
        <span class="section-number">01</span>
        <div>
          <h2>Trajectoire sur trois ans</h2>
          <p>Le modèle part d'une traction commerciale déjà existante, puis fait progressivement basculer le revenu vers des abonnements liés aux use cases live chez les grands comptes.</p>
        </div>
      </div>
      <div class="trajectory-grid" id="trajectoryCards"></div>
    </section>

    <section id="traction" class="section split-section">
      <div class="section-intro sticky-intro">
        <span class="section-number">02</span>
        <div>
          <h2>Traction existante et outlook 2026</h2>
          <p>Vue annuelle 2026 complète : les six premiers mois montrent la traction existante ; le second semestre modélise la continuité des services et les premiers revenus plateforme.</p>
        </div>
      </div>
      <div class="content-card wide">
        <div class="chart-head">
          <div>
            <h3>Revenu commercial mensuel — 2026</h3>
            <p>Jan–Jun actuals / estimation, Jul–Déc forecast. Montants HT.</p>
          </div>
          <div class="legend compact">
            <span><i class="dot actual"></i>Actuel / estimé</span>
            <span><i class="dot forecast"></i>Forecast</span>
          </div>
        </div>
        <div id="monthlyRevenueChart" class="chart tall"></div>
        <div id="revenue2026Table" class="table-wrap"></div>
      </div>
    </section>

    <section id="model" class="section">
      <div class="section-intro">
        <span class="section-number">03</span>
        <div>
          <h2>Modèle de revenu par grand compte</h2>
          <p>Chaque nouveau grand compte démarre par un use case cadré, passe par un déploiement 0→1, puis génère un abonnement par use case live.</p>
        </div>
      </div>
      <div class="phase" id="unitEconomics"></div>
    </section>

    <section id="growth" class="section split-section">
      <div class="section-intro sticky-intro">
        <span class="section-number">04</span>
        <div>
          <h2>Modèle de croissance : comptes et use cases</h2>
          <p>L'ARR est construit par deux moteurs : nouveaux comptes enterprise et expansion du nombre de use cases live dans les comptes existants.</p>
        </div>
      </div>
      <div class="grid-two">
        <div class="content-card">
          <div class="chart-head"><h3>Comptes enterprise et use cases live</h3></div>
          <div id="accountsUsecasesChart" class="chart medium"></div>
        </div>
        <div class="content-card">
          <h3>Jalons de fin d'année</h3>
          <div id="milestonesTable"></div>
          <p class="footnote">L'ending ARR est le run-rate d'abonnement annualisé en fin de période. Revenu récurrent reconnu et ending ARR sont deux métriques distinctes.</p>
        </div>
      </div>
    </section>

    <section class="section split-section">
      <div class="section-intro sticky-intro">
        <span class="section-number">05</span>
        <div>
          <h2>Mix de revenus et montée en ARR</h2>
          <p>Les revenus services et déploiement restent actifs pendant que le revenu récurrent plateforme devient le principal moteur de croissance à mesure que les use cases déployés passent en live.</p>
        </div>
      </div>
      <div class="grid-two">
        <div class="content-card">
          <div class="chart-head"><h3>Mix de revenus annuel</h3></div>
          <div id="revenueMixChart" class="chart medium"></div>
        </div>
        <div class="content-card">
          <div class="chart-head"><h3>ARR en fin de trimestre</h3></div>
          <div id="arrChart" class="chart medium"></div>
        </div>
      </div>
      <div class="content-card wide table-only" id="annualTable"></div>
    </section>

    <section class="section split-section" id="runway">
      <div class="section-intro sticky-intro">
        <span class="section-number">06</span>
        <div>
          <h2>Scalabilité, runway et usage des fonds</h2>
          <p>La levée finance le produit, l'engineering, la capacité FDE et le go-to-market enterprise. La capacité par FDE augmente avec les playbooks, connecteurs, tooling interne et self-serve progressif.</p>
        </div>
      </div>
      <div class="grid-two">
        <div class="content-card">
          <div class="chart-head"><h3>Capacité FDE vs déploiements actifs</h3></div>
          <div id="capacityChart" class="chart medium"></div>
        </div>
        <div class="content-card">
          <div class="chart-head"><h3>Cash runway</h3></div>
          <div id="cashChart" class="chart medium"></div>
        </div>
      </div>
      <div class="grid-two bottom-grid">
        <div class="content-card" id="capacityTable"></div>
        <div class="content-card" id="useOfFunds"></div>
      </div>
    </section>

    <section class="download-section">
      <div>
        <p class="eyebrow">Téléchargements</p>
        <h2>Modèles Excel générés depuis le même pipeline.</h2>
        <p>Le BP complet pour une revue détaillée, le BP simplifié pour une version VC-facing allégée. Les deux sont issus des mêmes tables modèle.</p>
      </div>
      <div class="download-actions">
        <a class="button primary" href="downloads/Fonction_Labs_BP_Seed_2026_2028_full_pipeline_v2.xlsx">BP complet Excel</a>
        <a class="button secondary" href="downloads/Fonction_Labs_BP_Seed_2026_2028_simplified_pipeline_v2.xlsx">BP simplifié Excel</a>
      </div>
    </section>
  </main>

  <script src="assets/dashboard_data.js"></script>
  <script src="assets/dashboard.js"></script>
</body>
</html>
'''

CSS = r''':root{
  --bg:#f6f3eb;
  --paper:#fffdfa;
  --ink:#111111;
  --muted:#62615c;
  --soft:#ebe6dc;
  --line:#ded7c9;
  --line-strong:#c9bfad;
  --accent:#2f45ff;
  --accent-soft:#e8ebff;
  --olive:#73715f;
  --sand:#f1ece1;
  --black:#111111;
  --green:#0d7a59;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
.topbar{position:sticky;top:0;z-index:30;display:flex;justify-content:space-between;align-items:center;padding:17px 34px;background:rgba(246,243,235,.9);backdrop-filter:blur(20px);border-bottom:1px solid rgba(222,215,201,.8)}
.brand{text-decoration:none;font-weight:760;letter-spacing:-.03em;font-size:21px}
nav{display:flex;gap:22px;align-items:center;font-size:13px;color:#4d4b46}
nav a{text-decoration:none}nav a:hover{color:#111}.nav-download{padding:9px 13px;border:1px solid var(--ink);border-radius:999px;color:#111}
main{max-width:1240px;margin:0 auto;padding:0 32px 90px}
.hero{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:42px;align-items:end;padding:74px 0 56px;border-bottom:1px solid var(--line)}
.eyebrow{margin:0 0 12px;text-transform:uppercase;letter-spacing:.11em;font-size:12px;font-weight:720;color:var(--muted)}
h1,h2,h3,p{margin-top:0}.hero h1{font-size:74px;line-height:.92;letter-spacing:-.065em;max-width:900px;margin:16px 0 22px}.lead{font-size:21px;line-height:1.45;max-width:760px;color:#383731;margin-bottom:0}
.meta{margin-top:20px;display:flex;flex-wrap:wrap;gap:10px}.pill{border:1px solid var(--line);background:rgba(255,255,255,.6);padding:8px 11px;border-radius:999px;font-size:13px;color:#333}
.hero-actions,.download-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}.button{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:12px 17px;text-decoration:none;font-weight:700;font-size:14px}.button.primary{background:#111;color:#fff;border:1px solid #111}.button.secondary{border:1px solid var(--line-strong);color:#111;background:rgba(255,255,255,.28)}
.hero-panel{background:#111;color:#fff;border-radius:28px;padding:26px;box-shadow:0 24px 80px rgba(38,30,14,.12)}.hero-panel .panel-label{display:block;color:#bdb7ac;text-transform:uppercase;letter-spacing:.1em;font-size:12px;font-weight:700;margin-bottom:18px}.hero-panel strong{font-size:38px;letter-spacing:-.05em}.hero-panel p{color:#d4d1ca;line-height:1.5;margin:18px 0 0}
.kpi-band{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:26px 0 56px}.kpi-card{min-height:154px;background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:20px;display:flex;flex-direction:column;justify-content:space-between}.kpi-card.feature{background:#111;color:#fff}.kpi-card p{font-size:13px;color:var(--muted);line-height:1.25;margin:0}.kpi-card.feature p,.kpi-card.feature span{color:#d4d1ca}.kpi-card strong{font-size:31px;line-height:1;letter-spacing:-.055em}.kpi-card span{font-size:12px;color:#77746d}
.section{margin:76px 0}.section-intro{display:grid;grid-template-columns:54px minmax(0,760px);gap:20px;margin-bottom:24px}.section-number{height:36px;width:36px;border:1px solid var(--line-strong);border-radius:999px;display:inline-flex;align-items:center;justify-content:center;font-size:12px;color:#68645c}.section-intro h2{font-size:42px;line-height:1.02;letter-spacing:-.052em;margin-bottom:12px}.section-intro p{font-size:18px;line-height:1.52;color:var(--muted);margin:0}.split-section{display:grid;grid-template-columns:340px minmax(0,1fr);gap:34px;align-items:start}.sticky-intro{position:sticky;top:92px;grid-template-columns:54px minmax(0,1fr)}
.trajectory-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.trajectory-card{background:#111;border-radius:26px;padding:26px;min-height:260px;color:#fff;display:flex;flex-direction:column}.trajectory-card .year{font-size:13px;color:#c9c2b6;margin-bottom:44px}.trajectory-card h3{font-size:27px;line-height:1.03;letter-spacing:-.04em;margin-bottom:14px}.trajectory-card p{color:#d6d1c8;line-height:1.48;margin:auto 0 0}
.phase{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.phase-card{border:1px solid var(--line);background:var(--sand);border-radius:18px;padding:18px}.phase-card .phase-label{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-bottom:10px;display:block}.phase-card strong{display:block;font-size:22px;letter-spacing:-.03em;margin-bottom:8px}.phase-card span{display:block;font-size:13px;color:#555;line-height:1.4}
.content-card,.phase-table-card{background:var(--paper);border:1px solid var(--line);border-radius:28px;padding:26px;box-shadow:0 16px 70px rgba(53,44,28,.035)}.wide{grid-column:2}.chart-head{display:flex;justify-content:space-between;gap:20px;align-items:start;margin-bottom:16px}.chart-head h3,.content-card h3{font-size:22px;letter-spacing:-.035em;margin-bottom:5px}.chart-head p{color:var(--muted);font-size:14px;line-height:1.45;margin:0}.legend{display:flex;gap:14px;align-items:center;white-space:nowrap}.legend span{font-size:12px;color:#605d56}.dot{display:inline-block;width:9px;height:9px;border-radius:99px;margin-right:7px}.dot.actual{background:#111}.dot.forecast{background:#9a958b}.dot.services{background:#d0ccff}.dot.platform{background:#2f45ff}.chart{width:100%;min-height:270px}.chart.tall{min-height:330px}.chart.medium{min-height:290px}.grid-two{display:grid;grid-template-columns:1fr 1fr;gap:18px}.bottom-grid{margin-top:18px}.table-wrap{margin-top:20px}.summary-table,.phase-table{width:100%;border-collapse:collapse;font-size:14px}.summary-table th,.summary-table td,.phase-table th,.phase-table td{padding:15px 14px;border-top:1px solid var(--line);text-align:right}.summary-table th:first-child,.summary-table td:first-child,.phase-table th:first-child,.phase-table td:first-child{text-align:left}.summary-table thead th,.phase-table thead th{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#77736a;background:#f8f5ee;border-top:none}.summary-table tbody tr:first-child td,.phase-table tbody tr:first-child td{border-top:1px solid var(--line)}.phase-name{display:block;font-weight:780}.phase-note{display:block;margin-top:3px;font-size:12px;color:var(--muted)}.footnote{font-size:13px!important;color:#77736a!important;line-height:1.45!important;margin-top:18px!important}.table-only{margin-top:18px}
svg{display:block;width:100%;height:auto}.axis-label{font-size:11px;fill:#79756d}.value-label{font-size:11px;fill:#33312d;font-weight:700}.bar-label{font-size:12px;fill:#57534b}.grid-line{stroke:#e7e1d5;stroke-width:1}.line-svc{stroke:#7772d9}.line-platform{stroke:#2f45ff}.chart-title-note{font-size:12px;color:#77736a}.fund-list{display:grid;gap:13px}.fund-item{border-top:1px solid var(--line);padding-top:13px}.fund-item:first-child{border-top:none;padding-top:0}.fund-top{display:flex;justify-content:space-between;gap:20px;font-weight:760}.fund-purpose{font-size:12px;color:var(--muted);margin-top:4px}.fund-bar{height:8px;background:#ece6dc;border-radius:999px;overflow:hidden;margin-top:10px}.fund-bar div{height:100%;background:#111;border-radius:999px}.download-section{margin-top:84px;border-top:1px solid var(--line);padding-top:42px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:30px;align-items:end}.download-section h2{font-size:34px;line-height:1.06;letter-spacing:-.045em;margin-bottom:12px}.download-section p{color:var(--muted);line-height:1.5;max-width:670px}.download-actions{margin:0;align-items:center;justify-content:flex-end}
@media(max-width:1060px){.hero{grid-template-columns:1fr}.hero h1{font-size:56px}.kpi-band{grid-template-columns:repeat(2,1fr)}.split-section{grid-template-columns:1fr}.sticky-intro{position:static}.wide{grid-column:auto}.trajectory-grid,.grid-two,.phase{grid-template-columns:repeat(2,1fr)}.download-section{grid-template-columns:1fr}.download-actions{justify-content:flex-start}}
@media(max-width:720px){.topbar{padding:14px 20px}nav a:not(.nav-download){display:none}main{padding:0 18px 64px}.hero{padding-top:46px}.hero h1{font-size:43px}.lead{font-size:18px}.kpi-band{grid-template-columns:1fr}.phase{grid-template-columns:1fr}.section-intro{grid-template-columns:1fr}.section-intro h2{font-size:32px}.content-card,.phase-table-card{padding:18px;border-radius:22px}.chart-head{display:block}.legend{margin-top:12px;flex-wrap:wrap}.summary-table,.phase-table{font-size:13px}.summary-table th,.summary-table td,.phase-table th,.phase-table td{padding:11px 9px}.hero-panel strong{font-size:30px}}
'''

JS = r'''const data = window.DASHBOARD_DATA;

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
  }
};

function getKpi(name) { return data.kpis.find(k => k.metric === name); }
function kpiValue(k) { return k.unit === 'EUR' ? fmt.eur(k.value) : fmt.count(k.value); }
function setHTML(id, html) { const el = document.getElementById(id); if (el) el.innerHTML = html; }
function svg(width, height, inner) { return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-hidden="true">${inner}</svg>`; }

function renderKpis() {
  const items = [
    { metric: 'Actual commercial revenue Jan-Jun 2026', sub: 'Chiffre d\'affaires commercial H1', dark: true },
    { metric: '2026E revenue',                sub: 'Revenu annuel total 2026E' },
    { metric: '2027E revenue',                sub: 'Services, déploiement et abonnement' },
    { metric: 'Ending ARR Dec-2027',          sub: 'Run-rate abonnement annualisé' },
    { metric: 'Enterprise accounts Dec-2027', sub: 'Comptes enterprise activés' },
    { metric: 'Live use cases Dec-2027',      sub: 'Use cases en abonnement' },
    { metric: '2028E revenue',                sub: 'Croissance par expansion compte', computed: true },
    { metric: 'Ending ARR Dec-2028',          sub: 'Run-rate abonnement annualisé', computed: true },
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
'''


def run(paths: Paths, scenario: str = "vc_case") -> Path:
    paths.dashboard_dir.mkdir(parents=True, exist_ok=True)
    (paths.dashboard_dir / "assets").mkdir(parents=True, exist_ok=True)
    (paths.dashboard_dir / "index.html").write_text(HTML, encoding="utf-8")
    (paths.dashboard_dir / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (paths.dashboard_dir / "assets" / "dashboard.js").write_text(JS, encoding="utf-8")

    # Also expose the dashboard at repository root for one-click opening.
    (paths.root / "assets").mkdir(parents=True, exist_ok=True)
    (paths.root / "index.html").write_text(HTML, encoding="utf-8")
    (paths.root / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (paths.root / "assets" / "dashboard.js").write_text(JS, encoding="utf-8")
    if paths.dashboard_data_js.exists():
        shutil.copy2(paths.dashboard_data_js, paths.root / "assets" / "dashboard_data.js")

    return paths.dashboard_dir / "index.html"
