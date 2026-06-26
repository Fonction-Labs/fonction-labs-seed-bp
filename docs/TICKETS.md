# Tickets — Refonte Business Plan post-reunion Jean (24/06/2026)

Ref : [Synthese reunion](./2026-06-24_reunion-jean-bp-synthese.md)

---

## T1 — Narrative & structure du BP

### T1.1 — Rediger la narrative "3 etapes"

**Statut** : DONE
**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : Aucune (premier chantier)
**Doc de reference** : [T1.1_narrative-3-etapes_conclusions.md](./T1.1_narrative-3-etapes_conclusions.md)

**Conclusions principales** :
- 3 phases : Transition (2026), Elargissement (2027), Growth exponentielle (2028)
- Modele transition (sept 2026 → Q3 2027) : abonnement per-agent (1.5-2k EUR/mois) + service FDE facture separement
- Modele SaaS (Q3 2027+) : usage-based (tokens/succes) + packages enterprise avec FDE integre (Option C : FDE = cout de delivery, pas un produit)
- Bascule progressive par segment : ETI d'abord (Q3 2027), grands comptes (Q4 2027), TGC (2028+ / SecNumCloud)
- Regression service pur : stop new business post-levee, <10% fin 2027, ~0 en 2028
- Split clients plateforme : ETI majoritaire (7-8 en 2027), GC (3-4), TGC (1-2 max)
- Ton VC : "on est deja plateforme avec du service en complement"
- Position SaaS : on gere les modeles pour le client, on revend les tokens avec marge

---

### T1.2 — Documenter "modele intermediaire" vs "modele cible"

**Statut** : DONE
**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : Aucune
**Doc de reference** : [T1.2_modeles-intermediaire-vs-cible_conclusions.md](./T1.2_modeles-intermediaire-vs-cible_conclusions.md)

**Conclusions principales** :
- Modele intermediaire = 2 lignes (abonnement per-agent + service FDE en forfait mensuel)
- Tiers : Starter (1.5-2k/agent/mois) / Growth (2.5-3k/agent/mois) / Enterprise (forfait negocie, deploiement personnalise)
- Modele cible = credits (standard, marge ~30%) + success fee par case "done" (option premium)
- FDE dans le modele cible = cout de delivery integre au package enterprise (pas un produit vendu)
- ETI self-service = amelioration continue via SDK client (roadmap M5)
- Bascule progressive : ETI Q3 2027 (RGPD suffit) → GC Q4 2027 (ISO 27001) → TGC 2028+ (SecNumCloud/OVH)
- Transition client = grandfathering + migration incitee au renouvellement
- SLA = custom par client pour l'instant

---

### T1.3 — Creer la vue decomposee "ARR total" vs "ARR plateforme"

**Statut** : DONE (methodologie) — chiffres precis a remplir apres T2.1/T2.2/T2.3
**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : T2.1, T2.2, T2.3 pour les chiffres exacts
**Doc de reference** : [T1.3_arr-decomposition_conclusions.md](./T1.3_arr-decomposition_conclusions.md)

