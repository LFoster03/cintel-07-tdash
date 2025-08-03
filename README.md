# PyShiny Basic Dashboard (Penguins)

## Tools

- Python
- Shiny for Python
- VS Code + Python Extension
- Git
- GitHub

## Try in the Browser

Go to PyShiny Templates at <https://shiny.posit.co/py/templates/>.
Go to Dashboards / Basic Dashboard.

- <https://shiny.posit.co/py/templates/dashboard/>

## Reference App with Detailed Instructions

For more detailed instructions, see <https://github.com/denisecase/pyshiny-penguins-dashboard-express>.
That project README.md has more detailed instructions, including reminders for Mac and Linux. 

## Get the Code

Fork this project into your own GitHub account.
Clone **your** GitHub repo down to your local machine.
IMPORTANT: Use your GitHub **username** in place of denisecase.
[GitHub CLI](https://cli.github.com/) may work better on some machines.

```shell
git clone https://github.com/denisecase/cintel-07-tdash
```

## Run Locally - Initial Start

After cloning your project down to your Documents folder, open the project folder for editing in VS Code.

Create a local project virtual environment named .venv, activate it, and install the requirements.

When VS Code asks to use it for the workspace, select Yes.
If you miss the window, after installing, select from the VS Code menu, View / Command Palette, and type "Python: Select Interpreter" and select the .venv folder.

Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands (for Windows - the activate command is slightly different Linux/Mac).

```shell
py -m venv .venv
.venv\Scripts\Activate
py -m pip install --upgrade pip setuptools
py -m pip install --upgrade -r requirements.txt
```

Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands.

```shell
shiny run --reload --launch-browser app/app.py
```

Open a browser to <http://127.0.0.1:8000/> and test the app.

## Run Locally - Subsequent Starts

Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands.

```shell
.venv\Scripts\Activate
shiny run --reload --launch-browser app/app.py
```

While the app is running, the terminal is fully engaged and cannot be used for other commands. 
To kill the terminal, click the trashcan icon in the VS Code terminal window. 

## After Changes, Export to Docs Folder

Export to docs folder and test GitHub Pages locally.

Open a new terminal (VS Code menu "Terminal" / "New Terminal") in the root project folder and run these commands. 
Remember to activate the environment first. 

```shell
.venv\Scripts\Activate
shiny static-assets remove
shinylive export app docs
py -m http.server --directory docs --bind localhost 8008
```

Open a browser to <http://[::1]:8008/> and test the Pages app.

## Push Changes back to GitHub

Open a terminal (VS Code menu "Terminal" / "New Terminal") in the root project folder and run these commands.

```shell
git add .
git commit -m "Useful commit message"
git push -u origin main
```

## Enable GitHub Pages

Go to your GitHub repo settings and enable GitHub Pages for the docs folder.

## Code Walkthrough

1. Overview
At the top of app.py, you’ll find a header comment summarizing:

What the app does (interactive penguin data dashboard).

What dataset it uses (Palmer Penguins).

Which libraries are required.

2. Data Loading
Explains how the dataset is loaded with palmerpenguins.load_penguins() and stored in a pandas DataFrame for analysis.
3. Page Layout
Comments describe ui.page_opts() for setting the page title and fill behavior.

The sidebar section is fully commented to explain:

The purpose of sliders and checkboxes.

Why links to resources are included for reference.

4. Value Boxes
Each value box (Penguin Count, Average Bill Length, Average Bill Depth) has:

A description of what metric it shows.

In PyShiny Express, you can customize display text in several ways depending on which element you’re talking about:

Page title (ui.page_opts)

Sidebar labels / headers / links

Value box labels and numbers

Card headers and plot labels

Data grid column labels

1. Change the Page Title
You set this here:

python
Copy
Edit
ui.page_opts(title="Penguins dashboard", fillable=True)
To customize it:

python
Copy
Edit
ui.page_opts(title="My Custom Penguin Dashboard", fillable=True)
2. Change Sidebar Text
For the slider label:

python
Copy
Edit
ui.input_slider("mass", "Mass", 2000, 6000, 6000)
Change "Mass" to "Max Body Mass (grams)" or any text you want:

python
Copy
Edit
ui.input_slider("mass", "Max Body Mass (grams)", 2000, 6000, 6000)
For checkbox group label:

python
Copy
Edit
ui.input_checkbox_group(
    "species",
    "Species",  # <-- Change this
    ["Adelie", "Gentoo", "Chinstrap"],
    selected=["Adelie", "Gentoo", "Chinstrap"],
)
3. Change Value Box Labels
These are just strings placed before the @render.text function. Example:

python
Copy
Edit
with ui.value_box(showcase=icon_svg("earlybirds")):
    "Number of penguins"  # <-- This is your label text

    @render.text
    def count():
        return filtered_df().shape[0]
Change "Number of penguins" to whatever you want, e.g., "Penguin Count".

4. Change Card Headers
Example:

python
Copy
Edit
ui.card_header("Bill length and depth")
Change it to:

python
Copy
Edit
ui.card_header("Bill Dimensions (Length vs Depth)")
5. Change Column Names in Data Grid
If you want friendlier column names in the table:

python
Copy
Edit
cols = [
    "species",
    "island",
    "bill_length_mm",
    "bill_depth_mm",
    "body_mass_g",
]
Rename columns with pandas before returning:

python
Copy
Edit
table_df = filtered_df()[cols].rename(columns={
    "species": "Species",
    "island": "Island",
    "bill_length_mm": "Bill Length (mm)",
    "bill_depth_mm": "Bill Depth (mm)",
    "body_mass_g": "Body Mass (g)"
})
return render.DataGrid(table_df, filters=True)
Example with Custom Display Text
python
Copy
Edit
with ui.value_box(showcase=icon_svg("earlybirds")):
    "Penguin Count"

    @render.text
    def count():
        return f"{filtered_df().shape[0]} penguins"

with ui.value_box(showcase=icon_svg("ruler-horizontal")):
    "Avg Bill Length"

    @render.text
    def bill_length():
        return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

# Load dataset
df = palmerpenguins.load_penguins()

# Set page title
ui.page_opts(title="Lindsay Foster's Penguins Dashboard", fillable=True)

# Sidebar controls
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
    ui.a("GitHub Source", href="https://github.com/denisecase/cintel-07-tdash", target="_blank")
    ui.a("GitHub App", href="https://denisecase.github.io/cintel-07-tdash/", target="_blank")
    ui.a("GitHub Issues", href="https://github.com/denisecase/cintel-07-tdash/issues", target="_blank")
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Template: Basic Dashboard", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")
    ui.a("See also", href="https://github.com/denisecase/pyshiny-penguins-dashboard-express", target="_blank")

