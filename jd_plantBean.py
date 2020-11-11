import requests
import time
import json
import jdCookie


"""
种豆得豆

1、plantUuid 为自己的助力码，但是需要别人为自己助力
2、cron 35 6-23 * * *
"""

plantUuid = ["e7lhibzb3zek27gfeceqb6wwm45gshcaroxg5ka", # DoveBoy
"igefhjvuw6xvttzinfclhdqx32hqfwy7ik7bvpq", #勾寻文2
"ycr5557mgdopyat3lbjx3hikhk44ew5ktg5nyri", # muzi13
"vbkunq7afsudascdq3z6krakjc45b5tui6b3tj3amayufh5s57sq", # zaccheo
"mlrdw3aw26j3xych4vkjtv2fvj6dj7wfralfvuq", # zaccheo
"4vvbjlml6tdfdxk5evdtgofbb4onctf3ikszncq", # zaccheo
"olmijoxgmjutz6rufgoyyxlyhdkxn2i5ssi7uba", # leeyiding
"2i76mnp6etaxkqwwiguq7qicru5ac3f4ijdgqji", # GitCourser
"bnxvlp4ffm6c64kqzuofew46vi5ac3f4ijdgqji", # zhudan
"fxnwpfvlyg2bjsayzhvfprz65mo5xypodtsgjnq", # Matear890
"e7lhibzb3zek2v6lfnqcpejss755xgeesooegwa", # sdogsq
"7bfy6xxncgn3cra6vysnzff4iq", # sdogsq
"4npkonnsy7xi3ot4m6stw6w2aq2w2vqh7ltkbxq", # watewq
"2ipsfzdbgsvktdx2cbjxrxo7tnmvren2celq6lq", # awei4287
"nf4huobli66bv5yjpgr6xvtw643h7wlwy7o5jii", # wuli01
"cyjvf5btxliufhxf52gsdrzwnd2b4juzqkep47y", # wuli01
"53hz7smmdl62xurlffm24zdovq5ac3f4ijdgqji", # heros-sky
"4npkonnsy7xi23s7mq2rsrofkksnse3lbija4ya",# CzRQ
"fbdwqsx52ku446hvnga2zhk5wn726767tw62vda",# CzRQ
"e7lhibzb3zek3rc3nkeb2utelglt6z67mdg6hhq",# CzRQ
"fb227jqogvovf5dekrautr3vly3h7wlwy7o5jii",# Mac
"wsr6thb5bd25l532pbkr2w7ltlcnxnsttyd3a6y",# erse
"entryId=2tpyf45pvqnbyoqbns6eertieu", # pazza
"ohh7i5v7bjv7xggctiadqsblga3h7wlwy7o5jii",# QGsen
"e7lhibzb3zek2ovqwcjbf3ienys6y42l5jbzicq",
"5kk5tctolkrkcquwab2sinv6zm",
"twcyyfxmuxfv4ka537q4bguytu",# Passtey
"6o2dhu4lgbdhjubnysnhphmr6a", # kasim
"h4k4725iodq7l6c4hhwzyu47tu",# 872119925
"olmijoxgmjutzlngqgs7cyf57xpzwsasj5h3pfy",# 872119925
"wrirm5dzfnv263tamt5d3dc3fa5ac3f4ijdgqji",# Pyj
"d2dohdsppwgsynmsh55xhozjf4", # chenyz1984
"nkiu2rskjyetah2cxwgmgpzhnz72gjsybycp5wi", # chenyz1984
"mwgcqm2qt5ak3frmuk3rspcm5q5ac3f4ijdgqji", # chenyz1984
"tcwhysgunqvnwotm6n5pn2kura",# yyteiark
"4npkonnsy7xi2xaebjhxhq4qrxjuxcakeat3k5i",# doudou628
"kgaroyrauafivcbp2cpznl3xoa",# wg1977
"za6kg6vamtzyyelngvu4egas74",# wg1977
            ]  # 填写别人的助力码

