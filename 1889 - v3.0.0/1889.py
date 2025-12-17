# v3.0.0 ✠




import os
import time
import sys




from tqdm import tqdm
from rich.console import Console



from PROTOCOL.S import S_Login          # v3.0.0 ✠
from SECURITY import Option_G1          # v3.0.0 ✠
from STALK import Option_T1             # v3.0.0 ✠
from NETHUNTER import Option_H1         # v3.0.0 ✠




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
       
    1889 I.E.N.A / S PROTOCOL
                            
    Sahip Lisansı : 1889  |  Yazar : Vinnie  |  Sürüm : v3.0.0  [bold green]✠[/bold green][bold red]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():

    Console_Instance.print("[bold red]╠══    [bold blue]GÜVENLİK[/bold blue][/bold red]\n")

    Console_Instance.print("    [bold white][ G1 ][/bold white] [bold blue]Güvenlik Merkezi[/bold blue]\n")

    Console_Instance.print("[bold red]╠══    [bold yellow]TAKİP[/bold yellow][/bold red]\n")

    Console_Instance.print("    [bold white][ T1 ][/bold white] [bold yellow]Takip Merkezi[/bold yellow]\n")

    Console_Instance.print("[bold red]╠══    [bold green]NETHUNTER[/bold green][/bold red]\n")

    Console_Instance.print("    [bold white][ H1 ][/bold white] [bold green]Nethunter Merkezi[/bold green]\n\n")


    Console_Instance.print("[bold red]╠═══════════════════════════════════════════════════════════════════════╣\n")
    
    Console_Instance.print("    [bold white][ S ][/bold white]  [bold red]S Protokolüne Giriş Yap[/bold red]\n")

    Console_Instance.print("    [bold white][ E ][/bold white]  [bold red]İstemciden Çık[/bold red]\n")

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
            Option_G1.Main()
        
        if Choice == 't1':
            Option_T1.Main()
        
        if Choice == 'h1':            
            Option_H1.Main()

        if Choice == 's':
            S_Login.Main()
        
        if Choice == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)




if __name__ == "__main__":
    Main()
