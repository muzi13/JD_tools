import jdCookie
import json
import requests
import time
import notification

"""
东东农场

1、shareCode 为自己的助力码，但是需要别人为自己助力
2、waterTimesLimit 自定义的每天浇水最大次数
3、retainWaterLimit 完成10次浇水任务的基础上,希望水滴始终高于此数;优先级高于waterTimesLimit
4、水滴高于100时,默认使用翻倍卡;其他情况不使用道具
5、cron 35 6,11,17,23 * * *
"""
waterTimesLimit = 20  # 自定义的每天浇水最大次数
retainWaterLimit = 100  # 完成10次浇水任务的基础上,希望水滴始终高于此数
waterFriendLimit = 2  # [0,2]   0: 始终不替他人浇水   2: 替他人浇水2次以完成任务获得25水

shareCodes = ["d2d5d435675544679413cb9145577e0f", # DoveBoy
"a9fe029bdfc74ecdb395fa848da56026", #勾寻文2
"101e53c859b5424b8d29fb389aa5aca7", # muzi13
"58a45733c946470bb6436bf1ada57be2", # leeyiding
"62e6c1861d4c4fbebe1e40f109755100", # GitCourser
"f0c3537f49b74bf2a4c7399d8cccda65", # zhudan
"3de9821f43c14c33b3c482fd61136633", # Matear890
"01766d5c8676418da8f0cf4d49c0640b", # sdogsq
"6d06fa98969f4fd2aa8b03b3178cc597", # sdogsq
"0f3db2ee6707429eb07fca305121a3d4", # zaccheo
"5d73bb7a53fd4aef8af8050531e2d6f5", # watewq
"8a8ac88e98904f40a25a41c9e492436e", # zaccheo
"ac0357128b554a928cad2456c0985db1", # zaccheo
"5fc25368858e4418a90975a7d0e23c6c", # awei4287
"3b2e1bee164249bca099b60d7e4b0082", # wuli01
"6447c9c61b0c4f9a89b6d497fcaf47c9",# wuli01
"e4ab3f1c4add4513b07ee88b9c9f7784", # heros-sky
"ab54f776995e4a34b405e16724833517",# CzRQ
"99773b2ed45449aca7f6f5aee4434fb4",# CzRQ
"abdc07b6aa804a5ba183bdd88fd68654",# CzRQ
"72b1f2cb90e749559873370405df141d",# kotorin
"88a661231c504d9db5fd53a04be3752d",# Mac
"6503632e4284446787818ad8fb39baeb",# erse
"698d6f61c879488a9e9414b526aab95c", # pazza
"6b79344657394201a12ed07aad1082a3",# QGsen
"dbe88523e4044f87b90e643fe62c79f6",
"cd1c9e18dc45494183255e989d52401c",
"7eb56b9a182a46939846d5afab39e93e",# Passtey
"804b416fde154c64a56e6662abd9b6bf", # kasim
"82ae5bd339d84fd188a690610cc120b8",# 872119925
"fb7c8066b68f464eb5b83007241f47bd",# 872119925
"5dc2fab7051f4969a459f8fa10ccff51",# Pyj
"283f780699344343ae1c47743df4b1f8", # chenyz1984
"48e6f7c3b2494ab89fdf3479212121df", # chenyz1984
"4fd723be248f420ba7492d2dd9087b84", # chenyz1984
"ba237aedd1ef4968a355610b776e341f",# yyteiark
"241d233796d84cb8b69cf927b00aa1c9",# doudou628
"a50e6d7efcd848ca8281cb9de0fc87e4",# wg1977
"95fb0d29333e4042b757b9e3d9fa0ab7",# wg1977]


def postTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', functionId),
    )
    data = {
        'body': json.dumps(body),
        "appid": "wh5",
        "clientVersion": "9.1.0"
    }
    response = requests.post(
        'https://api.m.jd.com/client.action', headers=headers, cookies=cookies, data=data, params=params)
    return response.json()


def getTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'Host': 'api.m.jd.com',
    }
    body["version"] = 4
    body["channel"] = 1
    params = (
        ('functionId', functionId),
        ('body', json.dumps(body)),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    return response.json()


def duck(cookies):
    print("\n【小鸭子】")
    for _ in range(4):
        result = postTemplate(cookies, "getFullCollectionReward", {
                              "type": 2, "version": 6})
        # print(result)
        if result["code"] == "10" or result["hasLimit"]:
            print(">>>小鸭子游戏达到上限,跳出")
            return


def luck(cookies):
    print("\n【随机水滴】")
    result = postTemplate(cookies, "gotWaterGoalTaskForFarm", {"type": 3})
    if result["code"] == "0":
        print("addEnergy ", result["addEnergy"])
    if result["code"] == "7":
        print("暂无")


def water(cookies):
    print("\n【Water】")
    result = postTemplate(cookies, "initForFarm", {"version": 2})
    totalWaterTaskTimes = postTemplate(cookies, "taskInitForFarm", {"version": 2})[
        "totalWaterTaskInit"]["totalWaterTaskTimes"]
    toFlowTimes = result["toFlowTimes"]
    toFruitTimes = result["toFruitTimes"]
    totalEnergy = result["farmUserPro"]["totalEnergy"]
    print(f"当前水滴: {totalEnergy}")
    doubleCard = postTemplate(cookies, "myCardInfoForFarm",
                              {"version": 4, "channel": 1})["doubleCard"]
    # print("检索[水滴翻倍卡]")
    if doubleCard > 0 and totalEnergy >= 100:
        print("存在[水滴翻倍卡],且水滴高于100")
        for i in range(doubleCard):
            print("使用[翻倍卡]", postTemplate(cookies, "userMyCardForFarm",
                                          {"cardType": "doubleCard"}))

    if totalWaterTaskTimes >= 10 and totalEnergy < retainWaterLimit+10:
        print(
            f"""10次浇水完成,保留水滴{totalEnergy}g (retainWaterLimit={retainWaterLimit} 限制)""")
        print("跳出自动浇水")
        return
    if totalWaterTaskTimes >= waterTimesLimit:
        print("跳过浇水")
        print(f"今日实际浇水 {totalWaterTaskTimes} 次")
        print(f"已达今日最大浇水 {waterTimesLimit} 次")
        print("\n请自行修改 waterTimesLimit")
        return
    for i in range(waterTimesLimit):
        print(f"自动浇水...[{i}]")
        time.sleep(0.2)
        waterInfo = postTemplate(cookies, "waterGoodForFarm", {})  # 实际浇水
        print(waterInfo)
        totalEnergy = waterInfo["totalEnergy"]
        totalWaterTimes = waterInfo["totalWaterTimes"]
        if waterInfo["finished"]:
            print("\n水果成熟,退出浇水")
            return
        if waterInfo["treeEnergy"] == 10:
            # 奖励30水
            print(postTemplate(cookies, "gotStageAwardForFarm", {"type": 1}))
            totalEnergy += 30
        if waterInfo["treeEnergy"] == toFlowTimes*10:
            # 奖励40水
            print(postTemplate(cookies, "gotStageAwardForFarm", {"type": 2}))
            totalEnergy += 40
        if waterInfo["treeEnergy"] == toFruitTimes*10:
            # 奖励50水
            print(postTemplate(cookies, "gotStageAwardForFarm", {"type": 3}))
            totalEnergy += 50
        if totalWaterTimes >= 10 and totalEnergy < retainWaterLimit+10:
            print(
                f"""10次浇水完成,保留水滴{totalEnergy}g (retainWaterLimit= {retainWaterLimit}限制)""")
            print("跳出自动浇水")
            return
        if totalWaterTimes >= waterTimesLimit:
            print("跳过浇水")
            print(f"今日实际浇水 {totalWaterTimes} 次")
            print(f"已达今日最大浇水 {waterTimesLimit} 次")
            print("\n请自行修改 waterTimesLimit")
            return
        if totalEnergy < 10:
            print("水滴不足")
            return


def friends(cookies):
    print("\n【好友浇水】")
    data = postTemplate(cookies, "friendListInitForFarm",
                        {"version": 4, "channel": 1})
    print(f"""今日邀请 {data["inviteFriendCount"]}/10""")
    if data["inviteFriendCount"] > 0 and data["inviteFriendCount"] > data["inviteFriendGotAwardCount"]:
        print("领取邀请奖励")
        print(postTemplate(cookies, "awardInviteFriendForFarm", {}))
    if waterFriendLimit == 0:
        print("始终不为好友浇水\n跳过")
        return
    needWater = [i["shareCode"]
                 for i in data["friends"] if i["friendState"] == 1]
    waterFriendCountKey = postTemplate(cookies, "taskInitForFarm", {})[
        "waterFriendTaskInit"]["waterFriendCountKey"]
    print(f"今日为好友浇水次数:{waterFriendCountKey}")
    needWater = shareCodes+needWater
    if waterFriendCountKey >= waterFriendLimit:
        print("助力浇水完成\n")
        return
    N = waterFriendLimit - waterFriendCountKey
    for i in needWater:
        print(i)
        if N == 0:
            return
        data = postTemplate(cookies, "waterFriendForFarm",
                            {"shareCode": i, "version": 6})
        print(data)
        if data["code"] == "0":
            N -= 1
        if data["code"] == "11":
            print("水滴不够,跳出")
            return


def bag(cookies):
    print("\n【背包】")
    data = postTemplate(cookies, "myCardInfoForFarm",
                        {"version": 6, "channel": 1})
    beanCard = data['beanCard']
    fastCard = data["fastCard"]
    doubleCard = data["doubleCard"]
    signCard = data["signCard"]
    print(f"""水滴换豆卡 {beanCard}""")
    print(f"""快速浇水卡 {fastCard}""")
    print(f"""水滴翻倍卡 {doubleCard}""")
    print(f"""额外签到卡 {signCard}""")


def takeTask(cookies):
    print("\n【任务列表】")
    taskList = postTemplate(cookies, "taskInitForFarm", {})
    if "signInit" in taskList:
        _signInit = taskList["signInit"]  # 连续签到
        print(f"""todaySigned: {_signInit["todaySigned"]}""")
        if not _signInit["todaySigned"]:
            print("连续签到")
            postTemplate(cookies, "signForFarm", {"type": 2})

    _gotBrowseTaskAdInit = taskList["gotBrowseTaskAdInit"]  # 浏览
    print(f"""BrowseTaskAd: {_gotBrowseTaskAdInit["f"]}""")
    if not _gotBrowseTaskAdInit["f"]:
        for i in _gotBrowseTaskAdInit["userBrowseTaskAds"]:
            print("浏览广告")
            postTemplate(cookies, "browseAdTaskForFarm", {
                         "type": 0, "advertId": i["advertId"]})
            time.sleep(0.4)
            postTemplate(cookies, "browseAdTaskForFarm", {
                         "type": 1, "advertId": i["advertId"]})

    _gotThreeMealInit = taskList["gotThreeMealInit"]  # 定时领水 6-9，11-14，17-21
    print(f"""ThreeMeal: {_gotThreeMealInit["f"]}""")
    if not _gotThreeMealInit["f"]:
        print("三餐定时领取")
        postTemplate(cookies, "gotThreeMealForFarm", {})

    _firstWaterInit = taskList["firstWaterInit"]  # 每日首次浇水
    print(f"""firstWater: {_firstWaterInit["f"]}""")
    if not _firstWaterInit["f"]:
        print("首次浇水奖励")
        postTemplate(cookies, "firstWaterTaskForFarm", {})

    _totalWaterTaskInit = taskList["totalWaterTaskInit"]  # 每日累计浇水
    print(
        f"""totalWaterTask: {_totalWaterTaskInit["f"]}  ({_totalWaterTaskInit["totalWaterTaskTimes"]}/10)""")
    if not _totalWaterTaskInit["f"] and _totalWaterTaskInit["totalWaterTaskTimes"] >= 10:
        print("浇水10次奖励")
        postTemplate(cookies, "totalWaterTaskForFarm", {})

    _waterRainInit = taskList["waterRainInit"]  # 收集水滴雨
    print(f"""waterRain: {_waterRainInit["winTimes"]}/2""")
    if not _waterRainInit["f"]:
        print(">>>>水滴雨")
        postTemplate(cookies, "waterRainForFarm", {
            "type": 1, "hongBaoTimes": 100, "version": 3})
    _waterFriendTaskInit = taskList["waterFriendTaskInit"]
    print(
        f"""waterFriend: {_waterFriendTaskInit["waterFriendCountKey"]}/{_waterFriendTaskInit["waterFriendMax"]}   {_waterFriendTaskInit["f"]}""")
    if not _waterFriendTaskInit["f"] and _waterFriendTaskInit["waterFriendCountKey"] >= _waterFriendTaskInit["waterFriendMax"]:
        print(">>>>帮助好友浇水奖励")
        postTemplate(cookies, "waterFriendGotAwardForFarm",
                     {"version": 4, "channel": 1})
    return _totalWaterTaskInit["totalWaterTaskTimes"]


def _help(cookies, shareCodes):
    for i in shareCodes:
        postTemplate(cookies, "initForFarm", {"shareCode": i})
        postTemplate(cookies, "initForFarm", {
            "shareCode": f"{i}-inviteFriend"})


def masterHelp(cookies):
    print("\n【助力得水】")
    help_me_list = postTemplate(cookies, "masterHelpTaskInitForFarm", {})
    masterHelpPeoples = len(help_me_list["masterHelpPeoples"])
    print(
        f"""完成进度 {masterHelpPeoples}/5   {help_me_list["f"]}""")
    if not help_me_list["f"] and masterHelpPeoples >= 5:
        print("领取奖励")
        help_me_list1 = postTemplate(
            cookies, "masterGotFinishedTaskForFarm", {})
        print(help_me_list1)


def clockIn(cookies):
    print("\n【打卡领水】")
    clockInInit = postTemplate(
        cookies, "clockInInitForFarm", {})
    if clockInInit["totalSigned"] == 7 and not clockInInit["gotClockInGift"]:  # 惊喜礼包
        print('[领取惊喜礼包]', postTemplate(cookies, "clockInForFarm", {"type": 2}))

    print(f"""todaySigned: {clockInInit["todaySigned"]}""")
    if not clockInInit["todaySigned"]:
        print("今日签到")
        print(postTemplate(cookies, "clockInForFarm", {"type": 1}))

    if "themes" in clockInInit:
        if clockInInit["themes"]:
            print(
                f""">>> 限时关注得水滴 {clockInInit["myFollowThemeConfigTimes"]}/3""")
            for i in [i["id"] for i in clockInInit["themes"] if not i["hadGot"]]:
                print(f"""关注id [{i}]""")
                postTemplate(cookies, "clockInFollowForFarm", {
                    "id": i, "type": "theme", "step": 1})
                time.sleep(0.5)
                postTemplate(cookies, "clockInFollowForFarm", {
                    "id": i, "type": "theme", "step": 2})
                time.sleep(0.5)

    if "venderCoupons" in clockInInit:
        if clockInInit["venderCoupons"]:
            print(
                f""">>> 限时领券得水滴 {clockInInit["myFollowVenderCouponTimes"]}/3""")
            for i in [i["id"] for i in clockInInit["venderCoupons"] if not i["hadGot"] and i["hadStock"]]:
                print(f"""领券id [{i}]""")
                time.sleep(0.5)
                postTemplate(cookies, "clockInFollowForFarm",
                             {"id": i, "type": "venderCoupon", "step": 1})
                time.sleep(0.5)
                postTemplate(cookies, "clockInFollowForFarm",
                             {"id": i, "type": "venderCoupon", "step": 2})


def turnTable(cookies):
    print("\n【天天抽奖】")
    result = getTemplate(cookies, "initForTurntableFarm", {})
    if "turntableBrowserAds" in result:
        for i in result["turntableBrowserAds"]:
            if i["status"]:
                continue
            print("浏览广告>>")
            print(getTemplate(cookies, "browserForTurntableFarm",
                              {"type": 1, 'adId': i["adId"], }))
            time.sleep(1)
            print(getTemplate(cookies, "browserForTurntableFarm",
                              {"type": 2, 'adId': i["adId"], }))
    if "timingGotStatus" in result:
        if not result["timingGotStatus"] and result["sysTime"]-result["timingLastSysTime"] > 14400000:  # 领取定时奖励
            print('[定时奖励] ', getTemplate(
                cookies, "timingAwardForTurntableFarm", {}))
    print(
        f"""为我助力: {result["masterHelpTimes"]}/{result["helpedTimesByOther"]}""")

    for i in shareCodes:
        getTemplate(cookies, "initForFarm", {"shareCode": f"{i}-3"})  # 助力

    result = getTemplate(cookies, "initForTurntableFarm", {})
    for i in range(result["remainLotteryTimes"]):  # 抽奖次数
        print(f'[抽奖 {i}] ', getTemplate(
            cookies, "lotteryForTurntableFarm", {"type": 1}))  # 抽奖
        time.sleep(2)


def run():
    for cookies in jdCookie.get_cookies():
        result = postTemplate(cookies, 'initForFarm', {"version": 4})
        treeState = result["treeState"]
        if treeState == 0:
            print("还未开始种植")
            continue
        if treeState in [2, 3]:
            print("可以兑换了")
            notification.notify(
                f"""东东农场可兑换【{cookies["pt_pin"]}】""", f"""东东农场 账号【{cookies["pt_pin"]}】 可以兑换了""")
            continue
        nickName = result["farmUserPro"]["nickName"]
        myshareCode = result["farmUserPro"]["shareCode"]
        treeEnergy = result["farmUserPro"]["treeEnergy"]
        lastTimes = int(
            (result["farmUserPro"]["treeTotalEnergy"]-treeEnergy)/10)
        print(
            f"""\n\n[ {nickName} ]\n{result["farmUserPro"]["name"]} (通用红包)""")
        print(f'已经薅了{result["farmUserPro"]["winTimes"]}次')
        print(f"""我的助力码: {myshareCode}""")
        print(
            f"""treeEnergy: {treeEnergy}/{result["farmUserPro"]["treeTotalEnergy"]}""")
        print(
            f"""剩余浇水次数: {lastTimes}""")
        turnTable(cookies)
        clockIn(cookies)
        _help(cookies, shareCodes)
        takeTask(cookies)
        masterHelp(cookies)
        luck(cookies)
        duck(cookies)
        friends(cookies)
        bag(cookies)
        water(cookies)
        print("\n")
        print("##"*30)


if __name__ == "__main__":
    run()
