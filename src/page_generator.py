import os
import sys
import json
import re

def _render_template(template_content: str, data: dict, config: dict) -> str:
    """
    Renders a template with a clean data structure, supporting nested loops and
    conditional blocks.
    """
    
    app_loop_pattern = re.compile(r'<!-- BEGIN-APP-LOOP -->(.*?)<!-- END-APP-LOOP -->', re.DOTALL)
    app_template_match = app_loop_pattern.search(template_content)
    
    if not app_template_match:
        return "<!-- APP-LOOP not found in template -->"

    app_template = app_template_match.group(1)
    all_app_html = []

    sorted_app_ids = sorted(data.keys(), key=lambda k: data[k]['display_name'])

    for app_id in sorted_app_ids:
        app_data = data[app_id]
        app_html = app_template
        
        # --- Conditional Block: Check for latest_release ---
        conditional_pattern = re.compile(r'<!-- IF RELEASES EXIST -->(.*?)<!-- ELSE -->(.*?)<!-- END IF -->', re.DOTALL)
        conditional_match = conditional_pattern.search(app_html)
        
        if conditional_match:
            if_template = conditional_match.group(1)
            else_template = conditional_match.group(2)
            
            if app_data.get('latest_release'):
                app_html = conditional_pattern.sub(if_template, app_html)
            else:
                app_html = conditional_pattern.sub(else_template, app_html)

        # --- App & Latest Release Placeholders ---
        app_html = app_html.replace('{{app.display_name}}', app_data['display_name'])
        if app_data.get('latest_release'):
            latest = app_data['latest_release']
            app_html = app_html.replace('{{app.latest_release.version}}', latest.get('version', 'N/A'))
            app_html = app_html.replace('{{app.latest_release.published_at}}', latest.get('published_at', ''))
            app_html = app_html.replace('{{app.latest_release.download_url}}', latest.get('download_url', '#'))

        # --- Inner Loop: Previous Releases ---
        release_loop_pattern = re.compile(r'<!-- BEGIN-RELEASE-LOOP -->(.*?)<!-- END-RELEASE-LOOP -->', re.DOTALL)
        release_template_match = release_loop_pattern.search(app_html)
        
        if release_template_match:
            release_template = release_template_match.group(1)
            all_releases_html = []
            
            for release in app_data.get('previous_releases', []):
                release_html = release_template
                release_html = release_html.replace('{{release.version}}', release.get('version', 'N/A'))
                release_html = release_html.replace('{{release.download_url}}', release.get('download_url', '#'))
                release_html = release_html.replace('{{release.published_at}}', release.get('published_at', ''))
                all_releases_html.append(release_html)
            
            app_html = release_loop_pattern.sub(''.join(all_releases_html), app_html)

        all_app_html.append(app_html)

    final_html = app_loop_pattern.sub(''.join(all_app_html), template_content)
    final_html = final_html.replace('{{bot_repo}}', config['github']['botRepo'])
    
    return final_html

def main():
    config = load_config()
    if not os.path.exists(paths.RELEASES_JSON_FILE):
        print(f"::error::Release data file not found at '{paths.RELEASES_JSON_FILE}'. Cannot generate page.", file=sys.stderr)
        sys.exit(1)
    with open(paths.RELEASES_JSON_FILE, 'r') as f:
        releases_data = json.load(f)
    custom_template_name = config['reddit']['templates'].get('custom_landing')
    template_path = paths.get_template_path(custom_template_name) if custom_template_name and os.path.exists(paths.get_template_path(custom_template_name)) else paths.DEFAULT_LANDING_PAGE
    print(f"Using template: {template_path}")
    with open(template_path, 'r') as f:
        template_content = f.read()
    final_html = _render_template(template_content, releases_data, config)
    os.makedirs(paths.DIST_DIR, exist_ok=True)
    output_path = os.path.join(paths.DIST_DIR, 'index.html')
    with open(output_path, 'w') as f:
        f.write(final_html)
    print(f"Successfully generated landing page at: {output_path}")

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import paths
    from helpers import load_config
    main()