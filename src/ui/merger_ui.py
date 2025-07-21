"""
Power BI Report Merger - Frontend UI
Simplified and optimized while keeping all design and functionality
Built by Reid Havens of Analytic Endeavors
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser
import threading
from pathlib import Path
from typing import Optional, Dict, Any, Callable
import sys

# Add parent directory to Python path for organized imports
sys.path.append(str(Path(__file__).parent.parent))

from core.constants import AppConstants
from core.merger_core import (
    MergerEngine, ValidationService, 
    ValidationError, InvalidReportError, FileOperationError
)

# =============================================================================
# UI MANAGER - SIMPLIFIED BUT COMPLETE
# =============================================================================

class UIManager:
    """Simplified UI manager with all functionality preserved."""
    
    def __init__(self, root: tk.Tk, app):
        self.root = root
        self.app = app
        
        # UI Variables
        self.report_a_path = tk.StringVar()
        self.report_b_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.theme_choice = tk.StringVar(value="report_a")
        
        # UI Components
        self.analyze_button = None
        self.merge_button = None
        self.analysis_text = None
        self.progress_bar = None
        self.theme_frame = None
        
        self._setup_styling()
    
    def _setup_styling(self):
        """Setup simplified professional styling."""
        style = ttk.Style()
        style.theme_use('clam')
        colors = AppConstants.COLORS
        
        self.root.configure(bg=colors['background'])
        
        # Essential styles only
        styles = {
            'Brand.TLabel': {'background': colors['background'], 'foreground': colors['primary'], 'font': ('Segoe UI', 16, 'bold')},
            'Title.TLabel': {'background': colors['background'], 'foreground': colors['text_primary'], 'font': ('Segoe UI', 18, 'bold')},
            'Subtitle.TLabel': {'background': colors['background'], 'foreground': colors['text_secondary'], 'font': ('Segoe UI', 10)},
            'Section.TLabelframe': {'background': colors['background'], 'borderwidth': 1, 'relief': 'solid'},
            'Section.TLabelframe.Label': {'background': colors['background'], 'foreground': colors['primary'], 'font': ('Segoe UI', 12, 'bold')},
            'Action.TButton': {'background': colors['primary'], 'foreground': colors['surface'], 'font': ('Segoe UI', 10, 'bold'), 'padding': (20, 10)},
            'Secondary.TButton': {'background': colors['border'], 'foreground': colors['text_primary'], 'font': ('Segoe UI', 10), 'padding': (15, 8)},
            'Brand.TButton': {'background': colors['accent'], 'foreground': colors['surface'], 'font': ('Segoe UI', 10, 'bold'), 'padding': (15, 8)},
            'Info.TButton': {'background': colors['info'], 'foreground': colors['surface'], 'font': ('Segoe UI', 9), 'padding': (12, 6)},
            'TProgressbar': {'background': colors['accent'], 'troughcolor': colors['border']},
            'TEntry': {'fieldbackground': colors['surface']},
            'TFrame': {'background': colors['background']},
            'TLabel': {'background': colors['background']},
            # Prettier radio buttons without borders
            'TRadiobutton': {
                'background': colors['background'],
                'foreground': colors['text_primary'],
                'font': ('Segoe UI', 10),
                'focuscolor': 'none',
                'borderwidth': 0,
                'relief': 'flat'
            },
            # PBIR requirement notice style
            'Requirement.TLabel': {
                'background': colors['warning'],
                'foreground': colors['surface'],
                'font': ('Segoe UI', 11, 'bold'),
                'relief': 'solid',
                'borderwidth': 1,
                'padding': (10, 5)
            },
            'RequirementText.TLabel': {
                'background': colors['background'],
                'foreground': colors['warning'],
                'font': ('Segoe UI', 10, 'bold')
            }
        }
        
        for style_name, config in styles.items():
            style.configure(style_name, **config)
        
        # Radio button hover and selection effects
        style.map('TRadiobutton',
                 background=[('active', colors['background']),
                           ('selected', colors['background'])],
                 foreground=[('active', colors['primary']),
                           ('selected', colors['primary'])])
        
        style.map('Action.TButton', background=[('active', colors['secondary'])])
    
    def setup_ui(self):
        """Setup the complete user interface."""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)  # Analysis log section (moved down)
        
        # Setup sections
        self._setup_header(main_frame)
        self._setup_data_sources(main_frame)
        self._setup_theme_selection(main_frame)
        self._setup_output_section(main_frame)  # Moved up before analysis log
        self._setup_analysis_log(main_frame)    # Moved down after theme selection
        self._setup_action_buttons(main_frame)
        self._setup_progress_bar(main_frame)
    
    def _setup_header(self, main_frame):
        """Setup header section."""
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 25))
        header_frame.columnconfigure(1, weight=1)
        
        # Left: Branding
        brand_frame = ttk.Frame(header_frame)
        brand_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(brand_frame, text=AppConstants.BRAND_TEXT, style='Brand.TLabel').pack(anchor=tk.W)
        ttk.Label(brand_frame, text=AppConstants.MAIN_TITLE, style='Title.TLabel').pack(anchor=tk.W, pady=(5, 0))
        ttk.Label(brand_frame, text=AppConstants.TAGLINE, style='Subtitle.TLabel').pack(anchor=tk.W, pady=(3, 0))
        ttk.Label(brand_frame, text=AppConstants.BUILT_BY_TEXT, style='Subtitle.TLabel').pack(anchor=tk.W, pady=(8, 0))
        
        # Right: Action buttons (WEBSITE as rightmost button)
        action_frame = ttk.Frame(header_frame)
        action_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(action_frame, text="🌐 WEBSITE", command=self.app.open_company_website, style='Brand.TButton').pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(action_frame, text="ℹ️ ABOUT", command=self.app.show_about_dialog, style='Info.TButton').pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(action_frame, text="❓ HELP", command=self.app.show_help_dialog, style='Info.TButton').pack(side=tk.RIGHT, padx=(5, 0))
    
    def _setup_data_sources(self, main_frame):
        """Setup data sources section with horizontal layout."""
        sources_frame = ttk.LabelFrame(main_frame, text="📁 DATA SOURCES", style='Section.TLabelframe', padding="20")
        sources_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        sources_frame.columnconfigure(1, weight=1)
        
        # Main horizontal layout
        content_frame = ttk.Frame(sources_frame)
        content_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))
        content_frame.columnconfigure(0, weight=1)  # Left side gets more space
        content_frame.columnconfigure(1, weight=1)  # Right side gets equal space
        
        # LEFT: Quick start guide (stays on left as requested)
        guide_frame = ttk.Frame(content_frame)
        guide_frame.grid(row=0, column=0, sticky=(tk.W, tk.N), padx=(0, 30))
        
        ttk.Label(guide_frame, text="🚀 QUICK START GUIDE:", font=('Segoe UI', 10, 'bold'), 
                 foreground=AppConstants.COLORS['info']).pack(anchor=tk.W)
        
        for step in AppConstants.QUICK_START_STEPS:
            ttk.Label(guide_frame, text=f"   {step}", font=('Segoe UI', 9),
                     foreground=AppConstants.COLORS['text_secondary'], 
                     wraplength=280).pack(anchor=tk.W, pady=1)
        
        # Add requirement notice to the quick start guide
        ttk.Label(guide_frame, text="   ⚠️ Requires PBIR format", font=('Segoe UI', 9, 'bold'),
                 foreground=AppConstants.COLORS['warning'], 
                 wraplength=280).pack(anchor=tk.W, pady=(5, 1))
        
        # RIGHT: File inputs with analyze button below
        inputs_frame = ttk.Frame(content_frame)
        inputs_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N))
        inputs_frame.columnconfigure(1, weight=1)
        
        self._create_file_input_row(inputs_frame, "Report A (PBIR):", 'a', 0)
        self._create_file_input_row(inputs_frame, "Report B (PBIR):", 'b', 1)
        
        # Analyze button (under the browse buttons on the right)
        self.analyze_button = ttk.Button(inputs_frame, text="🔍 ANALYZE REPORTS",
                                       command=self.app.analyze_reports, style='Action.TButton', state=tk.DISABLED)
        self.analyze_button.grid(row=2, column=0, columnspan=3, pady=(15, 0))
    
    def _create_file_input_row(self, parent, label_text, report_type, row):
        """Create file input row."""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=8)
        
        entry_var = self.report_a_path if report_type == 'a' else self.report_b_path
        entry = ttk.Entry(parent, textvariable=entry_var, width=80)
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(15, 10), pady=8)
        
        ttk.Button(parent, text="📂 Browse", command=lambda: self.app.browse_file(report_type)).grid(row=row, column=2, pady=8)
        
        # Bind events
        entry.bind('<KeyRelease>', lambda e: self._on_path_change())
        entry.bind('<FocusOut>', lambda e: self._on_path_change())
    
    def _setup_theme_selection(self, main_frame):
        """Setup theme selection (initially hidden)."""
        self.theme_frame = ttk.LabelFrame(main_frame, text="🎨 THEME CONFIGURATION", 
                                        style='Section.TLabelframe', padding="20")
    
    def _setup_analysis_log(self, main_frame):
        """Setup analysis log section."""
        log_frame = ttk.LabelFrame(main_frame, text="📊 ANALYSIS & PROGRESS LOG", 
                                 style='Section.TLabelframe', padding="15")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        content_frame = ttk.Frame(log_frame)
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Analysis text area
        self.analysis_text = scrolledtext.ScrolledText(
            content_frame, height=12, width=85, font=('Consolas', 9), state=tk.DISABLED,
            bg=AppConstants.COLORS['surface'], fg=AppConstants.COLORS['text_primary'],
            selectbackground=AppConstants.COLORS['accent'], relief='solid', borderwidth=1
        )
        self.analysis_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log controls
        log_controls = ttk.Frame(content_frame)
        log_controls.grid(row=0, column=1, sticky=tk.N, padx=(10, 0))
        
        ttk.Button(log_controls, text="📤 Export Log", command=self.app.export_log, 
                  style='Secondary.TButton', width=16).pack(pady=(0, 5), anchor=tk.W)
        ttk.Button(log_controls, text="🗑️ Clear Log", command=self.clear_analysis_log,
                  style='Secondary.TButton', width=16).pack(anchor=tk.W)
        
        self._show_welcome_message()
    
    def _setup_output_section(self, main_frame):
        """Setup output section."""
        output_frame = ttk.LabelFrame(main_frame, text="📁 OUTPUT CONFIGURATION", 
                                    style='Section.TLabelframe', padding="20")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output Path:").grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(output_frame, textvariable=self.output_path, width=80).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(15, 10), pady=8)
        ttk.Button(output_frame, text="📂 Browse", command=self.app.browse_output).grid(row=0, column=2, pady=8)
    
    def _setup_action_buttons(self, main_frame):
        """Setup action buttons."""
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=(20, 0))
        
        self.merge_button = ttk.Button(button_frame, text="🚀 EXECUTE MERGE", command=self.app.start_merge,
                                     style='Action.TButton', state=tk.DISABLED)
        self.merge_button.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(button_frame, text="🔄 RESET ALL", command=self.app.reset_application,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(button_frame, text="❌ EXIT", command=self.root.quit,
                  style='Secondary.TButton').pack(side=tk.LEFT)
    
    def _setup_progress_bar(self, main_frame):
        """Setup progress bar (hidden by default)."""
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        # Will be placed at row=6 when shown
    
    def _show_welcome_message(self):
        """Show welcome message with PBIR requirement."""
        messages = [
            "🎉 Welcome to the Enhanced Power BI Report Merger!",
            f"🏢 Built by {AppConstants.COMPANY_FOUNDER} of {AppConstants.COMPANY_NAME}",
            f"🌐 Visit us at: {AppConstants.COMPANY_WEBSITE}",
            "⌨️ Press Ctrl+H or F1 for help, Ctrl+R to reset",
            "=" * 60,
            "🚀 Ready to merge your Power BI reports!",
            "📁 Select your Report A and Report B files to begin..."
        ]
        for msg in messages:
            self.log_message(msg)
    
    def _on_path_change(self):
        """Handle path changes."""
        # Clean paths
        for path_var in [self.report_a_path, self.report_b_path]:
            current = path_var.get()
            cleaned = self.app.merger_engine.clean_path(current)
            if cleaned != current:
                path_var.set(cleaned)
        
        self._update_ui_state()
        self.app.auto_generate_output_path()
    
    def _update_ui_state(self):
        """Update UI state."""
        has_both = bool(self.report_a_path.get() and self.report_b_path.get())
        if self.analyze_button:
            self.analyze_button.config(state=tk.NORMAL if has_both else tk.DISABLED)
    
    def show_theme_selection(self, theme_a: Dict[str, Any], theme_b: Dict[str, Any]):
        """Show theme selection UI with horizontal layout."""
        self.theme_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Clear existing content
        for widget in self.theme_frame.winfo_children():
            widget.destroy()
        
        # Horizontal layout for theme selection
        content_frame = ttk.Frame(self.theme_frame)
        content_frame.pack(fill=tk.X, pady=5)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        
        # LEFT: Flavor text
        flavor_frame = ttk.Frame(content_frame)
        flavor_frame.grid(row=0, column=0, sticky=(tk.W, tk.N), padx=(0, 30))
        
        ttk.Label(flavor_frame, text="⚠️ THEME CONFLICT DETECTED", 
                 font=('Segoe UI', 11, 'bold'),
                 foreground=AppConstants.COLORS['warning']).pack(anchor=tk.W)
        
        ttk.Label(flavor_frame, text="The two reports use different themes.", 
                 font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(5, 0))
        
        ttk.Label(flavor_frame, text="Choose which theme to apply to the", 
                 font=('Segoe UI', 10)).pack(anchor=tk.W)
        
        ttk.Label(flavor_frame, text="merged report. This affects colors,", 
                 font=('Segoe UI', 10)).pack(anchor=tk.W)
        
        ttk.Label(flavor_frame, text="fonts, and visual styling.", 
                 font=('Segoe UI', 10)).pack(anchor=tk.W)
        
        # RIGHT: Theme selection options
        selection_frame = ttk.Frame(content_frame)
        selection_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N))
        
        ttk.Label(selection_frame, text="Select preferred theme:", 
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Theme A option with prettier styling
        theme_a_frame = ttk.Frame(selection_frame)
        theme_a_frame.pack(fill=tk.X, pady=5)
        
        # Create a visual container for the radio button option
        option_a_container = ttk.Frame(theme_a_frame, style='TFrame')
        option_a_container.pack(fill=tk.X, padx=5, pady=2)
        option_a_container.columnconfigure(1, weight=1)
        
        ttk.Radiobutton(option_a_container, text="📊 Report A Theme",
                       variable=self.theme_choice, value="report_a",
                       style='TRadiobutton').grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(option_a_container, text=theme_a['display'], 
                 font=('Segoe UI', 9), 
                 foreground=AppConstants.COLORS['text_secondary']).grid(row=0, column=1, sticky=tk.W, padx=(15, 0), pady=2)
        
        # Theme B option with prettier styling
        theme_b_frame = ttk.Frame(selection_frame)
        theme_b_frame.pack(fill=tk.X, pady=5)
        
        # Create a visual container for the radio button option
        option_b_container = ttk.Frame(theme_b_frame, style='TFrame')
        option_b_container.pack(fill=tk.X, padx=5, pady=2)
        option_b_container.columnconfigure(1, weight=1)
        
        ttk.Radiobutton(option_b_container, text="📊 Report B Theme",
                       variable=self.theme_choice, value="report_b",
                       style='TRadiobutton').grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(option_b_container, text=theme_b['display'], 
                 font=('Segoe UI', 9), 
                 foreground=AppConstants.COLORS['text_secondary']).grid(row=0, column=1, sticky=tk.W, padx=(15, 0), pady=2)
    
    def hide_theme_selection(self):
        """Hide theme selection UI."""
        if self.theme_frame:
            self.theme_frame.grid_remove()
    
    # State management
    def enable_merge_button(self):
        if self.merge_button:
            self.merge_button.config(state=tk.NORMAL)
    
    def set_analysis_state(self, analyzing: bool):
        if analyzing:
            self.progress_bar.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
            self.progress_bar.start()
            if self.analyze_button:
                self.analyze_button.config(state=tk.DISABLED)
        else:
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            self._update_ui_state()
    
    def set_merge_state(self, merging: bool):
        if merging:
            self.progress_bar.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
            self.progress_bar.start()
            if self.merge_button:
                self.merge_button.config(state=tk.DISABLED)
        else:
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            if self.merge_button:
                self.merge_button.config(state=tk.NORMAL)
    
    def reset_ui_state(self):
        if self.analyze_button:
            self.analyze_button.config(state=tk.DISABLED)
        if self.merge_button:
            self.merge_button.config(state=tk.DISABLED)
        if self.progress_bar:
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
        self.hide_theme_selection()
    
    # Logging
    def log_message(self, message: str):
        if self.analysis_text:
            self.analysis_text.config(state=tk.NORMAL)
            self.analysis_text.insert(tk.END, message + "\n")
            self.analysis_text.config(state=tk.DISABLED)
            self.analysis_text.see(tk.END)
            self.root.update_idletasks()
    
    def clear_analysis_log(self):
        if self.analysis_text:
            self.analysis_text.config(state=tk.NORMAL)
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.config(state=tk.DISABLED)
            self._show_welcome_message()
    
    def get_analysis_log_content(self) -> str:
        if self.analysis_text:
            return self.analysis_text.get(1.0, tk.END)
        return ""
    
    # Dialogs
    def show_file_dialog(self, report_type: str) -> Optional[str]:
        return filedialog.askopenfilename(
            title=f"Select Report {report_type.upper()} (.pbip file - PBIR format required)",
            filetypes=[("Power BI Project Files", "*.pbip"), ("All Files", "*.*")]
        )
    
    def show_save_dialog(self) -> Optional[str]:
        return filedialog.asksaveasfilename(
            title="Save Combined Report As", defaultextension=".pbip",
            filetypes=[("Power BI Project Files", "*.pbip"), ("All Files", "*.*")]
        )
    
    def show_export_dialog(self) -> Optional[str]:
        return filedialog.asksaveasfilename(
            title="Export Analysis Log", defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
    
    # Additional helper methods for secure architecture
    def show_error(self, title: str, message: str):
        """Show error dialog"""
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str):
        """Show info dialog"""
        messagebox.showinfo(title, message)
    
    def show_confirmation(self, title: str, message: str) -> bool:
        """Show confirmation dialog"""
        return messagebox.askyesno(title, message)
    
    def open_company_website(self):
        """Open company website"""
        try:
            import webbrowser
            webbrowser.open(AppConstants.COMPANY_WEBSITE)
            self.log_message(f"🌐 Opening {AppConstants.COMPANY_NAME} website...")
        except Exception as e:
            self.show_error("Error", f"Could not open website: {e}")
    
    def show_help_dialog(self):
        """Show help dialog with PBIR requirement information."""
        help_window = tk.Toplevel(self.root)
        help_window.title(f"{AppConstants.APP_NAME} - Help")
        help_window.geometry("650x650")
        help_window.resizable(False, False)
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Center window
        help_window.geometry(f"+{self.root.winfo_rootx() + 50}+{self.root.winfo_rooty() + 50}")
        
        self._create_help_content(help_window)
    
    def show_about_dialog(self):
        """Show about dialog."""
        about_window = tk.Toplevel(self.root)
        about_window.title(f"About - {AppConstants.APP_NAME}")
        about_window.geometry("500x490")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Center window
        about_window.geometry(f"+{self.root.winfo_rootx() + 100}+{self.root.winfo_rooty() + 100}")
        
        self._create_about_content(about_window)
    
    def _create_help_content(self, help_window):
        """Create help content"""
        help_window.configure(bg=AppConstants.COLORS['background'])
        
        main_frame = ttk.Frame(help_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(main_frame, text=f"❓ {AppConstants.APP_NAME} - Help", 
                 font=('Segoe UI', 16, 'bold'), 
                 foreground=AppConstants.COLORS['primary']).pack(anchor=tk.W, pady=(0, 20))
        
        # PBIR Requirement Section
        pbir_frame = ttk.Frame(main_frame)
        pbir_frame.pack(fill=tk.X, pady=(0, 20))
        
        warning_container = tk.Frame(pbir_frame, bg=AppConstants.COLORS['warning'], 
                                   padx=15, pady=10, relief='solid', borderwidth=2)
        warning_container.pack(fill=tk.X)
        
        ttk.Label(warning_container, text="⚠️  IMPORTANT DISCLAIMERS & REQUIREMENTS", 
                 font=('Segoe UI', 12, 'bold'), 
                 background=AppConstants.COLORS['warning'],
                 foreground=AppConstants.COLORS['surface']).pack(anchor=tk.W)
        
        warnings = [
            "• This tool ONLY works with PBIP enhanced report format (PBIR) files",
            "• This is NOT officially supported by Microsoft - use at your own discretion",
            "• Look for .pbip files with definition\\ folder (not report.json files)", 
            "• Always keep backups of your original reports before merging",
            "• Test thoroughly and validate merged results before production use",
            "• Enable 'Store reports using enhanced metadata format (PBIR)' in Power BI Desktop"
        ]
        
        for warning in warnings:
            ttk.Label(warning_container, text=warning, font=('Segoe UI', 10),
                     background=AppConstants.COLORS['warning'],
                     foreground=AppConstants.COLORS['surface']).pack(anchor=tk.W, pady=1)
        
        # Close button
        ttk.Button(help_window, text="❌ Close", command=help_window.destroy).place(
            relx=1.0, rely=1.0, anchor='se', x=-10, y=-15)
        
        help_window.bind('<Escape>', lambda e: help_window.destroy())
    
    def _create_about_content(self, about_window):
        """Create about content"""
        about_window.configure(bg=AppConstants.COLORS['background'])
        
        main_frame = ttk.Frame(about_window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(main_frame, text="🚀", font=('Segoe UI', 48)).pack()
        ttk.Label(main_frame, text=AppConstants.APP_NAME, font=('Segoe UI', 18, 'bold'),
                 foreground=AppConstants.COLORS['primary']).pack(pady=(10, 5))
        ttk.Label(main_frame, text=AppConstants.APP_VERSION, font=('Segoe UI', 12),
                 foreground=AppConstants.COLORS['text_secondary']).pack()
        
        # Description
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(pady=(20, 0))
        
        description = [
            f"The {AppConstants.APP_NAME} intelligently combines",
            "Power BI thin reports while preserving all content.",
            "",
            "⚠️ Requires PBIP format (PBIR) files only",
            "⚠️ NOT officially supported by Microsoft",
            "",
            f"Built by {AppConstants.COMPANY_FOUNDER}",
            f"of {AppConstants.COMPANY_NAME}"
        ]
        
        for line in description:
            ttk.Label(desc_frame, text=line, font=('Segoe UI', 10)).pack(pady=1)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(30, 0))
        
        ttk.Button(footer_frame, text="🌐 Visit Website", 
                  command=self.open_company_website).pack(side=tk.LEFT)
        ttk.Button(footer_frame, text="❌ Close", 
                  command=about_window.destroy).pack(side=tk.RIGHT)
        
        about_window.bind('<Escape>', lambda e: about_window.destroy())

# =============================================================================
# MAIN APPLICATION - SIMPLIFIED
# =============================================================================

class EnhancedPowerBIReportMergerApp:
    """Main application class."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        
        # Initialize components
        self.validation_service = ValidationService()
        self.merger_engine = MergerEngine(logger_callback=self._temp_log)
        
        self._setup_window()
        
        self.ui_manager = UIManager(root, self)
        self.merger_engine = MergerEngine(logger_callback=self._log_message)
        
        # State
        self.analysis_results = None
        self.is_analyzing = False
        self.is_merging = False
        
        self._setup_application()
    
    def _setup_window(self):
        """Configure main window."""
        self.root.title(AppConstants.WINDOW_TITLE)
        self.root.geometry(AppConstants.WINDOW_SIZE)
        self.root.minsize(*AppConstants.MIN_WINDOW_SIZE)
        
        # Try to load icon
        try:
            icon_paths = [
                Path(__file__).parent / "assets" / "favicon.ico",
                Path(__file__).parent / "assets" / "icon.ico"
            ]
            
            for icon_path in icon_paths:
                if icon_path.exists():
                    self.root.iconbitmap(str(icon_path))
                    break
        except Exception:
            pass  # Continue without icon
    
    def _setup_application(self):
        """Initialize application."""
        self.ui_manager.setup_ui()
        self._setup_events()
        self._setup_shortcuts()
    
    def _setup_events(self):
        """Setup event handlers."""
        self.ui_manager.report_a_path.trace('w', lambda *args: self._on_path_change())
        self.ui_manager.report_b_path.trace('w', lambda *args: self._on_path_change())
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        self.root.bind('<Control-r>', lambda e: self.reset_application())
        self.root.bind('<Control-h>', lambda e: self.show_help_dialog())
        self.root.bind('<F1>', lambda e: self.show_help_dialog())
        self.root.bind('<F5>', lambda e: self.analyze_reports() if self._can_analyze() else None)
    
    # Public methods
    def browse_file(self, report_type: str):
        file_path = self.ui_manager.show_file_dialog(report_type)
        if file_path:
            if report_type == 'a':
                self.ui_manager.report_a_path.set(file_path)
            else:
                self.ui_manager.report_b_path.set(file_path)
    
    def browse_output(self):
        file_path = self.ui_manager.show_save_dialog()
        if file_path:
            self.ui_manager.output_path.set(file_path)
    
    def analyze_reports(self):
        if not self._can_analyze():
            return
        
        try:
            report_a = self._get_clean_path('a')
            report_b = self._get_clean_path('b')
            self.validation_service.validate_input_paths(report_a, report_b)
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))
            return
        
        self._start_analysis_thread()
    
    def start_merge(self):
        if not self.analysis_results:
            messagebox.showerror("Error", "Please analyze reports first")
            return
        
        try:
            output_path = self._get_clean_output_path()
            self.validation_service.validate_output_path(output_path)
        except Exception as e:
            messagebox.showerror("Output Validation Error", str(e))
            return
        
        totals = self.analysis_results['totals']
        if not messagebox.askyesno("Confirm Merge", 
                                  f"Ready to merge reports?\n\n"
                                  f"📊 Combined report will have:\n"
                                  f"📄 {totals['pages']} pages\n"
                                  f"🔖 {totals['bookmarks']} bookmarks\n"
                                  f"📐 {totals.get('measures', 0)} measures\n\n"
                                  f"💾 Output: {output_path}"):
            return
        
        self._start_merge_thread()
    
    def reset_application(self):
        if self.is_analyzing or self.is_merging:
            if not messagebox.askyesno("Confirm Reset", "An operation is in progress. Stop and reset?"):
                return
        
        # Clear state
        self.ui_manager.report_a_path.set("")
        self.ui_manager.report_b_path.set("")
        self.ui_manager.output_path.set("")
        self.ui_manager.theme_choice.set("report_a")
        self.analysis_results = None
        
        self.ui_manager.reset_ui_state()
        self.ui_manager.clear_analysis_log()
        self._log_message("✅ Application reset successfully!")
    
    def show_help_dialog(self):
        """Show help dialog with PBIR requirement information."""
        help_window = tk.Toplevel(self.root)
        help_window.title(f"{AppConstants.APP_NAME} - Help")
        help_window.geometry("650x650")  # Reduced height to eliminate bottom space
        help_window.resizable(False, False)  # Make non-resizable
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Center window
        help_window.geometry(f"+{self.root.winfo_rootx() + 50}+{self.root.winfo_rooty() + 50}")
        
        self._create_help_content(help_window)
    
    def show_about_dialog(self):
        """Show about dialog."""
        about_window = tk.Toplevel(self.root)
        about_window.title(f"About - {AppConstants.APP_NAME}")
        about_window.geometry("500x490")  # Increased height by 20px
        about_window.resizable(False, False)  # Fixed size for about dialog
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Center window
        about_window.geometry(f"+{self.root.winfo_rootx() + 100}+{self.root.winfo_rooty() + 100}")
        
        self._create_about_content(about_window)
    
    def open_company_website(self):
        try:
            webbrowser.open(AppConstants.COMPANY_WEBSITE)
            self._log_message(f"🌐 Opening {AppConstants.COMPANY_NAME} website...")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open website: {e}")
    
    def export_log(self):
        try:
            log_content = self.ui_manager.get_analysis_log_content()
            file_path = self.ui_manager.show_export_dialog()
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"{AppConstants.APP_NAME} - Analysis Log\n")
                    f.write(f"Generated by {AppConstants.COMPANY_NAME}\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(log_content)
                
                self._log_message(f"✅ Log exported to: {file_path}")
                messagebox.showinfo("Export Complete", f"Log exported successfully!\n\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export log: {e}")
    
    def auto_generate_output_path(self):
        report_a = self._get_clean_path('a')
        report_b = self._get_clean_path('b')
        
        if report_a and report_b:
            try:
                output_path = self.merger_engine.generate_output_path(report_a, report_b)
                self.ui_manager.output_path.set(output_path)
            except Exception:
                pass  # Ignore errors in auto-generation
    
    # Private helpers
    def _can_analyze(self) -> bool:
        return (bool(self._get_clean_path('a')) and bool(self._get_clean_path('b')) and 
                not self.is_analyzing and not self.is_merging)
    
    def _get_clean_path(self, report_type: str) -> str:
        if report_type == 'a':
            return self.merger_engine.clean_path(self.ui_manager.report_a_path.get())
        else:
            return self.merger_engine.clean_path(self.ui_manager.report_b_path.get())
    
    def _get_clean_output_path(self) -> str:
        return self.merger_engine.clean_path(self.ui_manager.output_path.get())
    
    def _on_path_change(self):
        self.auto_generate_output_path()
        self.ui_manager._update_ui_state()
    
    def _on_window_close(self):
        if self.is_analyzing or self.is_merging:
            if not messagebox.askyesno("Confirm Exit", "An operation is in progress. Exit anyway?"):
                return
        self.root.destroy()
    
    def _log_message(self, message: str):
        self.ui_manager.log_message(message)
    
    def _temp_log(self, message: str):
        print(f"Init: {message}")
    
    # Threading
    def _start_analysis_thread(self):
        self.is_analyzing = True
        self.ui_manager.set_analysis_state(True)
        self.ui_manager.clear_analysis_log()
        
        thread = threading.Thread(target=self._analyze_thread)
        thread.daemon = True
        thread.start()
    
    def _analyze_thread(self):
        try:
            report_a = self._get_clean_path('a')
            report_b = self._get_clean_path('b')
            
            results = self.merger_engine.analyze_reports(report_a, report_b)
            self.analysis_results = results
            
            # Update UI
            if results['themes']['conflict']:
                self.root.after(0, lambda: self.ui_manager.show_theme_selection(
                    results['themes']['theme_a'], results['themes']['theme_b']))
            else:
                self.root.after(0, lambda: self.ui_manager.hide_theme_selection())
                self.ui_manager.theme_choice.set("same")
            
            self.root.after(0, lambda: self.ui_manager.enable_merge_button())
            self._show_analysis_summary(results)
            
        except Exception as e:
            self._log_message(f"❌ Analysis failed: {e}")
            self.root.after(0, lambda: messagebox.showerror("Analysis Error", str(e)))
        
        finally:
            self.is_analyzing = False
            self.root.after(0, lambda: self.ui_manager.set_analysis_state(False))
    
    def _start_merge_thread(self):
        self.is_merging = True
        self.ui_manager.set_merge_state(True)
        
        thread = threading.Thread(target=self._merge_thread)
        thread.daemon = True
        thread.start()
    
    def _merge_thread(self):
        try:
            self._log_message("\n🚀 Starting merge operation...")
            
            report_a = self._get_clean_path('a')
            report_b = self._get_clean_path('b')
            output_path = self._get_clean_output_path()
            theme_choice = self.ui_manager.theme_choice.get()
            
            success = self.merger_engine.merge_reports(
                report_a, report_b, output_path, theme_choice, self.analysis_results
            )
            
            if success:
                self._log_message("✅ MERGE COMPLETED SUCCESSFULLY!")
                self._log_message(f"💾 Output: {output_path}")
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "Merge Complete", 
                    f"Merge completed successfully!\n\n💾 Output:\n{output_path}"
                ))
            else:
                self.root.after(0, lambda: messagebox.showerror(
                    "Merge Failed", "The merge operation failed. Check the log for details."
                ))
        
        except Exception as e:
            self._log_message(f"❌ Merge error: {e}")
            self.root.after(0, lambda: messagebox.showerror("Merge Error", str(e)))
        
        finally:
            self.is_merging = False
            self.root.after(0, lambda: self.ui_manager.set_merge_state(False))
    
    def _show_analysis_summary(self, results):
        """Show analysis summary."""
        self._log_message("\n📊 ANALYSIS SUMMARY")
        self._log_message("=" * 50)
        
        report_a = results['report_a']
        report_b = results['report_b']
        totals = results['totals']
        themes = results['themes']
        
        self._log_message(f"🔄 Combining: {report_a['name']} + {report_b['name']}")
        self._log_message(f"📄 Total Pages: {totals['pages']} ({report_a['pages']} + {report_b['pages']})")
        self._log_message(f"🔖 Total Bookmarks: {totals['bookmarks']} ({report_a['bookmarks']} + {report_b['bookmarks']})")
        
        if 'measures' in totals:
            self._log_message(f"📐 Total Measures: {totals['measures']}")
        
        if themes['conflict']:
            self._log_message(f"⚠️ Theme Conflict: {themes['theme_a']['name']} vs {themes['theme_b']['name']}")
            self._log_message("   🎨 Please select your preferred theme above")
        else:
            self._log_message(f"✅ Consistent Theme: {themes['theme_a']['name']}")
        
        self._log_message("✅ Analysis complete! Ready to merge.")
    
    def _create_help_content(self, help_window):
        """Create simplified help content with PBIR requirement information."""
        help_window.configure(bg=AppConstants.COLORS['background'])
        
        main_frame = ttk.Frame(help_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(main_frame, text=f"❓ {AppConstants.APP_NAME} - Help", 
                 font=('Segoe UI', 16, 'bold'), 
                 foreground=AppConstants.COLORS['primary']).pack(anchor=tk.W, pady=(0, 20))
        
        # PBIR Requirement Section (Prominent placement)
        pbir_frame = ttk.Frame(main_frame)
        pbir_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create a combined warning box for PBIR requirement and disclaimers
        warning_container = tk.Frame(pbir_frame, bg=AppConstants.COLORS['warning'], padx=15, pady=10, relief='solid', borderwidth=2)
        warning_container.pack(fill=tk.X)
        
        ttk.Label(warning_container, text="⚠️  IMPORTANT DISCLAIMERS & REQUIREMENTS", 
                 font=('Segoe UI', 12, 'bold'), 
                 background=AppConstants.COLORS['warning'],
                 foreground=AppConstants.COLORS['surface']).pack(anchor=tk.W)
        
        combined_warnings = [
            "• This tool ONLY works with PBIP enhanced report format (PBIR) files",
            "• This is NOT officially supported by Microsoft - use at your own discretion",
            "• Look for .pbip files with definition\\ folder (not report.json files)", 
            "• Always keep backups of your original reports before merging",
            "• Test thoroughly and validate merged results before production use",
            "• Enable 'Store reports using enhanced metadata format (PBIR)' in Power BI Desktop"
        ]
        
        for warning in combined_warnings:
            ttk.Label(warning_container, text=warning, font=('Segoe UI', 10),
                     background=AppConstants.COLORS['warning'],
                     foreground=AppConstants.COLORS['surface']).pack(anchor=tk.W, pady=1)
        
        # Help sections
        help_sections = [
            ("🚀 Quick Start", [
                "1. Select Report A and Report B (.pbip files)",
                "2. Click 'ANALYZE REPORTS' to validate and preview",
                "3. Choose theme if there's a conflict",
                "4. Click 'EXECUTE MERGE' to create combined report"
            ]),
            ("📁 File Requirements", [
                "✅ Only .pbip files (enhanced PBIR format) are supported",
                "✅ Reports must have definition\\ folder structure",
                "❌ Legacy format with report.json files are NOT supported",
                "❌ .pbix files are NOT supported"
            ]),
            ("⌨️ Keyboard Shortcuts", [
                "• Ctrl+R: Reset application",
                "• Ctrl+H or F1: Show this help",
                "• F5: Analyze reports (when ready)",
                "• Escape: Close dialogs"
            ])
        ]
        
        for title, items in help_sections:
            section_frame = ttk.Frame(main_frame)
            section_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Label(section_frame, text=title, font=('Segoe UI', 12, 'bold'),
                     foreground=AppConstants.COLORS['primary']).pack(anchor=tk.W)
            
            for item in items:
                ttk.Label(section_frame, text=f"   {item}", font=('Segoe UI', 10)).pack(anchor=tk.W, pady=1)
        
        # Close button positioned in bottom-right corner (overlapping)
        close_button = ttk.Button(help_window, text="❌ Close", command=help_window.destroy)
        close_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-15)
        
        help_window.bind('<Escape>', lambda e: help_window.destroy())
    
    def _create_about_content(self, about_window):
        """Create simplified about content."""
        about_window.configure(bg=AppConstants.COLORS['background'])
        
        main_frame = ttk.Frame(about_window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(main_frame, text="🚀", font=('Segoe UI', 48)).pack()
        ttk.Label(main_frame, text=AppConstants.APP_NAME, font=('Segoe UI', 18, 'bold'),
                 foreground=AppConstants.COLORS['primary']).pack(pady=(10, 5))
        ttk.Label(main_frame, text=AppConstants.APP_VERSION, font=('Segoe UI', 12),
                 foreground=AppConstants.COLORS['text_secondary']).pack()
        
        # Description
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(pady=(20, 0))
        
        description = [
            f"The {AppConstants.APP_NAME} intelligently combines",
            "Power BI thin reports while preserving all content.",
            "",
            "⚠️ Requires PBIP format (PBIR) files only",
            "⚠️ NOT officially supported by Microsoft",
            "",
            f"Built by {AppConstants.COMPANY_FOUNDER}",
            f"of {AppConstants.COMPANY_NAME}"
        ]
        
        for line in description:
            style = 'RequirementText.TLabel' if "⚠️" in line else None
            ttk.Label(desc_frame, text=line, font=('Segoe UI', 10), style=style).pack(pady=1)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(30, 0))
        
        ttk.Button(footer_frame, text="🌐 Visit Website", command=self.open_company_website).pack(side=tk.LEFT)
        ttk.Button(footer_frame, text="❌ Close", command=about_window.destroy).pack(side=tk.RIGHT)
        
        about_window.bind('<Escape>', lambda e: about_window.destroy())


def main():
    """Main function."""
    try:
        root = tk.Tk()
        app = EnhancedPowerBIReportMergerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Critical Error: {e}")


if __name__ == "__main__":
    main()