const { Octokit } = require("@octokit/core");
const fs = require('fs');

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

async function getFriends() {
  const { data: issues } = await octokit.request('GET /repos/{owner}/{repo}/issues', {
    owner: 'xaoxuu',
    repo: 'friends',
    state: 'closed',
    labels: '友链'
  });

  const friends = issues.map(issue => {
    const { title, body, user } = issue;
    const [name, link, avatar, descr] = body.split('\n').map(item => item.split(': ')[1]);
    return {
      name,
      link,
      avatar,
      descr,
      tag: '大佬'
    };
  });

  fs.writeFileSync('friends.json', JSON.stringify(friends, null, 2));
}

getFriends();
