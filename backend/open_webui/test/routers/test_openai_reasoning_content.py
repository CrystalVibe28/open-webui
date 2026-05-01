import ast
import copy
import inspect
import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
sys.modules.setdefault('mimeparse', types.ModuleType('mimeparse'))

env_module = types.ModuleType('open_webui.env')
env_module.CHAT_STREAM_RESPONSE_CHUNK_MAX_BUFFER_SIZE = 0
sys.modules.setdefault('open_webui.env', env_module)


BACKEND_ROOT = Path(__file__).resolve().parents[3]
OPENAI_ROUTER_PATH = BACKEND_ROOT / 'open_webui' / 'routers' / 'openai.py'


def _load_openai_router_symbols() -> tuple[dict[str, set[str]], object, object]:
    module = ast.parse(OPENAI_ROUTER_PATH.read_text(encoding='utf-8'))

    selected_nodes = []
    for node in module.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == 'RESPONSES_ALLOWED_FIELDS':
                selected_nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in {
            '_normalize_stored_item',
            'convert_to_responses_payload',
        }:
            selected_nodes.append(node)

    compiled_module = ast.Module(body=selected_nodes, type_ignores=[])
    ast.fix_missing_locations(compiled_module)

    namespace: dict[str, object] = {}
    exec(compile(compiled_module, str(OPENAI_ROUTER_PATH), 'exec'), namespace)
    return (
        namespace['RESPONSES_ALLOWED_FIELDS'],
        namespace['_normalize_stored_item'],
        namespace['convert_to_responses_payload'],
    )


def _convert_output_to_messages(
    output: list[dict], *, raw: bool = True, preserve_reasoning_content: bool = False
) -> list[dict]:
    from open_webui.utils.misc import convert_output_to_messages

    signature = inspect.signature(convert_output_to_messages)
    if 'preserve_reasoning_content' in signature.parameters:
        return convert_output_to_messages(
            output,
            raw=raw,
            preserve_reasoning_content=preserve_reasoning_content,
        )
    return convert_output_to_messages(output, raw=raw)


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


def _find_key_paths(value: object, target_key: str, path: str = 'root') -> list[str]:
    paths = []

    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f'{path}.{key}'
            if key == target_key:
                paths.append(next_path)
            paths.extend(_find_key_paths(item, target_key, next_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            paths.extend(_find_key_paths(item, target_key, f'{path}[{index}]'))

    return paths


def test_default_chat_replay_emits_no_top_level_reasoning_content() -> None:
    output = [
        _reasoning_item('Need tool context'),
        _function_call_item(),
        _function_call_output_item(),
    ]

    messages = _convert_output_to_messages(output, raw=True)

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


def test_enabled_chat_replay_only_adds_reasoning_content_to_assistant_tool_call_message() -> None:
    output = [
        _message_item('Checking the latest weather.'),
        _reasoning_item('Need tool context'),
        _function_call_item(),
        _function_call_output_item(),
        _message_item('The weather is sunny.'),
    ]

    messages = _convert_output_to_messages(output, raw=True, preserve_reasoning_content=True)

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
        {
            'role': 'assistant',
            'content': 'The weather is sunny.',
        },
    ]


def test_convert_to_responses_payload_recursively_strips_chat_reasoning_content() -> None:
    _, _, convert_to_responses_payload = _load_openai_router_symbols()

    payload = {
        'model': 'gpt-4.1-mini',
        'messages': [
            {'role': 'system', 'content': 'Be precise.'},
            {'role': 'user', 'content': 'What is the weather in Taipei?'},
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
        ],
    }

    converted = convert_to_responses_payload(copy.deepcopy(payload))

    assert converted == {
        'model': 'gpt-4.1-mini',
        'input': [
            {
                'type': 'message',
                'role': 'user',
                'content': [{'type': 'input_text', 'text': 'What is the weather in Taipei?'}],
            },
            {
                'type': 'message',
                'role': 'assistant',
                'content': [{'type': 'output_text', 'text': 'Checking the latest weather.'}],
            },
            {
                'type': 'function_call',
                'call_id': 'call_1',
                'name': 'lookup_weather',
                'arguments': '{"city":"Taipei"}',
            },
            {
                'type': 'function_call_output',
                'call_id': 'call_1',
                'output': 'Sunny',
            },
        ],
        'instructions': 'Be precise.',
    }
    assert _find_key_paths(converted, 'reasoning_content') == []
