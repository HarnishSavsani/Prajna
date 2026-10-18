import json
from typing import Any, Dict, Optional

def format_sse(data: Dict[str, Any], event: Optional[str] = None) -> str:
    msg = f"data: {json.dumps(data)}\n\n"
    if event:
        msg = f"event: {event}\n" + msg
    return msg

def packet(obj: Dict[str, Any], turn_index: int = 0) -> str:
    payload = {
        "placement": {"turn_index": turn_index},
        "obj": obj
    }
    return format_sse(payload)

def message_start_packet(msg_id: str, turn_index: int = 0) -> str:
    return packet({"type": "message_start", "id": msg_id, "content": ""}, turn_index)

def reasoning_start_packet(turn_index: int = 0) -> str:
    return packet({"type": "reasoning_start"}, turn_index)

def reasoning_delta_packet(delta: str, turn_index: int = 0) -> str:
    return packet({"type": "reasoning_delta", "reasoning": delta}, turn_index)

def reasoning_done_packet(turn_index: int = 0) -> str:
    return packet({"type": "reasoning_done"}, turn_index)

def custom_tool_start_packet(tool_name: str, turn_index: int = 0) -> str:
    return packet({"type": "custom_tool_start", "tool_name": tool_name}, turn_index)

def custom_tool_args_packet(tool_name: str, tool_args: Dict[str, Any], turn_index: int = 0) -> str:
    return packet({"type": "custom_tool_args", "tool_name": tool_name, "tool_args": tool_args}, turn_index)

def custom_tool_delta_packet(tool_name: str, data: Any, turn_index: int = 0) -> str:
    return packet({"type": "custom_tool_delta", "tool_name": tool_name, "response_type": "json", "data": data}, turn_index)

def message_delta_packet(content: str, turn_index: int = 0) -> str:
    return packet({"type": "message_delta", "content": content}, turn_index)

def citation_info_packet(citation_num: int, doc_id: str, turn_index: int = 0) -> str:
    return packet({"type": "citation_info", "citation_number": citation_num, "document_id": doc_id}, turn_index)

def message_end_packet(turn_index: int = 0) -> str:
    return packet({"type": "message_end"}, turn_index)

def section_end_packet(turn_index: int = 0) -> str:
    return packet({"type": "section_end"}, turn_index)

def stop_packet(reason: str = "finished", turn_index: int = 0) -> str:
    return packet({"type": "stop", "stop_reason": reason}, turn_index)
