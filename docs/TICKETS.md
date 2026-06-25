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

**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : T2.1 (nombre de use cases par annee)

**Description** :
Construire le modele de staffing FDE base sur le nombre de use cases (pas le CA).

**Parametres** :
- Taux journalier de vente : 1 150 EUR/jour
- Base annuelle : 210 jours
- CA max par FDE : ~241 500 EUR/an (1 150 x 210)
- Capacite moyenne : ~4 use cases/an par FDE (variabilite forte)
- Les FDEs font aussi les ateliers (pas que le deploy/maintenance)

**Trajectoire a modeliser** :
- Fin 2026 : 3-4 FDEs (Jean insiste pour ne pas commencer a 2)
- 2027 : adapter au nombre de use cases cibles (24 use cases / ~4 par FDE = 6 FDEs theoriques, mais certains use cases sont quasi-automatises)
- 2028 : 4-6 FDEs minimum + prise en compte de l'automatisation progressive

**Facteurs a integrer** :
- Tous les use cases ne demandent pas un FDE a temps plein (certains resolus en 3 mois, d'autres demandent 3 ans)
- Probabilite d'automatisation croissante au fil des annees (reduit le besoin de FDE par use case)
- Un PM peut gerer 4 clients simultanement
- Variabilite : some use cases = 3 mois, others = amelioration continue permanente

---

### T3.2 — Budget marketing + bureaux

**Priorite** : Moyenne
**Owner** : Matthieu
**Dependances** : Aucune

**Description** :
Integrer les couts marketing et bureaux dans le modele de depenses.

**Marketing** :
- Actuel : ~3 000 EUR/mois = 36k/an
- Cible 2027 : tripler = ~100 000 EUR/an
- Objectif : doubler la pipeline de sales
- Profil de depenses : croissance progressive (pas un step function)

**Bureaux** :
- A chiffrer selon les besoins (2026 : taille actuelle, 2027-2028 : croissance equipe)

---

### T3.3 — Couts RH/back-office et certification

**Priorite** : Moyenne
**Owner** : Matthieu
**Dependances** : T4.1 (trajectoire SecNumCloud)

**Description** :
Anticiper les couts indirects lies a la croissance et a la strategie enterprise.

**RH / Back-office** :
- Anticiper un recrutement admin/facturation d'ici 2028
- Besoin : gestion de la facturation, back-office client, support admin
- Timing : probablement mi-2027 ou debut 2028 selon la croissance

**Certification** :
- Couts lies a la trajectoire SecNumCloud
- Timeline : plutot 2028
- Nature : audit, conformite, eventuellement consultants externes
- A chiffrer une fois la trajectoire T4.1 definie

---

## T4 — Strategie enterprise & infra

### T4.1 — Definir la trajectoire SecNumCloud

**Priorite** : Moyenne
**Owner** : Matthieu / a definir
**Dependances** : Aucune

**Description** :
Cartographier le chemin vers SecNumCloud : contraintes, timeline, couts, jalons.

**Questions a resoudre** :
- Quelles sont les exigences exactes pour la qualification SecNumCloud ?
- Quel est le delai realiste (estimation actuelle : 2-3 ans) ?
- Quels couts (audit, mise en conformite, infra) ?
- Est-ce qu'on le fait seul ou via un partenaire (cf T4.2) ?
- Quel jalon precis mettre dans le BP pour la bascule vers usage-based ?

**Contexte** :
- Les grandes entreprises sont "paranos de la securite"
- SecNumCloud est le prerequis pour facturer les tokens en direct (usage-based)
- Sans ca, impossible de "refacturer le modele" aux clients enterprise
- C'est le verrou principal vers le modele cible

---

### T4.2 — Explorer le partenariat OVH

**Priorite** : Moyenne
**Owner** : Matthieu / a definir
**Dependances** : T4.1

**Description** :
Evaluer la faisabilite d'un partenariat OVH comme chemin accelere vers le modele cible.

**Hypothese** :
Jean identifie OVH comme "le chemin le plus facile" vers un deploiement compatible exigences enterprise (SecNumCloud / souverainete).

**Questions a resoudre** :
- OVH propose-t-il deja une offre SecNumCloud compatible avec nos besoins ?
- Quel type de partenariat (technique, commercial, les deux) ?
- Quels delais vs le faire en solo ?
- Quels couts / contraintes ?
- Y a-t-il des contacts existants a activer ?

---

## T5 — Integration au BP

### T5.1 — Mettre a jour le modele financier complet

**Priorite** : Haute (mais derniere dans l'ordre d'execution)
**Owner** : Matthieu
**Dependances** : T1.3, T2.3, T3.1, T3.2, T3.3

**Description** :
Integrer tous les inputs des tickets precedents dans le modele financier du BP.

**Contenu** :
- Revenus : ventiles par poste (atelier, deploy, amelioration continue, abonnement) x par segment client x par annee
- ARR total vs ARR plateforme (trajectoire)
- Depenses : FDEs, marketing, bureaux, RH, certification
- Headcount : trajectoire par role
- Marges : par use case type, par segment, globale
- KPIs : #entreprises, #use cases, CA/client moyen, ratio service/plateforme

**Horizon** : 2026-2028 uniquement (pas au-dela)

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
