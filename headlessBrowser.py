import requests as r
import json
from time import sleep
from datetime import datetime
import os
import sys
from random import randint, choice


from databasemanager import DatabaseManager, Nike
from sneaker import Sneaker
from webhook import WebHookSender


class MaxRetries(Exception):
    pass

class NikeAgent:
    def __init__(self, searched_phrases: list, db: DatabaseManager):
        self.db_manager = db
        self.searched_phrases = searched_phrases
        self.comming_soon = []
        self.todayDate = datetime.now()
        # Debug variables
        self.current_sku = None
    

    def get_json_from_static(self, static):
        sleep(1)
        user_agent = self.generate_user_agent()
        for _ in range(10):
            headers = {
                'user-agent': user_agent,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            }
            req = r.get(static, headers=headers)
            print("Status code from static:", req.status_code)
            try:
                beg = req.text.index('<script id="__NEXT_DATA__" type="application/json">') + 51
                end = req.text[beg:].index("</script>")
                with open("test.html", "w", encoding="utf-8") as file:
                    file.write(req.text[beg: beg + end])
                data = json.loads(req.text[beg: beg + end])["props"]["pageProps"]["initialState"]
                data["Threads"]["products"]
                return data

            except ValueError as e:
                user_agent = self.generate_user_agent()
                print("Retry Value for: ", static)
                sleep(2)

            except KeyError as e:
                user_agent = self.generate_user_agent()
                print("Retry Key for: ", static)
                sleep(2)
        else:
            return None
    
    def get_json_from_api(self, api_link):
        user_agent = self.generate_user_agent()
        headers = {
            'user-agent': user_agent
        }
        req = r.get(api_link, headers=headers)
        print("Status code from API:", req.status_code)

        return json.loads(req.text)

    def generate_user_agent(self) -> dict:
        user_agent = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edge/12.246",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36 Edg/103.0.1264.62",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.62",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 OPR/88.0.4412.75"
        ]
        return choice(user_agent)

    def format_date_time(self, date_time):
        date_time = date_time.split("T")
        date = date_time[0]
        time = ":".join(date_time[1][:-5].split(":")[:2])
        return date, time
    
    def get_onsite_data(self, base: dict, url) -> None:
        skuIds_data = {}
        json_data = self.get_json_from_static(url)
        if json_data is None:
            return
        if "products" not in json_data["Threads"].keys():
            return

        skus = json_data["Threads"]["products"]
        for sku in skus.keys():
            if json_data["Threads"]["products"][sku]["publishType"] != "LAUNCH":
                continue

            sneaker = Sneaker()
            sneaker.apply_base(base)
            sneaker["sku"] = sku

            sneaker["image"] = json_data["Threads"]["products"][sku]["firstImageUrl"]
            sneaker["url"] = url[:url.rindex("/") + 1] + sku

            if json_data["Threads"]["products"][sku]["launchView"] is None:
                continue
            else:
                unformated_release = json_data["Threads"]["products"][sku]["launchView"]["startEntryDate"]
                date, time = self.format_date_time(unformated_release)

                year, month, day = date.split("-")
                hours, minutes = time.split(":")
                raw_release = datetime(int(year), int(month), int(day), int(hours), int(minutes))
                if self.todayDate >= raw_release:
                    return

                sneaker["release"] = (date, time)
                sneaker["raw_release"] = raw_release.timestamp()

            for sku_info in json_data["Threads"]["products"][sku]["availableSkus"]:
                if sku_info["available"] is True:
                    skuIds_data[sku_info["skuId"]] = {
                        "level": sku_info["level"],
                    }

            for sku_data in json_data["Threads"]["products"][sku]["skus"]:
                if sku_data["skuId"] in skuIds_data.keys():
                    skuIds_data[sku_data["skuId"]]["nikeSize"] = sku_data["nikeSize"]
                    skuIds_data[sku_data["skuId"]]["localizedSize"] = sku_data["localizedSize"]
                    skuIds_data[sku_data["skuId"]]["localizedSizePrefix"] = sku_data["localizedSizePrefix"]
            
            skuIds_data_sorted = list(skuIds_data.items())
            skuIds_data_sorted.sort(key=lambda x: float(x[1]["localizedSize"]))
            stock_levels = [f'{v["nikeSize"]} ({v["localizedSize"]}) - {v["level"]}' for k, v in skuIds_data_sorted]
            if len(stock_levels) == 0:
                sneaker["stock_levels"] = "All sizes are OOS"
            else:
                sneaker["stock_levels"] = stock_levels

            self.comming_soon.append(sneaker)

    def generate_data_from_api(self):
        template = "https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=69696969696969696969969696969696&country=pl&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(PL)%26filter%3Dlanguage(pl)%26filter%3DemployeePrice(true)%26searchTerms%3D{searched}%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=pl&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%93%20%7BhighestPrice%7D"

        for phrase in self.searched_phrases:
            next = True
            counter = 0
            while next:
                json_data = self.get_json_from_api(template.format(searched=phrase, anchor=counter*24))
                next = bool(json_data["data"]["products"]["pages"]["next"])

                for product in json_data["data"]["products"]["products"]:
                    for colorway in product["colorways"]:
                        if colorway["label"] == "COMING_SOON":
                            base = dict()
                            base["model"] = product["title"]
                            base["type"] = product["subtitle"]
                            base["price"] = product["price"]["currentPrice"]
                            base["currency"] = product["price"]["currency"]
                            url_formated = "https://www.nike.com/" + product["url"].format(countryLang = "pl")
                            self.get_onsite_data(base, url_formated)

                counter += 1
            
    def get_sneakers(self):
        return self.comming_soon


    def write_log(self, error_type, text):
        if os.path.isfile("log.txt"):
            mode = "a"
        else:
            mode = "w"

        with open("log.txt", mode, encoding="utf-8") as file:
            file.write(f"{error_type},{text},{datetime.now()}\n")


    def initialize(self):
        print("Looking for new sneakers (nike.com)...")

        self.generate_data_from_api()
            
        self.comming_soon.sort(key=lambda s: s["raw_release"])
        while len(self.comming_soon) > 0:
            sneaker = self.comming_soon.pop(0)
            sku = sneaker["sku"]
            stock_text = ",".join(sneaker["stock_levels"])
            values = {"stock": stock_text, "release_date": sneaker["raw_release"]}         
            if not self.db_manager.check_if_present(sku):
                WebHookSender(URL, sneaker).send()
                sleep(1)
                entity = Nike(sku, sneaker["raw_release"], stock_text)
                self.db_manager.add_entity(entity)
            elif not self.db_manager.compare(Nike, sku, values):
                WebHookSender(URL, sneaker, update=True).send()
                sleep(1)
                self.db_manager.update_entity(Nike, sku, values)


if __name__ == "__main__":
    debug = False

    URL = ""
    searched_phrases = ["dunk", "jordan%201"]


    db = DatabaseManager("Nike")
    if not debug:
        while True:
            try:
                agent = NikeAgent(searched_phrases, db)
                agent.initialize()
            except Exception as e:
                print("An exception occured")
                agent.write_log(sys.exc_info()[0], e)
            sleep(10)
    else:
        while True:
            agent = NikeAgent(searched_phrases, db)
            agent.initialize()
            sleep(10)
