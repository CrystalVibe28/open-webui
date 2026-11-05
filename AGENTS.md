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
- On an upstream merge, the upstream part follows the merged tag. `<N>` is given by the user for each merge; it stayed at `2` from `v0.11.0` to `v0.11.4`, became `3` with `v0.12.0` and stayed `3` for `v0.12.2`, `v0.12.3` and `v0.13.0`. Do not change `<N>` without being told.
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
- Patches merged into `crystalvibe28/main` are measured at `crystalvibe28/main @ 1ade36b39` (upstream base `v0.13.0`).
- Patches that are **not merged** are measured at their own branch tip, which sits on a much older upstream base, so their numbers do not match `crystalvibe28/main`.
- "merge `<hash>`" marks lines of the same patch that were re-resolved during an upstream merge and are now attributed to that merge commit.
- To measure one file: `git blame --porcelain <ref> -- <path>`, then collect the final line numbers of the lines attributed to the commit.
- To regenerate the commit list: `git log --branches --no-merges --author=CrystalVibe28 --format="%h %ad %s" --date=short`

### Overview

| #   | Patch                                  | Branch                                | In `crystalvibe28/main`      | Commits                                                                                                                                                    |
| --- | -------------------------------------- | ------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Preserve `reasoning_content` on replay | `feat/preserve-reasoning-content`     | No — obsolete, do not merge  | `12f510687`, `49ffac82e`                                                                                                                                   |
| 2   | Model context window metadata          | `feat/model-context-window`           | Yes                          | `d78a5cc29`, `685a7822e`, `6cdb1dfff`                                                                                                                      |
| 3   | Context window usage indicator         | `feat/context-window-usage-indicator` | Yes (partly superseded)      | `b8b0e4e6c`, `622272b51`                                                                                                                                   |
| 4   | Fork version suffix                    | `crystalvibe28/dev`                   | Yes                          | `ac7a62d95`, `f249ab0f4`                                                                                                                                   |
| 5   | GHCR-only image build workflow         | `crystalvibe28/main`                  | Yes                          | `808e1b4d5`, `036b4d6ba`                                                                                                                                   |
| 6   | Auto-scroll for streamed responses     | `crystalvibe28/fix`                   | Yes (partly superseded)      | `04846ab3b`                                                                                                                                                |
| 7   | Analysis group stays active            | `crystalvibe28/fix`                   | Yes (superseded by upstream) | `f82017e24`                                                                                                                                                |
| 8   | Group-based user visibility            | `feat/group-user-visibility`          | Yes                          | `3656be046`, `dae17c8ff`, `d8be77741`, `aef77fe61`, `fdc4598d4`, `5297d1781`, `4ee44089c`, `6a03dd13d`, `6c8cc8d02`, `6736092e2`, `732bcd0a6`, `f5bccff0f` |
| 9   | PWA app shell revalidation             | `crystalvibe28/fix`                   | Yes                          | `5b67b4292`                                                                                                                                                |

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

`d78a5cc29` (at `crystalvibe28/main @ 1ade36b39`)

