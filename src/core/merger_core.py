"""
Enhanced Power BI Report Merger - Backend Core
Business logic, validation, and merger engine
Built by Reid Havens of Analytic Endeavors
"""

import json
import shutil
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Any, Callable

from core.constants import AppConstants

# =============================================================================
# EXCEPTION HIERARCHY
# =============================================================================

class PBIPMergerError(Exception):
    """Base exception for PBIP merger operations."""
    pass

class InvalidReportError(PBIPMergerError):
    """Raised when report structure is invalid or file not found."""
    pass

class ValidationError(PBIPMergerError):
    """Raised when input validation fails."""
    pass

class FileOperationError(PBIPMergerError):
    """Raised when file operations fail."""
    pass

class ThemeConflictError(PBIPMergerError):
    """Raised when theme conflicts cannot be resolved."""
    pass

class MergeOperationError(PBIPMergerError):
    """Raised when merge operations fail."""
    pass

# =============================================================================
# VALIDATION SERVICE
# =============================================================================

class ValidationService:
    """Centralized validation service for all input validation needs."""
    
    @staticmethod
    def validate_input_paths(path_a: str, path_b: str) -> None:
        """Validate input PBIP file paths with comprehensive error reporting."""
        errors = []
        
        # Validate Report A
        try:
            ValidationService._validate_single_pbip_path(path_a, "Report A")
        except ValidationError as e:
            errors.append(str(e))
        
        # Validate Report B
        try:
            ValidationService._validate_single_pbip_path(path_b, "Report B")
        except ValidationError as e:
            errors.append(str(e))
        
        # Check for same file
        if path_a and path_b and Path(path_a).resolve() == Path(path_b).resolve():
            errors.append("Report A and Report B cannot be the same file")
        
        if errors:
            raise ValidationError("Input validation failed:\n• " + "\n• ".join(errors))
    
    @staticmethod
    def _validate_single_pbip_path(file_path: str, report_name: str) -> None:
        """Validate a single PBIP file path."""
        if not file_path:
            raise ValidationError(f"{report_name} path is required")
        
        path_obj = Path(file_path)
        
        # Check file extension
        if not file_path.lower().endswith('.pbip'):
            raise ValidationError(f"{report_name} must be a .pbip file (got: {path_obj.suffix})")
        
        # Check file exists
        if not path_obj.exists():
            raise ValidationError(f"{report_name} file not found: {file_path}")
        
        # Check file is actually a file (not directory)
        if not path_obj.is_file():
            raise ValidationError(f"{report_name} path must point to a file, not a directory")
        
        # Check read permissions
        try:
            with path_obj.open('r') as f:
                pass  # Just test if we can open it
        except PermissionError:
            raise ValidationError(f"{report_name} file cannot be read (permission denied): {file_path}")
        except Exception as e:
            raise ValidationError(f"{report_name} file cannot be accessed: {str(e)}")
        
        # Check corresponding .Report directory exists
        report_dir = path_obj.parent / f"{path_obj.stem}.Report"
        if not report_dir.exists():
            raise ValidationError(f"{report_name} missing corresponding .Report directory: {report_dir}")
        
        if not report_dir.is_dir():
            raise ValidationError(f"{report_name} .Report path exists but is not a directory: {report_dir}")
    
    @staticmethod
    def validate_output_path(output_path: str) -> None:
        """Validate output path for write access and structure."""
        if not output_path:
            raise ValidationError("Output path is required")
        
        path_obj = Path(output_path)
        
        # Check file extension
        if not output_path.lower().endswith('.pbip'):
            raise ValidationError(f"Output file must be a .pbip file (got: {path_obj.suffix})")
        
        # Check parent directory exists and is writable
        parent_dir = path_obj.parent
        if not parent_dir.exists():
            raise ValidationError(f"Output directory does not exist: {parent_dir}")
        
        # Check write permissions on parent directory
        try:
            test_file = parent_dir / f"write_test_{uuid.uuid4().hex[:8]}.tmp"
            test_file.touch()
            test_file.unlink()
        except PermissionError:
            raise ValidationError(f"Cannot write to output directory (permission denied): {parent_dir}")
        except Exception as e:
            raise ValidationError(f"Cannot write to output directory: {str(e)}")
    
    @staticmethod
    def validate_thin_report_structure(report_dir: Path, report_name: str) -> None:
        """Comprehensive validation of thin report structure."""
        errors = []
        
        # Check .Report directory structure
        if not report_dir.exists():
            errors.append(f"{report_name} .Report directory not found: {report_dir}")
            raise ValidationError("\n• ".join(errors))
        
        # Check for semantic model (should not exist for thin reports)
        semantic_model_dir = report_dir.parent / f"{report_name}.SemanticModel"
        if semantic_model_dir.exists():
            errors.append(f"{report_name} appears to have a semantic model (not a thin report): {semantic_model_dir}")
        
        # Check required directories and files
        required_paths = [
            (report_dir / "definition", "definition directory"),
            (report_dir / "definition" / "report.json", "report.json file"),
            (report_dir / ".pbi", ".pbi directory"),
            (report_dir / ".platform", ".platform file")
        ]
        
        for path, description in required_paths:
            if not path.exists():
                errors.append(f"{report_name} missing {description}: {path}")
        
        # Validate key JSON files
        if (report_dir / "definition" / "report.json").exists():
            try:
                ValidationService.validate_json_structure(report_dir / "definition" / "report.json")
            except ValidationError as e:
                errors.append(f"{report_name} has invalid report.json: {str(e)}")
        
        if (report_dir / ".platform").exists():
            try:
                ValidationService.validate_json_structure(report_dir / ".platform", "platform")
            except ValidationError as e:
                errors.append(f"{report_name} has invalid .platform file: {str(e)}")
        
        if errors:
            raise ValidationError("Report structure validation failed:\n• " + "\n• ".join(errors))
    
    @staticmethod
    def validate_json_structure(file_path: Path, expected_schema_key: str = None) -> Dict[str, Any]:
        """Validate JSON file structure with optional schema checking."""
        if not file_path.exists():
            raise ValidationError(f"JSON file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in {file_path.name}: {str(e)}")
        except UnicodeDecodeError as e:
            raise ValidationError(f"Cannot read {file_path.name} (encoding issue): {str(e)}")
        except Exception as e:
            raise ValidationError(f"Cannot read {file_path.name}: {str(e)}")
        
        # Basic structure validation
        if not isinstance(data, dict):
            raise ValidationError(f"{file_path.name} must contain a JSON object, not {type(data).__name__}")
        
        # Optional schema validation
        if expected_schema_key and expected_schema_key in AppConstants.SCHEMA_URLS:
            expected_schema = AppConstants.SCHEMA_URLS[expected_schema_key]
            actual_schema = data.get('$schema', '')
            
            if actual_schema and expected_schema not in actual_schema:
                # Log warning but don't fail - schemas can be flexible
                pass
        
        return data

