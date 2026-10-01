import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_duplicate_account_rejected(self):
        state = core.new_game()
        self.assertTrue(core.open_account(state, "a"))
        self.assertFalse(core.open_account(state, "a"))

    def test_02_negative_deposit_rejected(self):
        state = core.new_game()
        core.open_account(state, "a")
        self.assertFalse(core.deposit(state, "a", -5))

    def test_03_overdraft_rejected(self):
        state = core.new_game()
        core.open_account(state, "a")
        core.deposit(state, "a", 10)
        self.assertFalse(core.withdraw(state, "a", 20))

    def test_04_insufficient_transfer_no_change(self):
        state = core.new_game()
        core.open_account(state, "a")
        core.open_account(state, "b")
        core.deposit(state, "a", 5)
        core.transfer(state, "a", "b", 10)
        self.assertEqual(core.balance(state, "a"), 5)

    def test_05_transfer_credits_destination(self):
        state = core.new_game()
        core.open_account(state, "a")
        core.open_account(state, "b")
        core.deposit(state, "a", 10)
        core.transfer(state, "a", "b", 5)
        self.assertEqual(core.balance(state, "b"), 5)

    def test_06_missing_balance_zero(self):
        state = core.new_game()
        self.assertEqual(core.balance(state, "missing"), 0)

    def test_07_closed_blocks_deposit(self):
        state = core.new_game()
        core.open_account(state, "a")
        core.close(state, "a")
        self.assertFalse(core.deposit(state, "a", 5))

    def test_08_statement_scoped(self):
        state = core.new_game()
        core.open_account(state, "a")
        core.open_account(state, "b")
        core.deposit(state, "a", 5)
        core.deposit(state, "b", 7)
        rows = core.statement(state, "a")
        self.assertTrue(all(row[0] == "a" for row in rows))

    def test_09_negative_transfer_rejected(self):
        state = core.new_game()
        core.open_account(state, "a")
        core.open_account(state, "b")
        core.deposit(state, "a", 10)
        self.assertFalse(core.transfer(state, "a", "b", -3))

    def test_10_load_preserves_id(self):
        state = core.new_game()
        state["next_id"] = 9
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["next_id"], 9)


if __name__ == "__main__":
    unittest.main()
