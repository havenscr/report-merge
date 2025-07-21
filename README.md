# Power BI Report Merger

**Professional-grade tool for intelligent Power BI report consolidation**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## 🚀 What is Power BI Report Merger?

The Power BI Report Merger is a professional desktop application that intelligently combines multiple Power BI reports into a single consolidated report. Perfect for analysts, consultants, and organizations who need to merge reports while preserving all content, themes, and functionality.

**Built by [Reid Havens](https://linkedin.com/in/reid-havens) of [Analytic Endeavors](https://www.analyticendeavors.com)**

---

## ✨ Key Features

### 🎯 **Smart Report Consolidation**
- Automatically merges pages, bookmarks, and measures
- Intelligent conflict resolution for overlapping content
- Preserves all visualizations and data relationships

### 🎨 **Theme Management**
- Detects theme conflicts between reports
- Allows you to choose which theme to apply
- Maintains consistent styling across merged content

### 📊 **Professional Interface**
- Clean, intuitive user interface
- Real-time progress tracking
- Comprehensive analysis and validation

### 🔒 **Enterprise-Grade Security**
- Comprehensive audit logging
- Secure file handling
- Professional error management

---

## 📋 Requirements

### ⚠️ **Important: PBIR Format Required**
This tool **ONLY** works with **PBIP files** in the enhanced report format (PBIR). 

**To enable PBIR format in Power BI Desktop:**
1. Go to **File** → **Options and settings** → **Options**
2. Select **Preview features**
3. Enable **"Store reports using enhanced metadata format"**
4. Restart Power BI Desktop
5. Save your reports - they will now be in .pbip format with a `.Report` folder

### 🖥️ **System Requirements**
- **Windows 10/11** (64-bit recommended)
- **Python 3.8+** (for running from source)
- **Power BI Desktop** (for creating PBIR files)
- **4GB RAM** minimum, 8GB recommended

---

## 🚀 Quick Start

### Option 1: Download Release (Recommended)
1. **Download** the latest release from the [Releases page](../../releases)
2. **Choose your preferred option:**
   - **Setup Installer** (`Power BI Report Merger v1.0.1 Setup.exe`): Professional installation with automatic Power BI Desktop integration
   - **Standalone Portable** (`Power BI Report Merger.exe`): Run directly without installation
3. **For Setup Installer:**
   - Run the installer as Administrator
   - Launch from Start Menu or desktop shortcut
   - Tool automatically integrates with Power BI Desktop as an External Tool
4. **For Standalone Portable:**
   - Save to any location and run directly
   - No installation required - works immediately
   - Manual Power BI integration available if desired

### Option 2: Run from Source
1. **Clone** this repository
2. **Install** Python 3.8+ from [python.org](https://python.org/downloads)
3. **Navigate** to the source folder
4. **Run** `run_pbi_report_merger.bat`

---

## 📖 How to Use

### Step 1: Prepare Your Reports
- Ensure both reports are in **PBIP format** (not .pbix)
- Verify you have both `.pbip` files and corresponding `.Report` folders
- **Backup** your original reports before merging

### Step 2: Launch the Tool
- From **Power BI Desktop**: External Tools → Power BI Report Merger
- From **Start Menu**: Analytic Endeavors → Power BI Report Merger
- From **Source**: Run `run_security_enhanced.bat`

### Step 3: Select Your Reports
1. **Browse** for Report A (first .pbip file)
2. **Browse** for Report B (second .pbip file)
3. Click **"Analyze Reports"** to validate and preview

### Step 4: Review Analysis
- View the analysis summary showing pages, bookmarks, and measures
- **Resolve theme conflicts** if detected (choose preferred theme)
- Review any conflicts or warnings

### Step 5: Execute Merge
1. **Specify** output location (or use auto-generated path)
2. Click **"Execute Merge"** 
3. **Wait** for completion (progress shown in real-time)
4. **Open** your merged report in Power BI Desktop

---

## 🎨 Example Workflow

```
📁 Input:
   ├── Sales_Report_Q1.pbip      (5 pages, 12 bookmarks)
   ├── Sales_Report_Q1.Report/
   ├── Sales_Report_Q2.pbip      (4 pages, 8 bookmarks)
   └── Sales_Report_Q2.Report/

🔄 Process:
   ├── Analyze both reports
   ├── Detect theme differences
   ├── Choose preferred theme
   └── Execute intelligent merge

📊 Output:
   ├── Combined_Sales_Report_Q1_Q2.pbip    (9 pages, 20 bookmarks)
   └── Combined_Sales_Report_Q1_Q2.Report/
```

---

## ❓ Frequently Asked Questions

### **Q: What file formats are supported?**
**A:** Only PBIP files in enhanced report format (PBIR). Traditional .pbix files are NOT supported.

### **Q: Can I merge more than 2 reports?**
**A:** Currently supports merging 2 reports at a time. For multiple reports, merge them in pairs.

### **Q: Will my data connections be preserved?**
**A:** Yes, the tool merges report-level content only. Data connections and models remain intact.

### **Q: What happens if there are conflicts?**
**A:** The tool intelligently resolves conflicts by renaming duplicate elements and lets you choose theme preferences.

### **Q: Is this officially supported by Microsoft?**
**A:** No, this is a third-party tool. Always test thoroughly and keep backups of your original reports.

---

## 🛠️ Troubleshooting

### Common Issues

**"File format not supported"**
- Ensure you're using .pbip files (not .pbix)
- Enable PBIR format in Power BI Desktop settings
- Check that .Report folders exist alongside .pbip files

**"Python not found"** (when running from source)
- Install Python 3.8+ from [python.org](https://python.org/downloads)
- Ensure "Add to PATH" is checked during installation

**"Permission denied"**
- Run as Administrator if needed
- Check that files aren't open in Power BI Desktop
- Ensure antivirus isn't blocking the application

**Security warnings**
- The tool is code-signed for security
- Some antivirus software may show warnings for new applications
- Check our [Security Documentation](docs/SECURITY.md) for more details

---

## 🔒 Security & Privacy

### Data Handling
- **No data leaves your machine** - completely offline tool
- **No telemetry or tracking** - your privacy is protected
- **Audit logging** available for enterprise compliance
- **Professional security standards** implemented throughout

### Code Signing
- All releases are digitally signed for authenticity
- Enterprise-grade security architecture
- Regular security reviews and updates

---

## 📞 Support & Community

### Getting Help
- 📚 **Documentation**: Check our [Wiki](../../wiki) for detailed guides
- 🐛 **Bug Reports**: Use [Issues](../../issues) to report problems
- 💡 **Feature Requests**: Submit via [Issues](../../issues) with enhancement label
- 🌐 **Professional Support**: [Analytic Endeavors](https://www.analyticendeavors.com)

### Contributing
We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

---

## ⚖️ Legal & Disclaimers

### Important Notices
- **Not officially supported by Microsoft**
- **Use at your own risk** - always test thoroughly
- **Keep backups** of original reports before merging
- **Requires PBIR format** - traditional Power BI files not supported

### License
This software is proprietary. See [LICENSE](LICENSE) for terms and conditions.

---

## 🏢 About Analytic Endeavors

**Power BI Report Merger** is developed by [Analytic Endeavors](https://www.analyticendeavors.com), a consulting firm specializing in business intelligence and data analytics solutions.

**Founded by Reid Havens**, we create professional tools and provide consulting services for organizations looking to maximize their Power BI investments.

### Our Services
- Power BI consulting and development
- Custom tool development
- Training and workshops
- Enterprise BI strategy

---

## 🔄 Version History

### v1.0.0 - Enhanced Security Edition
- ✅ Initial public release
- ✅ PBIR format support
- ✅ Intelligent merge algorithms
- ✅ Theme conflict resolution
- ✅ Professional security architecture
- ✅ Power BI Desktop integration
- ✅ Comprehensive audit logging

---

## 🌟 Show Your Support

If you find this tool useful:
- ⭐ **Star this repository**
- 🐦 **Share** with your Power BI community
- 💼 **Connect** with us on [LinkedIn](https://linkedin.com/company/analytic-endeavors)
- 🌐 **Visit** our website: [analyticendeavors.com](https://www.analyticendeavors.com)

---

**Made with ❤️ by [Reid Havens](https://www.analyticendeavors.com) for the Power BI community**
