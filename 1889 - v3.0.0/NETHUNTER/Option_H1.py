# v3.0.0 ✠




import os
import time
import sys
import importlib




from tqdm import tqdm
from rich.console import Console




from NETHUNTER.IP_ACTIONS import Ip_Extract
from NETHUNTER.PORT_ACTIONS import Port_Extract




Modul_1889 = importlib.import_module("1889")




Console_Instance = Console()




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Loading_Animation(Duration):

    Console_Instance.print("[green]Loading...[/green]")

    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}", colour='green'):
        time.sleep(0.010)

    Clear_Terminal()




def Display_Banner():
    Console_Instance.print(r"""
[bold red]
╔═══════════════════════════════════════════════════════════════════════╗

    ┓┏┓┏┓┏┓
    ┃┣┫┣┫┗┫
    ┻┗┛┗┛┗┛
       
    NETHUNTER MERKEZİ    

    Owner License : 1889  |  Author : Vinnie  |  Version : v3.0.0  [bold green]✠[/bold green][bold red]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():

    Console_Instance.print("[bold red]╠══    [/bold red][bold green]NETHUNTER ARAÇLARI[/bold green]\n")

    Console_Instance.print("    [bold white][N1] [bold green]IP Sorgu Aracı[/bold green][/bold white]")
    Console_Instance.print("    [bold white][N2] [bold green]Port Sorgu Aracı[/bold green][/bold white]\n\n")


    Console_Instance.print("    [bold white][B]  [bold red]Ana Menüye Dön[/bold red][/bold white]")
    Console_Instance.print("    [bold white][E]  [bold red]Çıkış[/bold red][/bold white]\n")

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

        if Choice == 'n1':
            Ip_Extract.Main()

        if Choice == 'n2':
            Port_Extract.Main()

        if Choice == 'b':
            Modul_1889.Main()

        if Choice == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)




if __name__ == "__main__":
    Main()
