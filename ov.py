from playwright.sync_api import sync_playwright
import os
css="@font-face{font-family:A;src:url(Amiri-700-arabic.woff2)}body{margin:0;background:transparent;width:1080px;height:1920px;font-family:A;direction:rtl;color:#f0d48f;text-align:center;text-shadow:0 4px 24px #000,0 0 8px #000}.p{position:absolute;left:0;right:0;text-align:center}.band{background:linear-gradient(transparent,rgba(10,5,2,.78) 35%);padding:80px 0 30px}small{display:block;font-size:44px;color:#e6d2a4}"
items={
 "h":"<div class=p style='top:1300px;font-size:92px'>ما عدتُ أحتمل ضغط العمل</div>",
 "n1":"<div class=p style='top:1380px;font-size:130px'>ابن القيم<small>٦٩١ – ٧٥١ هـ</small></div>",
 "n2":"<div class=p style='top:1380px;font-size:130px'>ابن تيمية<small>٦٦١ – ٧٢٨ هـ</small></div>",
 "n3":"<div class=p style='top:1380px;font-size:130px'>ابن خلدون<small>٧٣٢ – ٨٠٨ هـ</small></div>",
 "n4":"<div class=p style='top:1380px;font-size:130px'>ابن سينا<small>٣٧٠ – ٤٢٨ هـ</small></div>",
 "cap":"<div class=p style='top:1625px;font-size:56px;color:#f3e3bd'>همّك: «ما عدتُ أحتمل ضغط العمل»</div><div class=p style='top:1720px;font-size:36px;color:#cdb98d'>الردود بالذكاء الاصطناعي · صور تخيّلية</div>",
}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1920})
    for k,h in items.items():
        open(k+".html","w").write(f"<meta charset=utf-8><style>{css}</style>{h}")
        pg.goto("file://"+os.getcwd()+"/"+k+".html"); pg.wait_for_timeout(400); pg.screenshot(path=k+".png",omit_background=True)
    b.close()
