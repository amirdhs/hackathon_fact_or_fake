import random

from colorama import Style

from colors import (
    INPUT_COLOR,
    PLAIN_HIGHLIGHT_COLOR,
    ERROR_COLOR,
)
from player import Player
from utils import clear_console


def print_paragraph_with_linebreaks(
    paragraph: str, line_length: int = 80, indent: int = 0
) -> None:
    """
    Print a paragraph with line breaks to ensure that no line exceeds the specified line length.
    The paragraph is indented by the specified number of spaces.

    :param paragraph: The paragraph to print.
    :param line_length: The maximum length of a line.
    :param indent: The number of spaces to indent the paragraph.
    """
    if not paragraph:
        return
    if line_length <= 0:
        raise ValueError("line_length must be greater than 0")
    if indent < 0:
        raise ValueError("indent must be greater than or equal to 0")

    words = paragraph.split()
    current_line_length = 0
    print((" " * indent) + words[0], end=" ")
    for word in words[1:]:
        if current_line_length + len(word) + 1 <= line_length:
            print(word, end=" ")
            current_line_length += len(word) + 1
        else:
            print("\n" + (" " * indent) + word, end=" ")
            current_line_length = len(word)
    print()


def print_two_paragraphs_side_by_side(
    heading1: str,
    paragraph1: str,
    heading2: str,
    paragraph2: str,
    line_length: int = 200,
    separator: str = "  │  ",
) -> None:
    """
    Print two paragraphs side by side with a separator in between to ensure that no line exceeds the specified line length.

    :param heading1: The heading for the first paragraph.
    :param paragraph1: The first paragraph to print.
    :param heading2: The heading for the second paragraph.
    :param paragraph2: The second paragraph to print.
    :param line_length: The maximum length of a line.
    :param separator: The separator between the two paragraphs.
    """
    if not paragraph1 or not paragraph2:
        return
    if line_length <= 0:
        raise ValueError("line_length must be greater than 0")

    words1 = paragraph1.split()
    words2 = paragraph2.split()

    line_length_per_paragraph = (line_length - len(separator)) // 2
    current_line_length1 = 0
    current_line_length2 = 0
    lines1 = []
    lines2 = []
    for _ in range(max(len(words1), len(words2))):
        line1 = ""
        while (
            words1
            and current_line_length1 + len(words1[0]) + 1 <= line_length_per_paragraph
        ):
            current_word = words1.pop(0)
            line1 += current_word + " "
            current_line_length1 += len(current_word) + 1
        line1 = line1.ljust(line_length_per_paragraph)
        lines1.append(line1)

        line2 = ""
        while (
            words2
            and current_line_length2 + len(words2[0]) + 1 <= line_length_per_paragraph
        ):
            current_word = words2.pop(0)
            line2 += current_word + " "
            current_line_length2 += len(current_word) + 1
        lines2.append(line2)

        current_line_length1 = 0
        current_line_length2 = 0

    space_after_heading1 = line_length_per_paragraph - len(heading1)
    if heading1:
        heading1 = PLAIN_HIGHLIGHT_COLOR + heading1 + Style.RESET_ALL
    if heading2:
        heading2 = PLAIN_HIGHLIGHT_COLOR + heading2 + Style.RESET_ALL
    if heading1 and heading2:
        print(heading1 + (" " * space_after_heading1) + separator + heading2)
        print("─" * line_length)
    for line1, line2 in zip(lines1, lines2):
        if line1.strip() == "" and line2.strip() == "":
            break
        print(line1 + separator + line2)


def get_player_answer(
    question: str, options: list[str], silent_error: bool = False
) -> int:
    """
    Get the player's answer to a multiple-choice question.

    :param question: The question to ask the player.
    :param options: The list of options to choose from.
    :param silent_error: Whether to suppress error messages.
    :return: The index of the chosen option.
    """
    if not question:
        raise ValueError("question must not be empty.")
    if not options:
        raise ValueError("options must not be empty.")
    if not all(isinstance(option, str) for option in options):
        raise ValueError("options must contain only strings.")
    if not all(options):
        raise ValueError("options must not contain empty strings.")

    print("─" * len(question))
    print(INPUT_COLOR + question + Style.RESET_ALL)
    answer_lines = ["", "", ""]
    for i, option in enumerate(options, start=1):
        text = f"{i}. {option}"
        horizontal_line = "─" * (len(text) + 2)
        answer_lines[0] += f"╭{horizontal_line}╮  "
        answer_lines[1] += f"│ {PLAIN_HIGHLIGHT_COLOR + text + Style.RESET_ALL} │  "
        answer_lines[2] += f"╰{horizontal_line}╯  "
    for line in answer_lines:
        print(line)
    while True:
        try:
            answer = int(input(""))
            if 1 <= answer <= len(options):
                return answer - 1
            else:
                if not silent_error:
                    print(
                        ERROR_COLOR
                        + f"Choose only between 1 - {len(options)}"
                        + Style.RESET_ALL
                    )
        except ValueError:
            if not silent_error:
                print(
                    ERROR_COLOR + "Input must be a number. Try again!" + Style.RESET_ALL
                )