def functionTemplate(cookies, functionId, body):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'JD4iPhone/167283 (iPhone;iOS 13.5.1;Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1,en-CN;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': "application/x-www-form-urlencoded"
    }
    if "version" not in body:
        body["version"] = "9.0.0.1"
    body["monitor_source"] = "plant_app_plant_index"
    body["monitor_refer"] = ""
    params = (
        ('functionId', functionId),
        ('body', json.dumps(body)),
        ('appid', 'ld'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    return response.json()


def postTemplate(cookies, functionId, body):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'JD4iPhone/167283 (iPhone;iOS 13.5.1;Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1,en-CN;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': "application/x-www-form-urlencoded"
    }
    params = (
        ('functionId', functionId),
    )
    body["version"] = "9.0.0.1"
    body["monitor_source"] = "plant_app_plant_index"
    body["monitor_refer"] = ""

    data = {
        'area': '5_274_49707_49973',
        'body': json.dumps(body),
        'appid': 'ld',
        'build': '167283',
        'client': 'apple',
        'clientVersion': '9.0.4',
    }
    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    return response.json()


def takeTask(cookies, taskList):
    for i in taskList:
        if i["isFinished"] == 1:
            continue
        print(i["taskName"])
        if i["dailyTimes"] == 1 and i["taskType"] != 8:  # 不含评价
            # print(i)
            taskResult = functionTemplate(cookies, "receiveNutrientsTask", {
                "monitor_refer": "receiveNutrientsTask", "awardType": str(i["taskType"])})
            print(taskResult)
            time.sleep(2)

        if i["taskType"] == 3:
            print("浏览店铺")
            N = int(i["totalNum"])-int(i["gainedNum"])
            plant_shopList = functionTemplate(cookies, "shopTaskList", {
                                              "monitor_refer": "plant_receiveNutrients"})["data"]
            goodShopList = [
                i for i in plant_shopList["goodShopList"] if i["taskState"] == "2"]
            moreShopList = [
                i for i in plant_shopList["moreShopList"] if i["taskState"] == "2"]
            shopList = goodShopList + moreShopList
            for shop in shopList:
                shopTaskId = shop["shopTaskId"]
                shopId = shop["shopId"]
                result = functionTemplate(cookies, "shopNutrientsTask", {
                                          "monitor_refer": "plant_shopNutrientsTask", "shopId": str(shopId), "shopTaskId": str(shopTaskId)})
                print(result)
                if "data" in result:
                    if result["data"]["nutrState"] == "1":
                        N -= 1
                if N == 0:
                    break
                time.sleep(1)
        if i["taskType"] == 10:
            print("关注频道")
            N = int(i["totalNum"])-int(i["gainedNum"])
            plant_ChannelList = functionTemplate(
                cookies, "plantChannelTaskList", {})["data"]
            goodChannelList = [
                i for i in plant_ChannelList["goodChannelList"] if i["taskState"] == "2"]
            normalChannelList = [
                i for i in plant_ChannelList["normalChannelList"] if i["taskState"] == "2"]
            channelList = goodChannelList+normalChannelList

            for channel in channelList:
                result = functionTemplate(cookies, "plantChannelNutrientsTask", {"channelTaskId": channel["channelTaskId"], "channelId": channel["channelId"]
                                                                                 })
                print(result)
                if "data" in result:
                    if result["data"]["nutrState"] == "1":
                        N -= 1
                if N == 0:
                    break
                time.sleep(1)
        if i["taskType"] == 5:
            print("挑选商品")
            N = int(i["totalNum"])-int(i["gainedNum"])
            productInfoList = functionTemplate(cookies, "productTaskList", {
                                               "monitor_refer": "plant_productTaskList"})["data"]["productInfoList"]
            productList = sum(productInfoList, [])
            productList = list(
                filter(lambda i: i["taskState"] == "2", productList))

            for product in productList:
                result = functionTemplate(cookies, "productNutrientsTask", {
                                          "productTaskId": product["productTaskId"], "skuId": product["skuId"], "monitor_refer": "plant_productNutrientsTask"})
                print(result)
                if "data" in result:
                    if result["data"]["nutrState"] == "1":
                        N -= 1
                if N == 0:
                    break
                time.sleep(1)


def _help(cookies, plantUuid):
    for i in plantUuid:
        functionTemplate(cookies, "plantBeanIndex", {
                         "plantUuid": i, "followType": "1", "wxHeadImgUrl": "", "shareUuid": "", })


def steal(cookies, roundId):
    print("\n【偷取营养液】\n默认对方有3个才会偷取\n不足自动跳过 ")
    result = functionTemplate(cookies, "plantFriendList", {"pageNum": "1"})

    if "errorCode" in result:
        return
    if "tips" in result["data"]:
        print("今日已达上限")
        return
    stealList = [i for i in result["data"]
                 ["friendInfoList"] if "nutrCount" in i]

    for i in stealList:
        if int(i["nutrCount"]) == 3:  # 为3时才会偷取
            print(i)
            print(functionTemplate(cookies, "collectUserNutr", {
                "paradiseUuid": i["paradiseUuid"], "roundId": roundId}))
            time.sleep(2)


def getReward(cookies, status,lastRoundId):
    print("\n[收获状况]")
    if status == "5":
        data = functionTemplate(
            cookies, "receivedBean", {"roundId": lastRoundId})["data"]
        print(f"""{data["growth"]}成长值兑换{data["awardBean"]}京豆""")
    if status == "6":
        print("您已领奖，去京豆明细页看看")


def water(cookies,currentRoundId):
    print("\n[浇水ing]")
    result = functionTemplate(cookies, "cultureBean", {
        "roundId": currentRoundId, "monitor_refer": "plant_index"})
    if "errorMessage" in result:
        print(result["errorMessage"])
        return


def egg(cookies):
    print("\n[天天扭蛋]")
    restLotteryNum = functionTemplate(cookies, "plantEggLotteryIndex", {})[
        "data"]["restLotteryNum"]
    if restLotteryNum == 0:
        print(">>>暂无扭蛋")
    for i in range(restLotteryNum):
        print(">>>扭蛋 ", i+1)
        functionTemplate(cookies, "plantEggDoLottery", {})


def waterWheel(cookies,currentRoundId):
    print("\n[水车生产(6-21)]")
    result = functionTemplate(cookies, "receiveNutrients", {
        "roundId": currentRoundId, "monitor_refer": "plant_receiveNutrients"})
    if "errorMessage" in result:
        print(result["errorMessage"])
        return

def run():
    for cookies in jdCookie.get_cookies():
        plantBeanIndex = postTemplate(cookies, "plantBeanIndex", {})
        print(
            f"""【{plantBeanIndex["data"]["plantUserInfo"]["plantNickName"]}】\n""")
        print(
            f"""我的助力码: {plantBeanIndex["data"]["jwordShareInfo"]["shareUrl"].split("=")[-1]}\n""")
        _help(cookies, plantUuid)
        roundList = plantBeanIndex["data"]["roundList"]
        lastRoundId = roundList[0]["roundId"]  # 上期id
        currentRoundId = roundList[1]["roundId"]  # 本期id
        taskList = plantBeanIndex["data"]["taskList"]  # 任务列表

        takeTask(cookies, taskList)  # 执行每日任务
        print("     任务   进度")
        for i in postTemplate(cookies, "plantBeanIndex", {})["data"]["taskList"]:
            print(
                f"""[{i["taskName"]}]  {i["gainedNum"]}/{i["totalNum"]}   {i["isFinished"]} """)

        egg(cookies)
        waterWheel(cookies,currentRoundId)
        steal(cookies, currentRoundId)
        water(cookies,currentRoundId)
        getReward(cookies, roundList[0]["awardState"],lastRoundId)
        print("\nEND\n")
        print("##"*30)
if __name__ == "__main__":
    run()
