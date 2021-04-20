import pandas as pd
import numpy as np
from os.path import join,dirname

catalog = pd.read_csv(join(dirname(__file__), r'lista manoscritti - Versione_con_aggiunte.csv'))

# conn = sql.connect(movie_path)
# query = open(join(dirname(__file__), 'query.sql')).read()
# catalog = psql.read_sql(query, conn)

#catalog["color"] = np.where(catalog["fogli"] > 0, "orange", "grey")
# coloro i codici a seconda del materiale
def color_material (row):
   if row['materiale'] == 'cartaceo':
        return 'orange'
   if row['materiale'] == 'membranaceo':
        return 'blue'
   if row['materiale'] == 'bombacino':
       return 'violet'   
   else:
        return 'gray'
catalog["color"] = catalog.apply (lambda row: color_material(row), axis=1)

def color_binding(row):
   if row['rilegatura'] == 'rilegato':
        return '#2B9332'
   if row['rilegatura'] == 'fascicoli':
        return '#800000'
   if row['rilegatura'] == 'fogli sciolti':
       return '#FF5733'   
   else:
        return '#888483'

catalog["color_rileg"] = catalog.apply (lambda row: color_binding(row), axis=1)
#catalog = catalog.replace({'preferred_manifest_url': {0:"/"}})
#catalog = catalog.replace({'preferred_manifest_url': {0:"/"}})
catalog.preferred_manifest_url.replace([0],"/",inplace=True)

def is_digitized(row):
   if row['preferred_manifest_url'] == "/":
        return 'Non digitalizzato'
   else:
        return '✓'

catalog["is_digitized"] = catalog.apply (lambda row: is_digitized(row), axis=1)

mdim = np.log(1 + (catalog.fogli/catalog.fogli.max())*1000)
mdim[mdim == 0] = 4
catalog["marker_dim"] = mdim

catalog["alpha"] = np.where(catalog["rilegatura"] == 'rilegato', 0.5, 0.15)
# catalog.fillna(0, inplace=True)  # just replace missing values with zero
catalog.fillna(0, inplace=True)
catalog.drop(["palinsesto","testo_indistinto","danni_fuoco","cancro_pergamena","margini_danneggiati","danni_umidita","restaurato","anno_restauro","dorature","disegni","miniato","colori","rosso","blue"], axis=1,inplace=True)
catalog.to_csv("catalogprocessdata.csv")




