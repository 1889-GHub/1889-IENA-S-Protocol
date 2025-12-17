# v3.0.0 ✠




import os
import socket
import ssl
import json




from rich.console import Console
from rich.table import Table




Console_Instance = Console()




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Display_Banner():
    Console_Instance.print(r"""
[bold red]╔═══════════════════════════════════════════════════════════════════════╗

    ┓┏┓┏┓┏┓
    ┃┣┫┣┫┗┫
    ┻┗┛┗┛┗┛
                           
    S PROTOCOL - Profil           
                           
    Sahip Lisansı - 1889  |  Yazar - Vinnie  |  Sürüm - v3.0.0  [bold green]✠[/bold green]

╠═ DURUM - [bold green]BAĞLI[/bold green]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Profile_Table(Profile_Data):
    
    Table_Structure = Table(
        show_header=False,
        box=None
    )
    
    Table_Structure.add_column("Key", style="bold red", justify="left")
    Table_Structure.add_column("Value", style="bold white", justify="left")

    Normal_Data = Profile_Data.get("Normal", {})
    Data_1889 = Profile_Data.get("1889", {})

    Table_Structure.add_row("Kullanıcı Adı", Normal_Data.get("Username", "Bilinmiyor"))
    Table_Structure.add_row("Rol", Normal_Data.get("Role", "Bilinmiyor"))
    Table_Structure.add_row("Hesap Durumu", Normal_Data.get("Account State", "Bilinmiyor"))
    Table_Structure.add_row("Kayıt Tarihi", Normal_Data.get("Created_At", "Bilinmiyor"))
    

    Permissions = Profile_Data.get("Permissions", {})

    Chat_Status = "[green]AÇIK[/green]" if Permissions.get("Chat") else "[red]KAPALI[/red]"
    File_Status = "[green]AÇIK[/green]" if Permissions.get("File_transfer") else "[red]KAPALI[/red]"

    Table_Structure.add_row("Sohbet İzni", Chat_Status)
    Table_Structure.add_row("Dosya Transfer İzni", File_Status)

    Table_Structure.add_row("1889 Sınıfı", Data_1889.get("1889 Class", "Yok"))
    Table_Structure.add_row("1889 Skor", Data_1889.get("1889 Score", "Yok"))
    Table_Structure.add_row("1889 Rütbe", Data_1889.get("1889 Rank", "Yok"))
    
    Console_Instance.print(Table_Structure)

    Console_Instance.print("\n[bold red]╠═ BİO [/bold red]\n")

    Console_Instance.print(f"[bold white]{Data_1889.get('1889 Bio', 'Boş')}[/bold white]\n")

    Console_Instance.print("[bold red]╚═══════════════════════════════════════════════════════════════════════╝[/bold red]\n")




def Load_Client_Config():

    Config_Path = "Client_Config.json"
    
    if not os.path.exists(Config_Path):
        Console_Instance.print("\n[bold red]Client_Config.json adlı dosyayı ne yaptın? Eğer sildiysen onu geri indir o silinemez[/bold red]")
        return None

    try:
        with open(Config_Path, 'r', encoding='utf-8') as F:
            return json.load(F)
    
    except Exception as Exception_Object:
        Console_Instance.print(f"\n[bold red]Config yüklenemedi {Exception_Object}[/bold red]")
        return None




def Fetch_Profile_Data(Connection_Data):
    
    Config = Load_Client_Config()

    if not Config:
        return None

    Client_Cert = Config["Client_Cert_Path"]
    Client_Key = Config["Client_Key_Path"]
    CA_Cert = Config["CA_Cert_Path"]

    if not os.path.exists(Client_Cert) or not os.path.exists(Client_Key):

        Console_Instance.print("\n[bold red]Sertifikalar eksik[/bold red]")
        return None

    SSL_Context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    SSL_Context.verify_mode = ssl.CERT_REQUIRED
    SSL_Context.load_verify_locations(CA_Cert)
    SSL_Context.load_cert_chain(certfile=Client_Cert, keyfile=Client_Key)

    Base_Socket = None
    Secure_Socket = None

    try:

        Base_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Base_Socket.settimeout(5)

        Secure_Socket = SSL_Context.wrap_socket(
            Base_Socket, 
            server_hostname=Connection_Data['host']
        )
        
        Secure_Socket.connect((Connection_Data['host'], Connection_Data['port']))
        
        Request_Message = f"13|{Connection_Data['session_token']}\n"

        Secure_Socket.sendall(Request_Message.encode('utf-8'))
        
        Response = Secure_Socket.recv(8192).decode('utf-8').strip()
        
        Parts = Response.split("|", 2)
        
        if len(Parts) >= 2 and Parts[0] == "13" and Parts[1] == "OK":
            
            Profile_JSON = Parts[2]
            
            try:
                Profile_Data = json.loads(Profile_JSON)
                return Profile_Data

            except json.JSONDecodeError:
                Console_Instance.print("\n[bold red]Profil verisi çözümlenemedi (JSON Hatası)[/bold red]")
                return None

        else:
            Console_Instance.print("\n[bold red]Profil verisi alınamadı (Sunucu Hatası)[/bold red]")
            return None

    except ConnectionRefusedError:
        Console_Instance.print("\n[bold red]Sunucu kapalı[/bold red]")
        return None
    
    except socket.timeout:
        Console_Instance.print("\n[bold red]Sunucu zaman aşımına uğradı[/bold red]")
        return None
    
    except ssl.SSLError as Exception_Object:
        Console_Instance.print(f"\n[bold red]SSL hatası {Exception_Object}[/bold red]")
        return None
    
    except Exception as Exception_Object:
        Console_Instance.print(f"\n[bold red]Genel hata {Exception_Object}[/bold red]")
        return None
    
    finally:

        try:
            if Secure_Socket:
                Secure_Socket.close()
        
        except Exception:
            pass
    
        try:
            if Base_Socket:
                Base_Socket.close()
        
        except Exception:
            pass




def Main(Connection_Data=None):

    while True:

        Clear_Terminal()

        Display_Banner()

        if not Connection_Data or not Connection_Data.get("session_token"):

            Console_Instance.print("\n[bold red]Oturum belirteci bulunamadı[/bold red]")
            
            Console_Instance.input("\n[bold red]Ana Menüye Dönmek İçin Enter[/bold red]").strip()
            
            break

        Profile_Data = Fetch_Profile_Data(Connection_Data)

        if Profile_Data is None:

            Console_Instance.print("\n[bold red]Profil verisi alınamadı[/bold red]")

            Console_Instance.input("\n[bold red]Ana Menüye Dönmek İçin Enter[/bold red]").strip()

            break

        Console_Instance.print()
        
        Display_Profile_Table(Profile_Data)
        
        Console_Instance.input("[bold red]Ana Menüye Dönmek İçin Enter[/bold red]").strip()

        break




if __name__ == "__main__":
    Main()
