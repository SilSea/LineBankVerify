from playwright.sync_api import sync_playwright
import os
import time

# กรอก Email และ Password ของ Line
email = ""
password = ""

def test_linebankverify():
    with sync_playwright() as p:

        # ทำการหา path ของไฟล์ฺ
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # ตั้งค่า path ของ extension
        extension_path = os.path.join(base_dir, "extension", "ophjlpahpchlmihnnnihgmmeilfjmjjc", "3.6.1_0")
        # ตั้งค่า path ของ tmp/user_data เพื่อเก็บข้อมูลการใช้งานชั่วคราว
        user_data_dir = os.path.join(base_dir, "tmp", "user_data")

        # กำหนดให้ Playwright ใช้ Chromium และโหลด extension Line
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ]
        )

        # เปิดหน้าเว็บที Line
        page = context.new_page()
        page.goto("chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html#", wait_until="commit")

        # เว้นระยะเวลา 3 วินาทีเพื่อให้หน้าโหลดเสร็จ
        time.sleep(3)

        # เข้าสู่ระบบ Line
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        login_button = page.wait_for_selector('span:text("Log in")')
        # ค้นหาข้อความ Log in
        current_element = login_button
        # หา parentElement ของข้อความ "Log in"
        for _ in range(2):
            current_element = current_element.evaluate_handle("e => e.parentElement")
        # หาปุ่มทั้งหมดใน parentElement
        login_button_open = current_element.query_selector_all("button")
        # กดปุ่มเพื่อเข้าสู่ระบบ
        login_button_open[0].click()

        # เว้นระยะเวลา 3 วินาทีเพื่อให้หน้าโหลดเสร็จ
        time.sleep(3)

        # เปิดหมวดช่องแชท
        find_chat = page.wait_for_selector('[aria-label="Chat"]')
        find_chat.click()
        # เว้นระยะเวลา 3 วินาทีเพื่อให้หน้าโหลดเสร็จ
        time.sleep(3)
        # ค้นหาแชท Krungthai Connext
        krungthai_chat = page.wait_for_selector("span:text('Krungthai Connext')")
        # หา parentElement ของข้อความ "Krungthai Connext"
        current_element = krungthai_chat
        for _ in range(5):
            current_element = current_element.evaluate_handle("e => e.parentElement")
        # หาปุ่มทั้งหมดใน parentElement
        krungthai_chat_open = current_element.query_selector_all("button")
        # กดปุ่มเพื่อเปิดแชท
        krungthai_chat_open[1].click()

        time.sleep(5)

        # หาทุก element ที่ attribute data-message-content เริ่มด้วย "เงินเข้า"
        locator = page.locator("xpath=//*[starts-with(@data-message-content, 'เงินเข้า')]")
        # นับจำนวน element ที่พบ
        last_count = locator.count()  # เก็บค่า count ของครั้งแรก
        # เช็คว่ามี element ที่ขึ้นต้นด้วย "เงินเข้า" หรือไม่
        assert last_count > 0, "ไม่พบ element ที่ขึ้นต้นด้วย 'เงินเข้า'"

        # เขียนข้อมูลลง transetion_history.txt
        with open("transaction_history.txt", "w", encoding="utf-8") as f:
            for i in range(last_count):
                content_div = locator.nth(i).locator("div.content")
                # ค้นหา span ทั้งหมดภายใน div.content
                spans = content_div.first.locator("span")
                span_count = spans.count()

                # รวมข้อความในแต่ละ span ด้วยเครื่องหมาย comma
                texts = []
                for j in range(span_count):
                    text = spans.nth(j).inner_text().strip()
                    if text:
                        texts.append(text)

                # เขียนผลลัพธ์ลงไฟล์
                f.write(",".join(texts) + "\n")

        try:
            # รันลูปรองเช็คการเปลี่ยนแปลงของ locator
            while True:
                time.sleep(5)
                # เช็คค่าของ locator ใหม่ทุกๆ 5 วินาที
                current_count = locator.count()

                # ถ้ามีการเพิ่มของ locator
                if current_count > last_count:
                    # เตรียมข้อมูลใหม่
                    new_lines = []
                    for i in range(last_count, current_count):
                        try:
                            # ดึงรายการใหม่ทีละรายการจริง ๆ
                            content_div = locator.nth(i).locator("div.content")
                            spans = content_div.locator("span")
                            span_count = spans.count()
                            
                            texts = []
                            for j in range(span_count):
                                text = spans.nth(j).inner_text().strip()
                                if text:
                                    texts.append(text)

                            line = ",".join(texts)
                            new_lines.append(line)

                        except Exception as e:
                            print("Error")

                    # อ่านข้อมูลเก่าจากไฟล์ (ถ้ามี)
                    try:
                        with open("transaction_history.txt", "r", encoding="utf-8") as f:
                            old_lines = f.readlines()
                    except FileNotFoundError:
                        old_lines = []

                    # เขียนใหม่ทั้งหมด โดย new อยู่ด้านบน
                    with open("transaction_history.txt", "w", encoding="utf-8") as f:
                        for line in new_lines:
                            f.write(line + "\n")
                        f.writelines(old_lines)
                    
                    # อัพเดต last_count เพื่อใช้ในการตรวจสอบรอบถัดไป
                    last_count = current_count
            
        except KeyboardInterrupt:
            print("\n ตรวจพบ Ctrl+C - กำลังปิด browser...")

        finally:
            context.close()