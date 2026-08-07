# Full Operational Testing (FOT) Suite
## TBK Vision Workflow - n8n Complete Validation
### Version 1.0 | Test Duration: 4-6 hours | Estimated Time: ~2 FTE days

---

## EXECUTIVE SUMMARY

This FOT suite validates **all 7 workflows** across **5 test levels**:

1. **Unit Tests** (Individual workflow validation)
2. **Integration Tests** (End-to-end happy path)
3. **Stress Tests** (High load, concurrent execution)
4. **Failure Tests** (Error handling, fallbacks, recovery)
5. **Performance Tests** (Latency, throughput, SLA compliance)

**Pass Criteria**: All tests must pass with zero critical failures.

**Expected Duration**: 4-6 hours (assuming parallel execution)

---

## TEST ENVIRONMENT SETUP

### Prerequisites
- ✅ Docker stack deployed (all services healthy)
- ✅ All 6 credentials added to n8n
- ✅ Master Orchestrator imported
- ✅ 6 sub-workflows created
- ✅ PostgreSQL schema initialized
- ✅ Test S3 bucket with sample images
- ✅ Datadog dashboards configured
- ✅ Slack #tbk-testing channel created

### Test Data Location
```
s3://tbk-images-test/
├── wedding_cake_001.jpg (3MB, 4000x3000px)
├── birthday_cake_001.jpg (2.5MB, 3500x2800px)
├── chocolate_cake_001.jpg (2.2MB, 3200x2600px)
├── cupcake_001.jpg (1.8MB, 2800x2200px)
├── fondant_cake_001.jpg (2.8MB, 3800x3000px)
├── invalid_image.txt (not an image, for error testing)
├── corrupted.jpg (corrupted JPEG header, for error testing)
└── duplicate_of_wedding_cake_001.jpg (same SHA256, for dedup test)
```

### Test Credentials
- n8n admin: admin / (password from .env)
- PostgreSQL: vision_user / (password from .env)
- Shopify: Test store (not production)
- Slack: #tbk-testing webhook
- Datadog: Test API key (read-only)

---

## LEVEL 1: UNIT TESTS (Individual Workflows)

### Test 1.1: Input Validation Workflow

**Objective**: Validate file upload, deduplication, format checking.

**Test Cases**:

#### 1.1.1 Happy Path - Valid Image Upload
```
Input:
{
  "batch_id": "unit_test_input_001",
  "source": "api",
  "file_urls": ["s3://tbk-images-test/wedding_cake_001.jpg"]
}

Expected Output:
{
  "validated": 1,
  "rejected": 0,
  "images": [
    {
      "image_id": "uuid",
      "file_hash": "sha256_hash",
      "s3_path": "s3://tbk-images-test/wedding_cake_001.jpg",
      "status": "queued"
    }
  ],
  "error_log": []
}

Validation:
✓ Image hash computed (SHA256 format)
✓ Image stored in PostgreSQL images table
✓ Status = 'queued'
✓ No errors
✓ Latency < 1 second
```

**Test Command**:
```bash
curl -X POST http://n8n:5678/webhook/input-validation \
  -H "Content-Type: application/json" \
  -d '{
    "batch_id": "unit_test_input_001",
    "source": "api",
    "file_urls": ["s3://tbk-images-test/wedding_cake_001.jpg"]
  }'

Expected HTTP: 200 OK
Expected response time: <1 second
```

**Pass Criteria**: ✅ All validations pass

---

#### 1.1.2 Duplicate Detection
```
Input:
{
  "batch_id": "unit_test_input_002",
  "source": "api",
  "file_urls": [
    "s3://tbk-images-test/wedding_cake_001.jpg",
    "s3://tbk-images-test/duplicate_of_wedding_cake_001.jpg"
  ]
}

Expected Output:
{
  "validated": 1,
  "rejected": 1,
  "images": [
    {
      "image_id": "uuid_1",
      "file_hash": "same_sha256",
      "s3_path": "s3://tbk-images-test/wedding_cake_001.jpg",
      "status": "queued"
    }
  ],
  "error_log": [
    {
      "file_url": "s3://tbk-images-test/duplicate_of_wedding_cake_001.jpg",
      "reason": "duplicate_hash_exists",
      "existing_image_id": "uuid_1"
    }
  ]
}

Validation:
✓ First image accepted
✓ Duplicate rejected with reason
✓ Error log populated
✓ Rejected count = 1
```

**Pass Criteria**: ✅ Duplicate correctly identified and rejected

---

