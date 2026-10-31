import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from services.pdf_service import PDFService
from services.image_service import ImageService


# ================= THEME =================
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


class PDFEditorApp:

    def __init__(self):
        self.service = PDFService()
        self.image_service = ImageService()
        self.cards = []

        self.root = ctk.CTk()
        self.root.title("PyPDF Studio | PDF Workspace")
        self.root.geometry("1150x760")
        self.root.minsize(900, 620)
        self.root.configure(fg_color=BG)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_dashboard()

    # ================= SIDEBAR =================
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(
            self.root,
            width=225,
            corner_radius=0,
            fg_color=SIDEBAR
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="📘 PyPDF Studio",
            font=("Arial", 23, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(28, 5))

        ctk.CTkLabel(
            sidebar,
            text="ALL-IN-ONE PDF TOOLKIT",
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(anchor="w", padx=20, pady=(0, 25))

        navigation = [
            ("⌂   Home", self.show_home),
            ("▣   Merge PDFs", self.merge_pdf),
            ("✂   Split PDF", self.split_pdf),
            ("⟳   Rotate Pages", self.rotate_page),
            ("▤   Delete Pages", self.delete_pages),
            ("▧   Images to PDF", self.images_to_pdf),
            ("▧   PDF to Images", self.pdf_to_images),
            ("≡   Extract Text", self.extract_text),
        ]

        for label, command in navigation:
            ctk.CTkButton(
                sidebar,
                text=label,
                command=command,
                height=42,
                corner_radius=9,
                fg_color="transparent",
                hover_color="#243858",
                text_color=TEXT,
                anchor="w",
                font=("Arial", 13)
            ).pack(fill="x", padx=10, pady=3)

        ctk.CTkFrame(
            sidebar, height=1, fg_color=BORDER
        ).pack(fill="x", padx=15, pady=(22, 12))

        ctk.CTkLabel(
            sidebar,
            text="Made with Python ♥️",
            text_color=MUTED,
            font=("Arial", 12)
        ).pack(side="bottom", pady=22)

    # ================= DASHBOARD =================
    def create_dashboard(self):
        self.content = ctk.CTkScrollableFrame(
            self.root,
            fg_color=BG,
            corner_radius=0
        )
        self.content.grid(
            row=0, column=1,
            sticky="nsew",
            padx=20, pady=14
        )

        self.content.grid_columnconfigure(
            (0, 1, 2),
            weight=1,
            uniform="tool_cards"
        )

        # Header
        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        header.grid(
            row=0, column=0,
            columnspan=3,
            sticky="ew",
            pady=(8, 20)
        )
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Welcome back 👋",
            font=("Arial", 27, "bold"),
            text_color=TEXT
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Manage your PDF files in one place.",
            font=("Arial", 13),
            text_color=MUTED
        ).grid(
            row=1, column=0,
            sticky="w", pady=(5, 0)
        )

        ctk.CTkButton(
            header,
            text="☾ Dark Mode",
            width=115,
            height=35,
            fg_color=CARD,
            hover_color=BORDER,
            command=self.toggle_theme
        ).grid(
            row=0, column=1,
            rowspan=2, padx=5
        )

        # Welcome banner
        hero = ctk.CTkFrame(
            self.content,
            fg_color="#172D59",
            corner_radius=17,
            border_width=1,
            border_color="#31549A"
        )
        hero.grid(
            row=1, column=0,
            columnspan=3,
            sticky="ew",
            pady=(0, 22)
        )

        ctk.CTkLabel(
            hero,
            text="YOUR PDF WORKSPACE",
            font=("Arial", 11, "bold"),
            text_color="#93C5FD"
        ).pack(
            anchor="w", padx=22, pady=(18, 4)
        )

        ctk.CTkLabel(
            hero,
            text="Every PDF task, made simple.",
            font=("Arial", 23, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=22, pady=4)

        ctk.CTkLabel(
            hero,
            text="Edit  •  Organize  •  Convert  •  Extract",
            font=("Arial", 13),
            text_color="#C7D8F5"
        ).pack(
            anchor="w", padx=22, pady=(4, 18)
        )

        # Tools heading
        ctk.CTkLabel(
            self.content,
            text="⚡ Quick Tools",
            font=("Arial", 21, "bold"),
            text_color=TEXT
        ).grid(
            row=2, column=0,
            columnspan=2,
            sticky="w",
            padx=4, pady=(0, 12)
        )

        # Search
        self.search = ctk.CTkEntry(
            self.content,
            placeholder_text="Search tools...",
            height=38,
            corner_radius=10,
            fg_color=CARD,
            border_color=BORDER
        )
        self.search.grid(
            row=2, column=2,
            sticky="ew",
            padx=5, pady=(0, 12)
        )
        self.search.bind(
            "<KeyRelease>", self.filter_tools
        )

        # Tool cards: actual methods are connected
        tools = [
            (
                "📑", "Merge PDFs",
                "Combine multiple PDF files",
                BLUE, self.merge_pdf
            ),
            (
                "✂", "Split PDF",
                "Extract a range of pages",
                PURPLE, self.split_pdf
            ),
            (
                "⟳", "Rotate Pages",
                "Change page orientation",
                "#059669", self.rotate_page
            ),
            (
                "▤", "Delete Pages",
                "Remove unwanted pages",
                "#DB2777", self.delete_pages
            ),
            (
                "🖼", "Images to PDF",
                "Create PDF from images",
                "#D97706", self.images_to_pdf
            ),
            (
                "📷", "PDF to Images",
                "Export pages as images",
                "#0891B2", self.pdf_to_images
            ),
            (
                "📄", "Extract Text",
                "Read text from PDF files",
                "#7C3AED", self.extract_text
            ),
        ]

        for index, (icon, name, description,
                    accent, action) in enumerate(tools):

            row = 3 + index // 3
            col = index % 3

            card = ctk.CTkFrame(
                self.content,
                fg_color=CARD,
                corner_radius=15,
                border_width=1,
                border_color=BORDER
            )
            card.grid(
                row=row, column=col,
                sticky="nsew",
                padx=5, pady=6
            )

            self.cards.append((card, name))

            ctk.CTkLabel(
                card,
                text=icon,
                font=("Arial", 27),
                text_color=accent
            ).pack(
                anchor="w", padx=14, pady=(14, 5)
            )

            ctk.CTkLabel(
                card,
                text=name,
                font=("Arial", 15, "bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=14, pady=3)

            ctk.CTkLabel(
                card,
                text=description,
                font=("Arial", 11),
                text_color=MUTED,
                wraplength=210,
                justify="left"
            ).pack(
                anchor="w", padx=14, pady=(2, 12)
            )

            ctk.CTkButton(
                card,
                text="Open Tool  →",
                command=action,
                height=34,
                corner_radius=9,
                fg_color=accent,
                hover_color=accent
            ).pack(
                fill="x", padx=14, pady=(0, 14)
            )

        # Footer
        ctk.CTkLabel(
            self.content,
            text="PyPDF Studio  •  All your PDF tools in one place",
            text_color=MUTED,
            font=("Arial", 11)
        ).grid(
            row=6, column=0,
            columnspan=3, pady=20
        )

    # ================= SEARCH =================
    def filter_tools(self, event=None):
        query = self.search.get().strip().lower()

        for card, name in self.cards:
            if query in name.lower():
                card.grid()
            else:
                card.grid_remove()

    def show_home(self):
        self.search.delete(0, "end")
        self.filter_tools()

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = (
            "light" if current.lower() == "dark"
            else "dark"
        )
        ctk.set_appearance_mode(new_mode)

    # ================= MERGE PDF =================
    def merge_pdf(self):
        files = filedialog.askopenfilenames(
            title="Select PDFs to merge",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not files:
            return

        output = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not output:
            return

        try:
            self.service.merge_pdfs(files, output)
            messagebox.showinfo(
                "Success", "PDFs merged successfully!"
            )
        except Exception as e:
            messagebox.showerror("Merge Error", str(e))

    # ================= SPLIT PDF =================
    def split_pdf(self):
        file = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not file:
            return

        start = simpledialog.askinteger(
            "Start Page", "Enter start page:",
            parent=self.root, minvalue=1
        )
        if start is None:
            return

        end = simpledialog.askinteger(
            "End Page", "Enter end page:",
            parent=self.root, minvalue=start
        )
        if end is None:
            return

        output = filedialog.asksaveasfilename(
            title="Save split PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not output:
            return

        try:
            self.service.split_pdf(
                file, start, end, output
            )
            messagebox.showinfo(
                "Success", "PDF split successfully!"
            )
        except Exception as e:
            messagebox.showerror("Split Error", str(e))

    # ================= ROTATE PAGE =================
    def rotate_page(self):
        file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not file:
            return

        page = simpledialog.askinteger(
            "Page Number",
            "Enter page number to rotate:",
            parent=self.root, minvalue=1
        )
        if page is None:
            return

        angle = simpledialog.askinteger(
            "Rotation Angle",
            "Enter 90, 180, or 270:",
            parent=self.root
        )
        if angle is None:
            return

        if angle not in (90, 180, 270):
            messagebox.showerror(
                "Invalid Input",
                "Angle must be 90, 180, or 270."
            )
            return

        output = filedialog.asksaveasfilename(
            title="Save rotated PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not output:
            return

        try:
            self.service.rotate_page(
                file, page, angle, output
            )
            messagebox.showinfo(
                "Success", "Page rotated successfully!"
            )
        except Exception as e:
            messagebox.showerror("Rotation Error", str(e))

    # ================= DELETE PAGES =================
    def delete_pages(self):
        file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not file:
            return

        pages = simpledialog.askstring(
            "Delete Pages",
            "Enter page numbers separated by commas (e.g. 2,4,6):",
            parent=self.root
        )
        if not pages:
            return

        try:
            page_list = [
                int(p.strip()) for p in pages.split(",")
            ]

            if any(p < 1 for p in page_list):
                raise ValueError(
                    "Page numbers must be 1 or greater."
                )

            output = filedialog.asksaveasfilename(
                title="Save edited PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )
            if not output:
                return

            self.service.delete_pages(
                file, page_list, output
            )
            messagebox.showinfo(
                "Success", "Selected pages deleted!"
            )
        except Exception as e:
            messagebox.showerror("Delete Error", str(e))

    # ================= IMAGES TO PDF =================
    def images_to_pdf(self):
        files = filedialog.askopenfilenames(
            title="Select images",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )
        if not files:
            return

        output = filedialog.asksaveasfilename(
            title="Save PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not output:
            return

        try:
            self.image_service.image_to_pdf(
                files, output
            )
            messagebox.showinfo(
                "Success", "PDF created successfully!"
            )
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    # ================= PDF TO IMAGES =================
    def pdf_to_images(self):
        pdf = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not pdf:
            return

        folder = filedialog.askdirectory(
            title="Choose output folder"
        )
        if not folder:
            return

        try:
            self.image_service.pdf_to_images(pdf, folder)
            messagebox.showinfo(
                "Success", "Images saved successfully!"
            )
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    # ================= EXTRACT TEXT =================
    def extract_text(self):
        file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not file:
            return

        try:
            text = self.service.extract_text(file)

            window = ctk.CTkToplevel(self.root)
            window.title("PyPDF Studio | Extracted Text")
            window.geometry("800x550")
            window.minsize(500, 350)
            window.configure(fg_color=BG)

            ctk.CTkLabel(
                window,
                text="📄 Extracted PDF Text",
                font=("Arial", 22, "bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=18, pady=(18, 8))

            textbox = ctk.CTkTextbox(
                window,
                corner_radius=10,
                fg_color=CARD,
                text_color=TEXT,
                font=("Arial", 13),
                wrap="word"
            )
            textbox.pack(
                fill="both", expand=True,
                padx=18, pady=10
            )
            textbox.insert("1.0", text or "No text found.")
            textbox.configure(state="disabled")

            def save_text():
                path = filedialog.asksaveasfilename(
                    parent=window,
                    title="Save extracted text",
                    defaultextension=".txt",
                    filetypes=[("Text Files", "*.txt")]
                )
                if not path:
                    return

                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(text or "")
                    messagebox.showinfo(
                        "Success", "Text saved successfully!",
                        parent=window
                    )
                except Exception as e:
                    messagebox.showerror(
                        "Save Error", str(e), parent=window
                    )

            ctk.CTkButton(
                window,
                text="Save Text",
                command=save_text,
                height=38,
                fg_color=BLUE,
                hover_color="#2563EB"
            ).pack(pady=(0, 16))

        except Exception as e:
            messagebox.showerror("Extraction Error", str(e))

    # ================= RUN APP =================
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PDFEditorApp()
    app.run()