# Connectors

## Tableau

Pour utiliser cette classe dans un autre script de ce projet

```python
from connectors.tableau import Tableau
```

### Méthodes de connexions APIs

- `connect()` : requete POST pour se connecter à Tableau server.


- `get_views()`: requete GET pour lister toutes les vues disponibles sur le Tableau server.

- `exportPDF(view_name, filter_name, values, email)`: combinaison de requetes pour rechercher la vue demandée puis faire l'export pour chaque valeurs du filtre et regrouper les exports dans un seul fichier qui sera envoyé par mail.

#### Exemple d'utilisation

```python
from connectors.tableau import Tableau

tableau = Tableau('server')

view = 'Cockpit Fournisseurs'
filter_field_name='Code Fournisseur'
email_to = "yanni-benoit.iyeze@saegus.com"
filter_values = ['Fournisseur_035', 'Fournisseur_032', 'Fournisseur_025', 'Fournisseur_089', 'Fournisseur_117']

tableau.exportPDF(view, filter_field_name, filter_values, email_to)
```


### Autres méthodes utilisés par la classe

- `send_email(filename, toaddr)`: méthode utilisée pour envoyer un mail

- `merger(output_path, input_paths)`: méthode permettant de regrouper des fichiers pdf stockés dans un même dossier.
