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
# This dataset includes species, island, bill dimensions, and body mass.
df = palmerpenguins.load_penguins()

# --------------------------------------------
# 2. Set Page Options
# --------------------------------------------
# The page title will appear in the browser tab and top of the dashboard.
ui.page_opts(title="Lindsay Foster's Penguins Dashboard", fillable=True, favicon="favicon-32x32.png")

# --------------------------------------------
# 3. Sidebar - Filters and Links
# --------------------------------------------
# The sidebar contains filter controls (slider + checkbox) and helpful links.
# Filters will dynamically update the dashboard when changed.

with ui.sidebar(title="Filter controls"):

    # Slider to filter penguins by maximum body mass
    # Range is from 2000g to 6000g, defaulting to 6000g
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)

    # Checkbox group to select which species to include
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    # Horizontal line and helpful resource links
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
# Value boxes display key metrics: count of penguins, avg bill length, avg bill depth.
# They update automatically when filters change.

with ui.layout_column_wrap(fill=False):

    # Total count of filtered penguins (custom color and new icon)
    with ui.value_box(showcase=icon_svg("feather-pointed"), theme='bg-cyan'):
        "Penguin Count"

        @render.text
        def count():
            return filtered_df().shape[0]  # Count number of rows in filtered data

    # Average bill length of filtered penguins (custom color)
    with ui.value_box(showcase=icon_svg("ruler-horizontal"), theme="bg-green"):
        "Average Bill Length"

        @render.text
        def bill_length():
            # Format to 1 decimal place and add "mm"
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Average bill depth of filtered penguins (custom color)
    with ui.value_box(showcase=icon_svg("ruler-vertical"), theme="bg-indigo"):
        "Average Bill Depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# --------------------------------------------
# 5. Main Content - Plots and Data Table
# --------------------------------------------
# Layout with two side-by-side cards: a scatter plot and a data table.

with ui.layout_columns():

    # ---- Scatter Plot Card ----
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Depth")

        @render.plot
        def length_depth():
            # Scatter plot colored by species
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # ---- Data Table Card ----
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            # Select only relevant columns
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]

            # Rename columns to be more readable for users
            renamed_df = filtered_df()[cols].rename(columns={
                "species": "Species",
                "island": "Island",
                "bill_length_mm": "Bill Length (mm)",
                "bill_depth_mm": "Bill Depth (mm)",
                "body_mass_g": "Body Mass (g)"
            })

            # Display DataGrid with filter controls enabled
            return render.DataGrid(renamed_df, filters=True)

# --------------------------------------------
# 6. Reactive Filter
# --------------------------------------------
# The reactive function automatically recalculates when inputs change.
# It filters penguins by selected species and max body mass.

@reactive.calc
def filtered_df():
    # Filter by species checkbox
    filt_df = df[df["species"].isin(input.species())]

    # Filter by mass slider
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]

    return filt_df