# Value boxes
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Penguin Count"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Cards
with ui.layout_columns():
    # Scatter plot card
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

    # Data table card with renamed columns
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            # Select columns
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]

            # Rename columns for display
            renamed_df = filtered_df()[cols].rename(columns={
                "species": "Species",
                "island": "Island",
                "bill_length_mm": "Bill Length (mm)",
                "bill_depth_mm": "Bill Depth (mm)",
                "body_mass_g": "Body Mass (g)"
            })

            return render.DataGrid(renamed_df, filters=True)

# Reactive filter
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
What Changed?
Added .rename(columns={...}) before returning the DataGrid to replace:

species → Species

island → Island

bill_length_mm → Bill Length (mm)

bill_depth_mm → Bill Depth (mm)

body_mass_g → Body Mass (g)

This ensures the display headers in your table are user-friendly, but the internal column names remain the same (important for filtering and plotting).


## python -m venv .venv
Code Walkthrough with Comments
The app.py file has been heavily commented to guide new developers learning Shiny for Python. Here’s what the comments explain:

1. Overview
At the top of app.py, you’ll find a header comment summarizing:

What the app does (interactive penguin data dashboard).

What dataset it uses (Palmer Penguins).

Which libraries are required.

2. Data Loading
Explains how the dataset is loaded with palmerpenguins.load_penguins() and stored in a pandas DataFrame for analysis.

3. Page Layout
Comments describe ui.page_opts() for setting the page title and fill behavior.

The sidebar section is fully commented to explain:

The purpose of sliders and checkboxes.

Why links to resources are included for reference.

4. Value Boxes
Each value box (Penguin Count, Average Bill Length, Average Bill Depth) has:

A description of what metric it shows.

A note about how it updates dynamically with user input.

5. Main Content
Comments explain:

How the scatter plot visualizes bill dimensions by species.

How the data table is filtered and column names renamed for clarity.

6. Reactive Programming
Explains the @reactive.calc function:

How it filters data dynamically based on sidebar inputs.

Why Shiny’s reactive model means you don’t manually refresh plots or tables.
7. Why Comments Are Helpful
Designed so someone new to Shiny can quickly:

Understand the UI/server flow.

See where to add or modify components.

Recognize how reactivity works in practice.

### Tips for New Contributors
Read Through Comments First: The comments are meant as a mini-tutorial—follow them top-to-bottom.

Experiment Safely: Try changing labels (e.g., slider or card headers) to see how they update in real-time.

Add Your Own Comments: If you add features (like new charts or filters), document them similarly to keep the project consistent.

Check the Render Functions: Anything decorated with @render will display output in the UI.

## Bonus Modifications
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