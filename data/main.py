"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

from . import prepare, tools
from .states import choose_level, high_score, game, main_menu, message_screen
from .states import pause


def main():
    """
    Add states to control here.
    """
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {'CHOOSE_LEVEL': choose_level.ChooseLevel(),
                  'HIGH_SCORE': high_score.HighScore(),
                  'GAME': game.Game(),
                  'MAIN_MENU': main_menu.MainMenu(),
                  'MESSAGE_SCREEN': message_screen.MessageScreen(),
                  'PAUSE': pause.Pause(),
                  }
    run_it.setup_states(state_dict, 'MAIN_MENU')
    run_it.main()
