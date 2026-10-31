import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog, simpledialog
from services.pdf_service import PDFService
from services.image_service import ImageService

# ---------- THEME ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0B1120"
SIDEBAR = "#101A30"
CARD = "#141F36"
BORDER = "#263653"
TEXT = "#F1F5F9"
MUTED = "#9CAFCB"
BLUE = "#3B82F6"
PURPLE = "#8B5CF6"

app = ctk.CTk()
app.title("PyPDF Studio")
app.geometry("1150x760")
app.minsize(900, 620)
app.configure(fg_color=BG)

# ---------- TOOL ACTION ----------
# ---------- PDF SERVICES ----------
pdf_service = PDFService()
image_service = ImageService()


def open_tool(tool):
    try:
        if tool == "Merge PDFs":
            files = filedialog.askopenfilenames(
                filetypes=[("PDF Files", "*.pdf")]
            )
            if not files:
                return

            output = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )
            if output:
                pdf_service.merge_pdfs(files, output)
                messagebox.showinfo("Success", "PDFs merged!")

        elif tool == "Split PDF":
            file = filedialog.askopenfilename(
                filetypes=[("PDF Files", "*.pdf")]
            )
            if not file:
                return

            start = simpledialog.askinteger(
                "Start Page", "Enter start page:", minvalue=1
            )
            if start is None:
                return

            end = simpledialog.askinteger(
                "End Page", "Enter end page:", minvalue=start
            )
            if end is None:
                return

            output = filedialog.asksaveasfilename(
                defaultextension=".pdf"
            )
            if output:
                pdf_service.split_pdf(file, start, end, output)
                messagebox.showinfo("Success", "PDF split!")

        elif tool == "Rotate Pages":
            file = filedialog.askopenfilename(
                filetypes=[("PDF Files", "*.pdf")]
            )
            if not file:
                return

            page = simpledialog.askinteger(
                "Page Number", "Enter page number:", minvalue=1
            )
            if page is None:
                return

            angle = simpledialog.askinteger(
                "Rotation", "Enter 90, 180, or 270:"
            )
            if angle not in (90, 180, 270):
                messagebox.showerror(
                    "Invalid Angle", "Use 90, 180, or 270."
                )
                return

            output = filedialog.asksaveasfilename(
                defaultextension=".pdf"
            )
            if output:
                pdf_service.rotate_page(file, page, angle, output)
                messagebox.showinfo("Success", "Page rotated!")

        elif tool == "Delete Pages":
            file = filedialog.askopenfilename(
                filetypes=[("PDF Files", "*.pdf")]
            )
            if not file:
                return

            pages = simpledialog.askstring(
                "Delete Pages", "Enter page numbers, e.g. 2,4,6:"
            )
            if not pages:
                return

            page_list = [int(p.strip()) for p in pages.split(",")]
            if any(p < 1 for p in page_list):
                raise ValueError("Page numbers must be positive.")

            output = filedialog.asksaveasfilename(
                defaultextension=".pdf"
            )
            if output:
                pdf_service.delete_pages(file, page_list, output)
                messagebox.showinfo("Success", "Pages deleted!")

        elif tool == "Images to PDF":
            files = filedialog.askopenfilenames(
                filetypes=[("Images", "*.png *.jpg *.jpeg")]
            )
            if not files:
                return

            output = filedialog.asksaveasfilename(
                defaultextension=".pdf"
            )
            if output:
                image_service.image_to_pdf(files, output)
                messagebox.showinfo("Success", "PDF created!")

        elif tool == "PDF to Images":
            file = filedialog.askopenfilename(
                filetypes=[("PDF Files", "*.pdf")]
            )
            if not file:
                return

            folder = filedialog.askdirectory()
            if folder:
                image_service.pdf_to_images(file, folder)
                messagebox.showinfo("Success", "Images saved!")

        elif tool == "Extract Text":
            file = filedialog.askopenfilename(
                filetypes=[("PDF Files", "*.pdf")]
            )
            if not file:
                return

            text = pdf_service.extract_text(file)

            window = ctk.CTkToplevel(app)
            window.title("Extracted Text")
            window.geometry("700x500")

            textbox = ctk.CTkTextbox(window, wrap="word")
            textbox.pack(fill="both", expand=True, padx=12, pady=12)
            textbox.insert("1.0", text or "No text found.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- MAIN LAYOUT ----------
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# ---------- SIDEBAR ----------
sidebar = ctk.CTkFrame(
    app, width=230, corner_radius=0, fg_color=SIDEBAR
)
sidebar.grid(row=0, column=0, sticky="nsew")
sidebar.grid_propagate(False)

ctk.CTkLabel(
    sidebar, text="📘 PyPDF Studio",
    font=("Arial", 24, "bold"), text_color=TEXT
).pack(padx=20, pady=(30, 5), anchor="w")

ctk.CTkLabel(
    sidebar, text="ALL-IN-ONE PDF TOOLKIT",
    font=("Arial", 10, "bold"), text_color=MUTED
).pack(padx=22, pady=(0, 30), anchor="w")

def nav_button(text, command):
    ctk.CTkButton(
        sidebar, text=text, command=command,
        height=44, corner_radius=10,
        fg_color="transparent", hover_color="#243858",
        text_color=TEXT, anchor="w",
        font=("Arial", 14)
    ).pack(fill="x", padx=12, pady=4)

nav_button("⌂   Home", lambda: show_home())
nav_button("▣   Merge PDFs", lambda: open_tool("Merge PDFs"))
nav_button("✂   Split PDF", lambda: open_tool("Split PDF"))
nav_button("⟳   Rotate Pages", lambda: open_tool("Rotate Pages"))
nav_button("▤   Delete Pages", lambda: open_tool("Delete Pages"))
nav_button("▧   Images to PDF", lambda: open_tool("Images to PDF"))
nav_button("▧   PDF to Images", lambda: open_tool("PDF to Images"))
nav_button("≡   Extract Text", lambda: open_tool("Extract Text"))

ctk.CTkLabel(
    sidebar, text="Made with Python ♥️",
    font=("Arial", 12), text_color=MUTED
).pack(side="bottom", pady=22)

# ---------- CONTENT AREA ----------
content = ctk.CTkFrame(app, fg_color=BG, corner_radius=0)
content.grid(row=0, column=1, sticky="nsew", padx=24, pady=20)
content.grid_columnconfigure((0, 1, 2), weight=1)

header = ctk.CTkFrame(content, fg_color="transparent")
header.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))
header.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(
    header, text="Welcome back 👋",
    font=("Arial", 27, "bold"), text_color=TEXT
).grid(row=0, column=0, sticky="w")

