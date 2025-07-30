import os
import sys
import re
import json
from helpers import load_config

def main():
    """
    Generates a static HTML page from release data and a template.
    It uses a custom template if specified in the config, otherwise falls back
    to a default template. It processes a loop block within the template.
    """
    config = load_config()
    releases_path = '../dist/releases.json'
    output_path = '../dist/index.html'

    # Determine which template to use
    template_path = config['reddit'].get('custom_landing_template')
    if template_path and os.path.exists(template_path):
        print(f"Using custom landing page template: {template_path}")
    else:
        template_path = 'templates/default_landing_page.html'
        print(f"Custom template not found or specified. Using default: {template_path}")
        if not os.path.exists(template_path):
            print(f"::error::Default template not found at {template_path}. Exiting.", file=sys.stderr)
            sys.exit(1)

    # Load data and template
    with open(releases_path, 'r') as f:
        releases_data = json.load(f)
    
    with open(template_path, 'r') as f:
        template_html = f.read()

    # Find the release loop block
    loop_pattern = re.compile(r"<!-- BEGIN-RELEASE-LOOP -->(.*?)<!-- END-RELEASE-LOOP -->", re.DOTALL)
    match = loop_pattern.search(template_html)
    
    if not match:
        print("::error::Could not find '<!-- BEGIN-RELEASE-LOOP -->' and '<!-- END-RELEASE-LOOP -->' block in the template.", file=sys.stderr)
        sys.exit(1)
        
    item_template = match.group(1).strip()
    
    # Generate HTML for each release
    all_releases_html = []
    for app_id, release_info in releases_data.items():
        item_html = item_template.replace('{{app_display_name}}', release_info['display_name'])
        item_html = item_html.replace('{{app_version}}', release_info['version'])
        item_html = item_html.replace('{{app_download_url}}', release_info['url'])
        all_releases_html.append(item_html)

    # Replace the entire loop block with the generated content
    final_html = loop_pattern.sub("\n".join(all_releases_html), template_html)
    
    # Replace other global placeholders
    bot_repo = config.get('github', {}).get('botRepo', '')
    final_html = final_html.replace('{{bot_repo}}', bot_repo)

    # Save the final HTML
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(final_html)

    print(f"Successfully generated landing page at: {output_path}")

if __name__ == "__main__":
    main()
