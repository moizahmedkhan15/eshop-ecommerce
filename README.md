# 🛍️ eShop - Django + Python E-Commerce Project

A fully functional eCommerce website built with Django and Python. This project includes features like user authentication, cart system, order checkout, and admin dashboard.

## 🔧 Features

- User registration & login
- Product listing & filtering
- Shopping cart
- Order checkout
- Admin panel to manage products and orders

## 🚀 Tech Stack

- Python 3
- Django Framework
- HTML, CSS, JavaScript
- Bootstrap (or any CSS framework you used)

## 📁 Project Structure

- `/eshop` – Main Django app
- `/templates` – HTML templates
- `/static` – Static files (CSS/JS/images)
- `manage.py` – Django project runner

## ▶️ Run Locally

```bash
git clone https://github.com/moizahmedkhan15/eshop-ecommerce.git
cd eshop-ecommerce
python -m venv env
env\Scripts\activate   # or source env/bin/activate on Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
