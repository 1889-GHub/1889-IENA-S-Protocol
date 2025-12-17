# v3.0.0 ✠




import os
import sys
import time
import json
import random
import warnings




from typing import Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich import box
from curl_cffi import requests as cffi_requests




from STALK import Option_T1




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
                  
    Website Kopyalama Aracı

    Kullanmadan önce anononimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                                      
╠═ NOT

    + Linkten Tıpa Tıp Site Kopyalar  
                                             
╠═ YETKİ - [bold blue]Normal[/bold blue]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():

    Console_Instance.print("    [bold white][B] [bold red]Geri[/bold red][/bold white]")
    Console_Instance.print("    [bold white][E] [bold red]Çıkış[/bold red][/bold white]\n")

    Console_Instance.print("[bold red]╚═══════════════════════════════════════════════════════════════════════╝[/bold red]\n")




def Reset_Report():
    global Report_Data
    Report_Data = {
        "Girdi": "",
        "Site bilgisi": {},
        "İndirilenler": {},
        "HTML analizi": {},
        "Hatalar": []
    }




def Make_Directory(Directory_Name):
    if not os.path.exists(Directory_Name):
        os.makedirs(Directory_Name)




def Save_File(Content, Filename):
    try:
        with open(Filename, 'w', encoding='utf-8') as File:
            File.write(Content)
        return True
    except Exception:
        return False




def Download_Css_File(Url, Folder):
    try:

        time.sleep(random.uniform(0.5, 1.5))

        Response = cffi_requests.get(Url, timeout=15, verify=False, impersonate="chrome")

        Response.raise_for_status()

        Filename = os.path.basename(urlparse(Url).path)

        if not Filename or Filename.endswith('/'):
            Filename = "style.css"
        
        if not Filename.endswith('.css'):
            Filename = f"{Filename}.css"

        Full_Path = os.path.join(Folder, Filename)

        with open(Full_Path, 'w', encoding='utf-8') as File:
            File.write(Response.text)
        return Filename
    
    except Exception:
        return None




def Process_Website_Data(Url):

    Site_Data = {}

    Download_Data = {}

    Html_Stats = {}

    Errors = []
    
    try:
        time.sleep(random.uniform(1.0, 2.0))
        Session = cffi_requests.Session()
        Response = Session.get(Url, timeout=20, verify=False, impersonate="chrome", allow_redirects=True)
        Response.raise_for_status()

        Parsed_Url = urlparse(Url)

        Site_Name = Parsed_Url.netloc.replace(':', '_').replace('.', '_')

        Site_Data["Domain"] = Parsed_Url.netloc

        Site_Data["Protokol"] = Parsed_Url.scheme

        Site_Data["Durum kodu"] = str(Response.status_code)

        Site_Data["İçerik tipi"] = Response.headers.get('Content-Type', 'Bilinmiyor')

        Site_Data["HTML boyutu"] = f"{len(Response.text) / 1024:.2f} KB"


        Root_Dir = "COPIED_WEBSITE_REPORT"

        Site_Folder_Path = os.path.join(Root_Dir, Site_Name)

        Make_Directory(Site_Folder_Path)

        Soup = BeautifulSoup(Response.text, 'html.parser')

        Html_Filename = os.path.join(Site_Folder_Path, 'index.html')
        
        if Save_File(Response.text, Html_Filename):
            Download_Data["HTML dosyası"] = "Kaydedildi (index.html)"
        
        else:
            Errors.append("HTML dosyası kaydedilemedi")

        Css_Links = Soup.find_all('link', rel='stylesheet')

        Downloaded_Css_List = []
        
        if Css_Links:
            for Link in Css_Links:
                Href = Link.get('href')
                if Href and isinstance(Href, str):
                    Full_Url = urljoin(Url, Href)
                    Saved_Name = Download_Css_File(Full_Url, Site_Folder_Path)
                    if Saved_Name:
                        Downloaded_Css_List.append(Saved_Name)
            
            Download_Data["CSS dosya sayısı"] = str(len(Downloaded_Css_List))
            Download_Data["CSS listesi"] = ", ".join(Downloaded_Css_List) if Downloaded_Css_List else "İndirilemedi"
        
        else:
            Download_Data["CSS durumu"] = "Harici CSS bulunamadı"

        Title = Soup.find('title')

        Html_Stats["Başlık"] = Title.get_text().strip()[:50] if Title else "Yok"

        Html_Stats["Meta tag"] = str(len(Soup.find_all('meta')))

        Html_Stats["Script"] = str(len(Soup.find_all('script')))

        Html_Stats["Görsel"] = str(len(Soup.find_all('img')))

        Html_Stats["Link"] = str(len(Soup.find_all('a')))


        return Site_Name, Site_Data, Download_Data, Html_Stats, Errors

    except Exception as Exception_Object:
        Errors.append(f"Bağlantı hatası: {str(Exception_Object)}")
        return None, {}, {}, {}, Errors




