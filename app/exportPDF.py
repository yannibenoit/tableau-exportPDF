from connectors.tableau import Tableau

#Import de la classe Tableau
tableau = Tableau('online')

# Nom de la vue à exporter
view = 'Cockpit Fournisseurs'

# Nom du champs utilisé comme filtre
filter_field_name='Code Fournisseur'

# Valeurs associés au filtre
filter_values = ['Fournisseur_035', 'Fournisseur_032', 'Fournisseur_025', 'Fournisseur_089', 'Fournisseur_117']

# Email pour recevoir le fichier
email_to = "yanni-benoit.iyeze@saegus.com"


tableau.exportPDF(view, filter_field_name, filter_values, email_to)
