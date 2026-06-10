#!/bin/bash
echo "============================================"
echo "  ShopEase E-Commerce - Setup & Run"
echo "============================================"

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -q
python3 seed.py

echo ""
echo "============================================"
echo "  App running at: http://127.0.0.1:8000"
echo "  Admin: admin@shop.com / 1234567@"
echo "  Press Ctrl+C to stop"
echo "============================================"
uvicorn main:app --reload --host 127.0.0.1 --port 8000