#### 1.1.3 Invalid File Format
```
Input:
{
  "batch_id": "unit_test_input_003",
  "source": "api",
  "file_urls": ["s3://tbk-images-test/invalid_image.txt"]
}

Expected Output:
{
  "validated": 0,
  "rejected": 1,
  "images": [],
  "error_log": [
    {
      "file_url": "s3://tbk-images-test/invalid_image.txt",
      "reason": "invalid_file_format",
      "details": "Expected JPEG/PNG, got text/plain"
    }
  ]
}

Validation:
✓ File format check passed
✓ Rejection reason clear
✓ No partial writes to DB
```

**Pass Criteria**: ✅ Invalid format rejected with clear error

---

#### 1.1.4 Corrupted Image File
```
Input:
{
  "batch_id": "unit_test_input_004",
  "source": "api",
  "file_urls": ["s3://tbk-images-test/corrupted.jpg"]
}

Expected Output:
{
  "validated": 0,
  "rejected": 1,
  "images": [],
  "error_log": [
    {
      "file_url": "s3://tbk-images-test/corrupted.jpg",
      "reason": "corrupted_image",
      "details": "JPEG header invalid"
    }
  ]
}

Validation:
✓ Image integrity check passed
✓ Corruption detected
✓ Rejected before processing
```

**Pass Criteria**: ✅ Corrupted file rejected early

---

#### 1.1.5 Dimension Check
```
Input:
{
  "batch_id": "unit_test_input_005",
  "source": "api",
  "file_urls": ["s3://tbk-images-test/small_image_400x300.jpg"]
}

Expected Output:
{
  "validated": 0,
  "rejected": 1,
  "error_log": [
    {
      "file_url": "...",
      "reason": "dimensions_too_small",
      "details": "400x300 < 800x600 minimum"
    }
  ]
}

Validation:
✓ Dimension check enforced (min 800x600)
✓ Rejection with reason
```

**Pass Criteria**: ✅ Minimum dimensions enforced

---

### Test 1.2: Qwen Vision Workflow

**Objective**: GPU inference, vision analysis, structured output.

**Test Cases**:

#### 1.2.1 Happy Path - Qwen Analysis
```
Input:
{
  "image_id": "unit_test_qwen_001",
  "s3_path": "s3://tbk-images-test/wedding_cake_001.jpg",
  "batch_id": "unit_test_qwen_batch"
}

Expected Output:
{
  "image_id": "unit_test_qwen_001",
  "vision_result": {
    "layers": 3,
    "frosting_type": "fondant",
    "decorations": ["flowers", "beads"],
    "colors": ["white", "pink", "gold"],
    "quality_score": 0.89,
    "confidence": 0.87,
    "text_on_cake": "Happy Anniversary"
  },
  "confidence_scores": {
    "layers": 0.92,
    "frosting": 0.85,
    "decorations": 0.78,
    "colors": 0.91,
    "quality": 0.89
  },
  "latency_ms": 2340,
  "model_version": "qwen2.5-vl-8b",
  "model": "qwen"
}

Validation:
✓ Vision data structured correctly
✓ All expected fields present
✓ Confidence scores in range [0-1]
✓ Latency < 2.5 seconds (p95)
✓ Model version tracked
```

**Test Command**:
```bash
# Execute Qwen Vision WF with test data
curl -X POST http://n8n:5678/webhook/qwen-vision \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "unit_test_qwen_001",
    "s3_path": "s3://tbk-images-test/wedding_cake_001.jpg",
    "batch_id": "unit_test_qwen_batch"
  }'

Expected HTTP: 200 OK
Expected latency: 2-3 seconds
```

**Pass Criteria**: ✅ Qwen returns structured vision data with confidence scores

---

#### 1.2.2 Qwen Fallback to CLIP
```
Test Scenario: Qwen GPU offline (simulate by stopping GPU service)

Input: (same as 1.2.1)

Expected Behavior:
1. Qwen API call times out (2.5s)
2. Fallback triggered automatically
3. CLIP model invoked (<1s)
4. Fallback results returned

Expected Output:
{
  "image_id": "unit_test_qwen_001",
  "vision_result": { ... },
  "confidence": 0.72,  // Lower than Qwen (70-80% accuracy)
  "model": "clip",
  "model_version": "clip-vit-large",
  "latency_ms": 950,
  "fallback_reason": "qwen_timeout"
}

Validation:
✓ Fallback triggered within 3 seconds
✓ CLIP results returned successfully
✓ Lower confidence scores vs Qwen (expected)
✓ Image still processable
✓ Fallback logged in audit trail
```

**Pass Criteria**: ✅ Fallback to CLIP works seamlessly

