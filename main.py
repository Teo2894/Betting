from webdriver import *
import time

debugmode = False
def condprint(string):
    if debugmode == True:
        print(string)

class surebet:
    def __init__(self):
        self.base_profit = 0 # listed from site
        self.rounded_profit_list = list() #When numbers are rounded - what can be won for each outcome.
        self.list_of_partial_bets = list()
    def add_partial_bet(self, partial_bet_dict):
        self.list_of_partial_bets.append(partial_bet_dict)
    def create_even_bets(self, investment_range):
        print("EVEN BETS")
        nr_of_partial_bets = len(self.list_of_partial_bets)
        suggested_total_bet = (investment_range[0]+investment_range[1])/2
        suggested_avg_bet_per_bookmaker = suggested_total_bet/nr_of_partial_bets
        total_bet=0 # Suggested bets added below
        for bet in self.list_of_partial_bets:
            odds = bet["odds"]
            investment_factor = round(nr_of_partial_bets/odds,3)
            suggested_partial_bet = investment_factor*suggested_avg_bet_per_bookmaker
            suggested_partial_bet_rounded = round(suggested_partial_bet/10)*10
            suggested_bet = suggested_partial_bet_rounded
            bet["suggested_bet"] = suggested_bet
            total_bet += suggested_bet

        # SUREBET CONTROL
        print("SUREBET CONTROL:")
        print("Total bet: " + str(total_bet))
        good_surebet = True
        for bet in self.list_of_partial_bets:
            print(bet["site"])
            print("Odds and bet: " + str(bet["odds"]) + ", " + str(bet["suggested_bet"]))
            win_return = bet["odds"] * bet["suggested_bet"]
            print("Return: "+str(win_return))
            gain = win_return-total_bet
            print("Gain: " + str(gain))
            if gain < 0:
                good_surebet = False
        if good_surebet == True:
            print("GOOD SUGGESTED BETS!")
            print("Make more even?")
        else:
            print("BAD SUGGESTED BETS!")
            print("Adjust?")




class sure_bet_finder:
    def __init__(self):
        self.d = driver(headless=False)
        self.d.get("https://oddspedia.com/surebets")
    def get_bets(self):
        self.list_of_surebets = list()
        #
        self.d.wait_until_element_is_loaded("/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/main/div")
        betlist_element_list = self.d.find_elements(By.CLASS_NAME,"btools-match")
        i=0 # Used below to scroll down page incremently to visualise bets to load bet-site links
        for bet in betlist_element_list: #Go through bets from list
            condprint("\nNew sure-bet:")
            bet_object = surebet()
            # Get gain percent
            base_profit_raw = bet.find_element(By.CLASS_NAME,"sure-bet-cta__inner").text
            base_profit = float(base_profit_raw[:base_profit_raw.find("%")])
            bet_object.base_profit = base_profit
            # Scroll down to load bookmakers
            i+=1
            self.d.execute_script("window.scrollTo(0,%s);"%(180*i)) # See above, scrolls page. Change to dynamic number?
            # GET BOOKMAKERS
            bookmaker_list = bet.find_elements(By.CLASS_NAME,"btools-odd-mini")
            for bookmaker in bookmaker_list: # Go through suggested bets per bookmaker tog get data
                condprint(bookmaker.find_element(By.TAG_NAME,"img").get_attribute("src"))
                site_link = bookmaker.find_element(By.TAG_NAME, "img").get_attribute("src")
                site_name = bookmaker.find_element(By.TAG_NAME,"img").get_attribute("src")[len(site_link)-site_link[::-1].find("/"):-4]
                condprint(site_name)
                condprint(bookmaker.find_element(By.CLASS_NAME,"btools-odd-mini__value").text)
                odds = float(bookmaker.find_element(By.CLASS_NAME,"btools-odd-mini__value").text)
                bet_object.add_partial_bet({"site":site_name, "odds":odds})
            self.list_of_surebets.append(bet_object)
        return self.list_of_surebets
    def filter_bets(self):
        self.list_of_filtered_surebets = list()
        for bet in self.list_of_surebets:
            print(bet.list_of_partial_bets)
            print("ADD FILTER")
        return self.list_of_filtered_surebets
    def end(self):
        quit_all()

def main():
    sbf = sure_bet_finder()
    list_of_bets = sbf.get_bets()
    list_of_good_bets = sbf.filter_bets()
    #
    bet_obj = list_of_bets[0]
    investment_range = (200,600)
    bet_obj.create_even_bets(investment_range)
    sbf.end()


main()