import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")  # Block notification popups
chrome_options.add_argument("--disable-infobars")  # Disable "Chrome is being controlled" infobar
chrome_options.add_argument("--disable-popup-blocking")  # Block popup windows
chrome_options.add_argument("--incognito")  # Run Chrome in incognito mode
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable image loading to speed up
chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
chrome_options.add_argument("--allow-insecure-localhost")   # Allow insecure connections

# Initialize list to store player information dictionaries
player_data = []

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# League dictionary
leagues = {
    13: {'country': 'England', 'name': 'Premier League'},
    16: {'country': 'France', 'name': 'Ligue 1'},
    19: {'country': 'Germany', 'name': 'Bundesliga'},
    31: {'country': 'Italy', 'name': 'Serie A'},
    53: {'country': 'Spain', 'name': 'La Liga'},
    4: {'country': 'Belgium', 'name': 'Pro League'},
    7: {'country': 'Brazil', 'name': 'Série A'},
    10: {'country': 'Netherlands', 'name': 'Eredivisie'},
    14: {'country': 'England', 'name': 'Championship'},
    17: {'country': 'France', 'name': 'Ligue 2'},
    20: {'country': 'Germany', 'name': '2. Bundesliga'},
    32: {'country': 'Italy', 'name': 'Serie B'},
    39: {'country': 'United States', 'name': 'Major League Soccer'},
    41: {'country': 'Norway', 'name': 'Eliteserien'},
    50: {'country': 'Scotland', 'name': 'Premiership'},
    54: {'country': 'Spain', 'name': 'La Liga 2'},
    56: {'country': 'Sweden', 'name': 'Allsvenskan'},
    60: {'country': 'England', 'name': 'League One'},
    61: {'country': 'England', 'name': 'League Two'},
    63: {'country': 'Greece', 'name': 'Super League'},
    64: {'country': 'Hungary', 'name': 'Nemzeti Bajnokság I'},
    65: {'country': 'Republic of Ireland', 'name': 'Premier Division'},
    66: {'country': 'Poland', 'name': 'Ekstraklasa'},
    68: {'country': 'Türkiye', 'name': 'Süper Lig'},
    80: {'country': 'Austria', 'name': 'Bundesliga'},
    83: {'country': 'Korea Republic', 'name': 'K League 1'},
    189: {'country': 'Switzerland', 'name': 'Super League'},
    308: {'country': 'Portugal', 'name': 'Primeira Liga'},
    313: {'country': 'Azerbaijan', 'name': 'Premyer Liqa'},
    317: {'country': 'Croatia', 'name': 'Hrvatska nogometna liga'},
    318: {'country': 'Cyprus', 'name': '1. Division'},
    319: {'country': 'Czechia', 'name': 'První liga'},
    322: {'country': 'Finland', 'name': 'Veikkausliiga'},
    330: {'country': 'Romania', 'name': 'Liga I'},
    332: {'country': 'Ukraine', 'name': 'Premier League'},
    335: {'country': 'Chile', 'name': 'Primera Division'},
    336: {'country': 'Colombia', 'name': 'Categoría Primera A'},
    337: {'country': 'Paraguay', 'name': 'División Profesional'},
    338: {'country': 'Uruguay', 'name': 'Primera División'},
    350: {'country': 'Saudi Arabia', 'name': 'Pro League'},
    351: {'country': 'Australia', 'name': 'A-League Men'},
    353: {'country': 'Argentina', 'name': 'Liga Profesional de Fútbol'},
    2012: {'country': 'China PR', 'name': 'Super League'},
    2013: {'country': 'United Arab Emirates', 'name': 'Pro League'},
    2017: {'country': 'Bolivia', 'name': 'División de Fútbol Profesional'},
    2018: {'country': 'Ecuador', 'name': 'Serie A'},
    2019: {'country': 'Venezuela', 'name': 'Primera Division'},
    2020: {'country': 'Peru', 'name': 'Liga 1'},
    2076: {'country': 'Germany', 'name': '3. Liga'},
    2149: {'country': 'India', 'name': 'Super League'}
}

