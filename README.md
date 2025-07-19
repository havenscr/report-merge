# Enhanced Power BI Report Merger v1.0

**Built by [Reid Havens](https://www.linkedin.com/in/reidhavens/) of [https://analyticsendeavors.com](https://analyticsendeavors.com)**  

## ⚠️ Important Disclaimer

**This is a third-party tool and is NOT officially supported by Microsoft.** Report merging using this method is not an officially supported Power BI operation. Use at your own discretion and always:

- **Back up your original reports** before attempting any merge operations
- **Test thoroughly** in development environments before using on production reports
- **Validate all merged content** to ensure data integrity and functionality
- **Be aware** that future Power BI updates may change file formats or structures

Microsoft does not provide support for issues arising from third-party report manipulation tools. Always follow your organization's data governance and change management policies.

## Overview

The Enhanced Power BI Report Merger is a professional-grade tool designed to intelligently combine two thin PBIP reports into a single unified report. This enhanced version features a modern user interface, comprehensive help system, and advanced branding integration.

## 🚀 Key Features in v1.0

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

## 📋 Requirements & Limitations

### **System Requirements**
- **Input Files**: Thin PBIP reports (.pbip files)
- **Structure**: Corresponding .Report directories must exist
- **Compatibility**: Files must NOT have semantic models (.SemanticModel folders)
- **System**: Python 3.7+ with tkinter support
- **Permissions**: Write access to output location

### **⚠️ Important Limitations**
- **Unsupported by Microsoft**: This tool manipulates Power BI file structures in ways not officially supported
- **Compatibility Risk**: Future Power BI updates may break functionality
- **Data Risk**: Always backup original files before use
- **Testing Required**: Thoroughly validate merged reports before deployment
- **Organizational Policy**: Ensure compliance with your organization's data governance policies

## 🛠️ Installation & Usage

### **📁 Project Structure**
- **`src/` folder**: Contains the base source code and Python files
- **`builds/` folder**: Contains ready-to-use executable files:
  - **`Power BI Report Merger v1.0.0 Setup.exe`**: Installation package for installing as an external tool
  - **`Power BI Report Merger.exe`**: Standalone executable that runs without installation

### **Installation Options**

#### **Option 1: Standalone Executable (Recommended for Quick Use)**
1. Navigate to the `builds/` folder
2. Double-click **`Power BI Report Merger.exe`**
3. Tool launches immediately - no installation required

#### **Option 2: Install as External Tool**
1. Navigate to the `builds/` folder
2. Run **`Power BI Report Merger v1.0.0 Setup.exe`**
3. Follow installation wizard to install as a system tool
4. Access from Start Menu or desktop shortcut

#### **Option 3: Run from Source Code**
1. Navigate to the `src/` folder
2. Run `run_enhanced_merger.bat` (Windows) or execute `python enhanced_pbip_merger.py`
3. Requires Python 3.7+ with tkinter support

### **⚠️ Pre-Usage Checklist**
- [ ] **Backup original reports** to a safe location
- [ ] **Verify organizational approval** for using third-party tools
- [ ] **Test in development environment** first
- [ ] **Ensure you have rollback capability**

### **Quick Start (Any Method)**
1. **Launch** the tool using any of the installation options above
2. **Select** your Report A and Report B files using the browse buttons
3. **Analyze** reports by clicking "🔍 ANALYZE REPORTS" (auto-enabled when both files selected)
4. **Review** analysis results and choose merge options
5. **Execute** merge by clicking "🚀 EXECUTE MERGE"
6. **⚠️ Validate merged report** thoroughly before use

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
   - **⚠️ Immediately test the merged report** in Power BI Desktop

4. **✅ POST-MERGE VALIDATION**
   - Open merged report in Power BI Desktop
   - Verify all visuals render correctly
   - Test data refresh and interactions
   - Validate measures and calculations
   - Check formatting and themes

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

## ⚠️ Risk Management & Best Practices

### **Before Using This Tool**
- **Backup Strategy**: Always maintain copies of original reports
- **Environment Testing**: Use development/test environments first
- **Change Management**: Follow your organization's change control processes
- **Documentation**: Keep records of what reports were merged and when

### **After Merging**
- **Immediate Validation**: Test all functionality in the merged report
- **Performance Testing**: Ensure the merged report performs acceptably
- **User Acceptance**: Have end users validate the merged content
- **Monitoring**: Watch for any issues in production use

### **If Issues Arise**
- **Rollback Plan**: Be prepared to revert to original reports
- **Microsoft Support**: Remember that Microsoft cannot support issues from third-party tools
- **Professional Help**: Consider consulting with Power BI experts if problems occur

## 📞 Support & Contact

**Analytic Endeavors**  
**Website**: [https://analyticsendeavors.com](https://analyticsendeavors.com)  
**Built by**: [Reid Havens](https://www.linkedin.com/in/reidhavens/)  

For technical support, feature requests, or consulting services, please visit our website.

**Note**: Support is provided for the tool functionality only. Microsoft Power BI-related issues arising from merged reports should be addressed through appropriate Power BI support channels, keeping in mind the unsupported nature of this merging approach.

## 📄 License & Usage

This tool is built by Analytic Endeavors for professional use in Power BI report management and consolidation workflows.

**Use of this tool constitutes acceptance of the risks associated with unsupported Power BI file manipulation. Users assume full responsibility for any issues arising from the use of this tool.**

---

**© 2024 Analytic Endeavors - Empowering data-driven decisions through innovative analytics solutions**

*This tool is provided "as-is" without warranty. Always backup your data and test thoroughly.*