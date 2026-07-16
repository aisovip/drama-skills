# Drama Skills

[中文](README.md) | English

A filesystem-based Agent Skill suite for vertical short-drama creation,
compatible with Claude Code, Codex, and other runtimes that support Agent
Skills. It distills transferable production know-how into workflows,
references, templates, examples, and review rubrics, covering the full chain
from story development to text delivery.

This repository only produces and manages text, Markdown, JSON, and JSONL:
screenplays, asset decisions, image prompts, storyboard/keyframe prompts,
video prompts, and review evidence. It does not generate images, video, or
audio, and it never calls media-generation services.

## Skills

| Skill | Responsibility |
|---|---|
| `short-drama` | Init, routing, state, recovery, acceptance/review lifecycle, delivery |
| `short-drama-develop` | Story promise, story engine, series arc, episode map |
| `short-drama-write` | Episode contract, causal beats, shootable screenplay, stable index |
| `short-drama-assets` | Character/Look, Location/View, Prop/State, continuity decisions |
| `short-drama-image-prompts` | Asset image prompts and text-treatment policy |
| `short-drama-storyboard` | Coverage, shots, frozen keyframes, spatial boundaries |
| `short-drama-video-prompts` | Performance, action, camera, audio, start/end-state video prompts |
| `short-drama-review` | Structural validation, evidence-based review, revision requests, independent verdicts |

## Install

The eight directories must stay siblings. Copy or link them into your host's
skills directory:

```bash
# Claude Code
mkdir -p "$HOME/.claude/skills"
for skill in skills/*; do
  ln -s "$PWD/$skill" "$HOME/.claude/skills/$(basename "$skill")"
done

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
for skill in skills/*; do
  ln -s "$PWD/$skill" "${CODEX_HOME:-$HOME/.codex}/skills/$(basename "$skill")"
done
```

If a skill with the same name already exists, remove the old link or choose
another install location — do not mix versions. After installing, start from
`$short-drama`; specific tasks can also invoke the matching skill directly.

## Workflow

```text
story development (optional) -> episode screenplay -> asset decisions
                                            |-> asset image prompts
                                            |-> coverage -> shots -> keyframes -> video prompts
                                                                       |
                                                       independent review -> text delivery package
```

Image prompts and storyboard can run in parallel once assets are accepted. An
existing screenplay can enter normalization or asset extraction directly —
no story-development files need to be fabricated. Candidate generation,
creator acceptance, independent review, and delivery are separate authorities;
one `accepted` flag cannot impersonate them all.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
ruff check --no-cache .
python3 skills/short-drama/scripts/verify_suite.py
```

Every skill should also pass `quick_validate.py` from `skill-creator` when the
host provides it. The suite manifest is rebuilt before release by
`skills/short-drama/scripts/update_suite_manifest.py`; the seven public child
skills each pin the core manifest through a strictly validated `suite-ref.json`.

## License

MIT — see [LICENSE](LICENSE).
