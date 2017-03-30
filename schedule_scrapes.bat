REM @echo off
REM For /f "tokens=2-4 delims= " %%a in ('date /t') do (set mydate=%%c.%%a.%%b)
for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set today=%Month%.%Day%.%Year%

echo %today%


schtasks /create /sc once /ri 5 /tn "Instacart_Scrape_1"  /st 12:00 /DU 24:00 /tr "H:\Soda_Tax_Scrapes\start_instacart.cmd 1 %today% john-smith@coe.edu InstaCart"
schtasks /create /sc once /ri 5 /tn "Instacart_Scrape_2"  /st 12:03 /DU 24:00 /tr "H:\Soda_Tax_Scrapes\start_instacart.cmd 2 %today% crain.dsccn@gmail.com sodatax"
schtasks /create /sc once /ri 5 /tn "Instacart_Scrape_3"  /st 12:05 /DU 24:00 /tr "H:\Soda_Tax_Scrapes\start_instacart.cmd 3 %today% claire.underwood@gmail.com sodatax"
schtasks /create /sc once /ri 5 /tn "Walmart_Scrape"  /st 12:08 /DU 24:00 /tr "H:\Soda_Tax_Scrapes\start_walmart.cmd %today% 


REM pause
