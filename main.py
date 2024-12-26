import sys
import os
import subprocess
import re
from datetime import datetime
from svn_worker import SVNWorker
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QLineEdit, QPushButton,
                            QProgressBar, QFileDialog, QMessageBox, QComboBox,
                            QTextEdit, QSplitter, QFormLayout, QGroupBox)
from PySide6.QtCore import Qt, QThread, Signal, QSettings
from PySide6.QtGui import QIcon
from translations import en_US, zh_CN

VERSION = "v1.1"  # Current version

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('SVNTool', 'SVNFileExporter')
        self.translations = {}
        self.initTranslations()
        self.initUI()
        self.loadSettings()
        
        # Set window icon and title with version
        icon_path = self.get_resource_path('resources/app.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle(f"{self.tr('window_title')} - {VERSION}")
        
    def get_resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
        
    def initTranslations(self):
        """Initialize translations and load the last used language"""
        self.translations = {
            'en_US': en_US.translations,
            'zh_CN': zh_CN.translations
        }
        self.current_language = self.settings.value('language', 'en_US')
        
    def tr(self, key):
        """Translate the given key to current language"""
        return self.translations[self.current_language].get(key, key)
        
    def changeLanguage(self, language):
        """Change the application language"""
        if language in self.translations and language != self.current_language:
            self.current_language = language
            self.settings.setValue('language', language)
            self.retranslateUI()
            
    def retranslateUI(self):
        """Update all UI text elements with the current language"""
        self.setWindowTitle(f"{self.tr('window_title')} - {VERSION}")
        self.url_label.setText(self.tr('svn_url'))
        self.username_label.setText(self.tr('username'))
        self.password_label.setText(self.tr('password'))
        self.filter_group.setTitle(self.tr('file_format_filter'))
        self.filter_input.setPlaceholderText(self.tr('file_format_placeholder'))
        self.excel_group.setTitle(self.tr('excel_save_location'))
        self.browse_button.setText(self.tr('choose_path'))
        self.progress_group.setTitle(self.tr('export_progress'))
        self.progress_bar.setFormat(self.tr('progress_format'))
        self.start_button.setText(self.tr('start_export'))
        self.log_label.setText(self.tr('log_info'))
        
    def validate_inputs(self):
        """Validate all required inputs"""
        missing_fields = []
        
        if not self.url_input.currentText().strip():
            missing_fields.append(self.tr('missing_fields')['svn_url'])
        if not self.username_input.text().strip():
            missing_fields.append(self.tr('missing_fields')['username'])
        if not self.password_input.text().strip():
            missing_fields.append(self.tr('missing_fields')['password'])
        if not self.excel_path_input.text().strip():
            missing_fields.append(self.tr('missing_fields')['excel_path'])
            
        return missing_fields
        
    def handle_return_pressed(self):
        """Handle return key press event"""
        missing_fields = self.validate_inputs()
        if missing_fields:
            QMessageBox.warning(
                self,
                self.tr('validation_title'),
                self.tr('validation_message') + '\n'.join(f'- {field}' for field in missing_fields)
            )
            return
            
        self.start_export()
        
    def initUI(self):
        self.setWindowTitle(self.tr('window_title'))
        self.setMinimumSize(800, 600)
        
        # Create and set main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create form layout for input area
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        # SVN URL input with language selector
        url_layout = QHBoxLayout()
        
        # URL input part
        url_input_layout = QHBoxLayout()
        self.url_input = QComboBox()
        self.url_input.setEditable(True)
        self.url_input.setMaxCount(10)
        self.url_input.setMinimumHeight(30)
        self.url_input.lineEdit().returnPressed.connect(self.handle_return_pressed)
        url_input_layout.addWidget(self.url_input)
        url_layout.addLayout(url_input_layout, stretch=1)  # Add stretch=1 to make it expand
        
        # Add language selector to URL layout
        language_layout = QHBoxLayout()
        language_layout.setSpacing(5)  # Reduce spacing between label and combo
        language_label = QLabel("Language/语言:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(['English', '中文'])
        self.language_combo.setCurrentText('English' if self.current_language == 'en_US' else '中文')
        self.language_combo.currentTextChanged.connect(
            lambda text: self.changeLanguage('en_US' if text == 'English' else 'zh_CN')
        )
        # Set fixed widths for language selector components
        language_label.setFixedWidth(120)
        language_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.language_combo.setFixedWidth(120)
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        url_layout.addLayout(language_layout)  # Add without stretch to keep it at minimum size
        
        # Add URL layout to form
        self.url_label = QLabel(self.tr('svn_url'))
        form_layout.addRow(self.url_label, url_layout)
        
        # Username input
        self.username_label = QLabel(self.tr('username'))
        self.username_input = QLineEdit()
        self.username_input.setMinimumHeight(30)
        self.username_input.returnPressed.connect(self.handle_return_pressed)
        form_layout.addRow(self.username_label, self.username_input)
        
        # Password input
        self.password_label = QLabel(self.tr('password'))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(30)
        self.password_input.returnPressed.connect(self.handle_return_pressed)
        form_layout.addRow(self.password_label, self.password_input)
        
        # Create upper widget for input area
        upper_widget = QWidget()
        upper_layout = QVBoxLayout(upper_widget)
        upper_layout.addLayout(form_layout)
        
        # File format filter
        self.filter_group = QGroupBox(self.tr('file_format_filter'))
        filter_layout = QVBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText(self.tr('file_format_placeholder'))
        self.filter_input.setMinimumHeight(30)
        self.filter_input.returnPressed.connect(self.handle_return_pressed)
        filter_layout.addWidget(self.filter_input)
        self.filter_group.setLayout(filter_layout)
        upper_layout.addWidget(self.filter_group)
        
        # Excel save path
        self.excel_group = QGroupBox(self.tr('excel_save_location'))
        excel_layout = QHBoxLayout()
        self.excel_path_input = QLineEdit()
        self.excel_path_input.setReadOnly(True)
        self.excel_path_input.setMinimumHeight(30)
        self.browse_button = QPushButton(self.tr('choose_path'))
        self.browse_button.setMinimumHeight(30)
        self.browse_button.clicked.connect(self.browse_save_location)
        excel_layout.addWidget(self.excel_path_input)
        excel_layout.addWidget(self.browse_button)
        self.excel_group.setLayout(excel_layout)
        upper_layout.addWidget(self.excel_group)
        
        # Progress information
        self.progress_group = QGroupBox(self.tr('export_progress'))
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setFormat(self.tr('progress_format'))
        progress_layout.addWidget(self.progress_bar)
        self.progress_group.setLayout(progress_layout)
        upper_layout.addWidget(self.progress_group)
        
        # Start button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.start_button = QPushButton(self.tr('start_export'))
        self.start_button.setMinimumSize(160, 36)
        font = self.start_button.font()
        font.setPointSize(10)
        font.setBold(True)
        self.start_button.setFont(font)
        self.start_button.clicked.connect(self.start_export)
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()
        upper_layout.addLayout(button_layout)
        
        # Create splitter and add widgets
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(upper_widget)
        
        # Lower part - Log area
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(10, 0, 10, 10)
        
        # Add log title
        self.log_label = QLabel(self.tr('log_info'))
        font = self.log_label.font()
        font.setPointSize(10)
        self.log_label.setFont(font)
        log_layout.addWidget(self.log_label)
        
        # Log text box
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        splitter.addWidget(log_widget)
        
        # Set initial splitter sizes (30% for upper part, 70% for log)
        main_layout.addWidget(splitter)
        splitter.setSizes([300, 700])
        
    def log(self, message):
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def loadSettings(self):
        urls = self.settings.value('svn_urls', [])
        if urls:
            self.url_input.addItems(urls)
            self.url_input.setCurrentText(urls[0])
        
        username = self.settings.value('username', '')
        if username:
            self.username_input.setText(username)
        
        excel_path = self.settings.value('excel_path', '')
        if excel_path:
            self.excel_path_input.setText(excel_path)
            
        file_filters = self.settings.value('file_filters', '')
        if file_filters:
            self.filter_input.setText(file_filters)
            
    def saveSettings(self):
        current_url = self.url_input.currentText().strip()
        if current_url:
            urls = [current_url]
            for i in range(self.url_input.count()):
                url = self.url_input.itemText(i)
                if url != current_url and url.strip():
                    urls.append(url)
            urls = urls[:10]
            self.settings.setValue('svn_urls', urls)
        
        username = self.username_input.text().strip()
        if username:
            self.settings.setValue('username', username)
        
        excel_path = self.excel_path_input.text().strip()
        if excel_path:
            self.settings.setValue('excel_path', excel_path)
            
        file_filters = self.filter_input.text().strip()
        if file_filters:
            self.settings.setValue('file_filters', file_filters)
            
    def browse_save_location(self):
        last_path = self.settings.value('excel_path', '')
        start_dir = os.path.dirname(last_path) if last_path else ""
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr('excel_save_location'),
            start_dir,
            "Excel files (*.xlsx)"
        )
        if file_path:
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            self.excel_path_input.setText(file_path)
            
    def start_export(self):
        url = self.url_input.currentText().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        excel_path = self.excel_path_input.text().strip()
        file_filters = self.filter_input.text().strip()
        
        if not all([url, username, password, excel_path]):
            QMessageBox.warning(self, self.tr('warning'), self.tr('fill_required'))
            return
            
        try:
            result = subprocess.run(['svn', '--version'], capture_output=True, text=True)
        except FileNotFoundError:
            QMessageBox.critical(self, self.tr('error'), self.tr('svn_not_found'))
            return
            
        self.saveSettings()
        self.log_text.clear()
            
        self.start_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Process file filters
        filter_patterns = []
        if file_filters:
            filter_patterns = [pattern.strip() for pattern in file_filters.split(';') if pattern.strip()]
        
        # Pass translations to SVNWorker
        self.worker = SVNWorker(url, username, password, excel_path, filter_patterns)
        self.worker.set_translations(self.translations[self.current_language])
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.export_finished)
        self.worker.log_message.connect(self.log)
        self.worker.start()
        
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
    def export_finished(self, success, message):
        self.start_button.setEnabled(True)
        if success:
            QMessageBox.information(self, self.tr('window_title'), message)
        else:
            QMessageBox.critical(self, self.tr('error'), message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 
