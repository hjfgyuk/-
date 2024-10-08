import requests
import bs4
import re
import asyncio
from pyppeteer import launch
import logging

 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': 'cna=s0pgHhOYmH4CAbfHGmyPphWO; lgc=tb689790719; t=e5a299de61b87074452deab6b795ac00; tracknick=tb689790719; thw=cn; mt=ci=-1_0; cookie2=1d4d5254ec1ba74b7053064c1fd82983; _tb_token_=3b13ed763ede7; mtop_partitioned_detect=1; _m_h5_tk=c10619f38334ff2bf75cdb8e78770db1_1709476385175; _m_h5_tk_enc=149bd3df9f7727e715fbb0e33b28b48a; _samesite_flag_=true; 3PcFlag=1709467390385; sgcookie=E100odpWLuezrhV36aA1r7zGqDnbLtgO%2BYBEX6vizuEbMqA6iW5Io%2BHxDEVQViysEFPbauMyeybWCgKTc0dmVw2t9bN0QwSjgTxLxGFjdxjJ1ro%3D; unb=2208625401184; uc1=cookie14=UoYenMkfIiZDew%3D%3D&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&pas=0&cookie21=UIHiLt3xTIkz; uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=F5RDJLZq6ZJGLo4%3D&id2=UUphwoF2mIUtd82C8g%3D%3D&vt3=F8dD3enXMPXwhfYntE4%3D; csg=e133140c; cancelledSubSites=empty; cookie17=UUphwoF2mIUtd82C8g%3D%3D; dnk=tb689790719; skt=7b452f70ba13bbad; existShop=MTcwOTQ2NzM5NQ%3D%3D; uc4=id4=0%40U2grGRlKQP9%2BB7t7aZO%2FCRMClPN%2BDVxS&nk4=0%40FY4I57OrPEyhjzV142ydJIl4WcPQtA%3D%3D; _cc_=U%2BGCWk%2F7og%3D%3D; _l_g_=Ug%3D%3D; sg=942; _nk_=tb689790719; cookie1=W5iSujXFYoUu8r0yj7wZ0t4XlTsTZCfybTYqnXieytE%3D; tfstk=eIeBn4x7feYQvVOH5wsacZl9bAH5by62R3i8mupe2vHKy5Z0P2SltvPsPPUsJpShtb37-vhuT4uEPYZulG7V3tr3xY0RuZW2ozg0AYBC718axkDkjWEuBZrHFE40RMXW8abNEuW2Cdpof2qTmexBARitrqZQDcmgCuGIkt0MeDwsAXgYvgRp3qZyZQtsiLisuGs6ZQv2Egi-auIEmXniAAs1feMt9cmsuGs6ZQcKjcR1fGTIB; isg=BPj4FgK16b8JsgVK9IfjSbAxyaaKYVzrYDm8eTJpRDPmTZg32nEsew5rBcV9BhTD'

}

my_index_url ='https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?jsv=2.6.2&appKey=12574478&t=1709467399677&sign=3bc0f2f0fe75f523df8a41b98a3ffe18&api=mtop.relationrecommend.WirelessRecommend.recommend&v=2.0&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22appId%22%3A%2234385%22%2C%22params%22%3A%22%7B%5C%22device%5C%22%3A%5C%22HMA-AL00%5C%22%2C%5C%22isBeta%5C%22%3A%5C%22false%5C%22%2C%5C%22grayHair%5C%22%3A%5C%22false%5C%22%2C%5C%22from%5C%22%3A%5C%22nt_history%5C%22%2C%5C%22brand%5C%22%3A%5C%22HUAWEI%5C%22%2C%5C%22info%5C%22%3A%5C%22wifi%5C%22%2C%5C%22index%5C%22%3A%5C%224%5C%22%2C%5C%22rainbow%5C%22%3A%5C%22%5C%22%2C%5C%22schemaType%5C%22%3A%5C%22auction%5C%22%2C%5C%22elderHome%5C%22%3A%5C%22false%5C%22%2C%5C%22isEnterSrpSearch%5C%22%3A%5C%22true%5C%22%2C%5C%22newSearch%5C%22%3A%5C%22false%5C%22%2C%5C%22network%5C%22%3A%5C%22wifi%5C%22%2C%5C%22subtype%5C%22%3A%5C%22%5C%22%2C%5C%22hasPreposeFilter%5C%22%3A%5C%22false%5C%22%2C%5C%22prepositionVersion%5C%22%3A%5C%22v2%5C%22%2C%5C%22client_os%5C%22%3A%5C%22Android%5C%22%2C%5C%22gpsEnabled%5C%22%3A%5C%22false%5C%22%2C%5C%22searchDoorFrom%5C%22%3A%5C%22srp%5C%22%2C%5C%22debug_rerankNewOpenCard%5C%22%3A%5C%22false%5C%22%2C%5C%22homePageVersion%5C%22%3A%5C%22v7%5C%22%2C%5C%22searchElderHomeOpen%5C%22%3A%5C%22false%5C%22%2C%5C%22search_action%5C%22%3A%5C%22initiative%5C%22%2C%5C%22sugg%5C%22%3A%5C%22_4_1%5C%22%2C%5C%22sversion%5C%22%3A%5C%2213.6%5C%22%2C%5C%22style%5C%22%3A%5C%22list%5C%22%2C%5C%22ttid%5C%22%3A%5C%22600000%40taobao_pc_10.7.0%5C%22%2C%5C%22needTabs%5C%22%3A%5C%22true%5C%22%2C%5C%22areaCode%5C%22%3A%5C%22CN%5C%22%2C%5C%22vm%5C%22%3A%5C%22nw%5C%22%2C%5C%22countryNum%5C%22%3A%5C%22156%5C%22%2C%5C%22m%5C%22%3A%5C%22pc%5C%22%2C%5C%22page%5C%22%3A%5C%221%5C%22%2C%5C%22n%5C%22%3A48%2C%5C%22q%5C%22%3A%5C%22%25E7%259B%25B8%25E6%259C%25BA%5C%22%2C%5C%22tab%5C%22%3A%5C%22all%5C%22%2C%5C%22pageSize%5C%22%3A48%2C%5C%22totalPage%5C%22%3A100%2C%5C%22totalResults%5C%22%3A4800%2C%5C%22sourceS%5C%22%3A%5C%220%5C%22%2C%5C%22sort%5C%22%3A%5C%22_coefp%5C%22%2C%5C%22bcoffset%5C%22%3A%5C%22%5C%22%2C%5C%22ntoffset%5C%22%3A%5C%22%5C%22%2C%5C%22filterTag%5C%22%3A%5C%22%5C%22%2C%5C%22service%5C%22%3A%5C%22%5C%22%2C%5C%22prop%5C%22%3A%5C%22%5C%22%2C%5C%22loc%5C%22%3A%5C%22%5C%22%2C%5C%22start_price%5C%22%3Anull%2C%5C%22end_price%5C%22%3Anull%2C%5C%22startPrice%5C%22%3Anull%2C%5C%22endPrice%5C%22%3Anull%2C%5C%22itemIds%5C%22%3Anull%2C%5C%22p4pIds%5C%22%3Anull%7D%22%7D'

