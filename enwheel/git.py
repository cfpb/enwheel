import subprocess


def ls_remote(repo):
    return subprocess.check_output(['git', 'ls-remote', repo])


def refs_with_prefix(ls_remote_output, prefix=''):
    for line in ls_remote_output.split('\n'):
        if line:
            try:
                hash, ref = line.split('\t')
                if ref.startswith(prefix):
                    remainder = ref[len(prefix):]
                    yield remainder
            except ValueError:
                continue


def tags_for_repo(repo_url):
    refs_raw = ls_remote(repo_url)
    tags = refs_with_prefix(refs_raw, prefix='refs/tags/')
    return tags