# =============================================================================
# THEME MANAGER
# =============================================================================

class ThemeManager:
    """Handles all theme-related operations for Power BI reports."""
    
    def __init__(self, logger_callback: Optional[Callable[[str], None]] = None):
        self.log_callback = logger_callback or self._default_log
    
    def _default_log(self, message: str) -> None:
        print(message)
    
    def detect_theme(self, report_dir: Path, report_name: str) -> Dict[str, Any]:
        """Detect theme used in a report - checks themeCollection for active theme."""
        theme_info = self._create_default_theme_info()
        
        # Check report.json for themeCollection
        report_json = report_dir / "definition" / "report.json"
        
        if not report_json.exists():
            return theme_info
        
        try:
            with open(report_json, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
        except:
            return theme_info
        
        # Look for themeCollection (modern PBIP format)
        theme_collection = report_data.get("themeCollection", {})
        if theme_collection:
            # The active theme is in customTheme, baseTheme is the foundation
            custom_theme = theme_collection.get("customTheme", {})
            base_theme = theme_collection.get("baseTheme", {})
            
            if custom_theme:
                theme_name = custom_theme.get("name", "")
                theme_type = custom_theme.get("type", "SharedResources")
                
                # Determine display name based on theme type and location
                if theme_type == "SharedResources":
                    if self._theme_exists_in_builtin(report_dir, theme_name):
                        display_name = f"Built-in Theme: {theme_name}"
                        actual_type = "builtin"
                    else:
                        display_name = f"Base Theme: {theme_name}"
                        actual_type = "base"
                else:
                    display_name = f"Custom Theme: {theme_name}"
                    actual_type = "custom"
                
                return {
                    "name": theme_name,
                    "display": display_name,
                    "theme_type": actual_type,
                    "active_theme": theme_collection,
                    "base_theme": base_theme
                }
            elif base_theme:
                # Only base theme, no custom theme applied
                theme_name = base_theme.get("name", "")
                return {
                    "name": theme_name,
                    "display": f"Base Theme: {theme_name}",
                    "theme_type": "base",
                    "active_theme": theme_collection,
                    "base_theme": base_theme
                }
        
        # Fallback to legacy theme detection
        return self._detect_legacy_theme(report_dir, report_data)
    
    def apply_theme_choice(self, choice: str, report_a_dir: Path, report_b_dir: Path, 
                          output_report_dir: Path, report_b_name: str) -> None:
        """Apply the selected theme choice with proper theme implementation."""
        self.log_callback(f"   🎨 Applying theme choice: {choice}")
        
        if choice == "report_b":
            # Use Report B theme - copy theme configuration and files
            self._apply_report_b_theme(report_b_dir, output_report_dir, report_b_name)
        elif choice == "same":
            # Themes are the same - ensure consistency
            self._ensure_theme_consistency(report_a_dir, report_b_dir, output_report_dir)
        # For "report_a", Report A theme is already in place (no action needed)
        
        self.log_callback("   ✅ Theme selection applied")
    
    def _create_default_theme_info(self) -> Dict[str, Any]:
        """Create default theme info structure."""
        return {
            "name": "default",
            "display": "Default Power BI Theme",
            "theme_type": "default",
            "active_theme": None
        }
    
    def _get_active_theme_from_report_json(self, report_dir, theme_info, report_name):
        """Extract active theme name from report.json."""
        report_json = report_dir / "definition" / "report.json"
        
        if not report_json.exists():
            return None
        
        try:
            with open(report_json, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
        except:
            return None
        
        if "theme" not in report_data:
            return None
        
        theme_section = report_data["theme"]
        theme_info["active_theme"] = theme_section
        
        # Handle inline themes (embedded themeJson)
        if "themeJson" in theme_section:
            theme_name = theme_section.get("name", "Inline Theme")
            theme_info.update({
                "name": theme_name,
                "display": f"Inline Theme: {theme_name}",
                "theme_type": "inline"
            })
            return None  # No file to search for
        
        # Handle named theme references
        if "name" in theme_section:
            return theme_section["name"]
        
        return None
    
    def _find_theme_by_name(self, report_dir, theme_name):
        """Find a specific theme by name in theme directories."""
        # Check BuiltInThemes first (these take precedence)
        builtin_theme = self._check_builtin_themes(report_dir, theme_name)
        if builtin_theme:
            return builtin_theme
        
        # Check BaseThemes (custom themes)
        base_theme = self._check_base_themes(report_dir, theme_name)
        if base_theme:
            return base_theme
        
        return None
    
    def _check_builtin_themes(self, report_dir, theme_name):
        """Check BuiltInThemes directory for a specific theme."""
        builtin_themes_dir = report_dir / "StaticResources" / "SharedResources" / "BuiltInThemes"
        if not builtin_themes_dir.exists():
            return None
        
        theme_file = builtin_themes_dir / f"{theme_name}.json"
        if theme_file.exists():
            return {
                "name": theme_name,
                "display": f"Built-in Theme: {theme_name}",
                "theme_type": "builtin",
                "active_theme": None
            }
        return None
    
    def _check_base_themes(self, report_dir, theme_name):
        """Check BaseThemes directory for a specific theme."""
        base_themes_dir = report_dir / "StaticResources" / "SharedResources" / "BaseThemes"
        if not base_themes_dir.exists():
            return None
        
        theme_file = base_themes_dir / f"{theme_name}.json"
        if theme_file.exists():
            return {
                "name": theme_name,
                "display": f"Custom Theme: {theme_name}",
                "theme_type": "base",
                "active_theme": None
            }
        return None
    
    def _create_missing_theme_info(self, theme_name):
        """Create theme info for a referenced but missing theme."""
        return {
            "name": theme_name,
            "display": f"Named Theme: {theme_name} (file not found)",
            "theme_type": "named",
            "active_theme": None
        }
    
    def _scan_for_implicit_themes(self, report_dir):
        """Scan for theme files when no explicit reference exists."""
        # Check BuiltInThemes first
        builtin_result = self._scan_theme_directory(report_dir, "BuiltInThemes", "Built-in Theme")
        if builtin_result:
            return builtin_result
        
        # Check BaseThemes
        base_result = self._scan_theme_directory(report_dir, "BaseThemes", "Custom Theme")
        if base_result:
            return base_result
        
        # No themes found - return default
        return self._create_default_theme_info()
    
    def _scan_theme_directory(self, report_dir, dir_name, theme_prefix):
        """Scan a specific theme directory for available themes."""
        theme_dir = report_dir / "StaticResources" / "SharedResources" / dir_name
        if not theme_dir.exists():
            return None
        
        theme_files = list(theme_dir.glob("*.json"))
        if not theme_files:
            return None
        
        # Use first theme file found
        theme_file = theme_files[0]
        theme_type = "builtin" if dir_name == "BuiltInThemes" else "base"
        
        if len(theme_files) == 1:
            # Single theme file - likely active
            display_suffix = ""
        else:
            # Multiple theme files - can't determine which is active
            display_suffix = " (multiple found)"
        
        return {
            "name": theme_file.stem,
            "display": f"{theme_prefix}: {theme_file.stem}{display_suffix}",
            "theme_type": theme_type,
            "active_theme": None
        }
    
    def _apply_report_b_theme(self, report_b_dir: Path, output_report_dir: Path, report_b_name: str) -> None:
        """Apply Report B theme to the output - complete implementation."""
        self.log_callback("     🔄 Applying Report B themes...")
        
        # Step 1: Read Report B's theme configuration
        report_b_json = report_b_dir / "definition" / "report.json"
        if not report_b_json.exists():
            self.log_callback("     ⚠️ Report B has no report.json - keeping Report A theme")
            return
        
        try:
            with open(report_b_json, 'r', encoding='utf-8') as f:
                report_b_data = json.load(f)
        except Exception as e:
            self.log_callback(f"     ⚠️ Cannot read Report B theme config: {e}")
            return
        
        # Step 2: Read current output report.json
        output_json = output_report_dir / "definition" / "report.json"
        try:
            with open(output_json, 'r', encoding='utf-8') as f:
                output_data = json.load(f)
        except Exception as e:
            self.log_callback(f"     ❌ Cannot read output report.json: {e}")
            return
        
        # Step 3: Copy themeCollection from Report B
        report_b_theme_collection = report_b_data.get("themeCollection", {})
        if report_b_theme_collection:
            output_data["themeCollection"] = report_b_theme_collection
            self.log_callback("     ✅ Theme collection updated")
        
        # Step 4: Update resourcePackages to include Report B's theme resources
        self._update_theme_resources(report_b_data, output_data, report_b_dir, output_report_dir)
        
        # Step 5: Copy theme files from Report B
        self._copy_theme_files(report_b_dir, output_report_dir, report_b_theme_collection)
        
        # Step 6: Write updated report.json
        try:
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
            self.log_callback("     ✅ Report.json updated with Report B theme")
        except Exception as e:
            self.log_callback(f"     ❌ Failed to update report.json: {e}")
    
    def _ensure_theme_consistency(self, report_a_dir: Path, report_b_dir: Path, 
                                 output_report_dir: Path) -> None:
        """Ensure theme consistency when both reports use the same theme."""
        self.log_callback("     ✅ Ensuring theme consistency...")
        
        # When themes are the same, we still need to ensure all required theme files are present
        # Read the current theme configuration to know what files we need
        output_json = output_report_dir / "definition" / "report.json"
        
        if not output_json.exists():
            return
        
        try:
            with open(output_json, 'r', encoding='utf-8') as f:
                output_data = json.load(f)
            
            theme_collection = output_data.get("themeCollection", {})
            if theme_collection:
                # Copy only the theme files that are actually being used
                self._copy_theme_files(report_b_dir, output_report_dir, theme_collection)
        except Exception as e:
            self.log_callback(f"     ⚠️ Error ensuring theme consistency: {e}")
        
        # Verify the theme configuration is properly set
        self._verify_theme_configuration(output_report_dir)
    
    def _theme_exists_in_builtin(self, report_dir: Path, theme_name: str) -> bool:
        """Check if theme exists in BuiltInThemes directory."""
        builtin_path = report_dir / "StaticResources" / "SharedResources" / "BuiltInThemes" / f"{theme_name}.json"
        return builtin_path.exists()
    
    def _detect_legacy_theme(self, report_dir: Path, report_data: Dict) -> Dict[str, Any]:
        """Fallback detection for legacy theme format."""
        # Legacy "theme" property (for older reports)
        if "theme" in report_data:
            theme_section = report_data["theme"]
            if "themeJson" in theme_section:
                theme_name = theme_section.get("name", "Inline Theme")
                return {
                    "name": theme_name,
                    "display": f"Inline Theme: {theme_name}",
                    "theme_type": "inline",
                    "active_theme": theme_section
                }
            elif "name" in theme_section:
                theme_name = theme_section["name"]
                return {
                    "name": theme_name,
                    "display": f"Named Theme: {theme_name}",
                    "theme_type": "named",
                    "active_theme": theme_section
                }
        
        return self._create_default_theme_info()
    
    def _update_theme_resources(self, report_b_data: Dict, output_data: Dict, 
                               report_b_dir: Path, output_report_dir: Path) -> None:
        """Update resourcePackages to include theme resources from Report B."""
        
        # Get Report B's theme resources
        report_b_packages = report_b_data.get("resourcePackages", [])
        output_packages = output_data.get("resourcePackages", [])
        
        # Find SharedResources in both
        output_shared = None
        report_b_shared = None
        
        for package in output_packages:
            if package.get("type") == "SharedResources":
                output_shared = package
                break
        
        for package in report_b_packages:
            if package.get("type") == "SharedResources":
                report_b_shared = package
                break
        
        if not report_b_shared:
            self.log_callback("     ⚠️ No SharedResources in Report B")
            return
        
        # Ensure output has SharedResources package
        if not output_shared:
            output_shared = {
                "name": "SharedResources",
                "type": "SharedResources",
                "items": []
            }
            output_packages.append(output_shared)
            output_data["resourcePackages"] = output_packages
        
        # Add theme items from Report B to output (avoiding duplicates)
        existing_items = {item.get("name", ""): item for item in output_shared.get("items", [])}
        
        for item in report_b_shared.get("items", []):
            item_name = item.get("name", "")
            item_type = item.get("type", "")
            
            # Add or update theme-related items
            if item_type in ["BaseTheme", "CustomTheme"] or item_name:
                existing_items[item_name] = item
                self.log_callback(f"     ✅ Added theme resource: {item_name} ({item_type})")
        
        # Update the items list
        output_shared["items"] = list(existing_items.values())
    
    def _copy_theme_files(self, report_b_dir: Path, output_report_dir: Path, 
                         theme_collection: Dict) -> None:
        """Copy only the active theme files from Report B to output."""
        
        if not theme_collection:
            self.log_callback("     ⚠️ No theme collection to copy")
            return
        
        # Get the active themes that need to be copied
        custom_theme = theme_collection.get("customTheme", {})
        base_theme = theme_collection.get("baseTheme", {})
        
        # Copy the active custom theme file
        if custom_theme:
            self._copy_specific_theme_file(report_b_dir, output_report_dir, custom_theme)
        
        # Copy the base theme file (always needed as foundation)
        if base_theme:
            self._copy_specific_theme_file(report_b_dir, output_report_dir, base_theme)
    
    def _copy_specific_theme_file(self, source_report_dir: Path, target_report_dir: Path,
                                 theme_info: Dict) -> None:
        """Copy a specific theme file based on theme info."""
        theme_name = theme_info.get("name", "")
        theme_type = theme_info.get("type", "SharedResources")
        
        if not theme_name:
            self.log_callback("     ⚠️ No theme name specified")
            return
        
        if theme_type == "SharedResources":
            # Check if it's in BuiltInThemes first
            if self._copy_builtin_theme_file(source_report_dir, target_report_dir, theme_name):
                return
            # Then check BaseThemes
            if self._copy_base_theme_file(source_report_dir, target_report_dir, theme_name):
                return
        elif theme_type == "RegisteredResources":
            # Copy from RegisteredResources
            self._copy_registered_theme_file(source_report_dir, target_report_dir, theme_name)
        
        self.log_callback(f"     ⚠️ Could not find theme file: {theme_name}")
    
    def _copy_builtin_theme_file(self, source_report_dir: Path, target_report_dir: Path,
                                theme_name: str) -> bool:
        """Copy a specific theme file from BuiltInThemes directory."""
        source_file = source_report_dir / "StaticResources" / "SharedResources" / "BuiltInThemes" / f"{theme_name}.json"
        
        if not source_file.exists():
            return False
        
        target_dir = target_report_dir / "StaticResources" / "SharedResources" / "BuiltInThemes"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_file = target_dir / f"{theme_name}.json"
        shutil.copy2(source_file, target_file)
        self.log_callback(f"     ✅ Copied built-in theme: {theme_name}.json")
        return True
    
    def _copy_base_theme_file(self, source_report_dir: Path, target_report_dir: Path,
                             theme_name: str) -> bool:
        """Copy a specific theme file from BaseThemes directory."""
        source_file = source_report_dir / "StaticResources" / "SharedResources" / "BaseThemes" / f"{theme_name}.json"
        
        if not source_file.exists():
            return False
        
        target_dir = target_report_dir / "StaticResources" / "SharedResources" / "BaseThemes"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_file = target_dir / f"{theme_name}.json"
        shutil.copy2(source_file, target_file)
        self.log_callback(f"     ✅ Copied base theme: {theme_name}.json")
        return True
    
    def _copy_registered_theme_file(self, source_report_dir: Path, target_report_dir: Path,
                                   theme_name: str) -> bool:
        """Copy a specific theme file from RegisteredResources directory."""
        # Look for the theme file (might have a different filename)
        source_reg_dir = source_report_dir / "StaticResources" / "RegisteredResources"
        
        if not source_reg_dir.exists():
            return False
        
        # Find theme file by name (might be named differently)
        theme_file = None
        for json_file in source_reg_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)
                if theme_data.get("name") == theme_name:
                    theme_file = json_file
                    break
            except:
                continue
        
        if not theme_file:
            return False
        
        target_dir = target_report_dir / "StaticResources" / "RegisteredResources"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_file = target_dir / theme_file.name
        shutil.copy2(theme_file, target_file)
        self.log_callback(f"     ✅ Copied registered theme: {theme_file.name}")
        return True
    
    def _copy_theme_directory(self, source_report_dir: Path, target_report_dir: Path, 
                             theme_dir_name: str) -> None:
        """Copy a theme directory (BaseThemes or BuiltInThemes)."""
        source_theme_dir = source_report_dir / "StaticResources" / "SharedResources" / theme_dir_name
        target_theme_dir = target_report_dir / "StaticResources" / "SharedResources" / theme_dir_name
        
        if not source_theme_dir.exists():
            return
        
        # Create target directory
        target_theme_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all theme files
        for theme_file in source_theme_dir.glob("*.json"):
            target_file = target_theme_dir / theme_file.name
            shutil.copy2(theme_file, target_file)
            self.log_callback(f"     ✅ Copied theme file: {theme_dir_name}/{theme_file.name}")
    
    def _copy_registered_themes(self, source_report_dir: Path, target_report_dir: Path) -> None:
        """Copy custom theme files from RegisteredResources."""
        source_reg_dir = source_report_dir / "StaticResources" / "RegisteredResources"
        target_reg_dir = target_report_dir / "StaticResources" / "RegisteredResources"
        
        if not source_reg_dir.exists():
            return
        
        target_reg_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy JSON files that might be custom themes
        for theme_file in source_reg_dir.glob("*.json"):
            target_file = target_reg_dir / theme_file.name
            shutil.copy2(theme_file, target_file)
            self.log_callback(f"     ✅ Copied registered theme: {theme_file.name}")
    
    def _verify_theme_configuration(self, output_report_dir: Path) -> None:
        """Verify that the theme configuration is correct."""
        output_json = output_report_dir / "definition" / "report.json"
        
        if not output_json.exists():
            self.log_callback("     ⚠️ No report.json found for verification")
            return
        
        try:
            with open(output_json, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            theme_collection = report_data.get("themeCollection", {})
            if theme_collection:
                custom_theme = theme_collection.get("customTheme", {})
                base_theme = theme_collection.get("baseTheme", {})
                
                if custom_theme:
                    theme_name = custom_theme.get("name", "")
                    self.log_callback(f"     ✅ Theme configuration verified: Active theme is {theme_name}")
                elif base_theme:
                    theme_name = base_theme.get("name", "")
                    self.log_callback(f"     ✅ Theme configuration verified: Base theme is {theme_name}")
                else:
                    self.log_callback("     ⚠️ Theme collection exists but no themes defined")
            else:
                self.log_callback("     ⚠️ No theme collection found in output")
                
        except Exception as e:
            self.log_callback(f"     ⚠️ Theme verification failed: {e}")

# =============================================================================
# MERGER ENGINE
# =============================================================================

class MergerEngine:
    """Core business logic for Power BI report merging operations."""
    
    def __init__(self, logger_callback: Optional[Callable[[str], None]] = None):
        self.log_callback = logger_callback or self._default_log
        self.validation_service = ValidationService()
        self.theme_manager = ThemeManager(logger_callback=self.log_callback)
        self._path_cache = {}
    
    def _default_log(self, message: str) -> None:
        print(message)
    
    def clean_path(self, path_str: str) -> str:
        """Clean a file path by removing quotes and trimming whitespace."""
        if not path_str:
            return path_str
        
        # Check cache first
        if path_str in self._path_cache:
            return self._path_cache[path_str]
        
        # Clean the path
        cleaned = path_str.strip()
        
        # Remove surrounding quotes
        if len(cleaned) >= 2:
            if (cleaned.startswith('"') and cleaned.endswith('"')) or \
               (cleaned.startswith("'") and cleaned.endswith("'")):
                cleaned = cleaned[1:-1]
        
        # Normalize path separators
        cleaned = str(Path(cleaned)) if cleaned else cleaned
        
        # Cache the result
        self._path_cache[path_str] = cleaned
        return cleaned
    
    def analyze_reports(self, report_a_path: str, report_b_path: str) -> Dict[str, Any]:
        """Perform comprehensive analysis of both reports."""
        self.log_callback("🔍 Starting comprehensive report analysis...")
        
        # Clean and validate paths
        clean_path_a = self.clean_path(report_a_path)
        clean_path_b = self.clean_path(report_b_path)
        
        # Validate inputs
        self.validation_service.validate_input_paths(clean_path_a, clean_path_b)
        
        # Get report directories
        report_a_dir = Path(clean_path_a).parent / f"{Path(clean_path_a).stem}.Report"
        report_b_dir = Path(clean_path_b).parent / f"{Path(clean_path_b).stem}.Report"
        
        # Validate thin report structures
        self.validation_service.validate_thin_report_structure(report_a_dir, Path(clean_path_a).stem)
        self.validation_service.validate_thin_report_structure(report_b_dir, Path(clean_path_b).stem)
        
        self.log_callback("✅ Both reports are valid thin reports")
        
        # Analyze content
        pages_a = self._count_pages(report_a_dir)
        pages_b = self._count_pages(report_b_dir)
        bookmarks_a = self._count_bookmarks(report_a_dir)
        bookmarks_b = self._count_bookmarks(report_b_dir)
        
        # Analyze themes
        theme_a_info = self.theme_manager.detect_theme(report_a_dir, Path(clean_path_a).stem)
        theme_b_info = self.theme_manager.detect_theme(report_b_dir, Path(clean_path_b).stem)
        
        # Analyze measures
        measures_a = self._get_measures_from_report(report_a_dir, Path(clean_path_a).stem)
        measures_b = self._get_measures_from_report(report_b_dir, Path(clean_path_b).stem)
        
        # Calculate conflicts
        measure_conflicts = self._find_measure_conflicts(measures_a, measures_b)
        total_measures_a = sum(len(measures) if measures else 0 for measures in measures_a.values())
        total_measures_b = sum(len(measures) if measures else 0 for measures in measures_b.values())
        
        self.log_callback(f"   📄 Report A: {pages_a} pages, {bookmarks_a} bookmarks, {total_measures_a} measures")
        self.log_callback(f"   📄 Report B: {pages_b} pages, {bookmarks_b} bookmarks, {total_measures_b} measures")
        self.log_callback(f"   🎨 Theme A: {theme_a_info['display']}")
        self.log_callback(f"   🎨 Theme B: {theme_b_info['display']}")
        
        if measure_conflicts:
            self.log_callback(f"   ⚠️ {len(measure_conflicts)} measure conflicts detected")
        
        return {
            'report_a': {
                'path': clean_path_a,
                'name': Path(clean_path_a).stem,
                'pages': pages_a,
                'bookmarks': bookmarks_a,
                'measures': total_measures_a
            },
            'report_b': {
                'path': clean_path_b,
                'name': Path(clean_path_b).stem,
                'pages': pages_b,
                'bookmarks': bookmarks_b,
                'measures': total_measures_b
            },
            'themes': {
                'theme_a': theme_a_info,
                'theme_b': theme_b_info,
                'conflict': theme_a_info['name'] != theme_b_info['name']
            },
            'measures': {
                'conflicts': measure_conflicts,
                'total_a': total_measures_a,
                'total_b': total_measures_b
            },
            'totals': {
                'pages': pages_a + pages_b,
                'bookmarks': bookmarks_a + bookmarks_b,
                'measures': total_measures_a + total_measures_b
            }
        }
    
    def merge_reports(self, report_a_path: str, report_b_path: str, output_path: str, 
                     theme_choice: str, analysis_results: Dict[str, Any]) -> bool:
        """Execute the report merge operation."""
        try:
            self.log_callback("🚀 Starting merge operation...")
            
            # Get clean paths
            clean_path_a = self.clean_path(report_a_path)
            clean_path_b = self.clean_path(report_b_path)
            clean_output = self.clean_path(output_path)
            
            # Setup merge environment
            self._setup_merge_environment(clean_path_a, clean_output)
            
            # Execute merge steps with progress
            merge_stats = self._execute_merge_steps(clean_path_a, clean_path_b, clean_output, theme_choice)
            
            # Finalize output
            self._finalize_merge_output(clean_output, merge_stats)
            
            self.log_callback("🎉 MERGE COMPLETED SUCCESSFULLY!")
            return True
            
        except Exception as e:
            self.log_callback(f"❌ Merge operation failed: {e}")
            self._cleanup_failed_merge(clean_output)
            return False
    
    def generate_output_path(self, report_a_path: str, report_b_path: str) -> str:
        """Generate output path based on input files."""
        path_a = Path(self.clean_path(report_a_path))
        path_b = Path(self.clean_path(report_b_path))
        
        output_dir = path_a.parent
        output_name = f"Combined_{path_a.stem}_{path_b.stem}.pbip"
        
        return str(output_dir / output_name)
    
    # Private helper methods
    def _count_pages(self, report_dir: Path) -> int:
        """Count pages in a report."""
        pages_dir = report_dir / "definition" / "pages"
        if not pages_dir.exists():
            return 0
        return len([d for d in pages_dir.iterdir() if d.is_dir() and d.name != "pages.json"])
    
    def _count_bookmarks(self, report_dir: Path) -> int:
        """Count bookmarks in a report."""
        bookmarks_dir = report_dir / "definition" / "bookmarks"
        if not bookmarks_dir.exists():
            return 0
        return len(list(bookmarks_dir.glob("*.bookmark.json")))
    
    def _get_measures_from_report(self, report_dir: Path, report_name: str) -> Dict[str, List]:
        """Get measures from a report's reportExtensions.json."""
        measures = {}
        extensions_file = report_dir / "definition" / "reportExtensions.json"
        
        try:
            data = self.validation_service.validate_json_structure(extensions_file)
            entities = data.get("entities", [])
            
            for entity in entities:
                if isinstance(entity, dict):
                    entity_name = entity.get("name", "")
                    if entity_name:
                        entity_measures = entity.get("measures", [])
                        measures[entity_name] = entity_measures or []
            
            return measures
            
        except Exception as e:
            self.log_callback(f"   ⚠️ Warning: Could not get measures from {report_name}: {e}")
            return measures
    
    def _find_measure_conflicts(self, measures_a: Dict[str, List], measures_b: Dict[str, List]) -> List[str]:
        """Find conflicting measure names between reports."""
        conflicts = []
        
        for entity_name in measures_a:
            if entity_name in measures_b:
                a_measures = measures_a[entity_name] or []
                b_measures = measures_b[entity_name] or []
                
                a_measure_names = {m.get("name", "") for m in a_measures if isinstance(m, dict)}
                b_measure_names = {m.get("name", "") for m in b_measures if isinstance(m, dict)}
                common_measures = a_measure_names & b_measure_names
                
                if common_measures:
                    conflicts.extend(list(common_measures))
        
        return conflicts
    
    def _setup_merge_environment(self, report_a_path: str, output_path: str):
        """Setup merge environment and prepare base structure."""
        self.log_callback("🏗️ Setting up merge environment...")
        
        output_file = Path(output_path)
        output_report_dir = output_file.parent / f"{output_file.stem}.Report"
        report_a_dir = Path(report_a_path).parent / f"{Path(report_a_path).stem}.Report"
        
        # Clean up existing output
        if output_report_dir.exists():
            shutil.rmtree(output_report_dir)
        if output_file.exists():
            output_file.unlink()
        
        # Copy Report A as base
        shutil.copytree(report_a_dir, output_report_dir)
        
        self.log_callback("   ✅ Base structure prepared")
    
    def _execute_merge_steps(self, report_a_path: str, report_b_path: str, 
                           output_path: str, theme_choice: str) -> Dict[str, int]:
        """Execute the core merge steps with actual implementations."""
        merge_stats = {'pages': 0, 'bookmarks': 0, 'measures': 0}
        
        # Get directories
        report_b_dir = Path(report_b_path).parent / f"{Path(report_b_path).stem}.Report"
        output_file = Path(output_path)
        output_report_dir = output_file.parent / f"{output_file.stem}.Report"
        report_a_dir = Path(report_a_path).parent / f"{Path(report_a_path).stem}.Report"
        
        # Actual merge operations
        steps = [
            ("Merging pages", lambda: self._merge_pages_smart(report_b_dir, output_report_dir, Path(report_b_path).stem)),
            ("Merging bookmarks", lambda: self._merge_bookmarks_smart(report_b_dir, output_report_dir, Path(report_b_path).stem)),
            ("Merging measures", lambda: self._merge_local_measures(report_a_dir, report_b_dir, output_report_dir)),
            ("Applying theme selection", lambda: self.theme_manager.apply_theme_choice(theme_choice, report_a_dir, report_b_dir, output_report_dir, Path(report_b_path).stem))
        ]
        
        for step_name, step_func in steps:
            self.log_callback(f"   {step_name}...")
            
            try:
                if step_name == "Merging pages":
                    merge_stats['pages'] = step_func()
                elif step_name == "Merging bookmarks":
                    merge_stats['bookmarks'] = step_func()
                elif step_name == "Merging measures":
                    merge_stats['measures'] = step_func()
                else:
                    step_func()  # Theme application
                
                self.log_callback(f"   ✅ {step_name} completed")
            except Exception as e:
                self.log_callback(f"   ❌ {step_name} failed: {e}")
                raise
        
        # Rebuild pages.json after merging
        self._rebuild_pages_json(output_report_dir / "definition" / "pages")
        
        return merge_stats
    
    def _finalize_merge_output(self, output_path: str, merge_stats: Dict[str, int]):
        """Finalize merge output and create PBIP file."""
        self.log_callback("🏁 Finalizing output...")
        
        # Create PBIP file
        output_file = Path(output_path)
        pbip_data = {
            "$schema": AppConstants.SCHEMA_URLS['pbip'],
            "version": "1.0",
            "artifacts": [{"report": {"path": f"{output_file.stem}.Report"}}],
            "settings": {"enableAutoRecovery": True}
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pbip_data, f, indent=2)
        
        # Log statistics
        self.log_callback(f"📊 Merge Statistics:")
        for key, value in merge_stats.items():
            self.log_callback(f"   {key.title()}: {value}")
    
    def _cleanup_failed_merge(self, output_path: str):
        """Clean up partial merge artifacts after failure."""
        try:
            self.log_callback("🧹 Cleaning up failed merge artifacts...")
            
            output_file = Path(output_path)
            output_report_dir = output_file.parent / f"{output_file.stem}.Report"
            
            if output_report_dir.exists():
                shutil.rmtree(output_report_dir, ignore_errors=True)
            if output_file.exists():
                output_file.unlink(missing_ok=True)
                
            self.log_callback("   ✅ Cleanup completed")
        except Exception as e:
            self.log_callback(f"   ⚠️ Warning: Cleanup error: {e}")
    
    def _merge_pages_smart(self, source_report_dir: Path, target_report_dir: Path, source_name: str) -> int:
        """Smart page merging with conflict resolution."""
        source_pages_dir = source_report_dir / "definition" / "pages"
        target_pages_dir = target_report_dir / "definition" / "pages"
        
        if not source_pages_dir.exists():
            return 0
        
        existing_pages = {d.name for d in target_pages_dir.iterdir() if d.is_dir() and d.name != "pages.json"}
        merged_count = 0
        
        for page_dir in source_pages_dir.iterdir():
            if page_dir.is_dir() and page_dir.name != "pages.json":
                
                # Resolve naming conflicts
                new_name = page_dir.name
                counter = 1
                while new_name in existing_pages:
                    new_name = f"{page_dir.name}_{source_name}_{counter}"
                    counter += 1
                
                target_page_dir = target_pages_dir / new_name
                shutil.copytree(page_dir, target_page_dir)
                
                # Update page metadata if renamed
                if new_name != page_dir.name:
                    self._update_page_metadata(target_page_dir, source_name)
                
                existing_pages.add(new_name)
                merged_count += 1
                self.log_callback(f"     ✅ Merged page: {page_dir.name}")
        
        return merged_count
    
    def _update_page_metadata(self, page_dir: Path, source_name: str):
        """Update page metadata after renaming."""
        page_json_file = page_dir / "page.json"
        
        if not page_json_file.exists():
            return
        
        try:
            with open(page_json_file, 'r', encoding='utf-8') as f:
                page_data = json.load(f)
            
            # Update display name and internal name
            if "displayName" in page_data:
                page_data["displayName"] = f"{page_data['displayName']} ({source_name})"
            
            if "name" in page_data:
                page_data["name"] = f"{page_data['name']}_{source_name}"
            
            with open(page_json_file, 'w', encoding='utf-8') as f:
                json.dump(page_data, f, indent=2)
                
        except Exception as e:
            self.log_callback(f"       ⚠️ Warning: Could not update page metadata: {e}")
    
    def _merge_bookmarks_smart(self, source_report_dir: Path, target_report_dir: Path, source_name: str) -> int:
        """Smart bookmark merging."""
        source_bookmarks_dir = source_report_dir / "definition" / "bookmarks"
        target_bookmarks_dir = target_report_dir / "definition" / "bookmarks"
        
        if not source_bookmarks_dir.exists():
            return 0
        
        target_bookmarks_dir.mkdir(parents=True, exist_ok=True)
        existing_bookmarks = {f.name for f in target_bookmarks_dir.glob("*.bookmark.json")}
        merged_count = 0
        
        for bookmark_file in source_bookmarks_dir.glob("*.bookmark.json"):
            # Resolve naming conflicts
            new_name = bookmark_file.name
            counter = 1
            while new_name in existing_bookmarks:
                name_part = bookmark_file.stem.replace(".bookmark", "")
                new_name = f"{name_part}_{source_name}_{counter}.bookmark.json"
                counter += 1
            
            target_file = target_bookmarks_dir / new_name
            shutil.copy2(bookmark_file, target_file)
            
            existing_bookmarks.add(new_name)
            merged_count += 1
            self.log_callback(f"     ✅ Merged bookmark: {bookmark_file.name}")
        
        # Update bookmarks.json
        self._update_bookmarks_json(target_bookmarks_dir)
        
        return merged_count
    
    def _update_bookmarks_json(self, bookmarks_dir: Path):
        """Update bookmarks.json file."""
        bookmark_files = list(bookmarks_dir.glob("*.bookmark.json"))
        
        if not bookmark_files:
            return
        
        bookmarks_data = {
            "bookmarks": [{"name": bf.stem.replace(".bookmark", "")} for bf in bookmark_files]
        }
        
        # Add schema if available
        schema_url = AppConstants.SCHEMA_URLS.get('bookmarks')
        if schema_url:
            bookmarks_data["$schema"] = schema_url
        
        bookmarks_json_file = bookmarks_dir / "bookmarks.json"
        with open(bookmarks_json_file, 'w', encoding='utf-8') as f:
            json.dump(bookmarks_data, f, indent=2)
    
    def _merge_local_measures(self, report_a_dir: Path, report_b_dir: Path, target_report_dir: Path) -> int:
        """Merge local measures from thin reports."""
        target_extensions_file = target_report_dir / "definition" / "reportExtensions.json"
        
        entities_dict = {}
        
        # Process Report A measures (already copied as base)
        report_a_extensions = report_a_dir / "definition" / "reportExtensions.json"
        if report_a_extensions.exists():
            entities_dict.update(self._load_measures_from_file(report_a_extensions, "Report A"))
        
        # Process Report B measures
        report_b_extensions = report_b_dir / "definition" / "reportExtensions.json"
        if report_b_extensions.exists():
            b_entities = self._load_measures_from_file(report_b_extensions, "Report B")
            
            # Merge with conflict resolution
            for entity_name, entity_data in b_entities.items():
                if entity_name in entities_dict:
                    # Merge measures, handling conflicts
                    existing_names = {m["name"] for m in entities_dict[entity_name]["measures"]}
                    
                    for measure in entity_data["measures"]:
                        if measure["name"] in existing_names:
                            # Rename conflicting measure
                            measure["name"] = f"{measure['name']}_B"
                            self.log_callback(f"     ⚠️ Renamed conflicting measure to: {measure['name']}")
                        
                        entities_dict[entity_name]["measures"].append(measure)
                else:
                    # New entity
                    entities_dict[entity_name] = entity_data
        
        if not entities_dict:
            return 0
        
        # Create combined reportExtensions.json
        combined_data = {
            "name": "extension",
            "entities": list(entities_dict.values())
        }
        
        # Add schema if available
        schema_url = AppConstants.SCHEMA_URLS.get('report_extension')
        if schema_url:
            combined_data["$schema"] = schema_url
        
        with open(target_extensions_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2)
        
        total_measures = sum(len(entity["measures"]) for entity in entities_dict.values())
        self.log_callback(f"     ✅ Combined {total_measures} local measures across {len(entities_dict)} entities")
        
        return total_measures
    
    def _load_measures_from_file(self, extensions_file: Path, report_name: str) -> Dict[str, Dict]:
        """Load measures from a reportExtensions.json file."""
        entities_dict = {}
        
        try:
            data = self.validation_service.validate_json_structure(extensions_file)
            if not data:
                return entities_dict
            
            entities = data.get("entities", [])
            if entities is None:
                entities = []
            
            for entity in entities:
                if not isinstance(entity, dict):
                    continue
                    
                entity_name = entity.get("name", "")
                if entity_name:
                    measures = entity.get("measures", [])
                    if measures is None:
                        measures = []
                    
                    entities_dict[entity_name] = {
                        "name": entity_name,
                        "measures": measures
                    }
                    
                    # Preserve additional entity properties
                    for key, value in entity.items():
                        if key not in ["name", "measures"]:
                            entities_dict[entity_name][key] = value
            
            return entities_dict
            
        except Exception as e:
            self.log_callback(f"     ⚠️ Warning: Could not load measures from {report_name}: {e}")
            return entities_dict
    
    def _rebuild_pages_json(self, pages_dir: Path):
        """Rebuild pages.json file after merging."""
        all_page_names = []
        
        for page_dir in pages_dir.iterdir():
            if page_dir.is_dir() and page_dir.name != "pages.json":
                page_json_file = page_dir / "page.json"
                if page_json_file.exists():
                    try:
                        with open(page_json_file, 'r', encoding='utf-8') as f:
                            page_data = json.load(f)
                        all_page_names.append(page_data.get("name", page_dir.name))
                    except:
                        all_page_names.append(page_dir.name)
        
        if not all_page_names:
            return
        
        # Create updated pages.json with correct structure
        pages_data = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
            "pageOrder": all_page_names,
            "activePageName": all_page_names[0] if all_page_names else None
        }
        
        pages_json_file = pages_dir / "pages.json"
        with open(pages_json_file, 'w', encoding='utf-8') as f:
            json.dump(pages_data, f, indent=2)
        
        self.log_callback(f"     ✅ Rebuilt pages.json with {len(all_page_names)} pages")
