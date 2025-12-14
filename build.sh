#!/bin/bash
set -e

echo "🔹 Creating virtual environment..."
# Check if venv exists to avoid recreation
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

echo "🔹 Installing dependencies..."
pip install -r requirements.txt

echo "🔹 Cleaning previous build..."
rm -rf build dist

echo "🔹 Building MechKeys.app..."
python setup.py py2app

echo "✅ Build Complete!"
echo "Your app is located in the 'dist' folder: dist/MechKeys.app"
echo ""
echo "👉 To Update: Drag 'dist/MechKeys.app' to your Applications folder (Replace existing)."