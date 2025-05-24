# 🔐 Dynamic Graphical Password Authentication System

A secure and user-friendly Django-based authentication system that replaces traditional text-based login with a graphical password mechanism. Users upload their own images and choose specific click-points as their password, making authentication more intuitive and harder to guess.

---

## 🧠 Why Graphical Passwords?

Traditional text passwords can be hard to remember and are prone to common attacks like brute force and dictionary-based guessing. This project offers a more natural alternative by:
- Relying on human visual memory
- Allowing users to choose memorable points on an image
- Increasing password complexity and entropy

---

## 🚀 Features

- 📸 Upload custom images for password registration
- 🖱️ Select multiple click-points as graphical passwords
- 🔐 Secure login using the same image and click sequence
- 🎯 Tolerance mechanism for minor variations in click positions
- 🧩 Personalized user experience with improved security

---

## ⚙️ Tech Stack

- **Backend Framework:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript 
- **Database:** MySQL
- **Image Handling:** Pillow (PIL) for processing uploads

---

## 🛠 How It Works

### Registration Flow
1. User signs up by entering basic credentials.
2. User uploads an image of their choice.
3. User clicks on **up to 4 points** on the image to set as their graphical password.
4. Image and encrypted coordinates are saved to the database.

### Login Flow
1. User enters their credentials.
2. The **same uploaded image** is automatically displayed (no need to re-upload).
3. User clicks on the same points used during registration.
4. The system checks if the clicked coordinates match (within a tolerance range) and logs the user in.

---

## 🛡️ Security Measures

- Password data (click-points) stored as encrypted coordinate sets
- Tolerance radius prevents exact click dependency while preserving security
- Can be enhanced with CAPTCHA, session timeouts, and multi-factor authentication

---

