import pytest
from app.agent import ask

def test_ask(mocker):
    mocker.patch('app.agent.client.models.generate_content')
    ask("Hello")
