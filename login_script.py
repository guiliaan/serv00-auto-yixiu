import json
import asyncio
from pyppeteer import launch
from datetime import datetime, timedelta
import aiofiles
import random
import requests
import os

# 从环境变量中获取 Telegram Bot Token 和 Chat ID
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def format_to_iso(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

async def delay_time(ms):
    await asyncio.sleep(ms / 1000)

# 全局浏览器实例
browser = None

# telegram消息
message = ""

# 用于存储各个服务成功与失败的账号
login_results = {}

def get_service_name(panel):
    if 'ct8' in panel:
        return 'CT8'
    elif 'panel' in panel:
        try:
            panel_number = int(panel.split('panel')[1].split('.')[0])
            return f'S{panel_number}'
        except ValueError:
            return 'Unknown'
    return 'Unknown'

async def login(username, password, panel):
    global browser

    page = None
    service_name = get_service_name(panel)
    try:
        if not browser:
            browser = await launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
            )

        page = await browser.newPage()
        # 注入 JS 隐藏自动化检测
        await page.evaluateOnNewDocument('''() => {
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        }''')

        url = f'https://{panel}/login/?next=/'
        await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 30000})

        # 等待表单元素加载
        try:
            await page.waitForSelector('#id_username', timeout=10000)
        except Exception as e:
            print(f'{service_name} 等待用户名输入框失败: {e}')
            return False

        # 清空并输入用户名
        username_input = await page.querySelector('#id_username')
        if username_input:
            await page.evaluate('''(input) => input.value = ""''', username_input)
        await page.type('#id_username', username, delay=random.randint(50, 150))

        # 输入密码
        await page.type('#id_password', password, delay=random.randint(50, 150))

        # 点击登录按钮
        login_button = await page.querySelector('#submit')
        if login_button:
            await login_button.click()
        else:
            # Fallback: 尝试提交表单
            await page.evaluate('document.querySelector("form").submit()')
            print(f'{service_name} 未找到 #submit 按钮，使用表单提交。')

        # 等待导航完成
        try:
            await page.waitForNavigation(options={'waitUntil': 'networkidle0', 'timeout': 30000})
        except Exception as e:
            print(f'{service_name} 导航等待失败: {e}')

        # 改进的登录验证
        is_logged_in = await page.evaluate('''() => {
            const logoutButton = document.querySelector('a[href="/logout/"]');
            const currentUrl = window.location.pathname;
            return logoutButton !== null || currentUrl.includes('/dashboard/') || currentUrl.includes('/home/') || !currentUrl.includes('/login/');
        }''')

        # 调试信息（可选，生产时可注释）
        print(f'{service_name} 登录后 URL: {await page.url()}')
        print(f'{service_name} 登录后标题: {await page.title()}')

        # 可选截图调试（生产时可注释）
        # await page.screenshot({'path': f'{service_name}_{username}_after_login.png'})

        return is_logged_in

    except Exception as e:
        print(f'{service_name}账号 {username} 登录时出现错误: {e}')
        return False

    finally:
        if page:
            await page.close()

async def shutdown_browser():
    global browser
    if browser:
        await browser.close()
        browser = None

async def main():
    global message, login_results

    try:
        async with aiofiles.open('accounts.json', mode='r', encoding='utf-8') as f:
            accounts_json = await f.read()
        accounts = json.loads(accounts_json)
    except Exception as e:
        print(f'读取 accounts.json 文件时出错: {e}')
        return

    for account in accounts:
        username = account['username']
        password = account['password']
        panel = account['panel']

        service_name = get_service_name(panel)
        is_logged_in = await login(username, password, panel)

        now_beijing = format_to_iso(datetime.utcnow() + timedelta(hours=8))

        # 统计成功和失败的账号
        if service_name not in login_results:
            login_results[service_name] = {'success': [], 'fail': []}

        if is_logged_in:
            login_results[service_name]['success'].append(username)
            message += f"✅*{service_name}*账号 *{username}* 于北京时间 {now_beijing} 登录面板成功！\n\n"
            print(f"{service_name}账号 {username} 于北京时间 {now_beijing} 登录面板成功！")
        else:
            login_results[service_name]['fail'].append(username)
            message += f"❌*{service_name}*账号 *{username}* 于北京时间 {now_beijing} 登录失败\n\n❗请检查 *{username}* 账号和密码是否正确。\n\n"
            print(f"{service_name}账号 {username} 登录失败，请检查 {service_name} 账号和密码是否正确。")

        delay = random.randint(1000, 8000)
        await delay_time(delay)

    # 删除之前的登录成功和失败的详情，只保留失败账户统计
    message += "\n🔚脚本结束，失败账户统计如下：\n"
    for service, results in login_results.items():
        if results['fail']:
            message += f"📦 *{service}* 登录失败账户数: {len(results['fail'])} 个，分别是: {', '.join(results['fail'])}\n"

    await send_telegram_message(message)
    print(f'所有账号登录完成！')
    await shutdown_browser()

async def send_telegram_message(message):
    formatted_message = f"""
*🎯 serv00&ct8自动化保号脚本运行报告*

🕰 *北京时间*: {format_to_iso(datetime.utcnow() + timedelta(hours=8))}

⏰ *UTC时间*: {format_to_iso(datetime.utcnow())}

📝 *任务报告*:

{message}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': formatted_message,
        'parse_mode': 'Markdown'
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"发送消息到 Telegram 失败: {response.text}")
    except Exception as e:
        print(f"发送消息到 Telegram 时出错: {e}")

if __name__ == '__main__':
    asyncio.run(main())
