import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPlainTextEdit, QPushButton,
    QVBoxLayout, QMessageBox, QHBoxLayout
)

class URLConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('URL Converter')

        # Create main layout
        main_layout = QVBoxLayout()

        # Create plain text area for input URLs
        self.input_area = QPlainTextEdit(self)
        self.input_area.setPlaceholderText("Enter URLs here (one per line, max 100)")
        main_layout.addWidget(self.input_area)

        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create button to sanitize URLs
        self.sanitize_button = QPushButton('Sanitize', self)
        self.sanitize_button.clicked.connect(self.sanitize_urls)
        button_layout.addWidget(self.sanitize_button)

        # Create button to unsanitize URLs
        self.unsanitize_button = QPushButton('Unsanitize', self)
        self.unsanitize_button.clicked.connect(self.unsanitize_urls)
        button_layout.addWidget(self.unsanitize_button)

        # Create button to clear text
        self.clear_button = QPushButton('Clear Text', self)
        self.clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        # Create plain text area for output URLs
        self.output_area = QPlainTextEdit(self)
        self.output_area.setPlaceholderText("Processed URLs will appear here...")
        self.output_area.setReadOnly(True)
        main_layout.addWidget(self.output_area)

        self.setLayout(main_layout)

        # Set the window size
        self.setGeometry(100, 100, 1000, 800)

    def sanitize_urls(self):
        input_urls = self.input_area.toPlainText().splitlines()[:100]
        sanitized_urls = []

        for url in input_urls:
            original_url = url.strip()
            if not original_url:
                continue  # Skip empty lines

            # Remove spaces within the URL
            sanitized_url = re.sub(r'\s+', '', original_url)

            # Replace http and https with hXXp and hXXps
            sanitized_url = re.sub(
                r'^https?',
                lambda m: 'hXXps' if m.group(0).lower() == 'https' else 'hXXp',
                sanitized_url,
                flags=re.IGNORECASE
            )

            # Replace . with [.]
            sanitized_url = sanitized_url.replace('.', '[.]')

            sanitized_urls.append(sanitized_url)

        self.output_area.setPlainText('\n'.join(sanitized_urls) if sanitized_urls else 'No URLs to sanitize.')

    def unsanitize_urls(self):
        input_urls = self.input_area.toPlainText().splitlines()[:100]
        corrected_urls = []
        invalid_urls = []

        for url in input_urls:
            original_url = url.strip()
            if not original_url:
                continue  # Skip empty lines

            # Remove spaces within the URL
            corrected_url = re.sub(r'\s+', '', original_url)

            # Replace hXXp and hXXps with http and https
            corrected_url = re.sub(
                r'^hXXps?',
                lambda m: 'https' if m.group(0).lower() == 'hxxps' else 'http',
                corrected_url,
                flags=re.IGNORECASE
            )

            # Replace [.] with .
            corrected_url = corrected_url.replace('[.]', '.')

            # Extract the domain up to the TLD for validation
            domain_match = re.match(r'^(https?://)?([^/\s]+)', corrected_url, flags=re.IGNORECASE)
            if domain_match:
                domain = domain_match.group(2)

                # Validate the domain using a simple regex
                domain_regex = re.compile(
                    r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
                )
                if domain_regex.match(domain):
                    # The domain is valid, keep the entire URL including paths
                    corrected_urls.append(corrected_url)
                else:
                    # Invalid domain, include the original URL in the error message
                    invalid_urls.append(original_url)
            else:
                # No domain found, include the original URL in error message
                invalid_urls.append(original_url)

        if invalid_urls:
            QMessageBox.warning(
                self,
                'Invalid URLs',
                'The following URLs could not be processed:\n' + '\n'.join(invalid_urls),
                QMessageBox.Ok
            )

        self.output_area.setPlainText('\n'.join(corrected_urls) if corrected_urls else 'No valid URLs converted.')

    # Define the clear_text method
    def clear_text(self):
        self.input_area.clear()
        self.output_area.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = URLConverter()
    ex.show()
    sys.exit(app.exec_())
