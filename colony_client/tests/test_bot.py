from colony_client.bot import Bot

def test_bot_get_balance() -> None:
    testBot = Bot(1, 100)
    assert testBot.getBalance() == 100

def test_bot_set_balance() -> None:
    testBot = Bot(1, 100)
    testBot.setBalance(testBot.getBalance() + 100)
    assert testBot.getBalance() == 200

def test_bot_update_coin_request() -> None:
    testBot = Bot(1, 100)
    
def test_bot_get_coin_balance() -> None:
    testBot = Bot(1, 100)
    testBot.investInCoin()
    assert testBot.getCoinBalance() == testBot._coinBalance 

def test_bot_set_all_coin() -> None:
    testBot = Bot(1, 100)
    testBot.investInCoin()
    testBot.setAllCoin()
    assert testBot._coinBalance == 0 and testBot._balance != 0



