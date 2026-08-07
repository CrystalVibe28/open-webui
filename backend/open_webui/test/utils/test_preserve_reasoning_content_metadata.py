import ast
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[3]
MAIN_PATH = BACKEND_ROOT / 'open_webui' / 'main.py'
MIDDLEWARE_PATH = BACKEND_ROOT / 'open_webui' / 'utils' / 'middleware.py'
PAYLOAD_PATH = BACKEND_ROOT / 'open_webui' / 'utils' / 'payload.py'


def _load_function(path: Path, function_name: str):
    module = ast.parse(path.read_text(encoding='utf-8'))

    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            function_module = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(function_module)
            namespace = {}
            exec(compile(function_module, str(path), 'exec'), namespace)
            return namespace[function_name]

    raise AssertionError(f'Function {function_name} was not found in {path}')


def _keyword_names(call: ast.Call) -> dict[str, ast.AST]:
    return {keyword.arg: keyword.value for keyword in call.keywords if keyword.arg is not None}


def test_main_resolver_defaults_to_off_when_flag_is_absent() -> None:
    resolve_flag = _load_function(MAIN_PATH, '_resolve_preserve_reasoning_content')

    assert resolve_flag({}, {}) is None


def test_main_resolver_prefers_explicit_request_param() -> None:
    resolve_flag = _load_function(MAIN_PATH, '_resolve_preserve_reasoning_content')

    assert resolve_flag({'preserve_reasoning_content': True}, {'preserve_reasoning_content': False}) is True
    assert resolve_flag({'preserve_reasoning_content': False}, {'preserve_reasoning_content': True}) is False


def test_main_resolver_uses_model_param_when_request_param_is_absent() -> None:
    resolve_flag = _load_function(MAIN_PATH, '_resolve_preserve_reasoning_content')

    assert resolve_flag({}, {'preserve_reasoning_content': True}) is True


def test_main_resolver_ignores_default_model_params_merge() -> None:
    module = ast.parse(MAIN_PATH.read_text(encoding='utf-8'))

    call_nodes = [
        node
        for node in ast.walk(module)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == '_resolve_preserve_reasoning_content'
    ]

    assert len(call_nodes) == 1

    call = call_nodes[0]
    assert len(call.args) == 2
    assert isinstance(call.args[0], ast.Name)
    assert call.args[0].id == 'request_params'
    assert isinstance(call.args[1], ast.Name)
    assert call.args[1].id == 'model_own_params'
    assert call.keywords == []


def test_middleware_helper_only_enables_for_explicit_true() -> None:
    should_preserve = _load_function(MIDDLEWARE_PATH, '_should_preserve_reasoning_content')

    assert should_preserve({}) is False
    assert should_preserve({'params': {}}) is False
    assert should_preserve({'params': {'preserve_reasoning_content': False}}) is False
    assert should_preserve({'params': {'preserve_reasoning_content': True}}) is True


def test_middleware_only_adds_preserve_flag_to_tool_loop_replay_calls() -> None:
    module = ast.parse(MIDDLEWARE_PATH.read_text(encoding='utf-8'))

    raw_convert_calls = []
    for node in ast.walk(module):
        if not isinstance(node, ast.Call):
            continue

        if not isinstance(node.func, ast.Name) or node.func.id != 'convert_output_to_messages':
            continue

        keywords = _keyword_names(node)
        raw_value = keywords.get('raw')
        if isinstance(raw_value, ast.Constant) and raw_value.value is True:
            raw_convert_calls.append(node)

    assert len(raw_convert_calls) == 4

    calls_with_preserve_flag = []
    calls_without_preserve_flag = []

    for call in raw_convert_calls:
        keywords = _keyword_names(call)
        preserve_value = keywords.get('preserve_reasoning_content')
        if preserve_value is None:
            calls_without_preserve_flag.append(call)
            continue

        assert isinstance(preserve_value, ast.Call)
        assert isinstance(preserve_value.func, ast.Name)
        assert preserve_value.func.id == '_should_preserve_reasoning_content'
        assert len(preserve_value.args) == 1
        assert isinstance(preserve_value.args[0], ast.Name)
        assert preserve_value.args[0].id == 'metadata'
        calls_with_preserve_flag.append(call)

    assert len(calls_with_preserve_flag) == 3
    assert len(calls_without_preserve_flag) == 1


def test_remove_open_webui_params_filters_preserve_reasoning_content() -> None:
    remove_open_webui_params = _load_function(PAYLOAD_PATH, 'remove_open_webui_params')

    params = {
        'preserve_reasoning_content': True,
        'temperature': 0.2,
    }

    assert remove_open_webui_params(params) == {'temperature': 0.2}


def test_apply_params_to_form_data_filters_preserve_reasoning_content_from_provider_payload() -> None:
    apply_params_to_form_data = _load_function(MIDDLEWARE_PATH, 'apply_params_to_form_data')

    form_data = {
        'params': {
            'preserve_reasoning_content': True,
            'temperature': 0.2,
        }
    }

    result = apply_params_to_form_data(form_data, {'owned_by': 'openai'})

    assert result == {'temperature': 0.2}
