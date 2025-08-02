# Guide: Templates & Customization

This guide explains how to customize the bot's output, such as the Reddit posts and the optional landing page.

---

## Reddit Post Templates

You can change the content of the Reddit posts by editing the Markdown template files in the `templates/` directory.

-   `post_template.md`: The main template for all new release announcements.
-   `inject_template.md`: The template for the banner that is injected into outdated posts.

### Placeholders for `post_template.md`

| Placeholder             | Description                                                                 |
| ----------------------- | --------------------------------------------------------------------------- |
| `{{changelog}}`         | **(Primary)** A generated list of all updated apps and their versions.      |
| `{{download_portal_url}}` | **(Landing Page Mode Only)** The URL to the generated GitHub Pages site.    |
| `{{bot_name}}`            | The name of your bot (from `config.toml`).                                  |
| `{{bot_repo}}`            | Your bot's repository name, like `YourUsername/BitBot`.                     |
| `{{asset_name}}`          | The name of the file asset, like `MonetizationVars`.                        |
| `{{creator_username}}`    | The creator's Reddit username (from `config.toml`).                         |
| `{{initial_status}}`      | The full, formatted initial status line for the post.                       |

---

## Landing Page Template

The bot supports a powerful hybrid system for the download landing page. You can either use the convenient default template or provide your own for full control over the HTML, CSS, and JavaScript.

### How it Works

1.  **Default Mode:** By default, the bot uses a clean, built-in template (`templates/default_landing_page.html`) to generate the `index.html` file. No action is needed to use this.

2.  **Custom Mode:** To use your own design:
    a. Create a new HTML file (e.g., `my_landing_page.html`) inside the `templates/` directory.
    b. In `config.toml`, uncomment and set the `custom_landing_template` key to point to your new file:
       ```toml
       [reddit]
       # ...
       custom_landing_template = "templates/my_landing_page.html"
       ```
    c. The bot will now use your template instead of the default. An example can be found at `templates/custom_landing_page.example.html`.

### Landing Page Placeholders

When creating your custom HTML template, you can use the following placeholders.

#### Global Placeholders
These appear once per page.

| Placeholder    | Description                                      |
| -------------- | ------------------------------------------------ |
| `{{bot_repo}}` | The name of the bot's repository from `config.toml`. |

#### Loop Block Placeholders
This is the core of the templating engine. The script will find this block and repeat it for every app that was updated.

```html
<!-- BEGIN-RELEASE-LOOP -->
<!-- The HTML for a single item goes here. -->
<!-- END-RELEASE-LOOP -->
```

Inside the loop block, you can use these placeholders:

| Placeholder            | Description                               |
| ---------------------- | ----------------------------------------- |
| `{{app_display_name}}` | The user-friendly name of the application. |
| `{{app_version}}`      | The version number for this specific app. |
| `{{app_download_url}}` | The direct download URL for this app's asset. |