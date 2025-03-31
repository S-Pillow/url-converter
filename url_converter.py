import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPlainTextEdit, QPushButton, QLabel,
    QVBoxLayout, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl

# Define transformation rules

# Sanitizing rules:
SANITIZE_RULES = [
    (r'\s+', ''),  # remove internal spaces
    (r'^https?', lambda m: 'hXXps' if m.group(0).lower() == 'https' else 'hXXp'),
    (r'\.', '[.]'),
]

# Unsanitizing rules:
UNSANITIZE_RULES = [
    (r'\s+', ''),
    (r'^hXXps?', lambda m: 'https' if m.group(0).lower() == 'hxxps' else 'http'),
    (r'\[\.\]', '.'),
    (r'\[://\]', '://'),
]

def apply_rules(text, rules):
    """Apply a series of pattern/replacement rules to a text."""
    for pattern, repl in rules:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE) if not callable(repl) else re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text

class URLConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('URL Converter')

        main_layout = QVBoxLayout()

        self.input_area = QPlainTextEdit(self)
        self.input_area.setPlaceholderText("Enter URLs here (one per line, max 100)")
        main_layout.addWidget(self.input_area)

        button_layout = QHBoxLayout()

        self.sanitize_button = QPushButton('Sanitize', self)
        self.sanitize_button.clicked.connect(self.sanitize_urls)
        button_layout.addWidget(self.sanitize_button)

        self.unsanitize_button = QPushButton('Unsanitize', self)
        self.unsanitize_button.clicked.connect(self.unsanitize_urls)
        button_layout.addWidget(self.unsanitize_button)

        self.extract_domains_button = QPushButton('Extract Domains', self)
        self.extract_domains_button.clicked.connect(self.extract_domains)
        button_layout.addWidget(self.extract_domains_button)

        self.clear_button = QPushButton('Clear Text', self)
        self.clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        self.output_area = QPlainTextEdit(self)
        self.output_area.setPlaceholderText("Processed URLs will appear here...")
        self.output_area.setReadOnly(True)
        main_layout.addWidget(self.output_area)

        # Add hyperlink label
        self.credit_label = QLabel('<a href="https://steven-pillow.com/" style="color: gray; font-size: 8px;">By Pillow</a>', self)
        self.credit_label.setOpenExternalLinks(True)
        self.credit_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.credit_label)

        self.setLayout(main_layout)
        self.setGeometry(100, 100, 1000, 800)

    def sanitize_urls(self):
        input_urls = self.input_area.toPlainText().splitlines()[:100]
        sanitized_urls = [apply_rules(url.strip(), SANITIZE_RULES) for url in input_urls if url.strip()]
        self.output_area.setPlainText('\n'.join(sanitized_urls) if sanitized_urls else 'No URLs to sanitize.')

    def unsanitize_urls(self):
        input_urls = self.input_area.toPlainText().splitlines()[:100]
        corrected_urls = [apply_rules(url.strip(), UNSANITIZE_RULES) for url in input_urls if url.strip()]
        self.output_area.setPlainText('\n'.join(corrected_urls) if corrected_urls else 'No valid URLs converted.')

    def extract_domains(self):
        input_urls = self.input_area.toPlainText().splitlines()[:100]
        domains = set()

        for url in input_urls:
            original_url = url.strip()
            if not original_url:
                continue

            match = re.match(r'^(?:https?://)?([^/]+)', original_url, flags=re.IGNORECASE)
            if match:
                full_domain = match.group(1).lower()
                domain_parts = full_domain.split('.')
                if len(domain_parts) > 2:
                    domain = '.'.join(domain_parts[-2:])  # Extract only the last two parts (1st level domain)
                else:
                    domain = full_domain
                domains.add(domain)

        self.output_area.setPlainText('\n'.join(domains) if domains else 'No valid domains extracted.')

    def clear_text(self):
        self.input_area.clear()
        self.output_area.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = URLConverter()
    ex.show()
    sys.exit(app.exec_())

