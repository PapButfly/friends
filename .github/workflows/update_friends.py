import os
import json
import re
from github import Github

# 从环境变量中获取GitHub Token
github_token = os.environ.get('GITHUB_TOKEN')
if not github_token:
    raise ValueError("GitHub Token not found in environment variables.")

# 初始化GitHub API客户端
g = Github(github_token)
repo = g.get_repo(os.environ.get('GITHUB_REPOSITORY'))

def get_issues():
    """
    获取所有带有 '友链' 标签的已关闭 Issue。
    """
    # 使用 labels=['友链'] 精确过滤
    issues = repo.get_issues(state='closed', labels=['友链'])
    return issues

def parse_issue_body(body):
    """
    从 Issue 正文中解析 JSON 数据。
    """
    # 使用正则表达式精确匹配```json...```中的内容
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', body)
    if json_match:
        json_data = json_match.group(1)
        try:
            # 尝试解析JSON
            data = json.loads(json_data)
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    return None

def generate_friends_list():
    """
    生成 friends.json 文件。
    """
    friends = []
    issues = get_issues()

    for issue in issues:
        parsed_data = parse_issue_body(issue.body)
        if parsed_data:
            friend_entry = {
                "name": parsed_data.get("title", ""),
                "link": parsed_data.get("url", ""),
                "avatar": parsed_data.get("icon", ""),
                "descr": parsed_data.get("description", ""),
                "tag": "大佬"
            }
            friends.append(friend_entry)

    with open('friends.json', 'w', encoding='utf-8') as f:
        json.dump(friends, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    generate_friends_list()
