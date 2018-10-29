from typing import Dict

from colorama import Back, Fore, Style
from enums import Color


class ConsoleHelper:
    __back_colors: Dict[Color, int] = {
        Color.BLACK: Back.BLACK,
        Color.WHITE: Back.WHITE,
        Color.RED: Back.RED,
        Color.GREEN: Back.GREEN,
        Color.BLUE: Back.BLUE,
        Color.YELLOW: Back.YELLOW
    }
    
    __fore_colors: Dict[Color, int] = {
        Color.BLACK: Fore.BLACK,
        Color.WHITE: Fore.WHITE,
        Color.RED: Fore.RED,
        Color.GREEN: Fore.GREEN,
        Color.BLUE: Fore.BLUE,
        Color.YELLOW: Fore.YELLOW
    }

    __last_back_colors = [Color.BLACK]
    __last_fore_colors = [Color.WHITE]

    @staticmethod
    def set_print_background(background: Color, save_color=True) -> None:
        """
        Sets the background color print() uses
        :param background: The foreground (text) color
        :param save_color: Indicates if the color will be saved so that it can be reverted to should another color
                           be set after it
        """

        if save_color:
            ConsoleHelper.__last_back_colors.append(background)

        print(ConsoleHelper.__back_colors[background], end='')

    @staticmethod
    def set_print_foreground(foreground: Color, save_color=True) -> None:
        """
        Sets the foreground color print() uses
        :param foreground: The foreground (text) color
        :param save_color: Indicates if the color will be saved so that it can be reverted to should another color
                           be set after it
        """

        if save_color:
            ConsoleHelper.__last_fore_colors.append(foreground)

        print(ConsoleHelper.__fore_colors[foreground], end='')

    @staticmethod
    def reset_all_colors() -> None:
        """
        Resets the color that print uses
        """
        print(Style.RESET_ALL)

    @staticmethod
    def revert_print_background():
        """
        Sets the background color print() uses to be the last one from when set_print_background was called
        """

        # We need to go two colors back, as the last color is what we're currently on
        if len(ConsoleHelper.__last_back_colors) > 1:
            ConsoleHelper.set_print_background(ConsoleHelper.__last_back_colors[-2], False)

        # Never delete the original color
        if len(ConsoleHelper.__last_back_colors) > 1:
            del ConsoleHelper.__last_back_colors[-1]

    @staticmethod
    def revert_print_foreground():
        """
        Sets the foreground color print() uses to be the last one from when set_print_foreground was called
        """
        # We need to go two colors back, as the last color is what we're currently on
        if len(ConsoleHelper.__last_fore_colors) > 1:
            ConsoleHelper.set_print_foreground(ConsoleHelper.__last_fore_colors[-1], False)

        # Never delete the original color
        if len(ConsoleHelper.__last_fore_colors) > 1:
            del ConsoleHelper.__last_fore_colors[-1]
