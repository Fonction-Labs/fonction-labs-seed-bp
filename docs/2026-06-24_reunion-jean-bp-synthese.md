# Synthese reunion Jean — Business Plan

**Date** : 24 juin 2026
**Participants** : Jean, Matthieu (+ mentions Antoine pour historique pricing)

---

## 1. Constat de depart et objectifs de la discussion

Le BP actuel presente des projections de revenus (600k fin 2026, 2.8M en 2027, 7M en 2028) mais souffre de plusieurs faiblesses :

- Pas de distinction claire entre revenu "service/people" et revenu "plateforme/logiciel"
- Le modele economique n'est pas arrete (usage-based vs abonnement vs hybride)
- Les hypotheses de pricing ne sont pas suffisamment ancrees dans la realite terrain (arbitrage client)
- La partie depenses/headcount est absente
- La trajectoire vers un modele scalable (usage-based) est bloquee par les contraintes enterprise (SecNumCloud)

---

## 2. Narrative "3 etapes" a structurer

### 2026 — Transition / Demarrage
- Continuer l'effort commercial
- Revenu deja present mais domine par le service (deploy + amelioration continue)
- Petit frais de plateforme en complement
- Objectif : signer les premiers clients, demontrer la valeur

### 2027 — Elargissement des use cases
- Couverture de plus de cas d'usage par client
- Montee en gamme progressive (packages silver/gold/enterprise)
- Cible : 12 entreprises, 24 use cases live
- Revenus cibles : ~2.8M total, ~2.4M ARR

### 2028 — Croissance exponentielle
- Bascule vers usage-based (si SecNumCloud atteint ou partenariat OVH)
- 30 entreprises, 60 use cases
- Revenus cibles : ~7M
- Part plateforme dominante dans le mix revenus

---

## 3. Modele economique : decisions prises

### Modele intermediaire (phase de transition — maintenant a mi-2027)

**Principe** : Service + petit fee plateforme. Le plus facile a vendre, le plus realiste.

**Composantes** :
- **Atelier decouverte** : ~20 000 EUR
- **Deploiement par use case** : ~40 000 EUR
- **Amelioration continue** : variable, moyenne estimee ~50 000 EUR/an (ou 15-20k/an par use case selon packaging)
- **Abonnement plateforme** : debute tres bas (ex : 40k/an pour 2 agents chez Bouygues en phase 1), monte progressivement

**Strategie de montee en gamme** :
- Commencer par une offre volontairement limitee et abordable
- Rendre le client "accro" via la valeur demonstree
- Proposer des packages superieurs (silver, gold, enterprise)
- Exemple Bouygues : 40k/an pour 2 agents → formule enterprise ~300k/an quand 3-4-5 agents + features avancees

### Modele cible (post-SecNumCloud / partenariat OVH)

**Principe** : Usage-based (facturation au token/usage avec marge ~30%)

**Prerequis** :
- Hebergement compatible exigences enterprise (SecNumCloud)
- Ou partenariat OVH comme "chemin le plus facile"
- Delai estime : 2-3 ans

**Pourquoi le VC veut entendre ca** :
- Controle de la supply chain complete
- Marges bien superieures sur l'usage vs abonnement fixe
- Positionnement "proprietaire critique" dans les grandes entreprises
- Lock-in par l'integration a tout l'ecosysteme du client

---

## 4. Transparence ARR pour les VCs

### Decomposition necessaire
- **ARR total** = tout le revenu recurrent (service inclus)
- **ARR plateforme** = uniquement la part logiciel sans ressources humaines

### Position convenue
- Etre honnete et transparent sur l'etat actuel (domine par le service)
- Montrer la trajectoire : la part service diminue, la part plateforme augmente
- Le VC doit comprendre qu'on accepte moins de profit court terme pour devenir un "proprietaire critique" dans les grandes entreprises
- Ne pas chercher a masquer la part people — l'assumer comme un choix strategique de la phase de transition

### Chiffres cles actuels
- ARR annualise possible fin 2026 (abonnement seul) : ~120k EUR
- Le reste du revenu = service/FDE (recurrent mais percu comme "people-based")

---

## 5. Typologies de clients a profiler

Trois segments retenus :

| Segment | CA entreprise | Profil |
|---------|--------------|--------|
| ETI | ~100M EUR | Plus simple a acquerir, moins de use cases |
| Grand compte | ~1Md EUR | Volume intermediaire |
| Tres grand compte | ~40-50Md EUR | Beaucoup de use cases, cycles longs, exigences securite maximales |

