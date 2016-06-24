from datetime import datetime
import github.GithubException as GithubException

def get_orgn_repos(g, orgn):
    org = g.get_organization(orgn)
    return org.get_repos()


def get_rc_branch_name(rc_prefix, rc_format, dt_format):
    now = datetime.now()
    return (rc_prefix + now.strftime(rc_format)), now.strftime(dt_format)


def print_github_exc(msg, ex):
    assert isinstance(ex, GithubException)

    if 'errors' in ex.data:
        errMsg = ', '.join([e['message'] for e in ex.data['errors']])
    elif 'message' in ex.data:
        errMsg = ex.data['message']
    else:
        errMsg = 'Unknown error from Github API'

    print(msg + ': ' + errMsg)
