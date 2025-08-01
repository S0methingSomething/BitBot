import os
import sys
import json
import re

def _render_template(template_content: str, data: dict, config: dict) -> str:
    """Renders a template with nested loops and placeholders."""
    
    # --- Outer Loop: App Loop ---
    app_loop_pattern = re.compile(r'<!-- BEGIN-APP-LOOP -->(.*?)<!-- END-APP-LOOP -->', re.DOTALL)
    app_template_match = app_loop_pattern.search(template_content)
    
    if not app_template_match:
        # Fallback to old system if new loops aren't used
        return _render_legacy_template(template_content, data, config)

    app_template = app_template_match.group(1)
    all_app_html = []

    # Sort apps by display name for consistent ordering
    sorted_app_ids = sorted(data.keys(), key=lambda k: data[k]['display_name'])

    for app_id in sorted_app_ids:
        app_data = data[app_id]
        app_html = app_template
        
        # --- Placeholders for the current app ---
        app_html = app_html.replace('{{app.display_name}}', app_data['display_name'])
        # Add more app-level placeholders here if needed in the future

        # --- Inner Loop: Release Loop ---
        release_loop_pattern = re.compile(r'<!-- BEGIN-RELEASE-LOOP -->(.*?)<!-- END-RELEASE-LOOP -->', re.DOTALL)
        release_template_match = release_loop_pattern.search(app_html)
        
        if release_template_match:
            release_template = release_template_match.group(1)
            all_releases_html = []

            for release in app_data.get('releases', []):
                release_html = release_template
                # --- Placeholders for the current release ---
                release_html = release_html.replace('{{release.version}}', release.get('version', 'N/A'))
                release_html = release_html.replace('{{release.download_url}}', release.get('download_url', '#'))
                release_html = release_html.replace('{{release.published_at}}', release.get('published_at', ''))
                release_html = release_html.replace('{{release.release_notes}}', release.get('release_notes', ''))
                release_html = release_html.replace('{{release.release_url}}', release.get('release_url', '#'))
                all_releases_html.append(release_html)
            
            # Replace the release loop block with the generated HTML
            app_html = release_loop_pattern.sub(''.join(all_releases_html), app_html)

        all_app_html.append(app_html)

    # Replace the main app loop block with the generated HTML
    final_html = app_loop_pattern.sub(''.join(all_app_html), template_content)

    # --- Global Placeholders ---
    final_html = final_html.replace('{{bot_repo}}', config['github']['botRepo'])
    
    return final_html

def _render_legacy_template(template_content: str, data: dict, config: dict) -> str:
    """Fallback renderer for the old single-loop template system."""
    print("::warning::Using legacy template rendering. Consider updating your template to use the new APP-LOOP/RELEASE-LOOP structure.")
    loop_pattern = re.compile(r'<!-- BEGIN-RELEASE-LOOP -->(.*?)<!-- END-RELEASE-LOOP -->', re.DOTALL)
    match = loop_pattern.search(template_content)
    if not match:
        return template_content

    template_part = match.group(1)
    all_html = []
    
    # Flatten the new data structure to work with the old template
    flat_data = []
    for app_id, app_info in data.items():
        if app_info.get('releases'):
            latest_release = app_info['releases'][0]
            flat_data.append({
                "display_name": app_info['display_name'],
                "version": latest_release['version'],
                "download_url": latest_release['download_url']
            })

    sorted_data = sorted(flat_data, key=lambda x: x['display_name'])

    for release in sorted_data:
        html_part = template_part
        html_part = html_part.replace('{{app_display_name}}', release['display_name'])
        html_part = html_part.replace('{{app_version}}', release['version'])
        html_part = html_part.replace('{{app_download_url}}', release['download_url'])
        all_html.append(html_part)

    final_html = loop_pattern.sub(''.join(all_html), template_content)
    final_html = final_html.replace('{{bot_repo}}', config['github']['botRepo'])
    return final_html


def main():
    config = load_config()
    
    if not os.path.exists(paths.RELEASES_JSON_FILE):
        print(f"::error::Release data file not found at '{paths.RELEASES_JSON_FILE}'. Cannot generate page.", file=sys.stderr)
        sys.exit(1)
        
    with open(paths.RELEASES_JSON_FILE, 'r') as f:
        releases_data = json.load(f)

    # Determine which template to use
    custom_template_name = config['reddit']['templates'].get('custom_landing')
    template_path = paths.get_template_path(custom_template_name) if custom_template_name and os.path.exists(paths.get_template_path(custom_template_name)) else paths.DEFAULT_LANDING_PAGE
    
    print(f"Using template: {template_path}")
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Render the final HTML
    final_html = _render_template(template_content, releases_data, config)

    # Save the final page
    if not os.path.exists(paths.DIST_DIR):
        os.makedirs(paths.DIST_DIR)
    
    output_path = os.path.join(paths.DIST_DIR, 'index.html')
    with open(output_path, 'w') as f:
        f.write(final_html)
        
    print(f"Successfully generated landing page at: {output_path}")

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import paths
    from helpers import load_config
    main()