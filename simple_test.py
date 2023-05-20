import pytest
import time
from robotics import Robot

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

@pytest.fixture(scope='session')
def robot(): 
    robot = Robot("TestQuandrinaunt")
    yield robot

def test_simple(robot): 
    robot.get_scientists_info_from_wiki(SCIENTISTS)
    # sleep as es is eventually consistent
    time.sleep(1)
    result = robot.get_scientists_info_from_es({
            "query": {
                "match_all": {}
            }
        })
    
    result_names = set([scientist['name'] for scientist in result])
    for scientist in SCIENTISTS: 
        assert scientist in result_names