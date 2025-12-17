# v3.0.0 ✠




import os
import time
import sys
import importlib




from tqdm import tqdm
from rich.console import Console




from SECURITY.LINK_ACTIONS import Phishing_Analysis
from SECURITY.DDOS_ACTIONS import DDoS_Analysis




Modul_1889 = importlib.import_module("1889")




Console_Instance = Console()




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Loading_Animation(Duration):

    Console_Instance.print("[green]Yükleniyor...[/green]")

    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='green'):
        time.sleep(0.010)

    Clear_Terminal()




def Display_Banner():
    Console_Instance.print(r"""
[bold red]
╔═══════════════════════════════════════════════════════════════════════╗

    ┓┏┓┏┓┏┓
    ┃┣┫┣┫┗┫
    ┻┗┛┗┛┗┛
    
    GÜVENLİK MERKEZİ                       

    Sahip Lisansı - 1889  |  Yazar - Vinnie  |  Sürüm - v3.0.0  [bold green]✠[/bold green][bold red]                                            
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():

    Console_Instance.print("[bold red]╠══    [/bold red][bold blue]GÜVENLİK ARAÇLARI[/bold blue]\n")

    Console_Instance.print("    [bold white][G1] [bold blue]Link Analiz Aracı[/bold blue][/bold white]")
    Console_Instance.print("    [bold white][G2] [bold blue]DDoS Analiz Aracı[/bold blue][/bold white]\n\n")

    Console_Instance.print("    [bold white][B] [bold red]Ana Menüye Dön[/bold red][/bold white]")
    Console_Instance.print("    [bold white][E] [bold red]Çıkış[/bold red][/bold white]\n")

    Console_Instance.print("[bold red]╚═══════════════════════════════════════════════════════════════════════╝[/bold red]\n")




def Main():
    while True:
        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print()

        Display_Menu()

        Choice = Console_Instance.input("[bold red]╠═ Komut Girin [/bold red]").strip().lower()

        if Choice == 'g1':
            Phishing_Analysis.Main()

        if Choice == 'g2':
            DDoS_Analysis.Main()

        if Choice == 'b':
            Modul_1889.Main()

        if Choice == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış yapıldı[/bold red]")
            sys.exit(0)




if __name__ == "__main__":
    Main()
