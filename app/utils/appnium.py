# -*- encoding:utf-8 -*-
"""
@Time   :   2020/7/23 14:30 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :   
"""
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time
import operator
from config import appiumconfig

def autoEnterHisPage(driver):
    print("进行自动化登录")
    #以手机号的方式登录微信
    try:
        print("进行隐式等待......")
        driver.implicitly_wait(15)
        time.sleep(20)
        print("单击进行搜索控件.....")
        driver.find_element_by_id("com.tencent.mm:id/f8y").click() #单击进行搜索
        time.sleep(3)
        print("单击输入框控件.....")
        TouchAction(driver).tap(x=258, y=63).perform()
        TouchAction(driver).tap(x=258, y=63).perform()
        #搜索框输入关键字 获取搜索框的控件 获取不到  存在问题？
        time.sleep(3)
        print("获取搜索框控件.....")
        inputkey =driver.find_element_by_id("com.tencent.mm:id/l6")
        print("输入关键字......")
        inputkey.send_keys("wenjianchuanshuzhushou")
        time.sleep(3)
        # 点击搜索到的文件助手
        TouchAction(driver).tap(x=193, y=198).perform()
        time.sleep(3)
        #单击文件助手的发送消息（error）
        print("单击发送消息控件")
        TouchAction(driver).tap(x=271, y=460).perform()
        #输入公众号连接入口地址
        time.sleep(1)
        input_url = driver.find_element_by_id("com.tencent.mm:id/al_")
        input_url.send_keys("https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MTI0MDU3NDYwMQ==&scene=124#wechat_redirect")
        #点击发送链接
        time.sleep(5)
        driver.find_element_by_id("com.tencent.mm:id/anv").click()
        time.sleep(3)
        #单击url连接
        print("单击url链接.....")
        TouchAction(driver).tap(x=244, y=316).perform()
        print("进入旧版公众号微信入口，进行下一步操作：自动化下拉历史消息文章........")
    except Exception as e:
        print(e)
def scrollPage(driver):
    print("成功进入微信公众号历史消息页面，准备进行自动化下拉历史消息........")
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    before = driver.page_source
    print(width)
    print(height)
    x = width / 2
    starty = height * 0.75
    endy = height * 0.25
    driver.swipe(x, starty, x, endy, 500)
    after = driver.page_source
    if operator.eq(before,after):
        print("到底了,已无就历史消息文章...........")
        return True
    return False
if __name__ == '__main__':
    desired_caps = {}
    desired_caps['platformName'] = appiumconfig.get("platformName")
    desired_caps['platformVersion'] = appiumconfig.get("platformVersion")
    desired_caps['deviceName'] = appiumconfig.get("deviceName")
    desired_caps['appPackage'] = 'com.tencent.mm'
    desired_caps['appActivity'] = 'com.tencent.mm.ui.LauncherUI'
    desired_caps['resetKeyboard'] = appiumconfig.get("resetKeyboard")
    desired_caps['automationName'] = appiumconfig.get("automationName")
    desired_caps['noReset'] = appiumconfig.get("noReset")
    driver = webdriver.Remote(appiumconfig.get("url"),desired_caps)
    autoEnterHisPage(driver)
    time.sleep(30)
    while True:
        if scrollPage(driver) ==False:
            print("自动化下拉操作进行中.......")
            time.sleep(3)
        else:
            print("完成对该公众号的历史文章页面的自动下拉.....")
            break
    driver.quit()
