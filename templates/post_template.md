<!-- TUTORIAL-START -->
TUTORIAL: How to Customize This Post Template
---------------------------------------------
This file controls the format of the Reddit post. You can edit anything outside of this comment block.
The bot replaces placeholders (like {{version}}) with data from the config file and the release process.
This entire block, including these lines, will be removed by the script before posting.

Available Placeholders:
| Placeholder                 | Description                                              |
| --------------------------- | -------------------------------------------------------- |
| {{version}}                 | The new version number, like `4.2.0`.                    |
| {{direct_download_url_bitlife}} | Direct link for BitLife MonetizationVars.                |
| {{direct_download_url_bitlife_go}} | Direct link for BitLife Go MonetizationVars.             |
| {{bot_name}}                | The name of your bot (from `config.json`).               |
| {{bot_repo}}                | Your bot's repository name, like `YourUsername/BitBot`.  |
| {{asset_name}}              | The name of the file asset, like `MonetizationVars`.     |
| {{creator_username}}        | The creator's Reddit username (from `config.json`).      |
| {{initial_status}}          | The full, formatted initial status line for the post.    |
| {{update_timestamp}}        | Timestamp of when post was last updated.                 |
| {{app_count}}               | Number of apps currently available.                      |
<!-- TUTORIAL-END -->

## **[⬇️ Download All Releases Here]({{download_portal_url}})**

> ⚠️ **Important:** Ensure the downloaded file is named exactly `{{asset_name}}` before installation.

---

## 📖 How to Use
**[BitGuides - Unlocking IAP](https://s0methingsomething.github.io/BitGuides/modding/monetizationvars/unlocking-iap/)**

### ❓ FAQ
**Q: The time machine/age down button is greyed out**  
A: To fix this, make a new life then surrender it.

**Q: Can I get an APK instead?**  
A: I'm not gonna recommend one since I don't use any and I don't have a source I trust.

**Q: Is there a guide for iOS/PC (emulation)?**  
A: I don't really know nor am I planning to make one since I don't emulate or use an iOS device.

---

## 📋 Latest Update ({{update_timestamp}})
{{changelog}}

---

## 📦 Currently Available ({{app_count}} apps)
{{available_list}}

---

## 🔧 Project Information
**Creator:** u/{{creator_username}}
**Repository:** {{bot_repo}}

## 🛠️ Related Projects
**BitEdit** - [Modify MonetizationVars on the web in a human readable format JSON](https://s0methingsomething.github.io/BitEdit/)
