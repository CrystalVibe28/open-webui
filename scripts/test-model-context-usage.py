"""Run with Python's standard library; no application/database startup required."""

import ast
import math
import unittest
from numbers import Number
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_usage_functions():
    # Isolate the pure functions from modules whose imports initialize the application.
    namespace = {'math': math, 'Number': Number}
    names = {
        'normalize_usage', 'merge_usage', '_is_numeric_usage_value', '_merge_numeric_usage_map',
        'USAGE_TOKEN_KEYS', 'USAGE_COST_KEYS', 'USAGE_SUMMABLE_KEYS', 'USAGE_DETAIL_KEYS',
        'get_model_context_usage_checkpoint',
    }
    for filename in ('response.py', 'middleware.py'):
        path = ROOT / 'backend/open_webui/utils' / filename
        tree = ast.parse(path.read_text(encoding='utf-8'))
        tree.body = [
            node for node in tree.body
            if (isinstance(node, ast.FunctionDef) and node.name in names)
            or (isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id in names for target in node.targets
            ))
        ]
        exec(compile(tree, str(path), 'exec'), namespace)
    return namespace['merge_usage'], namespace['get_model_context_usage_checkpoint']


merge_usage, checkpoint = load_usage_functions()


class ModelContextUsageTests(unittest.TestCase):
    def test_latest_invocation_not_cumulative_tool_usage(self):
        for input_key, output_key in (
            ('prompt_tokens', 'completion_tokens'),
            ('input_tokens', 'output_tokens'),
            ('prompt_eval_count', 'eval_count'),
            ('prompt_n', 'predicted_n'),
        ):
            with self.subTest(provider=input_key):
                usage = merge_usage(None, {input_key: 100, output_key: 20})
                usage = merge_usage(usage, {input_key: 150, output_key: 30})
                self.assertEqual(usage['total_tokens'], 300)
                self.assertEqual(checkpoint(usage, 'a'), {
                    'model_id': 'a', 'input_tokens': 150, 'output_tokens': 30,
                })
                usage = merge_usage(usage, {input_key: 200, output_key: 0})
                self.assertEqual(checkpoint(usage, 'a')['output_tokens'], 0)

    def test_missing_and_invalid_output(self):
        for value in (None, True, -1, 1.5, math.inf, math.nan, '50', 2**53):
            with self.subTest(value=value):
                self.assertEqual(checkpoint({'input_tokens': 100, 'output_tokens': value}, 'a'), {
                    'model_id': 'a', 'input_tokens': 100, 'output_tokens': 0,
                })
        self.assertEqual(checkpoint({'input_tokens': 100}, 'a')['output_tokens'], 0)
        self.assertIsNone(checkpoint({'input_tokens': 0, 'output_tokens': 50}, 'a'))

    def test_reasoning_is_already_in_output(self):
        self.assertEqual(checkpoint({
            'input_tokens': 100, 'output_tokens': 30,
            'output_tokens_details': {'reasoning_tokens': 20},
        }, 'a'), {'model_id': 'a', 'input_tokens': 100, 'output_tokens': 30})


if __name__ == '__main__':
    unittest.main()
