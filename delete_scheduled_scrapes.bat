

schtasks /end /tn "Instacart_Scrape_1" /f
schtasks /delete /tn "Instacart_Scrape_1" /f
schtasks /end /tn "Instacart_Scrape_2" /f
schtasks /delete /tn "Instacart_Scrape_2" /f
schtasks /end /tn "Instacart_Scrape_3" /f
schtasks /delete /tn "Instacart_Scrape_3" /f
schtasks /end /tn "Walmart_Scrape" /f
schtasks /delete /tn "Walmart_Scrape" /f