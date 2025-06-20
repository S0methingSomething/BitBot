<!-- TUTORIAL-START -->
TUTORIAL: How to Customize This Post Template
---------------------------------------------
This file controls the format of the Reddit post. You can edit anything outside of this comment block.
The bot replaces placeholders (like {{version}}) with data from the config file and the release process.
This entire block, including these lines, will be removed by the script before posting.

Available Placeholders:
| Placeholder           | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| {{version}}           | The new version number, like `4.2.0`.                          |
| {{direct_download_url}} | The direct link to download the patched asset file.            |
| {{bot_name}}          | The name of your bot (from `config.json`).                     |
| {{bot_repo}}          | Your bot's repository name, like `YourUsername/BitBot`.        |
| {{asset_name}}        | The name of the file asset, like `MonetizationVars`.           |
| {{creator_username}}  | The creator's Reddit username (from `config.json`).            |
| {{initial_status}}    | The default status for a new post ("Not enough feedback...").  |
<!-- TUTORIAL-END -->

This is an automated post by [{{bot_name}}](https://github.com/{{bot_repo}}).

---

### **Download Link**

You can download the pre-patched file from the official release page:

**[Download {{asset_name}} (Patched for v{{version}})](https://github.com/{{bot_repo}}/releases/latest)**

This file has been pre-patched to set all available boolean-based features to `true`. **Please ensure the downloaded file is named exactly `{{asset_name}}` before use.**

---

This bot was created by u/{{creator_username}}.

**Current Status (based on comments):** {{initial_status}}
