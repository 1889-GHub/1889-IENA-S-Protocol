# v3.0.0 ✠




import os
import json
import time
import sys
import re
import random
import warnings




from typing import Any
from rich.console import Console
from rich.table import Table
from rich import box
from tqdm import tqdm




from STALK.STALK_ACTIONS import SMM_Menu




Console_Instance = Console()
warnings.simplefilter('ignore')




Report_Data: dict[str, Any] = {}




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

    Sahip Lisansı - 1889  |  Yazar - Vinnie  |  Sürüm - v3.0.0  [bold green]✠[/bold green][bold red]
                  
    OSINT Aracı

    Kullanmadan önce anononimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                                      
╠═ YETENEKLER

    + Yan Profilleri Arayabilir 
                                             
╠═ YETKİ - [bold blue]Normal[/bold blue]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():
    Console_Instance.print("    [bold white][B] [bold red]Geri[/bold red][/bold white]")
    Console_Instance.print("    [bold white][E] [bold red]Çıkış[/bold red][/bold white]\n")
    Console_Instance.print("[bold red]╚═══════════════════════════════════════════════════════════════════════╝[/bold red]\n")




def Reset_Report():

    global Report_Data

    Report_Data = {
        "Hedef Kullanıcı": "",
        "Olası Profiller": {},
        "Hatalar": []
    }




def Make_Directory(Directory_Name):
    if not os.path.exists(Directory_Name):
        os.makedirs(Directory_Name)




def Format_Input(Input_Str: str, Platform: str) -> str:
    try:

        Cleaned_Input = Input_Str.strip()

        if Platform == "GitHub":
            Cleaned_Input = Cleaned_Input.lower()
            Cleaned_Input = re.sub(r'[^a-z0-9-]', '', Cleaned_Input)
            Cleaned_Input = re.sub(r'-{2,}', '-', Cleaned_Input).strip('-')
            return Cleaned_Input[:39]
        
        elif Platform in ("Twitter", "X"):
            return re.sub(r'[^A-Za-z0-9_]', '', Cleaned_Input)[:15]
        
        elif Platform == "Instagram":
            Cleaned_Input = re.sub(r'[^A-Za-z0-9._]', '', Cleaned_Input)
            Cleaned_Input = re.sub(r'\.{2,}', '.', Cleaned_Input).strip('.')
            return Cleaned_Input[:30]
        
        elif Platform == "Facebook":
            return re.sub(r'[^A-Za-z0-9.]', '', Cleaned_Input)[:50]
        
        elif Platform == "LinkedIn":
            return re.sub(r'[^A-Za-z0-9-]', '', Cleaned_Input)[:100]
        
        elif Platform == "Reddit":
            return re.sub(r'[^A-Za-z0-9_-]', '', Cleaned_Input)[:20]
        
        elif Platform == "TikTok":
            Cleaned_Input = re.sub(r'[^A-Za-z0-9._]', '', Cleaned_Input)
            if Cleaned_Input.endswith('.'):
                Cleaned_Input = Cleaned_Input[:-1]
            return Cleaned_Input[:24]
        
        elif Platform == "Pinterest":
            return re.sub(r'[^A-Za-z0-9]', '', Cleaned_Input)[:30]
        
        elif Platform == "Snapchat":
            Cleaned_Input = re.sub(r'[^A-Za-z0-9._-]', '', Cleaned_Input)
            Cleaned_Input = re.sub(r'^[^A-Za-z]+|[^A-Za-z0-9]+$', '', Cleaned_Input)
            return Cleaned_Input[:15]
        
        elif Platform == "YouTube":
            Cleaned_Input = re.sub(r'[^0-9A-Za-z_\-\.\·]', '', Cleaned_Input)
            Cleaned_Input = re.sub(r'^[._\-·]+|[._\-·]+$', '', Cleaned_Input)
            return Cleaned_Input[:30]
        
        elif Platform == "Telegram":
            return re.sub(r'[^A-Za-z0-9_]', '', Cleaned_Input)[:32]
        
        elif Platform == "Medium":
            Cleaned_Input = Cleaned_Input.lower()
            return re.sub(r'[^a-z0-9_-]', '', Cleaned_Input)[:50]
        
        else:
            return re.sub(r'[^\w\-\.]', '', Cleaned_Input)
        
    except Exception:
        return Input_Str




