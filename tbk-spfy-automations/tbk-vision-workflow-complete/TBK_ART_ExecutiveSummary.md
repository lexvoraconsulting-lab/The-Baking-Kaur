# TBK Vision Workflow – ART Framework Executive Summary
## Vision Processing Platform v1.1 | 10-Week Release Train

---

## The Vision

Transform The Baking Kaur's cake catalog from manual photography into an **enterprise-grade, AI-powered image processing pipeline** that:

- **Automates** 95% of metadata generation (colors, decorations, serving size, occasion tags)
- **Reduces** product upload time from 20 minutes to <8 seconds per image
- **Scales** to 1,000+ images per day without manual overhead
- **Ensures** brand consistency through AI quality gates & confidence scoring
- **Provides** audit trails for compliance & troubleshooting

---

## What is ART and Why TBK Needs It?

### The Problem
TBK is growing: from manually uploading 20–50 cakes/week to needing 1,000+/day. This requires:
- **Multiple engineering teams** (input, AI, content, publishing) working in sync
- **Clear handoffs** between stages (upload → validation → Qwen analysis → SEO → publish)
- **Shared accountability** for meeting SLAs (latency, quality, throughput)
- **Risk mitigation** (Qwen API failure, Shopify rate limits, metadata drift)

### The ART Solution
**Agile Release Train** = synchronized 4-team sprint structure with:
- **10-week cycle** (1 PI) = planning week + 5 two-week sprints + release week
- **4 teams** working on sequential pipeline stages
- **Shared metrics** (throughput, latency, error rate) tracked daily
- **Weekly demos** showing end-to-end progress
- **Clear dependencies** managed at standup level

---

## The 4-Team Structure

```
INPUT & VALIDATION (T1)    AI VISION & METADATA (T2)    SEO & QUALITY (T3)    PUBLISH & OPS (T4)
├─ Batch upload          ├─ Qwen2.5-VL inference       ├─ SEO generation     ├─ Shopify API
├─ File validation       ├─ Cake Genome Builder        ├─ Quality gates      ├─ Approval workflow
└─ Duplicate detection   └─ Confidence scoring         └─ Metadata review    └─ Monitoring
     Stages 1–3               Stages 4–5                 Stages 6–7          Stages 8–10
```

| Team | Focus | Deliverable |
|------|-------|-------------|
| **T1** | **Throughput** | 1,000 images/day through pipeline |
| **T2** | **Accuracy** | Qwen latency <2.5s; confidence >0.75 avg |
| **T3** | **Quality** | SEO titles, metadata review, quality gates |
| **T4** | **Reliability** | 99.5% Shopify publish success, audit logs |

---

## Sprint 1 Breakdown (Weeks 1–2)

### Goal: "Build foundational batch processing + AI pipeline orchestration"

#### Team 1: Input & Validation
| Story | Points | Deliverable |
|-------|--------|-------------|
| **VIS-001** Batch upload handler | 5 | Upload 50+ images → Redis queue |
| **VIS-002** Enhanced validation | 3 | Detect duplicates, reject corrupted files |

**Result**: Ready to process 100-image batches; throughput tracking in place.

#### Team 2: AI Vision & Metadata
| Story | Points | Deliverable |
|-------|--------|-------------|
| **VIS-003** Qwen2.5-VL integration | 8 | GPU-based inference; <3s latency |
| **VIS-004** Cake Genome Builder | 5 | 50+ metadata fields with confidence scores |

**Result**: Qwen running on GPU; raw vision data structured for downstream use.

#### Team 3: SEO & Quality
| Story | Points | Deliverable |
|-------|--------|-------------|
| **VIS-005** SEO title generator (MVP) | 5 | AI-generated titles scored >0.70 avg |

**Result**: Titles generated for all cakes from Genome data.

#### Team 4: Publishing & Operations
| Story | Points | Deliverable |
|-------|--------|-------------|
| **VIS-006** Shopify publish skeleton | 3 | Dry-run publish (no live writes yet) |
| **VIS-007** Logging & audit trail | 3 | All images logged through pipeline |

**Result**: Publishing validated; audit logs flowing.

### Sprint 1 Demo (End of Week 2)
**Live**: Upload 10-image batch → Qwen analysis → Genome + title generation → dry-run Shopify publish  
**Metrics**: Latency breakdown, error rate, GPU utilization  
**Logging**: All 10 images traced in ELK  

---

## Qwen Integration: The AI Heart

### What is Qwen2.5-VL?

State-of-the-art vision-language model (8B parameters) that analyzes cake images and extracts:

| Input | Output |
|-------|--------|
| Cake image (JPEG/PNG) | `{ "layers": 3, "frosting_type": "fondant", "decorations": ["flowers", "beads"], "colors": ["white", "pink"], "quality_score": 0.91, ... }` |

