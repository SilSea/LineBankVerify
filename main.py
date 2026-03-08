import os
import subprocess

# Get the bank path
bank_path = os.path.join(os.path.dirname(__file__), "bank")

def run_test(file_path):
    if os.path.exists(file_path):
        print("Press Ctrl+C to stop the Program.")
        subprocess.run(["pytest", "-s", file_path]) # ใส่ -s เพื่อให้เห็นข้อความ print ใน terminal
    else:
        print("This function is currently unavailable.")

def main():
    # Clear the screen
    subprocess.run("cls", shell=True)

    print("Welcome to LineBankVerify")
    print("Please select the bank to monitor:")
    print("1. Krungthai")
    print("2. Kbank")
    print("3. SCB")
    print("4. GSB")
    
    bank_select = input("Select Bank: ")

    # Map bank selection to file names
    banks = {
        "1": "krungthai.py",
        "2": "kbank.py",
        "3": "scb.py",
        "4": "gsb.py"
    }

    if bank_select not in banks:
        print("Invalid selection. Please try again.")
        return

    filename = banks[bank_select]
    file_path = os.path.join(bank_path, filename)
    
    print("\nกำลังเปิดเบราว์เซอร์... กรุณาล็อกอิน LINE บนหน้าต่างเว็บให้เรียบร้อย")
    run_test(file_path)

if __name__ == "__main__":
    main()