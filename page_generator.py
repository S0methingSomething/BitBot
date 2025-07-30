import json
import os

from helpers import load_config

def main():
    """
    Generates a static HTML page from release data and a template.
    """
    config = load_config()
    releases_path = 'dist/releases.json'
    template_path = 'page_template.html'
    output_path = 'dist/index.html'

    bot_repo = config.get('github', {}).get('botRepo', '')

    with open(releases_path, 'r') as f:
        releases_data = json.load(f)
    
    with open(template_path, 'r') as f:
        template_html = f.read()

    release_html_blocks = []
    for app_id, release_info in releases_data.items():
        display_name = release_info['display_name']
        version = release_info['version']
        url = release_info['url']
        
        block = f"""
        <div class="release-group">
            <h2>{display_name} v{version}</h2>
            <a href="{url}" class="download-button">Download Asset</a>
        </div>
        """
        release_html_blocks.append(block)

    final_html = template_html.replace('<!-- Release groups will be injected here by the script -->', "\n".join(release_html_blocks))
    final_html = final_html.replace('{{bot_repo}}', bot_repo)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(final_html)

    print(f"Successfully generated landing page at: {output_path}")

if __name__ == "__main__":
    main()
