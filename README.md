# README Generator Agent

A Python-based agent that automatically generates professional README.md files for GitHub repositories with customizable templates.

## Features

- **GitHub API Integration**: Fetches repository metadata automatically
- **Customizable Templates**: Use default template or create your own
- **Language Detection**: Automatically identifies tech stack and languages
- **Rich Metadata**: Includes stars, forks, issues, license, and dates
- **Windows 11 Optimized**: PowerShell wrapper for seamless Windows workflow
- **No Authentication Required**: Works without GitHub token (with rate limits)
- **Local File Generation**: Downloads README directly to your computer

## Prerequisites

- Python 3.7 or higher
- Windows 11 (optimized for, but works on other platforms)
- Internet connection for GitHub API access

## Installation

### Quick Setup

1. **Download** the project files to a directory
2. **Run setup** (PowerShell):
   ```powershell
   .\setup.ps1
   ```

### Manual Setup

```powershell
# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### Using PowerShell (Recommended for Windows)

```powershell
# Basic usage
.\generate-readme.ps1 owner/repo

# Examples
.\generate-readme.ps1 microsoft/vscode
.\generate-readme.ps1 torvalds/linux
.\generate-readme.ps1 https://github.com/octocat/Hello-World

# With custom output location
.\generate-readme.ps1 owner/repo -Output C:\Projects\README.md

# With custom template
.\generate-readme.ps1 owner/repo -Template my_template.md

# Create default template for customization
.\generate-readme.ps1 -CreateTemplate
```

### Using Python Directly

```bash
# Basic usage
python readme_agent.py owner/repo

# Examples
python readme_agent.py microsoft/vscode
python readme_agent.py torvalds/linux -o linux_README.md

# Create template
python readme_agent.py --create-template

# View all options
python readme_agent.py --help
```

## GitHub Token (Optional but Recommended)

Without a token, you're limited to 60 requests/hour. With a token, you get 5,000 requests/hour.

### Setting Up Token

1. **Create token** at: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `public_repo` (for public repos only)
   - Generate and copy the token

2. **Set environment variable** (PowerShell):
   ```powershell
   # Temporary (current session)
   $env:GITHUB_TOKEN = "your_token_here"
   
   # Permanent (add to PowerShell profile)
   notepad $PROFILE
   # Add this line:
   $env:GITHUB_TOKEN = "your_token_here"
   ```

3. **Or pass directly**:
   ```powershell
   .\generate-readme.ps1 owner/repo -Token "your_token_here"
   ```

## Template Customization

### Create Default Template

```powershell
python readme_agent.py --create-template
```

This creates `readme_template.md` with the default template.

### Template Variables

Available variables to use in your template:

| Variable | Description | Example |
|----------|-------------|---------|
| `{repo_name}` | Repository name | "vscode" |
| `{owner}` | Repository owner | "microsoft" |
| `{description}` | Short description | "Visual Studio Code" |
| `{overview}` | Detailed overview | Same as description by default |
| `{features}` | Features list | Default placeholder |
| `{install_instructions}` | Installation code | Default placeholder |
| `{usage_instructions}` | Usage examples | Default placeholder |
| `{tech_stack}` | Languages breakdown | "TypeScript: 85.2%" |
| `{created_date}` | Creation date | "May 15, 2015" |
| `{updated_date}` | Last update | "December 7, 2024" |
| `{stars}` | Star count | "150000" |
| `{forks}` | Fork count | "25000" |
| `{open_issues}` | Open issues | "5000" |
| `{license}` | License name | "MIT" |
| `{license_info}` | License details | "This project is licensed..." |
| `{primary_language}` | Main language | "TypeScript" |
| `{repo_url}` | Repository URL | Full GitHub URL |
| `{homepage_link}` | Homepage (if exists) | Formatted link |
| `{generation_date}` | Generated timestamp | Current date/time |

### Example Custom Template

```markdown
# {repo_name}

> {description}

## Quick Stats

⭐ Stars: {stars} | 🍴 Forks: {forks} | 🐛 Issues: {open_issues}

## Technology

{tech_stack}

## Installation

{install_instructions}

## License

{license_info}

---
Generated: {generation_date}
```

## Project Structure

```
readme-agent/
├── readme_agent.py         # Main Python agent
├── generate-readme.ps1     # PowerShell wrapper
├── setup.ps1               # Setup script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## How It Works

1. **Parse Input**: Accepts repository in format `owner/repo` or full GitHub URL
2. **Fetch Data**: Calls GitHub API to get repository metadata
3. **Extract Info**: Processes languages, dates, statistics
4. **Render Template**: Fills template with extracted data
5. **Save File**: Writes README.md to specified location

## API Rate Limits

- **Without token**: 60 requests/hour
- **With token**: 5,000 requests/hour

The agent will notify you if you hit the rate limit.

## Error Handling

The agent handles:
- Repository not found (404)
- API rate limit exceeded (403)
- Network errors
- Invalid repository format
- Missing permissions

## Examples

### Generate for popular repositories

```powershell
# Python
.\generate-readme.ps1 python/cpython

# Rust
.\generate-readme.ps1 rust-lang/rust

# React
.\generate-readme.ps1 facebook/react

# Linux kernel
.\generate-readme.ps1 torvalds/linux
```

### Batch generation

```powershell
$repos = @("microsoft/vscode", "torvalds/linux", "python/cpython")
foreach ($repo in $repos) {
    .\generate-readme.ps1 $repo
}
```

## Troubleshooting

### Python not found
```powershell
# Install from python.org or Microsoft Store
winget install Python.Python.3.12
```

### Module 'requests' not found
```powershell
pip install requests
```

### API rate limit
Set `GITHUB_TOKEN` environment variable with your personal access token.

### Permission denied on .ps1 files
```powershell
# Run once to enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Advanced Usage

### Custom template with specific sections

```powershell
# Create base template
python readme_agent.py --create-template

# Edit readme_template.md to your liking

# Use custom template
.\generate-readme.ps1 owner/repo -Template readme_template.md
```

### Integration with other tools

The agent can be integrated into your workflow:

```powershell
# Clone and generate README
git clone https://github.com/owner/repo.git
cd repo
..\readme-agent\generate-readme.ps1 owner/repo -Output README_NEW.md
```

## Security Notes

- **Never commit your GitHub token** to version control
- Use environment variables or secure credential storage
- Tokens should have minimal required permissions
- For public repositories, no special scopes needed

## Limitations

- Does not parse existing README content
- Requires internet connection
- Template variables are predefined (extensible in code)
- Generates markdown only (no HTML/RST)

## Contributing

Feel free to modify the code to suit your needs. The agent is designed to be straightforward and extensible.

## License

This project is provided as-is for developer use.

---

*Built for Windows 11 developers who need quick, professional README generation*
