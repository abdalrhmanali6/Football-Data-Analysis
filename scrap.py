import requests
from bs4 import BeautifulSoup
import lxml
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from datetime import datetime


#####################################################################head to head teams matches##################################################################
def head_to_head_data(team1,team2):
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.binary_location = "/usr/bin/chromium"
        chrome_driver_path = "./chromedriver"
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)


        driver.get(f"https://www.11v11.com/teams/{team1}/tab/opposingTeams/opposition/{team2}/")
        print("page Loaded...")
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "lxml")
        title_text = soup.find("div", class_="club").find("h1").text.strip()
        teamA, teamB = re.split(r"football club: record v\s+", title_text)

        matches = []
        table = soup.find("table", class_="sortable")
        
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            date_text = cols[0].text.strip()
            teams_text = cols[1].text.strip()
            score_text = cols[3].text.strip()
            competition = cols[4].text.strip()

            # Extract Home & Away teams
            HomeTeam, AwayTeam = re.split(r"\s+v\s+", teams_text)
            
            # Extract scores (handles formats like "2-1", "3 - 0")
            home_goals, away_goals = map(int, re.findall(r"\d+", score_text))
            
            # Extract date (adjust regex based on actual format)
            date_match = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})", date_text)
            date = datetime.strptime(date_match.group(), "%d %b %Y") if date_match else "Unknown"

            matches.append({
                "Date": date,
                "HomeTeam": HomeTeam.strip(),
                "AwayTeam": AwayTeam.strip(),
                "Score": f"{home_goals}-{away_goals}",
                "Competition": competition,
                "Winner": HomeTeam if home_goals > away_goals else AwayTeam if away_goals > home_goals else "Draw"
            })

        matches = pd.DataFrame(matches)
        matches = matches[matches["Competition"].str.contains(r"premier league", flags=re.IGNORECASE)]
        matches_list = matches.to_dict(orient="records")
        return matches, matches_list

    except Exception as e:
        print(f"Error: {e}")
  
    











############################################################Leauge standing data##################################################################################


def League_Standing(Date):  
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.binary_location = "/usr/bin/chromium"
        chrome_driver_path = "./chromedriver"
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

        # Fetch the page
        url = f"https://www.11v11.com/league-tables/premier-league/{Date}/"
        driver.get(url)
        print("Page loaded...")

        # Wait for JavaScript to render (critical!)
        time.sleep(5)  # Adjust delay if needed

        # Get page source and parse with BeautifulSoup
        html = driver.page_source
        driver.quit()  # Close the browser

        soup = BeautifulSoup(html, "lxml")
        table=soup.find("tbody").find_all("tr")[:10]
        rank_list=[]
        for team in table:
            team_rank=team.find("td").text.strip()
            team_name=team.find_all("td")[1].text.strip()
            game_played=team.find_all("td")[2].text.strip()
            team_win=team.find_all("td")[3].text.strip()
            team_draw=team.find_all("td")[4].text.strip()
            team_lose=team.find_all("td")[5].text.strip()
            goals_for=team.find_all("td")[6].text.strip()
            goals_in=team.find_all("td")[8].text.strip()
            points=team.find_all("td")[9].text.strip()

            rank_list.append({
            "Team rank":int(team_rank),
            "Team name":team_name,
            "Game played":int(game_played),
            "Team win":int(team_win),
            "Team draw":int(team_draw),
            "Team lose":int(team_lose),
            "Goals for":int(goals_for),
            "Goals in":int(goals_in),
            "Points":int(points)
            })

        Ranks=pd.DataFrame(rank_list)
        ranks_dic = Ranks.to_dict(orient='records')  # List of row-wise dictionaries

        return Ranks,ranks_dic
    except Exception as e:
        print("Please enter the date in this format: dd-month-yyyy (e.g., 07-April-2024). The year must be between 1993 and 2025, and the month should be written in English.")
        return None
