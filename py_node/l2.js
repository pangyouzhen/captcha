const puppeteer = require('puppeteer');
const readline = require('readline');

// 用户输入验证码函数
async function readLine() {

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    return new Promise(resolve => {

        rl.question('Enter captcha: ', (answer) => {
            rl.close();
            resolve(answer)
        });
    })
}

(async () => {
    const browser = await puppeteer.launch({headless: true, args: ['--start-maximized'],});
    const page = await browser.newPage();
//   跳过反扒检测
    await page.evaluateOnNewDocument(() => {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
    });
    await page.setUserAgent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36");
    await page.goto('https://www.iwencai.com');
    // 显示悬浮登陆
    await page.hover('div.login-box.auto_width > i');
    // 点击登陆
    await page.evaluate(() => {
        document.getElementsByClassName('to-pay-btn title1 f14 fb tc pointer white_text')[0].click()
    });

    await page.waitForTimeout(4000)
    //一共三层iframe,没有timewait的第三层不会渲染完成
    const frame = await page.frames()[2]
    const text = await frame.$eval('#to_account_login', (element) => element.textContent);
    console.log(text);
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
    const captcha = await readLine();
    account_captcha.type(captcha);
    await page.waitForTimeout(2000);
    await frame.click('div.b_f.pointer.tc.submit_btn.enable_submit_btn');
    await page.waitForTimeout(5000);

    // 判断此时的 frame 有多少个,进行搜索
    if (page.frames().length > 1) {
        console.log("多个frame,验证码失败");
    } else {
        // 搜索数据
        console.log("跳转成功")
        const input_bar = await page.waitForSelector("#searchInputWrap > div:nth-child(1) > div > textarea")
        input_bar.type("涨停");
        await page.waitForTimeout(2000);
        await page.keyboard.press('Enter');
        await page.waitForTimeout(5000);

        //点击导出数据
        await page.evaluate(() => {
            document.getElementsByClassName('table-icon exp-icon')[0].click()
        });
        await page.waitForTimeout(1000);
        await page.screenshot({path: 'download.png'});
        console.log("导出成功");
    }
    await browser.close();
})();