**Conclusions principales** :
- La decomposition ARR plateforme vs ARR service n'est pertinente que pour 2026-2027 (modele de transition)
- En 2028 (modele cible), le FDE est un cout de delivery interne — plus de ligne "service" dans le revenu
- 3 buckets en transition : one-shot (atelier + deploy, non recurrent), ARR service (amelioration continue ~50k/an/use case), ARR plateforme (per-agent)
- Ordres de grandeur 2027 : ~1.15M ARR plateforme + ~1.2M ARR service = ~2.35M total (a affiner avec T2)
- ARR fin 2026 recalcule a ~48k (pas 120k — l'ancien pricing 10k/mois est abandonne)
- One-shot toujours traite comme revenue non recurrent, jamais annualise (Option A actee)

---

## T2 — Segmentation clients & pricing

### T2.1 — Construire les 3 typologies clients

**Statut** : DONE (validé)
**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : Aucune
**Doc de reference** : [T2_synthese-complete_conclusions.md](./T2_synthese-complete_conclusions.md)

**Conclusions principales** :
- ETI : 1-2 UC annee 1, rythme +1/an, cycle 2-4 mois, interlocuteur DG/Head of Data, tier Starter
- GC : 2-3 UC annee 1, rythme +2/an, cycle 4-8 mois, interlocuteur DSI+metier, tier Growth
- TGC : 3 UC annee 1, rythme +3-4/an, cycle 6-18 mois, interlocuteur DSI+RSSI, tier Enterprise
- Clients : 1 fin 2026 / 12 fin 2027 / 30 fin 2028

---

### T2.2 — Chiffrer 3-4 use cases types

**Statut** : DONE (validé)
**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : Aucune
**Doc de reference** : [T2_synthese-complete_conclusions.md](./T2_synthese-complete_conclusions.md)

**Conclusions principales** :
- 4 use cases : Facturation, Service client, Saisie/execution, Analyse/reporting
- Value-based pricing : prix = cout humain / 2 (ROI x2 client minimum)
- Prix moyens : ETI 2k/UC/mois, GC 5.25k, TGC 16.25k
- Cout tokens negligeable (marge brute >94%) — vrai cout = FDE amorti (~45k/an/UC)
- Modele final = abonnement leger + credits prepay (1 credit = X tokens)

---

### T2.3 — Recaler la grille de pricing et projeter le CA 2026-2028

**Statut** : DONE (validé)
**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : T2.1, T2.2
**Doc de reference** : [T2_synthese-complete_conclusions.md](./T2_synthese-complete_conclusions.md)

**Conclusions principales** :
- CA 2026 total : ~374k (264k service pur actuals/forecast Qonto + 110k plateforme)
- CA 2027 : ~2.5M (1.22M one-shot + 0.4M ARR plateforme + 0.84M ARR service)
- CA 2028 : ~7.1M (2.56M one-shot + 4.1M ARR plateforme)
- ARR fin 2027 : ~2.25M / fin 2028 : ~4.55M
- Coherent avec Jean (ecart max -11% sur 2027, +1% sur 2028)
- Point ouvert : ratio credit/token et prix abonnement leger a fixer
- "600k signe 2026" ≠ CA facture — distinction importante pour le BP

---

## T3 — Modele de depenses

### T3.1 — Modeliser le headcount FDE

**Statut** : DONE (validé)
**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : T2.1
**Doc de reference** : [T3_depenses-headcount_conclusions.md](./T3_depenses-headcount_conclusions.md)

**Conclusions principales** :
- Formule FDE : #FDE = (UC_deploy × 1.0) + (UC_AC × 0.25) — remplace toute cible arbitraire
- Contrainte deploy : 1 FDE focalisé sur 1 UC actif en déploiement
- AC : 1 FDE gère 4 UC simultanément (0.25 FDE/UC)
- Coût FDE interne : 11k/mois fully loaded (maintien YAML — cohérent CDI senior Paris)
- YAML sous-estime significativement : ~4 FDE fin 2027 vs ~9 formule → recalibration en T5.1
- Calibration mois par mois : à faire en T5.1 depuis enterprise_cohort_plan

---

### T3.2 — Budget marketing + bureaux + headcount non-FDE

**Statut** : DONE (validé)
**Priorite** : Moyenne
**Owner** : Matthieu
**Dependances** : Aucune
**Doc de reference** : [T3_depenses-headcount_conclusions.md](./T3_depenses-headcount_conclusions.md)

**Conclusions principales** :
- Nomenclature simplifiée : Lead AI Engineer / AI Engineer / Sales Engineer / Sales / Customer Ops
- Sales Engineer ajouté déc 2026 (10k/mois) — quasi recruté, absent du YAML
- Sales Dev avancé à jan 2027 (vs oct 2027 YAML) — pour nourrir le pipeline 2028
- Marketing : ligne séparée opex_base (+64k/an en 2027, +114k/an en 2028)
- Bureaux : dans opex_base YAML, pas de changement
- AI dev tooling : ligne absente du YAML — ~3k/mois 2026, ~8k/mois 2027, ~12k/mois 2028 (~1k/personne technique)

---

### T3.3 — RH/back-office, certification, Wassym, marge brute

**Statut** : DONE (validé)
**Priorite** : Moyenne
**Owner** : Matthieu
**Dependances** : T4.1 (trajectoire SecNumCloud)
**Doc de reference** : [T3_depenses-headcount_conclusions.md](./T3_depenses-headcount_conclusions.md)

**Conclusions principales** :
- Customer Ops : maintenir YAML (juillet 2027, 8k/mois fully loaded)
- ISO 27001 : maintenir jalons YAML (30-40k par jalon) — lancer maintenant si pas commencé (12-18 mois)
- SecNumCloud : TBD post-T4.1/T4.2 — non chiffré dans le BP actuel
- Wassym BPCE : corrigé dans YAML (20j/mois, 950 EUR/j) — sous-estimation de +16k/mois revenu corrigée
- Wassym non affiché comme ligne séparée dans les outputs agrégés
- Gross margin = formule dérivée (COGS = FDE + tokens + infra client-facing) — ~57% estimé 2027
- Règle pipeline : tout output = hypothèse nommée ou formule — zéro hardcode (documenté dans AGENT.md)

---

## T4 — Strategie enterprise & infra

### T4.1 — Definir la trajectoire SecNumCloud

**Statut** : DONE (validé)
**Priorite** : Moyenne
**Owner** : Matthieu
**Dependances** : Aucune
**Doc de reference** : [T4_strategie-enterprise_conclusions.md](./T4_strategie-enterprise_conclusions.md)

**Conclusions principales** :
- Approche retenue : hébergement sur OVH S3NS (JV OVH × Thales, qualifiée SecNumCloud) — pas certification produit propre
- Certification produit propre abandonnée (100-300k+, 2-3 ans — hors scope BP)
- AWS non qualifié SecNumCloud → disqualifié pour les TGC français
- Jalon BP : Q1 2027 partenariat OVH formalisé → infrastructure qualifiée disponible → déblocage TGC

---

### T4.2 — Explorer le partenariat OVH

**Statut** : DONE (validé)
**Priorite** : Moyenne
**Owner** : Matthieu
**Dependances** : T4.1
**Doc de reference** : [T4_strategie-enterprise_conclusions.md](./T4_strategie-enterprise_conclusions.md)

**Conclusions principales** :
- Contact OVH existant (bien placé) — à activer juil-sept 2026 sur dimensions technique + commercial
- Priorité : hébergement qualifié OVH S3NS d'abord, partenariat commercial ensuite
- AWS/Azure : options valides pour ETI et GC (ISO 27001 suffit)
- Coût OVH S3NS (~20-30% premium vs AWS standard) inclus dans budget infra cloud T3.4
- Prospection TGC à démarrer Q1 2027 (cycle 6-18 mois → closes H1 2028)

---

## T5 — Integration au BP

### T5.1 — Mettre a jour le modele financier complet

**Statut** : DONE
**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : T1.3, T2.3, T3.1, T3.2, T3.3

**Description** :
Integrer tous les inputs des tickets precedents dans le modele financier du BP.

**Contenu livré** :
- Revenue 100% formula-driven : workshop (cohort) + deploy 40k/UC (cohort) + FDE billable (formule live UC × utilization) + plateforme (segment pricing × live UC)
- Actuals H1 2026 = facturé Qonto (335k€)
- COGS bottom-up : FDE hires réels + freelances + tokens + infra cloud + Freelance BPCE
- Opex décomposé : bureaux/admin/marketing/misc (sous-lignes nommées) + security/legal + AI tooling (formule) + SaaS
- Cold callers (Mooniz) + Sales freelance avec dates de fin
- Headcount accéléré (15 fin 2027) pour justifier le seed de 2.5M€
- Cohort plan réaliste (cycle vente 3-6 mois, gaps trimestriels)

**Targets révisées (vs T2.3 initiaux)** :
- Clients fin 2027 : 8 (vs 12 initial — cycle rallongé pour réalisme)
- UC live fin 2027 : 18 (vs 25 — conséquence directe)
- Clients fin 2028 : 20 (vs 30 — idem)
- UC live fin 2028 : 59 (vs 70 — idem)
- Justification : cycle enterprise 3-6 mois (vs 1-2 mois implicite avant), pas de signature chaque mois

**KPIs finaux** :
- Revenue 2026: 567k€ | 2027: 1.65M€ | 2028: 5.37M€
- ARR fin 2027: 1.35M€ | fin 2028: 3.9M€
- Gross margin: 51% → 53% → 75%
- Cash fin 2027: 1.39M€ (burn 1.13M€ en 15 mois post-seed)

**Horizon** : 2026-2028 uniquement (pas au-dela)

---

### T5.3 — Simulation Monte Carlo du pipeline commercial

**Statut** : TODO
**Priorite** : Basse (post-pitch, amélioration future)
**Owner** : Matthieu
**Dependances** : T5.1

**Description** :
Ajouter une couche probabiliste au cohort plan. Aujourd'hui chaque client signe à date fixe (déterministe). En réalité, le pipeline a un taux de conversion et un délai variable.

**Contenu** :
- Distribution sur les dates de signature (± 1-2 mois)
- Taux de conversion pipeline → signé (ex: 30-40% pour ETI, 20-25% pour GC/TGC)
- Simulation N tirages → distribution de l'ARR fin 2027 (P10 / P50 / P90)
- Représentation bayésienne dans le dashboard (fan chart ou confidence intervals)
- Permet de répondre à "quel est le worst case réaliste ?" en pitch

**Note** : le modèle déterministe actuel est suffisant pour le pitch seed. Le Monte Carlo serait un bonus pour la data room ou un suivi post-levée.

---

### T5.2 — Mettre a jour le deck/pitch

**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : T1.1, T5.1

**Description** :
Aligner le deck de presentation aux VCs avec la nouvelle narrative et les nouveaux chiffres.

**Contenu a mettre a jour** :
- Slide narrative "3 etapes" (transition → elargissement → growth)
- Slide business model (modele intermediaire + modele cible + conditions de bascule)
- Slide financier (avec decomposition ARR total vs ARR plateforme)
- Slide depenses / use of funds
- Slide strategie enterprise (trajectoire SecNumCloud, positionnement "proprietaire critique")
- Message "on accepte moins de profit court terme pour devenir incontournable"

---

## Ordre d'execution recommande

```
Semaine 1 :  T1.1 + T1.2 + T2.1 + T2.2  (en parallele, pas de dependances)
Semaine 2 :  T2.3 + T3.1 + T3.2           (pricing + depenses)
Semaine 3 :  T1.3 + T3.3 + T4.1 + T4.2   (ARR decompose + couts indirects + strategie)
Semaine 4 :  T5.1 + T5.2                   (integration finale)
```

---

## Checklist de validation finale

- [ ] La narrative 3 etapes est coherente avec tous les chiffres
- [ ] On distingue clairement signe vs facture pour 2026
- [ ] ARR total vs ARR plateforme est explicite et honnete
- [ ] Chaque segment client a un profil d'offre chiffre
- [ ] Au moins 3 use cases sont chiffres en detail (volumetrie, effort, marge)
- [ ] La grille de pricing de transition est credible (passe le test de l'arbitrage client)
- [ ] Le headcount FDE est coherent avec le nombre de use cases
- [ ] Les depenses sont completes (FDE, marketing, bureaux, RH, certif)
- [ ] La trajectoire SecNumCloud a un jalon date
- [ ] Le BP ne projette pas au-dela de 2028
- [ ] Le message VC est clair : land-and-expand → proprietaire critique → usage-based high-margin
