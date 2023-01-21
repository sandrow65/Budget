# Application de gestion de budget

Il faut avoir créé l'image et démarré le container pour pouvoir utiliser l'application ! (*build_run.sh* à exécuter)

## Interface de saisie
### Paramétrages à définir soi-même 
- les catégories de transactions, exemple : Logement, Courses, Sorties, ...
- les expéditeurs
- les destinataires
### Ajout des transactions
Différents champs à remplir :
- le type : Débit/Crédit
- la catégorie : sélectionnable selon le paramétrage effectué
- l'expéditeur : sélectionnable selon le paramétrage effectué
- le destinataire : sélectionnable selon le paramétrage effectué
- l'intitulé, exemple: "Loyer Mai 2022", "Repas amis", ...
- le montant

## Interface graphique
- Consulter la liste de toutes les transactions, par mois ou global
- Consulter l'évolution des recettes/dépenses et les économies effectuées par mois
- Voir son top 10 des dépenses

## Sécurité
- Nécessite d'avoir un compte pour rentrer dans l'application / consulter les données
- Seul quelqu'un qui a accès à l'application peut ajouter un nouvel utilisateur

## Base de données 
Deux BDD : 
- Stockage des transactions
- Stockage des utilisateurs
