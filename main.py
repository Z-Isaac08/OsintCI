import typer
import json
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from modules.banner import show_banner
from modules.validator import analyze_number
from modules.carrier import get_carrier
from modules.social_checker import check_all
from modules.spam_checker import check_spam
from modules.email_checker import generate_email_dorks, analyze_email

app = typer.Typer(help="OSINT Tool for Ivoirian Phone Numbers (+225)")
console = Console()

def save_output(data, number):
    if not os.path.exists("output"):
        os.makedirs("output")

    filename = f"output/scan_{number.replace('+', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    console.print(f"\n[bold green]✓[/bold green] Results exported to [cyan]{filename}[/cyan]")

@app.command()
def validate(number: str):
    """Validate a phone number format and existence."""
    show_banner()
    with console.status("[bold green]Validating..."):
        result = analyze_number(number)

    table = Table(title=f"Validation Results: {number}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in result.items():
        table.add_row(str(key), str(value))

    console.print(table)

@app.command()
def carrier(number: str):
    """Get carrier information for a number."""
    show_banner()
    with console.status("[bold green]Looking up carrier..."):
        result = get_carrier(number)

    if "error" in result:
        rprint(f"[bold red]Error:[/bold red] {result['error']}")
        return

    table = Table(title=f"Carrier Info: {number}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in result.items():
        table.add_row(str(key), str(value))

    console.print(table)

@app.command()
def spam(number: str):
    """Check if a number is flagged as spam."""
    show_banner()
    with console.status("[bold green]Checking spam status..."):
        result = check_spam(number)

    table = Table(title=f"Spam Check: {number}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in result.items():
        table.add_row(str(key), str(value))

    console.print(table)

@app.command()
def social(number: str):
    """Check social media presence and generate dorks."""
    show_banner()
    # We need E164 and local number
    v_result = analyze_number(number)
    if not v_result.get("valid"):
        rprint("[bold red]Invalid number for social check.[/bold red]")
        return

    e164 = v_result["e164"]
    local = str(v_result["national_number"])

    with console.status("[bold green]Searching social info..."):
        result = check_all(e164, local)

    rprint(Panel(f"Social Media & Dorks for [bold cyan]{number}[/bold cyan]", expand=False))

    for platform, info in result.items():
        table = Table(show_header=True, header_style="bold blue")
        table.add_column(platform.capitalize(), style="yellow")
        table.add_column("Info")

        for k, v in info.items():
            table.add_row(k, str(v))
        console.print(table)

@app.command()
def email(target: str):
    """Analyze an email address or discover emails linked to a phone number."""
    show_banner()
    if "@" in target:
        # Standalone email analysis
        with console.status(f"[bold green]Analyzing email: {target}..."):
            result = analyze_email(target)

        if "error" in result:
            rprint(f"[bold red]Error:[/bold red] {result['error']}")
            return

        rprint(Panel(f"Email OSINT: [bold cyan]{target}[/bold cyan]", expand=False))
        for key, info in result["dorks"].items():
            table = Table(show_header=True, header_style="bold blue")
            table.add_column(key.replace("_", " ").capitalize(), style="yellow")
            table.add_column("Value")
            for k, v in info.items():
                table.add_row(k, str(v))
            console.print(table)
    else:
        # Discover emails linked to phone
        v_result = analyze_number(target)
        if not v_result.get("valid"):
            rprint("[bold red]Invalid phone number for email discovery.[/bold red]")
            return

        with console.status(f"[bold green]Discovering emails for: {target}..."):
            result = generate_email_dorks(str(v_result["national_number"]))

        rprint(Panel(f"Email Discovery Dorks for [bold cyan]{target}[/bold cyan]", expand=False))
        for key, info in result.items():
            table = Table(show_header=True, header_style="bold blue")
            table.add_column(key.replace("_", " ").capitalize(), style="yellow")
            table.add_column("Value")
            for k, v in info.items():
                table.add_row(k, str(v))
            console.print(table)

@app.command()
def scan(number: str, export: bool = typer.Option(False, "--export", help="Export results to JSON")):
    """Full OSINT scan on a phone number."""
    show_banner()
    rprint(f"[bold]Starting full scan for:[/bold] [cyan]{number}[/cyan]\n")

    results = {"timestamp": datetime.now().isoformat(), "number": number}

    # 1. Validation
    with console.status("[bold green]Validating..."):
        v_res = analyze_number(number)
        results["validation"] = v_res

    if not v_res.get("valid"):
        rprint("[bold red]! Invalid number. Aborting further checks.[/bold red]")
        if export:
            save_output(results, number)
        return

    # 2. Carrier
    with console.status("[bold green]Carrier Lookup..."):
        c_res = get_carrier(number)
        results["carrier"] = c_res

    # 3. Spam
    with console.status("[bold green]Spam Check..."):
        s_res = check_spam(number)
        results["spam"] = s_res

    # 4. Social
    with console.status("[bold green]Social Check..."):
        soc_res = check_all(v_res["e164"], str(v_res["national_number"]))
        results["social"] = soc_res

    # 5. Email Discovery
    with console.status("[bold green]Email Discovery..."):
        e_res = generate_email_dorks(str(v_res["national_number"]))
        results["email_discovery"] = e_res

    # Display Summary
    rprint(Panel("[bold green]Scan Complete[/bold green]", expand=False))

    # Simple summary display
    summary_table = Table(show_header=False, box=None)
    summary_table.add_row("[cyan]Valid:[/cyan]", str(v_res.get("valid")))
    summary_table.add_row("[cyan]Carrier:[/cyan]", c_res.get("operator", "Unknown"))
    summary_table.add_row("[cyan]Line Type:[/cyan]", c_res.get("line_type", "Unknown"))
    summary_table.add_row("[cyan]Risk Level:[/cyan]", s_res.get("risk_level", "Unknown"))
    summary_table.add_row("[cyan]Email Dorks:[/cyan]", f"{len(e_res)} generated")
    console.print(summary_table)

    if export:
        save_output(results, number)

if __name__ == "__main__":
    app()
