## crystalvibe28 custom patches

This repository is a personal fork of [open-webui/open-webui](https://github.com/open-webui/open-webui). The sections below list every fork-specific change so that they can be preserved (or consciously dropped) when merging upstream releases.

### Remotes and branches

- **Remotes:** `upstream` = open-webui/open-webui, `origin` = the fork (`CrystalVibe28/open-webui`).

| Branch               | Purpose                                                                                                                                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `crystalvibe28/main` | The main patch branch. It receives three things: upstream release merges, custom patch branches (`feat/*`), and `crystalvibe28/fix`. It is the deployed branch; every push builds and publishes the image (patch 5). |
| `crystalvibe28/fix`  | Small fixes: a problem that one commit can solve and that does not deserve a branch of its own. Long-lived; merged into `crystalvibe28/main` after each fix.                                                         |
| `feat/<topic>`       | One branch per custom feature or larger change. Kept after merging; follow-up work on the same patch goes on the same branch and is merged again.                                                                    |
| `crystalvibe28/dev`  | **Deprecated — do not commit to it or branch from it.** See below.                                                                                                                                                   |
| `main`, `dev`        | Local mirrors of upstream's `main` and `dev`. Never commit to them; only fast-forward them from `upstream`.                                                                                                          |

History of `crystalvibe28/dev`: it was created on 2026-08-12 together with `crystalvibe28/main`, both from upstream tag `v0.11.0`, as the integration branch. Feature branches were forked from it and merged back into it; a version bump was then committed on it, and it was merged into `crystalvibe28/main` and tagged. It was last used on 2026-08-14 (`0.11.0+crystalvibe28.2`). Since the `v0.11.1` merge, everything goes straight into `crystalvibe28/main`, and `crystalvibe28/dev` has stayed on `v0.11.0`.

### Commit conventions

- **Language:** English, for every commit message in this repository. This overrides any general preference for another language. (One early commit, `12f510687`, is in Chinese; do not follow it.)
- **Format:** [Conventional Commits](https://www.conventionalcommits.org/), subject line only, no body: `<type>(<scope>): <imperative summary in lower case>`. The scope is optional.
  - Types in use: `feat`, `fix`, `ci`, `chore`, `docs`.
  - Scopes in use: `chat`, `models`, `openai`, `pwa`, `release`, `agents`.
  - Examples: `fix(chat): restore auto-scroll for streamed responses`, `feat(models): add context window metadata setting`, `ci: rename Docker image build workflow`.
- **Version bumps:** `chore(release): bump version to <version>`.
- **Merge commits:** keep git's default subject, with no body.
  - Upstream release: `Merge tag 'vX.Y.Z' into crystalvibe28/main`
  - Custom branch: `Merge branch '<branch>' into crystalvibe28/main`
- **Always** create a merge commit (`--no-ff`). Never rebase, squash or fast-forward a merge into `crystalvibe28/main`.
- **Author:** all custom commits are authored by `CrystalVibe28`.
- Commit, push and tag only when asked. Never force-push.
- After every commit, update this file (see "Rule: keep this file in sync with every commit").

### Version convention

- The version is `<upstream version>+crystalvibe28.<N>`, for example `0.12.0+crystalvibe28.3` (patch 4).
- It is edited by hand in three places: `version` in `package.json`, and the top-level and `packages[""]` entries in `package-lock.json`.
- On an upstream merge, the upstream part follows the merged tag. `<N>` is given by the user for each merge; it stayed at `2` from `v0.11.0` to `v0.11.4` and became `3` with `v0.12.0`. Do not change `<N>` without being told.
- Release tags, when asked for, are lightweight tags named `v<version>` on the merge commit in `crystalvibe28/main` (so far `v0.11.0+crystalvibe28.1` and `v0.11.0+crystalvibe28.2`).

### Merging a custom patch branch

Applies to `feat/*` and `crystalvibe28/fix`. The target is always `crystalvibe28/main`.

1. Start the work from the current `crystalvibe28/main`:
   - a feature: create `feat/<topic>` from `crystalvibe28/main`;
   - a small fix: fast-forward `crystalvibe28/fix` to `crystalvibe28/main` first, then commit on `crystalvibe28/fix`.
2. Commit on the branch, following the commit conventions. One commit per fix.
3. Switch to `crystalvibe28/main` and merge with `git merge --no-ff <branch>`, keeping the default message.
4. If the merge conflicts, keep both sides' intent: upstream's code is the base and the patch logic is re-applied on top (same principles as an upstream merge, below). Run the tests that cover the patch before completing the merge commit.
5. Do not delete the branch.
6. Update this file.

### Merging an upstream release

Upstream is merged only when it publishes a release, by its tag (`vX.Y.Z`). Do not merge arbitrary commits of `upstream/main` or `upstream/dev`.

The work has two phases, with a stop in between whenever there are conflicts.

**Phase 1 — prepare and merge**

1. Check that the working tree is clean. Never overwrite, restore or delete existing changes. If there are uncommitted changes, stop and report.
2. Fetch from `upstream`, including tags, and fast-forward the local `main` so that it contains the release tag.
3. Switch to the local branch that tracks `crystalvibe28/main`. If the branch name or its tracking relationship is unclear, report the current branch and remote state before going further.
4. Look at the earlier upstream merge commits and reuse their message format: `Merge tag 'vX.Y.Z' into crystalvibe28/main`.
5. Merge the tag with `git merge --no-ff vX.Y.Z`. No rebase, no squash.
6. If there are no conflicts, set the version (see "Version convention"), run the checks from phase 2 step 4, complete the merge commit and report.
7. If there are conflicts:
   - Leave the repository in the conflicted state. Do not resolve anything, do not create the merge commit, and do not run `git merge --abort`.
   - List every conflicted file.
   - For each one, compare the upstream release with the fork's patch and explain the cause of the conflict, how the two implementations differ, and the proposed way to integrate them. Use the patch sections of this file to identify what the fork's side is for.
   - Stop and wait for instructions.

**Phase 2 — resolve, after the user has replied to the analysis**

1. Resolve by these principles:
   - The result must contain the upstream release in full **and** keep every fork patch.
   - Upstream's code is the base. Re-integrate the necessary patch logic on top of it.
   - Where both sides implement the same or a similar feature, build on upstream's latest implementation and behaviour. Do not keep an old implementation that upstream has replaced; port the fork's customisation onto upstream's version.
   - Never settle a conflict by taking the whole of "ours" or the whole of "theirs" when that loses an important change from either side.
   - Do not touch anything unrelated to the merge.
2. Apply the standing resolutions:
   - Version: `<new upstream version>+crystalvibe28.<N>` in all three places.
   - Workflows: keep `docker-image-build.yaml`, keep `docker.yaml` deleted, and keep the `*.disabled` workflows disabled (patch 5).
3. Make sure no conflict markers remain.
4. Run the applicable format checks, tests and build.
5. Once the result is confirmed, create the merge commit with the message from phase 1 step 4.
6. Report:
   - which conflicts were resolved, and how each was integrated;
   - how each fork patch was preserved;
   - where the version was changed;
   - the merge commit's hash and message;
   - the test and build results.
7. Update this file: re-measure line ranges, move the reference commit, and record anything upstream superseded.

### Rule: keep this file in sync with every commit

Every commit made in this fork must be reflected in this file. Do this as part of the commit task, without being asked.

**When**

- Right after each commit. The hash is only known once the commit exists, so the update follows the commit.
- Commit the update on its own as `docs(agents): <summary>`, by default on `crystalvibe28/fix`, and merge it into `crystalvibe28/main` like any other small fix. One such commit may cover all the commits of the same task. Doc-only commits are not patches and are not listed here.

**What to update**

| Kind of commit                        | Required update                                                                                                                                          |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| New fork-specific change              | Add a new numbered section at the end and a row in the Overview table.                                                                                   |
| Follow-up to an existing patch        | Update that patch's section: summary, reason, commit list, files and line ranges, status.                                                                |
| Feature or fix branch merged          | Update the patch's status and its Overview row, then re-measure its line ranges at the new `crystalvibe28/main`.                                         |
| Upstream merge (`Merge tag 'vX.Y.Z'`) | Re-measure the line ranges of every merged patch, update the reference commit in "How to read the line ranges", and record anything upstream superseded. |
| Version bump                          | Update the current value in patch 4.                                                                                                                     |
| Patch dropped, reverted or superseded | Keep the section, mark it in the status line and say why. Do not delete it.                                                                              |

**Format of a patch section** (all in English)

1. Heading: `### <N>. <topic>`.
2. `**Status:**` — required unless the patch is fully merged into `crystalvibe28/main` and intact.
3. `**What it changes**` — behaviour and mechanism: the functions, components, setting keys and endpoints involved.
4. `**Why**` — the problem that led to the change. Take it from the request that started the work; if the reason is inferred from the code, say so.
5. `**Branch:**` — the branch the work was committed on.
6. `**Commits**` — one line each: `` `<9-char hash>` (YYYY-MM-DD) `<full subject>` ``.
7. `**Files and line ranges**` — grouped per commit, with the reference commit stated. Follow "How to read the line ranges". Locale files are given as a glob plus the keys added.
8. `**Merge notes**` — what must be re-applied or re-checked after an upstream merge.

**Checks before finishing**

- Every hash listed exists: `git log -1 <hash>`.
- The Overview table and the sections agree on branch, status and commits.
- Nothing is recorded that was not actually committed.

### How to read the line ranges

- Ranges are `git blame` attributions: the lines each commit **still owns** at the reference commit named in the section. They are current locations, not the hunks at commit time, and they drift with every upstream merge.
- Patches merged into `crystalvibe28/main` are measured at `crystalvibe28/main @ 8d385a22e` (upstream base `v0.12.0`).
- Patches that are **not merged** are measured at their own branch tip, which sits on a much older upstream base, so their numbers do not match `crystalvibe28/main`.
- "merge `<hash>`" marks lines of the same patch that were re-resolved during an upstream merge and are now attributed to that merge commit.
- To measure one file: `git blame --porcelain <ref> -- <path>`, then collect the final line numbers of the lines attributed to the commit.
- To regenerate the commit list: `git log --branches --no-merges --author=CrystalVibe28 --format="%h %ad %s" --date=short`

### Overview

| #   | Patch                                  | Branch                                | In `crystalvibe28/main`      | Commits                                                                                                |
| --- | -------------------------------------- | ------------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1   | Preserve `reasoning_content` on replay | `feat/preserve-reasoning-content`     | No — obsolete, do not merge  | `12f510687`, `49ffac82e`                                                                               |
| 2   | Model context window metadata          | `feat/model-context-window`           | Yes                          | `d78a5cc29`, `685a7822e`, `6cdb1dfff`                                                                  |
| 3   | Context window usage indicator         | `feat/context-window-usage-indicator` | Yes                          | `b8b0e4e6c`, `622272b51`                                                                               |
| 4   | Fork version suffix                    | `crystalvibe28/dev`                   | Yes                          | `ac7a62d95`, `f249ab0f4`                                                                               |
| 5   | GHCR-only image build workflow         | `crystalvibe28/main`                  | Yes                          | `808e1b4d5`, `036b4d6ba`                                                                               |
| 6   | Auto-scroll for streamed responses     | `crystalvibe28/fix`                   | Yes (partly superseded)      | `04846ab3b`                                                                                            |
| 7   | Analysis group stays active            | `crystalvibe28/fix`                   | Yes (superseded by upstream) | `f82017e24`                                                                                            |
| 8   | Group-based user visibility            | `feat/group-user-visibility`          | Yes                          | `3656be046`, `dae17c8ff`, `d8be77741`, `aef77fe61`, `fdc4598d4`, `5297d1781`, `4ee44089c`, `6a03dd13d` |
| 9   | PWA app shell revalidation             | `crystalvibe28/fix`                   | Yes                          | `5b67b4292`                                                                                            |

---

### 1. Preserve `reasoning_content` on tool-call replay

**Status:** obsolete — **do not merge** `feat/preserve-reasoning-content` into `crystalvibe28/main` (decided 2026-10-12). The feature is still wanted, but the branch predates upstream's `reasoning_format` rewrite. It has to be re-implemented against the current code, with compatibility handling, before it can land. The branch is kept as a reference for the design and the tests. It was originally written as a candidate upstream PR.

**What it changes**

- Adds an opt-in, per-model param `preserve_reasoning_content` (UI shows "Default" / "On"; the frontend never writes `false`). The toggle is rendered in `AdvancedParams.svelte` only inside the model editor, for admins.
- `main.py`: `_resolve_preserve_reasoning_content(request_params, model_own_params)` resolves the flag as request param → the model's own params → off, and stores it in `metadata['params']`.
- `middleware.py`: `_should_preserve_reasoning_content(metadata)` is true only for an explicit `True`. It is passed to 3 of the 4 `convert_output_to_messages(output, raw=True)` calls in `streaming_chat_response_handler` (the tool-loop replay calls).
- `misc.py`: `convert_output_to_messages(..., preserve_reasoning_content=False)`. With the flag on, reasoning that precedes a tool call is emitted as a top-level `reasoning_content` on the assistant message that carries `tool_calls`, instead of `<think>…</think>` inside `content`. Whitespace-only reasoning is dropped. With the flag off, behaviour is unchanged.
- `49ffac82e` makes the flag internal-only: it is added to the Open WebUI-only param lists in `apply_params_to_form_data` (`middleware.py`) and `remove_open_webui_params` (`payload.py`) so it never reaches the provider, and the resolver stops inheriting it from the merged default model params. It also adds the two i18n keys and ignores `.sisyphus/`.

**Why**

- DeepSeek, Kimi and similar thinking models reject a follow-up request when thinking and native tool calling are both enabled: `The reasoning_content in the thinking mode must be passed back to the API.`
- Upstream once sent `reasoning_content` unconditionally (`3dd825581`) and removed it again (`e88e565ab`), because strict providers reject unknown fields. This patch brings it back as an explicit per-model switch.
- A review of the first commit found that the flag itself could leak into the provider payload and trigger "unknown parameter" errors on strict OpenAI-compatible providers. `49ffac82e` fixes that.
- Only Chat Completions replay is affected. The Responses API path strips `reasoning_content`.

**Branch:** `feat/preserve-reasoning-content`

**Commits**

- `12f510687` (2026-05-01) `feat(openai): 模型參數新增「保留 reasoning_content」以支援工具回放`
- `49ffac82e` (2026-08-07) `fix: isolate reasoning content preservation setting`

**Files and line ranges** (at `feat/preserve-reasoning-content @ 49ffac82e`)

`12f510687`

- `backend/open_webui/main.py`: 1733-1735, 1737-1742, 1793, 1798, 2178-2195
- `backend/open_webui/utils/middleware.py`: 2218-2221, 4793-4795, 4797-4798, 4801-4805, 4807-4808, 5028-5030, 5032-5033 (merge `25b05ea68`: 4796, 4806, 5031)
- `backend/open_webui/utils/misc.py`: 134, 140 (merge `25b05ea68`: 20-21, 137-139, 150-152, 159-160, 165-167, 171, 184, 261, 278-279)
- `src/lib/components/chat/Settings/Advanced/AdvancedParams.svelte`: 14, 22, 181-212
- `src/lib/components/workspace/Models/ModelEditor.svelte`: 723-728
- `backend/open_webui/test/utils/test_reasoning_content_replay.py`: 1-209 (new)
- `backend/open_webui/test/utils/test_preserve_reasoning_content_metadata.py`: 1-142 (new; shared with `49ffac82e`)
- `backend/open_webui/test/routers/test_openai_reasoning_content.py`: 1-278 (new; shared with `49ffac82e`)

`49ffac82e`

- `backend/open_webui/main.py`: removes the `model_info_params` argument at the call (1740) and in the signature (2181); no added lines
- `backend/open_webui/utils/middleware.py`: 2072
- `backend/open_webui/utils/payload.py`: 76
- `backend/open_webui/test/routers/test_openai_reasoning_content.py`: 6, 8, 48-71, 268-278
- `backend/open_webui/test/utils/test_preserve_reasoning_content_metadata.py`: 8, 32, 38-39, 45, 49-59, 61-67, 117-142
- `.gitignore`: 313
- `src/lib/i18n/locales/*/translation.json` (61 files): keys `Preserve Reasoning Content` and `Passes assistant reasoning_content back during native tool-call replay for compatible thinking models such as DeepSeek or Kimi. Leave disabled for providers that reject unknown fields.` The `ko-KR` file was regenerated in the same commit (238-line diff, unrelated to the feature).

**Merge notes**

- `test_middleware_only_adds_preserve_flag_to_tool_loop_replay_calls` asserts, via AST, exactly 4 `convert_output_to_messages(raw=True)` calls of which 3 pass the flag. It fails whenever upstream adds or removes such a call.
- If the entries in the two Open WebUI-only param lists are lost, the flag leaks to providers.
- State as of 2026-10-12: the branch is pushed to `origin` and sits on upstream `v0.9.5` (2026-05-10), 2,179 commits behind `crystalvibe28/main`. A trial merge into `crystalvibe28/main` conflicts in 68 files: 61 locale files plus `.gitignore`, `main.py`, `middleware.py` (4 hunks), `misc.py` (6 hunks), `payload.py`, `AdvancedParams.svelte` and `ModelEditor.svelte`.
- Upstream has since rewritten this area. `convert_output_to_messages` now takes `reasoning_format`, chosen by `get_reasoning_format(model)` in `middleware.py`: `thinking` for Ollama, `reasoning_content` when the connection's provider type is `llama.cpp`, otherwise none. On `crystalvibe28/main`, DeepSeek or Kimi behind a plain OpenAI-compatible connection therefore still get no `reasoning_content` on replay.
- Because of that rewrite, porting means re-implementing the flag on top of `reasoning_format` rather than merging the branch. The tests live under `backend/open_webui/test/`, which no longer exists on `crystalvibe28/main` (tests are in `backend/tests/`).
- Work still to do for the re-implementation:
  - Decide how the per-model flag maps onto `reasoning_format` (for example, forcing `reasoning_content` for that model) and how it interacts with the provider-type rule and with `reasoning_details`.
  - Keep the flag out of the provider payload (the two Open WebUI-only param lists).
  - Keep the Responses API path free of `reasoning_content`.
  - Re-add the toggle, the i18n keys and the tests in their current locations.

---

### 2. Model context window metadata

**What it changes**

- `d78a5cc29`: adds `ModelMeta.context_window: int | None = Field(default=None, gt=0, strict=True)` and a numeric "Context Window" input in the workspace model editor. The value lives in the model's `meta` JSON (API path `info.meta.context_window`), so there is no DB migration. It is informational: it is not sent to the provider and is not used for truncation.
- `685a7822e`: `get_upstream_context_window()` in `utils/models.py`. In `get_all_models`, a custom model without its own value inherits the first value found along its `base_model_id` chain: custom ancestors first, then the native/arena base model (exact id, then the id without the Ollama `:tag`). A `visited` set guards against cycles. The result is written only to the in-memory model list, never to the DB.
- `6cdb1dfff`: relaxes validation to `ge=0` and adds the validator `coerce_zero_context_window`, which turns `0` into `None`.

**Why**

- Upstream had no per-model context window value (only Ollama's `params.num_ctx`). The fork needs a "max input tokens" number per model as the denominator of the usage indicator (patch 3).
- Workspace models built on another model showed no value unless it was entered again; the expected behaviour was to inherit it.
- Model configs exported from Open WebUI or LiteLLM may contain `context_window: 0` meaning "not configured". Importing them failed validation.

**Branch:** `feat/model-context-window`

**Commits**

- `d78a5cc29` (2026-08-13) `feat(models): add context window metadata setting`
- `685a7822e` (2026-08-14) `feat(models): inherit context_window from upstream model chain`
- `6cdb1dfff` (2026-08-27) `fix(models): treat zero context_window as unset`

**Files and line ranges**

`d78a5cc29` (at `crystalvibe28/main @ 8d385a22e`)

- `backend/open_webui/models/models.py`: no surviving lines (the field line was rewritten by `6cdb1dfff`)
- `src/lib/apis/index.ts`: 1788
- `src/lib/components/workspace/Models/ModelEditor.svelte`: 169 (merge `cbd352c23`: 1251-1270, 1272-1273 — the Context Window input, rewritten as a row of upstream's redesigned settings grid, placed before the Tags row)
- `src/lib/i18n/locales/*/translation.json` (63 files): key `Context Window` (zh-TW: `上下文窗口`)

`685a7822e` (at `crystalvibe28/main @ 8d385a22e`)

- `backend/open_webui/utils/models.py`: 90-112, 212, 232, 243-246, 307-315

`6cdb1dfff` (at `crystalvibe28/main @ 8d385a22e`, merged by `0fb55dab3` on 2026-10-12)

- `backend/open_webui/models/models.py`: 149, 158-171

**Merge notes**

- `get_all_models` is a hot upstream function. Re-apply `custom_model_lookup`, the base-meta copy in the override branch, and the inheritance block before `model['info'] = info`.
- In the override branch of `get_all_models`, the base-meta copy sits directly after upstream's block that restores an arena model's `access_grants`, `model_ids` and `filter_mode` (`b8de508db`, `v0.12.0`). Both blocks follow `model['info'] = custom_model.model_dump()` and conflicted in the `v0.12.0` merge; keep both.
- Upstream redesigned `ModelEditor.svelte` in `v0.12.0`. The Context Window input is now one grid row inside `<div class="flex min-w-0 flex-col gap-2">`, between the base model row and the Tags row, and is covered by `<fieldset disabled={readOnly}>`. If the grid changes again, re-create the row in upstream's current row style.
- The locale files conflict on every upstream release that adds or retranslates a neighbouring key. Take upstream's file and re-insert the fork's keys with the fork's values (four keys for patches 2 and 3). `fo-FO` has never had the fork's keys.
- Downgrading to an official build is safe: `ModelMeta` uses `extra='allow'`.
- In `ModelMeta`, upstream's `i18n` field sits directly below `context_window`, and `coerce_zero_context_window` sits directly above upstream's `check_image_url` validator (which also covers `background_image_url`). Both spots conflicted when `6cdb1dfff` was merged; keep both sides if they conflict again.

---

### 3. Context window usage indicator

**What it changes**

- A circular meter left of the model selector in the chat input shows how much of the model's context window is used. The tooltip shows `Used X% (Y% remaining)` and `Used A / B tokens`, with compact token counts (`126k`, `1.05m`).
- It is shown only when all of these hold: one selected model, not an arena model, `info.meta.capabilities.usage === true`, a positive `info.meta.context_window` (patch 2), and a usage checkpoint for that same model. It is hidden for new chats and multi-model chats.
- Backend (`middleware.py`): `get_model_context_usage_checkpoint` takes the latest provider call's input tokens (first valid of `prompt_tokens`, `input_tokens`, `prompt_eval_count`, `prompt_n`). `persist_model_context_usage_checkpoint` stores it in the message's `meta.model_context_usage`, for both the streaming and non-streaming handlers. Failed or cancelled replies do not persist a checkpoint.
- Frontend: `src/lib/utils/modelContextUsage.ts` finds the latest checkpoint on the active branch. `Chat.svelte` keeps committed / preview / pending usage state and passes `modelContextUsage` to `MessageInput.svelte`. `Messages.svelte`, `Message.svelte` and `MultiResponseMessages.svelte` gain an `onBranchChange` prop so the meter follows branch switches.
- `stream_options.include_usage` is now requested only when `capabilities.usage === true` (previously `?? false`).
- `622272b51`: used tokens become `input + output` of the latest call. Output is the first valid of `completion_tokens`, `output_tokens`, `eval_count`, `predicted_n`. `merge_usage` in `utils/response.py` keeps a zero `completion_tokens` and no longer carries output over from an earlier call. The non-streaming `chat:completion` event now includes `usage`.

**Why**

- The fork wanted a native-looking indicator of context consumption, based on the provider's reported usage rather than an estimate.
- The value must be the latest provider call, not the sum over a tool loop, which would over-count.
- `622272b51`: the first version ignored the tokens just generated, which occupy context on the next turn (100,000 input + 5,000 output showed 100,000 instead of 105,000). `total_tokens` is deliberately not used because it can accumulate across tool loops, and reasoning tokens are already part of output.

**Branch:** `feat/context-window-usage-indicator`

**Commits**

- `b8b0e4e6c` (2026-08-13) `feat(chat): add context window usage indicator`
- `622272b51` (2026-09-21) `fix(chat): include output tokens in context window usage`

**Files and line ranges**

`b8b0e4e6c` (at `crystalvibe28/main @ 8d385a22e`)

- `backend/open_webui/utils/middleware.py`: 10, 4249-4264, 4278-4280, 4282-4311, 4314, 4328-4338, 4490, 4494-4505, 4884-4890, 4947-4948, 4984-4985, 4999-5009, 5062-5063, 5224, 5263, 5285, 5330-5331, 5394, 6722, 6736-6738 (merge `ab859ad51`: 5284, 6731)
- `src/lib/components/chat/Chat.svelte`: 74-77, 79-80, 473-477, 479-548, 550-555, 558-570, 576-581, 587-617, 620-629, 631-645, 648-650, 656-674, 1003-1004, 1146, 1724, 1753-1757, 1796, 2697, 2939, 3024-3028, 3512, 3566, 3574-3575, 4031, 4420, 4431, 4505, 4523, 4645-4646, 5248, 5310, 5406 (merge `ab859ad51`: 3086, 3089-3092)
- `src/lib/components/chat/MessageInput.svelte`: 160, 573-596, 598, 600-603, 606-614, 616-619, 2693-2748
- `src/lib/components/chat/Messages.svelte`: 42, 225, 262, 302, 362, 379-380, 382-392, 406, 476, 536
- `src/lib/components/chat/Messages/Message.svelte`: 26, 134
- `src/lib/components/chat/Messages/MultiResponseMessages.svelte`: 42, 99, 115, 131, 199
- `src/lib/utils/modelContextUsage.ts`: 1-142 (new; shared with `622272b51`)
- `src/lib/utils/modelContextUsage.test.ts`: 1-143 (new; shared with `622272b51`)
- `src/lib/i18n/locales/*/translation.json` (63 files): keys `Context Window:`, `Used {{inputTokens}} / {{contextWindow}} tokens`, `Used {{usedPercent}}% ({{remainingPercent}}% remaining)`

`622272b51` (at `crystalvibe28/main @ 8d385a22e`, merged by `06369d6fc` on 2026-10-12)

- `backend/open_webui/utils/middleware.py`: 4265-4277, 4281, 4465, 4474
- `backend/open_webui/utils/response.py`: 137-138, 140
- `src/lib/components/chat/Chat.svelte`: 78, 478, 549, 556-557, 571-575, 582-586, 618-619, 630, 646-647, 651-655
- `src/lib/components/chat/MessageInput.svelte`: 76-80, 597, 599, 604-605, 615
- `src/lib/utils/modelContextUsage.ts`: 4, 23, 67-80, 106-107, 133-139
- `src/lib/utils/modelContextUsage.test.ts`: 7-9, 47, 75, 93-142
- `scripts/test-model-context-usage.py`: 1-73 (new; standalone `unittest`, standard library only)

**Merge notes**

- `Chat.svelte` and both response handlers in `middleware.py` change in almost every upstream release, and this patch has many scattered call sites there. After a merge, check the begin / record / commit / hydrate / clear calls, the `onBranchChange` plumbing and the `capabilities.usage === true` condition.
- In `non_streaming_chat_response_handler`, `usage = normalize_usage(...)` must stay after upstream's `if continuing:` block and before the `chat:completion` event, which includes `usage`. This spot conflicted when `622272b51` was merged, and again in the `v0.12.0` merge, where upstream added `finish_reason = ...` next to its own `usage =` line below the event. Keep `finish_reason` there and do not bring the second `usage =` back.
- Call sites in `Chat.svelte` that were re-placed in the `v0.12.0` merge, because upstream rewrote the code around them for shared chats and the realtime voice bridge:
  - `chatCompletionEventHandler`, `if (done)`: `commitCompletedModelContextUsage(message)` and `settleModelContextUsage(message)` must run before upstream's early returns (`if (shared) return;` and the `message.error` branch). Otherwise a failed reply never settles its pending usage.
  - `stopResponse(processQueue, messageId)`: `clearPendingModelContextUsage()` comes after upstream's ownership check, so stopping someone else's reply in a shared chat does not clear local state. It still clears every pending entry.
  - `handleOpenAIError` is now synchronous and builds the message with `getErrorMessage`; `clearPendingModelContextUsage([responseMessage.id])` is its first line.
  - `chat:message:error`: the clear is the first line of the branch. `chat:tasks:cancel`: the clear follows upstream's `if (!event.shared) dismissContextCompactionToast();`.
  - `loadChat`: the clear for the current message comes before upstream's loop that marks every interrupted assistant message as done.
- Upstream has its own, unrelated context panel in `MessageInput.svelte` (`contextUsage`, `statusContextUsage`, used for compaction). It coexists with this patch's `modelContextUsage` meter; do not merge the two.
- `merge_usage` in `utils/response.py` is a core upstream helper. Re-apply the zero-preserving `completion_tokens` logic if upstream rewrites it.
- After an upstream merge, run `npx vitest run src/lib/utils/modelContextUsage.test.ts` and `python scripts/test-model-context-usage.py`.

---

### 4. Fork version suffix

**What it changes**

- The version is `<upstream version>+crystalvibe28.<N>`, hand-edited in three places: `package.json` (`version`) and `package-lock.json` (top level and `packages[""]`). `pyproject.toml` and `CHANGELOG.md` are not touched.
- Current value on `crystalvibe28/main`: `0.12.0+crystalvibe28.3`.
- Releases were tagged with lightweight tags on the merge commit: `v0.11.0+crystalvibe28.1`, `v0.11.0+crystalvibe28.2`.

**Why**

- The version must show which official release the fork is based on while staying distinct from official numbers. The fork keeps merging upstream releases, so it cannot invent numbers such as `0.11.1`.
- `npm version` strips `+…` build metadata, hence the manual edit.
- Container tags cannot contain `+`, so the image workflow (patch 5) publishes the tag with `+` replaced by `-`.

**Branch:** `crystalvibe28/dev` (merged into `crystalvibe28/main`)

**Commits**

- `ac7a62d95` (2026-08-14) `chore(release): bump version to 0.11.0+crystalvibe28.1`
- `f249ab0f4` (2026-08-14) `chore(release): bump version to 0.11.0+crystalvibe28.2`

**Files and line ranges** (at `crystalvibe28/main @ 8d385a22e`)

- `package.json`: 3
- `package-lock.json`: 3, 9
- These lines are now attributed to merge `cbd352c23` (`Merge tag 'v0.12.0'`), where the suffix was re-applied and `<N>` went from `2` to `3`.

**Merge notes**

- These three lines conflict on every upstream version bump. Resolve to `<new upstream version>+crystalvibe28.<N>`.
- Since `v0.12.0` the UI shows the version through upstream's `BuildVersion.svelte`, which appends `(build · <hash>)` unless the build channel is `main`. The image workflow passes `BUILD_CHANNEL=main` (patch 5), so the fork's version is shown without that suffix.

---

### 5. GHCR-only image build workflow

**What it changes**

- `808e1b4d5` rewrites the Docker workflow as a single job, `Build Open WebUI Image`:
  - Triggers: push to `crystalvibe28/main`, or `workflow_dispatch`.
  - Builds one image: `linux/amd64`, `USE_CUDA=false`, `USE_OLLAMA=false`, `USE_SLIM=false`, `BUILD_HASH=${{ github.sha }}`, and since the `v0.12.0` merge `BUILD_CHANNEL=main`.
  - Pushes to `ghcr.io/<owner>/<repo>` with two tags: the `package.json` version with `+` replaced by `-` (for example `0.12.0-crystalvibe28.3`) and `latest`.
  - Removed from upstream's version: the amd64/arm64 matrix, the cuda / cuda126 / ollama / slim variants, the registry cache, SBOM, the manifest merge job, the Docker Hub copy and the Helm chart notification.
- The same commit disables `backend`, `frontend`, `issue-label`, `release-pypi` and `release` by renaming them to `*.disabled` (GitHub only runs `.yml` / `.yaml`), each with a one-line comment at the top.
- `036b4d6ba` renames `docker.yaml` to `docker-image-build.yaml` and updates the `workflow_id` reference in `release.disabled`.

**Why**

- The fork only needs its own base image on GHCR. Upstream's pipeline is a full release pipeline (multi-arch, five variants, GitHub Release, PyPI, Docker Hub, Helm).

**Branch:** committed directly on `crystalvibe28/main`

**Commits**

- `808e1b4d5` (2026-08-29) `ci: simplify GHCR image build workflow`
- `036b4d6ba` (2026-08-29) `ci: rename Docker image build workflow`

**Files and line ranges** (at `crystalvibe28/main @ 8d385a22e`)

`808e1b4d5`

- `.github/workflows/docker-image-build.yaml` (was `docker.yaml`): 1, 5-6, 9, 17, 26-32, 35, 46-49, 56, 62-65, 69-71 (merge `cbd352c23`: 68, the `BUILD_CHANNEL=main` build-arg). Treat the whole file (1-71) as fork-owned.
- `.github/workflows/backend.disabled` (was `backend.yaml`): 1
- `.github/workflows/frontend.disabled` (was `frontend.yaml`): 1
- `.github/workflows/issue-label.disabled` (was `issue-label.yaml`): 1
- `.github/workflows/release-pypi.disabled` (was `release-pypi.yml`): 1
- `.github/workflows/release.disabled` (was `release.yml`): 1

`036b4d6ba`

- `.github/workflows/docker.yaml` → `.github/workflows/docker-image-build.yaml` (pure rename)
- `.github/workflows/release.disabled`: 73

**Merge notes**

- Upstream edits to the renamed workflows surface as rename or modify/delete conflicts. Keep the `*.disabled` names and make sure no `docker.yaml` comes back.
- When upstream changes `docker.yaml`, check whether the change belongs in `docker-image-build.yaml` too. In `v0.12.0` upstream added a `BUILD_CHANNEL` build-arg (`51f0e0125`) that the `Dockerfile` passes to the frontend build as `APP_BUILD_CHANNEL`; the fork's workflow sets it to `main`. The same release renamed the image's `WEBUI_BUILD_VERSION` environment variable to `WEBUI_BUILD_HASH`.
- A new upstream workflow is active by default. `regression.yaml` (upstream, 2026-09-05) is currently active; it only triggers on pull requests to `main` / `dev`.
- `codespell.disabled`, `lint-backend.disabled` and `lint-frontend.disabled` were disabled by upstream, not by this fork.

---

### 6. Auto-scroll for streamed responses

**Status:** in `crystalvibe28/main`, but the `Chat.svelte` half has been superseded by upstream.

**What it changes**

- `Chat.svelte`: `responseCompletionEventHandler` (the `response:completion` stream events) schedules a scroll to the bottom, as the `chat:completion` handler already did.
- `MessageInput.svelte`: the scroll-to-bottom button uses `behavior: 'auto'` instead of `'smooth'`.
- `chatScroll.test.ts` runs the real handlers extracted from the `.svelte` sources (`svelte/compiler` + `vm`) and checks that scrolling follows `autoScroll` and `settings.scrollOnResponseGeneration`.

**Why**

- On upstream `v0.11.3` the view stopped following the model's output, even after clicking the scroll-to-bottom button.
- Cause 1: the `response:completion` handler added upstream in `a1579a01f` never requested a scroll.
- Cause 2: during a smooth scroll the scroll listener sees a distance to the bottom greater than its threshold and turns `autoScroll` off again.
- Upstream fixed cause 1 itself in `dfde08aa7` / `88e78b781` (released in `v0.11.4`) with `autoScrollToBottom`. The `v0.11.4` merge (`ec3b1c2c1`) adopted that version and adapted the test. Cause 2 is still fork-only.

**Branch:** `crystalvibe28/fix`

**Commits**

- `04846ab3b` (2026-09-21) `fix(chat): restore auto-scroll for streamed responses`

**Files and line ranges** (at `crystalvibe28/main @ 8d385a22e`)

- `src/lib/components/chat/MessageInput.svelte`: 928
- `src/lib/components/chat/chatScroll.test.ts`: 1-22, 24-35, 55-80 (new; merge `ec3b1c2c1`: 23, 36-54)
- `src/lib/components/chat/Chat.svelte`: no surviving lines (the added `scheduleResponseScrollToBottom();` call was replaced by upstream's `autoScrollToBottom`)

**Merge notes**

- Keep `behavior: 'auto'` in `scrollToBottom` of `MessageInput.svelte`.
- The test depends on the declaration names `responseCompletionEventHandler`, `shouldAutoScrollResponse`, `autoScrollToBottom` and `scrollRAF` in `Chat.svelte`. An upstream rename breaks it.

---

### 7. Analysis group stays active during reasoning

**Status:** superseded by upstream in `v0.12.0`. Upstream fixed the same problem in `19957bc19` with its own `hasActiveDetails`, and the `v0.12.0` merge (`cbd352c23`) took upstream's code in full (decided 2026-10-12). `ConsecutiveDetailsGroup.svelte` is now identical to upstream. Only the fork's test file remains, and it passes against upstream's implementation.

**What it changes**

- `ConsecutiveDetailsGroup.svelte` adds `hasActiveDetails`: true when a tool call is still active, **or** when the message is not done and a `reasoning` or `code_interpreter` item has `done` set to something other than `'true'`.
- The "Exploring" / "Explored" prefix, the spinner and the shimmer class now key on `hasActiveDetails` instead of `hasActiveToolCalls`.
- Upstream's version, which replaced the above: `hasActiveDetails` is a single `tokens.some(...)`. A `tool_calls` item is active unless it is rejected, failed, incomplete or done; any other item is active when the message is not done and its `done` attribute is set to something other than `'true'`. It is not limited to `reasoning` and `code_interpreter`, and `hasActiveToolCalls` no longer exists.

**Why**

- After a tool call finished and the model went on thinking, the collapsed group showed "Explored" with a check mark instead of "Exploring" with a spinner.
- Upstream `7d99b2716` (`v0.11.1`) narrowed the activity check to tool calls only; `v0.11.0` treated any unfinished item as active.

**Branch:** `crystalvibe28/fix`

**Commits**

- `f82017e24` (2026-09-21) `fix(chat): keep analysis groups active during reasoning`

**Files and line ranges** (at `crystalvibe28/main @ 8d385a22e`)

- `src/lib/components/chat/Messages/Markdown/ConsecutiveDetailsGroup.svelte`: no surviving lines (replaced by upstream's implementation)
- `src/lib/components/chat/Messages/Markdown/ConsecutiveDetailsGroup.test.ts`: 1-63 (new)

**Merge notes**

- Nothing to re-apply in the component. Keep the test file: it checks the rendered result ("Exploring", the spinner, the `!messageDone` guard, the rejected and failed icons) and will show a regression if upstream narrows the check again.

---

### 8. Group-based user visibility

**What it changes**

The rule, implemented by `UserVisibility` in `backend/open_webui/utils/user_visibility.py`. It is always on; there is no config flag.

- Admins see everyone.
- Other users see themselves, every admin, and every member of the groups they belong to. A user with no group sees only the admins. (Until `5297d1781`, admins were hidden like anyone else and a user with no group saw nobody; changed on request on 2026-10-12, so that admin-owned workspace models, skills and tools keep their owner and admins can be reached.)
- Pending accounts are as upstream: they cannot call any of the user endpoints. The one thing they can read is the admin contact on the pending screen (`/auths/admin/details`, only while `auth.admin.show` is on).
- Group membership here means direct membership. Upstream's nested groups (`v0.12.0`) do not widen it: a member of a child group does not see the members of its parent groups (decided 2026-10-12, see the merge notes).
- Inside a channel the visible set is replaced by a channel-scoped one:
  - DM and private group channels: the active channel members.
  - Standard channels without a public read grant: the users with read access, the channel owner and the admins (who can read every standard channel).
  - Public channels: the group-based rule above. `is_open_channel(channel)` is the single test for "public" used by `for_channel` and by the model reply handler.
- Hidden users and foreign groups return 404 rather than 403.

Enforcement happens at three layers:

1. **Routes.**
   - `routers/users.py`: `GET /users/search`, `/{user_id}/info`, `/{user_id}/profile/image` and `/{user_id}/active` are filtered and accept an optional `channel_id`.
   - `routers/channels.py`: member lists, DM lookup, channel creation and add-member (`require_channel_user_ids_visible`), mentions in new or edited messages (`require_visible_user_mentions`), and notifications.
   - `routers/groups.py`: `GET /groups/id/{id}/info` requires membership.
   - `routers/auths.py`: `get_admin_details` returns 404 if the admin is not visible.
2. **Response sanitiser.** `UserVisibilityMiddleware` (`user_visibility_middleware.py`, registered in `main.py` so that it runs inside response compression) buffers 2xx JSON responses for non-admins and passes them through `sanitize_user_payload` (`user_visibility_payload.py`). That function nulls hidden user objects (`user`, `owner`, `author`, …), blanks hidden id fields (`user_id`, `created_by`, …), filters `users` / `members` / `user_ids` lists, rewrites `<@U:id|…>` mentions to `@Unknown` and profile image URLs to `/user.png`, and limits `groups`, `group_ids` and `access_grants` to the viewer's own groups.
3. **Sockets.** `PrivacyAsyncServer` in `socket/main.py` replaces the `sio` server. For `events:channel`, `events:note` and `ydoc:*` events it emits a separately sanitised copy to each recipient. Yjs handlers take `user_id` / `user_name` from the authenticated session instead of client data.
   - Shared chat events (`aef77fe61`): an `events` payload with `shared: True` that carries `user_id` or `user` (typing, and the reply events mirrored to the `chat:{id}` room) is no longer broadcast to the room. `_emit_shared_chat` sends each session in the room its own copy through `sanitize_user_payload`, so a viewer who may not see the acting user gets `user: null` and `user_id: ''`; the frontend already ignores a typing event without a user. Sessions come from the local room plus, with the Redis manager, the `chat_ids` index in `SESSION_POOL`. Each viewer's policy is cached for `SHARED_CHAT_POLICY_TTL` (5 seconds), because a streamed reply produces several events per second. `events` payloads without those fields, such as `chat:access` and every non-shared event, pass through unchanged.

Supporting changes:

- Sharing: `filter_allowed_access_grants(..., existing_grants=...)` in `utils/access_control/__init__.py` rejects new grants to hidden users or foreign groups, and preserves hidden grants that already exist when a resource is edited. Every router that updates access grants passes `existing_grants`.
- Search: the owner-name match in `models/{knowledge,models,prompts,skills}.py` is AND-ed with the visible user ids, so a search cannot reveal hidden owners.
- Builtin tools: `search_channel_messages`, `view_channel_message` and `view_channel_thread` in `tools/builtin.py` apply the same rules, so a model cannot leak identities.
- Frontend: profile image, user info and active-status requests carry `channel_id`; components pass a `channelId` prop or context; null users are tolerated ("Unknown User", `/user.png`).
- `dae17c8ff` fixes two problems found in testing. Public group channels no longer narrow the visible set, so same-group users can be mentioned there, and `MentionList.svelte` calls `searchUsers` (with `channel_id`) for every role. The group search in `models/groups.py` always applies the `member_id` filter, so the add-member dialog lists only groups the user belongs to.
- `d8be77741`: in `sanitize_user_payload`, a user object without `id` or `user_id` is nulled when the record that holds it belongs to a hidden user (`_user_object(..., hidden_owner)`). This covers upstream's version history entries, which carry `user: {'name': …}` next to the entry's own `user_id`.
- `fdc4598d4` — sanitiser and grant filter:
  - Identity fields are only treated as such when their value is a string. A JSON schema that names a parameter `user_id`, `owner_id`, `author_id` or `role` used to raise `TypeError` (unhashable dict) and turn the whole response into a 500; tool `specs` are now also opaque.
  - New fields: `parent_group_id` is nulled unless it is one of the viewer's groups; `attendees` is a user list, so a hidden attendee's row is dropped; a list of grant-shaped dicts (`principal_type` + `principal_id`) is filtered even without an `access_grants` key (`GET /chats/shared/{id}/access`).
  - `_EMBEDDED`: inside a resource's otherwise opaque `data` / `meta`, `data.files`, `meta.access_grants` (an arena model with a DB override) and `meta.knowledge` are still sanitised.
  - `filter_allowed_access_grants` returns `None` unchanged. `None` means "leave the grants alone"; with `existing_grants` set it used to fall through and raise.
- `5297d1781` — scopes:
  - `get_admin_ids()` and the admin rule above; `UserVisibility.common()` is the set every viewer shares (the admins). The `channel_scoped` flag is gone, as nothing returns an empty directory for "no group" any more.
  - `GET /users/groups?include_inherited=true` ignores the flag for non-admins, so inherited parent groups are not listed.
  - `require_channel_user_ids_visible` checks a group's members with `include_inherited=True`, because `Channels._collect_unique_user_ids` (upstream) adds the members of child groups too.
  - `model_response_handler`: in an open channel the model gets real names only for the users in `UserVisibility.common()`. Everyone else is `User 1`, `User 2`, … (stable within the thread) and user mentions become `@Unknown`, because the reply is read by people outside the caller's groups. Private channels and DMs keep real names.
- `4ee44089c`:
  - `GET /chats/all` is an NDJSON stream, which the middleware does not buffer. `generate_chat_export_ndjson(user)` sanitises each chat for non-admins; a cloned shared chat, or one that others replied to, carries `user` / `user_id` on its messages.
  - Calendar events: `_filter_event_attendees` in `routers/calendar.py` rejects (404) attendees the caller cannot see, on create and update, and re-appends attendees that are already on the event but hidden from the caller.
- `6a03dd13d` — frontend, for the shapes the sanitiser produces:
  - `UserMessage.svelte`: `authorId` uses `??`, so an empty `user_id` (hidden author) no longer falls back to the chat owner.
  - `ChannelItem.svelte`: the sidebar DM avatar carries `channel_id`.
  - `RecursiveFolder.svelte`: only a missing `user_id` marks a shared-folder chat as the viewer's own; an empty one does not.

**Why**

- This instance is shared by several unrelated circles of people who should not be able to see each other.
- On upstream `v0.11.3` any enabled user can search all users through `/api/v1/users/search`, read `/users/{id}/info` (email and role included), and see every account in channel mention and member pickers. The upstream PR that restricted mentions to channel members (#28522) was closed without being merged.
- Only identity visibility is restricted. Which channels a user can see is unchanged.
- `d8be77741` and `aef77fe61` close two paths that upstream `v0.12.0` opened and the patch did not cover, found while analysing that merge:
  - The version history of models, tools, skills and functions returned the author's name in a `user` object without an id, which the sanitiser passed through.
  - Shared chats with "Allow replies" send typing and reply events, with the acting user's id and name, to everyone who has the chat open. The socket server only sanitised channel, note and Yjs events. The HTTP responses for the same chats were already covered.
- The last four commits come from a second audit of the whole patch on the `v0.12.0` base (2026-10-12). It found no way for a user to list or look up accounts outside their scope, but it did find:
  - identity reaching a user outside the sanitiser: the chat export stream, the bare grant list of a shared chat, names repeated by a model in a public channel, calendar attendees, and three nested-group paths;
  - faults caused by the patch itself: the 500 on tool lists and on updates that omit `access_grants`, and hidden authors shown as the chat owner.
- The owner then restated the rule with admins visible to everyone, as long as normal use is not affected; see "What it changes".

**Branch:** `feat/group-user-visibility`

**Commits**

- `3656be046` (2026-09-25) `feat: restrict user visibility by shared groups and channel access`
- `dae17c8ff` (2026-09-25) `fix: align channel mentions and group selection with visibility rules`
- `d8be77741` (2026-10-12) `fix: hide version history authors outside the viewer's groups`
- `aef77fe61` (2026-10-12) `fix: sanitize shared chat events for each viewer`
- `fdc4598d4` (2026-10-12) `fix: harden the identity sanitizer and keep grants an update omits`
- `5297d1781` (2026-10-12) `feat: show admins to every user and tighten group and channel scopes`
- `4ee44089c` (2026-10-12) `fix: sanitize chat exports and validate calendar attendees`
- `6a03dd13d` (2026-10-12) `fix: handle hidden users in shared chats, folders and DM avatars`

**Files and line ranges** (at `crystalvibe28/main @ 8d385a22e`)

`3656be046` — core

- `backend/open_webui/utils/user_visibility.py`: 1-5, 27-31, 37-46, 48-69, 71-82, 85-86, 88-98, 100-104, 106-107, 109-112, 114-126 (new)
- `backend/open_webui/utils/user_visibility_middleware.py`: 1-98 (new)
- `backend/open_webui/utils/user_visibility_payload.py`: 1-27, 29, 34-42, 44-49, 52-55, 60-81, 84-88, 99-102, 104-124, 127-128, 132-134, 136-148 (new)
- `backend/open_webui/utils/access_control/__init__.py`: 231, 259-301, 347-349
- `backend/open_webui/main.py`: 221, 820-821
- `backend/open_webui/socket/main.py`: 60-61, 105-121, 135-296, 340, 350, 366, 642-648, 681-682, 756, 789, 800, 834, 858, 900, 1094-1095, 1264 (merge `cbd352c23`: 678)
- `backend/open_webui/tools/builtin.py`: 31, 1848-1854, 1880, 1882-1884, 1887-1891, 1930-1936, 1973-1975, 2000-2006, 2058-2067

`3656be046` — routers

- `backend/open_webui/routers/users.py`: 15, 17, 21, 23-24, 26, 49, 151, 159, 161-163, 828-831, 833-836, 838-839, 842, 874-885, 889, 894, 896, 929-932, 934-935
- `backend/open_webui/routers/channels.py`: 50, 137-149, 152-176, 225, 240, 242, 250, 291-297, 356-358, 459-461, 469, 501-509, 603-605, 620, 623, 627-629, 712-713, 815, 1048-1052, 1063-1065, 1078-1079, 1089-1091, 1158-1161, 1174-1175, 1270-1273, 1649-1652
- `backend/open_webui/routers/knowledge.py`: 37, 51-52, 1188, 1265, 1338-1345, 1347
- `backend/open_webui/routers/groups.py`: 33, 133-134
- `backend/open_webui/routers/auths.py`: 1140-1146
- `backend/open_webui/routers/models.py`: 620, 1232, 1314
- `backend/open_webui/routers/notes.py`: 543, 623
- `backend/open_webui/routers/prompts.py`: 298, 479
- `backend/open_webui/routers/skills.py`: 384, 463
- `backend/open_webui/routers/tools.py`: 673 (merge `cbd352c23`: 581)
- `backend/open_webui/routers/calendar.py`: 454
- `backend/open_webui/routers/chats.py`: 2169
- `backend/open_webui/routers/folders.py`: 561

`3656be046` — models

- `backend/open_webui/models/knowledge.py`: 27, 282-292, 297
- `backend/open_webui/models/models.py`: 18, 514-524, 529
- `backend/open_webui/models/prompts.py`: 19, 304-313, 319
- `backend/open_webui/models/skills.py`: 298-307, 313 (merge `cbd352c23`: 14)

`3656be046` — frontend

- `src/lib/apis/users/index.ts`: 335, 338-341, 522, 525-528
- `src/routes/+layout.svelte`: 904, 917-919
- `src/lib/components/channel/Channel.svelte`: 156, 199
- `src/lib/components/channel/ChannelInfoModal/UserList.svelte`: 221-227, 230
- `src/lib/components/channel/MessageInput.svelte`: 909
- `src/lib/components/channel/MessageInput/MentionList.svelte`: 6, 248
- `src/lib/components/channel/Messages.svelte`: 83
- `src/lib/components/channel/Messages/Message.svelte`: 321, 354, 358, 362-367, 382, 414-415, 417, 421, 454, 590 (merge `cbd352c23`: 422-426)
- `src/lib/components/channel/Messages/Message/ProfilePreview.svelte`: 21, 60
- `src/lib/components/channel/Messages/Message/UserStatus.svelte`: 28 (merge `cbd352c23`: 82)
- `src/lib/components/channel/Messages/Message/UserStatusLinkPreview.svelte`: 11, 22-24, 26-30, 32-34, 36, 41, 56
- `src/lib/components/channel/Navbar.svelte`: 101
- `src/lib/components/channel/Thread.svelte`: 76, 115
- `src/lib/components/chat/Messages/Markdown.svelte`: 34-35, 43, 68-71
- `src/lib/components/chat/Messages/Markdown/MarkdownInlineTokens/MentionToken.svelte`: 6, 14, 87, 123
- `src/lib/components/layout/Sidebar/ChannelItem.svelte`: one unused import removed; no added lines

`dae17c8ff`

- `backend/open_webui/models/groups.py`: 333-337
- `backend/open_webui/routers/users.py`: 144, 150
- `backend/open_webui/utils/user_visibility.py`: 84 (the rest was folded into `is_open_channel` by `5297d1781`)
- `src/lib/apis/users/index.ts`: 202-203, 211
- `src/lib/components/channel/MessageInput/MentionList.svelte`: 47, 62-74

`d8be77741`

- `backend/open_webui/utils/user_visibility_payload.py`: 43, 50-51, 103

`aef77fe61`

- `backend/open_webui/socket/main.py`: 101-104, 122-134, 297-339

`fdc4598d4`

- `backend/open_webui/utils/user_visibility_payload.py`: 28, 30-33, 56-59, 82-83, 89-98, 125-126, 129-131, 135
- `backend/open_webui/utils/access_control/__init__.py`: 238-239

`5297d1781`

- `backend/open_webui/utils/user_visibility.py`: 6-26, 32-36, 47, 70, 83, 87, 99, 105, 108, 113
- `backend/open_webui/routers/users.py`: 160, 182-183
- `backend/open_webui/routers/channels.py`: 49, 150-151, 1080-1088, 1172, 1199. It also removes the "no group, public channel" early return from `get_channel_visible_user_ids`.

`4ee44089c`

- `backend/open_webui/routers/chats.py`: 50-51, 1040, 1048-1050, 1054, 1064-1069, 1082
- `backend/open_webui/routers/calendar.py`: 30, 84-95, 299-300, 356-358

`6a03dd13d`

- `src/lib/components/chat/Messages/UserMessage.svelte`: 60-61
- `src/lib/components/layout/Sidebar/ChannelItem.svelte`: 120
- `src/lib/components/layout/Sidebar/RecursiveFolder.svelte`: 153, 402

**Merge notes**

- This is the largest and most conflict-prone patch, and it has **no automated tests** (the tests written during development were removed before the commit). After every upstream merge, re-check by hand as a non-admin user: user search, mention lists, channel member lists, the add-member dialog and profile previews. Since `v0.12.0` also check a shared chat with "Allow replies" (typing line, sender names) and the version history of a shared model, tool or skill. Since the 2026-10-12 audit also check: "Export All Chats" after cloning someone else's shared chat, `@model` in a public channel, the sidebar avatar of a DM with someone outside the viewer's groups, and the Tools page (it must not return 500).
- The second-audit commits were checked by reading the code, by a throwaway script against `sanitize_user_payload` / `UserVisibility.load`, and by `npm run build`. They were not exercised against a running server.
- Upstream code added later is not covered automatically:
  - A new endpoint or socket event that returns user data needs an explicit check. The sanitiser only recognises the field names listed above.
  - A new router that calls `filter_allowed_access_grants` must pass `existing_grants`.
  - A response that is not `application/json` (NDJSON, SSE, a download) skips the middleware. The two that carry identities sanitise by hand: the chat export in `routers/chats.py` and the pending-file stream in `routers/knowledge.py`.
  - A new input that takes user ids (like calendar `attendees`) needs its own `visibility.require_user` check; the grant filter only covers `access_grants`.
- `model_response_handler` in `routers/channels.py` is upstream code with the fork's naming woven in (`author_label`, the `is_open_channel` switch, `visibility.filter_users`). If upstream rewrites how the thread history is built, re-apply all three, or a public-channel reply can name users its readers may not see. The chat completion it starts still runs as the caller, so a model system prompt that uses `{{USER_NAME}}` is outside this protection.
- Known and left alone: the Overview graph labels user nodes with the viewer when the chat owner is hidden; workspace cards show "Deleted User" for a hidden author; `/api/usage` exposes the instance-wide active user count to every user unless `ENABLE_PUBLIC_ACTIVE_USERS_COUNT=false`; the channel typing event forwards client-supplied data.
- `app.add_middleware(UserVisibilityMiddleware)` must stay registered before `CompressMiddleware`, so it sees uncompressed JSON.
- Both `sio = socketio.AsyncServer(...)` constructors (Redis and non-Redis) must stay `PrivacyAsyncServer`. Since `v0.12.0` the Redis one picks its manager class through `WEBSOCKET_REDIS_ROOM_CHANNELS` (`AsyncRedisRoomChannelManager`). `PrivacyAsyncServer` with that manager has not been tested.
- `SESSION_POOL` entries must be written by merging into the existing entry (`{**(SESSION_POOL.get(sid) or {}), **…}`) in `connect`, `user_join` and `heartbeat`. Upstream rebuilds the entry and keeps only `chat_ids`, which drops the `channel_ids` and `note_ids` that `PrivacyAsyncServer` uses to find recipients on other workers. These three spots conflicted in the `v0.12.0` merge; keep upstream's `token` in `save_session` and its `LOCAL_AUTHENTICATED_SIDS.add(sid)`.
- `enter_room_for_users` uses upstream's permission loop (`028dab8f1`: users without the Channels permission do not join) with the fork's `get_session_ids_by_user_id` lookup and `remember_session_resource` call.
- Nested groups (`v0.12.0`, `d4c561d9f`). Upstream's access checks count inherited membership (`include_inherited=True`), but this patch deliberately keeps direct membership (decided 2026-10-12): `UserVisibility.load`, the group check in `require_channel_user_ids_visible`, the unconditional `member_id` filter in `Groups.get_groups` and `GET /users/groups` all use it, so the sharing dialog, the grant filter and the sanitiser agree with each other. The one place that expands inheritance is the member check in `require_channel_user_ids_visible`, and only to refuse: inviting a parent group would add child-group members the caller cannot see. Nothing changes while no group has a parent. Once a parent group is used, the two rules differ: a user who reaches a standard channel only through an inherited grant gets 404 from the channel-scoped user endpoints and no realtime events for that channel, because `UserVisibility.for_channel` passes the direct `group_ids` to `AccessGrants.has_access`. Making visibility follow inheritance is a separate change on `feat/group-user-visibility`.
- In `_update_tool` (`routers/tools.py`) the grant filter now runs only `if version_id is None:` (upstream does not change grants when a version is restored); `existing_grants=tools.access_grants` must stay in that call.
- `MentionToken.svelte`: upstream now declares `let openPreview = false` itself. The `v0.12.0` merge left both declarations in place without a conflict, and only the frontend build caught it. Run `npm run build` after every merge. On this machine the build runs out of memory in "rendering chunks" with Node's default heap; set `NODE_OPTIONS=--max-old-space-size=8192` first.
- `UserStatus.svelte` was rewritten upstream in `v0.12.0` (local time, last seen). The fork keeps the `channelId` prop and the `channel_id` query on the profile image; the null-user fallback avatar in `channel/Messages/Message.svelte` follows upstream's avatar size.

---

### 9. PWA app shell revalidation

**What it changes**

- Moves `SPAStaticFiles` out of `main.py` into `backend/open_webui/utils/spa_static_files.py` and overrides `file_response` to set `Cache-Control: no-cache` on `*.html` and `version.json`, including 304 and HEAD responses and the SPA fallback to `index.html`.
- Hashed assets under `_app/immutable` keep their normal caching.
- The existing fallback is unchanged: a 404 serves `index.html`, except for missing `.js` files, which stay 404.

**Why**

- After a new image was deployed, the installed PWA (Android + Chrome) sometimes hung on the splash logo and only recovered after a while or after several restarts.
- Most likely cause: a cached `index.html` from the previous build references JS bundles that no longer exist, which also prevents the app's own update check from starting. This was not confirmed on a device.

**Branch:** `crystalvibe28/fix`

**Commits**

- `5b67b4292` (2026-09-26) `fix(pwa): revalidate app shell after deployment updates`

**Files and line ranges** (at `crystalvibe28/main @ 8d385a22e`)

- `backend/open_webui/utils/spa_static_files.py`: 1-23 (new)
- `backend/tests/test_spa_static_files.py`: 1-58 (new)
- `backend/open_webui/main.py`: 289 (import). The inline `SPAStaticFiles` class and the `StarletteHTTPException` import were removed.

**Merge notes**

- If upstream edits the inline `SPAStaticFiles` in `main.py`, the merge can bring the class back. Port the upstream change into `spa_static_files.py` and keep only the import in `main.py`.
- This happened in `v0.12.0`: upstream `c94ac152e` (#31631, a reload loop after a server upgrade) gave the inline class a `file_response` that sets `Cache-Control: no-cache` on `*.html`. That is a subset of what `spa_static_files.py` already does (it also covers `version.json`), so the merge dropped the inline class again and nothing had to be ported. The patch is still needed for `version.json`.
