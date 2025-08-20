import os, pathlib
from dataclasses import dataclass
from typing import Optional

try:
    import tomllib  as _toml
except ImportError:
    print("tomllib not available, using tomli for Python < 3.11")
    try:
        import tomli as _toml
    except ImportError:
        print("tomli not available, please install tomli or use Python 3.11+")
        _toml = None

CONFIG_FILE = pathlib.Path.home() / ".flex-support-cli.toml"
DEFAULT_PROFILE = "guest"

class ConfigError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

@dataclass(frozen=True)
class Config:
    username: Optional[str] = None
    password: Optional[str] = None
    workspace_sid: Optional[str] = None
    guest_mode: Optional[bool] = True
    timeout_seconds: Optional[int] = 30
    timezone: Optional[str] = "UTC"
    inactivity_months: Optional[int] = 6
    workers_report: Optional[str] = "WORKERS_REPORT"
    queue_report: Optional[str] = "QUEUE_REPORT"
    profile: str = DEFAULT_PROFILE

    def auth_mode(self) -> str:
        """Determine the authentication mode based on provided credentials."""
        if self.username and self.password:
            return "username/password"
        else:
            return "token"
    
    def set_guest_mode(self, guest: bool):
        """Set the guest mode flag."""
        object.__setattr__(self, 'guest_mode', guest)
        
def _read_profiles() -> dict:
    """Read profiles from the configuration file."""
    if not CONFIG_FILE.exists():
        return {}
    if not _toml:
        raise ConfigError(f"Found {CONFIG_FILE}, but no toml parser.",0)
    
    with open(CONFIG_FILE, 'rb') as f:
        data = _toml.load(f)
        if isinstance(data, dict) and "profiles" in data:
            return data["profiles"]
        else:
            return {}

def list_profiles() -> list[str]:
    return sorted(_read_profiles().keys())

def load_config(profile: str = DEFAULT_PROFILE) -> Config:
    
    profiles = _read_profiles()
    merged = {}
    
    if profile != DEFAULT_PROFILE and profile not in profiles:
        raise ConfigError(f"Profile '{profile}' not found in {CONFIG_FILE}", 1)
    
    if profile == DEFAULT_PROFILE:
        cfg = Config(
            username = "token"
        )
        return cfg
    
    profile_data = profiles.get(profile, {})
    merged.update(profile_data)


    if cfg.auth_mode() == "username/password":
        cfg = Config(
            username=profile_data.get("USERNAME"),
            password=profile_data.get("PASSWORD"),
            workspace_sid=profile_data.get("WORKSPACE_SID", None),
            timeout_seconds=profile_data.get("TIMEOUT", 30),
            timezone=profile_data.get("TIMEZONE", "UTC"),
            profile=profile
        )
        cfg.set_guest_mode(False)
        return cfg
    else:
        return cfg


def save_profile(
        name: str, **values
) -> None:
    """Save a profile to the configuration file."""
    profiles = {}
    print(CONFIG_FILE)
    if CONFIG_FILE.exists():
        if not _toml:
            raise ConfigError("No TOML parser available", 0)
        with CONFIG_FILE.open("rb") as f:
            profiles = _toml.load(f) or {}
    if "profiles" not in profiles:
        profiles["profiles"] = {}      
    profiles["profiles"][name] = values

    lines = []
    for pname, table in profiles["profiles"].items():
        lines.append(f"[profiles.{pname}]\n")
        for key, value in table.items():
            if isinstance(value, str):
                lines.append(f"{key} = '{value}'\n")
            elif isinstance(value, bool):
                lines.append(f"{key} = {'true' if value else 'false'}\n")
            else:
                s = str(value).replace("\\", "\\\\").replace('"', '\\"')
                lines.append(f"{key} = {s}\n")
    
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text("\n".join(lines), encoding="utf-8")