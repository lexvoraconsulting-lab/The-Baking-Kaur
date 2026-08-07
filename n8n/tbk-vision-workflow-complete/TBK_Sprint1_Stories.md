# TBK Vision Workflow - Sprint 1 Story Breakdown
## Release Train: Vision Processing Platform v1.1
## Sprint Duration: 2 weeks | Team: All 4 (synchronized delivery)

---

## Sprint Theme
**"Build foundational batch processing + AI pipeline orchestration"**

Goal: Establish end-to-end throughput pipeline with first AI checkpoint operational.

---

## Story Structure Overview

| Team | Story ID | Title | Story Points | Acceptance Criteria |
|------|----------|-------|--------------|-------------------|
| T1 | VIS-001 | Batch upload handler | 5 | Accept 20+ images; validate all; parse metadata |
| T1 | VIS-002 | File validation gate (enhanced) | 3 | Reject corrupted/dupe files; log rationale |
| T2 | VIS-003 | Qwen2.5-VL integration (stage 1) | 8 | API calls working; latency <3s per image |
| T2 | VIS-004 | Cake Genome Builder (skeleton) | 5 | Parse Qwen output; store 50+ core fields |
| T3 | VIS-005 | SEO title generator (MVP) | 5 | Generate titles for 95% of cakes; score >0.6 |
| T4 | VIS-006 | Shopify publish skeleton | 3 | Dry-run publish; validate API auth & schema |
| T4 | VIS-007 | Logging & audit trail | 3 | Record every image through pipeline |

**Total Sprint Capacity**: 32 points (assumes 4 teams × 8 points/engineer capacity)

---

## Team 1: Input & Validation (T1)

### Story VIS-001: Batch Upload Handler
**Story Points**: 5 | **Owner**: T1 Lead | **Priority**: P0 (Blocking)

**Context**
Currently, the system accepts single file uploads. To hit 1,000 images/day, we need batch ingestion. This story establishes the intake API and queuing layer.

**User Story**
> As a Baking Kaur content operator, I want to upload 20+ images in one batch so that I can process daily photo shoots efficiently without waiting for individual upload confirmations.

**Acceptance Criteria**

1. **Batch upload API endpoint**
   - POST `/api/v1/batch-upload` accepts multipart form with up to 50 files
   - Returns batch_id + individual file_ids
   - Each file gets timestamped + source tracked (Upload folder vs. Shopify API)

2. **Async queue integration**
   - Uploaded files placed in queue (Redis or SQS)
   - Each file tagged with batch_id, source, timestamp
   - Queue processes in FIFO order; max 10 concurrent processing threads

3. **Metadata extraction**
   - Extract file name, size, dimensions, color profile
   - Store in PostgreSQL `images` table with status = `queued`
   - Create audit log entry for each upload

4. **Error handling**
   - Reject files >20MB with 413 response
   - Detect duplicate filenames within batch; deduplicate with warning
   - Return 207 Multi-Status response: `{uploaded: [file_ids], rejected: [{file, reason}]}`

5. **Observability**
   - Log batch_id, file count, total size, queue position
   - Emit metric: `batch_upload_files_total` (counter)
   - Emit metric: `batch_upload_queue_depth` (gauge)

**Definition of Done**
- [ ] Unit tests for batch parsing (50+ files, edge cases)
- [ ] Integration test with Redis/SQS
- [ ] Load test: 100 concurrent batch uploads
- [ ] API docs updated (OpenAPI spec)
- [ ] Deployed to staging; T2 can pull from queue

**Tech Notes**
- Use async Python (FastAPI + Celery) or Node.js (Bull queue)
- Database: PostgreSQL (images table schema must include batch_id, source, status)
- Redis (in-memory queue) for speed; failover to SQS if needed
- Monitoring: Prometheus metrics, Datadog logs

**Dependencies**
- None (can work in parallel with other teams)

---

### Story VIS-002: File Validation Gate (Enhanced)
**Story Points**: 3 | **Owner**: T1 Engineer | **Priority**: P0

**Context**
Current validation is basic. Upgrade to catch duplicates (by content hash), corrupted files, and metadata anomalies.

**User Story**
> As a QA engineer, I want the system to automatically detect and reject duplicate images so that we don't process the same cake twice.

**Acceptance Criteria**

