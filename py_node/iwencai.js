const puppeteer = require('puppeteer');
const request = require('request');


(async () => {
    for (let i = 0; i < 4; i++) {
        console.log("第%d次请求", i)
        const browser = await puppeteer.launch({headless: false, args: ['--start-maximized'],});
        const page = await browser.newPage();
        await page.evaluateOnNewDocument(() => {
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
        });
        await page.setUserAgent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36");
        // await page.setViewport({
        //     width: 1920,
        //     height: 1080
        // });
        await page.goto('https://www.iwencai.com');
        // 显示悬浮登陆
        await page.hover('div.login-box.auto_width > i');
        // 点击登陆
        await page.evaluate(() => {
            document.getElementsByClassName('to-pay-btn title1 f14 fb tc pointer white_text')[0].click()
        });

        await page.waitForTimeout(4000)
        //一共三层iframe,没有timewait的第三层不会渲染完成
        //切换iframe
        const frame = await page.frames()[2]
        await frame.click('#to_account_login');


        const uname = await frame.waitForSelector('#uname');
        uname.type('pangtong126');
        await page.waitForTimeout(2000)
        const passwd = await frame.waitForSelector('#passwd');
        passwd.type('thsmmxztxq2011');
        await page.waitForTimeout(2000)
        const account_captcha = await frame.waitForSelector('#account_captcha');
        await page.screenshot({path: 'captcha.png'});
        // 用户输入验证码
        console.log("用户输入验证码");
        request('http://127.0.0.1:8081/cnn', {json: true}, (err, res, body) => {
            if (err) {
                return console.log(err);
            }
            console.log(body);
            account_captcha.type(body);
        });
        await page.waitForTimeout(2000)
        await page.waitForTimeout(2000);
        await frame.click('div.b_f.pointer.tc.submit_btn.enable_submit_btn');
        await page.waitForTimeout(5000);

        // 判断此时的 frame 有多少个,进行搜索
        if (page.frames().length > 1) {
            console.log("多个frame,验证码失败");
            // 将错误的验证码进行一的移动,保存
            request('http://127.0.0.1:8081/error', {json: true}, (err, res, body) => {
                if (err) {
                    return console.log(err);
                }
                console.log(body);
                account_captcha.type(body);
            });
            await browser.close();
        } else {
            // 搜索数据
            console.log("跳转成功")
            const input_bar = await page.waitForSelector("#searchInputWrap > div:nth-child(1) > div > textarea")
            input_bar.type("涨停");
            await page.waitForTimeout(2000);
            await page.keyboard.press('Enter');
            await page.waitForTimeout(5000);

            //点击导出数据
            // await page.evaluate(() => {
            //     document.getElementsByClassName('table-icon exp-icon')[0].click()
            // });
            // await page.waitForTimeout(1000);
            // await page.screenshot({path: 'download.png'});
            // console.log("导出成功");
            // 将成功的验证码进行移动保存
            request('http://127.0.0.1:8081/success', {json: true}, (err, res, body) => {
                if (err) {
                    return console.log(err);
                }
                console.log(body);
                account_captcha.type(body);
            });
            await browser.close();
            break;
        }

    }
})();