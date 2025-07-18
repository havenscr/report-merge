# Enhanced Power BI Report Merger v2.0

**Built by Reid Havens of Analytic Endeavors**  
**Website: https://analyticsendeavors.com**

## Overview

The Enhanced Power BI Report Merger is a professional-grade tool designed to intelligently combine two thin PBIP reports into a single unified report. This enhanced version features a modern user interface, comprehensive help system, and advanced branding integration.

## 🚀 Key Enhancements in v2.0

### **Professional Branding & UI**
- Modern analytics-themed interface with Analytic Endeavors branding
- Company website integration and about dialog
- Enhanced color scheme and professional typography
- Improved layout with better spacing and visual hierarchy

### **Smart User Experience**
- **Auto-enabled Analyze button**: Only becomes active when both report paths are provided
- **Auto-path cleaning**: Automatically removes quotes from pasted file paths
- **Auto-output generation**: Automatically suggests output path based on input files
- **Real-time validation**: Immediate feedback on file selection

### **Enhanced Help System**
- **Comprehensive Help Dialog** (Ctrl+H or F1): Detailed guide with workflow, features, and troubleshooting
- **About Dialog**: Company information and tool details
- **Quick Start Guide**: Embedded in the main interface
- **Website Integration**: Direct links to Analytic Endeavors website

### **Advanced Features**
- **Keyboard Shortcuts**: 
  - `Ctrl+R`: Reset application
  - `Ctrl+H` / `F1`: Show help
  - `F5`: Analyze reports (when ready)
  - `Escape`: Close dialogs
- **Enhanced Progress Tracking**: Visual feedback during operations
- **Log Export**: Save analysis logs for audit trails
- **Professional Error Handling**: User-friendly error messages with guidance

## 📋 Requirements

- **Input Files**: Thin PBIP reports (.pbip files)
- **Structure**: Corresponding .Report directories must exist
- **Compatibility**: Files must NOT have semantic models (.SemanticModel folders)
- **System**: Python 3.7+ with tkinter support
- **Permissions**: Write access to output location

## 🛠️ Installation & Usage

### **Quick Start**
1. **Download** the enhanced version files to a folder
2. **Run** `run_enhanced_merger.bat` (Windows) or execute `python enhanced_pbip_merger.py`
3. **Select** your Report A and Report B files using the browse buttons
4. **Analyze** reports by clicking "🔍 ANALYZE REPORTS" (auto-enabled when both files selected)
5. **Review** analysis results and choose merge options
6. **Execute** merge by clicking "🚀 EXECUTE MERGE"

### **Professional Workflow**
1. **📁 DATA SOURCES**
   - Use File Explorer to navigate to your .pbip files
   - Right-click → "Copy as path" → Paste into path fields
   - Quotes are automatically cleaned
   - Output path is auto-generated

2. **🔍 ANALYSIS**
   - Click "Analyze Reports" when both files are selected
   - Review comprehensive analysis in the progress log
   - Check for conflicts and compatibility

3. **🚀 MERGE EXECUTION**
   - Click "Execute Merge" to combine reports
   - Monitor real-time progress
   - Verify output integrity

## 🎨 Architecture & Composition

The enhanced version uses a clean composition structure with four main components:

### **1. AppConstants**
- Company branding and configuration
- UI styling and color schemes
- Help content and documentation
- Professional messaging

### **2. ValidationService**
- Comprehensive input validation
- File structure verification
- Error handling with user guidance
- Path cleaning and normalization

### **3. MergerEngine**
- Core business logic for merging
- Report analysis and comparison
- Conflict resolution algorithms
- Progress tracking and logging

### **4. UIManager**
- Professional interface management
- Event handling and state management
- Dialog creation and styling
- Enhanced user experience features

### **5. Main Application**
- Orchestrates all components
- Threading for background operations
- Keyboard shortcuts and accessibility
- Professional error handling

## 🔧 Features in Detail

### **Intelligent Conflict Resolution**
- Automatically resolves naming conflicts
- Handles duplicate measures with smart renaming
- Preserves all content from both reports

### **Advanced Theme Management**
- Detects and compares report themes
- Allows user choice when themes differ
- Properly merges theme resources and references

### **Comprehensive Validation**
- Validates file structure before processing
- Checks for thin report compatibility
- Ensures output integrity after merge

### **Professional Progress Tracking**
- Real-time analysis and merge logging
- Comprehensive statistics and summaries
- Export capability for audit trails

## 📞 Support & Contact

**Analytic Endeavors**  
**Website**: https://analyticsendeavors.com  
**Built by**: Reid Havens  

For technical support, feature requests, or consulting services, please visit our website.

## 📄 License & Usage

This tool is built by Analytic Endeavors for professional use in Power BI report management and consolidation workflows.

---

**© 2024 Analytic Endeavors - Empowering data-driven decisions through innovative analytics solutions**
