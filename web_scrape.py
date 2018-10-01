"""

Author: Giebas, Jordan
Date: 30/09/2018

Description:

    1. Scrape
        a. nba.com/stats
        b. espn.com
        c. basketball-reference.com
    2. Merge all data together as master_df
    3. Create Directory ./{today's date}
        a. Store individual data sources to ./{today's date}/individual_srcs
        b. Store master dataframe to ./{today's date}/main

"""

# Import necessary modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from selenium import webdriver
from datetime import datetime
import time
import os

"""
Create directory to store data in 
"""

td = datetime.today().strftime('%m_%d_%Y'); path = "./" + td + "/"
os.system( "mkdir {}".format(td) )

"""
NBA.COM/STATS SCRAPE
"""

print("\n ====== NBA.com/stats SCRAPING ====== \n")

# Define dictionary for all url parsing
nba_stats_info = {"http://stats.nba.com/players/usage/": \
                  [["/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[2]",\
                   "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]",\
                   "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]"],\
                  "nba-stat-table__overflow",\
                  [8,10] + [i for i in range(12,20)] + [23],\
                  ['%FGA','%3PA','%FTA','%OREB','%DREB','%REB','%AST','%TOV','%STL','%BLK','%PTS'],\
                  1,\
                  3],\
                  "http://stats.nba.com/players/rebounding/": \
                  [["/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[1]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]"],\
                   "table",\
                   [6,7,8,9],\
                   ["Consested_REB", "Consested_REB%", "REB_changes", "REB_changes%"],\
                   8,\
                   2],\
                  "http://stats.nba.com/players/opponent/": \
                  [["/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[3]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]"],\
                   "nba-stat-table__overflow",\
                   [6,7,9,10,12] + [x for x in range(14,21)] + [24,25],\
                   ["opp_FGA/100p","opp_FG%","opp_3PA/100p","opp_3P%","opp_FTA/100p",\
                    "opp_OREB/100p","opp_DREB/100p","opp_REB/100p", "opp_AST/100p", \
                    "opp_TOV/100p", "opp_STL/100p", "opp_BLK/100p", "opp_PTS/100p", "opp_plusminus/100p"],\
                   40,\
                   3],\
                  "http://stats.nba.com/players/defense/": \
                  [["/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[3]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]"],\
                   "nba-stat-table__overflow",\
                   [-1],\
                   ["Def_WS/100p"],\
                   10,\
                   3],\
                  "http://stats.nba.com/players/advanced/": \
                  [["/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]"],\
                   "nba-stat-table__overflow",\
                   [15,11,19,20],\
                   ["TO_ratio", "AST_ratio", "Pace", "PIE"],\
                   1,\
                   3],\
                  "http://stats.nba.com/players/touches/": \
                  [["/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[1]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]"],\
                   "nba-stat-table__overflow",\
                   [6,11],\
                   ["Touches/game", "PTS/Touch"],\
                   12,\
                   2],\
                  "http://stats.nba.com/players/speed-distance/": \
                  [["/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[1]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]"],\
                   "nba-stat-table__overflow",\
                   [y for y in range(6,12)],\
                   ["Dist_miles/g", "Dist_miles_off/g", "Dist_miles_def/g", "avg_speed/g", \
                    "avg_speed_off/g", "avg_speed_def/g"],\
                   1,\
                   2],\
                  "http://stats.nba.com/players/defense-dash-overall/": \
                  [["/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[1]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[1]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[2]",\
                    "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]"],\
                   "nba-stat-table__overflow",\
                   [y for y in range(7,11)],\
                   ["DFGA","DFG%","FG%","DIFF%"],\
                   1,\
                   2] }


# Define function to scrape nba stats
def scrape_nba_stats(url):
    print("URL: ", url)

    def populate_2(data, stat_args, player_names, player_stats):

        for idx, elm in enumerate(data):
            if idx % 2 == 0:
                player_names.append(elm)
            else:
                player_stats.append(np.array(elm.split(" "))[stat_args])

        return player_names, player_stats

    def populate_3(data, stat_args, player_names, player_stats):

        for idx, elm in enumerate(data):
            if idx % 3 == 1:
                player_names.append(elm)
            elif idx % 3 == 2:
                player_stats.append(np.array(elm.split(" "))[stat_args])

        return player_names, player_stats

    ## Unpack data
    xpaths = nba_stats_info[url][0]
    class_name = nba_stats_info[url][1]
    stats_args = nba_stats_info[url][2]
    cols = nba_stats_info[url][3]
    dp = nba_stats_info[url][4]
    fn = nba_stats_info[url][5]

    ## Set up chrome driver, open browser
    path_to_chromedriver = "./web_scraping/chromedriver"
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get(url);
    time.sleep(4)  ## make sure the browswer loads before executing xpaths

    ## Use the xpaths to click the necessary browswer buttons
    for xpath in xpaths:
        browser.find_element_by_xpath(xpath).click();
        time.sleep(4)  # Sleep in between

    ## Populate containers
    table = browser.find_element_by_class_name(class_name)

    # Containers
    player_names = [];
    player_stats = []
    data = table.text.split("\n")[dp:]

    if fn == 2:
        player_names, player_stats = populate_2(data, stats_args, player_names, player_stats)
    else:
        player_names, player_stats = populate_3(data, stats_args, player_names, player_stats)

    # Create dataframe
    df = pd.DataFrame(columns=["PLAYER"] + cols)
    for i, col in enumerate(df.columns):
        if col == "PLAYER":
            df[col] = player_names
        else:
            df[col] = [j[i - 1] for j in player_stats]

    browser.quit()

    return df

