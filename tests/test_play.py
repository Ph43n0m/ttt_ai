import unittest

from ttt_ai.play import Play


class TestPlayWinRate(unittest.TestCase):
    def test_get_win_rate(self):
        play = Play()
        play.games_won = 0
        play.game_count = 0
        print("Testing win rate with no games played.")
        self.assertEqual(
            play._get_win_rate(),
            0.0,
            "Win rate should be 0.0 when no games are played.",
        )
        for rounds in range(1, 11):
            for wins in range(0, rounds + 1):
                play.games_won = wins
                play.game_count = rounds
                expected_rate = wins / rounds
                print(
                    f"Testing win rate for {wins} wins out of {rounds} games: {expected_rate:.2f}"
                )
                self.assertEqual(play._get_win_rate(), expected_rate)
        play.games_won = 0
        play.game_count = 7
        print("Testing win rate with no game played.")
        self.assertEqual(play._get_win_rate(), 0.0)
        play.games_won = -1
        play.game_count = 10
        print("Testing win rate with negative games_won.")
        self.assertEqual(play._get_win_rate(), 0.0)
        play.games_won = 5
        play.game_count = -10
        print("Testing win rate with negative game_count.")
        self.assertEqual(play._get_win_rate(), 0.0)
        play.games_won = -3
        play.game_count = -7
        print("Testing win rate with both negative games_won and game_count.")
        self.assertEqual(play._get_win_rate(), 0.0)


class TestPlayWinLossRatio(unittest.TestCase):
    def test_get_wl_ratio(self):
        play = Play()
        play.games_won = 0
        play.games_lost = 0
        print("Testing win/loss ratio with no games played.")
        self.assertEqual(play._get_wl_ratio(), 0.0)
        play.games_won = 5
        play.games_lost = 0
        print("Testing win/loss ratio with 5 wins and 0 losses.")
        self.assertEqual(play._get_wl_ratio(), 5.0)
        play.games_won = 0
        play.games_lost = 3
        print("Testing win/loss ratio with 0 wins and 3 losses.")
        self.assertEqual(play._get_wl_ratio(), 0.0)
        for loses in range(0, 11):
            for wins in range(0, loses * 2 + 1):
                play.games_won = wins
                play.games_lost = loses
                expected_ratio = wins / loses if loses > 0 else float(wins)
                print(
                    f"Testing win/loss ratio for {wins} wins and {loses} losses: {expected_ratio:.2f}"
                )
                self.assertEqual(play._get_wl_ratio(), expected_ratio)
        play.games_won = -2
        play.games_lost = 4
        print("Testing win/loss ratio with -2 wins and 4 losses.")
        self.assertEqual(play._get_wl_ratio(), 0.0)
        play.games_won = 4
        play.games_lost = -2
        print("Testing win/loss ratio with 4 wins and -2 losses.")
        self.assertEqual(play._get_wl_ratio(), 0.0)
        play.games_won = -2
        play.games_lost = -2
        print("Testing win/loss ratio with -2 wins and -2 losses.")
        self.assertEqual(play._get_wl_ratio(), 0.0)


if __name__ == "__main__":
    unittest.main()
