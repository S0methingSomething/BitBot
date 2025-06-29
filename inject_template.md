<!-- TUTORIAL-START -->
TUTORIAL: How to Customize This Injection Template
----------------------------------------------------
This file's content will be injected at the TOP of an outdated post.
The bot will replace the placeholders below with details about the latest available release.
This entire tutorial block will be removed by the script before posting.

Available Placeholders:
| Placeholder               | Description                                           |
| ------------------------- | ----------------------------------------------------- |
| {{latest_post_title}}     | The full title of the latest release post.            |
| {{latest_post_url}}       | The shortlink URL to the latest release post.         |
| {{latest_version}}        | The version number of the latest release (e.g., 4.2.0). |
| {{latest_download_url}}   | The direct download link for the latest asset file.   |
| {{asset_name}}            | The name of the file asset (from `config.json`).      |
| {{bot_name}}              | The name of your bot (from `config.json`).            |
| {{bot_repo}}              | The bot's repository name (from `config.json`).       |
<!-- TUTORIAL-END -->

<!-- BANNER START -->
## ⚠️ Outdated Post

A newer version of **{{asset_name}}** (v{{latest_version}}) is now available. Please refer to the latest post to download.

👉 [**Go to the latest post: {{latest_post_title}}**]({{latest_post_url}})
<!-- BANNER END -->
