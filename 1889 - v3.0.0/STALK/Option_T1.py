# v3.0.0 ✠




import os
import time
import sys
import importlib




from tqdm import tqdm
from rich.console import Console




from STALK.COPY_ACTIONS import Copy_Html_Css
from STALK.STALK_ACTIONS import SMM_Menu




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
       
    TAKİP MERKEZİ

    Sahip Lisansı - 1889  |  Yazar - Vinnie  |  Sürüm - v3.0.0  [bold green]✠[/bold green][bold red]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():

    Console_Instance.print("[bold red]╠══    [bold yellow]KOPYALAMA ARAÇLARI[/bold yellow][/bold red]\n")

    Console_Instance.print("    [bold white][ K1 ][/bold white]  [bold yellow]Website Kopyalama Aracı[/bold yellow]\n")

    Console_Instance.print("[bold red]╠══    [bold yellow]SOSYAL MEDYA ARAÇLARI[/bold yellow][/bold red]\n")

    Console_Instance.print("    [bold white][ S1 ][/bold white] [bold yellow]Sosyal Medya Merkezi[/bold yellow]\n\n")


    Console_Instance.print("    [bold white][ B ][/bold white]  [bold red]Ana Menüye Dön[/bold red]")
    Console_Instance.print("    [bold white][ E ][/bold white]  [bold red]Çıkış[/bold red]\n")
    
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

        if Choice == 'k1':
            Copy_Html_Css.Main()

        if Choice == 's1':
            SMM_Menu.Main()

        if Choice == 'b':
            Modul_1889.Main()

        if Choice == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış yapıldı")
            sys.exit(0)




if __name__ == "__main__":
    Main()