ctk.CTkLabel(
    header, text="Manage your PDF files in one place.",
    font=("Arial", 13), text_color=MUTED
).grid(row=1, column=0, sticky="w", pady=(5, 0))

ctk.CTkButton(
    header, text="⚙ Settings", width=110, height=36,
    fg_color=CARD, hover_color=BORDER,
    border_width=1, border_color=BORDER,
    command=lambda: messagebox.showinfo(
        "Settings", "Settings panel coming soon."
    )
).grid(row=0, column=1, rowspan=2, padx=(15, 0))

# ---------- HERO BANNER ----------
hero = ctk.CTkFrame(
    content, fg_color="#172D59",
    corner_radius=18, border_width=1, border_color="#31549A"
)
hero.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 25))
hero.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(
    hero, text="YOUR PDF WORKSPACE",
    font=("Arial", 11, "bold"), text_color="#93C5FD"
).grid(row=0, column=0, padx=24, pady=(22, 5), sticky="w")

ctk.CTkLabel(
    hero, text="Every PDF task, made simple.",
    font=("Arial", 24, "bold"), text_color=TEXT
).grid(row=1, column=0, padx=24, pady=5, sticky="w")

ctk.CTkLabel(
    hero, text="Edit  •  Organize  •  Convert  •  Extract",
    font=("Arial", 13), text_color="#C7D8F5"
).grid(row=2, column=0, padx=24, pady=(5, 22), sticky="w")

# ---------- SEARCH ----------
ctk.CTkLabel(
    content, text="Quick Tools",
    font=("Arial", 21, "bold"), text_color=TEXT
).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 12))

search = ctk.CTkEntry(
    content, placeholder_text="Search tools...",
    height=38, corner_radius=10,
    fg_color=CARD, border_color=BORDER
)
search.grid(row=2, column=2, sticky="ew", padx=(5, 0), pady=(0, 12))

# ---------- TOOL CARDS ----------
tools = [
    ("📑", "Merge PDFs", "Combine multiple PDF files", BLUE),
    ("✂", "Split PDF", "Separate pages into files", PURPLE),
    ("⟳", "Rotate Pages", "Change page orientation", "#059669"),
    ("▤", "Delete Pages", "Remove unwanted pages", "#DB2777"),
    ("🖼", "Images to PDF", "Create PDF from images", "#D97706"),
    ("📷", "PDF to Images", "Export pages as images", "#0891B2"),
    ("📄", "Extract Text", "Read text from PDF files", "#7C3AED"),
]

card_frames = []

for index, (icon, name, description, accent) in enumerate(tools):
    row = 3 + index // 3
    col = index % 3

    card = ctk.CTkFrame(
        content, fg_color=CARD, corner_radius=16,
        border_width=1, border_color=BORDER
    )
    card.grid(
        row=row, column=col, sticky="nsew",
        padx=5, pady=6
    )
    card.grid_columnconfigure(0, weight=1)
    card_frames.append((card, name))

    ctk.CTkLabel(
        card, text=icon, font=("Arial", 27),
        text_color=accent
    ).grid(row=0, column=0, padx=14, pady=(14, 5), sticky="w")

    ctk.CTkLabel(
        card, text=name, font=("Arial", 15, "bold"),
        text_color=TEXT
    ).grid(row=1, column=0, padx=14, pady=3, sticky="w")

    ctk.CTkLabel(
        card, text=description, font=("Arial", 11),
        text_color=MUTED, wraplength=200, justify="left"
    ).grid(row=2, column=0, padx=14, pady=(2, 10), sticky="w")

    ctk.CTkButton(
        card, text="Open Tool  →", height=32,
        fg_color=accent, hover_color=accent,
        corner_radius=8,
        command=lambda n=name: open_tool(n)
    ).grid(row=3, column=0, padx=14, pady=(0, 14), sticky="ew")

# ---------- SEARCH FUNCTION ----------
def filter_tools(*args):
    query = search.get().strip().lower()

    for card, name in card_frames:
        if query in name.lower():
            card.grid()
        else:
            card.grid_remove()

search.bind("<KeyRelease>", filter_tools)

# ---------- HOME ----------
def show_home():
    search.delete(0, "end")
    filter_tools()

app.mainloop()