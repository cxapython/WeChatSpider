# -*- encoding:utf-8 -*-
"""
@Time   :   2020/7/24 10:15 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :    实现初始化的自动化登录(通过输入手机号码和密码的方式进行自动化登录)
"""
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time
from config import appiumconfig
def autoLogin(driver):
    print("自动化登录微信..............")
    driver.implicitly_wait(60)
    print("单击登录......")
    driver.find_element_by_id('com.tencent.mm:id/fam').click()#单击登录
    time.sleep(1)
    print("输入手机号码.........")
    user = driver.find_element_by_id("com.tencent.mm:id/bhn")
    user.send_keys("15659599610")
    time.sleep(1)
    print("单击下一步控件.......")
    driver.find_element_by_id("com.tencent.mm:id/e3i").click()#单击下一步
    time.sleep(1)
    driver.find_element_by_id("com.tencent.mm:id/doz").click() # 单击我知道控件...
    time.sleep(1)
    driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button").click()#单击允许控件
    time.sleep(1)
    driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button").click()  # 单击允许控件
    print("输入微信用户的密码......")
    password = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.EditText")
    password.send_keys("yanjerry")
    time.sleep(1)
    driver.find_element_by_id("com.tencent.mm:id/e3i").click()#登录
    time.sleep(5)
    driver.find_element_by_id("com.tencent.mm:id/doz").click()#单击 是 控件
    print("你成功的自动登录微信了......hhhh")
if __name__ == '__main__':
    desired_caps = {}
    desired_caps['platformName'] = appiumconfig.get("platformName")
    desired_caps['platformVersion'] = appiumconfig.get("platformVersion")
    desired_caps['deviceName'] = appiumconfig.get("deviceName")
    desired_caps['appPackage'] = 'com.tencent.mm'
    desired_caps['appActivity'] = 'com.tencent.mm.ui.LauncherUI'
    desired_caps['resetKeyboard'] = appiumconfig.get("resetKeyboard")
    desired_caps['automationName'] = appiumconfig.get("automationName")
    # desired_caps['noReset'] = appiumconfig.get("noReset")
    driver = webdriver.Remote(appiumconfig.get("url"),desired_caps)
    autoLogin(driver)

