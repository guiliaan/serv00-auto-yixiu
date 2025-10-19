async def login(username, password, panel):
    global browser
    page = None
    service_name = get_service_name(panel)
    screenshot_path = f'screenshots/{service_name}_{username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'

    try:
        if not browser:
            browser = await launch(headless=False)  # 可视化调试；成功后改True

        page = await browser.newPage()
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        url = f'https://{panel}/login/?next=/'
        await page.goto(url, {'waitUntil': 'networkidle2'})

        # 等待表单出现（基于JS: data-login-form）
        await page.waitForSelector('[data-login-form], form:has(input[name="login"]), form:has(input[name="username"])', {'timeout': 10000})

        # 提取CSRF token（如果有，Django常见）
        csrf_token = await page.evaluate('''() => {
            const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
            return csrf ? csrf.value : null;
        }''')
        if csrf_token:
            print(f'找到CSRF token: {csrf_token[:10]}...')  # 日志

        # 用户名输入：优先name="login"（JS变更），fallback username或ID
        login_selectors = ['input[name="login"]', 'input[name="username"]', '#id_username']
        login_input = None
        for selector in login_selectors:
            login_input = await page.querySelector(selector)
            if login_input:
                print(f'✅ 找到用户名输入: {selector}')
                break
        if not login_input:
            raise Exception('无法找到用户名/登录输入框')

        # 清空并输入（键盘模拟）
        await page.click(selector)
        await page.keyboard.down('Control')
        await page.keyboard.press('a')
        await page.keyboard.up('Control')
        await page.keyboard.press('Backspace')
        await page.type(selector, username)

        # 密码输入：name="password"（确认不变）
        password_input = await page.querySelector('input[name="password"], #id_password')
        if not password_input:
            raise Exception('无法找到密码输入框')
        print(f'✅ 找到密码输入: input[name="password"]')
        await page.click('input[name="password"]')
        await page.keyboard.down('Control')
        await page.keyboard.press('a')
        await page.keyboard.up('Control')
        await page.keyboard.press('Backspace')
        await page.type('input[name="password"]', password)

        # 提交：优先form.submit()（基于JS on('submit')），无按钮
        form_selector = '[data-login-form], form:has(input[name="login"]), form'
        form = await page.querySelector(form_selector)
        if form:
            print(f'✅ 找到表单: {form_selector}')
            # 小延迟 + 提交
            await asyncio.sleep(0.5)
            await page.evaluate('form => form.submit()', form)
        else:
            # fallback: 按Enter在密码框
            print('⚠️ 未找到表单，使用Enter提交')
            await page.keyboard.press('Enter')

        # 等待提交/导航（监听loader或URL变）
        await page.waitForFunction('''() => {
            return !document.querySelector('[data-form-loader]') || window.location.pathname !== '/login/';
        }''', {'timeout': 15000})

        await page.waitForNavigation({'timeout': 10000, 'waitUntil': 'networkidle0'})

        # 成功检查（增强）
        is_logged_in = await page.evaluate('''() => {
            const logout = document.querySelector('a[href="/logout/"]') !== null;
            const notLogin = window.location.pathname !== '/login/';
            const successMsg = document.querySelector('.alert-success, .dashboard') !== null;
            return logout || notLogin || successMsg;
        }''')
        print(f'登录结果: {"成功" if is_logged_in else "失败"} | 当前URL: {await page.url()}')

        if not is_logged_in:
            await page.screenshot({'path': screenshot_path, 'fullPage': True})
            print(f'❌ 截图: {screenshot_path} - 检查验证错误或loader')

        return is_logged_in

    except Exception as e:
        print(f'❌ {service_name} {username} 异常: {e}')
        if page:
            await page.screenshot({'path': screenshot_path, 'fullPage': True})
        return False

    finally:
        if page:
            await page.close()