# Store dataframes
df_list = [scrape_nba_stats(url) for url in nba_stats_info.keys()]

# Fix df3, player names comma separated
tmp_df3 = df_list[2]
for i, name in enumerate(tmp_df3.PLAYER):

    L = name.split(", ")
    if (len(L) == 2):
        second = L[0];
        first = L[1]
        new_name = first + " " + second
        tmp_df3.iloc[i, 0] = new_name

df_list[2] = tmp_df3

# Store in indivdual directories
for url, df in zip(list(nba_stats_info.keys()), df_list):
    outfile_name = "NBASTATS_" + url.split("/")[4]
    df.to_csv( path + outfile_name + ".csv" )

# Create first instance of master dataframe
master_df = pd.DataFrame(columns=["PLAYER"])
master_df.PLAYER = df_list[0].PLAYER
for i in range( len( df_list ) ):
    master_df = master_df.merge( df_list[i] )

"""
ESPN SCRAPE
"""

print("\n ====== EPSN.com SCRAPING ====== \n")

espn_df_list = [];
root_espn_url = "http://www.espn.com/nba/statistics/rpm"
for i in range(1, 15):

    url = root_espn_url
    if (i != 1):
        url += "/_/page/{}".format(i)

    print("URL: ", url)

    ## Fetch necessary EPSN data
    espn_data = pd.read_html(url)[0]
    espn_data.columns = espn_data.iloc[0, :].tolist()
    espn_data = espn_data.iloc[1:, :]
    espn_data.index = pd.RangeIndex(0, len(espn_data))
    tmp_df = espn_data[["NAME", "ORPM", "DRPM", "RPM", "WINS"]]
    tmp_df.columns = ["PLAYER", "ORPM", "DRPM", "RPM", "WINS"]

    ## Format the PLAYER so upon merge it aligns with other formats
    for j, name in enumerate(tmp_df["PLAYER"]):

        L = name.split(" ")
        first = L[0];
        second = L[1];
        pos = L[2]

        if len(L) != 3:  ## edge case
            pos = L[3]

        tmp_df.loc[j, "PLAYER"] = first + " " + second[:-1]
        tmp_df.loc[j, "POSITION"] = pos

    # print( "{} shape: {}".format(i, tmp_df.shape) )
    espn_df_list.append(tmp_df)


master_espn_df = pd.concat(espn_df_list)
master_espn_df.to_csv( path + "ESPN_DATA.csv" )

"""
BBREF SCRAPE
"""
print("\n ====== BBREF.com SCRAPING ====== \n")

master_bbref_df = pd.DataFrame()

# Fetch Per 100 possession data
br_per100_url = "https://www.basketball-reference.com/leagues/NBA_2018_per_poss.html"
print( "URL: {}".format(br_per100_url) )
br_per100_data = pd.read_html(br_per100_url)[0]
br_per100_data.columns = [stat + "_BR_100" for stat in br_per100_data.columns.tolist()]

cols_100 = [elm for elm in br_per100_data.columns.tolist()[8:]]
cols_100.append(br_per100_data.columns.tolist()[1])

# Append to master dataframe
for stat in cols_100:
    master_bbref_df[stat] = br_per100_data[stat]

# Fetch Advanced data
br_adv_url = "https://www.basketball-reference.com/leagues/NBA_2018_advanced.html"
print( "URL: {}".format(br_adv_url) )
br_adv_data = pd.read_html(br_adv_url)[0]
br_adv_data.columns = [stat + "_BR_ADV" for stat in br_adv_data.columns.tolist()]
cols_adv = br_adv_data.columns.tolist()[1:3] + br_adv_data.columns.tolist()[4:]

# Append to master dataframe
for stat in cols_adv:
    master_bbref_df[stat] = br_adv_data[stat]

# Fetch Total data
br_tot_url = "https://www.basketball-reference.com/leagues/NBA_2018_totals.html"
print( "URL: {}".format(br_tot_url) )
br_tot_data = pd.read_html(br_tot_url)[0]
br_tot_data.columns = [stat + "_BR_TOT" for stat in br_tot_data.columns.tolist()]

cols_list = br_tot_data.columns.tolist()
cols_tot = [stat for stat in cols_list[8:] if (('%' not in stat) or (stat == "eFG%_BR_TOT"))]
cols_tot.append(cols_list[1])

# Append to master dataframe
for stat in cols_tot:
    master_bbref_df[stat] = br_tot_data[stat]

master_bbref_df.columns = master_bbref_df.columns.tolist()[:-1] + ["PLAYER"]
master_bbref_df.to_csv( path + "BBREF_DATA.csv" )

"""
Merge all dataframes together
"""

master_df = master_df.merge( master_bbref_df, on="PLAYER" )
master_df = master_df.merge( master_espn_df, on="PLAYER" )

print("Love you, \n \tJG")


