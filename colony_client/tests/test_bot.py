from colony_client.bot import Bot

def test_bot_get_balance() -> None:
    testBot = Bot(1, 100)
    assert testBot.getBalance() == 100

def test_bot_set_balance() -> None:
    testBot = Bot(1, 100)
    testBot.setBalance(testBot.getBalance() + 100)
    assert testBot.getBalance() == 200