---

#### 1.2.3 Qwen Latency Measurement
```
Test 100 images sequentially, measure latency distribution

Expected Results:
- p50: 2.0s
- p95: 2.5s
- p99: 2.8s
- max: <3.5s

Validation:
✓ p95 < 2.5s (SLA compliance)
✓ No outliers >4s
✓ Consistent latency
```

**Pass Criteria**: ✅ Latency meets SLA targets

---

### Test 1.3: Genome Builder Workflow

**Objective**: Transform vision data → 300+ fields.

**Test Cases**:

#### 1.3.1 Vision to Genome Mapping
```
Input:
{
  "vision_data": {
    "layers": 3,
    "frosting_type": "fondant",
    "decorations": ["flowers", "beads"],
    "colors": ["white", "pink"]
  },
  "image_id": "unit_test_genome_001",
  "confidence_scores": {
    "layers": 0.92,
    "frosting": 0.85,
    "decorations": 0.78,
    "colors": 0.91
  }
}

Expected Output:
{
  "image_id": "unit_test_genome_001",
  "genome": {
    "cake_structure": {
      "layers": 3,
      "frosting_type": "fondant",
      "frosting_smooth": true,
      "height_estimate_cm": 18
    },
    "appearance": {
      "color_palette": ["white", "pink", "gold"],
      "primary_color": "white",
      "color_harmony": "complementary"
    },
    "decorations": {
      "flowers": true,
      "beads": true,
      "piping": false
    },
    "metadata": {
      "schema_version": "1.0",
      "created_at": "2026-08-04T12:34:56Z"
    },
    // ... 290+ more fields ...
  },
  "schema_version": "1.0",
  "field_coverage": 0.98,
  "fields_with_low_confidence": 2
}

Validation:
✓ Vision fields mapped to genome correctly
✓ ≥300 fields populated
✓ Field coverage ≥95%
✓ Confidence propagation correct
✓ Schema version tracked
✓ Timestamp present
```

**Pass Criteria**: ✅ Genome has 300+ fields with >95% coverage

---

### Test 1.4: SEO Generator Workflow

**Objective**: LLM-based content generation.

**Test Cases**:

#### 1.4.1 SEO Title Generation
```
Input:
{
  "genome": { ... 300+ fields ... },
  "image_id": "unit_test_seo_001",
  "batch_id": "unit_test_seo_batch"
}

Expected Output:
{
  "image_id": "unit_test_seo_001",
  "seo_content": {
    "title": "Luxury Fondant Wedding Cake with Pink Ombre – 24–30 Servings",
    "title_alt": "Custom Fondant Cake, Pink Ombre Design, Floral Toppers",
    "meta_description": "Handcrafted fondant wedding cake with pink ombre gradient & fresh flower toppers. Serves 24–30 guests.",
    "tags": ["fondant cake", "wedding cake", "pink ombre", "custom cake"],
    "alt_text": "Three-layer white and pink ombre fondant wedding cake with fresh flower toppers and pearl bead details",
    "faq": [
      {
        "question": "How many people does this cake serve?",
        "answer": "This cake serves 24–30 guests depending on slice size."
      }
    ]
  },
  "seo_scores": {
    "title_score": 0.78,
    "description_score": 0.82,
    "tags_score": 0.75,
    "alt_text_score": 0.81,
    "avg_score": 0.79
  }
}

Validation:
✓ Title <60 chars
✓ Meta description 150-200 chars
✓ 4-8 relevant tags
✓ Alt text descriptive (>50 chars)
✓ FAQ has 3-5 Q&A pairs
✓ All scores in [0-1] range
✓ Average score >0.7
```

**Pass Criteria**: ✅ SEO content generated with avg score >0.7

---

### Test 1.5: Shopify Publisher Workflow

**Objective**: GraphQL product creation/update.

**Test Cases**:

#### 1.5.1 Product Create
```
Input:
{
  "image_id": "unit_test_shopify_001",
  "genome": { ... },
  "seo_content": { ... },
  "batch_id": "unit_test_shopify_batch"
}

Expected Output:
{
  "image_id": "unit_test_shopify_001",
  "publish_status": "success",
  "shopify_product_id": "gid://shopify/Product/12345678901234",
  "published_fields": ["title", "description", "tags", "metafields"],
  "errors": []
}

Validation:
✓ Product created in Shopify (test store)
✓ Product ID returned (gid format)
✓ All fields published
✓ No errors
✓ Shopify API response time <1s
```

**Pass Criteria**: ✅ Product published to Shopify successfully

---

