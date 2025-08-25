# flex-support-cli

A Python-based command-line tool for generating reports and managing configuration for **Twilio Flex** support operations.  
It centralizes authentication, report generation, and profile management into one CLI.

---

## 🚀 Features

- **Profile management**  
  Save multiple Twilio account credentials in `~/.flex-support-cli.toml` and switch with `--profile`.

- **Global options**  
  `--profile`, `--token`, and `--profile-only` available across all commands.

- **Reports (initial set)**  
  - **Taskrouter**: TaskRouter reports and helpers.  
  - **Conversations**: Conversations reports and helpers.  

- **Extensible architecture**  
  New reports can be added under `reports/` and wired into the CLI via subparsers.

---

## 📦 Installation

Clone the repo and install with [pipx](https://pypa.github.io/pipx/) (recommended):

```bash
git clone https://github.com/twilio-dclarke/flex-support-cli.git
cd FlexSupportCli
pipx install .
```

Or install locally for development:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

This installs the CLI as the command:

```bash
flex-support-cli
```

---

## 🔧 Configuration

### Profiles
Profiles are stored in `~/.flex-support-cli.toml`. Example:

```toml
[profiles.prod]
USERNAME = "ACxx or SKxx"
PASSWORD  = "your_auth_token_or_api_key_here"
WORKSPACE_SID = "WSxx"
```

### Creating a profile
```bash
flex-support-cli profiles --create-profile
```

---

## 🖥️ Usage

### Global options
- `--profile <name>` : select profile (default: `default`)  
- `--token <value>`  : override token/secret at runtime  

### Examples

**List profiles**
```bash
flex-support-cli profiles list
```

**Export TaskRouter Details**
```bash
flex-support-cli taskrouter --tr-queues --profile=PROFILE_NAME
```
```bash
flex-support-cli taskrouter --tr-workers --workspace-sid=WSxx --token=eyxxx
```

---

## 📄 License

MIT License (update as appropriate for your project).
