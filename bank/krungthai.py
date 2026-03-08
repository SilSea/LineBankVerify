from playwright.sync_api import sync_playwright
import os
import time

# Search path from file
file_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(file_dir)
# Setting path for extension
extension_path = os.path.join(base_dir, "extension", "ophjlpahpchlmihnnnihgmmeilfjmjjc", "3.6.1_0")
# Setting path for tmp/user_data collection temporary
user_data_dir = os.path.join(base_dir, "tmp", "user_data")

def test_krungthai():
    with sync_playwright() as p:
        # Setting Playwright use Chromium and load extension Line
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ]
        )

        # Open tab Line
        page = context.new_page()
        page.goto("chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html#", wait_until="commit")

        print("รอการล็อกอิน... กรุณาสแกน QR Code หรือใส่อีเมล/รหัสผ่านบนเบราว์เซอร์")

        # รอจนกว่าผู้ใช้จะล็อกอินสำเร็จ โดยรอให้ปุ่มแชทปรากฏ (timeout=0 คือรอแบบไม่มีกำหนดเวลา)
        find_chat = page.wait_for_selector('[aria-label="Chat"]', timeout=0)
        print("ล็อกอินสำเร็จ! กำลังเข้าสู่แชท Krungthai Connext...")
        find_chat.click()
        
        # Wait 3 seconds for the page to load
        time.sleep(3)
        
        # Search Chat Krungthai Connext
        krungthai_chat = page.wait_for_selector("span:text('Krungthai Connext')")
        # Find parentElement from text "Krungthai Connext"
        current_element = krungthai_chat
        for _ in range(5):
            current_element = current_element.evaluate_handle("e => e.parentElement")
        # Search all button in parentElement
        krungthai_chat_open = current_element.query_selector_all("button")
        # Click button open chat
        krungthai_chat_open[1].click()

        # Wait 5 seconds for the page to load
        time.sleep(5)

        # Find all element attribute data-message-content start with text "เงินเข้า"
        locator = page.locator("xpath=//*[starts-with(@data-message-content, 'เงินเข้า')]")
        # Count all element found
        last_count = locator.count()  
        
        # Check element start with text "เงินเข้า"
        assert last_count > 0, "ไม่พบ element ที่ขึ้นต้นด้วย 'เงินเข้า'"
        print(f"พบประวัติเงินเข้า {last_count} รายการ กำลังเริ่มระบบ Monitoring...")

        # จัดการโฟลเดอร์ logs ให้แน่ใจว่าถูกสร้างไว้แล้ว
        log_path = os.path.join(base_dir, "logs", "transaction_krungthai.txt")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Write data to transaction_krungthai.txt
        with open(log_path, "w", encoding="utf-8") as f:
            for i in range(last_count):
                content_div = locator.nth(i).locator("div.content")
                # Search span all in div.content
                spans = content_div.first.locator("span")
                span_count = spans.count()

                # Combine span with comma
                texts = []
                for j in range(span_count):
                    text = spans.nth(j).inner_text().strip()
                    if text:
                        texts.append(text)

                # Write to file
                f.write(",".join(texts) + "\n")

        try:
            # Loop check new message
            while True:
                time.sleep(5)
                # Check new message every 5 seconds
                current_count = locator.count()

                # If have new message เงินเข้า
                if current_count > last_count:
                    # New data
                    new_lines = []
                    for i in range(last_count, current_count):
                        try:
                            # Get all data from element
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
                            print(f"รายการใหม่เข้า: {line}")

                        except Exception as e:
                            print(f"เกิดข้อผิดพลาดในการอ่านข้อความใหม่: {e}")

                    # Read old file if have
                    try:
                        with open(log_path, "r", encoding="utf-8") as f:
                            old_lines = f.readlines()
                    except FileNotFoundError:
                        old_lines = []

                    # Write new data and new data to top
                    with open(log_path, "w", encoding="utf-8") as f:
                        for line in new_lines:
                            f.write(line + "\n")
                        f.writelines(old_lines)
                    
                    # Update last_count to check new message
                    last_count = current_count
            
        except KeyboardInterrupt:
            print("\nตรวจพบ Ctrl+C - กำลังปิด browser...")

        finally:
            context.close()