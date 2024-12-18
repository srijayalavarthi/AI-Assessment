import tkinter as tk
from tkinter import ttk, messagebox
from owlready2 import get_ontology

# Load the ontology
ONTOLOGY_PATH = "periodic_table_ontology.owl"  # Ensure the OWL file exists in the same directory
ontology = get_ontology(ONTOLOGY_PATH).load()

# Explicitly find the Element class
element_class = ontology.search_one(iri="http://test.org/periodic#Element")
if not element_class:
    print("The 'Element' class could not be found in the ontology.")
    exit()


class PeriodicTableTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("Periodic Table Tutor")
        self.root.geometry("1200x700")
        self.create_gui()

    def create_gui(self):
        """Create GUI components for the periodic table."""
        # Title Label
        title_label = tk.Label(self.root, text="Periodic Table Tutor", font=("Helvetica", 24, "bold"), bg="#3c3f41", fg="white")
        title_label.pack(fill=tk.X, pady=10)

        # Search Frame
        search_frame = tk.Frame(self.root, bg="#f7f7f7")
        search_frame.pack(pady=20)
        tk.Label(search_frame, text="Search by Symbol:", font=("Helvetica", 14), bg="#f7f7f7").grid(row=0, column=0, padx=10)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Helvetica", 14), width=10)
        search_entry.grid(row=0, column=1, padx=10)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_element)
        search_button.grid(row=0, column=2, padx=10)

        # Periodic Table Frame
        table_frame = tk.Frame(self.root, bg="#e1e1e1")
        table_frame.pack(pady=20)
        self.create_periodic_table(table_frame)

        # Info Display Frame
        self.info_label = tk.Label(self.root, text="Click on an element to see details.",
                                   font=("Helvetica", 16), wraplength=1000, justify="left", bg="#f7f7f7", relief=tk.GROOVE, bd=2)
        self.info_label.pack(pady=20, fill=tk.BOTH, expand=True)

    def create_periodic_table(self, frame):
        """Create a grid of buttons for the periodic table."""
        elements_layout = [
            ["H", None, None, None, None, None, None, None, None, None, None, None, None, "He"],
            ["Li", "Be", None, None, None, None, None, None, None, None, "B", "C", "N", "O", "F", "Ne"],
            ["Na", "Mg", None, None, None, None, None, None, None, None, "Al", "Si", "P", "S", "Cl", "Ar"],
            ["K", "Ca", None, None, None, None, None, None, None, None, "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"],
            ["Rb", "Sr", None, None, None, None, None, None, None, None, "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd"],
            ["Cs", "Ba", None, None, None, None, None, None, None, None, "La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg"],
            ["Fr", "Ra", None, None, None, None, None, None, None, None, "Ac", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn"],
        ]

        colors = {
            "H": "#f4b942",  # Hydrogen color
            "He": "#b0d4e3",  # Noble gas color
            "Li": "#fdd835",  # Alkali metal color
            "Be": "#cfd8dc",  # Alkaline earth metal color
            "B": "#90caf9",  # Metalloid color
            "C": "#8bc34a",  # Non-metal color
            "N": "#8bc34a",  # Non-metal color
            "O": "#8bc34a",  # Non-metal color
            "F": "#8bc34a",  # Non-metal color
            "Ne": "#b0d4e3",  # Noble gas color
        }

        for r, row in enumerate(elements_layout):
            for c, el in enumerate(row):
                if el:
                    color = colors.get(el, "#cfd8dc")  # Default color
                    button = tk.Button(frame, text=el, width=5, height=2, bg=color, font=("Helvetica", 10, "bold"),
                                       command=lambda symbol=el: self.show_element_details(symbol))
                    button.grid(row=r, column=c, padx=5, pady=5)

    def show_element_details(self, symbol):
        """Display details of the selected element."""
        for element in element_class.instances():
            if hasattr(element, "symbol") and element.symbol and element.symbol[0] == symbol:
                details = (
                    f"Element: {getattr(element, 'name', ['Unknown'])[0]}\n"
                    f"Symbol: {getattr(element, 'symbol', ['Unknown'])[0]}\n"
                    f"Atomic Number: {getattr(element, 'atomicNumber', ['Unknown'])[0]}\n"
                    f"Group: {getattr(element, 'group', ['Unknown'])[0]}\n"
                    f"Reactivity: {getattr(element, 'reactivity', ['Unknown'])[0]}"
                )
                self.info_label.config(text=details)
                return

        messagebox.showerror("Error", f"No data found for element with symbol '{symbol}'.")

    def search_element(self):
        """Search for an element by its symbol."""
        symbol = self.search_var.get().strip()
        if not symbol:
            messagebox.showerror("Error", "Please enter a symbol to search.")
            return
        self.show_element_details(symbol)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PeriodicTableTutor(root)
    root.mainloop()
