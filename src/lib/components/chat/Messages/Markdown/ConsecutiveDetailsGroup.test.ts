import { render } from 'svelte/server';
import { writable } from 'svelte/store';
import { describe, expect, it, vi } from 'vitest';
import ConsecutiveDetailsGroup from './ConsecutiveDetailsGroup.svelte';
import { buildOutputDisplayItems, type OutputDetailToken } from '../structuredOutput';

vi.mock('$lib/stores', () => ({ settings: writable({}), config: writable({}) }));

function renderGroup(tokens: OutputDetailToken[], messageDone = false) {
	return render(ConsecutiveDetailsGroup, {
		props: { tokens, messageDone },
		context: new Map([['i18n', writable({ t: (key: string) => key })]])
	}).body;
}

function tool(status = 'completed', done = 'true', text = ''): OutputDetailToken {
	return { summary: '', text, attributes: { type: 'tool_calls', name: 'search', status, done } };
}

describe('consecutive detail group status', () => {
	it.each(['reasoning', 'open_webui:code_interpreter'])(
		'keeps the group active for %s after a tool returns',
		(type) => {
			const output = [
				{ type: 'function_call', call_id: 'call', name: 'search', status: 'completed' },
				{ type: 'function_call_output', call_id: 'call', output: [] },
				{ type, status: 'in_progress' }
			];
			const group = buildOutputDisplayItems(output)[0];
			if (group.type !== 'detail_group') throw new Error('Expected a detail group');
			const active = renderGroup(group.tokens);
			expect(active).toContain('Exploring');
			expect(active).toContain('spinner_ajPY');
			expect(active).not.toContain('text-emerald-500');

			output[2].status = 'completed';
			const completed = buildOutputDisplayItems(output)[0];
			if (completed.type !== 'detail_group') throw new Error('Expected a detail group');
			const settled = renderGroup(completed.tokens);
			expect(settled).toContain('Explored');
			expect(settled).not.toContain('spinner_ajPY');
			expect(settled).toContain('text-emerald-500');
			// A finished message must not revive stale reasoning as active.
			expect(renderGroup(group.tokens, true)).not.toContain('spinner_ajPY');
		}
	);

	it.each(['pending', 'in_progress', 'completed'])('preserves active tool status %s', (status) => {
		expect(renderGroup([tool(status, 'false')])).toContain('spinner_ajPY');
	});

	it.each(['rejected', 'failed'])('preserves the %s error indicator', (status) => {
		const html = renderGroup([tool(status)]);
		expect(html).toContain('text-red-');
		expect(html).not.toContain('spinner_ajPY');
		expect(html).not.toContain('text-emerald-500');
	});

	it('keeps tool-result errors visible and incomplete tools settled', () => {
		expect(renderGroup([tool('completed', 'true', 'Error: tool failed')])).toContain('text-red-');
		expect(renderGroup([tool('incomplete', 'false')])).not.toContain('spinner_ajPY');
	});
});
