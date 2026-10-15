# Scénario : ShopNova, une marketplace qui perd ses paniers

## Contexte
**ShopNova** est une marketplace en ligne de type Amazon. Elle vend **20 500 produits** répartis en 9 catégories (Electronics, Home & Kitchen, Sports & Outdoors…), entre 6 $ et 900 $.

La direction a constaté trois problèmes :
- **Le tunnel de conversion fuit.** Sur 120 000 interactions, on compte 53 800 pages vues, 12 000 ajouts au panier et seulement **6 144 achats**.
- **Les paniers sont abandonnés.** Seules **15 % des sessions** se terminent par un achat spontané.
- **Les remises sont distribuées à l'aveugle.** L'équipe marketing envoie des codes promo sans savoir à qui ils servent vraiment.

## Problématique
> **Comment ShopNova peut-il augmenter son taux de conversion et son panier moyen en personnalisant l'expérience client (recommandations, ventes croisées, parcours) et en ciblant ses remises uniquement sur les clients qui en ont besoin ?**

## Questions de travail

### Axe 0 : Comprendre le catalogue (`catalog.csv`)
1. Comment les produits se répartissent-ils entre catégories et entre gammes de prix ?
2. Existe-t-il un lien entre le prix, la note (`stars_given`) et le nombre d'avis ?
3. Quelles catégories ont les produits les mieux et les moins bien notés ?
4. Y a-t-il des produits « invisibles », c'est-à-dire présents au catalogue mais jamais consultés ?

### Axe 1 : Recommandation personnalisée (`interactions.csv`)
5. À quelle étape du tunnel (vue → clic → panier → achat) perd-on le plus de clients, et cela varie-t-il selon la catégorie ?
6. Quels produits ont le meilleur taux de transformation, de la vue à l'achat ?
7. Les clients restent-ils dans une seule catégorie ou en explorent-ils plusieurs ?
8. **Peut-on recommander à chaque client 10 produits qu'il est susceptible d'acheter ?** Pour l'évaluer : Precision@10 et Recall@10.
9. Comment traiter les nouveaux clients qui n'ont encore aucun historique (le problème du « démarrage à froid ») ?

### Axe 2 : Ventes croisées (`baskets.csv`)
10. Combien d'articles contient une commande, et pour quelle valeur moyenne ?
11. Quels produits ou quelles catégories sont souvent achetés ensemble ? On peut mesurer ces associations avec les règles d'association (support, confiance, lift).
12. Quelles règles permettraient de proposer un « Fréquemment achetés ensemble » sur la fiche produit ?
13. Les associations entre catégories (par exemple Office → Electronics) sont-elles plus fortes que celles entre produits ?

### Axe 3 : Parcours de navigation (`sessions.csv`)
14. Combien de temps dure une session, combien d'étapes compte-t-elle, et jusqu'où les clients font-ils défiler les pages ?
15. Le temps passé sur une page et la profondeur de défilement révèlent-ils l'intérêt du client ?
16. Les clients restent-ils dans une même catégorie au fil d'une session ?
17. **Peut-on prédire le prochain produit consulté à partir des précédents ?** Pour l'évaluer : HitRate@k.

### Axe 4 : Abandon et ciblage des remises (`abandonment_features.csv`)
18. Quels profils convertissent le plus ? On peut comparer selon le niveau de compte (Prime ou Guest), l'appareil, la source de trafic, la région, l'heure et le week-end.
19. Quels comportements annoncent un abandon (frais de port affichés, retrait d'articles du panier, intention de sortie, avis lus…) ?
20. **Peut-on prédire si une session va convertir sans aide ?** Les deux cibles possibles sont `did_convert_organically` et `should_receive_discount`.
21. Comment gérer le déséquilibre des classes (environ 15 % de cas positifs) ? On peut évaluer avec la PR-AUC plutôt que l'accuracy.
22. **À qui envoyer une remise ?** Il s'agit d'éviter d'en offrir aux clients qui auraient acheté de toute façon (293 sessions ont converti seules alors qu'elles étaient ciblées pour une remise).
23. Combien d'argent récupérerait-on (valeur des paniers sauvés) par rapport au coût des remises ?

### Question de synthèse
24. Si ShopNova ne pouvait financer qu'**un seul** de ces chantiers ce trimestre, lequel aurait le plus d'impact, et pourquoi ?

## Contraintes à garder en tête
- Les données sont **synthétiques**. Les descriptions produits suivent des modèles, donc l'analyse de texte apportera peu.
- On ne peut pas relier `sessions.csv` (identifiants `SESSION_`) à `abandonment_features.csv` (identifiants `SESS_`). Les axes 3 et 4 restent donc indépendants.

Chaque axe correspond à un notebook : de `notebooks/00_eda_catalog.ipynb` à `notebooks/04_abandonment_propensity.ipynb`.
