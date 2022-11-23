from colony_client.core_controller import CoreController


def test_create_core_controller() -> None:
    coreController = CoreController("testcreatecore")
    assert coreController.currentBotId == 0


def test_create_core_controller_bot() -> None:
    coreController = CoreController("testcreatecorebot")
    coreController.createBot(100)
    assert len(coreController.bots) == 1


def test_delete_core_controller_bot() -> None:
    coreController = CoreController("testdeletecorebot")
    coreController.createBot(100)
    coreController.deleteBot(coreController.bots[-1])
    assert len(coreController.bots) == 0


def test_notify_sentiment_controller() -> None:
    coreController = CoreController("testnotifysentiment")
    coreController.notifySentimentController()
    assert len(coreController.bots) == 0