async def get_detail(index_url):
    logging.info('正在爬取商品列表页')
    response = requests.get(index_url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, features="lxml")

    print(soup.prettify())
    urls = re.findall(r'"auctionURL":"(.*?)"', soup.prettify(), re.S)  # 获取详情页
    return urls


async def get_evaluations(detail_url):
    await asyncio.sleep(1)  # 点击过快好像会提前触发淘宝反爬，所以设置了时间间隔
    browser = await launch(headless=False, devtools=False, args=[f'--window-size={1366},{768}', ],
                           userDataDir=r'D:\python1\bug\基础知识\userdata_taobao_search', )  # 这里的文件路径需要重新设置一下
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})  # 调整页面大小
    await page.evaluateOnNewDocument(
        'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})')  # 隐蔽webdriver属性
    await page.goto('https:' + detail_url)
    await asyncio.sleep(1000)  # 等待加载页面
    name = re.findall(r"<title>(.*?)</title>", await page.content(), re.S) if re.findall(r"<title>(.*?)</title>",
                                                                                         await page.content(),
                                                                                         re.S) else None
    store = re.findall(r'class="ShopHeader--title--2qsBE1A".*?title="(.*?)"', await page.content(), re.S) if re.findall(
        r'class="ShopHeader--title--2qsBE1A".*?title="(.*?)"', await page.content(), re.S) else None
    button = await page.querySelector('.Comments--tabDetailItemTitle--2BFfLMr')
    await button.click()
    await button.click()
    await asyncio.sleep(2)
    await page.evaluate("""{window.scrollBy(0, document.body.scrollHeight);}""")
    await asyncio.sleep(2)
    print(page.content())
    evaluations = re.findall(r'<div class="Comment--content--22pGCmW">(.*?)</div>', await page.content(),
                             re.S) if re.findall(r'<div class="Comment--content--22pGCmW">(.*?)</div>',
                                                 await page.content(), re.S) else None
    photo = re.findall('<img data-once="true" src="(.*?)"', await page.content(), re.S) if re.findall(
        r'<img data-once="true" src="(.*?)"', await page.content(), re.S) else None
    logging.info('已完成对%s店铺的%s的爬取,评论为%s', store, name, evaluations)

    for i, m in zip(photo, range(0, 10)):
        with open(r"D:\python1\bug\bug_exercise\taobao_photo\{n}_{m}.jpg".format(m=m,n=name), "wb") as b:
            r = requests.get('https:' + i)
            b.write(r.content)
    await browser.close()
    return {
        'name': name,
        'store': store,
        'evaluations': evaluations
    }


async def main():
    urls = await get_detail(my_index_url)
    print(urls)
    with open('goods.txt', 'a', encoding='utf-8') as gd:
        for url in urls[3:]:  # 有时候urls会爬取一些其他商品的网址为此并没有从第一个开始
            a = await get_evaluations(url)
            gd.write(str(a) + '\n')
            logging.info('已获取商品内容')


if __name__ == '__main__':
    print('初次使用需手动登陆一下淘宝账户并更改一下cookie和url（为此需将时间间隔先延长一下以方便登录），'
          '在爬取大约30左右的商品数据时，淘宝页面会要求再次登陆账户或滑动验证，由于本人技术有限，目前还仍无法解决')
    asyncio.get_event_loop().run_until_complete(main())
