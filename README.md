# <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/LINE_logo.svg/2048px-LINE_logo.svg.png" width="30px" height="auto" /> LineBankVerify

This project is created to extract transaction data from messages sent by banks via the LINE chat application, and save the transactions to a text file.

## 🛠️Develop on Python

## 🚀 Installation
```bash
# Clone git
git clone https://github.com/SilSea/LineBankVerify.git
cd LineBankVerify

```

## 📦Package Requirement
```bash
# Install Pytest and Playwright
pip install pytest-playwright
playwright install
pip install pillow
```

## ⚙️Config setting.txt file to use login Line Application <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/LINE_logo.svg/2048px-LINE_logo.svg.png" width="30px" height="auto" />

(You can login using a QR code by providing a file with the name ending in 'QR')

```bash
email : "input email here"
password : "input password here"
```

## 🚀Run Command (Change name same file Bank You Use)
```bash
pytest krungthai.py
```

## 🏛️Bank Support

### 1.Krungthai ✅

### 2.Kasikornbank ❌

### 3.SCB ❌

### 4.GSB ❌

## 📦Features

### 1.Login Line ✅

### 2.ReadMessage from Line ✅

### 3.GetTransaction from Line ✅

### 4.Save to Textfile ✅
