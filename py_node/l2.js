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
    // console.log('waiting for iframe with form to be ready.');
    // await page.waitForSelector('iframe');
    // console.log('iframe is ready. Loading iframe content');
    // const elementHandle = await page.$(
    //     '#login_iframe',
    // );
    // const frame = await elementHandle.contentFrame();
    // console.log(frame);
    // await frame.type('#Name', 'Bob', { delay: 100 });
    // await console.log(page.frames());
    // const targetFrameUrl = 'http://upass.iwencai.com/login';
    // await console.log(page.frames().length);
    // console.log(page.frames())
    // console.log(page.frames())

    // const frame = await page.frames().find(frame => frame.url().includes(targetFrameUrl));
    const frame = await page.frames()[2]
    // console.log(frame)
    // await frame.evaluate(() => {
    //     console.log(document);
    //     document.querySelector('#to_account_login').textContent;
    // });

    // await frame.waitFor('#to_account_login');
    // console.log(frame)
    const text = await frame.$eval('#to_account_login', (element) => element.textContent);
    console.log(text);
    // const phone = await frame.waitForSelector('#mobile');
    // phone.type('123456');
    // frame.focus("#mobile");
    // phone.click()
    // await frame.evaluate(() => {
    //     document.getElementById('to_account_login')[0].click();
    // });
    // await frame.evaluate(() => {
    //     document.querySelector('.base_bg.style_').style.display = 'yes';
    //     document.querySelector("#to_account_login").textContent;
    // });

    // const display = await frame.evaluate(() =>
    //     window.getComputedStyle(document.querySelector('#to_account_login')).display
    // );
    // for (let i = 0; i < 5; i++)
    //     console.log(i)
    // await page.keyboard.press('Tab');
    // await frame.evaluate(() => {
    //     $("#to_account_login").click();
    // console.log(document.querySelector("#to_account_login").textContent);
    // });
    // await frame.evaluate(() => {
    //     $("#to_account_login").click();
    // });
    // (await frame.$('#to_account_login')).click();
    // await console.log(frame.click('#to_account_login'));
    // await page.click();
    // await frame.focus('#to_account_login');
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