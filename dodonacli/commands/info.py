import click
from click_default_group import DefaultGroup


@click.group(help="Info about shell-completion, changelog, version, update-availability and GitHub page.",
             cls=DefaultGroup, default='version', default_if_no_args=True)
def info():
    pass


@click.command(help='Display the current version of DodonaCLI. The versioning system '
                    'uses a YYYY.M.D format.')
def version():
    from dodonacli.source import pretty_console
    dodonacli_version = get_dodonacli_version()

    pretty_console.console.print(
        f"DodonaCLI {dodonacli_version}"
    )


@click.command(help='Checks if there is a new update available for DodonaCLI.')
def check_update():
    from packaging.version import parse
    from pkg_info import get_pkg_info
    from dodonacli.source import pretty_console

    dodonacli_version = get_dodonacli_version()

    pkg = get_pkg_info('DodonaCLI')

    if parse(pkg.version) > parse(dodonacli_version):
        pretty_console.console.print(
            f"There is a new version available: {pkg.version}.\n"
            f"You can update your old version ({dodonacli_version}) with"
            "\n\tpip install --upgrade DodonaCLI"
        )
    else:
        print("Your DodonaCLI is up-to-date.")


@click.command(help='Tab completion, very handy for fast use')
def completion():
    from dodonacli.source import pretty_console

    pretty_console.console.print(
        "\nThere are 2 ways of doing tab-completion: \n"
        "   - using Click's default tab-completion for bash/zsh/fish\n"
        "   - using DodonaCLI's custom script for bash only\n"
        "\nThe reason there is a custom script, is because the default completion lacks "
        "a bit here and there.\n"
        "The default option is easier to use, and doesn't need a redownload after an update.\n\n"
        "To install the default completion:\n"
        "   Follow this short tutorial:\n"
        "       https://click.palletsprojects.com/en/8.1.x/shell-completion/#enabling-completion\n"
        "   Replace every occurence of 'foo-bar' with 'dodona'\n"
        "   Do notice that you can choose how you name the file, and where you put it.\n\n"
        "To install the custom script for bash:\n"
        "   Go to DodonaCLI's GitHub: https://www.github.com/BWindey/DodonaCLI\n"
        "   And download 'dodonacli_completion_script.sh' (at top-level of project structure)\n"
        "   Now add 'source <PATH TO SCRIPT>' to your '.bashrc',\n"
        "   where you fill in the path to the downloaded script."
        "\n\n"
        "For both ways you'll have to either restart your terminal, or re-'source' your .bashrc/.fishrc/...\n"
        "Happy tabbing!\n"
    )


@click.command(help='Link to the GitHub page of DodonaCLI. Can be handy for the README page, manpages,'
                    ' Issues (bug reports) and pull requests.')
def github():
    from dodonacli.source import pretty_console

    pretty_console.console.print("https://www.github.com/BWindey/DodonaCLI")


@click.command(help='Changelog for the latest version.')
def changelog():
    from rich.markdown import Markdown
    from dodonacli.source import pretty_console

    changelog_raw = (
        "\t- Reworked tutorial to be more user-friendly, and look a bit better\n"
        "\t- Tweaked some message-endings here and there to be more consistent\n"
        "\t\n"
        "\tAs always, you can use the '--help' flag after every command and sub-command to learn more.\n"
        "\tHappy coding!\n"
    )
    md = Markdown(changelog_raw)
    pretty_console.console.print(md)


def get_dodonacli_version():
    from importlib import metadata
    return metadata.version(__package__.split('.')[0])


info.add_command(version)
info.add_command(check_update)
info.add_command(completion)
info.add_command(github)
info.add_command(changelog)
