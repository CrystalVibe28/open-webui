import { describe, expect, it } from 'vitest';

import {
	countToolUsageItems,
	findLatestModelContextUsage,
	formatCompactTokenCount,
	getLatestInputTokens,
	getLatestOutputTokens,
	getModelContextUsedTokens
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
		).toEqual({ modelId: 'a', inputTokens: 100, outputTokens: 0 });
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
		).toEqual({ modelId: 'a', inputTokens: 600, outputTokens: 0 });
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

	it('counts the latest input and output without adding cumulative tool usage or reasoning twice', () => {
		const checkpoint = findLatestModelContextUsage(
			[
				{
					role: 'assistant',
					model: 'a',
					done: true,
					usage: {
						prompt_tokens: 100_000,
						completion_tokens: 5_000,
						input_tokens: 250_000,
						output_tokens: 15_000,
						total_tokens: 265_000,
						completion_tokens_details: { reasoning_tokens: 2_000 }
					}
				}
			],
			'a'
		);
		expect(getModelContextUsedTokens(checkpoint)).toBe(105_000);
		expect(getLatestOutputTokens({ completion_tokens: 0, output_tokens: 15_000 })).toBe(0);
	});

	it('supports provider output formats and ignores invalid or missing output', () => {
		for (const key of ['completion_tokens', 'output_tokens', 'eval_count', 'predicted_n']) {
			expect(getLatestOutputTokens({ [key]: 50 })).toBe(50);
			for (const value of [-1, 1.5, Infinity, NaN, '50', true]) {
				expect(getLatestOutputTokens({ [key]: value })).toBe(0);
			}
		}
		expect(getModelContextUsedTokens({ modelId: 'a', inputTokens: 100 })).toBe(100);
		expect(getModelContextUsedTokens(null)).toBe(0);
	});

	it('restores the saved output checkpoint even after a failed continuation', () => {
		const checkpoint = findLatestModelContextUsage(
			[
				{
					role: 'assistant',
					model: 'a',
					error: { content: 'failed' },
					meta: { model_context_usage: { model_id: 'a', input_tokens: 600, output_tokens: 40 } },
					usage: { input_tokens: 900, output_tokens: 100 }
				}
			],
			'a'
		);
		expect(getModelContextUsedTokens(checkpoint)).toBe(640);
	});
});