# Function to scrape data from a single page
def scrape_page(soup, lg):
    table_rows = soup.find_all('tr')

    for i, row in enumerate(table_rows):
        # Initialize dictionary to store player data
        player_info = {}
        player_info['League'] = f"{leagues[lg]['name']} ({leagues[lg]['country']})"
        
        # Extract player name
        player_link = row.find('a', href=lambda href: href and "player" in href)
        player_info['Player'] = player_link.get('data-tippy-content') if player_link else None

        # Extract team name
        team_link = row.find('a', href=lambda href: href and "team" in href)
        player_info['Team'] = team_link.text.strip() if team_link else None

        # Extract positions
        position_elements = row.find_all('span', class_='pos')
        player_positions = ", ".join([pos.text for pos in position_elements]) if position_elements else None
        player_info['Position'] = player_positions

        # Extract other data columns
        td_elements = row.find_all('td')
        for td in td_elements:
            data_col = td.get('data-col')
            if data_col:
                player_info[data_col] = td.text.strip()

        # Extract contract term
        contract_cell = row.find('div', class_='sub')
        if contract_cell:
            contract_text = contract_cell.text.strip()
            if '~' in contract_text:
                start, end = contract_text.split('~')
                player_info['Contract Start'] = start.strip()
                player_info['Contract End'] = end.strip()
            else:
                player_info['Contract Start'] = None
                player_info['Contract End'] = contract_text.strip()
        else:
            player_info['Contract Start'] = None
            player_info['Contract End'] = None

        # Append player info to list
        player_data.append(player_info)

# Loop through pages of the league
for lg in leagues.keys():
    print(leagues[lg]['name'])
    offset = 0
    base_url = f"https://sofifa.com/players?type=all&showCol%5B%5D=pi&showCol%5B%5D=ae&showCol%5B%5D=hi&showCol%5B%5D=wi&showCol%5B%5D=pf&showCol%5B%5D=oa&showCol%5B%5D=pt&showCol%5B%5D=bo&showCol%5B%5D=bp&showCol%5B%5D=gu&showCol%5B%5D=jt&showCol%5B%5D=le&showCol%5B%5D=vl&showCol%5B%5D=wg&showCol%5B%5D=rc&showCol%5B%5D=ta&showCol%5B%5D=cr&showCol%5B%5D=fi&showCol%5B%5D=he&showCol%5B%5D=sh&showCol%5B%5D=vo&showCol%5B%5D=ts&showCol%5B%5D=dr&showCol%5B%5D=cu&showCol%5B%5D=fr&showCol%5B%5D=lo&showCol%5B%5D=bl&showCol%5B%5D=to&showCol%5B%5D=ac&showCol%5B%5D=sp&showCol%5B%5D=ag&showCol%5B%5D=re&showCol%5B%5D=ba&showCol%5B%5D=tp&showCol%5B%5D=so&showCol%5B%5D=ju&showCol%5B%5D=st&showCol%5B%5D=sr&showCol%5B%5D=ln&showCol%5B%5D=te&showCol%5B%5D=ar&showCol%5B%5D=in&showCol%5B%5D=po&showCol%5B%5D=vi&showCol%5B%5D=pe&showCol%5B%5D=cm&showCol%5B%5D=td&showCol%5B%5D=ma&showCol%5B%5D=sa&showCol%5B%5D=sl&showCol%5B%5D=tg&showCol%5B%5D=gd&showCol%5B%5D=gh&showCol%5B%5D=gc&showCol%5B%5D=gp&showCol%5B%5D=gr&showCol%5B%5D=tt&showCol%5B%5D=bs&showCol%5B%5D=wk&showCol%5B%5D=sk&showCol%5B%5D=aw&showCol%5B%5D=dw&showCol%5B%5D=ir&showCol%5B%5D=bt&showCol%5B%5D=hc&showCol%5B%5D=pac&showCol%5B%5D=sho&showCol%5B%5D=pas&showCol%5B%5D=dri&showCol%5B%5D=def&showCol%5B%5D=phy&showCol%5B%5D=t1&showCol%5B%5D=t2&showCol%5B%5D=ps1&showCol%5B%5D=ps2&showCol%5B%5D=tc&showCol%5B%5D=at&lg={lg}&offset="

    while True:
        driver.get(base_url + str(offset))
        driver.execute_script("window.stop();")  # Stop page load
        time.sleep(1)  # Allow the page to load

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        scrape_page(soup, lg)

        # Check for the "Next" button
        next_button = driver.find_elements(By.LINK_TEXT, "Next")
        if next_button:
            offset += 60  # Move to the next page
        else:
            break

        driver.delete_all_cookies()

# Close the driver after scraping
driver.quit()

# Create a DataFrame from the player data and save it
df = pd.DataFrame(player_data)
df.to_csv('sofifa_player_data_teams.csv', index=False)
