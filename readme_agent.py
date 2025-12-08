#!/usr/bin/env python3
"""
README Generator Agent
Generates professional README.md files for GitHub repositories using customizable templates.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
import requests
from datetime import datetime


class GitHubAPIClient:
    """Client for interacting with GitHub API"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository information from GitHub API"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 404:
            raise ValueError(f"Repository {owner}/{repo} not found")
        elif response.status_code == 403:
            raise ValueError("API rate limit exceeded. Set GITHUB_TOKEN environment variable.")
        elif response.status_code != 200:
            raise ValueError(f"GitHub API error: {response.status_code}")
        
        return response.json()
    
    def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Fetch repository languages"""
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return {}
    
    def get_readme_content(self, owner: str, repo: str) -> Optional[str]:
        """Fetch existing README if it exists"""
        url = f"{self.base_url}/repos/{owner}/{repo}/readme"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get('content', '')
        return None


class TemplateEngine:
    """Template engine for README generation"""
    
    def __init__(self, template_path: Optional[Path] = None):
        self.template_path = template_path
        if template_path and template_path.exists():
            self.template = template_path.read_text(encoding='utf-8')
        else:
            self.template = self.get_default_template()
    
    @staticmethod
    def get_default_template() -> str:
        """Returns the default README template"""
        return """# {repo_name}

{description}

## Overview

{overview}

## Features

{features}

## Installation

```bash
git clone https://github.com/{owner}/{repo_name}.git
cd {repo_name}
```

{install_instructions}

## Usage

{usage_instructions}

## Technology Stack

{tech_stack}

## Repository Information

- **Created:** {created_date}
- **Last Updated:** {updated_date}
- **Stars:** {stars}
- **Forks:** {forks}
- **Open Issues:** {open_issues}
- **License:** {license}
- **Primary Language:** {primary_language}

## Links

- **Repository:** [{repo_url}]({repo_url})
{homepage_link}

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

{license_info}

---

