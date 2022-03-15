from PyQt5.QtCore import pyqtSignal, QObject

from time import sleep

from pawnCounter import PawnCounter


class Worker(QObject):
    """
    Connects the PawnCounter and GUI application by getting information
    from the PawnCounter and then emitting a signal to the App.
    """
    progress = pyqtSignal(tuple)

    def __init__(self, player_hash: str):
        super(Worker, self).__init__()
        self.pawn_counter = PawnCounter(player_hash)
        self.player_number = self.pawn_counter.get_player_number()


    def run(self) -> None:

        last_pl_0_set = None
        last_pl_1_set = None

        while True:

            pl_0_set, pl_1_set = self.pawn_counter.get_players_sets()

            if pl_0_set != last_pl_0_set or pl_1_set != last_pl_1_set:
                # check if sets differ from the last ones, to not emit them to App unnecessarily

                # depending on player_number emit pl_0_set firstly and pl_1_set then or conversely
                # so the app gets the user's set firstly and the opponent's set then
                if self.player_number == 0:
                    self.progress.emit((pl_0_set, pl_1_set))

                elif self.player_number == 1:
                    self.progress.emit((pl_1_set, pl_0_set))

                last_pl_0_set = pl_0_set.copy()
                last_pl_1_set = pl_1_set.copy()

            sleep(1)
