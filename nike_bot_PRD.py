import time
import re
from random import randint, choice  
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import requests
import json
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
import mysql.connector
from datetime import datetime
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "pw",
    database = "db"
)

def webhook(_gender,_name,_url,_icon,_id,_price,_release_date,_stock_level,_timestamp,_update):
    webhook = DiscordWebhook(url = "https://discord.com/api/webhooks/1054080621728772156/knYtxpbxbJJ0FSuhevZ7D1e-vvttSD-ewoce3dh9Bff9xZKzqXivc5vHKl3ecxC_jHiX",username="NikeBot",rate_limit_retry=True)
    embed = DiscordEmbed(description=_gender,color= "008E45")
    embed.set_author(name=(_name+_update),url=_icon,icon=_url)
    embed.add_embed_field(name="SKU",value=_id,inline=False)
    embed.add_embed_field(name="Price",value = _price,inline=False)
    embed.add_embed_field(name="Release Date",value=_release_date,inline=False)
    embed.add_embed_field(name="Stock Level",value=_stock_level)
    embed.set_thumbnail(url=_url)
    embed.set_footer(text=_timestamp)
    webhook.add_embed(embed)
    response = webhook.execute()

mycursor = db.cursor(buffered=True)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) 
driver = webdriver.Chrome(chrome_options=chrome_options)
achains = ActionChains(driver)

driver.get('https://www.nike.com/pl/w?q=dunk&vst=dunk')
time.sleep(1)

