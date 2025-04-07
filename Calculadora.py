import tkinter as tk
from tkinter import font as tkfont
import math

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("350x550")
        self.root.resizable(False, False)

        # Cores (tema escuro)
        self.bg_color = "#1e1e1e"
        self.display_bg = "#2d2d2d"
        self.button_bg = "#3c3c3c"
        self.button_active_bg = "#5c5c5c"
        self.operation_bg = "#4a90e2"
        self.operation_active_bg = "#357ABD"
        self.special_bg = "#606060"
        self.text_color = "#ffffff"

        self.root.configure(bg=self.bg_color)

        # Variáveis
        self.current_input = "0"
        self.stored_value = None
        self.current_operation = None
        self.reset_input = False

        # Fontes
        self.display_font = tkfont.Font(size=32, weight="bold")
        self.button_font = tkfont.Font(size=16)

        # Display
        self.display_var = tk.StringVar()
        self.display_var.set(self.current_input)

        self.display = tk.Label(
            root,
            textvariable=self.display_var,
            font=self.display_font,
            bg=self.display_bg,
            fg=self.text_color,
            anchor="e",
            padx=20,
            pady=30
        )
        self.display.pack(fill=tk.X)

        # Botões
        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.pack(expand=True, fill=tk.BOTH)

        buttons = [
            ["√", "π", "^", "!"],
            ["AC", "( )", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ",", "⌫", "="]
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text in ["+", "-", "×", "÷", "=", "^", "!"]:
                    color_bg = self.operation_bg
                    color_active = self.operation_active_bg
                elif text in ["√", "π", "AC", "( )", "%", "⌫"]:
                    color_bg = self.special_bg
                    color_active = self.button_active_bg
                else:
                    color_bg = self.button_bg
                    color_active = self.button_active_bg

                btn = tk.Button(
                    self.button_frame,
                    text=text,
                    font=self.button_font,
                    bg=color_bg,
                    activebackground=color_active,
                    fg=self.text_color,
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

        # Expandir os botões para ocupar toda a área
        for i in range(len(buttons)):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.button_frame.grid_columnconfigure(j, weight=1)

    def on_button_click(self, text):
        if text.isdigit() or text == ",":
            self.handle_digit(text)
        elif text in ["+", "-", "×", "÷", "^"]:
            self.handle_operation(text)
        elif text == "=":
            self.handle_equals()
        elif text == "AC":
            self.handle_clear()
        elif text == "π":
            self.handle_pi()
        elif text == "√":
            self.handle_square_root()
        elif text == "%":
            self.handle_percentage()
        elif text == "( )":
            self.handle_parentheses()
        elif text == "⌫":
            self.handle_backspace()
        elif text == "!":
            self.handle_factorial()

        self.update_display()

    def format_number(self, value):
        try:
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            return f"{value:,.0f}".replace(",", ".")
        except:
            return str(value)

    def handle_digit(self, digit):
        if self.reset_input:
            self.current_input = "0"
            self.reset_input = False

        if digit == ",":
            if "." not in self.current_input:
                self.current_input += "."
        else:
            if self.current_input == "0":
                self.current_input = digit
            else:
                self.current_input += digit

    def handle_operation(self, op):
        self.stored_value = float(self.current_input.replace(",", "."))
        self.current_operation = op
        self.reset_input = True

    def handle_equals(self):
        try:
            current_value = float(self.current_input.replace(",", "."))
            result = 0
            if self.current_operation == "+":
                result = self.stored_value + current_value
            elif self.current_operation == "-":
                result = self.stored_value - current_value
            elif self.current_operation == "×":
                result = self.stored_value * current_value
            elif self.current_operation == "÷":
                result = self.stored_value / current_value
            elif self.current_operation == "^":
                result = math.pow(self.stored_value, current_value)

            self.current_input = self.format_number(result)
        except:
            self.current_input = "Erro"

        self.current_operation = None
        self.reset_input = True

    def handle_clear(self):
        self.current_input = "0"
        self.stored_value = None
        self.current_operation = None
        self.reset_input = False

    def handle_pi(self):
        self.current_input = self.format_number(round(math.pi, 8))
        self.reset_input = True

    def handle_square_root(self):
        try:
            val = float(self.current_input.replace(",", "."))
            if val >= 0:
                result = math.sqrt(val)
                self.current_input = self.format_number(result)
            else:
                self.current_input = "Erro"
        except:
            self.current_input = "Erro"

    def handle_percentage(self):
        try:
            val = float(self.current_input.replace(",", ".")) / 100
            self.current_input = self.format_number(val)
        except:
            self.current_input = "Erro"

    def handle_parentheses(self):
        if "(" not in self.current_input:
            self.current_input = "(" + self.current_input + ")"
        else:
            self.current_input = self.current_input.replace("(", "").replace(")", "")

    def handle_backspace(self):
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"

    def handle_factorial(self):
        try:
            val = int(float(self.current_input.replace(",", ".")))
            self.current_input = self.format_number(math.factorial(val))
        except:
            self.current_input = "Erro"

    def update_display(self):
        self.display_var.set(self.current_input)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()
