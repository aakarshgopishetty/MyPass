# 🔐 MyPass - Your Secure Password Manager

**MyPass** is a simple and secure password manager that helps you generate, store, and manage strong passwords. It ensures your passwords are safe using encryption and provides strength analysis and suggestions for creating more secure passwords.

## 🚀 Features

- 🔒 Secure password storage with encryption
- 📈 Password strength checker and suggestions
- 🔑 Random strong password generator
- 🌐 Option to use as a browser extension *(coming soon)*
- 📁 Export/Import passwords (encrypted format)
- 🔐 Master password protection

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python
- **Database**: LocalStorage (for browser extension)
- **Security**: AES encryption (crypto-js / libsodium / other)
- **Others**: bcrypt (for hashing master password)


## 🧠 How It Works

1. **User creates a master password** – it's hashed and used to unlock the vault.
2. **Passwords are encrypted** with AES and stored securely.
3. **Strength checker** gives real-time feedback on new passwords.
4. **Password generator** helps users create strong passwords on demand.

## 📦 Installation

### For Web App

```bash
git clone https://github.com/aakarshgopishetty/MyPass.git
cd mypass