while True:
    achains.key_down(Keys.F5).key_up(Keys.F5).perform()
    time.sleep(5)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(5)

    elem_list = driver.find_element(By.CSS_SELECTOR,"#Wall > div > div.results__body > div.product-grid.css-1hl0l1w > main > section > div")
    items = elem_list.find_elements(By.XPATH,'//div[@data-testid="product-card"]')

    id_list = []
    count = 0
    for item in items:

        try:
            button = driver.find_element(By.XPATH,'//button[@class="pre-modal-btn-close bg-transparent"]')
            achains.move_to_element(button).click().perform()
        except:
            pass
        try:
            z = driver.find_element(By.XPATH,'//svg[@aria-hidden="true"]')
            if z:
                achains.move_to_element(z).click().perform()
        except NoSuchElementException:
            pass

        if "Już wkrótce" in item.text:
            data_product_position = str(item.get_attribute('data-product-position'))
            
            name = elem_list.find_element(By.XPATH,'//div[@data-product-position="'+data_product_position+'"]//child::a[@data-testid="product-card__img-link-overlay"]')
            name = name.get_attribute('aria-label')

            gender = elem_list.find_element(By.XPATH,'//div[@data-product-position="'+data_product_position+'"]//child::div[@class="product-card__subtitle"]')
            gender = gender.text

            price = elem_list.find_element(By.XPATH,'//div[@data-product-position="'+data_product_position+'"]//child::div[@data-test="product-price"]')
            price = price.text
            price = float(price.replace(",",".").replace(" zł",""))

            status = elem_list.find_element(By.XPATH,'//div[@data-product-position="'+data_product_position+'"]//child::div[@data-testid="product-card__messaging"]')
            status = status.text

            pic = elem_list.find_element(By.XPATH,'//div[@data-product-position="'+data_product_position+'"]//child::img[@loading="lazy"]')
            pic = pic.get_attribute('src')

            link = elem_list.find_element(By.XPATH,'//div[@data-product-position="'+data_product_position+'"]//child::a[@class="product-card__img-link-overlay"]')
            pagelink = link.get_attribute('href')
    
            product_link = driver.find_element(By.XPATH,'//div[@data-product-position="'+data_product_position+'"]')
            
            try:
                button = driver.find_element(By.XPATH,'//button[@class="pre-modal-btn-close bg-transparent"]')
                achains.move_to_element(button).click().perform()
            except:
                pass
            try:
                achains.move_to_element(product_link).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
                time.sleep(1)
            except:
                pass
            p = driver.current_window_handle
            parent = driver.window_handles[0]
            try:
                chld = driver.window_handles[1]   
            except:
                try:
                    button = driver.find_element(By.XPATH,'//svg[@class="pre-close-icon"]')
                    achains.move_to_element(button).click().perform()
                except:
                    pass
            driver.switch_to.window(chld)
            time.sleep(5)
            try:
                z = driver.find_element(By.XPATH,'//svg[@aria-hidden="true"]')
                if z:
                    achains.move_to_element(z).click().perform()
            except NoSuchElementException:
                pass
            
            uuid = driver.find_element(By.XPATH,'//li[@class="description-preview__style-color ncss-li"]')
            uuid = uuid.text
            pattern = re.compile('\w{2}\d{4}[-]\d{3}')
            matches = pattern.finditer(uuid)
            id = []
            for match in matches:
                x = match.group()
                id.append(x)
            id =str(id)
            id = id.strip("['']")
            id_list.append(id)

            try:
                rd = driver.find_element(By.XPATH,'//p[@class="description-preview responsive-body-3-2 ta-sm-c mt2-sm"]')
                pattern = re.compile('\d{1,2}.\d{1,2}')
                matches = pattern.finditer(rd.text)

                release_date = []
                for match in matches:
                    x = match.group()
                    release_date.append(x)
                _date = release_date[0]
                _time = release_date[1]
                _day = int(_date[0:2])
                _month = int(_date[3:])

                pattern = re.compile('GMT-\d')
                matches = pattern.finditer(rd.text)
                timezone = []
                for match in matches:
                    x = match.group()
                    timezone.append(x)
                    timezone = str(timezone).strip("'[]'")
            except NoSuchElementException:
                _date = "NULL"
                _time = 0
                _day = 0
                _month = 0
                timezone = "NULL"

            initial = driver.page_source
            file = open('sourcecode.txt','w+',encoding='utf-8')
            file.write(initial)
            file.close()
            html = 'sourcecode.txt'
            with open(html,'r',encoding='utf-8') as file:
                var = file.read()
                file.close()
                pass

            sk = 'skuId":"'
            pattern = re.compile('(?<=' + sk + ').{36}(?=","localizedSize":")')
            matches = pattern.finditer(var)
            skuId = []
            size_and_stock = {
                "sku_id" : []
                ,"nik_size" : []
                ,"loc_size" : []
                ,"stk" : []
            }
            match_count = 0
            for match in matches:
                match_count += 1
                x = match.group()
                size_and_stock["sku_id"].append(x)

                pattern = re.compile('(?<="nikeSize":")\d{1,2}\.?\w?\w?\d?(?=","skuId":"' + x +'")')
                shoesize = pattern.finditer(var)
                for shoes in shoesize:
                    shoes = shoes.group()
                    size_and_stock['nik_size'].append(shoes)

                pattern = re.compile('(?<="'+ x +'","localizedSize":")\d{2}(?:\.\d)?(?=")')
                locsize = pattern.finditer(var)
                for loc in locsize:
                    loc = loc.group()
                    size_and_stock['loc_size'].append(loc)

                pattern = re.compile('(?<="level":")\w{3,7}(?=","skuId":"' + x +'")')
                stk = pattern.finditer(var)
                for amt in stk:
                    amt = amt.group()
                    size_and_stock['stk'].append(amt)

            mycursor.execute("SELECT COUNT(id) FROM shoes")
            shoe_count = mycursor.fetchone()
            shoe_count = int(str(shoe_count).strip("(''),"))
            missing = 0

            mycursor.execute("SELECT id FROM shoes")
            id_checker = mycursor.fetchall()
            
            for i in id_checker: # if current id in database
                i = (str(i)).strip("(''),")
                if id in i: # if id is in database, check if shoes table has changes, check if size chart has made updates
                    update_notification = []    
                    mycursor.execute("SELECT * FROM shoes WHERE id = %s AND active = %s",(i,1))
                    try:
                        name_db = list(mycursor.fetchone())
                        mycursor.execute("""SELECT st.sku_id, st.nik_size, st.loc_size, st.stock_level
                                            FROM shoes as s
                                            RIGHT JOIN size_and_stock as st
                                            ON st.id = s.id
                                            WHERE s.id = %s
                                            AND s.active = %s
                                            ORDER BY st.row_id""",(i,1))
                        stock_db = mycursor.fetchall()

                        if name != name_db[1]:
                            mycursor.execute("UPDATE shoes SET name = %s WHERE id = %s AND active = %s",(name,i,1))
                            db.commit()
                            update_notification.append("name")
                        if gender != name_db[3]:
                            mycursor.execute("UPDATE shoes SET last_updated = %s, gender = %s WHERE id = %s AND active = %s",(datetime.now(),gender,i,1))
                            db.commit()
                            update_notification.append("gender")
                        if price != name_db[4]:
                            mycursor.execute("UPDATE shoes SET last_updated = %s, price = %s WHERE id = %s AND active = %s",(datetime.now(),price,i,1))
                            db.commit()
                            update_notification.append("price")
                        if status != name_db[5]:
                            mycursor.execute("UPDATE shoes SET last_updated = %s, status = %s WHERE id = %s AND active = %s",(datetime.now(),status,i,1))
                            db.commit()
                            update_notification.append("status")
                        if pic != name_db[6]: 
                            mycursor.execute("UPDATE shoes SET last_updated = %s, pic = %s WHERE id = %s AND active = %s",(datetime.now(),pic,i,1))
                            db.commit()
                            update_notification.append("status")
                        if pagelink != name_db[7]: 
                            mycursor.execute("UPDATE shoes SET last_updated = %s, pagelink = %s WHERE id = %s AND active = %s",(datetime.now(),pagelink,i,1))
                            db.commit()
                            update_notification.append("status")
                        if _day != name_db[8]:
                            mycursor.execute("UPDATE shoes SET last_updated = %s, release_day = %s WHERE id = %s AND active = %s",(datetime.now(),_day,i,1))
                            db.commit()
                            update_notification.append("_day")
                        if _month != name_db[9]:
                            mycursor.execute("UPDATE shoes SET last_updated = %s, release_month= %s WHERE id = %s AND active = %s",(datetime.now(),_month,i,1))
                            db.commit()
                            update_notification.append("_month")
                        if str(_time) != name_db[10] and _time != 0:
                            mycursor.execute("UPDATE shoes SET last_updated = %s, release_time = %s WHERE id = %s AND active = %s",(datetime.now(),_time,i,1))
                            db.commit()
                            update_notification.append("_time")
            
                        if len(stock_db) > match_count:
                            counter = 0
                            for k in stock_db:
                                mycursor.execute("SELECT nik_size FROM size_and_stock WHERE nik_size = %s AND sku_id = %s",(k[1],k[0]))
                                test = str(mycursor.fetchone()).strip("(), ")

                                if k[0] not in size_and_stock['sku_id']:
                                    mycursor.execute("DELETE FROM size_and_stock WHERE sku_id = %s AND row_id > %s",(k[0],0))
                                    db.commit()
                                    mycursor.execute("UPDATE shoes SET last_updated = %s WHERE id = %s",(datetime.now(),id))
                                    db.commit()
                                    update_notification.append("sku_id//shoe size NO LONGER AVAILABLE")
                                    continue

                                elif str(k[1]).replace(".0","") not in size_and_stock['nik_size']:
                                    mycursor.execute("UPDATE size_and_stock SET stock_level = NULL WHERE nik_size = %s AND sku_id = %s",(datetime.now(),k[1],k[0]))
                                    db.commit()
                                    mycursor.execute("UPDATE shoes SET last_updated = %s WHERE id = %s",(datetime.now(),id))
                                    db.commit()
                                    update_notification.append("nik_size//shoe size out of stock")
                                
                                elif str(k[2]).replace(".0","") not in size_and_stock['loc_size']:
                                    mycursor.execute("UPDATE size_and_stock SET stock_level = NULL WHERE loc_size = %s AND sku_id = %s",(k[2],k[0]))
                                    db.commit()
                                    mycursor.execute("UPDATE shoes SET last_updated = %s WHERE id = %s",(datetime.now(),id))
                                    db.commit()
                                    update_notification.append("loc_size//shoe size out of stock")
                                counter += 1

                                mycursor.execute("""SELECT COUNT(st.loc_size) 
                                                    FROM size_and_stock st
                                                    INNER JOIN shoes as s
                                                    ON s.id = st.id
                                                    WHERE s.id = %s
                                                    AND s.active = %s"""
                                                    ,(id,1))    
                                
                                length = mycursor.fetchone()
                                length = int(str(length).strip("(),"))
                                if length == counter:
                                    mycursor.execute("""SELECT s.id,s.name,s.last_updated,s.gender,s.price
                                                        ,s.status,s.pic,s.pagelink,s.release_day
                                                        ,s.release_month,s.release_time
                                                    FROM shoes as s
                                                    INNER JOIN size_and_stock as st
                                                    ON s.id = st.id
                                                    WHERE s.id = %s
                                                    AND s.active = %s
                                                    ORDER BY st.loc_size
                                                    ;""", (id,1))
                                    data1 = mycursor.fetchall()
                                    __id = data1[0][0]
                                    __name = str(data1[0][1])
                                    __timestamp = str(data1[0][2]).replace("-",".")
                                    __timestamp = __timestamp[:-3] 
                                    __gender = data1[0][3]
                                    __price = str("{} PLN".format(data1[0][4]))
                                    __status = data1[0][5]
                                    __icon = data1[0][6]
                                    __url = data1[0][7]
                                    if data1[0][9] == 0 and int(data1[0][10]) == 0:
                                        __release_date = "TBD"
                                    elif data1[0][9] == 12:
                                        __release_date = "2022-{}-{} {}".format(data1[0][9],data1[0][8],data1[0][10])
                                    else:
                                        __release_date = "2023-{}-{} {}".format(data1[0][9],data1[0][8],data1[0][10]) 

                                    mycursor.execute("""SELECT st.nik_size,st.loc_size,st.stock_level
                                                        FROM shoes as s
                                                        INNER JOIN size_and_stock as st
                                                        ON s.id = st.id
                                                        WHERE s.id = %s
                                                        AND s.active = %s
                                                        ORDER BY st.loc_size
                                                        ;""", (id,1))
        
                                    data2 = mycursor.fetchall()
                                    arr_shoe_sizes = []
                                    for k in data2:
                                        arr_shoe_sizes.append("{} ({}) - {}".format(k[0],k[1],k[2]))
                                    shoe_arr = (
                                                """
                                                {}
                                                """.format("\n".join(arr_shoe_sizes)))
                                    webhook(
                                        __gender,__name,__icon,__url,__id,__price,__release_date,shoe_arr,__timestamp," (UPDATE)"
                                    )
                                else:
                                    pass
                        
                        elif len(stock_db) == match_count: # num of records, check sku_id's
                            counter = 0
                            for k in stock_db:
                                if k[0] not in size_and_stock['sku_id']:
                                    mycursor.execute("DELETE FROM size_and_stock WHERE sku_id = %s AND row_id > %s",(k[0],0))
                                    db.commit()
                                    mycursor.execute("UPDATE shoes SET last_updated = %s WHERE id = %s",(datetime.now(),id))
                                    db.commit()
                                    update_notification.append("sku_id//shoe size NO LONGER AVAILABLE")
                                    continue
                                else:
                                    mycursor.execute("SELECT stock_level FROM size_and_stock WHERE id = %s AND sku_id = %s",(id,k[0]))
                                    test = str(mycursor.fetchone()).strip("(), ")                    
                                    test = test.replace("'","")
                                    if k[3] != test:
                                        if str(k[3]) == "None" and str(test) == "None":
                                            pass
                                        else:
                                            mycursor.execute("UPDATE size_and_stock SET stock_level = %s WHERE sku_id = %s",(k[3],k[0]))
                                            db.commit()
                                            mycursor.execute("UPDATE shoes SET last_updated = %s WHERE id = %s",(datetime.now(),id))
                                            db.commit()
                                            update_notification.append('stock_level')
                                    else:
                                        pass

                                counter += 1
                        
                        elif len(stock_db) < match_count: # if the db has less then add the new size record into the database and send an update 
                            mycursor.execute("SELECT sku_id FROM size_and_stock WHERE id = %s AND row_id > %s",(i,0))
                            test = str(mycursor.fetchall()).strip("(), ")                    
                            counter = 0
                            for q in size_and_stock['sku_id']:
                                if q not in test:
                                    try:
                                        mycursor.execute("INSERT INTO size_and_stock (id,nik_size,loc_size,stock_level,row_id,sku_id) VALUES (%s,%s,%s,%s,%s,%s)",(id,size_and_stock['nik_size'][counter],size_and_stock['loc_size'][counter],size_and_stock['stk'][counter],counter+1,q))
                                        db.commit()
                                        mycursor.execute("UPDATE shoes SET last_updated = %s WHERE id = %s",(datetime.now(),id))
                                        db.commit()
                                        update_notification("new size added")
                                    except IndexError:
                                        mycursor.execute("INSERT INTO size_and_stock (id,nik_size,loc_size,stock_level,row_id,sku_id) VALUES (%s,%s,%s,%s,%s,%s)",(id,0,size_and_stock['loc_size'][counter],size_and_stock['stk'][counter],counter+1,q))
                                        db.commit()
                                        mycursor.execute("UPDATE shoes SET last_updated = %s WHERE id = %s",(datetime.now(),id))
                                        db.commit()
                                        update_notification.append("new size added")
                                    counter+=1

                        if update_notification == []:
                            db.commit()
                        else:
                            db.commit()
                            mycursor.execute("""SELECT s.id,s.name,s.last_updated,s.gender,s.price
                                                    ,s.status,s.pic,s.pagelink,s.release_day
                                                    ,s.release_month,s.release_time
                                                FROM shoes as s
                                                INNER JOIN size_and_stock as st
                                                ON s.id = st.id
                                                WHERE s.id = %s
                                                AND s.active = %s
                                                ORDER BY st.loc_size
                                                ;""", (id,1))
                            data1 = mycursor.fetchall()
                            __id = data1[0][0]
                            __name = str(data1[0][1])
                            __timestamp = str(data1[0][2]).replace("-",".")
                            __timestamp = __timestamp[:-3] 
                            __gender = data1[0][3]
                            __price = str("{} PLN".format(data1[0][4]))
                            __status = data1[0][5]
                            __icon = data1[0][6]
                            __url = data1[0][7]
                            if data1[0][9] == 0 and int(data1[0][10]) == 0:
                                __release_date = "TBD"
                            elif data1[0][9] == 12:
                                __release_date = "2022-{}-{} {}".format(data1[0][9],data1[0]
                                [8],data1[0][10])
                            else:
                                __release_date = "2023-{}-{} {}".format(data1[0][9],data1[0]
                                [8],data1[0][10])
                            mycursor.execute("""SELECT st.nik_size,st.loc_size,st.stock_level
                                                FROM shoes as s
                                                INNER JOIN size_and_stock as st
                                                ON s.id = st.id
                                                WHERE s.id = %s
                                                AND s.active = %s
                                                ORDER BY st.loc_size
                                                ;""", (id,1))
                            data2 = mycursor.fetchall()
                            arr_shoe_sizes = []
                            for k in data2:
                                arr_shoe_sizes.append("{} ({}) - {}".format(k[0],k[1],k[2]))
                            shoe_arr = (
                                        """
                                        {}
                                        """.format("\n".join(arr_shoe_sizes)))
                            webhook(
                                __gender,__name,__icon,__url,__id,__price,__release_date,shoe_arr,__timestamp," (UPDATE)"
                            )
                    except TypeError:
                        pass           
                else:
                    missing +=1            
            if missing == shoe_count:
                mycursor.execute("INSERT INTO shoes (id,name,last_updated,gender,price,status,pic,pagelink,release_day,release_month,release_time,timezone,active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (id,name,datetime.now(),gender,price,status,pic,pagelink,_day,_month,_time,timezone,1))
                db.commit()

                row_id = 1 
                for i in size_and_stock['sku_id']:
                    mycursor.execute("INSERT INTO size_and_stock (sku_id,id,row_id) VALUES (%s,%s,%s)",(i,id,row_id))
                    db.commit()
                    row_id +=1
                
                row_id = 1
                for i in size_and_stock['nik_size']:
                    mycursor.execute("UPDATE size_and_stock SET nik_size = %s WHERE row_id = %s AND id = %s",(i,row_id,id))
                    row_id+=1
                    db.commit()
        
                row_id = 1
                for i in size_and_stock['loc_size']:
                    mycursor.execute("UPDATE size_and_stock SET loc_size = %s WHERE row_id = %s AND id = %s",(i,row_id,id))
                    row_id+=1
                    db.commit()
        
                row_id = 1
                for i in size_and_stock['stk']:
                    mycursor.execute("UPDATE size_and_stock SET stock_level = %s WHERE row_id = %s AND id = %s",(i,row_id,id))
                    row_id+=1
                    db.commit()

                mycursor.execute("UPDATE shoes SET last_updated = %s WHERE id = %s",(datetime.now(),id))
                db.commit()

                mycursor.execute("""SELECT s.id,s.name,s.last_updated,s.gender,s.price
                                    ,s.status,s.pic,s.pagelink,s.release_day
                                    ,s.release_month,s.release_time,s.timezone
                                FROM shoes as s
                                INNER JOIN size_and_stock as st
                                ON s.id = st.id
                                WHERE s.id = %s
                                AND s.active = %s
                                ORDER BY st.loc_size
                            ;""", (id,1))
                data1 = mycursor.fetchall()
                __id = data1[0][0]
                __name = data1[0][1]
                __timestamp = str(data1[0][2]).replace("-",".")
                __timestamp = __timestamp[:-3] 
                __gender = data1[0][3]
                __price = str("{} PLN".format(data1[0][4]))
                __status = data1[0][5]
                __icon = data1[0][6]
                __url = data1[0][7]
                if data1[0][9] == 0 and int(data1[0][10]) == 0:
                    __release_date = "TBD"
                elif data1[0][9] == 12:
                    __release_date = "2022-{}-{} {}".format(data1[0][9],data1[0][8],data1[0][10])
                else:
                    __release_date = "2023-{}-{} {}".format(data1[0][9],data1[0][8],data1[0][10])
                mycursor.execute("""SELECT st.nik_size,st.loc_size,st.stock_level
                                    FROM shoes as s
                                    INNER JOIN size_and_stock as st
                                    ON s.id = st.id
                                    WHERE s.id = %s
                                    AND s.active = %s
                                    ORDER BY st.loc_size
                                    ;""", (id,1))
                data2 = mycursor.fetchall()
                arr_shoe_sizes = []
                for k in data2:
                    arr_shoe_sizes.append("{} ({}) - {}".format(k[0],k[1],k[2]))
                shoe_arr = (
                            """
                            {}
                            """.format("\n".join(arr_shoe_sizes)))
                webhook(__gender,__name,__icon,__url,__id,__price,__release_date,shoe_arr,__timestamp," (NEW SHOE)")
            else:
                pass

            driver.close()
            driver.switch_to.window(parent)

            count += 1
        else:
            pass
    for i in id_checker:
        i = (str(i)).strip("(''),")
        if i in id_list:
            pass
        else:
            mycursor.execute("SELECT active FROM shoes WHERE id = %s ORDER BY %s",(i,i))
            actv = str(mycursor.fetchone()).strip("(), ")   
            if int(actv) == 1:
                mycursor.execute("UPDATE shoes SET last_updated = %s, active = %s WHERE id = %s",(datetime.now(),0,i))
                db.commit()                
                mycursor.execute("""SELECT s.id,s.name,s.last_updated,s.gender,s.price
                                        ,s.status,s.pic,s.pagelink,s.release_day
                                        ,s.release_month,s.release_time,s.timezone
                                    FROM shoes as s
                                    INNER JOIN size_and_stock as st
                                    ON s.id = st.id
                                    WHERE s.id = %s
                                    AND s.active = %s
                                    ORDER BY st.loc_size
                                ;""", (id,1))
                data1 = mycursor.fetchall()
                __id = data1[0][0]
                __name = data1[0][1]
                __timestamp = str(data1[0][2]).replace("-",".")
                __timestamp = __timestamp[:-3] 
                __gender = data1[0][3]
                __price = str("{} PLN".format(data1[0][4]))
                __status = data1[0][5]
                __icon = data1[0][6]
                __url = data1[0][7]
                if data1[0][9] == 0 and int(data1[0][10]) == 0:
                    __release_date = "TBD"
                elif data1[0][9] == 12:
                    __release_date = "2022-{}-{} {}".format(data1[0][9],data1[0][8],data1[0][10])
                else:
                    __release_date = "2023-{}-{} {}".format(data1[0][9],data1[0][8],data1[0][10])

                mycursor.execute("""SELECT st.nik_size,st.loc_size,st.stock_level
                                    FROM shoes as s
                                    INNER JOIN size_and_stock as st
                                    ON s.id = st.id
                                    WHERE s.id = %s
                                    AND s.active = %s
                                    ORDER BY st.loc_size
                                    ;""", (id,1))
                data2 = mycursor.fetchall()
                arr_shoe_sizes = []
                for k in data2:
                    arr_shoe_sizes.append("{} ({}) - {}".format(k[0],k[1],k[2]))
                shoe_arr = (
                            """
                            {}
                            """.format("\n".join(arr_shoe_sizes)))
                webhook(__gender,__name,__url,__icon,__id,__price,__release_date,shoe_arr,__timestamp, " (SHOE NO LONGER COMING SOON)")
            else:
                pass
    time.sleep(5)
    try:
        button = driver.find_element(By.XPATH,'//button[@class="pre-modal-btn-close bg-transparent"]')
        achains.move_to_element(button).click().perform()
    except:
        pass


    