def closing_screen() -> None:
    """Print closing screen to terminal"""
    clear_console()
    ascii_art = """

     ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
    ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                                                              
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⡉⣉⡛⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿   THANKS FOR PLAYING
    ⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠄⠄⠄⠄⠄⢀⣸⣿⣿⡿⠿⡯⢙⠿⣿⣿⣿⣿⣿⣿   We hope you had fun and learned something new.
    ⣿⣿⣿⣿⣿⣿⡿⠄⠄⠄⠄⠄⡀⡀⠄⢀⣀⣉⣉⣉⠁⠐⣶⣶⣿⣿⣿⣿⣿⣿   We had a lot of fun creating it!
    ⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠁⣿⣿⣀⠈⠿⢟⡛⠛⣿⠛⠛⣿⣿⣿⣿⣿⣿⣿   See you again soon.
    ⣿⣿⣿⣿⣿⣿⡆⠄⠄⠄⠄⠄⠈⠁⠰⣄⣴⡬⢵⣴⣿⣤⣽⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡇⠄⢀⢄⡀⠄⠄⠄⠄⡉⠻⣿⡿⠁⠘⠛⡿⣿⣿⣿⣿⣿⣿⣿      
    ⣿⣿⣿⣿⣿⡿⠃⠄⠄⠈⠻⠄⠄⠄⠄⢘⣧⣀⠾⠿⠶⠦⢳⣿⣿⣿⣿⣿⣿⣿   Don´t eat dogs and cats!
    ⣿⣿⣿⣿⣿⣶⣤⡀⢀⡀⠄⠄⠄⠄⠄⠄⠻⢣⣶⡒⠶⢤⢾⣿⣿⣿⣿⣿⣿⣿   
    ⣿⣿⣿⣿⡿⠟⠋⠄⢘⣿⣦⡀⠄⠄⠄⠄⠄⠉⠛⠻⠻⠺⣼⣿⠟⠋⠛⠿⣿⣿   
    ⠋⠉⠁⠄⠄⠄⠄⠄⠄⢻⣿⣿⣶⣄⡀⠄⠄⠄⠄⢀⣤⣾⣿⣿⡀⠄⠄⠄⠄⢹   
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿⣷⡤⠄⠰⡆⠄⠄⠈⠉⠛⠿⢦⣀⡀⡀⠄
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢿⣿⠟⡋⠄⠄⠄⢣⠄⠄⠄⠄⠄⠄⠄⠈⠹⣿⣀                    
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠘⣷⣿⣿⣷⠄⠄⢺⣇⠄⠄⠄⠄⠄⠄⠄⠄⠸⣿                                 
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠹⣿⣿⡇⠄⠄⠸⣿⡄⠄⠈⠁⠄⠄⠄⠄⠄⣿   ____________________________________________                             
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⡇⠄⠄⠄⢹⣧⠄⠄⠄⠄⠄⠄⠄⠄⠘   Creators: Dominik, Philipp, Amir, Jorge, Lea
    """

    # Print the full ASCII art
    print(ascii_art)


