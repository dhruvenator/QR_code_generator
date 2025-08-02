#!/bin/bash
cd ..
zip -r qr_code.zip . -x "*.git*" "*.DS_Store" "*.vscode*" "node_modules/*" "dist/*" "build/*" "coverage/*" "logs/*" "*.log" "*.tmp" "*.bak" "*.swp" "scripts/*" "*__pycache__*" "*.pyc" "*.pyo" "*.pyd" "venv/*" "env/*" "test/*" "tests/*" "docs/*" "examples/*" "assets/*" "images/*" "fonts/*" "data/*"