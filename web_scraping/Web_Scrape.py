"""
author: @giebasjo
Date  : 15/7/2018
Description:

    The module below is the main user interface for scraping data.
    These will be called through the main "driver" function later
    once the statistical methods are fit to the data.
"""

from selenium import webdriver
import pandas as pd

from sqlalchemy import *


## Util Fns
def write_df_to_csv( df, outFile_name ):

    df.to_csv( outFile_name + ".csv" )

class Web_Scrape(object):

    # Requested data can take on the elements in the following list
    #   ['br_100', 'br_tot', 'br_adv', 'nba_stats', 'all']
    def __init__( self, requested_data, season = "" ):
        self.reqdata = requested_data
        if( self.reqdata == "nba_stats" and season != "" ):
            self.season = season
        else:
            print("Season must be entered if requested data is nba_stats")
        self.dataframes = []

    ## NBA STATS
    def nbastats_table2df(self, table):

        player_ids = []
        player_names = []
        player_stats = []

        for line_id, lines in enumerate(table.text.split('\n')):
            if line_id == 0:
                column_names = lines.split(' ')[1:]
            else:
                if line_id % 3 == 1:
                    player_ids.append(lines)
                if line_id % 3 == 2:
                    player_names.append(lines)
                if line_id % 3 == 0:
                    player_stats.append([float(i) for i in lines.split(' ')])

        db = pd.DataFrame({'player': player_names,
                           'gp': [i[0] for i in player_stats],
                           'min': [i[1] for i in player_stats],
                           'pts': [i[2] for i in player_stats],
                           'fgm': [i[3] for i in player_stats],
                           'fga': [i[4] for i in player_stats],
                           'fg%': [i[5] for i in player_stats],
                           '3pm': [i[6] for i in player_stats],
                           '3pa': [i[7] for i in player_stats],
                           '3p%': [i[8] for i in player_stats],
                           'ftm': [i[9] for i in player_stats],
                           'fta': [i[10] for i in player_stats],
                           'ft%': [i[11] for i in player_stats],
                           'oreb': [i[12] for i in player_stats],
                           'dreb': [i[13] for i in player_stats],
                           'reb': [i[14] for i in player_stats],
                           'ast': [i[15] for i in player_stats],
                           'stl': [i[16] for i in player_stats],
                           'blk': [i[17] for i in player_stats],
                           'tov': [i[18] for i in player_stats],
                           'eff': [i[19] for i in player_stats]
                           });
        db = db[['player',
                 'gp',
                 'min',
                 'pts',
                 'fgm',
                 'fga',
                 'fg%',
                 '3pm',
                 '3pa',
                 '3p%',
                 'ftm',
                 'fta',
                 'ft%',
                 'oreb',
                 'dreb',
                 'reb',
                 'ast',
                 'stl',
                 'blk',
                 'tov',
                 'eff']]

        return db

    def nba_stats_scrape(self, season):

        # Drive web-interface with chromedriver
        path_to_chromedriver = "/Users/jordangiebas/NBA_project/web_scraping/chromedriver"
        browser = webdriver.Chrome(executable_path=path_to_chromedriver)

        # Initialize Broswer
        nba_stats_url = 'https://stats.nba.com/leaders'
        browser.get(nba_stats_url)

        ## Interact with website

        # Click "All" Players
        browser.find_element_by_xpath(
            '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]').click()

        # Click the correct season (should add functionality for multiple seasons later....)
        if (self.season == "1617"):
            option = "2"
        else:
            option = "1"

        xpath_year = '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[' + option + ']'
        browser.find_element_by_xpath(xpath_year).click()

        # Get table from HTML, convert to df
        table = browser.find_element_by_class_name('nba-stat-table__overflow')
        nbastats_df = nbastats_table2df(table)

        # Append this to ongoing list of dataframes
        self.dataframes.append(db)

        return nbastats_df

    ## BR
    def br_stats_per100(self):

        br_per100_url = "https://www.basketball-reference.com/leagues/NBA_2018_per_poss.html"
        return pd.read_html(br_per100_url)[0]

    def br_stats_adv(self):

        br_adv_url = "https://www.basketball-reference.com/leagues/NBA_2018_advanced.html"
        return pd.read_html(br_adv_url)[0]

    def br_stats_tot(self):

        br_tot_url = "https://www.basketball-reference.com/leagues/NBA_2018_totals.html"
        return pd.read_html(br_tot_url)[0]













