from bs4 import BeautifulSoup
import shutil
import re
import textwrap

from pretty_console import console, escape


def print_courses_data(json_data):
    display_data = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['teacher']))
    max_course_id_length = max(len(e[0]) for e in display_data)
    max_course_name_length = max(len(e[1]) for e in display_data)
    display_data = sorted(display_data, key=lambda x: x[1])

    console.print('[u bright_blue]Your courses:[/]')
    for e in display_data:
        print(f'{e[0].ljust(max_course_id_length)}: \033[1m{e[1].ljust(max_course_name_length)}\033[0m\tby {e[2]}')


def print_series_data(json_data):
    display_data = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['description']))
    max_series_id_length = max(len(e[0]) for e in display_data)
    max_series_name_length = max(len(e[1]) for e in display_data)

    console.print("[u bright_blue]All series:[/]")
    for e in display_data:
        description = e[2].split('\n')
        new_description = ''

        for line in description:
            # Convert Markdown links to Ansi links. TERMINAL DEPENDANT
            line = re.sub(r'{: target="_blank"}', '', line)
            # line = re.sub(r'\[(.*?)\]\((.*?)\)', '\033]8;;\\2\033\\ \\1\033]8;;\033\\ ', line)

            # Replace bold and italics in Markdown to use Ansi codes
            line = re.sub(r'\*\*(.*?)\*\*', '\033[1m\\1\033[0m', line)
            line = re.sub(r'_(.*?)_', '\033[3m\\1\033[0m', line)

            if len(line.replace("**", "").replace("_", "")) > shutil.get_terminal_size().columns - 8:
                line = line.split(" ")
                new_line = ''
                line_size = 0
                for word in line:
                    if line_size + len(word) > shutil.get_terminal_size().columns - 8:
                        new_line += '\n'
                        line_size = 0
                    new_line += word + ' '
                    line_size += len(word + ' ')
                line = new_line

            new_description += line + '\n'

        new_description = textwrap.indent(new_description, '\t')
        print(
            f"{e[0].ljust(max_series_id_length)}: \033[1m{e[1].ljust(max_series_name_length)}\033[0m\n{new_description}")


def print_exercise_data(json_data):
    display_data = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['last_solution_is_best'], field['has_solution']))
    max_exercise_id_length = max(len(e[0]) for e in display_data)
    max_exercise_name_length = max(len(e[1]) for e in display_data)

    console.print('[u bright_blue]Exercises:[/]')
    for e in display_data:
        console.print(
            f"{escape(e[0].ljust(max_exercise_id_length))}: [bold]{e[1].ljust(max_exercise_name_length)}[/]\t" +
            "[bold bright_green]SOLVED[/]" * (e[2] and e[3]) +
            "[bold bright_red]WRONG[/]" * (not e[2] and e[3]) +
            "[bold]NOT YET SOLVED[/]" * (not e[3])
        )


def print_exercise(json_data, connection, headers):
    description_url = json_data['description_url'][28:]
    connection.request("GET", description_url, headers=headers)
    res = connection.getresponse()
    data = res.read()
    connection.close()

    soup = BeautifulSoup(data, features="html.parser")
    description = soup.find("div", {"class": "activity-description"})

    print("\033[1;4;91mWARNING: the description may not be correct, DO NOT rely on this for exams and tests!!\n"
          "Instead, use this url:\033[0m " + json_data['description_url'])
    print(description.get_text())
    print("\033[1;4;91mWARNING: the description may not be correct, DO NOT rely on this for exams and tests!!\n"
          "Instead, use this url:\033[0m " + json_data['description_url'])


def print_result(json_results):
    if json_results['accepted']:
        console.print("[bold bright_green]All test passed![/] You can continue to next exercise.")
    else:
        for group in json_results['groups']:
            print(group['description'] + ": " + str(group['badgeCount']) + " tests failed.")

            if group['badgeCount'] > 0:
                print("Failed exercises:")
                for test in group['groups']:
                    if not test['accepted']:
                        print("\t- " + test['description']['description'] + "\n\t\t" +
                              test['groups'][0]['description']['description'])
