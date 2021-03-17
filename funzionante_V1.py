import sqlite3 as sql
from os.path import dirname, join

import numpy as np
import pandas.io.sql as psql

from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure
#from bokeh.sampledata.catalog_data import movie_path

# Added
import pandas as pd

catalog = pd.read_csv(join(dirname(__file__), r'lista_manoscritti_Versione_con_aggiunte.csv'))

# conn = sql.connect(movie_path)
# query = open(join(dirname(__file__), 'query.sql')).read()
# catalog = psql.read_sql(query, conn)

catalog["color"] = np.where(catalog["fogli"] > 0, "orange", "grey")

catalog["alpha"] = np.where(catalog["rilegatura"] == 'rilegato', 0.9, 0.25)
# catalog.fillna(0, inplace=True)  # just replace missing values with zero
catalog.fillna(0, inplace=True)
# catalog["revenue"] = catalog.BoxOffice.apply(lambda x: '{:,d}'.format(int(x)))

# with open(join(dirname(__file__), "razzies-clean.csv")) as f:
#     razzies = f.read().splitlines()
# catalog.loc[catalog.imdbID.isin(razzies), "color"] = "purple"
# catalog.loc[catalog.imdbID.isin(razzies), "alpha"] = 0.9

axis_map = {
    "Ampiezza (mm)": "ampiezza",
    "Altezza (mm)": "altezza",
    "Anno (massimo)": "datazione_f",

}

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

# Create Input controls
#reviews = Slider(title="Minimum number of reviews", value=80, start=10, end=300, step=10)
min_year = Slider(title="Inizio del periodo in esame", start=100, end=2000, value=300, step=1)
max_year = Slider(title="Fine del periodo in esame", start=100, end=2000, value=1500, step=1)
#oscars = Slider(title="Minimum number of Oscar wins", start=0, end=4, value=0, step=1)
#boxoffice = Slider(title="Dollars at Box Office (millions)", start=0, end=800, value=0, step=1)
#genre = Select(title="Genre", value="All",
#               options=open(join(dirname(__file__), 'genres.txt')).read().split())
parola_titolo = TextInput(title="Titolo contenente la seguente parola:")
#cast = TextInput(title="Cast names contains")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Ampiezza (mm)")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Altezza (mm)")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[], titolo=[], year=[], numero_del_codice=[],fogli=[],alpha=[]))

TOOLTIPS=[
    ("Segnatura", "@numero_del_codice"),
    ("Titolo", "@titolo"),
]

p = figure(plot_height=400, plot_width=400, title="", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="scale_both")
p.circle(x="x", y="y", source=source, size=7, color="color", line_color=None, fill_alpha="alpha")


def select_catalog():
    #genre_val = genre.value
    parola_titolo_val = parola_titolo.value.strip()
    #cast_val = cast.value.strip()
    selected = catalog[
        #(catalog.Reviews >= reviews.value) &
        #(catalog.BoxOffice >= (boxoffice.value * 1e6)) &
        ((catalog.datazione_f >= min_year.value) & (catalog.datazione_f <= max_year.value)) |
        ((catalog.datazione_i >= min_year.value) & (catalog.datazione_i <= max_year.value)) #&
        #(catalog.Oscars >= oscars.value)
    ]
    # if (genre_val != "All"):
    #     selected = selected[selected.Genre.str.contains(genre_val)==True]
    if (parola_titolo_val != ""):
        selected = selected[selected.titolo.str.contains(parola_titolo_val)==True]
    # if (cast_val != ""):
    #     selected = selected[selected.Cast.str.contains(cast_val)==True]
    return selected


def update():
    df = select_catalog()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d beni selezionati" % len(df)
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        titolo=df["titolo"],
        numero_del_codice = df["numero_del_codice"],
        year=df["datazione_f"],
        #revenue=df["revenue"],
        alpha=df["alpha"],
    )

# controls = [reviews, boxoffice, genre, min_year, max_year, oscars, director, cast, x_axis, y_axis]
controls = [min_year, max_year, x_axis, y_axis,parola_titolo]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320, height=600)
inputs.sizing_mode = "fixed"
l = layout([
    [desc],
    [inputs, p],
], sizing_mode="scale_both")

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "catalog"
import sqlite3 as sql
from os.path import dirname, join

import numpy as np
import pandas.io.sql as psql

from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure
#from bokeh.sampledata.catalog_data import movie_path

# Added
import pandas as pd

catalog = pd.read_csv(join(dirname(__file__), r'lista_manoscritti_Versione_con_aggiunte.csv'))

