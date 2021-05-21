import csv
import time
from selenium import webdriver
# 最新のchromeのversionへ合わせるため。
from webdriver_manager.chrome import ChromeDriverManager
# タグを一括取得するために利用する。
# 参考 : https://kurozumi.github.io/selenium-python/locating-elements.html
from selenium.webdriver.common.by import By
# HTML要素がない場合のエラーハンドリング
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
# ブラウザを開くことなくバックグラウンドにて実行する。
# options.add_argument('--headless')

# Chromeを立ち上げる。
driver = webdriver.Chrome(
    ChromeDriverManager().install(), options=options)
# ブラウジングするwindow幅を設定する。
driver.set_window_size(1300, 1040)

# 診療科目と所在地から探すのページ
driver.get('http://medinf.mmic.or.jp/kensaku/kensaku_menu2.php?mode=consul')

# ページ読み込みのために遅延させる。
time.sleep(5)

# 内科のチェックをクリック
# 参考 : https://kurozumi.github.io/selenium-python/locating-elements.html
driver.find_element_by_name('chkbox1[0]').click()

# 小児科のチェックをクリック
# 参考 : https://kurozumi.github.io/selenium-python/locating-elements.html
driver.find_element_by_name('chkbox1[6]').click()

# 検索ボタンをクリック
# 参考 : https://kurozumi.github.io/selenium-python/locating-elements.html
driver.find_element_by_xpath("//input[@value='　検　索　']").click()

# ページ読み込みのために遅延させる。
time.sleep(5)

# 最終的なcsvへ書き出すためにデータ格納する変数
output = [['医療機関略称', '所在地', '電話番号']]

# 次の25件をクリックできなくなるまでループ。(try exceptのexceptに入ったら終了)
while True:
    # 「検索条件に該当した医療機関」に対応するtbody HTMLタグを選択する。[3]はindex位置。0番から数える。
    # 参考 : https://www.k-hitorigoto.online/entry/2017/03/09/223538
    # 参考 : https://kurozumi.github.io/selenium-python/locating-elements.html
    tbody = driver.find_elements(By.TAG_NAME, "tbody")[3]
    # tbody HTML内に含まれるtr HTMLタグリストを取得する。
    # 参考 : https://kurozumi.github.io/selenium-python/locating-elements.html
    trList = tbody.find_elements(By.TAG_NAME, "tr")

    # ヘッダ行は除いてtd HTMLタグリストを取得する。
    for i in range(1, len(trList)):
        # trList[i] HTMLタグ内に含まれる、td HTMLタグリストを取得する。
        # 参考 : https://kurozumi.github.io/selenium-python/locating-elements.html
        tdList = trList[i].find_elements(By.TAG_NAME, "td")
        # 医療機関略称、所在地、電話番号を取得して、outputへ格納する。
        output.append([tdList[0].text, tdList[1].text, tdList[2].text])

    # 次の25件がなくなる場合を想定して、例外処理を行う。
    try:
        # 次の25件をクリック
        # 参考 : https://kurozumi.github.io/selenium-python/locating-elements.html
        driver.find_element_by_xpath("//input[@value='次の25件　＞＞']").click()
    # HTML要素が存在しない場合(次の25件がない)、ループを終了する。
    except NoSuchElementException:
        break

    # ページ読み込みのために遅延させる。
    time.sleep(5)

# csv書き込み処理
# 参考 : https://www.irohabook.com/python-csv-write
with open('./data.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(output)
