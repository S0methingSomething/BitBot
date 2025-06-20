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

## 🚀 New Release v{{version}}

**Direct Download:**  
[📦 Download `{{asset_name}}`](https://github.com/{{bot_repo}}/releases/latest)

*The file is already patched to unlock all available IAP'S.  
Make sure the downloaded file is named **exactly** `{{asset_name}}` before using it.*

---

### About This Bot
Created and maintained by **u/{{creator_username}}**.  
Source code, changelogs, and issues are all on GitHub:  
<https://github.com/{{bot_repo}}>

---

### Community Feedback
**Current status:** {{initial_status}}  
Leave a comment below if something isn’t working, or if you have suggestions!

