from copy import deepcopy
import json
import requests
from typing import Tuple

from utils import DEFAULT_PLAYER_SET, get_rank_translation


class GameNotStartedError(Exception):
    pass


class PawnCounter:

    def __init__(self, player_hash: str):

        # player_0 is the one how has initialized a game - sent a link
        # player_1 is the other one who has joined
        self.player_0_set = DEFAULT_PLAYER_SET.copy()
        self.player_1_set = DEFAULT_PLAYER_SET.copy()

        self.player_hash = player_hash
        self.last_essential_data = ""


    def get_player_number(self):
        """
        From request gets player number (0 or 1)
        """
        request_text = self.get_data(self.player_hash)
        player_number = request_text["side"]

        return player_number


    def get_players_sets(self)-> Tuple[dict, dict]:
        """
        Returns updated players' pawn sets.
        """
        self.update()

        return self.player_0_set, self.player_1_set


    def update(self) -> None:
        """
        Depending on type of the move updates players' pawn sets.
        """

        try:
            essential_data = self.get_move_info_from_request()
        except GameNotStartedError:
            return

        if self.last_essential_data == essential_data:
            # pass if got request is about move that have been taken into consideration before
            pass

        elif essential_data["type"] == "move":
            # pass if it was only change of location without losses
            pass

        else:
            rv = deepcopy(essential_data)
            self.translate_data(rv)
            losses = self.interpret_battle(rv)
            self.update_pawns_after_battle(losses)

        self.last_essential_data = essential_data


    def get_data(self, player_hash) -> dict:
        """
        Gets data and returns dictionary with entire request.
        """
        url = f"https://www.stratego.io/api/game?player_hash={player_hash}"
        get_request = requests.get(url)
        get_request_text = json.loads(get_request.text)

        return get_request_text


    def get_move_info_from_request(self):
        """
        From request gets info about move or raises 'GameNotStartedError' if game hasn't started yet.
        """
        request_text = self.get_data(self.player_hash)

        if "last_move" not in request_text.keys():
            raise GameNotStartedError()

        return request_text["last_move"]


    def translate_data(self, pawn_data: dict) -> None:
        """
        Takes dictionary containing data about last move and converts string-written ranks into integers.
        """
        from_rank = pawn_data["from"]["piece"]["rank"]
        pawn_data["from"]["piece"]["rank"] = get_rank_translation(from_rank)

        to_rank = pawn_data["to"]["piece"]["rank"]
        pawn_data["to"]["piece"]["rank"] = get_rank_translation(to_rank)


    def interpret_battle(self, battle: dict) -> list:
        """
        Takes data about move. Returns list of tuples (tuple: (player, lost_rank)) with losses.
        """
        if battle["type"] == "won" or battle["type"] == "lost" or battle["type"] == "capture":
            losses = self.get_battle_losses(battle)
            return losses

        elif battle["type"] == "draw":
            rank = battle["from"]["piece"]["rank"]
            return [(0, rank), (1, rank)]


    def get_battle_losses(self, won_battle: dict) -> list:
        """
        Takes data about battle with winner (not draw).
        Returns list with tuple with info about player who lost: (player, lost_rank).
        """

        pawns_ranks_in_battle = [won_battle["from"]["piece"]["rank"], won_battle["to"]["piece"]["rank"]]

        # special battles
        if won_battle["from"]["piece"]["rank"] == 1 and won_battle["to"]["piece"]["rank"] == 10:
            # spy (1) vs 10 -> loser: 10
            loser_side = won_battle["to"]["piece"]["side"]
            loser_rank = 10
        elif won_battle["from"]["piece"]["rank"] == 3 and won_battle["to"]["piece"]["rank"] == 50:
            # sapper (3) vs bomb (50) -> loser: bomb (50)
            loser_side = won_battle["to"]["piece"]["side"]
            loser_rank = 50

        # typical battles
        else:
            # loser: smaller rank
            loser_rank = min(pawns_ranks_in_battle)
            if won_battle["from"]["piece"]["rank"] == loser_rank:
                loser_side = won_battle["from"]["piece"]["side"]
            else:
                loser_side = won_battle["to"]["piece"]["side"]

        return [(loser_side, loser_rank)]


    def update_pawns_after_battle(self, losses: list) -> None:
        """
        Takes losses and changes players' sets so they're valid
        """

        for lost in losses:
            if lost[0] == 0:
                self.player_0_set[lost[1]] -= 1
            elif lost[0] == 1:
                self.player_1_set[lost[1]] -= 1
