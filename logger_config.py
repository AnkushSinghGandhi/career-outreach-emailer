import logging
import os
from datetime import datetime
import yaml

class EmailLogger:
    """Enhanced logging system for email automation"""
    
    def __init__(self, script_name, config_path="config.yaml"):
        # Load config
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.log_config = self.config['logging']
        self.script_name = script_name
        
        # Create logs directory
        if not os.path.exists(self.log_config['log_dir']):
            os.makedirs(self.log_config['log_dir'])
        
        # Setup logger
        self.logger = logging.getLogger(script_name)
        self.logger.setLevel(getattr(logging, self.log_config['log_level']))
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        simple_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # File handler
        if self.log_config['enabled'] and self.log_config['file_output']:
            log_file = os.path.join(
                self.log_config['log_dir'],
                f"{script_name}_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            self.logger.addHandler(file_handler)
        
        # Console handler
        if self.log_config['console_output']:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(simple_formatter)
            self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def success(self, message):
        """Log success message (info level with prefix)"""
        self.logger.info(f"✓ {message}")
    
    def failed(self, message):
        """Log failure message (error level with prefix)"""
        self.logger.error(f"✗ {message}")

if __name__ == "__main__":
    # Test logger
    logger = EmailLogger("test_script")
    logger.info("This is an info message")
    logger.success("This is a success message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.failed("This is a failed message")