#### 1.5.2 Shopify Rate Limit Handling
```
Test Scenario: Send 20 products rapidly to trigger rate limit (2000 points/min)

Expected Behavior:
1. First 10 products succeed immediately
2. Subsequent products trigger 429 (Too Many Requests)
3. Exponential backoff engaged
4. Retry with 60s delay
5. All 20 eventually publish

Validation:
✓ Rate limit detected (429)
✓ Exponential backoff applied
✓ Retry after delay
✓ All products eventually published (no data loss)
✓ SLA met (all within queue timeout)
```

**Pass Criteria**: ✅ Rate limit handled gracefully with exponential backoff

---

### Test 1.6: Audit Logger Workflow

**Objective**: Log all events to PostgreSQL + Elasticsearch.

**Test Cases**:

#### 1.6.1 Audit Log Creation
```
Input:
{
  "image_id": "unit_test_audit_001",
  "batch_id": "unit_test_audit_batch",
  "stage": "04_vision",
  "status": "success",
  "latency_ms": 2340,
  "confidence_score": 0.87
}

Expected Output in PostgreSQL:
INSERT INTO pipeline_audits (
  audit_id, image_id, batch_id, stage, status, latency_ms,
  confidence_score, created_at
) VALUES (...)

Validation in Elasticsearch:
GET /pipeline-logs-2026.08.04/_search?q=image_id:unit_test_audit_001
→ Document found with same data

Validation:
✓ Record inserted in PostgreSQL
✓ Indexed in Elasticsearch
✓ Timestamp present (ISO 8601)
✓ Confidence score recorded
✓ No data loss
```

**Pass Criteria**: ✅ Audit logs in both PostgreSQL and Elasticsearch

---

## LEVEL 2: INTEGRATION TESTS (End-to-End)

### Test 2.1: Happy Path - 5 Images End-to-End

**Objective**: Complete workflow from upload to Shopify publish.

**Test Scenario**:
```
INPUT:
{
  "batch_id": "integration_test_001",
  "source": "api",
  "file_urls": [
    "s3://tbk-images-test/wedding_cake_001.jpg",
    "s3://tbk-images-test/birthday_cake_001.jpg",
    "s3://tbk-images-test/chocolate_cake_001.jpg",
    "s3://tbk-images-test/cupcake_001.jpg",
    "s3://tbk-images-test/fondant_cake_001.jpg"
  ]
}

EXPECTED DURATION: 45-60 seconds (5 images × ~10s average)

EXPECTED OUTPUT:
{
  "batch_id": "integration_test_001",
  "status": "success",
  "results": {
    "validation": {
      "validated": 5,
      "rejected": 0
    },
    "vision": {
      "latency_ms": 2340,
      "model": "qwen"
    },
    "genome": {
      "field_coverage": 0.98
    },
    "seo": {
      "avg_score": 0.79
    },
    "publish": {
      "publish_status": "success",
      "published_count": 5
    }
  },
  "duration_ms": 45000,
  "error_count": 0
}
```

**Test Execution**:
```bash
# POST to Master Orchestrator webhook
curl -X POST http://n8n:5678/webhook/tbk-vision-batch-upload \
  -H "Content-Type: application/json" \
  -d '{
    "batch_id": "integration_test_001",
    "source": "api",
    "file_urls": [...]
  }'

# Monitor execution in n8n UI
# Expected: ≈45 seconds end-to-end

# Verify outputs
psql -U vision_user -d tbk_pipeline -c \
  "SELECT * FROM batches WHERE batch_id='integration_test_001';"
# Expected status: success, processed_count: 5, error_count: 0

# Check Slack notification
# Expected: Message in #tbk-pipeline-notifications with 5/5 success

# Verify Datadog metrics
# Expected: tbk.vision.batch.duration ≈ 45000ms
```

**Pass Criteria**:
- ✅ All 5 images processed
- ✅ No errors in logs
- ✅ Slack notification received
- ✅ Batch status = 'success' in DB
- ✅ Shopify products created
- ✅ Audit logs complete
- ✅ Duration <60 seconds
- ✅ Zero data loss

---

### Test 2.2: Mixed Batch - Valid + Invalid Images

**Objective**: Ensure batch continues despite errors.

