import pytest
from prajna.app.agents.router import router_agent
from prajna.app.streaming.packets import message_start_packet, stop_packet

def test_router_intents():
    assert router_agent.route("who knows payments?")[0] == "who_knows"
    assert router_agent.route("what is the blast radius of auth?")[0] == "blast_radius"
    assert router_agent.route("what is the bus factor of gateway?")[0] == "bus_factor"
    assert router_agent.route("what are the most complaints?")[0] == "impact_ranking"
    assert router_agent.route("why did we make decision 2?")[0] == "decision_trace"
    assert router_agent.route("close the loop on issue 101")[0] == "draft_close_the_loop"

def test_sse_packets():
    start = message_start_packet("msg-1")
    assert "data: " in start
    assert "message_start" in start

    stop = stop_packet("finished")
    assert "data: " in stop
    assert "stop" in stop