- `backend/open_webui/models/models.py`: no surviving lines (the field line was rewritten by `6cdb1dfff`)
- `src/lib/apis/index.ts`: 1800
- `src/lib/components/workspace/Models/ModelEditor.svelte`: 209 (merge `c3bd1bd51`: 1376-1396 — the Context Window row, re-created in the `v0.13.0` merge in upstream's `ModelSettingsLabel` row style, between the base model row and the Tags row)
- `src/lib/i18n/locales/*/translation.json` (63 files): key `Context Window` (zh-TW: `上下文窗口`)

`685a7822e` (at `crystalvibe28/main @ 1ade36b39`)

- `backend/open_webui/utils/models.py`: 93-115, 216, 236, 247-250, 311-319

`6cdb1dfff` (at `crystalvibe28/main @ 1ade36b39`, merged by `0fb55dab3` on 2026-10-12)

- `backend/open_webui/models/models.py`: 155, 165-178

**Merge notes**

- `get_all_models` is a hot upstream function. Re-apply `custom_model_lookup`, the base-meta copy in the override branch, and the inheritance block before `model['info'] = info`.
- In the override branch of `get_all_models`, the base-meta copy sits directly after upstream's block that restores an arena model's `access_grants`, `model_ids` and `filter_mode` (`b8de508db`, `v0.12.0`). Both blocks follow `model['info'] = custom_model.model_dump()` and conflicted in the `v0.12.0` merge; keep both.
- Upstream redesigned `ModelEditor.svelte` in `v0.12.0`. The Context Window input is now one grid row inside `<div class="flex min-w-0 flex-col gap-2">`, between the base model row and the Tags row, and is covered by `<fieldset disabled={readOnly}>`. If the grid changes again, re-create the row in upstream's current row style.
- `v0.13.0` changed `ModelEditor.svelte` again: rows label themselves with `ModelSettingsLabel` (an optional `description` becomes a tooltip). Git aligned the fork's row against an unrelated block and the merge re-created it; the fork keeps a `<label for="workspace-model-context-window">` around `ModelSettingsLabel` without a description, so no new i18n key is needed.
- `v0.13.0` added `ProviderDetails.svelte` (admin-only, read-only): it shows the provider-reported `context_length` from the model's raw entry. It is not editable and does not replace `meta.context_window`. A later change could fall back to it when `context_window` is unset.
- The locale files conflict on every upstream release that adds or retranslates a neighbouring key. Take upstream's file and re-insert the fork's keys with the fork's values (four keys for patches 2 and 3). `fo-FO` has never had the fork's keys.
- Downgrading to an official build is safe: `ModelMeta` uses `extra='allow'`.
- In `ModelMeta`, upstream's `i18n` field sits directly below `context_window`, and `coerce_zero_context_window` sits directly above upstream's `check_image_url` validator (which also covers `background_image_url`). Both spots conflicted when `6cdb1dfff` was merged; keep both sides if they conflict again.

---

### 3. Context window usage indicator

**Status:** in `crystalvibe28/main`, but the `merge_usage` change in `utils/response.py` (`622272b51`) has been superseded by upstream. Upstream's `v0.13.0` `merge_usage` sums the canonical counters and keeps `prompt_tokens` / `completion_tokens` at the latest call's value, zero included (`302b8cfd5`, for context compaction), which is what the checkpoint needs. The `v0.13.0` merge (`c3bd1bd51`) took upstream's version in full; `scripts/test-model-context-usage.py` passes against it.

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

`b8b0e4e6c` (at `crystalvibe28/main @ 1ade36b39`)

- `backend/open_webui/utils/middleware.py`: 10, 3933-3948, 3962-3964, 3966-3995, 3998, 4022-4032, 4190, 4194-4205, 4583-4589, 4646-4647, 4717-4718, 4732-4742, 4795-4796, 4924, 4963, 4985, 5026-5027, 5094, 6476, 6491-6493 (merge `ab859ad51`: 4984, 6486; merge `c3bd1bd51`: 4161-4164, upstream's `if continuing: usage = merge_usage(...)` moved above the `chat:completion` event)
- `src/lib/components/chat/Chat.svelte`: 85-88, 90-91, 514-518, 520-589, 591-596, 599-611, 617-622, 628-658, 661-670, 672-686, 689-691, 697-715, 1049-1050, 1176, 1814, 1843-1847, 1887, 2888, 3156, 3246-3250, 3788, 3842, 3851-3852, 4430, 4812, 4823, 4921, 4939, 5067-5068, 5707, 5775, 5877 (merge `c3bd1bd51`: 1046-1048, 1051-1052, the model-change watcher; 3307-3313, the pending-usage clear in the task reconciliation)
- `src/lib/components/chat/MessageInput.svelte`: 176, 602-625, 627, 629-632, 635-643, 645-648, 2897-2952
- `src/lib/components/chat/Messages.svelte`: 42, 238, 275, 315, 375, 392-393, 395-405, 419, 489 (merge `c3bd1bd51`: 550)
- `src/lib/components/chat/Messages/Message.svelte`: 26, 139
- `src/lib/components/chat/Messages/MultiResponseMessages.svelte`: 42, 99, 115, 131, 199
- `src/lib/utils/modelContextUsage.ts`: 1-3, 5-22, 24-66, 81-105, 108-132, 140-142 (new; the rest is `622272b51`)
- `src/lib/utils/modelContextUsage.test.ts`: 1-6, 10-46, 48-74, 76-92, 143 (new; the rest is `622272b51`)
- `src/lib/i18n/locales/*/translation.json` (63 files): keys `Context Window:`, `Used {{inputTokens}} / {{contextWindow}} tokens`, `Used {{usedPercent}}% ({{remainingPercent}}% remaining)`

`622272b51` (at `crystalvibe28/main @ 1ade36b39`, merged by `06369d6fc` on 2026-10-12)

- `backend/open_webui/utils/middleware.py`: 3949-3961, 3965, 4160, 4173
- `backend/open_webui/utils/response.py`: no surviving lines (superseded by upstream's `merge_usage`, see "Status")
- `src/lib/components/chat/Chat.svelte`: 89, 519, 590, 597-598, 612-616, 623-627, 659-660, 671, 687-688, 692-696
- `src/lib/components/chat/MessageInput.svelte`: 86-90, 626, 628, 633-634, 644
- `src/lib/utils/modelContextUsage.ts`: 4, 23, 67-80, 106-107, 133-139
- `src/lib/utils/modelContextUsage.test.ts`: 7-9, 47, 75, 93-142
- `scripts/test-model-context-usage.py`: 1-16, 18-73 (new; standalone `unittest`, standard library only; merge `c3bd1bd51`: 17, `usage_counter` added to the extracted names)

**Merge notes**

- `Chat.svelte` and both response handlers in `middleware.py` change in almost every upstream release, and this patch has many scattered call sites there. After a merge, check the begin / record / commit / hydrate / clear calls, the `onBranchChange` plumbing and the `capabilities.usage === true` condition.
- In `non_streaming_chat_response_handler`, `usage = normalize_usage(...)` must stay after upstream's `if continuing:` block and before the `chat:completion` event, which includes `usage`. This spot conflicted when `622272b51` was merged, and again in the `v0.12.0` merge, where upstream added `finish_reason = ...` next to its own `usage =` line below the event. Keep `finish_reason` there and do not bring the second `usage =` back.
- Call sites in `Chat.svelte` that were re-placed in the `v0.12.0` merge, because upstream rewrote the code around them for shared chats and the realtime voice bridge:
  - `chatCompletionEventHandler`, `if (done)`: `commitCompletedModelContextUsage(message)` and `settleModelContextUsage(message)` must run before upstream's early returns (`if (shared) return;` and the `message.error` branch). Otherwise a failed reply never settles its pending usage.
  - `stopResponse(processQueue, messageId)`: `clearPendingModelContextUsage()` comes after upstream's ownership check, so stopping someone else's reply in a shared chat does not clear local state. It still clears every pending entry. Since `v0.12.2` it sits directly before upstream's `voice:cancel_animation` dispatch; the two lines conflicted in that merge, keep both.
  - `handleOpenAIError` is now synchronous and builds the message with `getErrorMessage`; `clearPendingModelContextUsage([responseMessage.id])` is its first line.
  - `chat:message:error`: the clear is the first line of the branch. `chat:tasks:cancel`: the clear follows upstream's `if (!event.shared) dismissContextCompactionToast();`.
  - `loadChat`: the clear for the current message comes before upstream's loop that marks every interrupted assistant message as done.
- Call sites in `Chat.svelte` that conflicted in the `v0.12.3` merge:
  - `continueResponse(message)` now takes the message to continue and checks `history.messages[message.id]` instead of `history.currentId`. `beginModelContextUsage(responseMessage)` and `delete responseMessage.error` sit directly inside upstream's condition, in that order (`beginModelContextUsage` skips a message that still has `error`).
  - `initEmbeddedDraft`: `clearModelContextUsage()` and upstream's `terminalContext = null;` are both the first lines; keep both.
- In `v0.12.3` upstream moved the Responses API stream handling out of `middleware.py` into `handle_responses_streaming_event` in `utils/response.py`. The checkpoint calls stayed in `middleware.py` and merged without a conflict.
- Upstream has its own, unrelated context panel in `MessageInput.svelte` (`contextUsage`, `statusContextUsage`, used for compaction). It coexists with this patch's `modelContextUsage` meter; do not merge the two. In `v0.13.0` it gained a live estimate (`src/lib/utils/contextUsage.ts`, `captureUsageCheckpoint` / `estimateUsageGrowth`), still measured against the compaction threshold rather than the model's context window. `captureUsageCheckpoint(message)` sits directly after the fork's `recordModelContextUsage(message, usage)` in `chatCompletionEventHandler`; keep both.
- `merge_usage` in `utils/response.py` is a core upstream helper. Since `v0.13.0` upstream keeps the `prompt_tokens` / `completion_tokens` aliases at the latest call's value, which the checkpoint reads first. If upstream ever changes that, the checkpoint starts reading cumulative values; `scripts/test-model-context-usage.py` catches it.
- Call sites that conflicted in the `v0.13.0` merge:
  - Upstream removed the `selectedModelIds` watcher that called `onSelectedModelIdsChange()` / `resetInput()` (`3aaecdd0e`; model defaults are now applied by `setDefaults`). The fork keeps its own small watcher (`modelContextUsageModelIds`) that only drops the committed and preview usage when the selection changes.
  - `initEmbeddedDraft`: upstream's `startChatLoad(); modelDefaults = null;` come first, then `clearModelContextUsage()`.
  - `chat:tasks:cancel`: upstream replaced `dismissContextCompactionToast()` with `clearContextCompaction(event.message_id)`; the fork's `clearPendingModelContextUsage(...)` follows it.
  - `loadChat` task reconciliation: upstream wrapped it in `if (taskIds === activeTaskIds)`; the fork's clear sits right after `taskIds = null;` inside it.
  - `if (done)` in `chatCompletionEventHandler`: the fork's commit / settle calls come before upstream's new `clearContextCompaction` line and before the early returns.
  - `middleware.py`, non-streaming: upstream added `if continuing: usage = merge_usage(previous, usage)`. The merge moved it above the `chat:completion` event, so the event and the stored message carry the same usage. Streaming: upstream renamed the parameter of `stream_body_handler` to `current_form_data`, sets `form_data['model']` from `selected_model_id`, and now tracks `current_usage` per call; the fork's `nonlocal` lines and `has_selected_model_id = True` stay.
- The frontend still adds `stream_options.include_usage` only when `capabilities.usage === true`. Since before `v0.12.3` upstream also adds it in `main.py` when `capabilities.usage` is truthy, so the frontend condition is now redundant but harmless.
- After an upstream merge, run `npx vitest run src/lib/utils/modelContextUsage.test.ts` and `python scripts/test-model-context-usage.py`. The script extracts named functions from `response.py` and `middleware.py` with `ast`; when upstream adds a helper those functions call (as `usage_counter` in `v0.13.0`), add its name to the list.

---

### 4. Fork version suffix

**What it changes**

- The version is `<upstream version>+crystalvibe28.<N>`, hand-edited in three places: `package.json` (`version`) and `package-lock.json` (top level and `packages[""]`). `pyproject.toml` and `CHANGELOG.md` are not touched.
- Current value on `crystalvibe28/main`: `0.13.0+crystalvibe28.3`.
- Releases were tagged with lightweight tags on the merge commit: `v0.11.0+crystalvibe28.1`, `v0.11.0+crystalvibe28.2`.

**Why**

- The version must show which official release the fork is based on while staying distinct from official numbers. The fork keeps merging upstream releases, so it cannot invent numbers such as `0.11.1`.
- `npm version` strips `+…` build metadata, hence the manual edit.
- Container tags cannot contain `+`, so the image workflow (patch 5) publishes the tag with `+` replaced by `-`.

**Branch:** `crystalvibe28/dev` (merged into `crystalvibe28/main`)

**Commits**

- `ac7a62d95` (2026-08-14) `chore(release): bump version to 0.11.0+crystalvibe28.1`
- `f249ab0f4` (2026-08-14) `chore(release): bump version to 0.11.0+crystalvibe28.2`

**Files and line ranges** (at `crystalvibe28/main @ 1ade36b39`)

- `package.json`: 3
- `package-lock.json`: 3, 9
- These lines are now attributed to merge `c3bd1bd51` (`Merge tag 'v0.13.0'`), where the suffix was re-applied with `<N>` kept at `3`. (`<N>` went from `2` to `3` in merge `cbd352c23`, `v0.12.0`.)

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

**Files and line ranges** (at `crystalvibe28/main @ 1ade36b39`)

`808e1b4d5`

- `.github/workflows/docker-image-build.yaml` (was `docker.yaml`): 1, 5-6, 9, 17, 26-32, 35, 46-49, 56, 62-65, 69-71 (merge `cbd352c23`: 68, the `BUILD_CHANNEL=main` build-arg). Treat the whole file (1-71) as fork-owned.
- `.github/workflows/backend.disabled` (was `backend.yaml`): 1
- `.github/workflows/frontend.disabled` (was `frontend.yaml`): 1
- `.github/workflows/issue-label.disabled` (was `issue-label.yaml`): 1
- `.github/workflows/release-pypi.disabled` (was `release-pypi.yml`): 1
- `.github/workflows/release.disabled` (was `release.yml`): 1

`036b4d6ba`

- `.github/workflows/docker.yaml` → `.github/workflows/docker-image-build.yaml` (pure rename)
- `.github/workflows/release.disabled`: 85

**Merge notes**

- Upstream edits to the renamed workflows surface as rename or modify/delete conflicts. Keep the `*.disabled` names and make sure no `docker.yaml` comes back.
- When upstream changes `docker.yaml`, check whether the change belongs in `docker-image-build.yaml` too. In `v0.12.0` upstream added a `BUILD_CHANNEL` build-arg (`51f0e0125`) that the `Dockerfile` passes to the frontend build as `APP_BUILD_CHANNEL`; the fork's workflow sets it to `main`. The same release renamed the image's `WEBUI_BUILD_VERSION` environment variable to `WEBUI_BUILD_HASH`.
- `v0.12.2` changed only `release.yml` (it shortens over-long release notes). Git followed the rename and applied it to `release.disabled`, which stays disabled; nothing was needed in `docker-image-build.yaml`.
- `v0.12.3` changed no workflow.
- `v0.13.0` changed only `release-pypi.yml` (Python 3.11 → 3.12). Git applied it to `release-pypi.disabled`, which stays disabled; nothing was needed in `docker-image-build.yaml`.
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

**Files and line ranges** (at `crystalvibe28/main @ 1ade36b39`)

- `src/lib/components/chat/MessageInput.svelte`: 1030
- `src/lib/components/chat/chatScroll.test.ts`: 1-22, 24-35, 55-74, 79-83 (new; merge `ec3b1c2c1`: 23, 36-54; merge `c3bd1bd51`: 75-78)
- `src/lib/components/chat/Chat.svelte`: no surviving lines (the added `scheduleResponseScrollToBottom();` call was replaced by upstream's `autoScrollToBottom`)

**Merge notes**

- Keep `behavior: 'auto'` in `scrollToBottom` of `MessageInput.svelte`.
- The test depends on the declaration names `responseCompletionEventHandler`, `shouldAutoScrollResponse`, `autoScrollToBottom` and `scrollRAF` in `Chat.svelte`. An upstream rename breaks it.
- The test runs `scrollToBottom` in a `vm` context, so every free variable it reads must be in that context. `v0.13.0` made it read the `messagesContainerId` prop; the merge added that name to the context.

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

**Files and line ranges** (at `crystalvibe28/main @ 1ade36b39`)

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
   - `routers/comments.py` (`f5bccff0f`): `GET /comments/mentions` only offers users the caller can see (an `IN` filter on the visible ids inside the SQL query, so the 40-candidate limit is not used up by hidden users). Creating, replying to and editing a comment run `require_visible_mentions`: a mention added by that request must name a visible user, or the request gets 404. Mentions already in the comment before an edit are not re-checked.
2. **Response sanitiser.** `UserVisibilityMiddleware` (`user_visibility_middleware.py`, registered in `main.py` so that it runs inside response compression) buffers 2xx JSON responses for non-admins and passes them through `sanitize_user_payload` (`user_visibility_payload.py`). That function nulls hidden user objects (`user`, `owner`, `author`, …), blanks hidden id fields (`user_id`, `created_by`, …), filters `users` / `members` / `user_ids` lists, rewrites `<@U:id|…>` mentions to `@Unknown` and profile image URLs to `/user.png`, and limits `groups`, `group_ids` and `access_grants` to the viewer's own groups.
3. **Sockets.** `PrivacyAsyncServer` in `socket/main.py` replaces the `sio` server. For `events:channel`, `events:note` and `ydoc:*` events it emits a separately sanitised copy to each recipient. Yjs handlers take `user_id` / `user_name` from the authenticated session instead of client data.
   - Shared chat events (`aef77fe61`): an `events` payload with `shared: True` that carries `user_id` or `user` (typing, and the reply events mirrored to the `chat:{id}` room) is no longer broadcast to the room. `_emit_shared_chat` sends each session in the room its own copy through `sanitize_user_payload`, so a viewer who may not see the acting user gets `user: null` and `user_id: ''`; the frontend already ignores a typing event without a user. Sessions come from the local room plus, with the Redis manager, the `chat_ids` index in `SESSION_POOL`. Each viewer's policy is cached for `SHARED_CHAT_POLICY_TTL` (5 seconds), because a streamed reply produces several events per second. `events` payloads without those fields, such as `chat:access` and every non-shared event, pass through unchanged.
   - Shared chat presence (`6c8cc8d02`): upstream's `chat:presence` event (`publish_chat_presence`, `v0.12.3`) lists every viewer of a shared chat as `{id, name}` in `data.data.users`. It takes the same per-viewer path, so each viewer's list keeps only the users they may see.
   - Note presence (`732bcd0a6`): upstream's `note:presence` event (`publish_note_presence`, `v0.13.0`) lists every viewer of a note as `{id, name, …location}` in `users`, sent to the `note:{id}` room. It now takes the `events:note` path: recipients are the room's sessions plus the sessions with the note in `SESSION_POOL[sid]['note_ids']`, each must still be able to read the note, and each gets a copy whose `users` list keeps only the users they may see.

Supporting changes:

- Sharing: in `utils/access_control/__init__.py`, `separate_hidden_access_grants(user_id, user_role, access_grants, existing_grants)` rejects (404) grants to users or groups a non-admin cannot see, and takes the stored grants the caller cannot see out of the list so they can be re-added unchanged. Both public entry points take `existing_grants=` and use it: `filter_allowed_access_grants` (create, silently drops audiences the caller may not grant) and `validate_access_grants` (update, 403 when any audience is not allowed). The policy itself is upstream's, renamed `_filter_access_grants_by_policy` and otherwise unchanged. Every `/access/update` endpoint passes `existing_grants`; create endpoints do not need it.
- Search: the owner-name match in `models/{knowledge,models,prompts,skills}.py` is AND-ed with the visible user ids, so a search cannot reveal hidden owners.
- Builtin tools: `search_channel_messages`, `view_channel_message` and `view_channel_thread` in `tools/builtin.py` apply the same rules, so a model cannot leak identities.
- Workspace search (`6736092e2`): upstream's `GET /api/v1/search` (`routers/search.py`, `v0.12.3`) titles a channel-message result with the author's name and names a DM after its members, as plain strings the sanitiser cannot recognise. `search_workspace` now checks each message author against `UserVisibility.for_channel` (cached per channel) and shows `Unknown User` when the author is hidden; DM names leave out inactive members for non-admins, as the DM rule does. Mentions in the snippet are still rewritten by the middleware, with the viewer's group-based set.
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
- `6c8cc8d02` and `6736092e2` close two paths that upstream `v0.12.3` opened, found while analysing that merge (2026-10-17): shared chat presence sent every viewer's id and name to the whole room, and the new workspace search showed the authors of public-channel messages to users outside their groups. Both were confirmed with a throwaway script against a temporary SQLite database before and after the fix.
- `732bcd0a6` and `f5bccff0f` close two paths that upstream `v0.13.0` opened, found while analysing that merge (2026-11-05): note presence sent every viewer's id and name to everyone who has a note open (a publicly readable note joins people from different groups), and the new comment threads offered every user who can open the resource as a mention candidate, which for a public model, prompt or note is every account. The presence leak was confirmed with a throwaway script against a temporary SQLite database before the fix; after the fix that script and the mention checks pass. Comment authors (`user`, `user_id`), notification actors (`actor`, `actor_id`) and `<@U:…>` mentions in comment text were already handled by the sanitiser, and the `comments:changed` / `notifications:changed` socket signals carry no identities.

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
- `6c8cc8d02` (2026-10-18) `fix: sanitize chat presence for each viewer`
- `6736092e2` (2026-10-18) `fix: hide search result authors outside the viewer's scope`
- `732bcd0a6` (2026-11-06) `fix: sanitize note presence for each viewer`
- `f5bccff0f` (2026-11-06) `fix: limit comment mentions to users the author can see`

**Files and line ranges** (at `crystalvibe28/main @ 1ade36b39`)

`3656be046` — core

- `backend/open_webui/utils/user_visibility.py`: 1-5, 27-31, 37-46, 48-69, 71-82, 85-86, 88-98, 100-104, 106-107, 109-112, 114-126 (new)
- `backend/open_webui/utils/user_visibility_middleware.py`: 1-98 (new)
- `backend/open_webui/utils/user_visibility_payload.py`: 1-27, 29, 34-42, 44-45, 48-49, 52-55, 60-81, 84-88, 99-102, 104-124, 127-128, 132-134, 136-148 (new; merge `1de5f4cbd`: 46-47, `'app'` added to the exempt roles)
- `backend/open_webui/utils/access_control/__init__.py`: 327-328, 335, 365 (merge `c3bd1bd51`: 233, 288-326, 329-334, 336-337, 340-364, 366, 374, 377-385, 388 — the rewrite on top of upstream's `v0.13.0` policy: `_filter_access_grants_by_policy`, `separate_hidden_access_grants`, and the `existing_grants` wrappers `filter_allowed_access_grants` / `validate_access_grants`)
- `backend/open_webui/main.py`: 224, 773-774
- `backend/open_webui/socket/main.py`: 63-64, 110-126, 145, 148-283, 285-307, 351, 369, 385, 771-777, 810-811, 898, 931, 942, 1022, 1303, 1525 (merge `cbd352c23`: 807)
- `backend/open_webui/tools/builtin.py`: 30, 1936-1942, 1968, 1970-1972, 1975-1979, 2018-2024, 2061-2063, 2088-2094, 2146-2155

`3656be046` — routers

- `backend/open_webui/routers/users.py`: 17, 19, 23, 25-26, 28, 52, 150, 158, 160-162, 802-805, 807-810, 812-813, 816, 846-857, 861, 866, 868, 899-902, 904-905
- `backend/open_webui/routers/channels.py`: 65, 154-166, 169-193, 239, 254, 256, 264, 304-310, 367-369, 469-471, 479, 512-520, 613-615, 630, 633, 637-639, 750-751, 1181-1185, 1196-1198, 1288-1289, 1299-1301, 1368-1371, 1384-1385, 1474-1477, 1843-1846 (merge `c3bd1bd51`: 885, `existing_grants=` in `update_channel_access_by_id`)
- `backend/open_webui/routers/knowledge.py`: 36, 50-51, 1231, 1299-1306, 1308
- `backend/open_webui/routers/groups.py`: 33, 127-128
- `backend/open_webui/routers/auths.py`: 1136-1142
- `backend/open_webui/routers/models.py`: 1255
- `backend/open_webui/routers/notes.py`: 641
- `backend/open_webui/routers/prompts.py`: 458
- `backend/open_webui/routers/skills.py`: 438
- `backend/open_webui/routers/tools.py`: 769
- `backend/open_webui/routers/calendar.py`: no surviving lines (merge `c3bd1bd51`: 463-468, the `validate_access_grants` call in `update_calendar_access_by_id`)
- `backend/open_webui/routers/chats.py`: 2134
- `backend/open_webui/routers/folders.py`: 548
- In knowledge, models, notes, prompts, skills, tools, chats and folders the listed line is the `existing_grants=` argument of the `validate_access_grants` call in the `/access/update` endpoint; git attributes it to `3656be046` because the text is unchanged.

`3656be046` — models

- `backend/open_webui/models/knowledge.py`: 30, 288-298, 303
- `backend/open_webui/models/models.py`: 20, 520-530, 535
- `backend/open_webui/models/prompts.py`: 21, 305-314, 320
- `backend/open_webui/models/skills.py`: 296-305, 311 (merge `cbd352c23`: 16)

`3656be046` — frontend

- `src/lib/apis/users/index.ts`: 335, 338-341, 522, 525-528
- `src/routes/+layout.svelte`: 921, 934-936
- `src/lib/components/channel/Channel.svelte`: 226, 269
- `src/lib/components/channel/ChannelInfoModal/UserList.svelte`: 272-278, 281
- `src/lib/components/channel/MessageInput.svelte`: 1004
- `src/lib/components/channel/MessageInput/MentionList.svelte`: 9 (merge `c3bd1bd51`: 279, the user avatar with `?channel_id=`)
- `src/lib/components/channel/Messages.svelte`: 105
- `src/lib/components/channel/Messages/Message.svelte`: 397, 440, 444, 448-453, 468 (merge `1de5f4cbd`: 559; merge `c3bd1bd51`: 519-520, 522, 526-531, the author avatar branch with `channelId`, `?channel_id=` and the `/user.png` fallback; merge `f1f2b8738`: 698-703, the message body `Markdown` with `channelId`)
- `src/lib/components/channel/Messages/Message/ProfilePreview.svelte`: 21 (merge `1de5f4cbd`: 65)
- `src/lib/components/channel/Messages/Message/UserStatus.svelte`: 32 (merge `cbd352c23`: 91)
- `src/lib/components/channel/Messages/Message/UserStatusLinkPreview.svelte`: 9, 22-24, 26-30, 32-34, 36, 59 (merge `1de5f4cbd`: 43-44)
- `src/lib/components/channel/Navbar.svelte`: 108
- `src/lib/components/channel/Thread.svelte`: 107, 146
- `src/lib/components/chat/Messages/Markdown.svelte`: 34-35, 43, 76-79
- `src/lib/components/chat/Messages/Markdown/MarkdownInlineTokens/MentionToken.svelte`: 22, 30, 137 (merge `1de5f4cbd`: 5-6, 10, 126, 183)
- `src/lib/components/layout/Sidebar/ChannelItem.svelte`: one unused import removed; no added lines

`dae17c8ff`

- `backend/open_webui/models/groups.py`: 326-330
- `backend/open_webui/routers/users.py`: 143, 149
- `backend/open_webui/utils/user_visibility.py`: 84 (the rest was folded into `is_open_channel` by `5297d1781`)
- `src/lib/apis/users/index.ts`: 202-203, 211
- `src/lib/components/channel/MessageInput/MentionList.svelte`: 61, 76-88

`d8be77741`

- `backend/open_webui/utils/user_visibility_payload.py`: 43, 50-51, 103

`aef77fe61`

- `backend/open_webui/socket/main.py`: 106-109, 129-132, 138-144, 308-350

`fdc4598d4`

- `backend/open_webui/utils/user_visibility_payload.py`: 28, 30-33, 56-59, 82-83, 89-98, 125-126, 129-131, 135
- `backend/open_webui/utils/access_control/__init__.py`: no surviving lines (the `None` handling lives on in the `v0.13.0` rewrite)

`5297d1781`

- `backend/open_webui/utils/user_visibility.py`: 6-26, 32-36, 47, 70, 83, 87, 99, 105, 108, 113
- `backend/open_webui/routers/users.py`: 159, 179-180
- `backend/open_webui/routers/channels.py`: 64, 167-168, 1290-1298, 1382, 1409. It also removes the "no group, public channel" early return from `get_channel_visible_user_ids`.

`4ee44089c`

- `backend/open_webui/routers/chats.py`: 49-50, 989, 997-999, 1003, 1013-1018, 1031
- `backend/open_webui/routers/calendar.py`: 30, 85-96, 296-297, 353-355

`6a03dd13d`

- `src/lib/components/chat/Messages/UserMessage.svelte`: 71-72
- `src/lib/components/layout/Sidebar/ChannelItem.svelte`: no surviving lines (merge `1de5f4cbd`: 96, 98 — upstream moved the DM avatar out of the link and wrapped it in `ProfilePreview`; the merge re-added `channelId` and `?channel_id=` there)
- `src/lib/components/layout/Sidebar/RecursiveFolder.svelte`: 173, 422

`6c8cc8d02`

- `backend/open_webui/socket/main.py`: 127-128, 133-137

`6736092e2`

- `backend/open_webui/routers/search.py`: 6, 20, 172-183, 188, 195-198, 462-464, 468

`732bcd0a6`

- `backend/open_webui/socket/main.py`: 146-147, 284

`f5bccff0f`

- `backend/open_webui/routers/comments.py`: 21, 56-64, 100, 110, 184, 271, 332

**Merge notes**

- This is the largest and most conflict-prone patch, and it has **no automated tests** (the tests written during development were removed before the commit). After every upstream merge, re-check by hand as a non-admin user: user search, mention lists, channel member lists, the add-member dialog and profile previews. Since `v0.12.0` also check a shared chat with "Allow replies" (typing line, sender names) and the version history of a shared model, tool or skill. Since the 2026-10-12 audit also check: "Export All Chats" after cloning someone else's shared chat, `@model` in a public channel, the sidebar avatar of a DM with someone outside the viewer's groups, and the Tools page (it must not return 500).
- Since `v0.12.2` also check channel apps: an app's messages and replies keep their author for a non-admin.
- Since `v0.12.3` also check the global search (`Ctrl+K`): a message by a user outside the viewer's groups in a public channel is titled `Unknown User`, and two viewers of the same shared chat from different groups do not see each other in the presence list.
- Since `v0.13.0` also check: two viewers of a public note from different groups do not see each other in the note's presence avatars; with Comments enabled (`ENABLE_COMMENTS`), the `@` picker in a comment on a public model lists only same-group users and admins; and the sharing dialog of a model shared by an admin with another group keeps that grant after a non-admin owner saves it.
- The second-audit commits were checked by reading the code, by a throwaway script against `sanitize_user_payload` / `UserVisibility.load`, and by `npm run build`. They were not exercised against a running server.
- Upstream code added later is not covered automatically:
  - A new endpoint or socket event that returns user data needs an explicit check. The sanitiser only recognises the field names listed above.
  - A new endpoint that replaces stored grants (`validate_access_grants`, or `filter_allowed_access_grants` on an existing resource) must pass `existing_grants`. `v0.13.0` added two such endpoints without a conflict (`update_channel_access_by_id`, `update_calendar_access_by_id`); the merge added the argument by hand.
  - A response that is not `application/json` (NDJSON, SSE, a download) skips the middleware. The two that carry identities sanitise by hand: the chat export in `routers/chats.py` and the pending-file stream in `routers/knowledge.py`.
  - A new input that takes user ids (like calendar `attendees`) needs its own `visibility.require_user` check; the grant filter only covers `access_grants`.
- `model_response_handler` in `routers/channels.py` is upstream code with the fork's naming woven in (`author_label`, the `is_open_channel` switch, `visibility.filter_users`). If upstream rewrites how the thread history is built, re-apply all three, or a public-channel reply can name users its readers may not see. The chat completion it starts still runs as the caller, so a model system prompt that uses `{{USER_NAME}}` is outside this protection.
- Known and left alone: the Overview graph labels user nodes with the viewer when the chat owner is hidden; workspace cards show "Deleted User" for a hidden author; `/api/usage` exposes the instance-wide active user count to every user unless `ENABLE_PUBLIC_ACTIVE_USERS_COUNT=false`; the channel typing event forwards client-supplied data.
- `app.add_middleware(UserVisibilityMiddleware)` must stay registered before `CompressMiddleware`, so it sees uncompressed JSON.
- Both `sio = socketio.AsyncServer(...)` constructors (Redis and non-Redis) must stay `PrivacyAsyncServer`. Since `v0.12.0` the Redis one picks its manager class through `WEBSOCKET_REDIS_ROOM_CHANNELS` (`AsyncRedisRoomChannelManager`). `PrivacyAsyncServer` with that manager has not been tested.
- `SESSION_POOL` entries must be written by merging into the existing entry (`{**(SESSION_POOL.get(sid) or {}), **…}`) in `connect`, `user_join` and `heartbeat`. Upstream rebuilds the entry and keeps only `chat_ids`, which drops the `channel_ids` and `note_ids` that `PrivacyAsyncServer` uses to find recipients on other workers. These three spots conflicted in the `v0.12.0` merge; keep upstream's `token` in `save_session` and its `LOCAL_AUTHENTICATED_SIDS.add(sid)`.
- `enter_room_for_users` uses upstream's permission loop (`028dab8f1`: users without the Channels permission do not join) with the fork's `get_session_ids_by_user_id` lookup and `remember_session_resource` call.
- Nested groups (`v0.12.0`, `d4c561d9f`). Upstream's access checks count inherited membership (`include_inherited=True`), but this patch deliberately keeps direct membership (decided 2026-10-12): `UserVisibility.load`, the group check in `require_channel_user_ids_visible`, the unconditional `member_id` filter in `Groups.get_groups` and `GET /users/groups` all use it, so the sharing dialog, the grant filter and the sanitiser agree with each other. The one place that expands inheritance is the member check in `require_channel_user_ids_visible`, and only to refuse: inviting a parent group would add child-group members the caller cannot see. Nothing changes while no group has a parent. Once a parent group is used, the two rules differ: a user who reaches a standard channel only through an inherited grant gets 404 from the channel-scoped user endpoints and no realtime events for that channel, because `UserVisibility.for_channel` passes the direct `group_ids` to `AccessGrants.has_access`. Making visibility follow inheritance is a separate change on `feat/group-user-visibility`.
- Sharing redesign (`v0.13.0`). Upstream moved every grant change out of the resources' `update` endpoints into dedicated `/access/update` endpoints, which call the new `validate_access_grants(..., resource_type=...)` and reject the whole request with 403 if any audience is not allowed. `filter_allowed_access_grants` now takes a `resource_type` (looked up in `_SHARING_PERMISSION_KEYS`) instead of permission keys and is used on create only. Importing an existing model no longer touches its grants (`_write_model` sets grants on insert only). The fork's code was rebuilt on that in the merge:
  - upstream's function body is kept verbatim as `_filter_access_grants_by_policy`; the fork's visibility logic is a separate function, `separate_hidden_access_grants`, called by the two public wrappers;
  - `validate_access_grants` compares the length of what the policy allowed with the caller's grants after the hidden stored ones were taken out, then appends them, so hidden grants never cause a 403;
  - the v0.12.3 pattern of keeping resent stored grants and filtering only new ones (`models.py`, `prompts.py`, `tools.py`) and the grant filter in `_update_tool` are gone with upstream's update code.
    If upstream changes `_filter_access_grants_by_policy` (its `filter_allowed_access_grants`), take the new body as it is and keep the wrappers.
- Comments (`v0.13.0`, `routers/comments.py`, `models/comments.py`, `utils/comments.py`, `socket/comments.py`). Access to a comment thread follows access to the resource (`comment_resource`), so on a public resource people from different groups share a thread. Authors are serialised as `user: {id, name, profile_image_url}` plus `user_id` and go through the sanitiser; `GET /comments/mentions` returns a bare `[{id, name}]` list that the sanitiser cannot recognise, so it filters by visibility itself. Notifications (`routers/notifications.py`, `utils/inbox.py`) carry `actor` / `actor_id`, both sanitiser fields.
- `MentionToken.svelte`: upstream now declares `let openPreview = false` itself. The `v0.12.0` merge left both declarations in place without a conflict, and only the frontend build caught it. Run `npm run build` after every merge. On this machine the build runs out of memory in "rendering chunks" with Node's default heap; set `NODE_OPTIONS=--max-old-space-size=8192` first.
- Since `v0.12.3` `npm run build` first runs `prebuild` (`crypto:verify`, `scripts/encryption/artifact.mjs`), which fails on Windows: it takes the repository root from `new URL(...).pathname` and reads `D:\D:\...`. This is upstream's script and is left alone; on this machine run `npm run pyodide:fetch` and then `npx vite build`.
- Channel apps (`v0.12.2`, `utils/apps.py`, `routers/apps.py`, `socket/apps.py`). App management is admin-only; `socket/apps.py` is an outbound client to the app, not a namespace clients can join. An app's message has `user_id=None` and an author object with `role: 'app'` (`Messages._resolve_user_info`), so `'app'` is in the sanitiser's exempt roles next to `model` and `webhook` (merge `1de5f4cbd`); without it non-admins see app messages without an author. Apps with the `channels:messages:read` scope receive each human author's raw `user_id` (`get_app_message_data`); this is treated as trusted egress to an admin-installed integration and left alone.
- `PrivacyAsyncServer.emit` routes a shared `events` payload through `_emit_shared_chat` when it has a top-level `user_id` or `user`, or when `data.type` is `chat:presence`. A new shared chat event that lists users somewhere else needs to be added there. Events sent to a note room (`events:note`, `note:presence`) go through `_privacy_recipients`; a new note-room event that names users needs to be added to both sets in `emit` and `_privacy_recipients`.
- Since `v0.13.0` upstream itself writes `SESSION_POOL` entries by merging into the existing entry and keeps `note_ids` (plus `note_locations`) up to date in `note:join` / `note:leave`; the three `SESSION_POOL` spots and the `note:join` hunk took upstream's code in that merge.
- `search_workspace` (`routers/search.py`, upstream since `v0.12.3`) builds result titles and DM scope names from `User.name` directly. If upstream adds another result kind that names a person (a chat owner, a note author), it needs the same check.
- Superseded in `v0.13.0`: access-grant updates in `routers/prompts.py` (`v0.12.3`, `5dff6489d`), `routers/tools.py` and `routers/models.py` kept the stored grants a save resends and filtered only new ones. Upstream removed that code with the sharing redesign above.
- `channel/Messages/Message.svelte` (`v0.12.3`): upstream wrapped the message body in `<slot name="content">` and dropped `paragraphTag`. The fallback `Markdown` inside the slot carries `channelId={channel?.id}`; git placed the fork's props on `StructuredOutputRenderer` in the merge, so check that spot after the next merge. The new encrypted-channel page (`channels/[id]/encrypted`) fills the slot with its own `Markdown` with `allowRemoteContent={false}`, which renders mentions as text, and it is limited to DM and private group channels, where the visible set is the channel members.
- `send_notification` (`routers/channels.py`): since `v0.12.2` upstream builds the recipients from the members for group and DM channels, and skips muted members who are not mentioned. The fork's per-recipient `UserVisibility` check and `sanitize_user_payload` of the content sit inside that loop. `update_message_by_id` keeps `require_visible_user_mentions` directly before upstream's `form_data.meta = None`.
- `extract_mentions` (`utils/channels.py`) requires a closing `>` since `v0.12.2`, so `require_visible_user_mentions` ignores a malformed `<@U:id` with no `>`. The sanitiser's mention pattern needs `>` as well, so such text is never rendered as a mention.
- Mention user lookup: since `v0.12.2` `MentionToken.svelte` resolves the user itself through a module-level `loadMentionUser` and hands the result to `UserStatusLinkPreview` (`resolvedUser`, `loadingUser`). The fork passes `$channelContext` into `loadMentionUser` (part of the cache key) and to `getUserInfoById`, and `UserStatusLinkPreview` keeps its `${channelId}:${id}` request key. Without the channel, mentions inside a channel resolve to 404 for non-admins.
- `ProfilePreview.svelte` was rewritten upstream in `v0.12.2` (Svelte 5 snippet, renders the bare slot without a user id); the fork keeps the `channelId` prop and passes it on. The sidebar DM avatar in `ChannelItem.svelte` and the reply avatar in `channel/Messages/Message.svelte` (order: model → app → user → `/user.png`) were re-placed in the same merge.
- Since `v0.12.2` the frontend needs `@codemirror/merge`; run `npm ci` after merging. On this machine Node is newer than `package.json`'s `engines` allow and `.npmrc` sets `engine-strict=true`, so use `npm ci --engine-strict=false`. npm here no longer runs dependency install scripts unless approved (`npm install-scripts`); the `v0.13.0` tests and build passed without them.
- `npx vite build` (after `npm run pyodide:fetch`) rewrites the icons in `backend/open_webui/static/` and `static/pyodide/pyodide-lock.json`. These are build output: restore them with `git restore --worktree` before committing a merge.
- `channel/Messages/Message.svelte` (`v0.13.0`): upstream wrapped the avatar column in `{#if !$$slots.header}` and gave app messages their own `profile_image_url` avatar. The fork's user branch (`{:else if message.user?.id}` with `channelId` and `?channel_id=`, then the `/user.png` fallback) was re-applied inside it. `MentionList.svelte` was restyled (`DropdownMenu`); the user avatar's `?channel_id=` was re-added on upstream's line.
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

**Files and line ranges** (at `crystalvibe28/main @ 1ade36b39`)

- `backend/open_webui/utils/spa_static_files.py`: 1-23 (new)
- `backend/tests/test_spa_static_files.py`: 1-58 (new)
- `backend/open_webui/main.py`: 294 (import). The inline `SPAStaticFiles` class and the `StarletteHTTPException` import were removed.

**Merge notes**

- If upstream edits the inline `SPAStaticFiles` in `main.py`, the merge can bring the class back. Port the upstream change into `spa_static_files.py` and keep only the import in `main.py`.
- This happened in `v0.12.0`: upstream `c94ac152e` (#31631, a reload loop after a server upgrade) gave the inline class a `file_response` that sets `Cache-Control: no-cache` on `*.html`. That is a subset of what `spa_static_files.py` already does (it also covers `version.json`), so the merge dropped the inline class again and nothing had to be ported. The patch is still needed for `version.json`.