def Process_Osint_Data(Username):

    Possible_Profiles = {}

    Errors = []
    
    Platforms = {
        "Twitter":   "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}",
        "Facebook":  "https://www.facebook.com/{}",
        "LinkedIn":  "https://www.linkedin.com/in/{}",
        "GitHub":    "https://github.com/{}",
        "Reddit":    "https://www.reddit.com/user/{}",
        "TikTok":    "https://www.tiktok.com/@{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Snapchat":  "https://www.snapchat.com/add/{}",
        "YouTube":   "https://www.youtube.com/user/{}",
        "Telegram":  "https://t.me/{}",
        "Medium":    "https://medium.com/@{}",
        "Flickr":    "https://www.flickr.com/people/{}"
    }

    try:
        time.sleep(random.uniform(1.0, 2.0))

        for Platform, Template_Url in Platforms.items():
            Formatted_Username = Format_Input(Username, Platform)
            Profile_Url = Template_Url.format(Formatted_Username)
            Possible_Profiles[Platform] = Profile_Url

        User_Folder = f"OSINT_{Username}"

        Root_Dir = "OSINT_REPORT"

        Full_Path = os.path.join(Root_Dir, User_Folder)

        Make_Directory(Full_Path)

        return User_Folder, Possible_Profiles, Errors

    except Exception as Exception_Object:
        Errors.append(f"Genel hata: {str(Exception_Object)}")
        return None, {}, Errors




def Create_Unified_Report(User_Folder, Possible_Profiles, Errors):
    
    Table_Report = Table(
        show_header=True,
        header_style="bold red",
        border_style="red",
        title="OSINT",
        title_style="bold red",
        box=box.HEAVY_HEAD,
        min_width=80
    )

    Table_Report.add_column("Platform", style="bold cyan", justify="left")
    Table_Report.add_column("Link", style="white", justify="left")

    for Platform, Profile_Url in Possible_Profiles.items():
        short_url = Profile_Url if len(Profile_Url) <= 80 else Profile_Url[:77] + "..."
        Table_Report.add_row(Platform, short_url)

    if Errors:
        Table_Report.add_section()
        for Error in Errors:
            Table_Report.add_row("[bold red]Hata[/bold red]", Error)

    Console_Instance.print(Table_Report)

    time.sleep(2)




def Save_Report_To_Json(User_Folder):

    try:
        Root_Dir = "OSINT_REPORT"
        Report_Dir = os.path.join(Root_Dir, User_Folder)
        Filename = "Osint_Results.json"
        
        Make_Directory(Report_Dir)

        Filepath = os.path.join(Report_Dir, Filename)
        
        Report_Data["Zaman damgası"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(Filepath, 'w', encoding='utf-8') as Output_File:
            json.dump(Report_Data, Output_File, ensure_ascii=False, indent=4)
            
        Console_Instance.print(f"\n[bold green]Rapor kaydedildi[/bold green] [white]{Filepath}[/white]")

    except Exception:
        pass




def Main():

    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print()

        Display_Menu()

        Input_Username = Console_Instance.input("[bold red]╠═ Kullanıcı Adı Girin [/bold red]").strip()

        Console_Instance.print()

        if Input_Username.lower() == 'b':
            SMM_Menu.Main()
            continue

        if Input_Username.lower() == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)

        if not Input_Username:
            continue

        Reset_Report()

        Report_Data["Hedef Kullanıcı"] = Input_Username

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print("\n[bold green]Olası profiller hazırlanıyor[/bold green]\n")
        
        Console_Instance.print()

        User_Folder, Possible_Profiles, Errors = Process_Osint_Data(Input_Username)

        if not User_Folder and Errors:
            Console_Instance.print(f"[bold red]{Errors[0]}[/bold red]")
            Console_Instance.input("\n[bold red]Devam etmek için Enter[/bold red]")
            continue

        Report_Data["Olası Profiller"] = Possible_Profiles
        Report_Data["Hatalar"] = Errors

        Create_Unified_Report(User_Folder, Possible_Profiles, Errors)
        Save_Report_To_Json(User_Folder)

        Console_Instance.input("\n[bold red]Dosyaları kontrol edin[/bold red]")




if __name__ == "__main__":
    Main()
