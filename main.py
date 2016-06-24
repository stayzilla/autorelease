import sys
from cfg import config
from lib import *
from github import Github
import github.GithubException as GithubException
from github.GithubException import BadCredentialsException

token = config.get('github', 'token')
orgn = config.get('github', 'organization')

base_branch = config.get('branches', 'base')
main_branch = config.get('branches', 'main')
rc_prefix = config.get('branches', 'rcprefix')
rc_format = config.get('branches', 'rcformat')
dt_format = config.get('branches', 'dtformat')

g = Github(login_or_token=token)

print('Process starting')
try:
    repos = get_orgn_repos(g, orgn)
    for repo in repos:
        try:
            bb = repo.get_branch(base_branch)
        except GithubException as ex:
            print('No branch ' + base_branch + ' in ' + repo.name)
            continue

        print('--')
        print(base_branch + ' branch found in ' + repo.name)

        ref_name, formatted_date = get_rc_branch_name(rc_prefix, rc_format, dt_format)
        ref_name = 'refs/heads/' + ref_name
        shastring = bb.commit.sha

        try:
            repo.create_git_ref(ref=ref_name, sha=shastring)
        except GithubException as ex:
            print_github_exc('Failed to create RC branch', ex)
            print('--')
            continue

        print('Created RC branch ' + ref_name)

        pr_title = '[bot] release candidate: ' + formatted_date
        pr_body = 'This rc branch has been pulled out from the latest devel branch'

        try:
            repo.create_pull(head=ref_name, base=main_branch, title=pr_title, body=pr_body)
        except GithubException as ex:
            print_github_exc('Unable to create pull request', ex)
            print('--')
            continue

        print('Created Pull Request successfully')

        print('Finished processing ' + repo.name)
        print('--')
except BadCredentialsException as ex:
    print("Bad Github token found in configuration.")
    print("Cannot proceed. Process will now exit.")
    sys.exit(1)
except Exception as ex:
    print("An un-foreseen exception has crashed this program.")
    print("Please forward the exception log below to the concerned person.")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print('Process complete')
sys.exit(0)
