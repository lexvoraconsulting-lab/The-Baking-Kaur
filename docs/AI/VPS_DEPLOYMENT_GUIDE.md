# Running TBK Cake Genome on the Hostinger VPS

Date: 2026-08-20
Purpose: move the Cake Genome pipeline onto the machine where inference actually runs, so the
Phase 1 regression stops depending on a tunnel that drops mid-batch.

**Read step 0 first.** Skipping it produces a VPS checkout without the Phase 1 engine, and the
failure looks like a broken pipeline rather than a missing push.

---

## Why do this at all

The architecture has been split since the beginning:

```
LOCAL WINDOWS                          HOSTINGER VPS
  Claude Code                            Ollama 0.32.14
  TBK repository            <-- gap -->  qwen3.5:4b
  no inference runtime                   no repository
```

Every Phase 1 blocker has been that gap. An SSH tunnel bridges it, but it dropped after image 1 of
the three-image regression and took the batch with it. Putting Claude Code and the repository on
the VPS removes the gap instead of bridging it: Ollama becomes `127.0.0.1:11434` with nothing in
between.

---

## Step 0 — push the work first (**required**)

The local branch is **62 commits ahead of GitHub**. The Phase 1 engine (`ai/cake_genome/`,
`ai/structure_discovery/`, `ai/vision/python/extraction.py`, `taxonomy_digest.py`, the authored
prompt and schemas) is committed locally at `89a3391` but **not on the remote**. A clone would come
back without any of it.

From Windows:

```bash
git push origin feature/vision-engine-v1
```

Verify it landed before going further:

```bash
git rev-list --left-right --count origin/feature/vision-engine-v1...HEAD
# expect: 0   0
```

`live-theme-sync/` (430 files, 6.9 MB) is deliberately excluded — it is a reference snapshot of the
live theme, not source. Decide separately whether to track or ignore it; it is not needed on the VPS.

---

## Step 1 — check what the VPS already has

```bash
ssh <user>@<vps-host>

node --version      # need 18+; Claude Code will not run on older
git --version
python3 --version   # need 3.11+ (the code uses `X | None` syntax and tomllib-era stdlib)
curl -s http://127.0.0.1:11434/api/version    # {"version":"0.32.14"}
ollama list                                    # qwen3.5:4b
free -h && df -h /                             # headroom
```

If Node is missing or old:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Do not reinstall Ollama.** It is already working; that is the whole reason for this move.

---

## Step 2 — install Claude Code on the VPS

```bash
curl -fsSL https://claude.ai/install.sh | bash
# or: npm install -g @anthropic-ai/claude-code

claude
```

First run opens a browser-code authentication flow. It uses **your existing Claude account** — no
separate API key, no extra subscription. On a headless VPS it prints a URL and a code; open the URL
on your laptop, paste the code back.

Claude Code is terminal-only there. If you want an editor over it, VS Code **Remote-SSH** gives you
the full extension against the VPS filesystem.

---

## Step 3 — clone the repository

```bash
cd ~
git clone https://github.com/lexvoraconsulting-lab/The-Baking-Kaur.git
cd The-Baking-Kaur
git checkout feature/vision-engine-v1
```

~9.4 MB packed. Confirm the engine actually arrived:

```bash
ls ai/cake_genome/ ai/structure_discovery/
test -s ai/vision/prompts/extractor_v1.md && echo "prompt present"
```

If `ai/cake_genome/` is missing, step 0 was skipped.

### Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests pydantic pyyaml
```

Verify the port from Windows to Linux — nothing in the pipeline is platform-specific, but prove it
rather than assume:

```bash
python -m ai.taxonomy.test_taxonomy
python -m ai.structure_discovery.test_structure_discovery
python -m ai.cake_genome.test_cake_genome
python -m ai.vision.python.test_config_providers
```

All four should pass. They are offline — no model call, no network.

---

## Step 4 — point the pipeline at the local Ollama

No code change and no edit to a tracked file. `ai/vision/config/vision.json` keeps its localhost
default; the environment supplies the rest (see [Configuration.md](Configuration.md)):

```bash
export OLLAMA_BASE_URL=http://127.0.0.1:11434
export OLLAMA_MODEL=qwen3.5:4b
```

Make it durable for the session:

```bash
echo 'export OLLAMA_BASE_URL=http://127.0.0.1:11434' >> ~/.bashrc
echo 'export OLLAMA_MODEL=qwen3.5:4b'                >> ~/.bashrc
```

Confirm what will actually be called before burning a model run:

```bash
python -c "from ai.vision.python.config import load_config, describe_runtime; \
print(describe_runtime(load_config('ai/vision/config/vision.json')))"
# http://127.0.0.1:11434/api/generate [OLLAMA_BASE_URL] model=qwen3.5:4b [OLLAMA_MODEL]
```

Both values must read `[OLLAMA_BASE_URL]` / `[OLLAMA_MODEL]`. If either says `[vision.json]`, the
export did not take and the run would hit the wrong target.

---

## Step 5 — run the Phase 1 regression

```bash
for i in 1 2 3; do
  python -m ai.cake_genome.run_phase1 \
    --image ai/vision/images/$i.png \
    --out ai/cake_genome/output/vps_00$i
done
```

Each image should report **17/17 gates**. Then check the two things that matter most:

```bash
grep -h prompt_leakage_count ai/cake_genome/output/vps_00*/08_diagnostics.json   # expect 0
git diff --quiet -- ai/taxonomy/ && echo "taxonomy unmutated"
```

Three images at 17/17 with zero leakage converts
[PHASE_1_FINAL_VALIDATION_REPORT.md](PHASE_1_FINAL_VALIDATION_REPORT.md) from **CONDITIONAL PASS**
to **FULL PASS — PHASE 1 LOCKED**.

### Known model behaviour

`qwen3.5:4b` is a **reasoning model**. With Ollama structured output and thinking both enabled it
returns an empty `response` and routes everything into `thinking`. `vision.json` already sets
`"think": false` for exactly this. If a run yields 0-byte responses, that setting is the first
thing to check — see the report's defect D-7.

---

## Security

- **Keep 11434 on loopback.** Ollama should bind `127.0.0.1` only. Do not open it in the Hostinger
  firewall; on the VPS the pipeline is already local to it, so there is nothing to expose.
  Verify: `ss -tlnp | grep 11434` should show `127.0.0.1:11434`, not `0.0.0.0:11434`.
- **The repository has no `.env` file** and no committed token — checked. But `.gitignore`
  currently has **no secret patterns at all**. Before working on the VPS, add:

  ```
  .env
  .env.*
  *.pem
  *_token
  ```

- `SHOPIFY_TOKEN` is not set anywhere and is not needed for Cake Genome. Only add it on the VPS if
  you intend to run `seo-ops/` there, and then via environment only, never a tracked file
  (`CLAUDE.md` golden rule).
- Claude Code on the VPS can read everything in the repo. That is the point, but it means the VPS
  now holds the full project history.

---

## Working across two machines

Two Claude Code sessions on one branch will conflict. Pick one:

| Pattern | Use when |
|---|---|
| **VPS is authoritative** — edit and run there, push, pull down locally | Running regressions, anything touching inference |
| **Local is authoritative** — edit here, push, `git pull` on VPS, run there | Editing with VS Code locally |
| **Split branches** — VPS on its own branch, merge deliberately | Long parallel work |

Whichever you pick, `git pull` before starting on either side. The 62-commit gap in step 0 is what
happens otherwise.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ai/cake_genome/` missing after clone | Step 0 skipped | Push from Windows, `git pull` on VPS |
| `describe_runtime` shows `[vision.json]` | Exports not applied | Re-export; check the shell is not a fresh non-login one |
| 0-byte model response, 7/17 gates | Reasoning model + structured output | Confirm `"think": false` in `vision.json` (D-7) |
| `ConnectionError` on 11434 | Ollama not running | `systemctl status ollama` — do **not** reinstall |
| `ReadTimeout` after 300 s | Cold model load | `timeout` is already 600 with `keep_alive: 30m`; pre-warm with a trivial call |
| Tests pass, run produces 2–3 observations | Model under-reporting | Expected on small models; `qwen3.5:4b` gave 14 on image 1 |

---

## Related

[Configuration.md](Configuration.md) (env overrides),
[PHASE_1_FINAL_VALIDATION_REPORT.md](PHASE_1_FINAL_VALIDATION_REPORT.md),
[VisionExtractionContract.md](VisionExtractionContract.md),
[ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md) (why Python owns the contract and the
runtime host owns execution).
