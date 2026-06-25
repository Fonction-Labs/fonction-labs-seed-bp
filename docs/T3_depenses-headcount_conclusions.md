# T3 — Modèle de dépenses et headcount : Conclusions et décisions

**Statut** : DONE (brainstorm + décisions actées)
**Date** : 25 juin 2026
**Ref** : [T2_synthese-complete_conclusions.md](./T2_synthese-complete_conclusions.md), [vc_case.yaml](../data/assumptions/vc_case.yaml)

---

## Contexte

Le modèle de dépenses est recalibré à partir de trois sources :
1. Le YAML existant (`vc_case.yaml`) — point de départ, maintenu sauf delta explicite
2. Les décisions T1/T2 — notamment le ramp UC validé et la formule FDE
3. Le feedback réunion Jean — notamment le sizing FDE, les coûts infra IA, et Wassym

Le principe : **ne changer le YAML que là où les nouvelles décisions créent un écart explicite. Les autres paramètres YAML seront recalibrés en T5.1.**

---

## T3.1 — Headcount FDE

### Formule de calibrage validée

La bonne approche est de dériver le headcount FDE depuis le nombre d'UC actifs, pas depuis une cible arbitraire.

**Formule (validée brainstorm) :**
```
FDE = (UC en déploiement × 1.0) + (UC en AC × 0.25)
```

**Logique :**
- Pendant le déploiement (3 mois), 1 FDE se concentre sur 1 UC à la fois — contrainte de focus, pas seulement de volume
- En amélioration continue, 1 FDE peut gérer 4 UC simultanément (0.25 par UC)
- Jean : "1 FDE = 3-4 UC en moyenne" → correspond à un portefeuille majoritairement en AC (steady state)

**Cette formule remplace toute cible arbitraire** — le nombre de FDEs découle mécaniquement du calendrier de déploiements UC.

---

### Application au ramp UC (T2.3)

Source des UC actifs : [T2_synthese-complete_conclusions.md](./T2_synthese-complete_conclusions.md)

| Date | UC total | UC en deploy* | UC en AC | FDE formule | FDE YAML | Delta |
|------|----------|--------------|----------|-------------|----------|-------|
| Fin 2026 | 2 | ~1 | ~1 | **~1.25 → 2 FDE** | 1 | **-1** |
| Mi 2027 | ~12 | ~3 | ~9 | **~5.25 → 6 FDE** | 2-3 | **-3** |
| Fin 2027 | ~25 | ~4 | ~21 | **~9.25 → 9 FDE** | 4 | **-5** |
| Fin 2028 | ~70 | ~5 | ~65 | **~21.25 → ≥10 FDE** | 6 | **à recalibrer** |

*UC en deploy = UC dont le démarrage remonte à moins de 3 mois.

**Note :** le delta YAML est significatif à partir de mi-2027. La calibration précise mois par mois sera faite en T5.1 en appliquant la formule au `enterprise_cohort_plan`.

**Les FDEs font aussi les ateliers** (~5 jours par atelier initial) — inclus dans la capacité FDE, pas modélisé séparément.

---

### Coût FDE interne

| Référence | Coût/mois | Coût/an |
|-----------|-----------|---------|
| CDI senior Paris (estimation marché) | ~9 500 EUR | ~115k |
| YAML actuel | 11 000 EUR | 132k |

**Décision : maintenir 11k/mois du YAML** — légèrement conservateur mais défendable VC pour un profil senior AI/infra CDI Paris.

**Économie FDE :** 1 150 EUR/jour × 210j = **241 500 EUR CA/an par FDE** → marge brute FDE ~46-48%.

---

## T3.2 — Headcount non-FDE (Product, Sales, Ops)

### Nomenclature simplifiée

Les rôles du YAML sont renommés pour la lisibilité VC. Solutions Architect est compté comme AI Engineer (même fonction, même coût).

