import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { parse } from 'svelte/compiler';
import { describe, expect, it, vi } from 'vitest';
import { applyResponseStreamEvent, getOutputText } from './Messages/structuredOutput';

// Execute the component's real handlers without mounting the entire chat application.
function declarations(file: string, names: string[]) {
	const source = readFileSync(new URL(file, import.meta.url), 'utf8');
	return parse(source)
		.instance!.content.body.filter(
			(node: any) =>
				node.type === 'VariableDeclaration' &&
				node.declarations.some((declaration: any) => names.includes(declaration.id.name))
		)
		.map((node: any) => source.slice(node.start, node.end))
		.join('\n');
}

const responseHandlers = declarations('./Chat.svelte', [
	'responseCompletionEventHandler',
	'shouldAutoScrollResponse',
	'scheduleResponseScrollToBottom',
	'scrollRAF'
]);

describe('response auto-scroll', () => {
	it.each([
		[true, true, 1],
		[false, true, 0],
		[true, false, 0]
	])('respects following=%s and response scrolling=%s', async (autoScroll, enabled, count) => {
		const scrollToBottom = vi.fn();
		const frames: Array<() => Promise<void>> = [];
		const message = { id: 'reply', content: '', output: [] };
		const handle = runInNewContext(`${responseHandlers}\nresponseCompletionEventHandler`, {
			autoScroll,
			$settings: { scrollOnResponseGeneration: enabled },
			history: { messages: {} },
			navigator: {},
			applyResponseStreamEvent,
			getOutputText,
			dispatchCallOverlayAudio: vi.fn(),
			scrollToBottom,
			requestAnimationFrame: (callback: () => Promise<void>) => frames.push(callback)
		});

		// Multiple chunks in one frame should update content and only schedule one scroll.
		handle({ type: 'response.output_text.delta', delta: 'Hello' }, message);
		handle({ type: 'response.output_text.delta', delta: ' world' }, message);
		expect(message.content).toBe('Hello world');
		expect(frames).toHaveLength(count);
		for (const frame of frames.splice(0)) await frame();
		expect(scrollToBottom).toHaveBeenCalledTimes(count);

		// Following must continue on subsequent frames, including reasoning updates.
		handle({ type: 'response.reasoning_text.delta', delta: 'Thinking' }, message);
		expect(frames).toHaveLength(count);
		for (const frame of frames) await frame();
		expect(scrollToBottom).toHaveBeenCalledTimes(count * 2);
	});

	it('returns to the bottom without a smooth-scroll interval that disables following', () => {
		const scrollTo = vi.fn();
		const scroll = runInNewContext(
			`${declarations('./MessageInput.svelte', ['scrollToBottom'])}\nscrollToBottom`,
			{ document: { getElementById: () => ({ scrollHeight: 2000, scrollTo }) } }
		);
		scroll();
		expect(scrollTo).toHaveBeenCalledWith({ top: 2000, behavior: 'auto' });
	});
});
