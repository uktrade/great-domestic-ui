"""Script to easily add a new redirect. Requires package 'ansicolors'"""
from colors import color
import pathlib
import os


__here__ = pathlib.Path(__file__).parent
project_root = __here__ / ".."

redirects_file = project_root / 'conf' / 'url_redirects.py'
redirects_tests_file = project_root / 'conf' / 'tests' / \
    'test_url_redirects.py'

start_redirects = 'redirects = [\n'
redirect_template = (
    '    url(\n'
    "        r'^{}/$',\n"
    '        QuerystringRedirectView.as_view(\n'
    "            url='{}'),\n"
    "        name='{}'\n"
    '    ),\n'
)
test_template = "    ('/{}/', '{}'),\n"


def file_string(filepath):
    """Get string from file."""
    with open(os.path.abspath(filepath)) as f:
        return f.read()


def insert_new(new_code, file_path):
    split = file_string(file_path).split(start_redirects, 1)
    new = ''.join([
        split[0],
        start_redirects,
        new_code,
        split[1],
        ])

    with open(file_path, "w") as f:
        f.write(new)


def main():
    redirect_from = input(color(
        "Enter the path you wish to redirect FROM (do not start with '/'):\n",
        fg='purple', style='bold')).strip()
    redirect_to = input(color(
        "Enter the url you wish to redirect TO (with a trailing '/'):\n",
        fg='purple', style='bold')).strip()
    redirect_name = input(color(
        "Enter the name of the redirect:\n",
        fg='purple', style='bold')).strip()
    confirm = (
        "Create {} that redirects "
        "from /{}/ to {}. Is this correct? y/n\n").format(
        redirect_name, redirect_from, redirect_to).strip()

    user_continue = input(color(confirm, fg='blue', style='bold'))

    if user_continue != 'y':
        return

    redirect_code = redirect_template.format(
        redirect_from, redirect_to, redirect_name)

    insert_new(redirect_code, redirects_file)

    print(color(
        "Redirect added to url_redirects.py", fg='green', style='bold'))

    test_code = test_template.format(redirect_from, redirect_to)

    insert_new(test_code, redirects_tests_file)

    print(color(
        "Redirect added to test_url_redirects.py", fg='green', style='bold'))


if __name__ == '__main__':
    main()
