from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import docx


class DownloadDocx(object):

    @staticmethod
    def download(url):
        options = ChromeOptions()
        # 无界 Chrome 运行
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1366,768')
        # UA 设置为 移动端
        options.add_argument(
            'user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        # 若
        html = driver.page_source
        title = driver.find_element_by_class_name('doc-title').text
        try:
            flod_page_text = driver.find_element_by_class_name('foldpagewg-text')
            driver.execute_script("arguments[0].click();", flod_page_text)  # 先点击一次
            process = driver.find_element_by_class_name('pagerwg-schedule').text[2:4]  # 获取文章进度
            html = driver.page_source
            # 点击到最后一页时，元素为空 所以 process 的值为 None  所以不用做过多处理
            while process:
                process = driver.find_element_by_class_name('pagerwg-schedule').text[2:4]  # 进度大于 10 %
                if flod_page_text is not None:
                    load_more_content = driver.find_element_by_class_name('pagerwg-button')
                    if load_more_content is not None:
                        driver.execute_script("arguments[0].click();", load_more_content)
                        html = driver.page_source  # 如果内容过多，重新赋值
        except:
            print("因文档内容不够，未能加载点击按钮")

        soup = BeautifulSoup(html, 'lxml')
        page_elements = soup.find_all(class_='rtcspage')
        doc = docx.Document()  # word 文档对象
        for page_element in page_elements:
            # 获取到所有的分页
            # 获取每一页所有的段落  并写入 word 文档
            paragraphs = page_element.find_all('p')
            for paragraph in paragraphs:
                doc.add_paragraph(paragraph.text)

        # 保存文档
        doc.save(title + '.docx')
        # 结束 浏览器运行  释放掉内存
        driver.quit()
