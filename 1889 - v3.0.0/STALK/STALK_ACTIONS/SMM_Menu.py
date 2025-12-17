# v3.0.0 ✠




import os
import time
import sys




from tqdm import tqdm
from rich.console import Console




from STALK import Option_T1
from STALK.STALK_ACTIONS.EXIF_ACTIONS import Exif_Extract
from STALK.STALK_ACTIONS.OSIN_ACTIONS import Osint_Extract
from STALK.STALK_ACTIONS.INSTAGRAM_ACTIONS import Instagram_Extract




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

    SOSYAL MEDYA MERKEZİ                
                    
    Sahip Lisansı - 1889  |  Yazar - Vinnie  |  Sürüm - v3.0.0  [bold green]✠[/bold green][bold red]      
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():

    Console_Instance.print("[bold red]╠══    [/bold red][bold yellow]SERBEST BİLGİ TOPLAYICILAR[/bold yellow]\n")

    Console_Instance.print("    [bold white][S1][/bold white] [bold yellow]EXIF Aracı[/bold yellow]")
    Console_Instance.print("    [bold white][S2][/bold white] [bold yellow]OSINT Aracı[/bold yellow]\n")

    Console_Instance.print("[bold red]╠══    [/bold red][bold purple]INSTAGRAM BİLGİ TOPLAYICILAR[/bold purple]\n")

    Console_Instance.print("    [bold white][I1][/bold white] [bold purple]Instagram Stalk Aracı[/bold purple]\n\n")


    Console_Instance.print("    [bold white][B][/bold white] [bold red]Geri Dön[/bold red]")
    Console_Instance.print("    [bold white][E][/bold white] [bold red]Çıkış[/bold red]\n")
    
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

        if Choice == "s1":
            Exif_Extract.Main()

        if Choice == "s2":
            Osint_Extract.Main()

        if Choice == "ı1":
            Instagram_Extract.Main()

        if Choice == 'b':
            Option_T1.Main()

        if Choice == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış yapıldı")
            sys.exit(0)




if __name__ == "__main__":
    Main()