def final(players) -> None:
    """display graphic, final score & credits"""
    clear_console()

    #  trophy = """
    #  ...         ...
    # --..-**-- .=*-..--
    # --  :#+==.:**:  --
    #  :: :*===:=**:.::
    #    .:*==+:=**:.
    #     ..++*+++..
    #        .++.
    #        -=:-
    #      .=+-:+=.
    #      .:.. .:.
    #      """
    #
    #
    #  print(GOLD_COLOR + trophy + Style.RESET_ALL)

    emojis = ["🏆 ", "🎉 ", "🥳 ", "🍾 ", "⭐ "]
    emoji_str = " "
    for i in range(1000):
        rand_emoji = random.choice(emojis)
        emoji_str += rand_emoji

    print_paragraph_with_linebreaks(emoji_str, 100)
    display_podium(players)

    max_score = max(player.score for player in players.values())
    winners = [
        player.color + player.name + Style.RESET_ALL
        for player in players.values()
        if player.score == max_score
    ]
    trophy_emoji = "🏆"

    if len(winners) == 1:
        fact_master = f"{trophy_emoji * 3} {winners[0]} is the **FACT MASTER**! {trophy_emoji * 3}"
    else:
        fact_master = f"{trophy_emoji * 3} {' and '.join(winners)} are the **FACT MASTERS**! {trophy_emoji * 3}"

    print(
        "\n\n"
        + PLAIN_HIGHLIGHT_COLOR
        + f"  {trophy_emoji} Congratulation To All Players {trophy_emoji}  "
        + Style.RESET_ALL
    )
    print()
    print(PLAIN_HIGHLIGHT_COLOR + fact_master + Style.RESET_ALL)
    print()


def header() -> None:
    """Print header to article"""
    clear_console()
    ascii_art = """
    ▗▄▄▄▖ ▗▄▖  ▗▄▄▖▗▄▄▄▖     ▗▄▖ ▗▄▄▖     ▗▄▄▄▖ ▗▄▖ ▗▖ ▗▖▗▄▄▄▖
    ▐▌   ▐▌ ▐▌▐▌     █      ▐▌ ▐▌▐▌ ▐▌    ▐▌   ▐▌ ▐▌▐▌▗▞▘▐▌   
    ▐▛▀▀▘▐▛▀▜▌▐▌     █      ▐▌ ▐▌▐▛▀▚▖    ▐▛▀▀▘▐▛▀▜▌▐▛▚▖ ▐▛▀▀▘
    ▐▌   ▐▌ ▐▌▝▚▄▄▖  █      ▝▚▄▞▘▐▌ ▐▌    ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▙▄▄▖
    """

    # Print the ASCII art
    print(ascii_art)


def opening_screen() -> None:
    """Print opening screen"""
    clear_console()
    ascii_art = """
    
    ███████╗ █████╗  ██████╗████████╗██████╗ ██╗   ██╗███████╗████████╗███████╗██████╗ ███████╗
    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝
    █████╗  ███████║██║        ██║   ██████╔╝██║   ██║███████╗   ██║   █████╗  ██████╔╝███████╗
    ██╔══╝  ██╔══██║██║        ██║   ██╔══██╗██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗╚════██║
    ██║     ██║  ██║╚██████╗   ██║   ██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║███████║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝
                                                                                               

    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⡉⣉⡛⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿   MAKE WIKIPEDIA TRUE AGAIN!
    ⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠄⠄⠄⠄⠄⢀⣸⣿⣿⡿⠿⡯⢙⠿⣿⣿⣿⣿⣿⣿   We live in uncertain times, with global crises such as climate change,
    ⣿⣿⣿⣿⣿⣿⡿⠄⠄⠄⠄⠄⡀⡀⠄⢀⣀⣉⣉⣉⠁⠐⣶⣶⣿⣿⣿⣿⣿⣿   war, fascism and fake news. Fortunately, you can at least do something
    ⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠁⣿⣿⣀⠈⠿⢟⡛⠛⣿⠛⠛⣿⣿⣿⣿⣿⣿⣿   about fake news here and now.
    ⣿⣿⣿⣿⣿⣿⡆⠄⠄⠄⠄⠄⠈⠁⠰⣄⣴⡬⢵⣴⣿⣤⣽⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡇⠄⢀⢄⡀⠄⠄⠄⠄⡉⠻⣿⡿⠁⠘⠛⡿⣿⣿⣿⣿⣿⣿⣿   The game will present you with two articles from Wikipedia.
    ⣿⣿⣿⣿⣿⡿⠃⠄⠄⠈⠻⠄⠄⠄⠄⢘⣧⣀⠾⠿⠶⠦⢳⣿⣿⣿⣿⣿⣿⣿   Unfortunately, we are not sure which of the articles are fake.
    ⣿⣿⣿⣿⣿⣶⣤⡀⢀⡀⠄⠄⠄⠄⠄⠄⠻⢣⣶⡒⠶⢤⢾⣿⣿⣿⣿⣿⣿⣿   You have to expose the fake.
    ⣿⣿⣿⣿⡿⠟⠋⠄⢘⣿⣦⡀⠄⠄⠄⠄⠄⠉⠛⠻⠻⠺⣼⣿⠟⠋⠛⠿⣿⣿
    ⠋⠉⠁⠄⠄⠄⠄⠄⠄⢻⣿⣿⣶⣄⡀⠄⠄⠄⠄⢀⣤⣾⣿⣿⡀⠄⠄⠄⠄⢹   When you are ready to start press "Enter", we are counting on you!
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿⣷⡤⠄⠰⡆⠄⠄⠈⠉⠛⠿⢦⣀⡀⡀⠄
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢿⣿⠟⡋⠄⠄⠄⢣⠄⠄⠄⠄⠄⠄⠄⠈⠹⣿⣀                            
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠘⣷⣿⣿⣷⠄⠄⢺⣇⠄⠄⠄⠄⠄⠄⠄⠄⠸⣿                            
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠹⣿⣿⡇⠄⠄⠸⣿⡄⠄⠈⠁⠄⠄⠄⠄⠄⣿                            
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⡇⠄⠄⠄⢹⣧⠄⠄⠄⠄⠄⠄⠄⠄⠘
    """

    # Print the full ASCII art
    print(ascii_art)

    input(INPUT_COLOR + 'Press "Enter" to start' + Style.RESET_ALL)


