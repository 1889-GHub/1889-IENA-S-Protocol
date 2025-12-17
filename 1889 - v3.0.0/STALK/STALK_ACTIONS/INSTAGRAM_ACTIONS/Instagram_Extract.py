# v3.0.0 ✠




import os
import json
import time
import sys
import requests
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
                  
    Instagram Stalk Aracı

    Kullanmadan önce anononimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                                      
╠═ YETENEKLER

    + Instagram Uzaktan Stalk
    + Instagram Profil Fotoğrafını indir
                                             
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
        "Hesap Bilgisi": {},
        "İstatistikler": {},
        "İndirilenler": {},
        "Hatalar": []
    }




def Make_Directory(Directory_Name):
    if not os.path.exists(Directory_Name):
        os.makedirs(Directory_Name)




def Download_Profile_Picture(Url, Folder):

    try:

        time.sleep(random.uniform(0.5, 1.5))
        Http_Response = requests.get(Url, timeout=15)
        Http_Response.raise_for_status()
        
        Filename = "Profil_Fotografi_FullHD.jpg"
        Full_Path = os.path.join(Folder, Filename)
        
        with open(Full_Path, 'wb') as Output_File:
            Output_File.write(Http_Response.content)
        return Filename
    
    except Exception:
        return None




def Process_Instagram_Data(Username):

    Account_Data = {}

    Stats_Data = {}

    Download_Data = {}

    Errors = []
    
    try:
        time.sleep(random.uniform(1.0, 2.0))
        
        Headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            'X-IG-App-ID': '936619743392459',
        }
        
        Url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={Username}"
        Http_Response = requests.get(Url, headers=Headers, timeout=15)
        
        if Http_Response.status_code != 200:
            return Process_Instagram_Data_Alternative(Username)
        
        Api_Data = Http_Response.json()

        User_Profile = Api_Data.get('data', {}).get('user')
        
        if not User_Profile:
            return Process_Instagram_Data_Alternative(Username)

        Account_Data["Kullanıcı adı"] = User_Profile.get('username', Username)

        Account_Data["Tam isim"] = User_Profile.get('full_name', 'Belirtilmemiş')

        Account_Data["Biyografi"] = User_Profile.get('biography', 'Boş')

        Account_Data["Hesap türü"] = "İşletme" if User_Profile.get('is_business_account') else "Kişisel"

        Account_Data["Doğrulanmış"] = "Evet" if User_Profile.get('is_verified') else "Hayır"

        Account_Data["Özel hesap"] = "Evet" if User_Profile.get('is_private') else "Hayır"

        Account_Data["Harici URL"] = User_Profile.get('external_url', 'Yok')

        Account_Data["Profil URL"] = f"https://instagram.com/{Username}"


        Stats_Data["Takipçi sayısı"] = f"{User_Profile.get('edge_followed_by', {}).get('count', 0):,}"

        Stats_Data["Takip edilen"] = f"{User_Profile.get('edge_follow', {}).get('count', 0):,}"

        Stats_Data["Gönderi sayısı"] = f"{User_Profile.get('edge_owner_to_timeline_media', {}).get('count', 0):,}"

        if User_Profile.get('is_business_account'):
            Stats_Data["Kategori"] = User_Profile.get('category_name', 'Belirtilmemiş')

        Profile_Pic_Url = User_Profile.get('profile_pic_url_hd') or User_Profile.get('profile_pic_url')

        User_Folder = f"INSTAGRAM_{Username}"

        Root_Dir = "INSTAGRAM_REPORT"

        Full_Path = os.path.join(Root_Dir, User_Folder)
        Make_Directory(Full_Path)

        if Profile_Pic_Url:
            Saved_Name = Download_Profile_Picture(Profile_Pic_Url, Full_Path)
            if Saved_Name:
                Download_Data["Profil Fotoğrafı"] = f"İndirildi → {Saved_Name}"
                Download_Data["Klasör"] = Full_Path

            else:
                Download_Data["Profil Fotoğrafı"] = "İndirilemedi"

        else:
            Download_Data["Profil Fotoğrafı"] = "Bulunamadı"

        return User_Folder, Account_Data, Stats_Data, Download_Data, Errors

    except Exception as Exception_Object:
        Errors.append(f"Bağlantı hatası: {str(Exception_Object)}")
        return Process_Instagram_Data_Alternative(Username)

