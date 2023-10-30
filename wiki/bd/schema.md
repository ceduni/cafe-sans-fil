# 🗃️ Schemas (Base de Données)

Ce document présente la structure de notre BD MongoDB.

## Collections

### User

```json
{
  "user_id": "string (UUID) (Unique)",
  "email": "string (Unique)",
  "matricule": "string (Unique)",
  "username": "string (Unique)",
  "hashed_password": "string (hashed)",
  "first_name": "string",
  "last_name": "string",
  "photo_url": "string (Optional)"
}

```

- **user_id**: Une chaîne unique (UUID) pour identifier chaque utilisateur.
- **email**: L'email de l'utilisateur.
- **matricule**: Matricule de l'étudiant.
- **username**: Nom d'utilisateur choisi par l'étudiant pour se connecter.
- **hashed_password**: Mot de passe de l'utilisateur, qui sera haché avant d'être stocké pour des raisons de sécurité.
- **first_name**: Prénom de l'utilisateur.
- **last_name**: Nom de famille de l'utilisateur.
- **photo_url**: URL pointant vers la photo de profil de l'utilisateur.
  
<br>

### Cafe

```json
{
  "cafe_id": "string (UUID) (Unique)",
  "name": "string",
  "description": "string (Optional)",
  "image_url": "string (Optional)",
  "faculty": "string",
  "location": {
    "pavillon": "string",
    "local": "string"
  },
  "is_open": "bool",
  "opening_hours": [
    {
      "day": "string",
      "blocks": [
        {
          "start": "string (HH:mm format)",
          "end": "string (HH:mm format)" 
        }
      ]
    }
  ],
  "contact": {
    "email": "string (Optional)",
    "phone_number": "string (Optional)",
    "website": "string (Optional)"
  },
  "social_media": [
    {
      "platform_name": "string (Optional)",
      "link": "string (Optional)"
    }
  ],
  "payment_methods": [
    {
      "method": "string",
      "minimum": "double (Optional)"
    }
  ],
  "staff": [
    {
      "user_id": "string (UUID)",
      "role": "string (e.g., 'benevole', 'admin')"
    }
  ],
  "menu_items": [
    {
      "item_id": "string (UUID) (Unique)",
      "name": "string",
      "description": "string (Optional)",
      "image_url": "string (Optional)",
      "price": "double",
      "is_available": "bool",
      "category": "string (Optional)",
      "options": {
        "type": "string (Optional)",
        "value": "string (Optional)",
        "fees": "double (Optional)"
      }
    }
  ],
  "additional_info": [
    {
      "type": "string (Optional)",
      "value": "string (Optional)",
      "start": "date (Optional)",
      "end": "date (Optional)"
    }
  ]
}
```

- **cafe_id**: Un identifiant unique (UUID) pour chaque café.
- **name**: Nom du café.
- **description**: Brève description du café.
- **image_url**: URL d'une image représentative du café.
- **faculty**: Faculté à laquelle le café est associé.
- **location**: L'emplacement précis du café sur le campus.
- **is_open**: Booléen indiquant si le café est actuellement ouvert ou fermé.
- **opening_hours**: Les heures d'ouverture pour chaque jour, présentées sous forme de blocs horaires.
- **contact**: Informations de contact telles que le numéro de téléphone, l'email, le site web.
- **social_media**: Réseaux sociaux associés au café (e.g., Facebook, Instagram).
- **payment_methods**: Les méthodes de paiement acceptées par le café et les montants minimums associés.
- **staff**: Liste des membres du personnel travaillant au café.
- **menu_items**: Liste des éléments disponibles dans le menu du café.
- **options**:
  - **type**: Type d'option pour le produit. Par exemple, "Taille" pour une boisson ou "Garniture" pour un hamburger.
  - **value**: Valeur spécifique ou choix pour cette option. Par exemple, pour la taille: "petit", "moyen", "grand" ou pour une garniture: "fromage", "bacon".
  - **fees**: Coût supplémentaire associé à cette option, le cas échéant.
- **additional_info**:
  - **type**: Catégorie d'information additionnelle. Par exemple, "Annonce" pour des nouvelles ou promotions spécifiques, ou "Autres" pour des informations diverses.
  - **value**: Message ou description associée à cette catégorie d'information.
  - **start**: Date de début, utile si l'information est temporaire ou saisonnière.
  - **end**: Date de fin, indiquant quand cette information ne sera plus pertinente ou valide.
  
<br>

### Order

```json
{
  "order_id": "string (UUID) (Unique)",
  "user_id": "string (UUID)",
  "cafe_id": "string (UUID)",
  "items": [
    {
      "item_id": "string (UUID)",
      "quantity": "int",
      "item_price": "double"
    }
  ],
  "total_price": "double",
  "status": "string (e.g., 'placed', 'ready', 'completed', 'cancelled')",
  "order_timestamp": "date"
}
```

- **order_id**: Un identifiant unique (UUID) pour chaque commande.
- **user_id**: L'identifiant de l'utilisateur qui a passé la commande.
- **cafe_id**: L'identifiant du café où la commande a été passée.
- **items**: Les articles que l'utilisateur a commandés.
- **total_price**: Prix total de la commande.
- **status**: État actuel de la commande (e.g., "placed", "ready", "completed", "cancelled").
- **order_time**: Heure à laquelle la commande a été passée.
- **completion_time**: Heure à laquelle la commande a été complétée.

### 📝 Notes sur les Statuts de Commande

Chaque commande traverse différents statuts qui indiquent sa progression :

- **🔄 placed**: 
  - **Définition** : La commande est enregistrée mais n'est pas encore traitée par le café.
  
- **✅ ready**: 
  - **Définition** : La commande a été traitée et est prête à être récupérée par le client.

- **✔️ completed**: 
  - **Définition** : La commande a été récupérée par le client et est considérée comme terminée.

- **❌ cancelled**: 
  - **Définition** : La commande a été annulée.
  - **Détails** : 
    - Peut se produire automatiquement si la commande n'est pas traitée ou récupérée dans le délai d'une heure.
    - Peut également être annulée manuellement par le client ou le café pour diverses raisons, telles que l'indisponibilité d'un article ou un autre problème opérationnel.