**Test Scenario**:
```
INPUT:
{
  "batch_id": "integration_test_002",
  "file_urls": [
    "s3://tbk-images-test/wedding_cake_001.jpg",      // ✓ Valid
    "s3://tbk-images-test/invalid_image.txt",         // ✗ Invalid format
    "s3://tbk-images-test/chocolate_cake_001.jpg",    // ✓ Valid
    "s3://tbk-images-test/corrupted.jpg",             // ✗ Corrupted
    "s3://tbk-images-test/cupcake_001.jpg"            // ✓ Valid
  ]
}

EXPECTED RESULT:
- 3 valid images: validated + processed ✓
- 2 invalid images: rejected with reason ✗
- Batch continues despite errors
- Error log populated
- Partial success (3/5)
```

**Pass Criteria**:
- ✅ 3 images successfully published
- ✅ 2 images rejected with clear error messages
- ✅ No cascade failures
- ✅ Batch status = 'partial' (not 'failed')
- ✅ Error log in Slack notification

---

## LEVEL 3: STRESS TESTS (High Load)

### Test 3.1: Throughput Test - 100 Images

**Objective**: Validate 1,000 img/day throughput.

**Test Scenario**:
```
SETUP:
- 100 test images in S3
- 10 concurrent batch submissions
- Each batch = 10 images
- Total execution time ≈10-15 minutes

EXPECTED METRICS:
- Total images processed: 100
- Success rate: >98%
- Average latency per image: <8 seconds
- Throughput: ≈6-10 images/minute
- Peak: Up to 12 images/minute (proof of 1,000/day capability)
```

**Test Execution**:
```bash
#!/bin/bash
# stress_test_100_images.sh

for i in {1..10}; do
  curl -X POST http://n8n:5678/webhook/tbk-vision-batch-upload \
    -H "Content-Type: application/json" \
    -d "{
      \"batch_id\": \"stress_test_batch_$i\",
      \"source\": \"api\",
      \"file_urls\": [
        \"s3://tbk-images-test/image_${i}_01.jpg\",
        \"s3://tbk-images-test/image_${i}_02.jpg\",
        ...
        \"s3://tbk-images-test/image_${i}_10.jpg\"
      ]
    }" &
done

wait  # Wait for all to complete

# Monitor progress in Datadog
# Expected: Queue drains smoothly, no backlog
```

**Datadog Monitoring**:
```
Dashboard queries:
- sum:tbk.vision.batch.success_count → Should reach 100
- avg:tbk.vision.batch.duration → Should avg 45-60s per batch
- avg:tbk.vision.stage_latency{stage:vision} → Should avg <2.5s
- max:tbk.vision.queue_depth → Should not exceed 30
```

**Pass Criteria**:
- ✅ 100 images processed in <15 minutes
- ✅ >98% success rate
- ✅ No queue buildup (depth never >50)
- ✅ No memory leaks (Redis stable)
- ✅ Database query latency <100ms

---

### Test 3.2: Concurrent Execution - 5 Parallel Batches

**Objective**: Verify no race conditions or data corruption.

**Test Scenario**:
```
SETUP:
- 5 batches submitted simultaneously (at exact same time)
- Each batch = 10 images
- Total = 50 images
- Expected duration: 60 seconds (same as single batch)

EXPECTED BEHAVIOR:
- Workflows execute in parallel
- No shared state conflicts
- Database transactions atomic
- All 50 images processed successfully
```

**Test Execution**:
```bash
#!/bin/bash
# concurrent_test.sh

for i in {1..5}; do
  curl -X POST http://n8n:5678/webhook/tbk-vision-batch-upload \
    -H "Content-Type: application/json" \
    -d "{\"batch_id\": \"concurrent_batch_$i\", ...}" &
done

wait

# Verify no duplicate image_ids
psql -U vision_user -d tbk_pipeline -c \
  "SELECT image_id, COUNT(*) FROM images 
   WHERE batch_id LIKE 'concurrent%' 
   GROUP BY image_id HAVING COUNT(*) > 1;"
# Expected: (empty result set - no duplicates)
```

**Pass Criteria**:
- ✅ All 50 images unique (no duplicates)
- ✅ All 50 processed successfully
- ✅ No race condition errors
- ✅ Total duration still ≈60s (not 300s sequential)
- ✅ Database integrity maintained

---

## LEVEL 4: FAILURE TESTS (Error Handling)

### Test 4.1: Qwen GPU Service Down

**Objective**: Verify fallback to CLIP works.

**Test Scenario**:
```
SETUP:
1. Stop Qwen GPU service: docker stop qwen-gpu-1
2. Submit 5-image batch
3. Monitor fallback activation
4. Verify results

EXPECTED BEHAVIOR:
- Qwen API call timeout (3 seconds)
- Fallback to CLIP triggered automatically
- CLIP returns results in <1 second
- Image processed successfully with lower confidence
- Alert sent to Slack #tbk-pipeline-alerts
```