def display_podium(players: dict[str, Player]) -> None:
    """Displays a podium for the happy winners using a grid structure."""
    sorted_scores = sorted(players.values(), key=lambda x: x.score, reverse=True)

    scale_factor = 10
    podium_info = [
        (player.name, player.score // scale_factor, player.score, player.color)
        for player in sorted_scores
    ]
    max_height = max(height for _, height, _, _ in podium_info)

    # rank_colors = [Fore.LIGHTYELLOW_EX, Fore.LIGHTWHITE_EX, Fore.YELLOW]
    # default_color = Fore.LIGHTGREEN_EX

    grid = []
    for level in range(max_height + 1):
        row = []
        for i, (_, height, _, color) in enumerate(podium_info):
            # color = rank_colors[i] if i < len(rank_colors) else default_color
            if max_height - level < height:
                row.append(color + "|      |" + Style.RESET_ALL)
            elif max_height - level == height:
                row.append(color + "@******@" + Style.RESET_ALL)
            else:
                row.append("        ")  #
        grid.append(row)

    for row in grid:
        print("  ".join(row))

    score_row = [
        f"{color}{str(score).center(8)}{Style.RESET_ALL}"
        for _, _, score, color in podium_info
    ]
    print("  ".join(score_row))

    name_row = [
        f"{color}{str(name).center(8)}{Style.RESET_ALL}"
        for name, _, _, color in podium_info
    ]
    print("  ".join(name_row))


def display_player_scores_vertically(players: dict[str, Player]) -> None:
    """Displays each player's name, score, and stars in a vertical format"""
    for player in players.values():
        stars = "*" * (player.score // 10)
        print(
            f"{player.color}{player.name:<10}{Style.RESET_ALL} {player.score:<3} {stars}"
        )


def display_player_scores_horizontally(players: dict[str, Player]) -> None:
    """Displays each player's name, score, and stars in a horizontal format"""
    column_width = 15

    name_row = "  ".join(
        f"{player.color}{player.name:<{column_width}}{Style.RESET_ALL}"
        for player in players.values()
    )
    score_row = "  ".join(
        f"{player.color}{str(player.score):<{column_width}}{Style.RESET_ALL}"
        for player in players.values()
    )

    print(" " * 2, name_row)
    print(" " * 2, score_row)


def main():
    def test_print_paragraph_with_linebreaks() -> None:
        paragraph = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
        print_paragraph_with_linebreaks(paragraph)
        print("=================")
        print_paragraph_with_linebreaks(paragraph, line_length=40)
        print("=================")
        print_paragraph_with_linebreaks(paragraph, line_length=40, indent=4)

    def test_print_two_paragraphs_side_by_side() -> None:
        paragraph = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
        header1 = "Paragraph 1"
        header2 = "Paragraph 2"
        print_two_paragraphs_side_by_side(header1, paragraph, header2, paragraph)
        print()
        print_two_paragraphs_side_by_side("", paragraph, "", paragraph, line_length=100)

    def test_get_player_answer() -> None:
        question = "Choose between 1 or 2 and hit enter!"
        options = ["FACT", "FAKE"]
        answer = get_player_answer(question, options)
        print(f"Player chose option {answer + 1}")

    # test_print_paragraph_with_linebreaks()
    # test_print_two_paragraphs_side_by_side()
    # test_get_player_answer()


if __name__ == "__main__":
    main()
