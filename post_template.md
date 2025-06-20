<!--
TUTORIAL: How to Customize This Post Template
---------------------------------------------
This file controls the format of the Reddit post. You can edit anything outside of this comment block.
The bot replaces placeholders (like {{version}}) with data from the config file and the release process.
This comment block will NOT appear on the final Reddit post.

Available Placeholders:
| Placeholder          | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| {{version}}          | The new version number, like `4.2.0`.                          |
| {{bot_name}}         | The name of your bot (from `config.json`).                     |
| {{bot_repo}}         | Your bot's repository name, like `YourUsername/BitBot`.        |
| {{asset_name}}       | The name of the file asset, like `MonetizationVars`.           |
| {{creator_username}} | The creator's Reddit username (from `config.json`).            |
| {{initial_status}}   | The default status for a new post ("Not enough feedback...").  |
-->
This is an automated post by [{{bot_name}}](https://github.com/{{bot_repo}}).

---

### **Download Link**

You can download the pre-patched file from the official release page:

**[Download {{asset_name}} (Patched for v{{version}})](https://github.com/{{bot_repo}}/releases/latest)**

> ### **How to Use This File**
>
> 1.  **Download:** Get the `{{asset_name}}` file from the link above.
> 2.  **Navigate:** On your device, go to your Files app.
> 3.  **Locate BitLife Folder:** Find the BitLife folder. For iOS, this is typically under "On My iPhone" > "BitLife".
> 4.  **Replace:** Move the file you downloaded into the BitLife folder, replacing the old one.
> 5.  **Check Name:** Ensure the file is named exactly `{{asset_name}}` with no extra numbers or extensions (e.g., not `{{asset_name}} (1)` or `{{asset_name}}.txt`).
>
> This file has been pre-patched to set all available boolean-based features (like God Mode, Job Packs, etc.) to `true`.

---

This bot was created by u/{{creator_username}}.

**Current Status (based on comments):** {{initial_status}}
