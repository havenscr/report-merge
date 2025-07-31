@echo off
title Code Signing and Security Validation - Power BI Report Merger
color 0B

echo ================================================
echo  CODE SIGNING AND SECURITY VALIDATION
echo  Power BI Report Merger - Security Hardening
echo  Built by Reid Havens of Analytic Endeavors
echo ================================================
echo.

REM Check for built files
if not exist "dist\*.msi" (
    echo ERROR: No MSI files found in dist directory
    echo Please run build_secure.bat first
    pause
    exit /b 1
)

if not exist "build\PowerBIReportMerger\PowerBIReportMerger.exe" (
    echo ERROR: No executable found in build directory
    echo Please run build_secure.bat first
    pause
    exit /b 1
)

echo Checking for code signing certificate...
set "CERT_FOUND=0"

REM Look for certificate in various stores
for /f %%i in ('certutil -store -user My ^| findstr /C:"Code Signing" 2^>nul') do set "CERT_FOUND=1"
for /f %%i in ('certutil -store My ^| findstr /C:"Code Signing" 2^>nul') do set "CERT_FOUND=1"

if "%CERT_FOUND%"=="1" (
    echo ✅ Code signing certificate found
    set /p SIGN_CODE="Would you like to sign the files? (y/n): "
) else (
    echo ⚠️ No code signing certificate found
    echo.
    echo 🔒 TO ELIMINATE FALSE POSITIVES, CONSIDER:
    echo.
    echo 1. **EV Code Signing Certificate** (Recommended)
    echo    - Purchase from DigiCert, Sectigo, GlobalSign, or Entrust
    echo    - Cost: $300-800/year for EV certificates
    echo    - Provides immediate reputation with Windows SmartScreen
    echo    - Required for enterprise distribution
    echo.
    echo 2. **Self-signed Certificate** (Testing Only)
    set /p CREATE_SELF="Create self-signed certificate for testing? (y/n): "
    if /i "!CREATE_SELF!"=="y" (
        echo Creating self-signed certificate...
        makecert -r -pe -n "CN=Analytic Endeavors PowerBI Tools" -b 01/01/2024 -e 01/01/2026 -eku 1.3.6.1.5.5.7.3.3 -ss my -sr CurrentUser -len 2048 -sp "Microsoft Enhanced RSA and AES Cryptographic Provider" -sy 24 selfcert.cer
        if not errorlevel 1 echo ✅ Self-signed certificate created
    )
    set "SIGN_CODE=n"
)

REM Sign the files if requested and possible
if /i "%SIGN_CODE%"=="y" (
    echo.
    echo 🔐 Signing files with timestamp...
    
    REM Find and sign the executable
    for %%f in (build\PowerBIReportMerger\*.exe) do (
        echo Signing: %%f
        signtool sign /a /t http://timestamp.digicert.com /fd SHA256 /d "Power BI Report Merger" /du "https://www.analyticendeavors.com" "%%f"
        if not errorlevel 1 (
            echo ✅ Successfully signed: %%f
        ) else (
            echo ❌ Failed to sign: %%f
        )
    )
    
    REM Sign the MSI
    for %%f in (dist\*.msi) do (
        echo Signing: %%f
        signtool sign /a /t http://timestamp.digicert.com /fd SHA256 /d "Power BI Report Merger Installer" /du "https://www.analyticendeavors.com" "%%f"
        if not errorlevel 1 (
            echo ✅ Successfully signed: %%f
        ) else (
            echo ❌ Failed to sign: %%f
        )
    )
)

echo.
echo ================================================
echo  SECURITY VALIDATION AND SUBMISSION PREP
echo ================================================
echo.

REM Create vendor submission package
echo 📦 Creating vendor submission package...
mkdir "security_submission" 2>nul

REM Copy files for submission
if exist "Security_Documentation.md" copy "Security_Documentation.md" "security_submission\" >nul
if exist "dist\*.msi" copy "dist\*.msi" "security_submission\" >nul
if exist "build\PowerBIReportMerger\*.exe" copy "build\PowerBIReportMerger\*.exe" "security_submission\" >nul
if exist "main.py" copy "main.py" "security_submission\" >nul
if exist "core\*.py" xcopy "core\*.py" "security_submission\core\" /I /Y >nul
if exist "ui\*.py" xcopy "ui\*.py" "security_submission\ui\" /I /Y >nul
if exist "README.md" copy "README.md" "security_submission\" >nul