### Deployment Strategy

**Self-hosted GPU** (recommended for TBK):
- **Hardware**: NVIDIA A100 (or A10) GPU + 64GB RAM
- **Cost**: ~$5–10K upfront + $37/month electricity per GPU
- **Throughput**: 1,000+ images/day with batching
- **Privacy**: Images never leave your infrastructure

**How it works**:
1. Batch upload handler (T1) queues 20 images in Redis
2. vLLM server (GPU) pulls images + runs Qwen inference
3. Vision output (~2.3 seconds per image) stored in PostgreSQL
4. Confidence scores propagated downstream to SEO & quality stages

### Latency Optimization

| Strategy | Technique | Latency | Speedup |
|----------|-----------|---------|---------|
| Baseline | Single inference | 2.5s | 1× |
| Quantization | INT8 weights | 1.5s | 1.7× |
| Batching | 4 images parallel | 0.7s per image | 3.5× |
| Caching | Redis cache hits | 0.01s | 250× |

**Sprint 1 target**: <2s latency (p99) on 1,000 images/day

### Fallback Strategy (if Qwen fails)

```
PRIMARY: Qwen (2.5s, 88% accuracy)
↓ [if slow/fails]
FALLBACK: CLIP (1s, 70% accuracy)
↓ [if still fails]
HEURISTIC: OpenCV (0.05s, 30% accuracy)
```

All three models deployed; chain tested weekly.

---

## Success Metrics (End of PI, Week 11)

### Throughput
- **Goal**: 1,000 images/day end-to-end
- **Measurement**: Pipeline logs (images reaching Stage 10 / day)
- **Success**: ≥900 images/day (90% of goal)

### Latency
- **Goal**: <8 seconds per image
- **Breakdown**: 1.5s T1 + 2.5s T2 + 1.5s T3 + 2s T4 = 7.5s
- **Measurement**: Latency histogram in Datadog
- **Success**: p99 <8s, p95 <6s

### Quality
- **Metadata completeness**: ≥95% of fields populated
- **SEO score**: Average >0.75 (on 0–1 scale)
- **Duplicate detection**: <1% false positives
- **Human approval time**: <2 minutes per image (after auto-gen)

### Reliability
- **Error rate**: <2% (max 20 failed images per 1,000)
- **Shopify publish SLA**: 99.5% success
- **Uptime**: 99.9% pipeline availability
- **Audit coverage**: 100% of images logged

### Team Velocity
- **Sprint 1 capacity**: 32 story points
- **Target burn**: 100% per sprint
- **Defect rate**: <5 bugs per sprint (post-demo)

---

## Critical Path & Risk Management

### Dependency Chain

```
VIS-001 (Batch upload)
  ↓ [feeds]
VIS-002 (Validation) + VIS-003 (Qwen) + VIS-006 (Shopify) + VIS-007 (Logging)
                              ↓
                        VIS-004 (Genome)
                              ↓
                        VIS-005 (SEO)
                              ↓
                        Live demo
```

**Critical path**: VIS-001 → VIS-002 → VIS-003 → VIS-004 → VIS-005  
**Bottleneck**: Qwen latency (if >3s, entire pipeline slows)

### Top Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| **Qwen latency > 3s** | Medium | High (blocks release) | CLIP fallback ready; load test GPUs early |
| **Shopify rate limits** | Medium | Medium | Batch writes; exponential backoff; queue retry |
| **Model drift** | Low | Medium | Weekly baselines on new cakes; A/B test updates |
| **Duplicate detection false positives** | Low | Medium | Tune hash algorithm; weekly precision audit |
| **GPU OOM errors** | Low | High (production outage) | Reduce batch size; enable INT8 quantization |

### Escalation Path

- **Blocker during sprint**: Escalate to RTE within 2 hours
- **Metric miss (SLA breach)**: Discuss in daily standup; plan mitigation
- **Incident (production outage)**: War room within 30 minutes; all hands

---

## Roadmap: Next Steps

### Immediate (Sprint 1: Weeks 1–2)
✅ Deploy vLLM + Qwen on GPU  
✅ Batch upload working  
✅ Genome + SEO MVP complete  
✅ Shopify dry-run validated  

### Sprint 2–3 (Weeks 3–6)
- Extend Genome to 300+ fields (500+ by PI end)
- Full SEO suite (description, FAQ, tags, alt text)
- Begin live Shopify publishes (start with 10/day, ramp to 100/day)
- Add human approval workflow (optional gate before publish)

### Sprint 4–5 (Weeks 7–10)
- Scale to 1,000 images/day
- Quality gates enforced (auto-reject metadata confidence <0.6)
- Monitoring & alerting fully automated
- Incident runbook tested

