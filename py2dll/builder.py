import os
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from .compiler import build_dll

class Py2DllUI:
    def __init__(self):
        self.console = Console()
        os.system("title py2dll Compiler-Builder")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_scripts(self):
        py_files = [f for f in os.listdir('.') if f.endswith('.py')]
        table = Table(title=f"[green]Scripts Found: ({len(py_files)})[/green]")
        table.add_column("No.", style="cyan")
        table.add_column("Script", style="magenta")
        for i, script in enumerate(py_files, start=1):
            table.add_row(str(i), script)
        self.console.print(table if py_files else "[red]No .py files found.[/red]")
        return py_files

    def build_interactive(self, py_files):
        if isinstance(py_files, str):
            py_files = py_files.split()

        name = Prompt.ask("DLL name", default="compiled")
        outdir = Prompt.ask("Output folder", default="output")

        try:
            self.console.print(f"[cyan]Building {', '.join(py_files)} → {name}.dll...[/cyan]")
            path = build_dll(py_files, name=name, outdir=outdir)
            self.console.print(f"[green]Build successful:[/green] {path}")
        except Exception as e:
            self.console.print(f"[red]Build failed:[/red] {e}")

    def run(self):
        py_files = self.show_scripts()

        while True:
            self.clear_screen()
            py_files = self.show_scripts()

            self.console.print("\nOptions: [blue](B)uild[/blue] | [red](R)efresh[/red] | [green](A)bout[/green] | (Q)uit")
            choice = Prompt.ask("Choose an action", choices=["b", "r", "a", "q"]).lower()

            if choice == "b":
                if not py_files:
                    self.console.print("[red]No Python files to build.[/red]")
                    time.sleep(2)
                    continue

                selection = Prompt.ask(
                    "Enter script number(s) or name(s)", default="1"
                )
                selected_files = []
                for item in selection.split():
                    if item.isdigit() and 1 <= int(item) <= len(py_files):
                        selected_files.append(py_files[int(item)-1])
                    elif os.path.exists(item):
                        selected_files.append(item)

                if selected_files:
                    self.build_interactive(selected_files)
                else:
                    self.console.print("[red]No valid files selected.[/red]")
                time.sleep(2)

            elif choice == "r":
                py_files = self.show_scripts()

            elif choice == "a":
                self.console.print("\nMade with love by ethanmal30! | [red]26/10/25[/red] | ver [green]1.0[/green]")
                time.sleep(3)

            elif choice == "q":
                break

def main():
    Py2DllUI().run()