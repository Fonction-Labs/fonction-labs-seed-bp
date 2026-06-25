# T2 — Synthese complete : Segmentation clients, use cases, pricing, projection CA

**Statut** : DONE (validé)
**Date** : 25 juin 2026
**Ref** : T1.1, T1.2, T1.3

---

## Principe fondamental de pricing

**Value-based pricing — pas du cost-plus.**

```
1. Cout humain equivalent aujourd'hui pour faire cette tache
2. Prix = cout humain / 2  →  ROI x2 minimum pour le client
3. Notre cout reel = tokens (marginal, negligeable) + FDE amorti
4. Marge brute visee = 70-90%+
```

Les credits masquent le cout token derriere un prix valeur. Le client achete de la valeur, pas des tokens.

**Modele final :**
- Abonnement léger (accès plateforme)
- + Credits prépayés : 1 crédit = X tokens
- La consommation de tokens génère les revenus cibles selon le volume par use case
- Ratio crédit/token et prix du crédit à fixer pour atteindre les ARPU cibles (à préciser en implementation)

---

## T2.1 — 3 typologies clients

### Segment ETI (~100M EUR CA)

| Critère | Valeur |
|---------|--------|
| Use cases année 1 | 1-2 (moy 1.5) |
| Use cases max (année 3+) | 3-4 |
| Rythme d'ajout | ~1/an |
| Cycle de vente | 2-4 mois |
| Interlocuteur entrée | DG ou Head of Data |
| Signataire | DG |
| Tier entrée (transition) | Starter (1-2 agents, 1 500-2 000 EUR/agent/mois) |
| Contrainte sécurité | RGPD + DPA (suffisant aujourd'hui) |
| Bascule modèle cible | Q3 2027 |
| Clients cibles 2027 | 7-8 |
| Clients cibles 2028 | 18-20 |

### Segment Grand compte (~1Md EUR CA)

| Critère | Valeur |
|---------|--------|
| Use cases année 1 | 2-3 (moy 2.5) |
| Use cases max (année 3+) | 6-8 |
| Rythme d'ajout | ~2/an |
| Cycle de vente | 4-8 mois |
| Interlocuteur entrée | DSI + direction métier |
| Signataire | DSI + direction métier (co-signature) |
| Tier entrée (transition) | Growth (3-5 agents, 2 500-3 000 EUR/agent/mois) |
| Contrainte sécurité | ISO 27001 + DPA |
| Bascule modèle cible | Q4 2027 / Q1 2028 |
| Clients cibles 2027 | 3-4 (dont Bouygues existant) |
| Clients cibles 2028 | 8-10 |

### Segment TGC (~40-50Md EUR CA)

| Critère | Valeur |
|---------|--------|
| Use cases année 1 | 2-3 (moy 3) |
| Use cases max (année 3+) | 10-15 |
| Rythme d'ajout | ~3-4/an |
| Cycle de vente | 6-18 mois |
| Interlocuteur entrée | DSI + direction métier (sponsor interne) |
| Signataire | DSI + DG |
| Tier entrée (transition) | Enterprise (forfait négocié, déploiement personnalisé) |
| Contrainte sécurité | SecNumCloud ou partenariat OVH |
| Bascule modèle cible | 2028+ |
| Clients cibles 2027 | 1-2 (Bouygues = référence, 57Md CA) |
| Clients cibles 2028 | 2-3 |

### Récapitulatif nombre de clients

| Segment | Fin 2026 | Fin 2027 | Fin 2028 |
|---------|----------|----------|----------|
| ETI | 0 | 7-8 | 18-20 |
| Grand compte | 1 (Bouygues) | 3-4 | 8-10 |
| TGC | 0 | 1-2 | 2-3 |
| **Total** | **1** | **12** | **30** |

---

## T2.2 — 4 use cases types chiffrés

### Hypothèses communes

**Coût humain de référence :**
- ETP junior (charge complète) : 50 000 EUR/an
- ETP senior : 70 000 EUR/an

**Modèles IA et coûts :**
| Modèle | Usage | Coût blendé |
|--------|-------|-------------|
| Claude Sonnet | Tâches complexes (facturation, analyse) | ~4 EUR/M tokens |
| Claude Haiku | Tâches simples (saisie, routing) | ~0.6 EUR/M tokens |

**Effort FDE (base 1 150 EUR/jour) :**
- Déploiement facturé forfait 40k quel que soit le temps réel
- Amélioration continue : forfait mensuel (~5j/mois/UC inclus), régie au-delà

---

### Use case 1 — Contrôle de facturation

**Description** : réception factures fournisseurs, rapprochement commandes/contrats, détection anomalies, validation ou rejet automatique.

**Coût humain équivalent :**
| Segment | ETP dédiés | Coût/an |
|---------|-----------|---------|
| ETI | 1 ETP junior | 50 000 EUR |
| Grand compte | 3 ETP junior | 150 000 EUR |
| TGC | 9 ETP | 450 000 EUR |

**Volumétrie tokens :**
| Segment | Factures/mois | Tokens/facture | Tokens/mois |
|---------|--------------|----------------|-------------|
| ETI | 500 | 20k | 10M |
| GC | 5 000 | 20k | 100M |
| TGC | 50 000 | 20k | 1 000M |

**Coût tokens mensuel (Sonnet, 4 EUR/M) :**
- ETI : 40 EUR/mois
- GC : 400 EUR/mois
- TGC : 4 000 EUR/mois

**Effort FDE :**
- Implémentation : 30j (dans forfait 40k)
- Amélioration continue : 3j/mois = ~41k/an

**Prix de vente value-based (ROI x2 client) :**
| Segment | Coût humain/an | Prix cible | Prix/mois |
|---------|---------------|------------|-----------|
| ETI | 50k | 25k/an | **2 000 EUR** |
| GC | 150k | 75k/an | **6 000 EUR** |
| TGC | 450k | 225k/an | **18 000 EUR** |

**Marge brute tokens : 98-99%**

---

### Use case 2 — Service client (triage et résolution)

**Description** : réception demandes clients, classification, résolution automatique des cas simples, routing des cas complexes avec contexte.

**Hypothèse** : l'agent résout automatiquement 30% des tickets.

**Coût humain équivalent (30% des agents) :**
| Segment | Valeur créée/an |
|---------|----------------|
| ETI | 0.3 × 125k = 37k |
| GC | 0.3 × 400k = 120k |
| TGC | 0.3 × 2M = 600k |

**Volumétrie tokens :**
| Segment | Tickets/mois | Tokens/ticket | Tokens/mois |
|---------|-------------|---------------|-------------|
| ETI | 1 000 | 5k | 5M |
| GC | 20 000 | 5k | 100M |
| TGC | 200 000 | 5k | 1 000M |

**Coût tokens mensuel :**
- ETI : 20 EUR/mois
- GC : 400 EUR/mois
- TGC : 4 000 EUR/mois

**Effort FDE :**
- Implémentation : 25j
- Amélioration continue : 4j/mois = ~55k/an

**Prix de vente :**
| Segment | Valeur créée/an | Prix cible | Prix/mois |
|---------|----------------|------------|-----------|
| ETI | 37k | 18k/an | **1 500 EUR** |
| GC | 120k | 60k/an | **5 000 EUR** |
| TGC | 600k | 300k/an | **25 000 EUR** |

**Marge brute tokens : >99%**

---

### Use case 3 — Saisie / exécution dans un outil métier

**Description** : instructions en langage naturel → actions dans ERP/CRM/SIRH (mise à jour données, création entrées, génération rapports).

**Coût humain équivalent :**
| Segment | ETP dédiés | Coût/an |
|---------|-----------|---------|
| ETI | 1 ETP | 50 000 EUR |
| GC | 2 ETP | 100 000 EUR |
| TGC | 5 ETP | 250 000 EUR |

**Volumétrie tokens (Haiku, tâches simples) :**
| Segment | Opérations/mois | Tokens/opération | Tokens/mois |
|---------|----------------|-----------------|-------------|
| ETI | 2 000 | 3k | 6M |
| GC | 20 000 | 3k | 60M |
| TGC | 100 000 | 3k | 300M |

**Coût tokens mensuel (Haiku, 0.6 EUR/M) :**
- ETI : 4 EUR/mois
- GC : 36 EUR/mois
- TGC : 180 EUR/mois

**Effort FDE :**
- Implémentation : 20j
- Amélioration continue : 2j/mois = ~28k/an

**Prix de vente :**
| Segment | Coût humain/an | Prix cible | Prix/mois |
|---------|---------------|------------|-----------|
| ETI | 50k | 25k/an | **2 000 EUR** |
| GC | 100k | 50k/an | **4 000 EUR** |
| TGC | 250k | 125k/an | **10 000 EUR** |

**Marge brute tokens : ~100%**

---

### Use case 4 — Analyse & reporting métier

**Description** : agrégation données multi-sources (ERP, BI, fichiers), analyses récurrentes, détection anomalies, synthèses pour la direction.

**Coût humain équivalent :**
| Segment | ETP dédiés | Coût/an |
|---------|-----------|---------|
| ETI | 1 ETP senior | 60 000 EUR |
| GC | 2 ETP senior | 140 000 EUR |
| TGC | 4 ETP senior | 280 000 EUR |

**Volumétrie tokens (Sonnet) :**
| Segment | Rapports/mois | Tokens/rapport | Tokens/mois |
|---------|--------------|----------------|-------------|
| ETI | 20 | 50k | 1M |
| GC | 100 | 50k | 5M |
| TGC | 500 | 50k | 25M |

**Coût tokens mensuel :**
- ETI : 4 EUR/mois
- GC : 20 EUR/mois
- TGC : 100 EUR/mois

**Effort FDE :**
- Implémentation : 35j (connecteurs multiples)
- Amélioration continue : 4j/mois = ~55k/an

**Prix de vente :**
| Segment | Coût humain/an | Prix cible | Prix/mois |
|---------|---------------|------------|-----------|
| ETI | 60k | 30k/an | **2 500 EUR** |
| GC | 140k | 70k/an | **6 000 EUR** |
| TGC | 280k | 140k/an | **12 000 EUR** |

**Marge brute tokens : ~100%**

---

### Récapitulatif prix modèle cible (par use case / mois)

| Use case | ETI | Grand compte | TGC |
|----------|-----|-------------|-----|
| Facturation | 2 000 EUR | 6 000 EUR | 18 000 EUR |
| Service client | 1 500 EUR | 5 000 EUR | 25 000 EUR |
| Saisie/exécution | 2 000 EUR | 4 000 EUR | 10 000 EUR |
| Analyse/reporting | 2 500 EUR | 6 000 EUR | 12 000 EUR |
| **Moyenne** | **2 000 EUR** | **5 250 EUR** | **16 250 EUR** |

### Récapitulatif effort FDE (moyenne)

| Métrique | Valeur |
|---------|--------|
| Implémentation moyenne | ~27.5j/use case |
| Amélioration continue moyenne | ~3.25j/mois/use case |
| Coût AC annuel moyen | ~45k/an/use case |

---

## T2.3 — Projection CA 2026-2028

### 2026

**Contexte** : Jan-Sept service pur (contrats existants), Sept-Oct déploiement Bouygues plateforme, Déc 1 mois de run.

**CA plateforme 2026 :**
```
Atelier Bouygues         :  20 000 EUR
Déploiement 2 UC         :  80 000 EUR  (2 × 40k)
1 mois run abonnement GC :  10 000 EUR  (2 UC × ~5k/mois)
Sous-total plateforme    : ~110 000 EUR
```

**CA service pur 2026 (Jan-Sept) :**
- Jan-Juin actuals (Qonto) : **183 907 EUR** *(source : vc_case.yaml > jan_jun_2026_commercial_revenue)*
- Juil-Sept (forecast) : 25k + 25k + 30k = **80 000 EUR** *(source : vc_case.yaml > service_forecast_baseline)*
- **Total service pur Jan-Sept : ~264 000 EUR**

**CA total 2026 : ~374k** (264k service pur + 110k plateforme)

**ARR annualisé fin 2026 :** ~126k (2 UC × 5.25k/mois × 12)

---

### 2027

**Hypothèse ramp clients :**
| Trimestre | Nouveaux clients | Segment |
|-----------|----------------|---------|
| Q1 | 2 | ETI |
| Q2 | 3 | ETI |
| Q3 | 4 | 2 ETI + 1 GC + 1 TGC |
| Q4 | 3 | 1 ETI + 1 GC |
| **Total** | **12** | 8 ETI + 3 GC + 1 TGC |

**One-shot 2027 :**
```
Ateliers (12 clients) : 12 × 20k = 240k
Déploiements ETI (8 × 1.5 UC × 40k) = 480k
Déploiements GC (3 nouveaux × 2.5 UC × 40k) = 300k
Déploiements TGC (1 × 3 UC × 40k) = 120k
Déploiements Bouygues UC supplémentaires (2 UC) = 80k
Total one-shot : ~1 220k
```

**ARR plateforme fin 2027 :**
```
ETI (8 clients × 1.5 UC × 2k/mois × 12) = 288k
GC (4 clients × 2.5 UC × 5.25k/mois × 12) = 630k
TGC (1 client, forfait ~200k/an) = 200k
Total ARR plateforme : ~1 118k
```

**ARR service fin 2027 (amélioration continue) :**
```
25 UC total × 45k/an = 1 125k
```

**CA encaissé 2027 :**
```
One-shot          : ~1 220k
ARR plateforme    :   ~401k  (encaissé prorata)
ARR service       :   ~844k  (encaissé moy 9 mois)
Total CA 2027     : ~2 465k ≈ 2.5M
```

**ARR total annualisé fin 2027 : ~2.25M**
*(vs cible Jean ~2.4M — écart -6%, cohérent)*

---

### 2028

**One-shot 2028 :**
```
Ateliers nouveaux (18 clients) : 360k
Déploiements nouveaux clients  : ~1 280k
Déploiements upsell UC existants : ~920k
Total one-shot : ~2 560k
```

**ARR modèle cible fin 2028 :**
```
ETI (19 clients × 2.5 UC × 2k/mois × 12)  = 1 140k
GC (9 clients × 4 UC × 5.25k/mois × 12)   = 2 268k
TGC (2 clients × 5 UC, forfait ~350k/an)   =   700k
Total ARR plateforme : ~4 108k
ARR service résiduel TGC : ~450k
ARR total : ~4 558k
```

**CA encaissé 2028 :**
```
One-shot       : ~2 560k
ARR plateforme : ~4 108k
ARR service    :   ~450k
Total CA 2028  : ~7 118k ≈ 7.1M
```

---

### Tableau de synthèse

| Métrique | 2026 | 2027 | 2028 |
|---------|------|------|------|
| CA total encaissé | ~374k (264k service pur + 110k plateforme) | ~2.5M | ~7.1M |
| ARR annualisé fin d'année | ~126k | ~2.25M | ~4.55M |
| dont ARR plateforme | ~126k | ~1.12M | ~4.1M |
| dont ARR service | ~0 | ~1.13M | ~450k |
| Ratio plateforme/ARR total | ~100% | ~50% | ~90% |
| Clients actifs | 1 | 12 | 30 |
| Use cases actifs | 2 | ~25 | ~70 |
| One-shot | ~100k | ~1.22M | ~2.56M |

---

### Cohérence avec objectifs réunion Jean

| Objectif Jean | Calculé | Écart | Statut |
|--------------|---------|-------|--------|
| CA 2027 ~2.8M | ~2.5M | -11% | Cohérent (Jean visait "un peu agressif") |
| ARR 2027 ~2.4M | ~2.25M | -6% | Cohérent |
| CA 2028 ~7M | ~7.1M | +1% | Aligné |
| 12 clients 2027 | 12 | 0% | Exact |
| 30 clients 2028 | 30 | 0% | Exact |

---

## Points ouverts

1. **CA service pur 2026** : chiffré à ~264k (183k actuals Qonto Jan-Juin + 80k forecast Juil-Sept) — source vc_case.yaml
2. **Ratio crédit/token** : à fixer précisément pour calibrer les prix de credits (abonnement léger + crédits prépayés)
3. **Prix abonnement léger** (accès plateforme de base, hors crédits) : à définir — peut être un flat fee mensuel faible (ex : 500-1000 EUR/mois) qui ouvre l'accès

---

## Décisions actées (récap T2)

| # | Décision | Source |
|---|----------|--------|
| 1 | Value-based pricing : prix = coût humain / 2 (ROI x2 client) | Validé |
| 2 | Marge brute tokens >94% — le vrai coût est le FDE amorti | Calculé |
| 3 | Modèle final = abonnement léger + crédits (1 crédit = X tokens) | Validé |
| 4 | 4 use cases types : facturation, service client, saisie/exec, reporting | Validé |
| 5 | Prix moyens : ETI 2k/UC/mois, GC 5.25k, TGC 16.25k | Validé |
| 6 | Effort FDE moyen : 27.5j implem + 45k/an AC | Validé |
| 7 | CA 2027 ~2.5M, ARR fin 2027 ~2.25M | Calculé, cohérent avec Jean |
| 8 | CA 2028 ~7.1M, ARR fin 2028 ~4.55M | Calculé, aligné avec Jean |
| 9 | 2026 plateforme ~110k encaissé + service pur à renseigner | Partiel |
