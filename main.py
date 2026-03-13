import typer
import json
import os
from typing import Any
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from modules.banner import show_banner
from modules.validator import analyze_number
from modules.carrier import get_carrier
from modules.social_checker import check_all
from modules.spam_checker import check_spam, add_to_blacklist
from modules.email_checker import generate_email_dorks, analyze_email

app = typer.Typer(help="OSINT CI — Ivoirian Phone Number Intelligence Tool (+225)")
console = Console()


# ─── CALLBACK ───────────────────────────────────────────────────────────────


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    show_banner()
    if ctx.invoked_subcommand is None:
        rprint("[yellow]Use --help to see available commands.[/yellow]")


# ─── HELPERS ────────────────────────────────────────────────────────────────


def save_output(data: dict, number: str):
    if not os.path.exists("output"):
        os.makedirs("output")
    filename = f"output/scan_{number.replace('+', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    console.print(f"\n[bold green]✓[/bold green] Exported to [cyan]{filename}[/cyan]")


def display_dict_table(title: str, data: dict):
    table = Table(title=title)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")
    for key, value in data.items():
        table.add_row(str(key), str(value))
    console.print(table)


def display_dorks_table(title: str, dorks: dict):
    table = Table(title=title)
    table.add_column("Type", style="yellow")
    table.add_column("Dork", style="cyan")
    table.add_column("URL", style="blue")
    for key, info in dorks.items():
        if isinstance(info, dict):
            table.add_row(
                key.replace("_", " ").capitalize(),
                str(info.get("dork", "")),
                str(info.get("url", info.get("dork_url", ""))),
            )
    console.print(table)


# ─── COMMANDS ───────────────────────────────────────────────────────────────


@app.command()
def validate(
    number: str = typer.Argument(
        ..., help="Phone number to validate e.g. +2250707777777"
    )
):
    """Validate a phone number format and existence."""
    with console.status("[bold green]Validating..."):
        result = analyze_number(number)
    display_dict_table(f"Validation — {number}", result)


@app.command()
def carrier(number: str = typer.Argument(..., help="Phone number for carrier lookup")):
    """Get carrier and line type information."""
    with console.status("[bold green]Looking up carrier..."):
        result = get_carrier(number)
    if "error" in result:
        rprint(f"[bold red]Error:[/bold red] {result['error']}")
        raise typer.Exit(1)
    display_dict_table(f"Carrier — {number}", result)


@app.command()
def spam(number: str = typer.Argument(..., help="Phone number to check for spam")):
    """Check if a number is flagged as spam or fraud."""
    with console.status("[bold green]Checking spam status..."):
        result = check_spam(number)
    display_dict_table(f"Spam Check — {number}", result)


@app.command()
def social(
    number: str = typer.Argument(..., help="Phone number for social media check")
):
    """Check social media presence and generate search dorks."""
    v_result = analyze_number(number)
    if not v_result.get("valid"):
        rprint("[bold red]✗ Invalid number.[/bold red]")
        raise typer.Exit(1)

    e164 = v_result["e164"]
    local = str(v_result["national_number"])

    with console.status("[bold green]Searching social info..."):
        result = check_all(e164, local)

    rprint(
        Panel(f"Social Media & Dorks — [bold cyan]{number}[/bold cyan]", expand=False)
    )

    for platform, info in result.items():
        if not isinstance(info, dict):
            continue
        if platform == "name_search":
            display_dorks_table("Name Search Dorks", info)
        else:
            table = Table(title=platform.capitalize())
            table.add_column("Field", style="yellow")
            table.add_column("Value", style="white")
            for k, v in info.items():
                table.add_row(str(k), str(v))
            console.print(table)


