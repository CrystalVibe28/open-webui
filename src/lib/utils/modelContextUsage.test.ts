import { describe, expect, it } from 'vitest';

import {
	countToolUsageItems,
	findLatestModelContextUsage,
	formatCompactTokenCount,
	getLatestInputTokens
} from './modelContextUsage';

describe('model context usage', () => {
	it('formats token counts with at most three significant digits', () => {
		expect(
			[999, 1000, 1050, 126_000, 256_000, 999_499, 999_500, 1_000_000, 1_049_000, 1e9, 1e15].map(
				formatCompactTokenCount
			)
		).toEqual(['999', '1k', '1.05k', '126k', '256k', '999k', '1m', '1m', '1.05m', '1b', '1q']);
		expect(formatCompactTokenCount(Number.NaN)).toBe('0');
		expect(formatCompactTokenCount(-1)).toBe('0');
	});

	it('prefers the latest provider invocation alias over cumulative input tokens', () => {
		expect(getLatestInputTokens({ prompt_tokens: 126_000, input_tokens: 250_000 })).toBe(126_000);
		expect(getLatestInputTokens({ input_tokens: 256_000 })).toBe(256_000);
		expect(getLatestInputTokens({ input_tokens: Number.POSITIVE_INFINITY })).toBeNull();
		expect(getLatestInputTokens({ input_tokens: 1.5 })).toBeNull();
	});

	it('detects tool activity and hydrates only a matching completed provider response', () => {
		expect(
			countToolUsageItems([
				{ type: 'reasoning' },
				{ type: 'function_call' },
				{ type: 'function_call_output' }
			])
		).toBe(2);
		expect(
			findLatestModelContextUsage(
				[
					{ role: 'assistant', model: 'a', done: true, usage: { input_tokens: 100 } },
					{ role: 'assistant', model: 'a', done: false, usage: { input_tokens: 200 } },
					{ role: 'assistant', model: 'b', done: true, usage: { input_tokens: 300 } }
				],
				'a'
			)
		).toEqual({ modelId: 'a', inputTokens: 100 });
		expect(
			findLatestModelContextUsage(
				[
					{
						role: 'assistant',
						model: 'a',
						done: true,
						error: { content: 'new continuation failed' },
						info: { modelContextUsage: { modelId: 'a', inputTokens: 400 } },
						usage: { input_tokens: 500 }
					}
				],
				'a'
			)
		).toEqual({ modelId: 'a', inputTokens: 400 });
		expect(
			findLatestModelContextUsage(
				[
					{
						role: 'assistant',
						model: 'a',
						done: true,
						meta: { model_context_usage: { model_id: 'a', input_tokens: 600 } }
					}
				],
				'a'
			)
		).toEqual({ modelId: 'a', inputTokens: 600 });
		expect(
			findLatestModelContextUsage(
				[
					{
						role: 'assistant',
						model: 'arena',
						selectedModelId: 'a',
						arena: true,
						done: true,
						info: { modelContextUsage: { modelId: 'a', inputTokens: 700 } },
						usage: { input_tokens: 700 }
					}
				],
				'a'
			)
		).toBeNull();
	});
});
