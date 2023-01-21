# Application de gestion de budget

## Pré-requis 
### Fichier de configuration

Créer le fichier de configuration dans le dossier *app*
``` config.py
####### config.py #######


HOST = 'db'
USER = 'USER_NAME'
PASSWORD = 'PASSWORD'
DATABASE = 'BUDGET'

SECRET_KEY = 'XXXX'
```

### Commandes Docker 
- Contruire l'image docker : ```docker compose build``` (seulement la première fois ou en cas de changement dans les fichiers python)
- Créer le container : ```docker compose up``` (ajouter ```-d``` à la fin pour ne pas voir les logs)
- Stopper le container : ```docker compose down```

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

## Base de données 
### Une BDD : *BUDGET* 
### Les tables (cf [db/db_creation.sql](https://github.com/sandrow65/Budget/blob/main/db/db_creation.sql)):

- **USER** : liste les utilisateurs ayant créé un compte
- **PROJECT** : liste tous les projets créés
- **PROJECT_DATA** : liste toutes les transactions reliées à un projet
- **TRANSACTION_TYPES** : paramétrable par l'utilisateur dans le bloc "Gérer")
- **TRANSACTION_CLASSES** : paramétrable par l'utilisateur dans le bloc "Gérer")
- **TRANSACTION_SENDER** : paramétrable par l'utilisateur dans le bloc "Gérer")
- **TRANSACTION_RECIPIENT** : paramétrable par l'utilisateur dans le bloc "Gérer")

