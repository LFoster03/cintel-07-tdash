# --------------------------------------------
# Penguins Dashboard - Shiny for Python
# Author: Lindsay Foster
# Purpose: Interactive dashboard to explore Palmer Penguins dataset
# --------------------------------------------

import seaborn as sns               # For plotting (scatter plot)
from faicons import icon_svg        # For using Font Awesome icons in value boxes

from shiny import reactive          # For reactive programming (auto-updates UI)
from shiny.express import input, render, ui   # Shiny Express: simpler syntax for UI + server
import palmerpenguins                # Dataset of penguin measurements

# --------------------------------------------
# 1. Load Data
# --------------------------------------------
# Load the Palmer Penguins dataset into a pandas DataFrame.
df = palmerpenguins.load_penguins()

# --------------------------------------------
# 2. Set Page Options
# --------------------------------------------
# Favicon note:
# Place favicon.ico in the *same folder as index.html* (e.g., docs/ after export)
# Shinylive will auto-detect it; no path required.
ui.page_opts(
    title="Lindsay Foster's Penguins Dashboard",
    fillable=True, favicon="C:\Projects\cintel-07-tdash\docs\favicon.png"
)

# --------------------------------------------
# 3. Sidebar - Filters and Links
# --------------------------------------------
with ui.sidebar(title="Filter controls"):

    ui.input_slider("mass", "Mass", 2000, 6000, 6000)

    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    ui.hr()
    ui.h6("Links")
    ui.a("GitHub Source", href="https://github.com/LFoster03/cintel-07-tdash", target="_blank")
    ui.a("GitHub App", href="https://lfoster03.github.io/cintel-07-tdash/", target="_blank")
    ui.a("GitHub Issues", href="https://github.com/LFoster03/cintel-07-tdash/issues", target="_blank")
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Template: Basic Dashboard", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")
    ui.a("See also", href="https://github.com/denisecase/pyshiny-penguins-dashboard-express", target="_blank")

# --------------------------------------------
# 4. Value Boxes - High-level Metrics
# --------------------------------------------
with ui.layout_column_wrap(fill=False):

    # Penguin count (custom color & icon)
    with ui.value_box(showcase=icon_svg("feather-pointed"), theme='bg-cyan'):
        "Penguin Count"

        @render.text
        def count():
            return filtered_df().shape[0]

    # Average bill length (custom color)
    with ui.value_box(showcase=icon_svg("ruler-horizontal"), theme="bg-green"):
        "Average Bill Length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Average bill depth (custom color)
    with ui.value_box(showcase=icon_svg("ruler-vertical"), theme="bg-indigo"):
        "Average Bill Depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# --------------------------------------------
# 5. Main Content - Plots and Data Table
# --------------------------------------------
with ui.layout_columns():

    # Scatter Plot Card
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Data Table Card
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = ["species", "island", "bill_length_mm", "bill_depth_mm", "body_mass_g"]

            renamed_df = filtered_df()[cols].rename(columns={
                "species": "Species",
                "island": "Island",
                "bill_length_mm": "Bill Length (mm)",
                "bill_depth_mm": "Bill Depth (mm)",
                "body_mass_g": "Body Mass (g)"
            })

            return render.DataGrid(renamed_df, filters=True)

# --------------------------------------------
# 6. Reactive Filter
# --------------------------------------------
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