@app.command()
def email(
    target: str = typer.Argument(
        ..., help="Email address OR phone number for email discovery"
    )
):
    """Analyze an email address or discover emails linked to a phone number."""
    if "@" in target:
        with console.status(f"[bold green]Analyzing email: {target}..."):
            result = analyze_email(target)
        if "error" in result:
            rprint(f"[bold red]Error:[/bold red] {result['error']}")
            raise typer.Exit(1)
        rprint(Panel(f"Email OSINT — [bold cyan]{target}[/bold cyan]", expand=False))
        dorks = result.get("dorks", {})
        if isinstance(dorks, dict):
            display_dorks_table("Email Dorks", dorks)

    else:
        v_result = analyze_number(target)
        if not v_result.get("valid"):
            rprint("[bold red]✗ Invalid phone number.[/bold red]")
            raise typer.Exit(1)
        with console.status(f"[bold green]Discovering emails for: {target}..."):
            result = generate_email_dorks(str(v_result["national_number"]))
        rprint(
            Panel(f"Email Discovery — [bold cyan]{target}[/bold cyan]", expand=False)
        )
        if isinstance(result, dict):
            display_dorks_table("Email Discovery Dorks", result)


@app.command()
def report(
    number: str = typer.Argument(..., help="Number to report"),
    type: str = typer.Option(
        "unknown", "--type", "-t", help="Type: arnaque / spam / harcelement"
    ),
):
    """Report a number as spam or fraud in the local blacklist."""
    result = add_to_blacklist(number, type)
    if result["action"] == "added":
        rprint(
            f"[bold green]✓ Added to blacklist:[/bold green] [cyan]{result['number']}[/cyan]"
        )
    else:
        rprint(
            f"[bold yellow]↑ Report updated:[/bold yellow] [cyan]{result['number']}[/cyan]"
        )
    rprint(f"[white]Type:[/white] [magenta]{result['type']}[/magenta]")


@app.command()
def scan(
    number: str = typer.Argument(..., help="Phone number to scan"),
    export: bool = typer.Option(False, "--export", "-e", help="Export results to JSON"),
):
    """Full OSINT scan on a phone number."""
    rprint(f"[bold]Starting full scan:[/bold] [cyan]{number}[/cyan]\n")

    results: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "number": number,
    }

    # 1. Validation
    with console.status("[bold green]Step 1/5 — Validating..."):
        v_res = analyze_number(number)
        results["validation"] = v_res

    if not v_res.get("valid"):
        rprint("[bold red]✗ Invalid number. Aborting.[/bold red]")
        if export:
            save_output(results, number)
        raise typer.Exit(1)

    # 2. Carrier
    with console.status("[bold green]Step 2/5 — Carrier Lookup..."):
        c_res = get_carrier(number)
        results["carrier"] = c_res

    # 3. Spam
    with console.status("[bold green]Step 3/5 — Spam Check..."):
        s_res = check_spam(number)
        results["spam"] = s_res

    # 4. Social
    with console.status("[bold green]Step 4/5 — Social Check..."):
        soc_res = check_all(v_res["e164"], str(v_res["national_number"]))
        results["social"] = soc_res

    # 5. Email Discovery
    with console.status("[bold green]Step 5/5 — Email Discovery..."):
        e_res = generate_email_dorks(str(v_res["national_number"]))
        results["email_discovery"] = e_res

    # ── Summary ──────────────────────────────────────────────────────────
    rprint(Panel("[bold green]✓ Scan Complete[/bold green]", expand=False))

    summary = Table(show_header=False, box=None, padding=(0, 2))
    summary.add_column(style="cyan")
    summary.add_column(style="white")
    summary.add_row("Number", number)
    summary.add_row("Valid", "Yes" if v_res.get("valid") else "❌ No")
    summary.add_row("Carrier", str(c_res.get("operator", "Unknown")))
    summary.add_row("Line Type", str(c_res.get("line_type", "Unknown")))
    summary.add_row("Risk Level", str(s_res.get("risk_level", "Unknown")))
    summary.add_row("Spam", "Yes" if s_res.get("is_spam") else "No")
    summary.add_row("Email Dorks", f"{len(e_res)} generated")
    console.print(summary)

    if export:
        save_output(results, number)


if __name__ == "__main__":
    app()
