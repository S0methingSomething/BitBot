import os
import sys
import re
import json
from helpers import load_config
import paths

def main():
    """
    Generates a static HTML page from release data and a template.
    """
    config = load_config()

    # Determine which template to use
    custom_template_name = config['reddit']['templates'].get('custom_landing')
    if custom_template_name and os.path.exists(paths.get_template_path(custom_template_name)):
        template_path = paths.get_template_path(custom_template_name)
        print(f"Using custom landing page template: {template_path}")
    else:
        template_path = paths.DEFAULT_LANDING_PAGE
        print(f"Custom template not found or specified. Using default: {template_path}")
        if not os.path.exists(template_path):
            print(f"::error::Default template not found at {template_path}. Exiting.", file=sys.stderr)
            sys.exit(1)

    # Load data and template
    with open(paths.RELEASES_JSON_FILE, 'r') as f:
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
    os.makedirs(os.path.dirname(paths.LANDING_PAGE_OUTPUT), exist_ok=True)
    with open(paths.LANDING_PAGE_OUTPUT, 'w') as f:
        f.write(final_html)

    print(f"Successfully generated landing page at: {paths.LANDING_PAGE_OUTPUT}")

if __name__ == "__main__":
    main()
