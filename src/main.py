"""
Security-Enhanced Power BI Report Merger
Minimal wrapper that adds security logging to existing application
Built by Reid Havens of Analytic Endeavors
"""

import sys
import os
from pathlib import Path
import logging
import datetime
import json
from typing import Dict, Any

# Add paths for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

class SecurityAuditLogger:
    """Lightweight security audit logger"""
    
    def __init__(self, app_name: str = "PowerBIReportMerger"):
        self.app_name = app_name
        
        # Create secure log directory
        log_dir = Path.home() / "AppData" / "Local" / "AnalyticEndeavors" / "Logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        log_file = log_dir / f"{app_name}_{datetime.date.today().isoformat()}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(app_name)
        self.logger.info(f"Security audit logger initialized for {app_name}")
    
    def log_startup(self):
        """Log application startup with security context"""
        try:
            startup_info = {
                "application": self.app_name,
                "version": "1.0.0 Security Enhanced",
                "author": "Reid Havens - Analytic Endeavors",
                "execution_path": str(Path(__file__).parent),
                "python_version": sys.version,
                "platform": sys.platform
            }
            
            self.logger.info(f"SECURITY: Application startup - {json.dumps(startup_info, default=str)}")
            
            # Check for Power BI Desktop
            self._check_powerbi_integration()
            
        except Exception as e:
            self.logger.error(f"SECURITY: Startup logging failed - {e}")
    
    def log_operation(self, operation: str, details: Dict[str, Any] = None):
        """Log operations with security context"""
        try:
            message = f"OPERATION: {operation}"
            if details:
                message += f" | Details: {json.dumps(details, default=str)}"
            self.logger.info(message)
        except Exception as e:
            self.logger.error(f"SECURITY: Operation logging failed - {e}")
    
    def log_shutdown(self):
        """Log application shutdown"""
        self.logger.info("SECURITY: Application shutdown")
    
    def _check_powerbi_integration(self):
        """Check Power BI Desktop integration status"""
        try:
            powerbi_paths = [
                Path(os.environ.get('PROGRAMFILES', '')) / "Microsoft Power BI Desktop",
                Path(os.environ.get('PROGRAMFILES(X86)', '')) / "Microsoft Power BI Desktop",
                Path.home() / "AppData" / "Local" / "Microsoft" / "WindowsApps"
            ]
            
            powerbi_found = False
            for path in powerbi_paths:
                if path.exists():
                    for pbi_exe in path.rglob("PBIDesktop.exe"):
                        powerbi_found = True
                        self.logger.info(f"SECURITY: Power BI Desktop found - {pbi_exe}")
                        break
                    if powerbi_found:
                        break
            
            if not powerbi_found:
                self.logger.warning("SECURITY: Power BI Desktop not found - external tool integration may not work")
            
        except Exception as e:
            self.logger.error(f"SECURITY: Power BI integration check failed - {e}")


def main():
    """Enhanced main entry point with security logging"""
    audit_logger = None
    
    try:
        # Initialize security logging
        audit_logger = SecurityAuditLogger()
        audit_logger.log_startup()
        
        print("🔒 Security Enhanced Power BI Report Merger")
        print("📊 Built by Reid Havens of Analytic Endeavors")
        print("🌐 https://www.analyticendeavors.com")
        print()
        print("✅ Security audit logging initialized")
        print("📁 Logs location: %USERPROFILE%\\AppData\\Local\\AnalyticEndeavors\\Logs")
        print()
        
        # Import and run the original application
        audit_logger.log_operation("Importing original application modules")
        
        # Try to import the original UI
        try:
            from ui.merger_ui import main as run_original_app
            audit_logger.log_operation("Original application imported successfully")
            print("🚀 Starting enhanced Power BI Report Merger...")
            print()
            
            # Run the original application
            run_original_app()
            
        except ImportError as e:
            audit_logger.log_operation("Import failed, trying alternative", {"error": str(e)})
            
            # Alternative: Try to run the original app directly
            import tkinter as tk
            from ui.merger_ui import EnhancedPowerBIReportMergerApp
            
            print("🚀 Starting Power BI Report Merger (alternative method)...")
            print()
            
            root = tk.Tk()
            app = EnhancedPowerBIReportMergerApp(root)
            audit_logger.log_operation("Application started successfully")
            root.mainloop()
        
        audit_logger.log_operation("Application completed successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("For support, visit: https://www.analyticendeavors.com")
        
        if audit_logger:
            audit_logger.log_operation("Application error", {"error": str(e)})
        
        input("Press Enter to exit...")
        
    finally:
        if audit_logger:
            audit_logger.log_shutdown()


if __name__ == "__main__":
    main()