| Rôle (nomenclature BP) | Rôle YAML original | Start | Coût/mois fully loaded | Note |
|---|---|---|---|---|
| Lead AI Engineer | Product Lead | sept 2026 | 12k | — |
| AI Engineer 1 | AI / Platform Engineer | nov 2026 | 11k | — |
| **Sales Engineer** | absent du YAML | **déc 2026** | **10k** | Quasi recruté — à ajouter |
| Sales 1 | Enterprise Sales | fév 2027 | 11k | — |
| AI Engineer 2 | Product Engineer | avr 2027 | 11k | — |
| Customer Ops | Customer Ops | juil 2027 | 8k | — |
| **Sales Dev** | Sales Development | ~~oct 2027~~ → **jan 2027** | 8k | **Avancer** : pipeline 2028 |
| AI Engineer 3 | Platform Engineer 2 | jan 2028 | 12k | — |
| Sales 2 | Enterprise Sales 2 | mars 2028 | 12k | — |
| AI Engineer 4 | Solutions Architect | sept 2028 | 12k | Compté AI Engineer |

**FDE Senior 1-6 : inchangés** (11k/mois, timeline YAML maintenue avec recalibration T5.1)

### Changements vs YAML actuel

1. **Sales Engineer déc 2026** — nouveau rôle à ajouter (10k/mois)
2. **Sales Dev avancé à jan 2027** — oct 2027 est trop tard pour nourrir le pipeline 2028 (cycle 4-8 mois)
3. Les autres timings et coûts sont maintenus tels quels — recalibration détaillée en T5.1

---

## T3.3 — Marketing + bureaux

### Marketing

