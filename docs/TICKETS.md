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

**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : Aucune

**Description** :
Definir 3 profils d'entreprises cibles avec des hypotheses chiffrees pour chacun.

**Livrable** :
Un tableau par segment :

| Critere | ETI (~100M CA) | Grand compte (~1Md CA) | Tres grand compte (~40-50Md CA) |
|---------|----------------|------------------------|---------------------------------|
| Nombre de use cases potentiels | ? | ? | ? |
| Rythme d'ajout use cases/an | ? | ? | ? |
| Ticket moyen deploiement | ? | ? | ? |
| Ticket moyen recurrent/an | ? | ? | ? |
| Cycle de vente estime | ? | ? | ? |
| Contraintes securite | ? | ? | ? |
| Nombre de clients vises 2027 | ? | ? | ? |

**Hypotheses structurantes a respecter** :
- Max 3 tres grands comptes en 2027 (realiste)
- L'essentiel du volume vient des ETI et grands comptes
- Bouygues (57Md CA) = reference pour le segment tres grand compte
- 12 entreprises total en 2027, 30 en 2028

**Offres a profiler par segment** :
- Quels packages pour chaque taille ?
- Quel prix d'entree vs prix cible a terme ?

---

### T2.2 — Chiffrer 3-4 use cases types

**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : Aucune (peut etre fait en parallele de T2.1)

**Description** :
Prendre 3-4 cas d'usage representatifs et estimer pour chacun les couts, volumetries et revenus.

**Use cases retenus** :
1. **Facturation** — controle, rapprochement, detection d'anomalies
2. **Service client** — triage, resolution automatisee, escalade
3. **Saisie/execution dans un outil** — automatisation de workflows metier
4. **[A definir]** — identifier un 4e use case classique (suggestions : conformite/audit, RH/onboarding, procurement)

**Pour chaque use case, estimer** :

| Dimension | A chiffrer |
|-----------|-----------|
| Volumetrie tokens (input/output par resolution) | ex : combien de tokens pour traiter une facture ? |
| Volume mensuel typique par segment client | ex : 1000 factures/mois pour une ETI, 50 000 pour un grand compte |
| Effort d'implementation (jours FDE) | ex : 20 jours, 40 jours, 60 jours |
| Effort amelioration continue (jours FDE/an) | ex : 5 jours/an (quasi-automatise) vs 60 jours/an (complexe) |
| Cout tokens mensuel pour nous | en EUR |
| Cout FDE imputable | en EUR (base 1 150 EUR/jour) |
| Prix de vente (transition) | deploiement + recurrent |
| Prix de vente (modele cible, usage-based) | marge token + fee plateforme |
| Marge par use case | brute et nette |

**Observation terrain a integrer** :
- Bouygues Telecom Wholesale : 2 agents facturation, dont 1 tres simple. Volumetrie relativement tranquille.
- Possibilite de generer du revenu recurrent vite via petits abonnements (10-15k/use case/an) meme en transition.

---

### T2.3 — Recaler la grille de pricing de transition et projeter le CA 2026-2028

**Priorite** : Haute
**Owner** : Matthieu
**Dependances** : T2.1, T2.2

**Description** :
A partir des typologies clients et des use cases chiffres, construire la grille de pricing definitive pour la phase de transition et en deduire un CA credible annee par annee.

**Grille de base discutee** :

| Poste | Montant | Frequence |
|-------|---------|-----------|
| Atelier decouverte | 20 000 EUR | One-shot par engagement |
| Deploiement | 40 000 EUR | One-shot par use case |
| Amelioration continue | ~50 000 EUR/an (moyenne) | Recurrent, grande variabilite |
| Abonnement plateforme (entree) | 15-20k EUR/an/use case | Recurrent |
| Abonnement plateforme (enterprise) | 200-300k EUR/an | Recurrent, quand 4-5+ use cases |

**Logique de montee en valeur a modeliser** :
1. Client entre a 40k/an pour 2 agents (phase test, facile a acheter)
2. Constate la valeur en 3-6 mois
3. Demande plus d'agents / features
4. On propose package superieur (silver → gold → enterprise)
5. Cible : 200-300k/an par client au bout de 12-18 mois

**Projection CA a produire** :
- CA 2026 : distinguer signe vs facture (le facture est plus bas que le signe)
- CA 2027 : ventile par segment + par poste (one-shot vs recurrent)
- CA 2028 : inclure la bascule progressive vers usage-based

**Point d'attention** :
- Le pricing de transition en petits abonnements par use case (10-15k) peut generer du CA rapide si on multiplie les micro-deployments (type Bouygues Wholesale)
- Ne pas projeter au-dela de 2028

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
