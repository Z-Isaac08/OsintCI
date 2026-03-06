from colorama import Fore, Style

BANNER = r"""
  __   ____  __  __ _  ____     ___  __
 /  \ / ___)(  )(  ( \(_  _)   / __)(  )
(  O )\___ \ )( /    /  )(    ( (__  )(
 \__/ (____/(__)\_)__) (__)    \___)(__)
"""


def show_banner():
    print(Fore.MAGENTA + BANNER)
    print(Fore.CYAN + "  " + "─" * 40)
    print(Fore.WHITE + "  Ivoirian Phone OSINT Tool")
    print(Fore.WHITE + "  By: ZC0ok  |  version: 1.0.0")
    print(Fore.CYAN + "  " + "─" * 40)
    print(Fore.YELLOW + "  ⚠️  Usage légal uniquement")
    print(Style.RESET_ALL)
