# v3.0.0 ✠




import os
import json
import time
import sys
import requests
import exifread
import warnings




from typing import Any
from rich.console import Console
from rich.table import Table
from rich import box
from tqdm import tqdm
from contextlib import redirect_stderr
from io import StringIO




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
                  
    EXIF Aracı

    Kullanmadan önce anononimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                                      
╠═ YETENEKLER

    + Fotoğraftan Zamanı Sapta
    + Fotoğraftan Konumu Sapta
    + Fotoğraftan Cihazı Sapta
                                         
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
        "Bulunan veriler": {},
        "Bulunamayan veriler": [],
        "Hatalar": []
    }




def Convert_To_Degrees(Value):
    Degree = float(Value.values[0].num) / float(Value.values[0].den)
    Minute = float(Value.values[1].num) / float(Value.values[1].den)
    Second = float(Value.values[2].num) / float(Value.values[2].den)
    return Degree + (Minute / 60.0) + (Second / 3600.0)


def Get_Location_From_Coords(Latitude, Longitude):
    try:
        URL = f"https://nominatim.openstreetmap.org/reverse?lat={Latitude}&lon={Longitude}&format=json"

        Response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)

        return Response.json().get('display_name', 'Konum bulunamadı')
    
    except Exception:
        return "Konum alınamadı"


def Extract_Exif_Data(Image_Path):

    Found_Data = {}

    Not_Found = []

    Errors = []

    try:
        Fake_Stderr = StringIO()
        with redirect_stderr(Fake_Stderr):
            with open(Image_Path, 'rb') as File:
                Tags = exifread.process_file(File, details=False, debug=False)

        if not Tags:
            Errors.append("EXIF verisi bulunamadı")
            return None, Not_Found, Errors

        Found_Data["Dosya adı"] = os.path.basename(Image_Path)

        Found_Data["Dosya boyutu"] = f"{os.path.getsize(Image_Path)/1024:.2f} KB"

        Found_Data["Dosya yolu"] = Image_Path


        GPS_Latitude = Tags.get('GPS GPSLatitude')

        GPS_Longitude = Tags.get('GPS GPSLongitude')


        Latitude_Ref = Tags.get('GPS GPSLatitudeRef')

        Longitude_Ref = Tags.get('GPS GPSLongitudeRef')

        if GPS_Latitude and GPS_Longitude and Latitude_Ref and Longitude_Ref:
            Latitude = Convert_To_Degrees(GPS_Latitude)
            Longitude = Convert_To_Degrees(GPS_Longitude)
            
            if Latitude_Ref.values[0] == 'S':
                Latitude = -Latitude
            
            if Longitude_Ref.values[0] == 'W':
                Longitude = -Longitude
                
            Location = Get_Location_From_Coords(Latitude, Longitude)

            Found_Data["GPS Koordinat"] = f"{Latitude:.6f}, {Longitude:.6f}"

            Found_Data["Konum"] = Location

        else:
            Not_Found.append("GPS bilgisi")

        for Tag in Tags:
            Key = str(Tag)
            Value = str(Tags[Tag])
            if Key not in ['MakerNote', 'Thumbnail', 'JPEGThumbnail']:
                if Key.startswith('GPS'):
                    continue
                Found_Data[Key] = Value

        return Found_Data, Not_Found, Errors

    except Exception:
        Errors.append("Dosya okunamadı veya desteklenmeyen format")
        return None, Not_Found, Errors




def Create_Unified_Report(Image_Name, Found_Data, Not_Found, Errors):
    
    Table_Report = Table(
        show_header=True, 
        header_style="bold red", 
        border_style="red",
        title="EXIF Analiz Raporu", 
        title_style="bold red",
        box=box.HEAVY_HEAD,
        min_width=80
    )

    Table_Report.add_column("Kategori", style="bold yellow", justify="left")
    Table_Report.add_column("Bilgi", style="white", justify="left")

    if Found_Data:
        Table_Report.add_section()
        for Key, Value in Found_Data.items():
            Table_Report.add_row("Bulunan veriler", f"[bold cyan]{Key}[/bold cyan] {Value}")

    if Not_Found:
        Table_Report.add_section()
        for Item in Not_Found:
            Table_Report.add_row("[bold red]Bulunamayan Veri[/bold red]", Item)

    if Errors:
        Table_Report.add_section()
        for Error in Errors:
            Table_Report.add_row("[bold red]Hata[/bold red]", Error)

    Console_Instance.print(Table_Report)

    time.sleep(2)




def Save_Report_To_Json(Image_Name):
    try:

        Root_Dir = "EXIF_REPORT"
        
        Report_Dir = os.path.join(Root_Dir, Image_Name.split('.')[0])

        Filename = "Exif_Results.json"
        
        os.makedirs(Report_Dir, exist_ok=True)

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

        Input_Path = Console_Instance.input("[bold red]╠═ Fotoğraf Yolu Girin [/bold red]").strip().strip('"').strip("'")

        Console_Instance.print()

        if Input_Path.lower() == 'b':
            SMM_Menu.Main()
            continue
        if Input_Path.lower() == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)

        if not Input_Path or not os.path.isfile(Input_Path):
            Console_Instance.print("[bold red]Geçersiz dosya yolu[/bold red]")
            time.sleep(1)
            continue

        Reset_Report()

        Report_Data["Girdi"] = Input_Path

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print("\n[bold green]Fotoğraf analiz ediliyor[/bold green]\n")
        
        Console_Instance.print()

        Found_Data, Not_Found, Errors = Extract_Exif_Data(Input_Path)

        if Found_Data is None and Errors:
             Console_Instance.print(f"[bold red]{Errors[0]}[/bold red]")
             Console_Instance.input("\n[bold red]Devam etmek için Enter[/bold red]")
             continue

        Report_Data["Bulunan veriler"] = Found_Data or {}
        Report_Data["Bulunamayan veriler"] = Not_Found
        Report_Data["Hatalar"] = Errors

        Image_Name = os.path.basename(Input_Path).split('.')[0]
        Create_Unified_Report(Image_Name, Found_Data or {}, Not_Found, Errors)
        Save_Report_To_Json(Image_Name)

        Console_Instance.input("\n[bold red]Raporları kontrol edin[/bold red]")




if __name__ == "__main__":
    Main()
