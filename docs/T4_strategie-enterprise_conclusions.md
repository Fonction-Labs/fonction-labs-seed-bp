# T4 — Stratégie enterprise & infra : Conclusions et décisions

**Statut** : DONE (brainstorm + décisions actées)
**Date** : 25 juin 2026
**Ref** : [T1.2_modeles-intermediaire-vs-cible_conclusions.md](./T1.2_modeles-intermediaire-vs-cible_conclusions.md), [T2_synthese-complete_conclusions.md](./T2_synthese-complete_conclusions.md)

---

## Contexte

Le déblocage des TGC (~40-50Md CA) est conditionné à la souveraineté des données. C'est le verrou principal vers le modèle cible usage-based pour ce segment. La stratégie est de passer par un partenariat infrastructure plutôt que par une certification produit propre — plus rapide, moins coûteux, réaliste d'ici 2028.

---

## T4.1 — Trajectoire SecNumCloud

### Deux approches possibles

**Approche A — Certification produit propre (abandonnée)**
- Qualifier la plateforme Fonction Labs directement SecNumCloud
- Coût : 100-300k+ en audit et mise en conformité
- Délai : 2-3 ans minimum depuis aujourd'hui
- **Verdict : hors scope BP 2026-2028. Non modélisé.**

**Approche B — Hébergement sur infrastructure qualifiée (retenue)**
- Déployer la plateforme sur OVH Trusted Cloud / S3NS (JV OVH × Thales, qualifiée SecNumCloud)
- On peut contractuellement dire : "hébergé sur infrastructure qualifiée SecNumCloud"
- Coût : partenariat commercial OVH + coûts d'hébergement (dans l'infra cloud déjà budgétée)
- Délai : **Q1 2027 réaliste** avec les contacts existants

**Pourquoi pas AWS pour les TGC :**
AWS n'est pas qualifié SecNumCloud — disqualification contractuelle pour les TGC français (Défense, banques systémiques, énergie, administrations). AWS reste pertinent pour les GC (ISO 27001 + hébergement EU suffit).

---

## T4.2 — Partenariat OVH

### Contacts et levier

Contact OVH existant, bien placé. Les deux dimensions sont à explorer :
- **Technique** : hébergement sur OVH Trusted Cloud / S3NS
- **Commercial** : partenariat de distribution (OVH resélle ou co-présente l'offre)

### Formes possibles du partenariat

| Forme | Description | Délai | Pertinence BP |
|-------|-------------|-------|---------------|
| Hébergement qualifié | On déploie sur OVH S3NS — infrastructure SecNumCloud | 3-6 mois | ✓ **Priorité** |
| Partenariat commercial | OVH référence Fonction Labs dans son écosystème | 6-12 mois | ✓ Upside |
| Co-développement | Offre AI agents souveraine co-construite | 12-24 mois | Non — hors scope 2028 |

**Priorité : formaliser l'hébergement qualifié d'abord.** Le partenariat commercial suit naturellement.

### AWS — rôle dans la stratégie

AWS (et Azure) restent pertinents pour :
- Les GC qui n'exigent pas SecNumCloud (ISO 27001 + RGPD suffit)
- Les ETI (aucune contrainte d'hébergement particulière)

**Dans le BP :** on mentionne AWS/Azure comme options pour les segments ETI et GC, OVH comme chemin souveraineté pour les TGC.

---

## Jalons actés

```
Juil-Sept 2026  : activation contacts OVH (technique + commercial)
                  + lancement ISO 27001 si pas déjà commencé

Oct-Déc 2026    : POC technique hébergement OVH Trusted Cloud / S3NS

Q1 2027         : partenariat OVH formalisé (accord commercial + technique)
                  → JALON BP : "infrastructure qualifiée SecNumCloud disponible"
                  → déblocage prospection TGC

Q2-Q3 2027      : premier déploiement client sur infra OVH
                  ISO 27001 obtenu (si lancé juil 2026)

Q4 2027         : pipeline TGC activée (cycle de vente 6-18 mois → 
                  commencer à prospecter maintenant pour closer en 2028)

H1 2028         : 1-2 TGC clients signés — aligné avec T2.3
```

**Jalon BP clé à retenir pour le pitch VC :**
> **Q1 2027 : partenariat OVH signé → infrastructure qualifiée SecNumCloud disponible → déblocage TGC**

---

## Conformité par segment — récapitulatif complet

| Segment | Exigence | Solution | Jalon |
|---------|----------|----------|-------|
| ETI (~100M CA) | RGPD + DPA | Hébergement EU standard (AWS/OVH) | Dès maintenant |
| Grand compte (~1Md CA) | ISO 27001 + DPA | ISO 27001 en cours + hébergement EU | Q2-Q3 2027 |
| TGC (~40-50Md CA) | SecNumCloud ou équivalent | OVH S3NS (infrastructure qualifiée) | Q1 2027 |

---

## Impact sur le modèle économique

Le partenariat OVH débloque la bascule vers le modèle cible usage-based pour les TGC :
- Avant OVH formalisé : TGC sur modèle intermédiaire (abonnement + FDE), facturation tokens impossible
- Après OVH formalisé (Q1 2027) : TGC peuvent basculer sur credits/usage-based dès leur renouvellement

**Coût additionnel hébergement OVH :** inclus dans la sous-ligne "infra cloud plateforme" déjà budgétée en T3.4. OVH S3NS est premium vs AWS standard (~20-30% plus cher), mais marginal à l'échelle du revenu TGC (forfaits 200-350k/an).

---

## Décisions actées

| # | Décision |
|---|----------|
| 1 | Approche SecNumCloud retenue : hébergement sur OVH S3NS, pas certification produit propre |
| 2 | AWS/Azure : options pour ETI et GC — pas pour TGC (non qualifié SecNumCloud) |
| 3 | Contact OVH existant (bien placé) — à activer juil-sept 2026 sur les deux dimensions |
| 4 | Priorité partenariat OVH : hébergement qualifié d'abord, commercial ensuite |
| 5 | Jalon BP : Q1 2027 partenariat OVH formalisé → déblocage TGC |
| 6 | ISO 27001 : à lancer immédiatement (Q3 2026) pour déblocage GC en Q2-Q3 2027 |
| 7 | Prospection TGC à démarrer dès Q1 2027 (cycle 6-18 mois → closes H1 2028) |
| 8 | Coût hébergement OVH S3NS : inclus dans budget infra cloud T3.4 (pas de ligne dédiée) |
| 9 | Co-développement OVH : hors scope BP 2026-2028 |
