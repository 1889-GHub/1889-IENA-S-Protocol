@ECHO OFF


cls


ruff check "1889 - v3.0.0\1889.py"
ruff check "1889 - v3.0.0\STALK\Option_T1.py"
ruff check "1889 - v3.0.0\STALK\STALK_ACTIONS\SMM_Menu.py"
ruff check "1889 - v3.0.0\STALK\STALK_ACTIONS\OSIN_ACTIONS\Osint_Extract.py"
ruff check "1889 - v3.0.0\STALK\STALK_ACTIONS\INSTAGRAM_ACTIONS\Instagram_Extract.py"
ruff check "1889 - v3.0.0\STALK\STALK_ACTIONS\EXIF_ACTIONS\Exif_Extract.py"
ruff check "1889 - v3.0.0/STALK/COPY_ACTIONS/Copy_Html_Css.py"


ruff check "1889 - v3.0.0\SECURITY\Option_G1.py"
ruff check "1889 - v3.0.0\SECURITY\LINK_ACTIONS\Phishing_Analysis.py"
ruff check "1889 - v3.0.0\SECURITY\DDOS_ACTIONS\DDoS_Analysis.py"


ruff check "1889 - v3.0.0\NETHUNTER\Option_H1.py"
ruff check "1889 - v3.0.0\NETHUNTER\PORT_ACTIONS\Port_Extract.py"
ruff check "1889 - v3.0.0\NETHUNTER\IP_ACTIONS\Ip_Extract.py"


ruff check "1889 - v3.0.0\PROTOCOL\S\S_Login.py"
ruff check "1889 - v3.0.0\PROTOCOL\S\S_Redirect.py"
ruff check "1889 - v3.0.0\PROTOCOL\S\S_Profile.py"


pause