*This README was generated on {generation_date}*
"""
    
    def render(self, data: Dict[str, Any]) -> str:
        """Render the template with provided data"""
        return self.template.format(**data)


class ReadmeGenerator:
    """Main README generator agent"""
    
    def __init__(self, github_token: Optional[str] = None, template_path: Optional[Path] = None):
        self.api_client = GitHubAPIClient(github_token)
        self.template_engine = TemplateEngine(template_path)
    
    def parse_repo_url(self, repo_identifier: str) -> tuple[str, str]:
        """Parse repository URL or owner/repo format"""
        # Handle full GitHub URLs
        if repo_identifier.startswith('http'):
            parts = repo_identifier.rstrip('/').split('/')
            return parts[-2], parts[-1]
        
        # Handle owner/repo format
        if '/' in repo_identifier:
            owner, repo = repo_identifier.split('/', 1)
            return owner, repo
        
        raise ValueError("Invalid repository format. Use 'owner/repo' or full GitHub URL")
    
    def extract_data(self, repo_info: Dict[str, Any], languages: Dict[str, int]) -> Dict[str, Any]:
        """Extract and format data for template"""
        
        # Calculate primary language
        primary_language = "Not specified"
        if languages:
            primary_language = max(languages.items(), key=lambda x: x[1])[0]
        
        # Format tech stack
        tech_stack = self._format_tech_stack(languages)
        
        # Format dates
        created_date = self._format_date(repo_info.get('created_at', ''))
        updated_date = self._format_date(repo_info.get('updated_at', ''))
        
        # License info
        license_info = "No license specified"
        license_name = "None"
        if repo_info.get('license'):
            license_name = repo_info['license'].get('name', 'Unknown')
            license_spdx = repo_info['license'].get('spdx_id', '')
            if license_spdx:
                license_info = f"This project is licensed under the {license_name} License."
        
        # Homepage link
        homepage_link = ""
        if repo_info.get('homepage'):
            homepage_link = f"- **Homepage:** [{repo_info['homepage']}]({repo_info['homepage']})"
        
        return {
            'repo_name': repo_info.get('name', 'Repository'),
            'owner': repo_info.get('owner', {}).get('login', ''),
            'description': repo_info.get('description', 'No description provided.'),
            'overview': repo_info.get('description', 'Add a detailed overview of your project here.'),
            'features': '- Feature 1: Add your features here\n- Feature 2: Describe key capabilities\n- Feature 3: Highlight unique aspects',
            'install_instructions': '```bash\n# Add installation commands here\n```',
            'usage_instructions': '```bash\n# Add usage examples here\n```',
            'tech_stack': tech_stack,
            'created_date': created_date,
            'updated_date': updated_date,
            'stars': repo_info.get('stargazers_count', 0),
            'forks': repo_info.get('forks_count', 0),
            'open_issues': repo_info.get('open_issues_count', 0),
            'license': license_name,
            'license_info': license_info,
            'primary_language': primary_language,
            'repo_url': repo_info.get('html_url', ''),
            'homepage_link': homepage_link,
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _format_tech_stack(self, languages: Dict[str, int]) -> str:
        """Format languages into a readable tech stack"""
        if not languages:
            return "- Language information not available"
        
        total = sum(languages.values())
        stack_lines = []
        
        for lang, bytes_count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            percentage = (bytes_count / total) * 100
            stack_lines.append(f"- **{lang}:** {percentage:.1f}%")
        
        return '\n'.join(stack_lines)
    
    def _format_date(self, date_str: str) -> str:
        """Format ISO date string to readable format"""
        if not date_str:
            return "Unknown"
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%B %d, %Y')
        except:
            return date_str
    
    def generate(self, repo_identifier: str, output_path: Optional[Path] = None) -> str:
        """Generate README for specified repository"""
        
        # Parse repository identifier
        owner, repo = self.parse_repo_url(repo_identifier)
        
        print(f"Fetching repository information for {owner}/{repo}...")
        
        # Fetch data from GitHub
        repo_info = self.api_client.get_repo_info(owner, repo)
        languages = self.api_client.get_languages(owner, repo)
        
        print(f"Repository found: {repo_info.get('full_name')}")
        print(f"Description: {repo_info.get('description', 'No description')}")
        
        # Extract and format data
        data = self.extract_data(repo_info, languages)
        
        # Render template
        readme_content = self.template_engine.render(data)
        
        # Save to file
        if output_path is None:
            output_path = Path.cwd() / f"{repo}_README.md"
        
        output_path.write_text(readme_content, encoding='utf-8')
        
        print(f"\n✓ README generated successfully!")
        print(f"✓ Saved to: {output_path.absolute()}")
        
        return str(output_path.absolute())


def main():
    parser = argparse.ArgumentParser(
        description='Generate professional README.md files for GitHub repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate README for a repository
  python readme_agent.py octocat/Hello-World

  # Use custom template
  python readme_agent.py microsoft/vscode -t my_template.md

  # Specify output location
  python readme_agent.py torvalds/linux -o ~/Documents/linux_README.md

  # Use GitHub token from environment
  set GITHUB_TOKEN=your_token_here
  python readme_agent.py owner/repo

Note: Set GITHUB_TOKEN environment variable to avoid API rate limits.
        """
    )
    
    parser.add_argument('repository',
                       help='GitHub repository (owner/repo or full URL)')
    
    parser.add_argument('-o', '--output',
                       type=Path,
                       help='Output file path (default: ./{repo}_README.md)')
    
    parser.add_argument('-t', '--template',
                       type=Path,
                       help='Custom template file path')
    
    parser.add_argument('--token',
                       help='GitHub personal access token (or set GITHUB_TOKEN env var)')
    
    parser.add_argument('--create-template',
                       action='store_true',
                       help='Create default template file and exit')
    
    args = parser.parse_args()
    
    # Create default template if requested
    if args.create_template:
        template_path = Path('readme_template.md')
        template_path.write_text(TemplateEngine.get_default_template(), encoding='utf-8')
        print(f"✓ Default template created: {template_path.absolute()}")
        print("  Edit this file to customize your README template.")
        return 0
    
    try:
        # Create generator
        generator = ReadmeGenerator(
            github_token=args.token,
            template_path=args.template
        )
        
        # Generate README
        generator.generate(args.repository, args.output)
        
        return 0
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
