#!/usr/bin/env python3

import subprocess
import tkinter as tk
import os
from pathlib import Path
from tkinter import messagebox


DEFAULT_DIR = Path(__file__).resolve().parent
SUMATRA_PDF = Path(r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe")
WINDOW_SIZE = "600x250"
BOOKLET_PAPER = {
    "A4": "A3",
    "A5": "A4",
}


def load_properties(properties_file):
    properties = {}
    if not properties_file.exists():
        return properties

    # Preserve Windows backslashes as literal characters.
    for line in properties_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "!")):
            continue

        key, separator, value = line.partition("=")
        if separator:
            properties[key.strip()] = value.strip()

    return properties


def load_pdf_directory(properties_file):
    value = load_properties(properties_file).get("pdf.directory", "")
    directory = DEFAULT_DIR
    if value:
        directory = Path(value)
        if not directory.is_absolute():
            directory = properties_file.parent / directory

    return directory


class PdfPrinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Printer - Medium")
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)

        self.script_dir = Path(__file__).resolve().parent
        self.selected_file = None
        self.booklet_size = tk.StringVar(master=root, value="A4")

        self._build_ui()

    def _build_ui(self):
        # Build a compact modal-style form.
        main_frame = tk.Frame(self.root, padx=12, pady=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        select_frame = tk.Frame(main_frame)
        select_frame.pack(fill=tk.X)

        select_label = tk.Label(select_frame, text="Sélectionner un fichier PDF:")
        select_label.pack(side=tk.LEFT)

        browse_button = tk.Button(select_frame, text="Parcourir", command=self._browse_file)
        browse_button.pack(side=tk.RIGHT)

        # Keep only the filename visible to the user.
        self.file_label = tk.Label(
            main_frame,
            text="Aucun fichier sélectionné",
            anchor=tk.W,
            bg="#e6e6e6",
            padx=8,
            pady=8,
            relief=tk.SUNKEN,
        )
        self.file_label.pack(fill=tk.X, pady=(18, 18))

        format_frame = tk.Frame(main_frame)
        format_frame.pack(fill=tk.X, pady=(0, 14))

        tk.Label(format_frame, text="Format du livret :").pack(side=tk.LEFT)
        for booklet_size, paper_size in BOOKLET_PAPER.items():
            tk.Radiobutton(
                format_frame,
                text=f"{booklet_size} (feuilles {paper_size})",
                variable=self.booklet_size,
                value=booklet_size,
            ).pack(side=tk.LEFT, padx=(10, 0))

        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        self.print_button = tk.Button(
            button_frame,
            text="Imprimer",
            command=self._print_file,
            state=tk.DISABLED,
            width=14,
        )
        self.print_button.pack(side=tk.LEFT)

        quit_button = tk.Button(button_frame, text="Quitter", command=self.root.destroy, width=14)
        quit_button.pack(side=tk.RIGHT)

    def _browse_file(self):
        try:
            initial_dir = load_pdf_directory(self.script_dir / "print-medium-pdf.properties")
        except (OSError, UnicodeError) as error:
            messagebox.showerror("Erreur", f"Impossible de lire print-medium-pdf.properties:\n{error}")
            return

        if not initial_dir.is_dir():
            initial_dir = self.script_dir

        file_path = self._select_pdf_file(initial_dir)

        if not file_path:
            return

        self.selected_file = Path(file_path)
        self.file_label.config(text=self.selected_file.name)
        self.print_button.config(state=tk.NORMAL)

    def _select_pdf_file(self, directory):
        candidates = self._get_printable_pdfs(directory)
        if len(candidates) == 0:
            messagebox.showinfo("Information", "Aucun PDF imprimable disponible.")
            return None

        dialog = tk.Toplevel(self.root)
        dialog.title("Sélectionner un fichier PDF")
        dialog.geometry("760x360")
        dialog.minsize(520, 260)
        dialog.transient(self.root)
        dialog.grab_set()

        selected_file = {"path": None}

        button_frame = tk.Frame(dialog, padx=10, pady=10)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Show only files that still need a booklet output.
        list_frame = tk.Frame(dialog, padx=10, pady=10)
        list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")

        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=listbox.yview)

        for file_path in candidates:
            listbox.insert(tk.END, file_path.name)

        def confirm_selection():
            selection = listbox.curselection()
            if len(selection) == 0:
                messagebox.showerror("Erreur", "Veuillez sélectionner un fichier PDF.")
                return

            selected_file["path"] = candidates[selection[0]]
            dialog.destroy()

        def cancel_selection():
            dialog.destroy()

        listbox.bind("<Double-Button-1>", lambda event: confirm_selection())
        listbox.bind("<Return>", lambda event: confirm_selection())

        select_button = tk.Button(button_frame, text="OK", command=confirm_selection, width=14)
        select_button.pack(side=tk.LEFT)

        cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_selection, width=14)
        cancel_button.pack(side=tk.RIGHT)

        listbox.focus_set()
        listbox.selection_set(0)
        self.root.wait_window(dialog)

        return selected_file["path"]

    def _get_printable_pdfs(self, directory):
        candidates = []

        for file_path in sorted(directory.glob("*.pdf"), key=lambda path: path.name.lower()):
            filename = file_path.name.lower()
            if filename.endswith("-book.pdf"):
                continue

            output_file = file_path.with_name(f"{file_path.stem}-book.pdf")
            if output_file.exists():
                continue

            candidates.append(file_path)

        return candidates

    def _print_file(self):
        if self.selected_file is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier PDF.")
            return

        if not self.selected_file.exists():
            messagebox.showerror("Erreur", "Le fichier sélectionné n'existe plus.")
            return

        if self.selected_file.suffix.lower() != ".pdf":
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier PDF.")
            return

        self.print_button.config(state=tk.DISABLED)
        self.root.update_idletasks()

        try:
            result = self._run_booklet_script()
        except OSError as error:
            messagebox.showerror("Erreur", f"Impossible d'exécuter create-booklet.bat:\n{error}")
            self.print_button.config(state=tk.NORMAL)
            return

        output_file = self.selected_file.with_name(f"{self.selected_file.stem}-book.pdf")

        if result.returncode != 0:
            error_text = result.stderr.strip()
            if not error_text:
                error_text = result.stdout.strip()
            if not error_text:
                error_text = f"Code retour: {result.returncode}"

            messagebox.showerror("Erreur", error_text)
            self.print_button.config(state=tk.NORMAL)
            return

        if not output_file.exists():
            messagebox.showerror("Erreur", f"Le fichier généré est introuvable:\n{output_file.name}")
            self.print_button.config(state=tk.NORMAL)
            return

        try:
            print_result = self._print_booklet_file(output_file)
        except OSError as error:
            messagebox.showerror("Erreur", f"Impossible de lancer l'impression:\n{error}")
            self.print_button.config(state=tk.NORMAL)
            return

        if print_result.returncode != 0:
            error_text = print_result.stderr.strip()
            if not error_text:
                error_text = print_result.stdout.strip()
            if not error_text:
                error_text = f"Code retour impression: {print_result.returncode}"

            messagebox.showerror("Erreur", error_text)
            self.print_button.config(state=tk.NORMAL)
            return

        messagebox.showinfo(
            "Succès",
            f"Fichier généré et envoyé à l'imprimante:\n{output_file.name}",
        )

        self.print_button.config(state=tk.NORMAL)

    def _run_booklet_script(self):
        bat_path = self.script_dir / "create-booklet.bat"
        tools_bin = self.script_dir / ".tools" / "bin"
        env = os.environ.copy()
        path_key = "PATH"
        for key in env:
            if key.upper() == "PATH":
                path_key = key
                break
        env[path_key] = f"{tools_bin};{env.get(path_key, '')}"

        # Run synchronously so the GUI waits for the final return code.
        return subprocess.run(
            [
                "cmd.exe", "/d", "/c", "call", str(bat_path),
                str(self.selected_file), BOOKLET_PAPER[self.booklet_size.get()],
            ],
            cwd=str(self.script_dir),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def _print_booklet_file(self, output_file):
        properties = load_properties(self.script_dir / "print-medium-pdf.properties")
        printer_name = properties.get("printer.name", "")
        if not printer_name:
            raise OSError("Renseignez printer.name dans print-medium-pdf.properties.")

        sumatra_pdf = Path(properties.get("sumatra.path", str(SUMATRA_PDF)))
        if not sumatra_pdf.is_absolute():
            sumatra_pdf = self.script_dir / sumatra_pdf
        if not sumatra_pdf.exists():
            raise OSError(f"SumatraPDF introuvable: {sumatra_pdf}")

        # Print all pages once to the configured network printer.
        return subprocess.run(
            [
                str(sumatra_pdf),
                "-silent",
                "-exit-when-done",
                "-print-to",
                printer_name,
                "-print-settings",
                f"paper={BOOKLET_PAPER[self.booklet_size.get()]},duplexshort,color,fit,1x",
                str(output_file),
            ],
            cwd=str(self.script_dir),
            capture_output=True,
            text=True,
            check=False,
        )


def main():
    root = tk.Tk()
    PdfPrinterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