**Test Execution**:
```bash
# Stop Qwen GPU
docker stop qwen-gpu-1

# Submit test batch
curl -X POST http://n8n:5678/webhook/tbk-vision-batch-upload \
  -H "Content-Type: application/json" \
  -d '{"batch_id": "fallback_test_001", ...}'

# Monitor n8n logs
docker-compose logs -f n8n | grep -i "fallback\|clip"
# Expected: "Fallback triggered: Qwen timeout"

# Check results
psql -U vision_user -d tbk_pipeline -c \
  "SELECT * FROM vision_results WHERE image_id IN (...) ORDER BY created_at DESC LIMIT 5;"
# Expected: model = 'clip', latency_ms < 1000

# Restart Qwen
docker start qwen-gpu-1
```

**Pass Criteria**:
- ✅ Fallback triggered automatically
- ✅ All 5 images processed via CLIP
- ✅ Results in confidence [0.7-0.8] (vs Qwen 0.85-0.95)
- ✅ Slack alert sent
- ✅ No data loss
- ✅ Total latency <5 seconds per image

---

### Test 4.2: PostgreSQL Connection Error

**Objective**: Verify retry logic and graceful degradation.

**Test Scenario**:
```
SETUP:
1. Simulate connection timeout: iptables DROP traffic to PostgreSQL
2. Submit batch
3. Monitor retry behavior
4. Verify recovery after 30 seconds

EXPECTED BEHAVIOR:
- First write attempt fails
- Retry with exponential backoff (1s, 2s, 4s, 8s...)
- After 30 seconds, iptables rule removed
- Connection restored
- Pending writes resume automatically
```

**Test Execution**:
```bash
# Block PostgreSQL (as root)
iptables -I INPUT -p tcp --dport 5432 -j DROP

# Submit batch (this will queue writes)
curl -X POST http://n8n:5678/webhook/tbk-vision-batch-upload \
  -H "Content-Type: application/json" \
  -d '{"batch_id": "db_error_test_001", ...}'

# Wait 30 seconds
sleep 30

# Restore PostgreSQL
iptables -D INPUT -p tcp --dport 5432 -j DROP

# Check logs
docker-compose logs -f n8n | grep -i "retry\|connection"
# Expected: Retries with exponential backoff

# Verify data consistency
psql -U vision_user -d tbk_pipeline -c \
  "SELECT * FROM batches WHERE batch_id='db_error_test_001';"
# Expected: status = 'success' (eventually)
```

**Pass Criteria**:
- ✅ Retry logic engaged
- ✅ No immediate failure
- ✅ Data eventually written after recovery
- ✅ No corrupted/partial records
- ✅ User notified via Slack

---

### Test 4.3: Shopify API Rate Limit (429)

**Objective**: Verify exponential backoff and eventual success.

**Test Scenario**:
```
SETUP:
1. Submit 20 images in rapid succession (high rate)
2. Monitor Shopify API responses
3. Verify 429 responses trigger backoff
4. Verify all 20 eventually publish

EXPECTED BEHAVIOR:
- First 10 products succeed (within rate limit: 2000 points/min)
- Products 11+ receive 429 responses
- Exponential backoff: 60s delay
- Retry after 60s
- All 20 eventually published (no data loss)
```

**Test Execution**:
```bash
#!/bin/bash
# shopify_rate_limit_test.sh

echo "Starting rapid Shopify publishes..."
for i in {1..20}; do
  curl -X POST http://n8n:5678/webhook/shopify-publish \
    -H "Content-Type: application/json" \
    -d "{\"image_id\": \"shopify_test_$i\", ...}" &
  
  # Small delay between requests
  sleep 0.5
done

wait

# Check publish status
psql -U vision_user -d tbk_pipeline -c \
  "SELECT publish_status, COUNT(*) FROM shopify_publishes 
   WHERE image_id LIKE 'shopify_test_%' 
   GROUP BY publish_status;"

# Expected output:
# publish_status | count
# ---------------+-------
# success        |    20
# (all eventually succeed after backoff)

# Verify Datadog logs
# Query: "service:shopify status:429" → should see 429 responses
# Then: "service:shopify status:200" → successful retries
```

**Pass Criteria**:
- ✅ Initial 10 products publish immediately
- ✅ Products 11-20 receive 429 responses
- ✅ Exponential backoff applied (60s+ delay)
- ✅ All 20 eventually published (100% success)
- ✅ No duplicate publishes (idempotent)
- ✅ Slack alert for rate limiting

---

