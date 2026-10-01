import json


def new_game():
    return {"accounts": {}, "next_id": 1, "closed": [], "audit": []}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["next_id"] += 1
    return state


def open_account(state, acct):
    state["accounts"][acct] = 0
    return True


def deposit(state, acct, amount):
    if acct in state["accounts"]:
        state["accounts"][acct] += amount
        state["audit"].append((acct, "deposit", amount))
        return True
    return False


def withdraw(state, acct, amount):
    if acct in state["accounts"]:
        state["accounts"][acct] -= amount
        state["audit"].append((acct, "withdraw", amount))
        return True
    return False


def transfer(state, src, dst, amount):
    state["accounts"][src] -= amount
    state["audit"].append((src, "transfer", amount))
    return True


def balance(state, acct):
    return state["accounts"].get(acct, -1)


def close(state, acct):
    if acct in state["accounts"]:
        if acct not in state["closed"]:
            state["closed"].append(acct)
        return True
    return False


def statement(state, acct):
    return list(state["audit"])


def main():
    print("命令: open/deposit/withdraw/transfer/balance/close/statement/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
