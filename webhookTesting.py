from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime 

x = ["5 (35.5) - HIGH",
        "5.5 (36) - HIGH"
        ,"6 (36.5) - HIGH"
        ,"6.5 (37) - HIGH"
        ,"7 (37.5) - HIGH"
        ,"7.5 (38)- HIGH"]

arr_shoes = (
                """
                {}
                """.format("\n".join(x)))

def webhook(_gender,_name,_url,_icon,_id,_price,_release_date,_stock_level,_timestamp):
    webhook = DiscordWebhook(url = "https://discord.com/api/webhooks/1052719399741689856/_xuQvw7yJY6ezTaWivyHnitEoxlXhI-AEVJBFsugQT2eNHifN7wDRuQWYuxhxosaQeT8",username="NikeBot",rate_limit_retry=True)
    embed = DiscordEmbed(description=_gender,color= "008E45")
    embed.set_author(name=_name+" (UPDATE)",url=_url,icon=_icon)
    embed.add_embed_field(name="SKU",value=_id,inline=False)
    embed.add_embed_field(name="Price",value = _price,inline=False)
    embed.add_embed_field(name="Release Date",value=_release_date,inline=False)
    embed.add_embed_field(name="Stock Level",value=_stock_level)
    embed.set_thumbnail(url=_icon)
    embed.set_footer(text=_timestamp)
    webhook.add_embed(embed)
    response = webhook.execute()
webhook("buty"
    ,"Nike Pump Boost"
    ,'https://www.nike.com/pl/t/buty-dla-malych-dunk-low-zhJ5P6/CW1588-100'
    ,"https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/d5a172a4-63de-4a03-b043-06649a0be10c/buty-dla-malych-dunk-low-zhJ5P6.png"
    ,"12AK-ST45"
    ,"429.99 PLN"
    ,"2022-12-20 14:00"
    ,"test"
    ,"20.12.2022 17:43"
    )