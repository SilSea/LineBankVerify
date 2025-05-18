import os
import subprocess
import getpass

# Get the bank path
bank_path = os.path.join(os.path.dirname(__file__), "bank")

def run_test(file_path):
    if os.path.exists(file_path):
        print("Press Ctrl+C to stop the Program.")
        subprocess.run(["pytest", file_path])
    else:
        print("This function is currently unavailable.")

def bank_menu(select):
    # Clear the screen
    subprocess.run("cls", shell=True)

    # Select Bank
    print("Select Bank")
    print("1. Krungthai")
    print("2. Kbank")
    print("3. SCB")
    print("4. GSB")
    bank_select = input("Select Bank: ")

    # Map bank selection to file names
    banks = {
        "1": "krungthai",
        "2": "kbank",
        "3": "scb",
        "4": "gsb"
    }

    # Invalid selection handling
    if bank_select not in banks:
        print("Invalid selection. Please try again.")
        return

    # Get the bank name based on selection
    bank_name = banks[bank_select]

    # Determine file based on login type
    if select == "1" or select == "3":
        filename = f"{bank_name}.py"
    elif select == "2":
        filename = f"{bank_name}_QR.py"
    else:
        print("Invalid login type.")
        return

    # Run pytest
    file_path = os.path.join(bank_path, filename)
    run_test(file_path)

def main():
    subprocess.run("cls", shell=True)
    # Select Function
    print("Welcome to LineBankVerify")
    print("1. Login with Email and Password")
    print("2. Login with QR Code")
    print("3. Login with recently used account (if you have logged in before with email and password)")
    login_select = input("Select Menu: ")

    # Login with Email and Password
    if login_select == "1":
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")

        # Save to setting.txt
        content = f'email : "{email}"\npassword : "{password}"'
        with open("setting.txt", "w", encoding="utf-8") as file:
            file.write(content)
        # Call the function
        bank_menu(login_select)

    # Login with QR Code
    elif login_select == "2":
        # Call the function
        bank_menu(login_select)

    elif login_select == "3":
        # Call the function
        bank_menu(login_select)

    else:
        print("Invalid selection. Please try again.")

main()