**Pour chaque segment, definir** :
- Nombre de use cases potentiels (et rythme d'ajout)
- Ticket moyen (deploiement + recurrent)
- Cycle de vente
- Contraintes specifiques (securite, procurement, etc.)

**Hypothese structurante** : on n'aura probablement pas plus de 3 tres grands comptes en 2027. L'essentiel viendra des ETI et grands comptes.

---

## 6. Use cases types a chiffrer

4 typologies d'agents retenues pour modeliser le pricing :

1. **Facturation** (controle, rapprochement, anomalies)
2. **Service client** (triage, resolution, escalade)
3. **Saisie/execution dans un outil** (automatisation de workflows metier)
4. **[A definir — 4e use case classique]**

**Pour chaque use case, estimer** :
- Volumetrie tokens (input/output par resolution)
- Effort d'implementation (jours ingenieur)
- Effort d'amelioration continue (recurrent vs one-shot)
- Prix coutant vs prix de vente
- Marge par use case

**Observation terrain importante** : Bouygues Telecom Wholesale a plein de cas d'usage resolvables rapidement → possibilite de generer du revenu recurrent vite meme en transition (10-15k/use case/an en abonnement).

---

## 7. Pricing de transition — Hypotheses a recaler

### Grille discutee

| Poste | Montant | Notes |
|-------|---------|-------|
| Atelier decouverte | 20 000 EUR | Par engagement |
| Deploiement | 40 000 EUR | Par use case |
| Amelioration continue (moyenne) | 50 000 EUR/an | Grande variabilite selon complexite |
| Abonnement plateforme (entree) | 15-20k EUR/an/use case | Offre limitee, facile a acheter |
| Abonnement plateforme (enterprise) | 200-300k EUR/an | Quand 4-5+ use cases + features premium |

### Logique de montee en valeur
1. Offre d'entree tres abordable (ex : 40k/an pour 2 agents)
2. Le client constate la valeur
3. Besoin de plus d'agents / plus de features
4. Proposition package superieur (silver → gold → enterprise)
5. Le client ne peut plus se passer de la plateforme (lock-in ecosystemique)

### Point d'attention critique
- L'arbitrage client existe toujours : Fonction vs prestataire vs internalisation
- A 10k/mois/use case, le client peut considerer qu'il replique seul
- La valeur doit etre justifiee par : rapidite, integration, amelioration continue, features plateforme exclusives
- Si le client peut "finir" le projet et ne plus avoir besoin de nous → probleme de retention

---

## 8. Depenses et headcount — A completer

### Forward Deployed Engineers (FDEs)

**Economie unitaire** :
- Taux journalier de vente : 1 150 EUR/jour
- Base : 210 jours/an

**Hypotheses de dimensionnement** :
- Capacite moyenne par FDE : ~4 use cases/an (avec variabilite forte)
- Ne pas commencer a 2 — plutot 3, 4, voire 6 (beaucoup de cas rapidement resolvables + ateliers a gerer)
- Modele : partir du nombre de use cases (pas du CA) pour dimensionner

**Trajectoire discutee** :
- Fin 2026 : 2 FDEs minimum (+ besoins ateliers)
- 2027 : 3 FDEs
- 2028 : 4-6 FDEs

**Remarque** : la bonne maniere de modeliser n'est PAS "CA → main d'oeuvre" mais "nombre de use cases → capacite FDE necessaire", en acceptant que certains use cases sont resolus en 3 mois et d'autres demandent 3 ans.

**Jean recommande de commencer plus haut** car :
- Beaucoup de cas sont rapidement resolvables
- Les FDEs font aussi les ateliers
- Un project manager peut gerer 4 clients simultanement

### Marketing
- Objectif : doubler la pipeline sales en 2027
- Budget actuel : ~3 000 EUR/mois (36k/an)
- Cible 2027 : tripler → ~100 000 EUR/an minimum
- Fourchette discutee : 70-100k EUR

### Autres couts a inclure
- **Bureaux** : a chiffrer
- **RH/back-office** : anticiper un recrutement admin/facturation d'ici 2028
- **Certification** : couts lies a la trajectoire SecNumCloud (plutot 2028)
- **Partenariat OVH** : a explorer comme chemin vers le modele cible

---

## 9. Trajectoire SecNumCloud et strategie enterprise

### Constat
- Les grandes entreprises sont "paranos de la securite"
- Impossible de faire du token/usage-based tant que le deploiement n'est pas compatible grosses exigences
- SecNumCloud = prerequis pour le modele cible mais extremement difficile a obtenir (~2-3 ans)

### Strategie retenue
- Phase de transition : ne pas forcer l'usage-based, vendre service + abonnement
- Parier sur un jalon precis (date a definir) pour SecNumCloud
- Explorer un partenariat OVH comme "chemin le plus facile"
- Accepter moins de profit court terme si la strategie montre qu'on devient un "proprietaire critique"

### Position sur la gestion des modeles IA
- Inspiration : startup parallele dans la sante (VC-backed, vend a l'usage)
- Question cle : est-ce que le client gere ses propres modeles, ou est-ce qu'on les gere pour lui ?
- **Position retenue** : on gere les modeles et on fait du SaaS — on revend les tokens avec marge, le client ne touche pas a l'infra IA

### Message VC
- On s'installe chez les clients via la transition (service + plateforme)
- On devient indispensable (lock-in ecosystemique)
- Quand SecNumCloud est atteint → bascule vers usage-based avec marges tres superieures
- Le VC doit voir : land-and-expand classique avec une trajectoire claire vers un modele high-margin

---

## 10. Decisions cles et points d'alignement

| Decision | Statut |
|----------|--------|
| Modele de transition = service + fee plateforme | Acte |
| Modele cible = usage-based post-SecNumCloud | Acte (conditionnel) |
| Decomposer ARR total vs ARR plateforme | A faire |
| 3 typologies clients (100M / 1Md / 40-50Md) | Acte |
| 4 use cases types a chiffrer | A faire |
| Commencer FDEs a 3-4-6 (pas 2) | Acte |
| Marketing 2027 : ~100k EUR | Acte |
| Ne pas projeter au-dela de 2028 dans le BP | Acte |
| Explorer partenariat OVH | A investiguer |

---

## 11. Points de divergence / tensions non resolues

- **Jean** penche pour un pricing plus agressif et une trajectoire usage-based affirmee des le pitch VC (meme si pas encore applicable)
- **Matthieu** est plus prudent sur la capacite a vendre cher tant que la credibilite n'est pas etablie et que le modele n'est pas deployable (SecNumCloud)
- Le nombre exact de FDEs en demarrage reste debattu (2 vs 3-4-6)
- La question "combien on gagne par use case" reste difficile a trancher sans donnees terrain supplementaires
- L'equilibre entre "etre realiste pour le BP" et "raconter une story ambitieuse au VC" n'est pas totalement resolu
