from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime

# 激活虚拟环境 .\venv\Scripts\activate
# 运行程序 python buy.py
print(datetime.datetime.now())

# 获取当前时间（使用本地时间）
def get_current_time():
    return datetime.datetime.now()

# 等待到指定时间
def wait_until(target_time):
    print(f"当前等待到指定时间: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
    while True:
        now = get_current_time()
        print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}", end='\r')
        if now >= target_time:
            print(f"\n已到达指定时间，继续执行程序...")
            break
        time.sleep(0.2)  # 每0.2秒检查一次
# 设置开抢时间（假设4月17日20:30开抢）
target_time = datetime.datetime(2025, 4, 17, 20, 30, 0)
# 1. 打开浏览器
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=chrome_options)
# 从文件读取账号密码
def read_account_information(file_path='account_information.txt'):
    account_information = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    account_information[key] = value
        return account_information
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return None

# 获取账号密码
account_information = read_account_information()
if not account_information or 'username' not in account_information or 'password' not in account_information:
    print("无法读取账号密码，请检查account_information.txt文件")
    driver.quit()
    exit(1)

# 2. 登录网站
driver.get('https://kyfw.12306.cn/otn/resources/login.html')
# 2.1 扫码登录

try:
    driver.find_element(By.CSS_SELECTOR, '.login-hd-account').click()
except:
    print("扫码登录失败，请手动登录")
input("请手动完成扫码验证，然后按下回车键继续...")
'''
# 此处为账号密码登录
driver.find_element(By.CSS_SELECTOR, '#J-userName').send_keys(account_information['username'])
driver.find_element(By.CSS_SELECTOR, '#J-password').send_keys(account_information['password'])
driver.find_element(By.CSS_SELECTOR, '#J-login').click()
# 2.2 输入短信验证码
print("等待验证码输入界面加载...")
time.sleep(0.8)
# 请求用户输入手机收到的验证码
driver.find_element(By.CSS_SELECTOR, '#id_card').send_keys(account_information['id'])
driver.find_element(By.CSS_SELECTOR, '#verification_code').click()
verification_code = input("请查看手机收到的验证码并在此输入: ")
driver.find_element(By.CSS_SELECTOR, '#code').send_keys(verification_code)
# 点击确认按钮
driver.find_element(By.CSS_SELECTOR, '#sureClick').click()
'''
# 等待网页加载
time.sleep(1.5)
print("已完成验证码验证，继续执行程序...")

# 3. 点击车票预订，进入购票页面
try:
    driver.find_element(By.CSS_SELECTOR, '#link_for_ticket').click()
    #4. 选择城市及时间，点击查询
    driver.find_element(By.CSS_SELECTOR, '#fromStationText').click()
    driver.find_element(By.CSS_SELECTOR, '#fromStationText').clear()
    driver.find_element(By.CSS_SELECTOR, '#fromStationText').send_keys('北京南') # 起点
    driver.find_element(By.CSS_SELECTOR, '#fromStationText').send_keys(Keys.ENTER)
    driver.find_element(By.CSS_SELECTOR, '#toStationText').click()
    driver.find_element(By.CSS_SELECTOR, '#toStationText').clear()
    driver.find_element(By.CSS_SELECTOR, '#toStationText').send_keys('南宁东') # 终点
    driver.find_element(By.CSS_SELECTOR, '#toStationText').send_keys(Keys.ENTER)
    driver.find_element(By.CSS_SELECTOR, '#train_date').click()
    driver.find_element(By.CSS_SELECTOR, '#train_date').clear()
    driver.find_element(By.CSS_SELECTOR, '#train_date').send_keys('2025-05-01') # 出发日期
    time.sleep(0.3)
    driver.find_element(By.CSS_SELECTOR, '#sf2').click()
    wait_until(target_time)# 等待到开抢时间
    time.sleep(0.2)
    driver.find_element(By.CSS_SELECTOR, '#query_ticket').click()
    # 5. 选择车次，点击预订
    time.sleep(0.4)
    # 循环尝试选择车次，直到成功
    max_attempts = 50  # 最大尝试次数
    for attempt in range(max_attempts):
        try:
            print(f"第{attempt+1}次尝试选择车次...")
            driver.find_element(By.CSS_SELECTOR, '#queryLeftTable tr:nth-child(1) .btn72').click() # 括号中的数字表示从上往下数的第1趟车，可以改成你需要的车次
            print("成功选择车次！")
            break  # 成功选择车次后跳出循环
        except Exception as e:
            print(f"选择车次失败: {e}")
            if attempt < max_attempts - 1:  # 如果不是最后一次尝试
                print("重新查询车次...")
                driver.find_element(By.CSS_SELECTOR, '#query_ticket').click()
                time.sleep(0.3)  # 等待查询结果加载
            else:
                print("已达到最大尝试次数，请手动选择车次")
                input("请手动选择车次，然后按回车继续...")
    # 6. 选择乘客
    time.sleep(0.3)
    driver.find_element(By.CSS_SELECTOR, '#normalPassenger_0').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#dialog_xsertcj_ok').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#normalPassenger_1').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#dialog_xsertcj_ok').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#normalPassenger_2').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#dialog_xsertcj_ok').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#normalPassenger_3').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#dialog_xsertcj_ok').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#submitOrder_id').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, '#qd_closeDefaultWarningWindowDialog_id').click()
except:
    print("无法找到元素，请检查网页是否发生变化")
    time.sleep(100)
# 7. 点击提交订单
try:
    time.sleep(1.5)
    driver.find_element(By.CSS_SELECTOR, '#qr_submit_id').click()
except:
    print("无法找到元素，请检查网页是否发生变化")
    time.sleep(100)
# 等待手动退出
input("按下回车键以退出程序...")

# 关闭浏览器
driver.quit()