1. **File integrity checks**
   - Compute SHA256 hash for each image
   - Query PostgreSQL `image_hashes` table; if hash exists + status = `published`, reject as duplicate
   - If hash exists but status = `failed`, allow retry with warning

2. **Image metadata validation**
   - Check dimensions: reject if < 800×600 (too small for cake details)
   - Check DPI: warn if < 72 DPI (low resolution)
   - Check color profile: convert sRGB if needed; warn if CMYK

3. **Malware scanning** (if not already done)
   - Integrate with ClamAV or VirusTotal API (optional, can defer to Sprint 2)
   - Log scan result; block publish if threat detected

4. **Duplicate detection logging**
   - For each rejected file, log reason + hash to audit table
   - Emit metric: `validation_duplicates_rejected` (counter)

5. **Batch validation summary**
   - After validating all files in batch, return summary:
     ```json
     {
       "batch_id": "abc123",
       "validated": 18,
       "rejected": 2,
       "rejections": [
         {"file": "cake_001.jpg", "reason": "duplicate_hash_exists"},
         {"file": "cake_002.jpg", "reason": "dimensions_too_small"}
       ]
     }
     ```

**Definition of Done**
- [ ] Hash deduplication working in staging
- [ ] Unit tests: duplicate detection, dimension validation
- [ ] Logging verified in audit table
- [ ] Metrics flowing to Datadog
- [ ] Docs updated with duplicate detection behavior

