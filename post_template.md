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

*Automated post by [{{bot_name}}](https://github.com/{{bot_repo}})*

---

## 📥 **Quick Download**

**[⬇️ Download {{asset_name}} v{{version}} (Pre-Patched)]({{direct_download_url}})**

> **Important:** Ensure the downloaded file is renamed to exactly `{{asset_name}}` before use.

---

## ✨ **What's Included**

This release contains a pre-patched version of {{asset_name}} with:
- ✅ All boolean-based features enabled (`true`)
- 🔧 Ready-to-use configuration
- 📦 Compatible with the latest version

## 🚀 **Installation**

1. Download the file using the link above
2. Rename it to `{{asset_name}}` (exact match required)
3. Replace your existing file
4. You're ready to go!

---

## 📊 **Community Feedback**

**Current Status:** {{initial_status}}

*Found this helpful? Let us know in the comments below!*

---

<sub>Created by u/{{creator_username}} | [View Source](https://github.com/{{bot_repo}}) | [Report Issues](https://github.com/{{bot_repo}}/issues)</sub>
