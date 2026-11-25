# Threads API

[English](#english) · [中文](#中文)

## English

This repo reads public Threads data with Python or curl. You can search posts by keyword, read a single post and its replies, and look up an account's profile and posts. You need one EveryInfra API key. You do not need a Threads account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 5 capabilities cost $0.56 to $0.78 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra Threads API has 25 capabilities, all listed on the platform page: <https://everyinfra.com/en/threads-api?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### Quick start

```bash
git clone https://github.com/everyinfra/threads-api.git
cd threads-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "camping gear" --out posts.csv
python main.py post "<post url>" --out post.json
python main.py replies "<post url>" --out replies.csv
python main.py user <username>
python main.py posts <username> --out user_posts.csv
```

- For `post` and `replies`, pass the `url` from a `search` result, for example https://www.threads.com/@<username>/post/<code>.
- For `user` and `posts`, pass the `author_username` from a `search` result, with or without the @. Do not pass the full profile link.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- `--pages N` follows `next_page_token` for N pages. Each page counts as one call.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"threads","action":"search","params":{"keyword":"camping gear"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `post_detail`, `comments`, `profile`, and `user_posts` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $0.78 |
| `post_detail` | $0.56 |
| `comments` | $0.56 |
| `profile` | $0.56 |
| `user_posts` | $0.56 |

- Billing is per call, about $0.00056 to $0.00078 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- Each page fetched with `--pages` counts as one call.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>
- Prices for the other 20 Threads capabilities are on the platform page: <https://everyinfra.com/en/threads-api?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### Fields

These are the fields that the 5 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `code` | Post code: the segment of the post link that comes after /post/. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `author_name` | Author's display name. |
| `author_id` | Author's unique ID on the platform. |
| `author_avatar_url` | Author avatar URL; signed link that expires. |
| `author_is_verified` | Whether the author's account has a verified badge. |
| `author_is_private` | Whether the author's account is private. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `quote_count` | Quotes: how many times others have quoted this post in their own posts. null means not disclosed, not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `media_type` | Post type: text (text only), image (one image), video (one video) or carousel (several images, or images and videos mixed). |
| `image_count` | Number of images. |
| `video_count` | Number of videos. |
| `topic` | Internal name of the topic the post is attached to, e.g. bakingthreads; the display name is in topic_name. |
| `topic_id` | ID of the topic the post is attached to. |
| `topic_name` | Display name of the topic, e.g. Baking Threads. |
| `topic_is_community` | Whether the topic is a community. |
| `language` | Content language code (for example zh, en) as judged by the platform; it can be wrong. |
| `is_edited` | Whether the post has been edited. |
| `is_reply` | Whether this post is a reply. |
| `is_pinned` | Whether the author pinned the post to their profile. |
| `is_spoiler` | Whether the post is marked with a spoiler overlay. |
| `reply_control` | Who can reply to this post, e.g. everyone. |
| `counts_hidden` | Whether the author hid the like and share counts; like_count is null when hidden. |
| `thread_id` | ID of the author's thread, the run of posts published in a row; posts in the same thread share this value. |
| `thread_length` | Number of posts in the author's thread; 1 when the post is not part of a thread. |
| `thread_position` | Position of this post within the thread. |
| `is_federated` | Whether the post is synced to the fediverse. |
| `is_paid_partnership` | Whether the post is labeled as a paid partnership. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `media_url` | URL of the first attachment; signed link that expires. |
| `video_duration_seconds` | Duration of the first video, in seconds; per-video durations are in duration_seconds on each media entry. |
| `hashtags` | Hashtags in the text, in order of appearance; absent when there are none. |
| `video_urls` | URLs of all videos; signed links that expire. |
| `media` | List of attachments, one entry each; absent when there are none. |
| `reply_to_username` | Username of the person this post replies to; absent when the post is not a reply. |
| `root_post_author_username` | Username of the author of the post at the top of this conversation. |
| `is_liked_by_author` | Replies only: whether the main post's author liked this reply. |
| `ai_label` | How the post is labeled as AI-generated, e.g. SELF_DISCLOSURE_FLOW (labeled by the author); absent when there is none. |
| `links` | Links in the text and links attached to the post. |
| `image_urls` | Array of image links in the platform's display order; absent when there are no images. |
| `share_count` | Shares. null means not disclosed, not 0. |

All parameters and fields: <https://everyinfra.com/en/threads-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

#### `post_detail` (post details)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `code` | Post code: the segment of the post link that comes after /post/. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `author_name` | Author's display name. |
| `author_id` | Author's unique ID on the platform. |
| `author_avatar_url` | Author avatar URL; signed link that expires. |
| `author_is_verified` | Whether the author's account has a verified badge. |
| `author_is_private` | Whether the author's account is private. |
| `author_follower_count` | Author's follower count. null means not disclosed. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `quote_count` | Quotes: how many times others have quoted this post in their own posts. null means not disclosed, not 0. |
| `share_count` | Shares. null means not disclosed, not 0. |
| `view_count` | Views or plays. null means not disclosed, not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `media_type` | Post type: text (text only), image (one image), video (one video) or carousel (several images, or images and videos mixed). |
| `image_count` | Number of images. |
| `video_count` | Number of videos. |
| `language` | Content language code (for example zh, en) as judged by the platform; it can be wrong. |
| `is_edited` | Whether the post has been edited. |
| `is_reply` | Whether this post is a reply. |
| `is_pinned` | Whether the author pinned the post to their profile. |
| `is_spoiler` | Whether the post is marked with a spoiler overlay. |
| `reply_control` | Who can reply to this post, e.g. everyone. |
| `counts_hidden` | Whether the author hid the like and share counts; like_count is null when hidden. |
| `thread_id` | ID of the author's thread, the run of posts published in a row; posts in the same thread share this value. |
| `thread_length` | Number of posts in the author's thread; 1 when the post is not part of a thread. |
| `thread_position` | Position of this post within the thread. |
| `is_federated` | Whether the post is synced to the fediverse. |
| `is_paid_partnership` | Whether the post is labeled as a paid partnership. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/threads-api/post_detail?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

#### `comments` (comments)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `author_name` | Author's display name. |
| `author_id` | Author's unique ID on the platform. |
| `author_avatar_url` | Author avatar URL; signed link that expires. |
| `author_is_verified` | Whether the author's account has a verified badge. |
| `author_is_private` | Whether the author's account is private. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `quote_count` | Quotes: how many times others have quoted this post in their own posts. null means not disclosed, not 0. |
| `share_count` | Shares. null means not disclosed, not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `media_type` | Post type: text (text only), image (one image), video (one video) or carousel (several images, or images and videos mixed). |
| `image_count` | Number of images. |
| `video_count` | Number of videos. |
| `language` | Content language code (for example zh, en) as judged by the platform; it can be wrong. |
| `is_edited` | Whether the post has been edited. |
| `is_reply` | Whether this post is a reply. |
| `reply_to_username` | Username of the person this post replies to; absent when the post is not a reply. |
| `root_post_author_username` | Username of the author of the post at the top of this conversation. |
| `reply_level` | Reply depth: 1 is a direct reply to the main post, 2 is a reply to a reply, and so on. |
| `is_pinned` | Whether the author pinned the post to their profile. |
| `is_spoiler` | Whether the post is marked with a spoiler overlay. |
| `reply_control` | Who can reply to this post, e.g. everyone. |
| `counts_hidden` | Whether the author hid the like and share counts; like_count is null when hidden. |
| `is_federated` | Whether the post is synced to the fediverse. |
| `is_paid_partnership` | Whether the post is labeled as a paid partnership. |
| `is_liked_by_author` | Replies only: whether the main post's author liked this reply. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `post_id` | Numeric ID of this reply (id is its post code). |
| `reply_to_id` | Post code of the post being replied to. |
| `reply_to_url` | Link to the post being replied to. |
| `reply_to` | Username of the person being replied to. |

All parameters and fields: <https://everyinfra.com/en/threads-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

#### `profile` (profile or object details)

| Field | Meaning |
|---|---|
| `user_id` | User's unique ID on the platform. |
| `username` | Username (@handle). |
| `display_name` | Display name; can differ from username. |
| `bio` | Profile bio written by the account; may contain line breaks and emoji. |
| `follower_count` | Followers. null means not disclosed, not 0. |
| `is_verified` | Whether the platform verified the account. null means it cannot be determined. |
| `is_private` | Whether the account is private. |
| `url` | Link to the record on the platform. |
| `avatar_url` | Avatar image link. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `external_url` | First link in the bio; absent when there is none. |
| `avatar_hd_url` | High-resolution avatar URL. |
| `public_view_count` | Public views over the last 30 days, the number Threads shows publicly on the profile; the start and end dates of the period are in public_view_count_start and public_view_count_end. |
| `public_view_count_start` | Start date of the period public_view_count covers, YYYY-MM-DD. |
| `public_view_count_end` | End date of the period public_view_count covers, YYYY-MM-DD. |
| `bio_links` | All links attached in the bio section. |
| `topics` | Topics attached to the account's profile page. |
| `bio_links_detail` | All links attached in the bio section, each with url, title (link title; only some have it) and is_verified (whether ownership has been verified). |
| `topics_detail` | Topics attached to the profile, each with id, name, display_name and is_community. |

All parameters and fields: <https://everyinfra.com/en/threads-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

#### `user_posts` (user content)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `code` | Post code: the segment of the post link that comes after /post/. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `author_name` | Author's display name. |
| `author_id` | Author's unique ID on the platform. |
| `author_avatar_url` | Author avatar URL; signed link that expires. |
| `author_is_verified` | Whether the author's account has a verified badge. |
| `author_is_private` | Whether the author's account is private. |
| `author_follower_count` | Author's follower count. null means not disclosed. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `quote_count` | Quotes: how many times others have quoted this post in their own posts. null means not disclosed, not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `media_type` | Post type: text (text only), image (one image), video (one video) or carousel (several images, or images and videos mixed). |
| `image_count` | Number of images. |
| `video_count` | Number of videos. |
| `topic` | Internal name of the topic the post is attached to, e.g. bakingthreads; the display name is in topic_name. |
| `topic_id` | ID of the topic the post is attached to. |
| `topic_name` | Display name of the topic, e.g. Baking Threads. |
| `topic_is_community` | Whether the topic is a community. |
| `language` | Content language code (for example zh, en) as judged by the platform; it can be wrong. |
| `is_edited` | Whether the post has been edited. |
| `is_reply` | Whether this post is a reply. |
| `is_pinned` | Whether the author pinned the post to their profile. |
| `is_spoiler` | Whether the post is marked with a spoiler overlay. |
| `reply_control` | Who can reply to this post, e.g. everyone. |
| `counts_hidden` | Whether the author hid the like and share counts; like_count is null when hidden. |
| `thread_id` | ID of the author's thread, the run of posts published in a row; posts in the same thread share this value. |
| `thread_length` | Number of posts in the author's thread; 1 when the post is not part of a thread. |
| `thread_position` | Position of this post within the thread. |
| `is_federated` | Whether the post is synced to the fediverse. |
| `is_paid_partnership` | Whether the post is labeled as a paid partnership. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/threads-api/user_posts?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### FAQ

**Do I need a Threads account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.56 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. When `urls` holds several links, each link counts as one call. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

**Can I connect the Threads API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>. An agent can then search Threads content, read comments, and look up accounts by itself.

**What legal points apply when I use Threads data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Threads data can I get?**

The EveryInfra Threads API has 25 capabilities:

- keyword search
- profile or object details
- user content
- post details
- comments
- profile discovery
- followers
- replies tab
- media posts
- user reposts
- news feed
- thread
- topic posts
- posts at a location
- trend posts
- follower list
- following list
- suggested profiles
- post activity
- trending
- communities
- engagement statistics
- search suggestions
- profiles in bulk
- posts in bulk

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/threads-api?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### Tested

Before release, we ran the 5 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "camping gear" --out posts.csv` | 2026-11-25 12:34 | 10 | $0.000778 |
| `python main.py post "<post url>" --out post.json` | 2026-11-25 12:34 | 1 | $0.000556 |
| `python main.py replies "<post url>" --out replies.csv` | 2026-11-25 12:35 | 10 | $0.000556 |
| `python main.py user <username>` | 2026-11-25 12:35 | 1 | $0.000556 |
| `python main.py posts <username> --out user_posts.csv` | 2026-11-25 12:35 | 10 | $0.000556 |

## 中文

本仓库用 Python 或 curl 读 Threads 公开数据：按关键词搜帖子，读单条帖子和回复，查账号资料和他发布的帖子。只需一把 EveryInfra API Key，不用 Threads 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 5 个能力每千次 $0.56 到 $0.78，失败和空结果不收费。Threads 共 25 个能力：<https://everyinfra.com/threads-api?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/threads-api.git
cd threads-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "camping gear" --out posts.csv
python main.py post "<帖子链接>" --out post.json
python main.py replies "<帖子链接>" --out replies.csv
python main.py user <username>
python main.py posts <username> --out user_posts.csv
```

- `post` 和 `replies` 传 `search` 结果里的 `url`，形如 https://www.threads.com/@<用户名>/post/<帖子短码>。
- `user` 和 `posts` 传 `search` 结果里的 `author_username`，带不带 @ 都行；不要传完整主页链接。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- `--pages N` 按 `next_page_token` 翻页，每翻一页算一次调用。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"threads","action":"search","params":{"keyword":"camping gear"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`post_detail`、`comments`、`profile`、`user_posts` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $0.78 |
| 内容详情 | `post_detail` | $0.56 |
| 评论 | `comments` | $0.56 |
| 主页或对象详情 | `profile` | $0.56 |
| 用户内容 | `user_posts` | $0.56 |

- 按调用次数计费，每次约 $0.00056 到 $0.00078；失败、空结果、参数错误和鉴权失败都不收费。
- `--pages` 翻的每一页算一次调用。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>
- Threads 其他 20 个能力的单价见平台页 <https://everyinfra.com/threads-api?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### 返回字段

下面是这 5 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `code` | 内容短码，用于拼 URL。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_is_verified` | 作者是否已认证。 |
| `author_is_private` | 作者账号是否私密。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `repost_count` | 转发数（区别于引用转发）。 |
| `quote_count` | 引用数：别人引用这条帖子发帖的次数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `media_type` | 帖子类型：text 纯文字、image 单图、video 单视频、carousel 多图，或图片和视频混合。 |
| `image_count` | 图片张数。 |
| `video_count` | 视频个数。 |
| `topic` | 帖子挂的话题的内部名，如 bakingthreads；显示名在 topic_name。 |
| `topic_id` | 帖子挂的话题的编号。 |
| `topic_name` | 话题的显示名，如 Baking Threads。 |
| `topic_is_community` | 话题是否为社区。 |
| `language` | 内容语言代码（如 zh、en），由平台判定，可能不准。 |
| `is_edited` | 帖子是否编辑过。 |
| `is_reply` | 这条帖子是否为回复。 |
| `is_pinned` | 是否被作者置顶在主页。 |
| `is_spoiler` | 是否标了剧透遮罩。 |
| `reply_control` | 谁能回复这条帖子，如 everyone。 |
| `counts_hidden` | 作者是否隐藏了点赞数和分享数；隐藏时 like_count 为 null。 |
| `thread_id` | 作者连发的这一串帖子的编号，同一串的帖子这个值相同。 |
| `thread_length` | 作者连发的这一串一共几条；不是连发时为 1。 |
| `thread_position` | 这条是连发串里的第几条。 |
| `is_federated` | 是否同步到联邦宇宙（Fediverse）。 |
| `is_paid_partnership` | 是否标注为付费合作内容。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `media_url` | 第一个附件的地址，带签名，会过期。 |
| `video_duration_seconds` | 第一个视频的时长，秒；每个视频各自的时长在 media 每一项的 duration_seconds。 |
| `hashtags` | 正文里的话题标签数组，按出现顺序；没有时不出现这个字段。 |
| `video_urls` | 全部视频地址，带签名，会过期。 |
| `media` | 附件列表，一个附件一项；没有附件时不出现。 |
| `reply_to_username` | 这条帖子回复的是谁（用户名）；不是回复时不出现。 |
| `root_post_author_username` | 这串对话最上面那条帖子的作者用户名。 |
| `is_liked_by_author` | 只在回复上出现：这条回复有没有被主帖作者点赞。 |
| `ai_label` | AI 生成内容的标注方式，如 SELF_DISCLOSURE_FLOW（作者自己标的）；没标注时不出现。 |
| `links` | 正文里的链接和帖子挂的链接。 |
| `image_urls` | 帖子的全部图片地址。 |
| `share_count` | 分享/转发数。 |

完整参数和字段：<https://everyinfra.com/threads-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

#### `post_detail`（内容详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `code` | 内容短码，用于拼 URL。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_is_verified` | 作者是否已认证。 |
| `author_is_private` | 作者账号是否私密。 |
| `author_follower_count` | 作者粉丝数。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `repost_count` | 转发数（区别于引用转发）。 |
| `quote_count` | 引用数：别人引用这条帖子发帖的次数。 |
| `share_count` | 分享/转发数。 |
| `view_count` | 浏览/播放数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `media_type` | 帖子类型：text 纯文字、image 单图、video 单视频、carousel 多图，或图片和视频混合。 |
| `image_count` | 图片张数。 |
| `video_count` | 视频个数。 |
| `language` | 内容语言代码（如 zh、en），由平台判定，可能不准。 |
| `is_edited` | 帖子是否编辑过。 |
| `is_reply` | 这条帖子是否为回复。 |
| `is_pinned` | 是否被作者置顶在主页。 |
| `is_spoiler` | 是否标了剧透遮罩。 |
| `reply_control` | 谁能回复这条帖子，如 everyone。 |
| `counts_hidden` | 作者是否隐藏了点赞数和分享数；隐藏时 like_count 为 null。 |
| `thread_id` | 作者连发的这一串帖子的编号，同一串的帖子这个值相同。 |
| `thread_length` | 作者连发的这一串一共几条；不是连发时为 1。 |
| `thread_position` | 这条是连发串里的第几条。 |
| `is_federated` | 是否同步到联邦宇宙（Fediverse）。 |
| `is_paid_partnership` | 是否标注为付费合作内容。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/threads-api/post_detail?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

#### `comments`（评论）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_is_verified` | 作者是否已认证。 |
| `author_is_private` | 作者账号是否私密。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `repost_count` | 转发数（区别于引用转发）。 |
| `quote_count` | 引用数：别人引用这条帖子发帖的次数。 |
| `share_count` | 分享/转发数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `media_type` | 帖子类型：text 纯文字、image 单图、video 单视频、carousel 多图，或图片和视频混合。 |
| `image_count` | 图片张数。 |
| `video_count` | 视频个数。 |
| `language` | 内容语言代码（如 zh、en），由平台判定，可能不准。 |
| `is_edited` | 帖子是否编辑过。 |
| `is_reply` | 这条帖子是否为回复。 |
| `reply_to_username` | 这条帖子回复的是谁（用户名）；不是回复时不出现。 |
| `root_post_author_username` | 这串对话最上面那条帖子的作者用户名。 |
| `reply_level` | 回复层级：1 是直接回复主帖，2 是回复的回复，以此类推。 |
| `is_pinned` | 是否被作者置顶在主页。 |
| `is_spoiler` | 是否标了剧透遮罩。 |
| `reply_control` | 谁能回复这条帖子，如 everyone。 |
| `counts_hidden` | 作者是否隐藏了点赞数和分享数；隐藏时 like_count 为 null。 |
| `is_federated` | 是否同步到联邦宇宙（Fediverse）。 |
| `is_paid_partnership` | 是否标注为付费合作内容。 |
| `is_liked_by_author` | 只在回复上出现：这条回复有没有被主帖作者点赞。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `post_id` | 这条回复的数字编号（id 是它的帖子码）。 |
| `reply_to_id` | 被回复那条的帖子码。 |
| `reply_to_url` | 被回复那条的链接。 |
| `reply_to` | 被回复的那个人的用户名。 |

完整参数和字段：<https://everyinfra.com/threads-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

#### `profile`（主页或对象详情）

| 字段 | 含义 |
|---|---|
| `user_id` | 用户在原平台的唯一 ID。 |
| `username` | 用户名（@handle）。 |
| `display_name` | 显示名，可能与 username 不同。 |
| `bio` | 个人简介，账号自己填写的文本。 |
| `follower_count` | 粉丝数。 |
| `is_verified` | 是否为平台认证账号（蓝V等）。 |
| `is_private` | 账号是否私密。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `avatar_url` | 头像图片链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `external_url` | 简介里的第一个链接；没有时不出现。 |
| `avatar_hd_url` | 高清头像地址。 |
| `public_view_count` | 近 30 天的公开浏览量，就是 Threads 在主页上公开显示的那个数；统计的起止日期在 public_view_count_start、public_view_count_end。 |
| `public_view_count_start` | public_view_count 统计区间的起始日期，YYYY-MM-DD。 |
| `public_view_count_end` | public_view_count 统计区间的截止日期，YYYY-MM-DD。 |
| `bio_links` | 简介区挂的全部链接。 |
| `topics` | 账号主页上挂的话题。 |
| `bio_links_detail` | 简介区挂的全部链接，每项 url、title（链接标题，有的才带）、is_verified（是否验证过归属）。 |
| `topics_detail` | 主页上挂的话题，每项 id、name、display_name、is_community。 |

完整参数和字段：<https://everyinfra.com/threads-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

#### `user_posts`（用户内容）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `code` | 内容短码，用于拼 URL。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_is_verified` | 作者是否已认证。 |
| `author_is_private` | 作者账号是否私密。 |
| `author_follower_count` | 作者粉丝数。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `repost_count` | 转发数（区别于引用转发）。 |
| `quote_count` | 引用数：别人引用这条帖子发帖的次数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `media_type` | 帖子类型：text 纯文字、image 单图、video 单视频、carousel 多图，或图片和视频混合。 |
| `image_count` | 图片张数。 |
| `video_count` | 视频个数。 |
| `topic` | 帖子挂的话题的内部名，如 bakingthreads；显示名在 topic_name。 |
| `topic_id` | 帖子挂的话题的编号。 |
| `topic_name` | 话题的显示名，如 Baking Threads。 |
| `topic_is_community` | 话题是否为社区。 |
| `language` | 内容语言代码（如 zh、en），由平台判定，可能不准。 |
| `is_edited` | 帖子是否编辑过。 |
| `is_reply` | 这条帖子是否为回复。 |
| `is_pinned` | 是否被作者置顶在主页。 |
| `is_spoiler` | 是否标了剧透遮罩。 |
| `reply_control` | 谁能回复这条帖子，如 everyone。 |
| `counts_hidden` | 作者是否隐藏了点赞数和分享数；隐藏时 like_count 为 null。 |
| `thread_id` | 作者连发的这一串帖子的编号，同一串的帖子这个值相同。 |
| `thread_length` | 作者连发的这一串一共几条；不是连发时为 1。 |
| `thread_position` | 这条是连发串里的第几条。 |
| `is_federated` | 是否同步到联邦宇宙（Fediverse）。 |
| `is_paid_partnership` | 是否标注为付费合作内容。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/threads-api/user_posts?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### 常见问题

**调用时要不要提供 Threads 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.56 起。失败、空结果、参数错误和鉴权失败都不收费；`urls` 传多个链接时每个算一次。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

**能把 Threads 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>。Agent 能自己搜 Threads 内容、读评论、查账号。

**用 Threads 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 Threads 的哪些数据？**

Threads 有 25 个能力：关键词搜索、主页或对象详情、用户内容、内容详情、评论、账号发现、粉丝数量、账号发的回复、带图片或视频的帖子、账号转发的帖子、推荐流、串帖、话题下的帖子、地点下的帖子、趋势下的帖子、粉丝列表、关注列表、推荐账号、帖子互动名单、热门话题、社区列表、互动率统计、搜索联想词、批量查账号、批量查帖子。每个能力的参数和返回字段见平台页 <https://everyinfra.com/threads-api?utm_source=github&utm_medium=example_repo&utm_campaign=threads-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 5 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "camping gear" --out posts.csv` | 2026-11-25 12:34 | 10 | $0.000778 |
| `python main.py post "<帖子链接>" --out post.json` | 2026-11-25 12:34 | 1 | $0.000556 |
| `python main.py replies "<帖子链接>" --out replies.csv` | 2026-11-25 12:35 | 10 | $0.000556 |
| `python main.py user <username>` | 2026-11-25 12:35 | 1 | $0.000556 |
| `python main.py posts <username> --out user_posts.csv` | 2026-11-25 12:35 | 10 | $0.000556 |

`post_detail` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "4037455647591333955",
  "text": "NAME SOMETHING PEOPLE ROMANTICIZE THAT'S ACTUALLY A TOTAL NI…",
  "like_count": 8921,
  "comment_count": 3191,
  "repost_count": 99,
  "quote_count": 22,
  "share_count": 44,
  "view_count": 555509,
  "posted_at": "2026-11-24T12:10:41+00:00",
  "media_type": "text",
  "image_count": 0,
  "video_count": 0,
  "language": "en"
}
```

## License

MIT