def Process_Instagram_Data_Alternative(Username):

    Errors = []

    try:
        Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        Http_Response = requests.get(f"https://www.instagram.com/{Username}/", headers=Headers, timeout=10)
        
        if Http_Response.status_code == 404:
            Errors.append("Hesap bulunamadı")
            return None, {}, {}, {}, Errors

        Match_Object = re.search(r'window\._sharedData = ({.*?});', Http_Response.text)
        if not Match_Object:
            Errors.append("Veri alınamadı")
            return None, {}, {}, {}, Errors

        Shared_Data = json.loads(Match_Object.group(1))
        User_Profile = Shared_Data.get('entry_data', {}).get('ProfilePage', [{}])[0].get('graphql', {}).get('user', {})

        if not User_Profile:
            Errors.append("Kullanıcı bilgisi yok")
            return None, {}, {}, {}, Errors

        Account_Data = {
            "Kullanıcı adı": Username,
            "Tam isim": User_Profile.get('full_name', 'Belirtilmemiş'),
            "Biyografi": User_Profile.get('biography', 'Boş'),
            "Özel hesap": "Evet" if User_Profile.get('is_private') else "Hayır",
            "Doğrulanmış": "Evet" if User_Profile.get('is_verified') else "Hayır",
            "Profil URL": f"https://instagram.com/{Username}"
        }

        Stats_Data = {
            "Takipçi sayısı": f"{User_Profile.get('edge_followed_by', {}).get('count', 0):,}",
            "Takip edilen": f"{User_Profile.get('edge_follow', {}).get('count', 0):,}",
            "Gönderi sayısı": f"{User_Profile.get('edge_owner_to_timeline_media', {}).get('count', 0):,}"
        }

        Download_Data = {"Not": "Alternatif yöntemde fotoğraf indirilmedi"}

        User_Folder = f"INSTAGRAM_{Username}"
        return User_Folder, Account_Data, Stats_Data, Download_Data, Errors

    except Exception:
        Errors.append("Alternatif yöntem başarısız")
        return None, {}, {}, {}, Errors

def Create_Unified_Report(User_Folder, Account_Data, Stats_Data, Download_Data, Errors):

    Table_Report = Table(
        show_header=True, 
        header_style="bold red", 
        border_style="red",
        title="Instagram Analiz Raporu", 
        title_style="bold red",
        box=box.HEAVY_HEAD,
        min_width=80
    )

    Table_Report.add_column("Kategori", style="bold yellow", justify="left")
    Table_Report.add_column("Bilgi", style="white", justify="left")

    if Account_Data:
        Table_Report.add_section()
        for Key, Value in Account_Data.items():
            Table_Report.add_row("Hesap Bilgisi", f"[bold cyan]{Key}[/bold cyan] {Value}")

    if Stats_Data:
        Table_Report.add_section()
        for Key, Value in Stats_Data.items():
            Table_Report.add_row("İstatistikler", f"[bold cyan]{Key}[/bold cyan] {Value}")

    if Errors:
        Table_Report.add_section()
        for Error_Message in Errors:
            Table_Report.add_row("[bold red]Hata[/bold red]", Error_Message)

    Console_Instance.print(Table_Report)
    time.sleep(2)




def Save_Report_To_Json(User_Folder):

    try:
        
        Root_Dir = "INSTAGRAM_REPORT"

        Report_Dir = os.path.join(Root_Dir, User_Folder)

        Filename = "Instagram_Results.json"
        
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

        Input_Username = Console_Instance.input("[bold red]╠═ Instagram Kullanıcı Adı Girin [/bold red]").strip().replace('@', '')

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

        Console_Instance.print("\n[bold green]Kullanıcı analiz ediliyor[/bold green]\n")
        
        Console_Instance.print()

        User_Folder, Account_Data, Stats_Data, Download_Data, Errors = Process_Instagram_Data(Input_Username)

        if not User_Folder and Errors:
             Console_Instance.print(f"[bold red]{Errors[0]}[/bold red]")
             Console_Instance.input("\n[bold red]Devam etmek için Enter[/bold red]")
             continue

        Report_Data["Hesap Bilgisi"] = Account_Data
        Report_Data["İstatistikler"] = Stats_Data
        Report_Data["İndirilenler"] = Download_Data
        Report_Data["Hatalar"] = Errors

        Create_Unified_Report(User_Folder, Account_Data, Stats_Data, Download_Data, Errors)
        Save_Report_To_Json(User_Folder)

        Console_Instance.input("\n[bold red]Dosyaları kontrol edin[/bold red]")




if __name__ == "__main__":
    Main()
