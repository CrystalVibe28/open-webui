import inspect
import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
sys.modules.setdefault('mimeparse', types.ModuleType('mimeparse'))

env_module = types.ModuleType('open_webui.env')
env_module.CHAT_STREAM_RESPONSE_CHUNK_MAX_BUFFER_SIZE = 0
sys.modules.setdefault('open_webui.env', env_module)


def _message_item(text: str) -> dict:
    return {
        'type': 'message',
        'content': [{'type': 'output_text', 'text': text}],
    }


def _reasoning_item(text: str) -> dict:
    return {
        'type': 'reasoning',
        'summary': [{'type': 'output_text', 'text': text}],
        'start_tag': '<think>',
        'end_tag': '</think>',
    }


def _function_call_item() -> dict:
    return {
        'type': 'function_call',
        'call_id': 'call_1',
        'name': 'lookup_weather',
        'arguments': '{"city":"Taipei"}',
    }


def _function_call_output_item() -> dict:
    return {
        'type': 'function_call_output',
        'call_id': 'call_1',
        'output': [{'type': 'input_text', 'text': 'Sunny'}],
    }


def _convert(output: list[dict], *, raw: bool = True, preserve_reasoning_content: bool = False) -> list[dict]:
    from open_webui.utils.misc import convert_output_to_messages

    signature = inspect.signature(convert_output_to_messages)
    if 'preserve_reasoning_content' in signature.parameters:
        return convert_output_to_messages(
            output,
            raw=raw,
            preserve_reasoning_content=preserve_reasoning_content,
        )
    return convert_output_to_messages(output, raw=raw)


def test_default_does_not_emit_top_level_reasoning_content() -> None:
    output = [
        _reasoning_item('Need tool context'),
        _function_call_item(),
        _function_call_output_item(),
    ]

    messages = _convert(output, raw=True)

    assert messages == [
        {
            'role': 'assistant',
            'content': '<think>Need tool context</think>',
            'tool_calls': [
                {
                    'id': 'call_1',
                    'type': 'function',
                    'function': {
                        'name': 'lookup_weather',
                        'arguments': '{"city":"Taipei"}',
                    },
                }
            ],
        },
        {
            'role': 'tool',
            'tool_call_id': 'call_1',
            'content': 'Sunny',
        },
    ]


def test_enabled_emits_reasoning_content_only_on_assistant_message_with_tool_calls() -> None:
    output = [
        _reasoning_item('Need tool context'),
        _function_call_item(),
        _function_call_output_item(),
        _message_item('The weather is sunny.'),
    ]

    messages = _convert(output, raw=True, preserve_reasoning_content=True)

    assert messages == [
        {
            'role': 'assistant',
            'content': '',
            'reasoning_content': 'Need tool context',
            'tool_calls': [
                {
                    'id': 'call_1',
                    'type': 'function',
                    'function': {
                        'name': 'lookup_weather',
                        'arguments': '{"city":"Taipei"}',
                    },
                }
            ],
        },
        {
            'role': 'tool',
            'tool_call_id': 'call_1',
            'content': 'Sunny',
        },
        {
            'role': 'assistant',
            'content': 'The weather is sunny.',
        },
    ]


def test_enabled_omits_reasoning_content_for_empty_or_whitespace_reasoning() -> None:
    output = [
        _reasoning_item(' \n\t '),
        _function_call_item(),
        _function_call_output_item(),
    ]

    messages = _convert(output, raw=True, preserve_reasoning_content=True)

    assert messages == [
        {
            'role': 'assistant',
            'content': '',
            'tool_calls': [
                {
                    'id': 'call_1',
                    'type': 'function',
                    'function': {
                        'name': 'lookup_weather',
                        'arguments': '{"city":"Taipei"}',
                    },
                }
            ],
        },
        {
            'role': 'tool',
            'tool_call_id': 'call_1',
            'content': 'Sunny',
        },
    ]


def test_enabled_omits_reasoning_content_when_no_tool_call_exists() -> None:
    output = [
        _reasoning_item('Background thinking'),
        _message_item('Final answer without tools.'),
    ]

    messages = _convert(output, raw=True, preserve_reasoning_content=True)

    assert messages == [
        {
            'role': 'assistant',
            'content': '<think>Background thinking</think>\nFinal answer without tools.',
        }
    ]


def test_enabled_does_not_duplicate_reasoning_in_content_and_reasoning_content() -> None:
    output = [
        _message_item('Checking the latest weather.'),
        _reasoning_item('Need tool context'),
        _function_call_item(),
        _function_call_output_item(),
    ]

    messages = _convert(output, raw=True, preserve_reasoning_content=True)

    assert messages == [
        {
            'role': 'assistant',
            'content': 'Checking the latest weather.',
            'reasoning_content': 'Need tool context',
            'tool_calls': [
                {
                    'id': 'call_1',
                    'type': 'function',
                    'function': {
                        'name': 'lookup_weather',
                        'arguments': '{"city":"Taipei"}',
                    },
                }
            ],
        },
        {
            'role': 'tool',
            'tool_call_id': 'call_1',
            'content': 'Sunny',
        },
    ]
