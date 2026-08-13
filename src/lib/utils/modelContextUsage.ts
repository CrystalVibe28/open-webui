export type ModelContextUsage = {
	modelId: string;
	inputTokens: number;
};

type ModelContextUsageMessage = {
	role?: string;
	done?: boolean;
	error?: unknown;
	arena?: boolean;
	selectedModelId?: string;
	model?: string;
	usage?: Record<string, unknown>;
	info?: {
		usage?: Record<string, unknown>;
		modelContextUsage?: ModelContextUsage;
	};
	meta?: {
		model_context_usage?: {
			model_id?: unknown;
			input_tokens?: unknown;
		};
	};
};

const TOKEN_UNITS = ['', 'k', 'm', 'b', 't', 'q'];
const TOOL_OUTPUT_TYPES = new Set([
	'function_call',
	'function_call_output',
	'open_webui:code_interpreter',
	'web_search_call',
	'file_search_call',
	'computer_call'
]);

export const formatCompactTokenCount = (tokens: number) => {
	if (!Number.isFinite(tokens) || tokens <= 0) return '0';

	let value = Math.round(tokens);
	let unit = 0;
	while (value >= 1000 && unit < TOKEN_UNITS.length - 1) {
		value /= 1000;
		unit += 1;
	}

	value = Number(value.toPrecision(3));
	if (value >= 1000 && unit < TOKEN_UNITS.length - 1) {
		value /= 1000;
		unit += 1;
	}

	return `${value}${TOKEN_UNITS[unit]}`;
};

export const getLatestInputTokens = (usage: Record<string, unknown> | null | undefined) => {
	for (const key of ['prompt_tokens', 'input_tokens', 'prompt_eval_count', 'prompt_n']) {
		const value = usage?.[key];
		if (typeof value === 'number' && Number.isSafeInteger(value) && value > 0) {
			return value;
		}
	}
	return null;
};

export const countToolUsageItems = (output: unknown) =>
	Array.isArray(output)
		? output.filter(
				(item) =>
					typeof item === 'object' &&
					item !== null &&
					'type' in item &&
					typeof item.type === 'string' &&
					TOOL_OUTPUT_TYPES.has(item.type)
			).length
		: 0;

export const findLatestModelContextUsage = (
	messages: ModelContextUsageMessage[],
	modelId: string
): ModelContextUsage | null => {
	for (let idx = messages.length - 1; idx >= 0; idx -= 1) {
		const message = messages[idx];
		const storedCheckpoint = message?.meta?.model_context_usage;
		const checkpoint =
			message.info?.modelContextUsage ??
			(typeof storedCheckpoint?.model_id === 'string' &&
			typeof storedCheckpoint.input_tokens === 'number'
				? {
						modelId: storedCheckpoint.model_id,
						inputTokens: storedCheckpoint.input_tokens
					}
				: null);
		if (
			message?.role === 'assistant' &&
			!message?.selectedModelId &&
			!message?.arena &&
			checkpoint?.modelId === modelId &&
			Number.isSafeInteger(checkpoint?.inputTokens) &&
			checkpoint.inputTokens > 0
		) {
			return checkpoint;
		}

		if (
			message?.role !== 'assistant' ||
			message?.done === false ||
			message?.error ||
			message?.selectedModelId ||
			message?.arena ||
			message?.model !== modelId
		) {
			continue;
		}

		const inputTokens = getLatestInputTokens(message?.usage ?? message?.info?.usage);
		if (inputTokens) return { modelId, inputTokens };
	}
	return null;
};