REM Create vendor submission documentation
(
echo # Vendor Submission Package - Power BI Report Merger
echo.
echo ## Application Information
echo - **Name**: Power BI Report Merger
echo - **Version**: 1.0.0 Enhanced Security Edition
echo - **Developer**: Reid Havens - Analytic Endeavors
echo - **Website**: https://www.analyticendeavors.com
echo - **Email**: reid@analyticendeavors.com
echo - **Purpose**: Business Intelligence tool for Power BI report consolidation
echo - **Technology**: Python 3.x with secure base tool architecture
echo.
echo ## Security Architecture Features
echo ### Base Tool Design Pattern
echo - Secure composition and inheritance from BaseExternalTool
echo - Professional error handling with audit trails
echo - Comprehensive security event logging
echo - Minimal attack surface with explicit dependencies
echo.
echo ### File Operations
echo - Read-only access to Power BI PBIP files
echo - No system modification beyond standard installation
echo - Secure path validation and cleaning
echo - Professional file handling with error recovery
echo.
echo ### Network Activity
echo - **NONE** - This is completely offline tool
echo - No internet connectivity required
echo - No data transmission or telemetry
echo - No remote server communication
echo.
echo ## False Positive Analysis
echo ### Why This Application May Trigger Scanners
echo 1. **Python Executable Packaging**
echo    - Uses cx_Freeze for standalone executable creation
echo    - Dynamic code loading patterns common in Python apps
echo    - Packed executable structure may resemble obfuscation
echo.
echo 2. **Business File Processing**
echo    - Reads and processes Power BI project files
echo    - JSON and ZIP file manipulation for legitimate business purposes
echo    - File copying and directory operations for report merging
echo.
echo 3. **GUI Framework Usage**
echo    - Tkinter GUI framework usage
echo    - Event-driven programming patterns
echo    - Threading for responsive user interface
echo.
echo ## Legitimacy Verification
echo ### Professional Development Standards
echo - Clean, well-documented source code
echo - Professional software architecture
echo - Enterprise-grade error handling
echo - Comprehensive logging and audit trails
echo.
echo ### Business Purpose Validation
echo - Clear business intelligence use case
echo - Integration with Microsoft Power BI ecosystem
echo - Professional branding and documentation
echo - Established company website and presence
echo.
echo ### Technical Quality Indicators
echo - Professional exception handling
echo - Secure coding practices implemented
echo - Modular architecture with separation of concerns
echo - Professional UI/UX design patterns
echo.
echo ## Vendor Whitelist Submission Requests
echo.
echo This application is submitted for whitelisting as a legitimate
echo business intelligence tool. It serves a clear professional purpose
echo and follows enterprise software development standards.
echo.
echo For any questions or additional verification requirements,
echo please contact Reid Havens at reid@analyticendeavors.com
echo.
echo Company verification available at: https://www.analyticendeavors.com
) > "security_submission\Vendor_Submission_Documentation.md"

echo ✅ Vendor submission package created in: security_submission\

echo.
echo ================================================
echo  RECOMMENDED SECURITY ACTIONS
echo ================================================
echo.
echo 🔒 **IMMEDIATE STEPS TO REDUCE FALSE POSITIVES:**
echo.
echo 1. **Code Signing Certificate** (Critical)
echo    - Purchase EV Code Signing Certificate
echo    - Sign both EXE and MSI files with timestamp
echo    - Builds Windows SmartScreen reputation over time
echo.
echo 2. **Vendor Whitelist Submissions**
echo    Submit to major antivirus vendors:
echo.
echo    🛡️ **Microsoft Defender:**
echo    - URL: https://www.microsoft.com/wdsi/filesubmission
echo    - Submit: EXE and MSI files with documentation
echo    - Include: Business justification and company info
echo.
echo    🛡️ **Symantec/Norton:**
echo    - URL: https://submit.symantec.com/false_positive/
echo    - Submit: Files with detailed business explanation
echo    - Include: Company verification information
echo.
echo    🛡️ **McAfee:**
echo    - URL: https://www.mcafee.com/enterprise/en-us/threat-center/file-submission.html
echo    - Submit: Complete package with source code
echo    - Include: Professional development documentation
echo.
echo    🛡️ **Trend Micro:**
echo    - URL: https://www.trendmicro.com/en_us/about/legal/detection-reevaluation.html
echo    - Submit: Application with detailed description
echo    - Include: Legitimate business use case
echo.
echo    🛡️ **Kaspersky:**
echo    - URL: https://support.kaspersky.com/faq/?qid=208280684
echo    - Submit: False positive report with evidence
echo    - Include: Professional software documentation
echo.
echo 3. **Build Enterprise Reputation**
echo    - Consistent releases from same certificate
echo    - Professional website and documentation
echo    - User testimonials and case studies
echo    - Corporate distribution channels
echo.
echo 4. **Alternative Distribution Methods**
echo    - Microsoft Store publication (highest trust)
echo    - Corporate app stores and repositories
echo    - Internal enterprise distribution initially
echo    - Partner channel distribution
echo.

echo.
echo 📊 **CURRENT PACKAGE STATUS:**
echo.
for %%f in (security_submission\*.exe) do echo ✅ Executable: %%f
for %%f in (security_submission\*.msi) do echo ✅ Installer: %%f
echo ✅ Source code included for verification
echo ✅ Security documentation included
echo ✅ Professional development standards demonstrated
echo ✅ Clear business purpose documented

echo.
echo 🚀 **NEXT STEPS:**
echo 1. Purchase and install EV Code Signing Certificate
echo 2. Re-run this script to sign all files
echo 3. Submit security_submission\ folder to antivirus vendors
echo 4. Monitor vendor responses and update as needed
echo 5. Distribute through professional channels

echo.
echo 📞 **SUPPORT AND CONTACT:**
echo Developer: Reid Havens
echo Company: Analytic Endeavors
echo Website: https://www.analyticendeavors.com
echo.
echo Files ready for vendor submission are in: security_submission\
echo.
pause