## LEVEL 5: PERFORMANCE TESTS (SLA Compliance)

### Test 5.1: Latency Distribution (p50, p95, p99)

**Objective**: Measure latency percentiles against SLA targets.

**Test Scenario**:
```
SETUP:
- 50 images submitted in batches
- Measure end-to-end latency for each
- Calculate percentiles

SLA TARGETS:
- p50: <5 seconds
- p95: <8 seconds
- p99: <10 seconds

EXPECTED RESULTS (Datadog):
{
  "metric": "tbk.vision.batch.duration",
  "p50": 4800,    // 4.8s
  "p95": 7200,    // 7.2s (PASS SLA <8s)
  "p99": 9500     // 9.5s (PASS SLA <10s)
}
```

**Test Execution**:
```bash
# Run 50-image test
bash stress_test_50_images.sh

# Query Datadog for percentiles
curl -X GET "https://api.datadoghq.com/api/v1/query" \
  -H "DD-API-KEY: $DATADOG_API_KEY" \
  -d "query=percentile:tbk.vision.batch.duration{*}:0.95"

# Expected: value close to 7.2 seconds
```

**Pass Criteria**:
- ✅ p95 < 8 seconds (SLA compliance)
- ✅ p99 < 10 seconds
- ✅ No outliers >12 seconds
- ✅ Consistent distribution (no bimodal)

---

### Test 5.2: Throughput Test - 1,000 img/day Capacity

**Objective**: Prove system can handle 1,000+ images in 24-hour period.

**Test Scenario**:
```
SETUP:
- 1,000 test images in S3
- Submitted in 10 batches of 100 images each
- Batches submitted every 15 minutes
- Total test duration: 2.5 hours (simulates 24-hour load)

EXPECTED METRICS:
- Total images: 1,000
- Success rate: >98% (max 20 failures)
- Average throughput: 400 img/hour
- Peak throughput: Up to 600 img/hour
- No queue buildup (depth never >100)
- Database stable (query latency <100ms)
- Memory stable (no leaks)
```

**Test Execution**:
```bash
#!/bin/bash
# throughput_test_1000_images.sh

for batch_num in {1..10}; do
  echo "Submitting batch $batch_num/10 (100 images)..."
  
  curl -X POST http://n8n:5678/webhook/tbk-vision-batch-upload \
    -H "Content-Type: application/json" \
    -d "{
      \"batch_id\": \"throughput_test_batch_$batch_num\",
      \"source\": \"api\",
      \"file_urls\": [...]
    }" &
  
  # Wait 15 minutes before next batch
  if [ $batch_num -lt 10 ]; then
    sleep 900  # 15 minutes
  fi
done

wait

# Monitor in Datadog
# Queries:
# sum:tbk.vision.batch.success_count → Should reach 1000
# avg:tbk.vision.queue_depth → Should stay <100
# avg:tbk.vision.db_query_latency → Should stay <100ms
```

**Pass Criteria**:
- ✅ 1,000 images processed in 2.5 hours
- ✅ >98% success rate (≤20 failures)
- ✅ No queue buildup
- ✅ Database performance stable
- ✅ Memory/CPU stable (no resource exhaustion)
- ✅ Demonstrates >1,000/day capacity

---

### Test 5.3: Memory & CPU Profiling

**Objective**: Ensure no memory leaks, stable resource usage.

**Test Scenario**:
```
SETUP:
- Run 500-image batch
- Monitor Docker stats during execution
- Check memory growth before/after

BASELINE (before test):
- n8n container: 250MB
- PostgreSQL: 300MB
- Redis: 50MB
- Total: 600MB

EXPECTED DURING LOAD:
- n8n container: <500MB (growth <250MB)
- PostgreSQL: <400MB
- Redis: <100MB
- Total: <1GB

EXPECTED AFTER TEST (wait 5 min):
- Should return to baseline
- No memory retained (no leaks)
```

**Test Execution**:
```bash
# Baseline
docker stats --no-stream tbk-n8n-1 tbk-postgres-1 tbk-redis-1
# Note: MEMORY values

# Run 500-image test
bash stress_test_500_images.sh &
TEST_PID=$!

# Monitor during execution
watch -n 5 'docker stats --no-stream tbk-n8n-1 tbk-postgres-1 tbk-redis-1'

# After completion, wait 5 minutes
wait $TEST_PID
sleep 300

# Check final stats
docker stats --no-stream tbk-n8n-1 tbk-postgres-1 tbk-redis-1
# Should be back to baseline (or close)
```