# conn = sql.connect(movie_path)
# query = open(join(dirname(__file__), 'query.sql')).read()
# catalog = psql.read_sql(query, conn)

#catalog["color"] = np.where(catalog["fogli"] > 0, "orange", "grey")
# coloro i codici a seconda del materiale
# QUESTE FUNZIONI POTREBBERO ESSERE FATTE PER CREARE UN NUOVO DATASET SENZA RICALCOLARLE
def color_material (row):
   if row['materiale'] == 'cartaceo':
        return 'orange'
   if row['materiale'] == 'membranaceo':
        return 'blue'
   if row['materiale'] == 'membranaceo':
       return 'yellow'   
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

catalog["marker_dim"] = 4 + catalog.fogli/catalog.fogli.max()*5

catalog["alpha"] = np.where(catalog["rilegatura"] == 'rilegato', 0.5, 0.15)
# catalog.fillna(0, inplace=True)  # just replace missing values with zero
catalog.fillna(0, inplace=True)
# catalog["revenue"] = catalog.BoxOffice.apply(lambda x: '{:,d}'.format(int(x)))

# with open(join(dirname(__file__), "razzies-clean.csv")) as f:
#     razzies = f.read().splitlines()
# catalog.loc[catalog.imdbID.isin(razzies), "color"] = "purple"
# catalog.loc[catalog.imdbID.isin(razzies), "alpha"] = 0.9

axis_map = {
    "Ampiezza (mm)": "ampiezza",
    "Altezza (mm)": "altezza",
    "Anno (massimo)": "datazione_f",

}

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

# Create Input controls
#reviews = Slider(title="Minimum number of reviews", value=80, start=10, end=300, step=10)
min_year = Slider(title="Inizio del periodo in esame", start=100, end=2000, value=300, step=1)
max_year = Slider(title="Fine del periodo in esame", start=100, end=2000, value=1500, step=1)
#oscars = Slider(title="Minimum number of Oscar wins", start=0, end=4, value=0, step=1)
#boxoffice = Slider(title="Dollars at Box Office (millions)", start=0, end=800, value=0, step=1)
#genre = Select(title="Genre", value="All",
#               options=open(join(dirname(__file__), 'genres.txt')).read().split())
parola_titolo = TextInput(title="Titolo contenente la seguente parola:")
#cast = TextInput(title="Cast names contains")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Ampiezza (mm)")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Altezza (mm)")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[],color_rileg=[],
                                    titolo=[], year=[], numero_del_codice=[],
                                    fogli=[],alpha=[],marker_dim = []))

TOOLTIPS=[
    ("Segnatura", "@numero_del_codice"),
    ("Titolo", "@titolo"),
]

p = figure(plot_height=400, plot_width=400, title="", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="scale_both")
p.circle(x="x", y="y", source=source, size="marker_dim", color="color", line_color="color_rileg", fill_alpha="alpha")


def select_catalog():
    #genre_val = genre.value
    parola_titolo_val = parola_titolo.value.strip()
    #cast_val = cast.value.strip()
    selected = catalog[
        #(catalog.Reviews >= reviews.value) &
        #(catalog.BoxOffice >= (boxoffice.value * 1e6)) &
        ((catalog.datazione_f >= min_year.value) & (catalog.datazione_f <= max_year.value)) |
        ((catalog.datazione_i >= min_year.value) & (catalog.datazione_i <= max_year.value)) #&
        #(catalog.Oscars >= oscars.value)
    ]
    # if (genre_val != "All"):
    #     selected = selected[selected.Genre.str.contains(genre_val)==True]
    if (parola_titolo_val != ""):
        selected = selected[selected.titolo.str.contains(parola_titolo_val)==True]
    # if (cast_val != ""):
    #     selected = selected[selected.Cast.str.contains(cast_val)==True]
    return selected


def update():
    df = select_catalog()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d beni selezionati" % len(df)
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        color_rileg = df["color_rileg"],
        titolo=df["titolo"],
        numero_del_codice = df["numero_del_codice"],
        year=df["datazione_f"],
        marker_dim = df["marker_dim"],
        #revenue=df["revenue"],
        alpha=df["alpha"],
    )

# controls = [reviews, boxoffice, genre, min_year, max_year, oscars, director, cast, x_axis, y_axis]
controls = [min_year, max_year, x_axis, y_axis,parola_titolo]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320, height=600)
inputs.sizing_mode = "fixed"
l = layout([
    [desc],
    [inputs, p],
], sizing_mode="scale_both")

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "catalog"
