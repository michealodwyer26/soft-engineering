from colony_client.core_controller import CoreController


def test_create_core_controller() -> None:
    coreController = CoreController()
    assert coreController.currentBotId == 0

def test_create_core_controller_bot() -> None:
    coreController = CoreController()
    coreController.createBot(100)
    assert coreController.currentBotId == 1

def test_delete_core_controller_bot() -> None:
    coreController = CoreController()
    coreController.createBot(100)
    coreController.deleteBot(coreController.bots[-1])
    assert len(coreController.bots) == 0