def Create_Unified_Report(Site_Name, Site_Data, Download_Data, Html_Stats, Errors):

    Table_Report = Table(
        show_header=True, 
        header_style="bold red", 
        border_style="red",
        title="Website Kopyalama Raporu", 
        title_style="bold red",
        box=box.HEAVY_HEAD,
        min_width=80
    )

    Table_Report.add_column("Kategori", style="bold yellow", justify="left")
    Table_Report.add_column("Bilgi", style="white", justify="left")

    if Site_Data:
        Table_Report.add_section()
        for Key, Value in Site_Data.items():
            Table_Report.add_row("Site bilgisi", f"[bold cyan]{Key}[/bold cyan] {Value}")

    if Download_Data:
        Table_Report.add_section()
        for Key, Value in Download_Data.items():
            Display_Value = Value[:80] + "..." if len(Value) > 80 else Value
            Table_Report.add_row("İndirilenler", f"[bold cyan]{Key}[/bold cyan] {Display_Value}")

    if Html_Stats:
        Table_Report.add_section()
        for Key, Value in Html_Stats.items():
            Table_Report.add_row("HTML analizi", f"[bold cyan]{Key}[/bold cyan] {Value}")

    if Errors:
        Table_Report.add_section()
        for Error in Errors:
            Table_Report.add_row("[bold red]Hata[/bold red]", Error)

    Console_Instance.print(Table_Report)
    time.sleep(2)




def Save_Report_To_Json(Site_Name):
    try:

        Root_Dir = "COPIED_WEBSITE_REPORT"

        Report_Dir = os.path.join(Root_Dir, Site_Name)

        Filename = "Copy_Html_Css_Results.json"
        
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

        Input_Url = Console_Instance.input("[bold red]╠═ URL Yapıştır [/bold red]").strip()

        Console_Instance.print()

        if Input_Url.lower() == 'b':
            Option_T1.Main()
            continue
    
        if Input_Url.lower() == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)

        if not Input_Url:
            Console_Instance.print("[bold red]Geçersiz URL[/bold red]")
            time.sleep(1)
            continue
        
        if not Input_Url.startswith('http://') and not Input_Url.startswith('https://'):
            Console_Instance.print("[bold red]Geçersiz URL formatı[/bold red]")
            time.sleep(1)
            continue

        Reset_Report()

        Report_Data["Girdi"] = Input_Url

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print("\n[bold green]Web sitesi kopyalanıyor[/bold green]\n")
        
        Console_Instance.print()

        Site_Name, Site_Data, Download_Data, Html_Stats, Errors = Process_Website_Data(Input_Url)

        if not Site_Name and Errors:
            Console_Instance.print(f"[bold red]{Errors[0]}[/bold red]")
            Console_Instance.input("\n[bold red]Devam etmek için Enter[/bold red]")
            continue

        Report_Data["Site bilgisi"] = Site_Data
        Report_Data["İndirilenler"] = Download_Data
        Report_Data["HTML analizi"] = Html_Stats
        Report_Data["Hatalar"] = Errors

        Create_Unified_Report(Site_Name, Site_Data, Download_Data, Html_Stats, Errors)
        Save_Report_To_Json(Site_Name)

        Console_Instance.input("\n[bold red]Raporları kontrol edin[/bold red]")




if __name__ == "__main__":
    Main()
