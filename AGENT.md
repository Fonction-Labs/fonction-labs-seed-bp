# AGENT.md — Règles de la pipeline BP

## Règle fondamentale : zéro hardcode

Toute valeur produite par la pipeline provient soit d'une **hypothèse explicitement nommée** (paramètre dans `vc_case.yaml`), soit d'une **formule dérivée** de ces hypothèses.

Aucune valeur n'est hardcodée dans les outputs.

**Pourquoi :** cela permet de faire des itérations sur les hypothèses sans tout recalculer manuellement. Changer un paramètre YAML doit propager automatiquement dans tous les outputs.

---

## Exemples de formules (pas de hardcode)

```
# Headcount FDE
nb_fde = (uc_en_deploiement × 1.0) + (uc_en_ac × 0.25)

# Capacité FDE
uc_en_deploiement = uc dont le start_month est dans les deployment_duration_months précédents
uc_en_ac          = uc_total - uc_en_deploiement

# Revenue FDE service
revenue_fde_service = nb_fde × fde_billable_day_rate × jours_facturables_par_mois

# COGS
cogs = (nb_fde_actifs × fde_monthly_loaded_cost)
     + token_costs_clients
     + infra_client_facing

# Gross margin
gross_margin_pct = (revenue - cogs) / revenue
```

---

## Paramètres maîtres (source de vérité)

Tous les paramètres maîtres sont dans `data/assumptions/vc_case.yaml`.

Les docs markdown dans `docs/` sont des **notes de décision** — ils expliquent le raisonnement et les hypothèses, mais ne sont pas la source de vérité des chiffres.

---

## Ce qui est autorisé

- Hypothèse nommée dans le YAML avec commentaire explicitant la source ou la logique
- Formule dérivée d'hypothèses YAML, documentée dans le code ou dans les docs
- Ordre de grandeur estimatif dans les docs markdown, **explicitement flagué** comme estimation (ex : "~57% estimé", "hypothèse BP")

## Ce qui est interdit

- Chiffre hardcodé dans un output sans référence à une hypothèse ou formule
- Chiffre copié d'un doc markdown vers un autre sans tracer la source
- Annualiser un one-shot (ateliers, déploiements) dans l'ARR
