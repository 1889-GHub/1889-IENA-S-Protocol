# v3.0.0 ✠




import os
import shutil
from rich.console import Console




Console_Instance = Console()




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Clear_Pycache():
    for Dirpath, Dirnames, Filenames in os.walk('.'):
        if '__pycache__' in Dirnames:
            Pycache_Path = os.path.join(Dirpath, '__pycache__')
            try:
                shutil.rmtree(Pycache_Path)
            except Exception:
                pass




if __name__ == "__main__":
    Clear_Terminal()
    Clear_Pycache()
    Console_Instance.print("[bold red]╔═══════════════════════════════════════════════════════════════════════╗[/bold red]")
    Console_Instance.print("")    
    Console_Instance.print("[bold white] Önbellekler Temizlendi[/bold white]")
    Console_Instance.print("")  
    Console_Instance.print("[bold red]╚═══════════════════════════════════════════════════════════════════════╝[/bold red]")
