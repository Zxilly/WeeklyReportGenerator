from mdutils import MdUtils

from static import static
from util import str2time

target_list = ["casbin", "casdoor"]

start_time = "2021-01-10T00:50:59Z"
end_time = "2021-05-17T00:50:59Z"

data = static(start_time, end_time)
info = data.get_info()

open_issues = []
open_prs = []
review_prs = []
comment_issues = []

for node in info['data']['user']['contributionsCollection']["issueContributions"]['nodes']:
    repo = node["issue"]["repository"]["nameWithOwner"]
    for target in target_list:
        if repo.find(target) != -1:
            open_issues.append(node)

for node in info['data']['user']['contributionsCollection']["pullRequestContributions"]['nodes']:
    repo = node["pullRequest"]["repository"]["nameWithOwner"]
    for target in target_list:
        if repo.find(target) != -1:
            open_prs.append(node)

for node in info['data']['user']['contributionsCollection']["pullRequestReviewContributions"]['nodes']:
    repo = node["pullRequest"]["repository"]["nameWithOwner"]
    for target in target_list:
        if repo.find(target) != -1:
            review_prs.append(node)

comment_issue_ids = []
for node in info['data']['user']["issueComments"]['nodes']:
    repo = node["issue"]["repository"]["nameWithOwner"]
    cur_datetime = str2time(node["issue"]["createdAt"])
    start_datetime = str2time(start_time)
    end_datetime = str2time(end_time)
    for target in target_list:
        if repo.find(target) != -1:
            if start_datetime <= cur_datetime <= end_datetime:
                if node['issue']['id'] not in comment_issue_ids:
                    comment_issue_ids.append(node['issue']['id'])
                    comment_issues.append(node)

mdFile = MdUtils(file_name='output', title='Weekly Report')

if len(open_issues) > 0:
    mdFile.new_header(level=2, title='Open Issues', add_table_of_contents='n')
    mdFile.new_list(
        map(lambda x: 'Open Issue ' + mdFile.new_inline_link(link=x['issue']['url'], text=x['issue']['title']),
            open_issues))

if len(open_prs) > 0:
    mdFile.new_header(level=2, title='Open PRs', add_table_of_contents='n')
    mdFile.new_list(
        map(lambda x: 'Open PR ' + mdFile.new_inline_link(link=x['pullRequest']['url'], text=x['pullRequest']['title']),
            open_prs))

if len(review_prs) > 0:
    mdFile.new_header(level=2, title='Review PRs', add_table_of_contents='n')
    mdFile.new_list(map(lambda x: 'Review PR ' + mdFile.new_inline_link(link=x['pullRequestReview']['url'],
                                                                        text=x['pullRequest']['title']), review_prs))

if len(comment_issues) > 0:
    mdFile.new_header(level=2, title='Reply Issues', add_table_of_contents='n')
    mdFile.new_list(
        map(lambda x: 'Reply Issue ' + mdFile.new_inline_link(link=x['issue']['url'], text=x['issue']['title']),
            comment_issues))

mdFile.create_md_file()
