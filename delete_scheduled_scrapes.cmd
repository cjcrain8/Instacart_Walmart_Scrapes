

schtasks /end /tn "Instacart_Scrape_1" 
schtasks /delete /tn "Instacart_Scrape_1" /f
schtasks /end /tn "Instacart_Scrape_2" 
schtasks /delete /tn "Instacart_Scrape_2" /f
schtasks /end /tn "Instacart_Scrape_3" 
schtasks /delete /tn "Instacart_Scrape_3" /f
schtasks /end /tn "Walmart_Scrape" 
schtasks /delete /tn "Walmart_Scrape" /f

pause