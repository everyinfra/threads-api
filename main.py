"""Threads API 示例（Threads API in Python）。

  python main.py search "camping gear" --out posts.csv  # 按关键词搜帖子 / search posts
  python main.py post "<帖子链接>" --out post.json      # 单条帖子 / one post
  python main.py replies "<帖子链接>" --out replies.csv # 帖子下的回复 / replies
  python main.py user <username>                        # 账号资料 / account profile
  python main.py posts <username> --out user_posts.csv  # 账号发布的帖子 / an account's posts
"""
import argparse

from everyinfra import fetch, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜帖子 / search posts by keyword")
    s.add_argument("keyword")
    po = sub.add_parser("post", help="单条帖子 / one post")
    po.add_argument("url")
    r = sub.add_parser("replies", help="帖子下的回复 / replies to one post")
    r.add_argument("url")
    u = sub.add_parser("user", help="账号资料 / account profile")
    u.add_argument("username")
    pos = sub.add_parser("posts", help="账号发布的帖子 / an account's posts")
    pos.add_argument("username")
    for x in (s, r, pos):
        x.add_argument("--pages", type=int, default=1, help="最多翻几页，每页算一次调用 / max pages, one call each")
    for x in (s, po, r, u, pos):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        rows, charged = fetch("search", {"keyword": a.keyword}, a.pages)
    elif a.cmd == "post":
        rows, charged = fetch("post_detail", {"url": a.url})
    elif a.cmd == "replies":
        rows, charged = fetch("comments", {"url": a.url}, a.pages)
    elif a.cmd == "user":
        rows, charged = fetch("profile", {"username": a.username})
    else:
        rows, charged = fetch("user_posts", {"username": a.username}, a.pages)
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
