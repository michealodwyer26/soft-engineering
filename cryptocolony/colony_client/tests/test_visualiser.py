from colony_client.visualiser import Visualiser

def test_initialise_visulaiser():
    test_vis = Visualiser(100)
    assert len(test_vis.bots) == 0


def test_renderText_visualiser():
    test_vis = Visualiser.renderText(1, 34, 34)
    assert len(test_vis.bots) == 0

def test_update_bot_data():
    test_vis = Visualiser.updateBotData(100)
    assert len(test_vis.bots) == 0


def test_add_bot_visualiser():
    test_vis = Visualiser.addBot()
    assert len(test_vis.bots) == 0


def test_run_visualiser():
    test_vis = Visualiser.run
    assert len(test_vis.bots) == 0