### PI Release (Week 11)
- Process 500 images end-to-end in UAT
- All metrics green: latency, quality, error rate
- Deploy to production (Shopify live)
- Monitor for 24 hours; rollback if SLA breached

---

## Stakeholder Responsibilities

### Release Train Engineer (RTE)
- Owns **flow & impediments**
- Runs daily standups, tracks burndown
- Escalates blockers
- Chairs weekly retrospectives

### Product Manager (PM)
- Owns **roadmap & vision**
- Prioritizes backlog (metadata fields, new validation rules)
- Makes trade-off calls (quality vs. throughput)
- Defines success criteria

### Solution Architect
- Ensures **technical alignment**
- Reviews dependency chains before sprint planning
- Flags tech debt / model replacement decisions
- Mentors teams on ML best practices

### Engineering Leads (T1–T4)
- Own **sprint delivery** for their team
- Forecast capacity & flag risks early
- Mentor engineers on technical excellence
- Participate in dependency sync meetings

---

## Success Criteria at PI End (Week 11)

### Go-Live Readiness (All Must be TRUE)

- [ ] Throughput: ≥900 images/day (90% of 1,000 goal)
- [ ] Latency: p99 <8 seconds end-to-end
- [ ] Quality: ≥95% metadata completeness, avg SEO score >0.75
- [ ] Reliability: <2% error rate, 99.5% Shopify publish SLA
- [ ] Audit: 100% of images logged with confidence scores
- [ ] Team Velocity: All sprints hit ≥80% of committed points
- [ ] Documentation: API docs, runbook, architecture diagram complete
- [ ] Testing: UAT passed with 500+ images; zero critical defects

### If Any Criteria Fails
- **Day 1 of PI+1**: Retro to understand root cause
- **Days 2–5**: Patch plan (assign teams, define stories for next PI)
- **Soft launch**: Deploy to staging + 10% of live traffic (canary)
- **Monitor**: 1 week at canary; if SLA holds, ramp to 100%

---

## Investment & ROI

### Estimated Investment (Sprint 1 + PI)

| Component | Cost | Notes |
|-----------|------|-------|
| **GPU hardware** | $5–10K | A100 or A10; amortized over 3 years |
| **Engineering** | ~$200K | 4 teams × 8 weeks × $50/hr average load |
| **Infrastructure** | $3K/month | GPU compute, Postgres, Redis, S3, ELK |
| **Tooling** | $1K/month | Datadog, Figma, GitHub, etc. |
| **Total (PI)** | **~$300K** | One-time + recurring |

### Expected ROI

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| **Time per cake** | 20 min (manual) | <8 sec (auto) | 99.3% ↓ |
| **Operator FTE needed** | 1 FTE/day | 0.1 FTE/day | 0.9 FTE/year → $80K+ |
| **Throughput** | 50 cakes/day | 1,000 cakes/day | 20× capacity |
| **Human review time** | N/A | 2 min/cake | Focused on quality, not data entry |
| **Error rate** | ~5% | <2% | Better Shopify data quality |

**Payback period**: 6–12 months (GPU + infra costs recouped via labor savings)

---

## Conclusion

The TBK Vision Workflow ART Framework is a **structured, risk-managed approach** to building an enterprise-grade image processing pipeline. By organizing 4 teams around a synchronized 10-week cycle, with clear dependencies, shared metrics, and fallback strategies, we can:

✅ Scale from 50 to 1,000+ images/day  
✅ Reduce manual work by 99%  
✅ Maintain quality with AI confidence scoring  
✅ Ensure compliance with audit trails  
✅ Recover from failures with fallback models  

**Sprint 1 starts now.** All teams deploy in Week 1, demo end of Week 2.

---

## Quick Reference: ART Terminology

| Term | Meaning |
|------|---------|
| **PI** | Program Increment (10-week release cycle) |
| **Sprint** | 2-week iteration within PI |
| **ART** | Agile Release Train (4 teams synchronized) |
| **RTE** | Release Train Engineer (removes impediments) |
| **PM** | Product Manager (owns roadmap) |
| **Velocity** | Story points completed per sprint |
| **Burndown** | Chart showing progress toward sprint goal |
| **SLA** | Service Level Agreement (latency, uptime targets) |
| **Qwen** | Vision-language AI model (Stage 4 checkpoint) |
| **Genome** | Structured metadata object (300+ fields) |

---

## Appendix: Files Delivered

1. **TBK_Sprint1_Stories.md** — Detailed story breakdown for all 7 Sprint 1 deliverables
2. **Qwen_Integration_Guide.md** — Complete Qwen2.5-VL deployment, optimization & fallback guide
3. **TBK_ART_ExecutiveSummary.md** — This document

---

**Questions?** Schedule sync with RTE (Release Train Engineer) or PM (Product Manager).

**Ready to start?** Kick off PI Planning in Week 1.