**Ligne marketing dédiée à ajouter** (non incluse dans l'opex_base YAML) :

| Année | Budget marketing total | Dans opex_base | Incrémental à ajouter |
|-------|----------------------|----------------|-----------------------|
| 2026 H2 | ~18k (~3k/mois) | ✓ inclus | 0 |
| 2027 | ~100k | ~36k inclus | **+64k** |
| 2028 | ~150k | ~36k inclus | **+114k** |

Objectif : doubler la pipeline de vente (conférences enterprise, content, événements sectoriels).

### Bureaux Paris

Déjà inclus dans l'opex_base YAML (42k/mois H2 2026, 65k en 2027, 95k en 2028). Estimation coworking premium Paris : 500-700 EUR/poste/mois → cohérent avec la taille de l'équipe. **Pas de changement.**

---

## T3.4 — Coûts infra — 4 sous-lignes distinctes

Le `product_infra_ai_tooling` du YAML agrège tout. Il doit être décomposé en 4 sous-lignes lors de la traduction en T5.1 — chaque ligne a sa propre logique de calcul et son propre traitement comptable (COGS vs OPEX).

### Sous-ligne 1 — Tokens clients → **COGS**

Coût des appels API aux modèles IA pour les UC clients en production. Calculé depuis T2.2 (max ~200 EUR/UC/mois en moyenne).

```
2026 H2 : 2 UC × ~40 EUR/mois    = ~0.5k/mois
2027 H1 : ~12 UC × ~200 EUR/mois = ~2.5k/mois
2027 H2 : ~25 UC × ~200 EUR/mois = ~5k/mois
2028    : ~70 UC × ~400 EUR/mois = ~28k/mois
```

Driver formule : `nb_uc_actifs × avg_token_cost_per_uc`

### Sous-ligne 2 — Infra cloud plateforme → **COGS**

Kubernetes, bases de données, stockage, monitoring. Héberge les workloads clients — 100% client-facing.

```
2026 H2 : ~7k/mois   (early stage, 2 UC en prod)
2027 H1 : ~12k/mois  (~12 UC)
2027 H2 : ~17k/mois  (~25 UC)
2028    : ~25-30k/mois (~70 UC)
```

Driver formule : scalable avec `nb_uc_actifs`, paramètre base à définir en T5.1.

### Sous-ligne 3 — AI dev tooling → **OPEX**

Cursor, Claude API dev/eval, GitHub Copilot, outils d'évaluation des agents. Utilisé par les personnes techniques pour développer et maintenir les UC. Source : Jean (~1 000 EUR/personne technique/mois).

```
2026 H2 : 1 Lead + 1 AI Eng + 1 FDE = 3 → ~3k/mois
2027    : 1 Lead + 2 AI Eng + ~4 FDE = 7-8 → ~8k/mois
2028    : 1 Lead + 4 AI Eng + ~7 FDE = 12 → ~12k/mois
```

Driver formule : `nb_personnes_techniques × ai_tooling_cost_per_person` (1k/mois)

### Sous-ligne 4 — SaaS divers → **OPEX**

GitHub, Notion, outils prod, monitoring SaaS, licences diverses.

```
2026 H2 : ~2k/mois
2027    : ~3k/mois
2028    : ~4k/mois
```

Driver formule : croissance progressive avec la taille équipe, paramètre fixe à affiner en T5.1.

---

### Vérification cohérence avec le YAML actuel

| Période | Tokens | Infra cloud | AI dev tooling | SaaS divers | **Total calculé** | **YAML** | Écart |
|---------|--------|-------------|----------------|-------------|------------------|---------|-------|
| 2026 H2 | 0.5k | 7k | 3k | 2k | **~12.5k** | 15k | -17% |
| 2027 H1 | 2.5k | 12k | 8k | 3k | **~25.5k** | 25k | +2% |
| 2027 H2 | 5k | 17k | 8k | 3k | **~33k** | 35k | -6% |
| 2028 H1 | 20k | 25k | 12k | 4k | **~61k** | 55k | +11% |
| 2028 H2 | 28k | 25k | 12k | 4k | **~69k** | 70k | -1% |

Cohérence bonne (~10% d'écart max) — les ordres de grandeur du YAML sont validés par le bottom-up.

---

### Traitement pour la formule COGS

```
infra_cogs  = tokens_clients + infra_cloud_plateforme   # sous-lignes 1 + 2
opex_tech   = ai_dev_tooling + saas_divers              # sous-lignes 3 + 4
```

Pas de ratio `infra_client_facing_pct` — chaque sous-ligne est calculée depuis ses propres drivers. En T5.1, `product_infra_ai_tooling` sera remplacé par ces 4 paramètres distincts dans le YAML.

---

## T3.5 — RH/back-office et certification

### Customer Ops

**Maintenir YAML** : juillet 2027, 8k/mois fully loaded. Couvre support client tier-1, facturation, admin, onboarding entreprise.

### ISO 27001

**Maintenir jalons YAML** (40k sept 2026, 30k jan 2027, 30k juil 2027, 40k jan 2028) — cohérent marché (25-40k one-shot + surveillance annuelle).

**Timing critique :** ISO 27001 prend 12-18 mois. C'est le déblocage pour les Grands Comptes (Q4 2027). Lancer immédiatement si pas commencé.

### SecNumCloud

**TBD post-T4.1/T4.2.** Coût réel non modélisé (100-300k+). Le YAML n'a que 40k en jan 2028, clairement insuffisant si on vise SecNumCloud directement. À résoudre via la stratégie OVH (T4.2).

---

## T3.6 — Wassym / BPCE

### Situation réelle

Wassym est déployé full-time chez BPCE. La section `service_continuity` du YAML est bien une ligne séparée (pas un doublon de `service_forecast_baseline`), mais les paramètres sont faux.

| Paramètre | YAML actuel | Réalité | Delta |
|-----------|-------------|---------|-------|
| `wassym_days_per_month` | 3.3j | **20j** | **+16.7j** |
| `wassym_revenue_day_rate` | 915 EUR/j | **950 EUR/j** | +35 EUR/j |
| `wassym_cost_day_rate` | 750 EUR/j | **750 EUR/j** | 0 |
| Revenue/mois résultant | ~3k | **~19k** | **+16k** |
| Coût/mois résultant | ~2.5k | **~15k** | **+12.5k** |
| Marge/mois | ~0.5k | **~4k** | — |

**Sous-estimation revenu : ~+16k/mois → ~+192k sur 2026 H2 + 2027** (significatif pour le cash).

### Décision affichage

Wassym est une ligne interne au YAML (paramètres séparés) mais **non affiché comme ligne séparée dans les outputs agrégés** — absorbé dans "Services & Deployment Revenue" comme prévu par `vc_facing_display: Included in Services & Deployment Revenue`.

**Correction YAML actée :** `wassym_days_per_month: 20`, `wassym_revenue_day_rate: 950`.

---

## T3.7 — Marge brute consolidée (formule)

La marge brute n'est pas un chiffre hardcodé — c'est une formule dérivée des hypothèses. Elle sera calculée en T5.1.

**Définition :**
```
cogs = (nb_fde_actifs × fde_monthly_cost)
     + token_costs_clients
     + infra_client_facing  # fraction de product_infra_ai_tooling

gross_margin_pct = (revenue - cogs) / revenue
```

**COGS = coûts de delivery uniquement.** Hors COGS : AI Engineers, Sales, G&A, marketing = opex.

**Estimation 2027 (ordre de grandeur) :**
```
Revenue              : ~2.5M
COGS FDE (~9 × ~8 mois moy × 11k) : ~792k
Tokens clients                     : ~100k
Infra client-facing                : ~180k
COGS total                         : ~1.07M
Gross Margin estimée               : ~57%
```

57% à ce stade est correct pour un VC. La trajectoire vers >70% en 2028 (automatisation progressive, moins de FDE/UC) est le message clé.

---

## Règle pipeline — AGENT.MD

**Décision structurelle :** toute valeur produite par la pipeline provient d'une hypothèse nommée (paramètre YAML) ou d'une formule dérivée. **Aucune valeur hardcodée dans les outputs.** Cela permet de faire des itérations sur les hypothèses sans tout recalculer manuellement.

Exemples :
- Nombre de FDEs → formule depuis `enterprise_cohort_plan` + `deployment_duration_months`
- Gross margin → formule depuis `fde_monthly_cost`, `nb_fde`, `token_costs`
- Marketing budget → paramètre YAML dédié, pas noyé dans opex_base

**Cette règle sera documentée dans AGENT.MD et appliquée lors de la traduction des docs en code (T5.1).**

---

## Synthèse delta YAML → BP recalibré

| Ligne | YAML actuel | Recalibré | Delta annuel 2027 |
|-------|-------------|-----------|------------------|
| FDE headcount | 4 FDE fin 2027 | ~9 FDE (formule) | **+5 FDE × ~8 mois × 11k = +440k** |
| Sales Engineer | absent | déc 2026 | **+10k × 6 mois = +60k** |
| Sales Dev | oct 2027 | jan 2027 | **+8k × 9 mois = +72k** |
| Marketing | ~36k/an inclus opex | ~100k/an | **+64k** |
| AI dev tooling | absent | ~96k/an | **+96k** |
| Wassym revenu | ~36k/an | **~228k/an** | **+192k revenu** |
| Wassym coût | ~30k/an | ~180k/an | +150k coût |
| Bureaux | inclus opex | inchangé | 0 |
| Certification ISO | jalons OK | inchangé | 0 |
| **Delta dépenses net 2027** | | | **~+732k dépenses** |
| **Delta revenu net 2027** | | | **~+192k revenu (Wassym)** |

**Note :** le delta FDE est partiellement autofinancé — chaque FDE génère ~241k de CA service/an.

---

## Décisions actées

| # | Décision |
|---|----------|
| 1 | Formule FDE : #FDE = (UC_deploy × 1.0) + (UC_AC × 0.25) |
| 2 | Contrainte deploy : 1 FDE focalisé sur 1 UC actif en déploiement |
| 3 | AC : 1 FDE gère 4 UC simultanément (0.25 FDE/UC) |
| 4 | Coût FDE interne : 11k/mois fully loaded (maintien YAML) |
| 5 | YAML sous-estime le headcount FDE — recalibration mois par mois en T5.1 |
| 6 | Nomenclature simplifiée : Lead AI Engineer, AI Engineer, Sales Engineer, Sales, Customer Ops |
| 7 | Sales Engineer ajouté déc 2026 (10k/mois) — quasi recruté |
| 8 | Sales Dev avancé à jan 2027 (vs oct 2027 YAML) |
| 9 | Marketing : ligne séparée opex_base (+64k en 2027, +114k en 2028) |
| 10 | Bureaux : dans opex_base YAML, pas de changement |
| 11 | Customer Ops : maintenir YAML (jul 2027, 8k/mois) |
| 12 | ISO 27001 : maintenir jalons YAML — lancer maintenant si pas commencé |
| 13 | SecNumCloud : TBD post-T4.1/T4.2, non chiffré |
| 14 | AI dev tooling : ajouter ~3k/mois 2026, ~8k/mois 2027, ~12k/mois 2028 (~1k/personne technique) |
| 15 | Tokens clients : négligeable, couvert dans product_infra_ai_tooling |
| 16 | Wassym : corriger YAML → 20j/mois, 950 EUR/j revenu (non doublon, ligne séparée confirmée) |
| 17 | Wassym : non affiché comme ligne séparée dans les outputs agrégés |
| 18 | Gross margin = formule dérivée (COGS = FDE + tokens + infra client-facing) — estimée ~57% 2027 |
| 19 | Règle pipeline : tout output = hypothèse nommée ou formule — zéro hardcode (→ AGENT.MD) |