**Pass Criteria**:
- ✅ Memory growth <250MB during test
- ✅ Returns to baseline after 5 minutes
- ✅ CPU usage <80% peak
- ✅ No OOM (Out of Memory) errors
- ✅ Logs show no memory warnings

---

## TEST EXECUTION SCHEDULE

### Phase 1: Unit Tests (Hour 1-1.5)
- 1.1: Input Validation (15 min)
- 1.2: Qwen Vision (15 min)
- 1.3: Genome Builder (10 min)
- 1.4: SEO Generator (10 min)
- 1.5: Shopify Publisher (10 min)
- 1.6: Audit Logger (5 min)

**Parallel**: All unit tests can run in parallel (different workflows)

---

### Phase 2: Integration Tests (Hour 1.5-2)
- 2.1: Happy Path (15 min)
- 2.2: Mixed Batch (15 min)

---

### Phase 3: Stress Tests (Hour 2-3)
- 3.1: Throughput 100 images (45 min)
- 3.2: Concurrent execution (15 min)

---

### Phase 4: Failure Tests (Hour 3-4)
- 4.1: Qwen GPU down (15 min)
- 4.2: PostgreSQL error (20 min)
- 4.3: Shopify rate limit (25 min)

---

### Phase 5: Performance Tests (Hour 4-6)
- 5.1: Latency distribution (45 min)
- 5.2: Throughput 1,000 images (2.5 hours)
- 5.3: Memory profiling (15 min)

---

## PASS/FAIL CRITERIA

### PASS (✅ Go to Production)
- ✅ ALL unit tests pass (0 failures)
- ✅ ALL integration tests pass (0 failures)
- ✅ Stress tests: >98% success rate
- ✅ Failure tests: Graceful handling, no data loss
- ✅ Performance: p95 latency <8s, throughput >1,000/day
- ✅ No critical issues in logs
- ✅ Memory/CPU stable (no leaks)

### CONDITIONAL PASS (⚠️ Fix and Retest)
- ⚠️ >1% failure rate in stress tests (1-2% acceptable if not >2%)
- ⚠️ p95 latency 8-9 seconds (target <8s, acceptable if <9s)
- ⚠️ Minor data loss in fallback scenarios (< 0.1% acceptable)

### FAIL (❌ Do Not Deploy)
- ❌ Any critical error (data loss, corruption, auth failure)
- ❌ >2% failure rate in stress tests
- ❌ p95 latency >10 seconds
- ❌ Shopify publish failures >5%
- ❌ Memory leaks detected
- ❌ Qwen fallback doesn't work

---

## TEST REPORT TEMPLATE

```markdown
# n8n FOT Report
Date: [DATE]
Tester: [NAME]
Duration: [X hours]

## Summary
- Total Tests: 20
- Passed: [X]
- Failed: [X]
- Status: [PASS / FAIL]

## Unit Tests
- 1.1 Input Validation: PASS ✅
- 1.2 Qwen Vision: PASS ✅
- 1.3 Genome Builder: PASS ✅
- 1.4 SEO Generator: PASS ✅
- 1.5 Shopify Publisher: PASS ✅
- 1.6 Audit Logger: PASS ✅

## Integration Tests
- 2.1 Happy Path: PASS ✅
- 2.2 Mixed Batch: PASS ✅

## Stress Tests
- 3.1 Throughput 100: PASS ✅ (avg 2.1 img/s)
- 3.2 Concurrent 50: PASS ✅ (no race conditions)

## Failure Tests
- 4.1 Qwen Fallback: PASS ✅ (fallback in 3s)
- 4.2 DB Error: PASS ✅ (retry successful)
- 4.3 Shopify Rate Limit: PASS ✅ (all 20 published)

## Performance Tests
- 5.1 Latency (p95): PASS ✅ (7.2s < 8s SLA)
- 5.2 Throughput 1,000: PASS ✅ (600 img/hr peak)
- 5.3 Memory: PASS ✅ (stable, no leaks)

## Issues Found
- None

## Recommendation
✅ **APPROVED FOR PRODUCTION**
Ready to deploy to live environment.

Signed: [TESTER] on [DATE]
```

---

## CONCLUSION

This FOT suite comprehensively validates all 5 levels:
1. **Unit** (individual workflows)
2. **Integration** (end-to-end)
3. **Stress** (high load)
4. **Failure** (error handling)
5. **Performance** (SLA compliance)

**Expected Duration**: 4-6 hours  
**Expected Pass Rate**: >95%  
**Time to Production**: 48-72 hours after passing FOT

---

**Document Version**: 1.0  
**Status**: Ready for Testing  
**Last Updated**: August 4, 2026

