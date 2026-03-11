#!/usr/bin/env python3
"""
VSSC BT Authorization Form
MacBook M1 compatible - Python + Tkinter
Usage: python3 BT_Form.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import subprocess, sys, os

# ── Auto-install fpdf2 for PDF export ──────────────────────────────────────
def ensure_fpdf():
    try:
        import fpdf
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2", "-q"])

ensure_fpdf()
from fpdf import FPDF

# ───────────────────────────────────────────────────────────────────────────
class BTForm(tk.Tk):
    NAVY  = "#1a3a6e"
    CREAM = "#f5f0e8"
    GOLD  = "#c8960c"
    EDIT  = "#fffde7"
    WHITE = "#ffffff"
    BORDER= "#cccccc"

    DEFAULTS = dict(
        ref_no          = "300",
        date            = "March 11, 2026",
        project         = "GSLV Continuation Project (Ph-6)",
        exp_type        = "Other Revenue Expenditure",
        table_project   = "GLSV Phase-6 (H6)",
        head            = "3402.00.101.63.33.15",
        line_item       = "H60140G3021",
        obj_head        = "A900",
        amount          = "Rs. 30,00,000/-",
        total_amount    = "Rs. 32,00,000/-",
        fy              = "2025-2026",
    )

    def __init__(self):
        super().__init__()
        self.title("VSSC – BT Authorization Form")
        self.configure(bg=self.CREAM)
        self.resizable(True, True)

        # Fonts
        self.f_title  = font.Font(family="Georgia", size=16, weight="bold")
        self.f_sub    = font.Font(family="Georgia", size=11)
        self.f_body   = font.Font(family="Georgia", size=11)
        self.f_bold   = font.Font(family="Georgia", size=11, weight="bold")
        self.f_small  = font.Font(family="Georgia", size=9, slant="italic")
        self.f_head   = font.Font(family="Georgia", size=10, weight="bold")
        self.f_btn    = font.Font(family="Helvetica Neue", size=11, weight="bold")

        self.vars = {k: tk.StringVar(value=v) for k, v in self.DEFAULTS.items()}

        self._build_ui()
        self.update_idletasks()
        w, h = 820, 700
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── UI Builder ────────────────────────────────────────────────────────
    def _build_ui(self):
        # Scrollable canvas
        outer = tk.Frame(self, bg=self.CREAM)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=self.CREAM, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.page = tk.Frame(canvas, bg=self.WHITE,
                             relief="flat", bd=0,
                             highlightbackground=self.BORDER,
                             highlightthickness=1)
        win_id = canvas.create_window((0, 0), window=self.page, anchor="nw")

        def _resize(e):
            canvas.itemconfig(win_id, width=e.width)
        canvas.bind("<Configure>", _resize)
        self.page.bind("<Configure>",
                       lambda e: canvas.configure(
                           scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        P = self.page
        pad = dict(padx=40, pady=0)

        # ── Header ───────────────────────────────────────────────────────
        hdr = tk.Frame(P, bg=self.NAVY, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Vikram Sarabhai Space Centre",
                 font=self.f_title, bg=self.NAVY, fg=self.WHITE).pack()
        tk.Label(hdr, text="Finance & Accounts Division",
                 font=self.f_sub,   bg=self.NAVY, fg="#ccd9f0").pack()
        tk.Label(hdr, text="Projects",
                 font=self.f_sub,   bg=self.NAVY, fg="#ccd9f0").pack()

        tk.Frame(P, height=1, bg=self.GOLD).pack(fill="x")

        sp = lambda h=10: tk.Frame(P, height=h, bg=self.WHITE).pack(fill="x")
        sp(16)

        # ── Ref No & Date ────────────────────────────────────────────────
        row1 = tk.Frame(P, bg=self.WHITE)
        row1.pack(fill="x", **pad)

        tk.Label(row1, text="No. VSSC/PROJ/BT/",
                 font=self.f_body, bg=self.WHITE).pack(side="left")
        self._entry(row1, "ref_no", width=8).pack(side="left")

        tk.Label(row1, text="Date:", font=self.f_body,
                 bg=self.WHITE, fg="#555").pack(side="right", padx=(0,4))
        self._entry(row1, "date", width=22).pack(side="right")

        sp(14)
        tk.Frame(P, height=1, bg="#e0d8cc").pack(fill="x", padx=40)
        sp(14)

        # ── Authorization para ───────────────────────────────────────────
        sec = tk.Frame(P, bg=self.WHITE)
        sec.pack(fill="x", **pad)

        tk.Label(sec,
                 text="Sr. Accounts & IFA, SDSC SHAR is authorized to make expenditure from",
                 font=self.f_body, bg=self.WHITE, wraplength=680, justify="left"
                 ).pack(anchor="w")

        r2 = tk.Frame(sec, bg=self.WHITE)
        r2.pack(anchor="w", pady=4)
        tk.Label(r2, text="Project:", font=self.f_body, bg=self.WHITE,
                 fg="#555").pack(side="left")
        self._entry(r2, "project", width=42).pack(side="left", padx=6)

        r3 = tk.Frame(sec, bg=self.WHITE)
        r3.pack(anchor="w", pady=4)
        tk.Label(r3, text="Expenditure Type:", font=self.f_body,
                 bg=self.WHITE, fg="#555").pack(side="left")
        self._entry(r3, "exp_type", width=32).pack(side="left", padx=6)
        tk.Label(r3, text="  for the F.Y", font=self.f_body,
                 bg=self.WHITE).pack(side="left")
        self._entry(r3, "fy", width=12).pack(side="left", padx=4)

        sp(16)
        tk.Frame(P, height=1, bg="#e0d8cc").pack(fill="x", padx=40)
        sp(8)

        # ── Amt note ────────────────────────────────────────────────────
        tk.Label(P, text="(Amt. in Rs.)", font=self.f_small,
                 bg=self.WHITE, fg="#777").pack(anchor="e", padx=44)
        sp(4)

        # ── Table ────────────────────────────────────────────────────────
        tbl_frame = tk.Frame(P, bg=self.WHITE)
        tbl_frame.pack(fill="x", padx=40, pady=4)

        cols = ["Project", "Head", "Line-Item Code\n& Object Head", "Amount"]
        widths = [160, 180, 190, 140]

        # Header row
        for ci, (c, w) in enumerate(zip(cols, widths)):
            cell = tk.Frame(tbl_frame, bg=self.NAVY,
                            width=w, height=44,
                            highlightbackground=self.WHITE,
                            highlightthickness=1)
            cell.pack_propagate(False)
            cell.grid(row=0, column=ci, sticky="nsew")
            tk.Label(cell, text=c, font=self.f_head,
                     bg=self.NAVY, fg=self.WHITE,
                     wraplength=w-10, justify="center").pack(expand=True)

        # Data row
        data_fields = [
            ("table_project", 160),
            ("head",          180),
            None,             # special: two fields
            ("amount",        140),
        ]

        def make_data_cell(parent, row, col, bg, w, h=56):
            cell = tk.Frame(parent, bg=bg, width=w, height=h,
                            highlightbackground=self.BORDER,
                            highlightthickness=1)
            cell.pack_propagate(False)
            cell.grid(row=row, column=col, sticky="nsew")
            return cell

        for ci, item in enumerate(data_fields):
            if ci == 2:
                cell = make_data_cell(tbl_frame, 1, ci, self.EDIT, 190, 72)
                self._entry(cell, "line_item", width=18).pack(pady=(8,2))
                self._entry(cell, "obj_head",  width=10).pack(pady=(2,8))
            else:
                key, w = item
                cell = make_data_cell(tbl_frame, 1, ci, self.EDIT, w)
                self._entry(cell, key, width=w//9).pack(expand=True)

        sp(18)
        tk.Frame(P, height=1, bg="#e0d8cc").pack(fill="x", padx=40)
        sp(14)

        # ── Summary para ─────────────────────────────────────────────────
        summ = tk.Frame(P, bg=self.WHITE)
        summ.pack(fill="x", **pad)

        tk.Label(summ,
                 text="With this the total allocation authorized to SDSC SHAR under",
                 font=self.f_body, bg=self.WHITE).pack(anchor="w")

        rs1 = tk.Frame(summ, bg=self.WHITE)
        rs1.pack(anchor="w", pady=4)
        tk.Label(rs1, text="Project:", font=self.f_body,
                 bg=self.WHITE, fg="#555").pack(side="left")
        self._entry(rs1, "project", width=42).pack(side="left", padx=6)

        rs2 = tk.Frame(summ, bg=self.WHITE)
        rs2.pack(anchor="w", pady=4)
        tk.Label(rs2, text="– Other Revenue Expenditure for the F.Y",
                 font=self.f_body, bg=self.WHITE).pack(side="left")
        self._entry(rs2, "fy", width=12).pack(side="left", padx=6)
        tk.Label(rs2, text="is", font=self.f_body,
                 bg=self.WHITE).pack(side="left")
        self._entry(rs2, "total_amount", width=18).pack(side="left", padx=6)

        sp(28)
        tk.Frame(P, height=1, bg="#e0d8cc").pack(fill="x", padx=40)
        sp(16)

        # ── Buttons ──────────────────────────────────────────────────────
        btn_row = tk.Frame(P, bg=self.WHITE)
        btn_row.pack(pady=(0, 24), padx=40, anchor="e")

        self._btn(btn_row, "↺  Reset", self.CREAM,    self.NAVY, self._reset
                  ).pack(side="left", padx=6)
        self._btn(btn_row, "⎙  Export PDF", self.NAVY, self.WHITE, self._export_pdf
                  ).pack(side="left", padx=6)

        # ── Legend ───────────────────────────────────────────────────────
        leg = tk.Frame(P, bg="#f9f7f3", pady=8)
        leg.pack(fill="x")
        tk.Label(leg,
                 text="💡  Yellow fields are editable — click and type to change values",
                 font=self.f_small, bg="#f9f7f3", fg="#888").pack()

    # ── Helpers ───────────────────────────────────────────────────────────
    def _entry(self, parent, key, width=20):
        e = tk.Entry(parent,
                     textvariable=self.vars[key],
                     font=self.f_bold,
                     width=width,
                     bg=self.EDIT,
                     fg="#1a1a1a",
                     relief="flat",
                     bd=0,
                     highlightbackground=self.GOLD,
                     highlightthickness=1,
                     insertbackground=self.NAVY)
        e.bind("<FocusIn>",  lambda ev, w=e: w.config(highlightbackground=self.NAVY, highlightthickness=2))
        e.bind("<FocusOut>", lambda ev, w=e: w.config(highlightbackground=self.GOLD, highlightthickness=1))
        return e

    def _btn(self, parent, text, bg, fg, cmd):
        b = tk.Button(parent, text=text, font=self.f_btn,
                      bg=bg, fg=fg, activebackground=self.GOLD,
                      activeforeground=self.WHITE,
                      relief="flat", padx=16, pady=7,
                      cursor="hand2", command=cmd,
                      highlightthickness=0, bd=0)
        return b

    def _reset(self):
        if messagebox.askyesno("Reset", "Sab fields original values par reset karein?"):
            for k, v in self.DEFAULTS.items():
                self.vars[k].set(v)

    # ── PDF Export ────────────────────────────────────────────────────────
    def _export_pdf(self):
        v = {k: var.get() for k, var in self.vars.items()}

        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(20, 20, 20)

        # Header
        pdf.set_fill_color(26, 58, 110)
        pdf.rect(0, 0, 210, 38, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 15)
        pdf.set_xy(0, 8)
        pdf.cell(210, 8, "Vikram Sarabhai Space Centre", align="C", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_x(0)
        pdf.cell(210, 7, "Finance & Accounts Division", align="C", ln=True)
        pdf.set_x(0)
        pdf.cell(210, 7, "Projects", align="C", ln=True)

        # Gold line
        pdf.set_draw_color(200, 150, 12)
        pdf.set_line_width(0.8)
        pdf.line(0, 38, 210, 38)
        pdf.set_line_width(0.2)
        pdf.set_draw_color(0, 0, 0)

        pdf.set_y(45)
        pdf.set_text_color(0, 0, 0)

        # Ref & Date
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(80, 7, f"No. VSSC/PROJ/BT/{v['ref_no']}", ln=False)
        pdf.cell(0, 7, v['date'], align="R", ln=True)
        pdf.ln(4)

        # Auth para
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6,
            f"Sr. Accounts & IFA, SDSC SHAR is authorized to make expenditure from "
            f"{v['project']} under {v['exp_type']} for the F.Y {v['fy']}.")
        pdf.ln(4)

        # Amt note
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, "(Amt. in Rs.)", align="R", ln=True)
        pdf.ln(2)

        # Table
        col_w = [50, 58, 55, 40]
        headers = ["Project", "Head", "Line-Item Code\n& Object Head", "Amount"]
        pdf.set_fill_color(26, 58, 110)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        for h, w in zip(headers, col_w):
            pdf.multi_cell(w, 5, h, border=1, align="C", fill=True,
                           new_x="RIGHT", new_y="LAST", max_line_height=5)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 253, 231)
        pdf.set_font("Helvetica", "B", 9)
        row_data = [v['table_project'], v['head'],
                    f"{v['line_item']}\n{v['obj_head']}", v['amount']]
        for d, w in zip(row_data, col_w):
            pdf.multi_cell(w, 5, d, border=1, align="C", fill=True,
                           new_x="RIGHT", new_y="LAST", max_line_height=5)
        pdf.ln(10)

        # Summary
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6,
            f"With this the total allocation authorized to SDSC SHAR under "
            f"{v['project']} - Other Revenue Expenditure for the F.Y {v['fy']} "
            f"is {v['total_amount']}.")

        # Save
        out = os.path.expanduser(f"~/Desktop/BT_Authorization_{v['ref_no']}.pdf")
        pdf.output(out)
        messagebox.showinfo("PDF Saved",
                            f"PDF saved to:\n{out}")


if __name__ == "__main__":
    app = BTForm()
    app.mainloop()