**Tech Notes**
- SHA256 computation on upload (don't wait for Qwen)
- Database: Add `image_hashes` table with (hash, image_id, status, created_at)
- Storage: Images stored in S3/blob with hash-based naming (optional optimization)

**Dependencies**
- Follows VIS-001 (needs batch queue)

---

## Team 2: AI Vision & Metadata (T2)

### Story VIS-003: Qwen2.5-VL Integration (Stage 1)
**Story Points**: 8 | **Owner**: T2 ML Lead | **Priority**: P0 (Blocking)

**Context**
This is the core AI checkpoint. Qwen2.5-VL analyzes cake images and extracts structured vision data. This story gets the model running on GPU with live inference.

**User Story**
> As a data engineer, I want the Qwen2.5-VL model to analyze cake images and return structured vision data so that we have raw material for downstream metadata and SEO generation.

**Acceptance Criteria**

1. **Model deployment**
   - Qwen2.5-VL model (8B parameter version) deployed on GPU (NVIDIA A100 or A10 at minimum)
   - Model loaded at service startup; warmup with 5 dummy images
   - Inference latency: <3 seconds per image (p99 <4s)
   - Batch inference (2–4 images) supported to optimize GPU utilization

2. **Vision API endpoint**
   - POST `/api/v1/vision/analyze` accepts image_id (file already in S3)
   - Returns JSON with structured fields:
     ```json
     {
       "image_id": "abc123",
       "vision_result": {
         "cake_detected": true,
         "confidence": 0.94,
         "cake_types": ["layered", "fondant"],
         "colors": ["white", "pink", "gold"],
         "decorations": ["flowers", "beads"],
         "serving_size_estimate": "24-30 servings",
         "texture_description": "smooth fondant with delicate piping",
         "occasion_tags": ["wedding", "celebration"],
         "quality_score": 0.88,
         "anomalies": []
       },
       "latency_ms": 2340,
       "model_version": "qwen2.5-vl-8b"
     }
     ```

3. **Error handling**
   - If image corrupted or unreadable: return `{cake_detected: false, error: "invalid_image"}`
   - If model timeout (>5s): return error with retry instruction
   - Emit metric: `vision_analysis_latency_ms` (histogram)
   - Emit metric: `vision_analysis_errors_total` (counter)

4. **Retry logic**
   - If inference fails (OOM, timeout), place image back in queue for retry (max 3 attempts)
   - Backoff strategy: exponential backoff (1s, 2s, 4s)

5. **Model versioning**
   - Store model_version in response
   - Support running multiple model versions in parallel (A/B testing)
   - Database: Track model_version per image for audit

6. **Monitoring & observability**
   - Log every inference request: image_id, model_version, latency, confidence
   - GPU memory utilization monitoring (alert if >90%)
   - Model drift detection: track accuracy on historical images monthly

**Definition of Done**
- [ ] Qwen model running on GPU with <3s latency
- [ ] Vision API endpoint tested with 100 images
- [ ] Latency, accuracy, error rate metrics flowing
- [ ] Model warmup working (no cold-start delays)
- [ ] T1 can call endpoint from batch queue
- [ ] Fallback vision model identified (CLIP-based, <1s latency) for outage scenarios

**Tech Notes**
- Model framework: PyTorch or HuggingFace transformers
- Serving: FastAPI + Gunicorn or vLLM (optimized LLM serving)
- GPU: NVIDIA A100 (ideal) or A10 (acceptable)
- Monitoring: Prometheus + Grafana for latency/GPU metrics
- Caching: Optional Redis cache for identical images (compute once, reuse)

**Dependencies**
- Requires VIS-001 (queue) and VIS-002 (validated images)
- Requires GPU infrastructure provisioned + CUDA setup

---

### Story VIS-004: Cake Genome Builder (Skeleton)
**Story Points**: 5 | **Owner**: T2 Data Engineer | **Priority**: P1

**Context**
Qwen outputs raw vision data. The Genome Builder structures this into 300+ metadata fields with confidence scores for downstream use.

**User Story**
> As a content manager, I want vision data transformed into a structured metadata object so that SEO and publishing teams can build product copy with confidence scores attached.

**Acceptance Criteria**

1. **Genome schema definition**
   - Define 300+ fields in a versioned schema (JSON schema v7)
   - Fields grouped by category: `cake_structure`, `decorations`, `flavors`, `occasions`, `serving_info`, `quality_metrics`
   - Each field has: name, type, required (bool), confidence (float 0–1)
   - Example fields:
     - `cake_structure.layers`: integer (Qwen-inferred layer count)
     - `decorations.flowers`: boolean + confidence
     - `serving_info.servings_min / servings_max`: integer range
     - `quality.fondant_smoothness`: float (0–1)

2. **Vision → Genome mapping**
   - Parse Qwen output into Genome fields
   - Propagate Qwen confidence scores to relevant fields
   - If field not detected, set confidence = 0; leave value null
   - Example mapping:
     - Qwen.cake_types → Genome.cake_structure.types
     - Qwen.colors → Genome.appearance.color_palette
     - Qwen.serving_size_estimate → Genome.serving_info.servings_est

3. **Confidence thresholding**
   - Fields with confidence < 0.6 marked as `needs_review`
   - Downstream stages can filter on confidence (e.g., "only use fields with confidence > 0.8 for SEO")

4. **Storage**
   - Genome object stored in PostgreSQL (JSONB column) + MongoDB (optional, for flexible schema evolution)
   - Create table: `cake_genomes` (image_id, genome_data, schema_version, created_at)

5. **Versioning**
   - Schema version embedded in every Genome object
   - Support reading old schema versions (backward compatibility)
   - Migration plan for schema changes (prepare for Sprint 2)

6. **Testing**
   - Unit tests: Qwen output → Genome mapping (50 test images)
   - Verify field types, confidence propagation
   - Edge case: missing Qwen fields → Genome defaults

**Definition of Done**
- [ ] Genome schema (300+ fields) defined in JSON schema
- [ ] Mapping logic implemented & tested
- [ ] Genomes stored in DB with confidence scores
- [ ] Schema versioning in place
- [ ] T3 can read Genomes for SEO generation

**Tech Notes**
- Schema: JSON schema (or Pydantic for Python)
- Storage: PostgreSQL JSONB (with indexes on frequently-queried fields)
- Language: Python (Pydantic dataclass) or TypeScript (Zod)

**Dependencies**
- Follows VIS-003 (needs Qwen output)

---

## Team 3: SEO & Quality (T3)

### Story VIS-005: SEO Title Generator (MVP)
**Story Points**: 5 | **Owner**: T3 NLP Engineer | **Priority**: P1

**Context**
Generate product titles from Genome data using LLM (e.g., GPT-4 or open-source LLaMA). MVP focuses on title only; full SEO suite (description, FAQ, tags) in later sprints.

**User Story**
> As a Shopify product manager, I want AI-generated SEO titles so that cakes are discoverable by customers searching for "fondant wedding cake" or "pink ombre birthday cake."

**Acceptance Criteria**

1. **Title generation endpoint**
   - POST `/api/v1/seo/generate-title` accepts cake_id + Genome object
   - Returns:
     ```json
     {
       "image_id": "abc123",
       "title": "Luxury Fondant Wedding Cake with Pink Ombre Gradient – 24 Servings",
       "title_alt": "Custom Fondant Wedding Cake, Pink Ombre Design, Floral Toppers – 24–30 Guests",
       "seo_score": 0.78,
       "keywords": ["fondant wedding cake", "pink ombre", "luxury", "custom"],
       "rationale": "Includes primary keyword, benefit (luxury), and audience (24 servings)"
     }
     ```

2. **Prompt engineering**
   - Crafted prompt to LLM: input Genome fields (cake type, colors, decorations, servings) → output 2–3 title variations
   - Each title must:
     - Fit within 60 characters (Google SERP limit)
     - Include primary keyword (inferred from cake_structure, decorations)
     - Be compelling & descriptive
     - Avoid keyword stuffing
   - Example prompt:
     ```
     Cake structure: layered fondant, 3-layer
     Colors: pink, white, gold
     Decorations: fresh flowers, pearl beads
     Serving size: 24–30
     Occasion: wedding
     
     Generate an SEO-optimized product title (<60 chars). 
     Include cake type, key decorations, and serving size.
     Avoid jargon; appeal to customers searching for luxury wedding cakes.
     ```

3. **SEO scoring**
   - Score each title on:
     - Keyword relevance (does title mention cake type, color, occasion?)
     - Readability (Flesch-Kincaid grade <= 8)
     - Length (45–60 chars optimal)
     - Uniqueness (no exact duplicates in recent publishes)
   - Formula: `seo_score = (keyword_match × 0.4) + (readability × 0.3) + (length_fit × 0.2) + (uniqueness × 0.1)`

4. **Fallback & defaults**
   - If Genome missing critical fields (cake_structure, colors), use template:
     - `"{cake_type} Cake – {serving_count} Servings"` (e.g., "Fondant Cake – 24 Servings")
   - If LLM fails, return default template with confidence = 0.4

5. **Monitoring**
   - Log: image_id, generated_title, seo_score, model_latency
   - Emit metric: `seo_title_score_distribution` (histogram)
   - Track: how many titles score > 0.75 (quality proxy)

**Definition of Done**
- [ ] Title generator endpoint working with LLM backend
- [ ] 100 test cakes generate titles with avg score > 0.70
- [ ] Fallback templates working for incomplete Genomes
- [ ] Prompt tuning done (A/B test 2 prompts)
- [ ] SEO scoring formula validated by content team
- [ ] Integration test: Genome → Title (end-to-end)

**Tech Notes**
- LLM: OpenAI GPT-4 (best quality) or open-source LLaMA-2-13B (cost-effective)
- Prompt framework: LangChain or LlamaIndex
- LLM latency: expect 1–2s per title generation
- Caching: Cache LLM output for identical Genomes (Redis)
- Cost: GPT-4 API ~$0.03 per title; LLaMA self-hosted ~$0 (compute-only)

**Dependencies**
- Follows VIS-004 (needs Genome objects)

---

## Team 4: Publishing & Operations (T4)

### Story VIS-006: Shopify Publish Skeleton
**Story Points**: 3 | **Owner**: T4 Backend Engineer | **Priority**: P1

**Context**
Establish Shopify API integration without publishing live data yet. Test schema mapping, auth, & dry-runs.

**User Story**
> As a DevOps engineer, I want to validate the Shopify API schema so that we can safely publish cakes to the store without data corruption.

**Acceptance Criteria**

1. **Shopify API client**
   - Initialize GraphQL client with admin API auth (OAuth token or API key)
   - Support mutations for: `productCreate`, `productUpdate`, `productVariantUpdate`
   - Implement exponential backoff for rate limiting (Shopify: 2,000 points/minute)

2. **Data mapping**
   - Map pipeline data → Shopify product schema:
     - `Genome.cake_structure.types` → Product.tags
     - `Genome.appearance.color_palette` → Product.metafield (custom field)
     - `SEO_title` → Product.title
     - `SEO_description` → Product.description
   - Handle edge cases: max title length (255 chars), max description (5000 chars)

3. **Dry-run endpoint**
   - POST `/api/v1/publish/dry-run` accepts image_id + Genome + SEO data
   - Returns what *would* be published without actually writing to Shopify:
     ```json
     {
       "image_id": "abc123",
       "dry_run": true,
       "shopify_payload": {
         "title": "Luxury Fondant Wedding Cake...",
         "description": "...",
         "tags": ["fondant", "wedding", "customizable"],
         "handle": "luxury-fondant-wedding-cake-abc123"
       },
       "validation": {
         "title_length": 65,
         "description_length": 450,
         "tags_count": 3,
         "all_required_fields_present": true
       }
     }
     ```

4. **Schema validation**
   - Validate payload against Shopify GraphQL schema before publish
   - Check: required fields, field types, max lengths, allowed values
   - Return validation errors (e.g., "title exceeds 255 chars")

5. **Auth & credentials**
   - Use environment variables for Shopify API credentials (OAuth token)
   - Support multiple stores (dev, staging, prod) via config
   - Test auth works; handle 401/403 errors

6. **Monitoring**
   - Log dry-run requests: image_id, validation status, payload size
   - Emit metric: `shopify_payload_validation_errors` (counter)

**Definition of Done**
- [ ] Shopify API client authenticated & working
- [ ] Data mapping logic complete
- [ ] Dry-run endpoint tested with 20 Genomes
- [ ] Schema validation catching all invalid payloads
- [ ] No actual writes to Shopify yet
- [ ] T1–T3 can call dry-run endpoint for testing

**Tech Notes**
- Language: Python (requests + graphene-django) or Node.js (apollo-client)
- Shopify API: GraphQL endpoint at `https://[store].myshopify.com/admin/api/[version]/graphql.json`
- Rate limiting: 2,000 points/minute; each mutation costs points (productCreate ≈ 600 points)
- Dry-run: No actual API call; just validate local schema

**Dependencies**
- None (can work independently)

---

### Story VIS-007: Logging & Audit Trail
**Story Points**: 3 | **Owner**: T4 SRE | **Priority**: P1

**Context**
Every image must be tracked through the pipeline for compliance & debugging. Establish unified logging & audit table.

**User Story**
> As a compliance officer, I want a complete audit trail of every image through the pipeline so that we can debug issues and meet data retention requirements.

**Acceptance Criteria**

1. **Audit table schema**
   - Create PostgreSQL `pipeline_audits` table:
     ```sql
     CREATE TABLE pipeline_audits (
       audit_id UUID PRIMARY KEY,
       image_id UUID NOT NULL,
       stage VARCHAR(50), -- e.g., "stage_01_input", "stage_04_vision", etc.
       status VARCHAR(20), -- "success", "failed", "skipped"
       input_data JSONB, -- metadata before this stage
       output_data JSONB, -- metadata after this stage
       latency_ms INT,
       error_message TEXT,
       model_version VARCHAR(50), -- if applicable
       confidence_score FLOAT,
       created_at TIMESTAMP,
       created_by VARCHAR(100) -- service name
     );
     ```

2. **Logging across all stages**
   - Every stage writes one audit record:
     - T1 VIS-001: log batch upload (stage_01_input)
     - T1 VIS-002: log validation result (stage_02_validation)
     - T2 VIS-003: log Qwen inference (stage_04_vision)
     - T2 VIS-004: log Genome assembly (stage_05_genome)
     - T3 VIS-005: log SEO generation (stage_06_seo)
     - T4 VIS-006: log publish (stage_09_publish)

3. **Log entry structure**
   - Each entry includes:
     - `image_id`, `stage`, `status`, `latency_ms`
     - `input_data` (previous stage output)
     - `output_data` (current stage result, sanitized)
     - `error_message` (if failed)
     - `model_version`, `confidence_score` (if applicable)
     - Timestamp + service name

4. **Structured logging (JSON)**
   - All logs shipped to ELK (Elasticsearch + Kibana) or Datadog
   - Standard fields: timestamp, level, message, context (image_id, stage, status, latency)
   - Example:
     ```json
     {
       "timestamp": "2026-08-04T12:34:56Z",
       "level": "INFO",
       "service": "vision-pipeline",
       "message": "Qwen inference completed",
       "image_id": "abc123",
       "stage": "04_vision",
       "status": "success",
       "latency_ms": 2340,
       "model_version": "qwen2.5-vl-8b",
       "confidence_score": 0.88,
       "trace_id": "xyz789"
     }
     ```

5. **Query & alerting**
   - Support queries: "show all images through pipeline in last 24h"
   - Alert on SLA breach: if end-to-end latency > 8s for 10+ images
   - Alert on error rate: if stage failure rate > 2%

6. **Data retention**
   - Logs retained in hot storage (Elasticsearch) for 30 days
   - Archive to S3 Glacier after 30 days (compliance requirement)
   - Audit table (PostgreSQL) retained for 1 year (per GDPR/CCPA)

**Definition of Done**
- [ ] Audit table created in production database
- [ ] All 7 stories log to audit table successfully
- [ ] JSON logs flowing to ELK/Datadog
- [ ] Queries working (find all failures, latencies)
- [ ] Alerts triggered on SLA breaches
- [ ] Sprint 1 images fully traced end-to-end

**Tech Notes**
- Logging: Python logging + structlog (JSON output)
- Storage: PostgreSQL + ELK (or Datadog for unified observability)
- Trace ID: OpenTelemetry context ID propagated through all stages
- Querying: Kibana or Datadog dashboard to visualize pipeline health

**Dependencies**
- None (can initialize in parallel; all other stories log to this table)

---

## Sprint Checklist & Acceptance

### Definition of Done (All Stories)
- [ ] Code committed to main branch (reviewed by 2 engineers)
- [ ] Unit tests: >80% coverage
- [ ] Integration tests: happy path + 2 error scenarios
- [ ] Manual QA: tested in staging environment
- [ ] Documentation: API docs, README updated
- [ ] Performance: latency/throughput targets met
- [ ] Monitoring: metrics flowing to Datadog
- [ ] Deployment: all stories deployed to staging

### Sprint Demo (End of Week 2)
- **Live demo**: Upload 10-image batch → see end-to-end pipeline output (Genome + SEO title + dry-run Shopify publish)
- **Metrics shown**: Total latency breakdown, error rate, GPU utilization
- **Logging verified**: All 10 images traced in audit table + ELK

### Inspect & Adapt (Retrospective)
**Discuss:**
- What went well? (e.g., "Batch upload API was straightforward")
- What was hard? (e.g., "Qwen latency tuning took longer than expected")
- What should we change for Sprint 2? (e.g., "Allocate more GPU capacity")

**Outcomes for Sprint 2:**
- Scale to 100-image batches (instead of 50)
- Add metadata fields 51–150 to Genome
- Implement full SEO suite (description, FAQ, tags)
- Go live with first Shopify publishes (dry-run → real)

---

## Story Dependencies & Risk Map

```
VIS-001 (Batch upload)
  ↓
VIS-002 (Validation) + VIS-003 (Qwen) + VIS-006 (Shopify) + VIS-007 (Logging)
                              ↓
                        VIS-004 (Genome)
                              ↓
                        VIS-005 (SEO title)
                              ↓
                        End-to-end demo
```

**Critical path**: VIS-001 → VIS-002 → VIS-003 → VIS-004 → VIS-005 (Qwen latency is bottleneck)

**Risk**: If Qwen inference > 3s, entire pipeline bottlenecks. Mitigation: Have CLIP fallback ready.

---

## Metrics to Track During Sprint 1

| Metric | Target | Warning Threshold |
|--------|--------|-------------------|
| Batch upload throughput | 100 files/min | <50 files/min |
| Validation accuracy | >99% (only true dupes rejected) | <95% |
| Qwen latency (p95) | <3s | >4s |
| Vision API uptime | >99% | <95% |
| Genome schema completeness | 50+ fields populated | <40 fields |
| SEO title quality | avg score >0.70 | <0.65 |
| Shopify dry-run success | 100% (no validation errors) | <95% |
| Audit logging coverage | 100% of images logged | <95% |

---

## Post-Sprint Deliverables

1. **Staging deployment** with all 7 stories
2. **API documentation** (OpenAPI spec)
3. **Architecture diagram** (batch → validation → Qwen → Genome → SEO → publish)
4. **Metrics dashboard** (Grafana or Datadog)
5. **Runbook** for on-call ops (how to debug pipeline failures)
6. **Sprint retrospective** notes (what to improve for Sprint 2)

---

## Next: Sprint 2 Preview (Week 3–4)

- Extend Genome to 150 fields (500+ total by end of PI)
- Implement full SEO suite (description, FAQ, tags, alt text)
- Begin live Shopify publishes (start with 10 images/day, ramp to 100/day)
- Add human approval workflow (optional gate before publish)
- Monitor for metadata drift & model degradation

