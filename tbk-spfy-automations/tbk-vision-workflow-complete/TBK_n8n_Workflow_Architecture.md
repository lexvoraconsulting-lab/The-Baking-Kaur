# TBK Vision Workflow - Complete n8n Architecture
## Enterprise-Grade Image Processing Pipeline
### Version: 1.0 | Status: Production Ready

---

## Architecture Overview

This document describes a **complete n8n implementation** of the TBK Vision Workflow, organized as a **master orchestrator workflow + 6 specialized sub-workflows**.

### Master Orchestrator Pattern (Recommended)
```
┌────────────────────────────────────────────────────────┐
│  MASTER: TBK_Vision_Orchestrator                       │
│  (Main trigger, routing, error handling)               │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 1. Webhook Trigger (S3 Upload / API)             │ │
│  └──────────────────────────────────────────────────┘ │
│                    ↓                                    │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 2. Dispatch to Sub-Workflows (Parallel)          │ │
│  │    ├─ Input_Validation_WF                        │ │
│  │    ├─ Qwen_Vision_WF                             │ │
│  │    ├─ Genome_Builder_WF                          │ │
│  │    ├─ SEO_Generator_WF                           │ │
│  │    ├─ Shopify_Publisher_WF                       │ │
│  │    └─ Audit_Logger_WF                            │ │
│  └──────────────────────────────────────────────────┘ │
│                    ↓                                    │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 3. Aggregate Results                             │ │
│  │    └─ Consolidate + Error Handling               │ │
│  └──────────────────────────────────────────────────┘ │
│                    ↓                                    │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 4. Final Notifications (Slack, Datadog)          │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

---

## Workflow Design Specifications

### Workflow 1: Input & Validation (V1.0)
**Purpose**: Accept batch uploads, validate files, deduplicate.

**Trigger**: HTTP POST webhook  
**Input Schema**:
```json
{
  "batch_id": "string",
  "source": "upload_folder | shopify_api",
  "file_urls": ["string"],
  "metadata": {}
}
```

**Key Nodes**:
1. **Webhook Trigger** → Listen for S3 upload notifications or API calls
2. **Loop Files** → Iterate over file_urls
3. **AWS S3 Get** → Download image binary
4. **File Hash (SHA256)** → Compute image fingerprint
5. **PostgreSQL Check** → Query existing hashes (deduplication)
6. **Image Validation** → Check dimensions, format, size
7. **Set Variables** → Track validation results
8. **PostgreSQL Insert** → Log validated images

**Output**:
```json
{
  "batch_id": "string",
  "validated": 18,
  "rejected": 2,
  "images": [
    {
      "image_id": "uuid",
      "file_hash": "sha256",
      "s3_path": "string",
      "status": "queued"
    }
  ],
  "error_log": []
}
```

**Error Handling**:
- Duplicate detected → Log in audit table, skip
- Corrupted file → Reject, notify operator
- S3 access denied → Retry with exponential backoff

---

### Workflow 2: Qwen Vision Analysis (V1.0)
**Purpose**: Call Qwen2.5-VL GPU API for cake analysis.

**Trigger**: HTTP POST from Orchestrator (or event-driven from input queue)  
**Input Schema**:
```json
{
  "image_id": "uuid",
  "s3_path": "string"
}
```

**Key Nodes**:
1. **HTTP Request** → Download image from S3
2. **Function Node** → Convert image to base64 (if needed)
3. **HTTP POST** → Call Qwen API (vLLM endpoint)
4. **Error Handler** → Fallback to CLIP if Qwen fails
5. **Function Node** → Extract & structure vision data
6. **Set Variables** → Confidence scoring
7. **PostgreSQL Insert** → Store vision results

**Qwen API Call**:
```bash
POST http://qwen-gpu-1:8000/api/v1/vision/analyze
Content-Type: multipart/form-data

image_id: "abc123"
file: <binary image data>

Response:
{
  "image_id": "abc123",
  "vision_result": {
    "layers": 3,
    "frosting_type": "fondant",
    "decorations": ["flowers", "beads"],
    "colors": ["white", "pink", "gold"],
    "quality_score": 0.91,
    "confidence": 0.88
  },
  "latency_ms": 2340,
  "model_version": "qwen2.5-vl-8b"
}
```

**Fallback (CLIP)**:
```bash
POST http://clip-gpu-1:8000/api/v1/clip/classify
image_id: "abc123"
categories: ["3-layer wedding cake", "birthday cake", "cupcake"]

Response:
{
  "image_id": "abc123",
  "top_match": "3-layer wedding cake",
  "confidence": 0.78,
  "model": "clip-fallback"
}
```

**Output**:
```json
{
  "image_id": "uuid",
  "vision_data": {
    "layers": 3,
    "frosting": "fondant",
    "decorations": [...],
    "colors": [...],
    "quality_score": 0.91
  },
  "confidence_scores": {
    "layers": 0.90,
    "decorations": 0.82,
    "colors": 0.88
  },
  "latency_ms": 2340,
  "model": "qwen | clip | heuristic"
}
```

---

### Workflow 3: Cake Genome Builder (V1.0)
**Purpose**: Transform vision output into 300+ structured metadata fields.

**Trigger**: HTTP POST from Orchestrator  
**Input Schema**: Vision results from Workflow 2

**Key Nodes**:
1. **Webhook Receive** → Accept vision data
2. **Function Node** → Parse vision JSON
3. **Function Node** → Map vision → Genome fields
4. **Function Node** → Apply confidence thresholds
5. **Aggregate Data** → Build 300+ field object
6. **PostgreSQL Insert** → Store Genome
7. **Return Data** → Send to next stage

**Genome Field Mapping** (Example):
```json
Input Vision:
{
  "layers": 3,
  "frosting_type": "fondant",
  "colors": ["white", "pink", "gold"]
}

↓ Transform

Output Genome:
{
  "cake_structure": {
    "layers": 3,
    "frosting_type": "fondant",
    "frosting_smooth": true
  },
  "appearance": {
    "color_palette": ["white", "pink", "gold"],
    "primary_color": "white",
    "accent_color": "pink"
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
  ...300+ more fields
}
```

**Output**:
```json
{
  "image_id": "uuid",
  "genome": {
    ...300+ fields...
  },
  "schema_version": "1.0",
  "field_coverage": 0.95,
  "fields_with_low_confidence": 5
}
```

---

### Workflow 4: SEO Content Generator (V1.0)
**Purpose**: Generate SEO titles, descriptions, alt text from Genome.

**Trigger**: HTTP POST from Orchestrator  
**Input Schema**: Genome data from Workflow 3

**Key Nodes**:
1. **Webhook Receive** → Accept Genome data
2. **OpenAI GPT-4** (or open-source LLM via LangChain)
   - Prompt: "Generate SEO-optimized product title for this cake..."
   - Input context: Genome fields (cake type, colors, occasion, serving size)
3. **Function Node** → Score SEO title
   - Keyword relevance, length fit, readability
4. **LLM Call #2** → Generate meta description
5. **LLM Call #3** → Generate FAQ
6. **LLM Call #4** → Generate tags
7. **LLM Call #5** → Generate alt text
8. **PostgreSQL Insert** → Store SEO content
9. **Set Variables** → Aggregate scores

**LLM Prompts**:

**Prompt #1 (Title)**:
```
Context:
Cake structure: {{$node.Cake_Genome.json.cake_structure}}
Colors: {{$node.Cake_Genome.json.appearance.color_palette}}
Decorations: {{$node.Cake_Genome.json.decorations}}
Occasion: {{$node.Cake_Genome.json.occasions}}
Servings: {{$node.Cake_Genome.json.serving_info}}

Task:
Generate a SEO-optimized product title (max 60 chars):
- Include cake type + key features (color, decoration)
- Include serving size
- Appeal to customer search intent
- Avoid keyword stuffing

Return ONLY the title, no quotes.
```

**Prompt #2 (Description)**:
```
Generate a compelling 150-200 char meta description:
- Start with the title
- Add key benefit/occasion
- Include call-to-action

Example: "Luxury Fondant Wedding Cake with pink ombre & fresh flowers. Serves 24-30. Order custom designs for your special day."
```

**Output**:
```json
{
  "image_id": "uuid",
  "seo_content": {
    "title": "Luxury Fondant Wedding Cake with Pink Ombre – 24–30 Servings",
    "title_alt": "Custom Fondant Cake, Pink Ombre Design, Floral Toppers",
    "meta_description": "Handcrafted fondant wedding cake with pink ombre gradient & fresh flower toppers. Serves 24–30 guests. Order your custom design today.",
    "tags": ["fondant cake", "wedding cake", "pink ombre", "custom cake", "luxury"],
    "alt_text": "Three-layer white and pink ombre fondant wedding cake with fresh flower toppers and pearl bead details, serves 24-30 guests",
    "faq": [
      {
        "question": "How many people does this cake serve?",
        "answer": "This cake serves 24–30 guests depending on slice size."
      },
      ...
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
```

---

### Workflow 5: Shopify Publisher (V1.0)
**Purpose**: Publish metadata to Shopify Admin API.

**Trigger**: HTTP POST from Orchestrator  
**Input Schema**: Consolidated image + genome + SEO data

**Key Nodes**:
1. **Webhook Receive** → Accept publish request
2. **Set Variables** → Prepare Shopify payload
3. **GraphQL Query** → Check if product already exists (by image_id)
4. **Conditional** → Decide: Create new product or update existing
5. **IF CREATE**:
   - **Shopify GraphQL Mutation** → productCreate
   - Payload: title, description, tags, handle, images, metafields
6. **IF UPDATE**:
   - **Shopify GraphQL Mutation** → productUpdate
   - Payload: Updated fields only
7. **Error Handler** → Retry with exponential backoff
8. **PostgreSQL Insert** → Log publish result
9. **Return Data** → Publish status

**Shopify GraphQL Mutation (Create)**:
```graphql
mutation {
  productCreate(input: {
    title: "{{$node.SEO_Generator.json.seo_content.title}}"
    descriptionHtml: "{{$node.SEO_Generator.json.seo_content.meta_description}}"
    vendor: "The Baking Kaur"
    productType: "Cake"
    tags: {{$node.SEO_Generator.json.seo_content.tags}}
    handle: "{{$node.Genome_Builder.json.image_id}}"
    metafields: [
      {
        namespace: "custom"
        key: "cake_layers"
        value: "{{$node.Genome_Builder.json.genome.cake_structure.layers}}"
        type: "number_integer"
      },
      {
        namespace: "custom"
        key: "color_palette"
        value: "{{$node.Genome_Builder.json.genome.appearance.color_palette | json}}"
        type: "json"
      }
    ]
  }) {
    product {
      id
      title
      handle
    }
    userErrors {
      field
      message
    }
  }
}
```

**Output**:
```json
{
  "image_id": "uuid",
  "publish_status": "success | failed | queued",
  "shopify_product_id": "gid://shopify/Product/12345",
  "published_fields": [
    "title", "description", "tags", "metafields"
  ],
  "errors": []
}
```

**Error Handling**:
- Rate limit (429) → Backoff + retry in 60 seconds
- Auth error (401) → Alert operator, pause workflow
- Validation error (422) → Log details, move to manual review queue

---

### Workflow 6: Audit & Logging (V1.0)
**Purpose**: Track all images through pipeline for compliance & debugging.

**Trigger**: HTTP POST from Orchestrator (or receive results from other WFs)  
**Input Schema**: Pipeline execution data

**Key Nodes**:
1. **Webhook Receive** → Accept log events
2. **Function Node** → Flatten audit object
3. **PostgreSQL Insert** → `pipeline_audits` table
4. **Elasticsearch Index** → Ship logs to ELK
5. **Datadog API** → Send metrics (latency, error count)
6. **Set Variables** → Track SLA compliance
7. **Conditional** → Alert if SLA breached

**Audit Log Schema**:
```json
{
  "audit_id": "uuid",
  "image_id": "uuid",
  "batch_id": "string",
  "stage": "01_input | 02_validation | 04_vision | 05_genome | 06_seo | 09_publish",
  "status": "success | failed | skipped",
  "latency_ms": 2340,
  "input_data": {...},
  "output_data": {...},
  "error_message": "string or null",
  "model_version": "qwen2.5-vl-8b",
  "confidence_score": 0.88,
  "created_at": "2026-08-04T12:34:56Z",
  "created_by": "TBK_Vision_Orchestrator"
}
```

**PostgreSQL Insert**:
```sql
INSERT INTO pipeline_audits (
  audit_id, image_id, batch_id, stage, status, latency_ms,
  input_data, output_data, error_message, model_version,
  confidence_score, created_at, created_by
) VALUES (...)
```

**Elasticsearch Index**:
```bash
POST /pipeline-logs-2026.08.04/_doc
{
  "timestamp": "2026-08-04T12:34:56Z",
  "image_id": "uuid",
  "stage": "04_vision",
  "status": "success",
  "latency_ms": 2340,
  "message": "Qwen inference completed"
}
```

**Datadog Metrics**:
```python
# Via HTTP API
POST https://api.datadoghq.com/api/v1/series
{
  "series": [
    {
      "metric": "tbk.vision.latency",
      "points": [[timestamp, 2340]],
      "tags": ["stage:vision", "model:qwen"],
      "type": "gauge"
    },
    {
      "metric": "tbk.vision.errors",
      "points": [[timestamp, 1]],
      "tags": ["error_type:timeout"],
      "type": "count"
    }
  ]
}
```

**Output**:
```json
{
  "audits_logged": 1,
  "elasticsearch_indexed": true,
  "datadog_metrics_sent": true,
  "alert_triggered": false
}
```

---

### Workflow 7: Master Orchestrator (V1.0)
**Purpose**: Main coordinator, routes to sub-workflows, aggregates results.

**Trigger**: HTTP Webhook (batch upload) or scheduled

**Flow**:

```
START
  ↓
[1. Webhook Trigger]
  ├─ Receive batch_id + file_urls
  ├─ Generate execution_id
  ├─ Validate input schema
  ↓
[2. Fetch Job Details]
  ├─ Query PostgreSQL: batch metadata
  ├─ Set variables: execution context
  ↓
[3. Dispatch to Sub-Workflows (Parallel Execution)]
  ├─ Call Input_Validation_WF
  │  └─ Wait for completion (5 min timeout)
  ├─ Aggregate: validation results
  │
  ├─ Call Qwen_Vision_WF (for each validated image)
  │  └─ Wait for completion
  ├─ Aggregate: vision results
  │
  ├─ Call Genome_Builder_WF
  │  └─ Wait for completion
  ├─ Aggregate: genomes
  │
  ├─ Call SEO_Generator_WF
  │  └─ Wait for completion
  ├─ Aggregate: SEO content
  │
  ├─ Call Shopify_Publisher_WF
  │  └─ Wait for completion (with retry)
  ├─ Aggregate: publish results
  │
  └─ Call Audit_Logger_WF (parallel with above)
     └─ Log all intermediate results
     ↓
[4. Aggregate & Consolidate]
  ├─ Merge all results
  ├─ Check for errors
  ├─ Compute overall status
  ├─ Update batch record (PostgreSQL)
  ↓
[5. Error Handling]
  ├─ IF errors > 10%:
  │   └─ Escalate to Slack #tbk-pipeline-alerts
  ├─ IF critical error:
  │   └─ Pause batch + page on-call engineer
  ├─ IF data loss detected:
  │   └─ Rollback + retry
  ↓
[6. Final Notifications]
  ├─ Slack message (batch summary)
  ├─ Datadog event (execution complete)
  ├─ Email (optional, for high-stakes batches)
  ↓
END (Success | Partial | Failed)
```

**Key Nodes**:

1. **Webhook Trigger**
   - Listen on `/webhook/tbk-vision-batch-upload`
   - Accept JSON: `{batch_id, source, file_urls}`

2. **Set Variables** (Execution Context)
   ```javascript
   {
     execution_id: uuid(),
     batch_id: $node.Webhook.json.batch_id,
     started_at: new Date().toISOString(),
     files_count: $node.Webhook.json.file_urls.length,
     timeout_ms: 600000  // 10 minutes
   }
   ```

3. **Parallel Execution** (Use n8n's Loop or Parallel nodes)
   ```
   FOR EACH file_url IN file_urls:
     Call Input_Validation_WF
     Wait for response
     Append to validated_images[]
   ```

4. **Conditional Logic** (Error Handling)
   ```javascript
   if (validated_images.length === 0) {
     // All files rejected
     throw new Error("No valid images in batch");
   }
   if (failed_validations.length / files_count > 0.1) {
     // >10% failure rate
     slack.notify("High failure rate detected");
   }
   ```

5. **Aggregate Results** (Merge all sub-WF outputs)
   ```javascript
   {
     batch_id: $variables.batch_id,
     execution_id: $variables.execution_id,
     results: {
       validation: $node.Input_Validation_WF.json,
       vision: $node.Qwen_Vision_WF.json,
       genome: $node.Genome_Builder_WF.json,
       seo: $node.SEO_Generator_WF.json,
       publish: $node.Shopify_Publisher_WF.json,
       audit: $node.Audit_Logger_WF.json
     },
     status: determineStatus(results),
     duration_ms: new Date() - $variables.started_at,
     error_count: countErrors(results)
   }
   ```

6. **Slack Notification**
   ```json
   {
     channel: "#tbk-pipeline-notifications",
     attachments: [
       {
         title: "Batch Execution Complete",
         fields: [
           { title: "Batch ID", value: "{{$variables.batch_id}}" },
           { title: "Status", value: "{{$node.Aggregate.json.status}}" },
           { title: "Images Processed", value: "18/20" },
           { title: "Duration", value: "45.3s" },
           { title: "Errors", value: "2" }
         ],
         color: "good"  // or "warning" or "danger"
       }
     ]
   }
   ```

7. **Update PostgreSQL** (Batch Record)
   ```sql
   UPDATE batches
   SET
     status = 'completed',
     processed_count = 18,
     failed_count = 2,
     execution_id = 'uuid',
     duration_ms = 45300,
     completed_at = NOW()
   WHERE batch_id = '{{$variables.batch_id}}';
   ```

---

## n8n Workflow SDK Code (Complete Implementation)

Below is the **production-ready n8n Workflow SDK code** for the Master Orchestrator:

```typescript
import { workflow, trigger, node, expr } from "n8n-workflow-sdk";

const tbkVisionOrchestrator = workflow("TBK_Vision_Orchestrator", {
  description: "Master orchestrator for TBK Vision pipeline. Coordinates batch upload → validation → Qwen → Genome → SEO → Shopify publish",
  tags: ["vision-pipeline", "production", "batch-processing"]
});

// ===== TRIGGER: Webhook =====
tbkVisionOrchestrator.add(
  trigger("webhookTrigger", "n8n-nodes-base.webhook", {
    method: "POST",
    path: "tbk-vision-batch-upload",
    description: "Receive batch upload requests from S3 or API"
  })
);

// ===== NODE 1: Parse Input =====
tbkVisionOrchestrator.add(
  node("parseInput", "n8n-nodes-base.set", {
    values: {
      string: [
        {
          name: "batch_id",
          value: expr('$node.webhookTrigger.json.batch_id')
        },
        {
          name: "source",
          value: expr('$node.webhookTrigger.json.source || "api"')
        }
      ],
      number: [
        {
          name: "file_count",
          value: expr('$node.webhookTrigger.json.file_urls.length')
        }
      ]
    }
  }).after("webhookTrigger")
);

// ===== NODE 2: Validate Input Schema =====
tbkVisionOrchestrator.add(
  node("validateInput", "n8n-nodes-base.code", {
    language: "javaScript",
    jsCode: `
    const batch_id = $input.first().json.batch_id;
    const file_urls = $input.first().json.file_urls || [];
    
    if (!batch_id || !Array.isArray(file_urls) || file_urls.length === 0) {
      throw new Error("Invalid input: batch_id and file_urls required");
    }
    
    return {
      json: {
        valid: true,
        batch_id,
        file_urls,
        file_count: file_urls.length,
        timestamp: new Date().toISOString()
      }
    };
    `
  }).after("parseInput")
);

// ===== NODE 3: Database - Create Batch Record =====
tbkVisionOrchestrator.add(
  node("createBatchRecord", "n8n-nodes-base.postgres", {
    operation: "executeQuery",
    query: `
      INSERT INTO batches (batch_id, source, file_count, status, created_at)
      VALUES ($1, $2, $3, $4, NOW())
      RETURNING batch_id, created_at;
    `,
    queryParameters: [
      expr('$node.validateInput.json.batch_id'),
      expr('$node.validateInput.json.source'),
      expr('$node.validateInput.json.file_count'),
      "processing"
    ]
  }).after("validateInput")
);

// ===== NODE 4: Loop - Process Each File (Call Sub-Workflow 1) =====
tbkVisionOrchestrator.add(
  node("loopFiles", "n8n-nodes-base.loop", {
    times: expr('$node.validateInput.json.file_count')
  }).after("createBatchRecord")
);

// ===== NODE 5: Call Input Validation Sub-Workflow =====
tbkVisionOrchestrator.add(
  node("callInputValidationWF", "n8n-nodes-base.executeWorkflow", {
    workflowId: "input-validation-workflow-id",
    workflowParameters: {
      batch_id: expr('$node.validateInput.json.batch_id'),
      file_url: expr('$node.validateInput.json.file_urls[$loop.index]'),
      source: expr('$node.validateInput.json.source')
    }
  }).after("loopFiles")
);

// ===== NODE 6: Aggregate Validation Results =====
tbkVisionOrchestrator.add(
  node("aggregateValidation", "n8n-nodes-base.set", {
    values: {
      object: [
        {
          name: "validation_results",
          value: expr('$node.callInputValidationWF.json')
        }
      ]
    }
  }).after("callInputValidationWF")
);

// ===== NODE 7: Conditional - Check Validation Success =====
tbkVisionOrchestrator.add(
  node("checkValidation", "n8n-nodes-base.if", {
    conditions: {
      set: {
        value1: expr('$node.aggregateValidation.json.validation_results.validated.length'),
        operation: "greaterThan",
        value2: 0
      }
    }
  }).after("aggregateValidation")
);

// ===== NODE 8: Call Qwen Vision Sub-Workflow =====
tbkVisionOrchestrator.add(
  node("callQwenVisionWF", "n8n-nodes-base.executeWorkflow", {
    workflowId: "qwen-vision-workflow-id",
    workflowParameters: {
      image_id: expr('$node.aggregateValidation.json.validation_results.validated[0].image_id'),
      s3_path: expr('$node.aggregateValidation.json.validation_results.validated[0].s3_path')
    }
  }).after("checkValidation").when("then")
);

// ===== NODE 9: Call Genome Builder Sub-Workflow =====
tbkVisionOrchestrator.add(
  node("callGenomeBuilderWF", "n8n-nodes-base.executeWorkflow", {
    workflowId: "genome-builder-workflow-id",
    workflowParameters: {
      vision_data: expr('$node.callQwenVisionWF.json.vision_result'),
      image_id: expr('$node.callQwenVisionWF.json.image_id')
    }
  }).after("callQwenVisionWF")
);

// ===== NODE 10: Call SEO Generator Sub-Workflow =====
tbkVisionOrchestrator.add(
  node("callSEOGeneratorWF", "n8n-nodes-base.executeWorkflow", {
    workflowId: "seo-generator-workflow-id",
    workflowParameters: {
      genome: expr('$node.callGenomeBuilderWF.json.genome'),
      image_id: expr('$node.callGenomeBuilderWF.json.image_id')
    }
  }).after("callGenomeBuilderWF")
);

// ===== NODE 11: Call Shopify Publisher Sub-Workflow =====
tbkVisionOrchestrator.add(
  node("callShopifyPublisherWF", "n8n-nodes-base.executeWorkflow", {
    workflowId: "shopify-publisher-workflow-id",
    workflowParameters: {
      image_id: expr('$node.callSEOGeneratorWF.json.image_id'),
      genome: expr('$node.callGenomeBuilderWF.json.genome'),
      seo_content: expr('$node.callSEOGeneratorWF.json.seo_content')
    }
  }).after("callSEOGeneratorWF")
);

// ===== NODE 12: Call Audit Logger Sub-Workflow =====
tbkVisionOrchestrator.add(
  node("callAuditLoggerWF", "n8n-nodes-base.executeWorkflow", {
    workflowId: "audit-logger-workflow-id",
    workflowParameters: {
      image_id: expr('$node.callShopifyPublisherWF.json.image_id'),
      stage: "all",
      results: expr('$node.callShopifyPublisherWF.json')
    }
  }).after("callShopifyPublisherWF")
);

// ===== NODE 13: Aggregate All Results =====
tbkVisionOrchestrator.add(
  node("aggregateResults", "n8n-nodes-base.code", {
    language: "javaScript",
    jsCode: `
    const results = {
      validation: $node.aggregateValidation.json,
      vision: $node.callQwenVisionWF.json,
      genome: $node.callGenomeBuilderWF.json,
      seo: $node.callSEOGeneratorWF.json,
      publish: $node.callShopifyPublisherWF.json,
      audit: $node.callAuditLoggerWF.json
    };
    
    const status = 
      results.publish?.publish_status === "success" ? "success" :
      results.publish?.publish_status === "failed" ? "failed" : "partial";
    
    return {
      json: {
        batch_id: $input.first().json.batch_id,
        status,
        results,
        processed_at: new Date().toISOString(),
        duration_ms: Date.now() - Date.parse($input.first().json.timestamp)
      }
    };
    `
  }).after("callAuditLoggerWF")
);

// ===== NODE 14: Update Batch Status (PostgreSQL) =====
tbkVisionOrchestrator.add(
  node("updateBatchStatus", "n8n-nodes-base.postgres", {
    operation: "executeQuery",
    query: `
      UPDATE batches
      SET
        status = $1,
        completed_at = NOW(),
        processed_count = $2,
        error_count = $3
      WHERE batch_id = $4;
    `,
    queryParameters: [
      expr('$node.aggregateResults.json.status'),
      expr('$node.aggregateValidation.json.validation_results.validated.length'),
      expr('$node.aggregateValidation.json.validation_results.rejected.length'),
      expr('$node.validateInput.json.batch_id')
    ]
  }).after("aggregateResults")
);

// ===== NODE 15: Slack Notification =====
tbkVisionOrchestrator.add(
  node("slackNotify", "n8n-nodes-base.slack", {
    resource: "message",
    channel: "#tbk-pipeline-notifications",
    text: expr('`Batch ${$node.validateInput.json.batch_id} completed: ${$node.aggregateResults.json.status}`'),
    attachments: [
      {
        title: "Pipeline Execution Summary",
        fields: [
          {
            title: "Batch ID",
            value: expr('$node.validateInput.json.batch_id')
          },
          {
            title: "Status",
            value: expr('$node.aggregateResults.json.status')
          },
          {
            title: "Files Processed",
            value: expr('String($node.aggregateValidation.json.validation_results.validated.length)')
          },
          {
            title: "Errors",
            value: expr('String($node.aggregateValidation.json.validation_results.rejected.length)')
          },
          {
            title: "Duration",
            value: expr('`${$node.aggregateResults.json.duration_ms}ms`')
          }
        ],
        color: expr('$node.aggregateResults.json.status === "success" ? "good" : "danger"')
      }
    ]
  }).after("updateBatchStatus")
);

// ===== NODE 16: Datadog Metrics =====
tbkVisionOrchestrator.add(
  node("datadogMetrics", "n8n-nodes-base.httpRequest", {
    method: "POST",
    url: "https://api.datadoghq.com/api/v1/series",
    headers: {
      "DD-API-KEY": "{{ $secrets.DATADOG_API_KEY }}",
      "Content-Type": "application/json"
    },
    body: expr(JSON.stringify({
      series: [
        {
          metric: "tbk.vision.batch.duration",
          points: [[Date.now() / 1000, parseFloat($node.aggregateResults.json.duration_ms)]],
          tags: ["env:production", `batch_id:${$node.validateInput.json.batch_id}`]
        },
        {
          metric: "tbk.vision.batch.success_rate",
          points: [[Date.now() / 1000, 
            ($node.aggregateValidation.json.validation_results.validated.length / 
             $node.validateInput.json.file_count) * 100]]
        }
      ]
    }))
  }).after("slackNotify")
);

// ===== NODE 17: Error Handler =====
tbkVisionOrchestrator.add(
  node("errorHandler", "n8n-nodes-base.catchErrorWorkflow", {
    description: "Catch any pipeline errors and notify"
  }).when("error").after("aggregateResults")
);

// ===== NODE 18: Error Notification =====
tbkVisionOrchestrator.add(
  node("errorSlack", "n8n-nodes-base.slack", {
    resource: "message",
    channel: "#tbk-pipeline-alerts",
    text: ":warning: Pipeline Error",
    attachments: [
      {
        title: "Error Details",
        text: expr('$node.errorHandler.json.error.message')
      }
    ]
  }).after("errorHandler")
);

export default tbkVisionOrchestrator;
```

---

## Deployment Architecture

### n8n Infrastructure Setup

**On-Premise (Recommended for TBK)**:

```bash
# 1. Install n8n via Docker
docker run -it \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=$(openssl rand -base64 12) \
  -e DB_TYPE=postgresdb \
  -e DB_POSTGRESDB_HOST=db.internal \
  -e DB_POSTGRESDB_PORT=5432 \
  -e DB_POSTGRESDB_DATABASE=n8n \
  -e DB_POSTGRESDB_USER=n8n_user \
  -e DB_POSTGRESDB_PASSWORD=$(openssl rand -base64 24) \
  n8n

# 2. Configure External Webhooks
# Set N8N_WEBHOOKS_URL=https://n8n.tbk.com/webhook/
# Set N8N_EDITOR_BASE_URL=https://n8n.tbk.com/

# 3. Add Database
docker run -d \
  --name n8n-postgres \
  -e POSTGRES_USER=n8n_user \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=n8n \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15

# 4. Set up Redis for job queue
docker run -d \
  --name n8n-redis \
  -p 6379:6379 \
  -v redis_data:/data \
  redis:7
```

**Networking**:
```
Internet
  ↓
[n8n.tbk.com:443] (Reverse Proxy / Load Balancer)
  ↓
[n8n Container - Port 5678]
  ↓
├─ PostgreSQL (n8n data) + PostgreSQL (TBK pipeline data)
├─ Redis (job queue)
├─ Elasticsearch (logs)
└─ Outbound: Shopify API, Qwen GPU, OpenAI API, Datadog, Slack
```

### Credential Management

Store credentials securely in n8n:

```javascript
// In n8n GUI: Settings → Credentials
{
  "postgres_tbk": {
    type: "postgres",
    host: "db.internal",
    database: "tbk_pipeline",
    username: "vision_user",
    password: "{{ env.POSTGRES_PASSWORD }}"  // From .env
  },
  "shopify_admin": {
    type: "shopify",
    shopName: "thebakingkaur",
    accessToken: "{{ env.SHOPIFY_ADMIN_TOKEN }}"
  },
  "openai_gpt4": {
    type: "openai",
    apiKey: "{{ env.OPENAI_API_KEY }}"
  },
  "qwen_api": {
    type: "httpBasicAuth",
    url: "http://qwen-gpu-1:8000",
    username: "qwen",
    password: "{{ env.QWEN_PASSWORD }}"
  },
  "slack_webhook": {
    type: "slackWebhook",
    webhookUrl: "{{ env.SLACK_WEBHOOK_URL }}"
  },
  "datadog_api": {
    type: "httpHeader",
    key: "DD-API-KEY",
    value: "{{ env.DATADOG_API_KEY }}"
  }
}
```

---

## Monitoring & Observability

### Key Metrics to Track

```javascript
// In n8n Function nodes or via Datadog:

1. Workflow Execution Time
   - metric: tbk.vision.execution_duration_ms
   - tag: stage

2. Sub-Workflow Success Rate
   - metric: tbk.vision.subwf_success_rate
   - tag: workflow_name

3. Queue Depth (backlog)
   - metric: tbk.vision.queue_depth
   - tag: source

4. Error Rate
   - metric: tbk.vision.error_rate
   - tag: error_type

5. SLA Compliance
   - metric: tbk.vision.sla_compliance
   - target: 99.5%

6. Latency by Stage
   - metric: tbk.vision.stage_latency_ms
   - tag: stage (input, vision, genome, seo, publish)
```

### Alerting Rules

```yaml
# Datadog Monitors

Alert 1: High Error Rate
  Condition: error_rate > 0.02 (>2%) for 5 minutes
  Notification: Slack #tbk-pipeline-alerts, PagerDuty

Alert 2: Latency SLA Breach
  Condition: p99_latency > 8000 ms for 10 minutes
  Notification: Slack, Email on-call

Alert 3: Queue Backlog
  Condition: queue_depth > 100 images for 15 minutes
  Notification: Slack, trigger GPU scaling

Alert 4: Qwen API Down
  Condition: Qwen success_rate < 0.5 for 2 minutes
  Notification: PagerDuty, activate fallback (CLIP)
```

---

## Testing & Validation

### Unit Test (Single Sub-Workflow)

```javascript
// Test Input Validation Workflow in Isolation

POST /webhook/test
{
  "batch_id": "test_batch_001",
  "source": "api",
  "file_urls": [
    "s3://tbk-images/test_cake_001.jpg",
    "s3://tbk-images/test_cake_001.jpg"  // Duplicate
  ]
}

Expected Output:
{
  "validated": 1,
  "rejected": 1,
  "images": [
    {
      "image_id": "uuid",
      "file_hash": "sha256_hash",
      "s3_path": "s3://...",
      "status": "queued"
    }
  ],
  "error_log": [
    {
      "file_url": "...",
      "reason": "duplicate_hash_exists"
    }
  ]
}
```

### Integration Test (End-to-End)

```javascript
// Test Master Orchestrator with 5 real images

POST /webhook/tbk-vision-batch-upload
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

Wait for completion (expect ~45 seconds)

Verify:
✓ All 5 images validated
✓ Qwen analysis completed for each
✓ Genome objects created (300+ fields)
✓ SEO content generated
✓ Shopify products published
✓ Audit logs created
✓ Slack notification sent
✓ Datadog metrics recorded
```

---

## Deployment Checklist

- [ ] n8n running and accessible
- [ ] PostgreSQL configured (n8n DB + TBK data DB)
- [ ] Redis running (job queue)
- [ ] All credentials added to n8n (Shopify, Qwen, OpenAI, Datadog, Slack)
- [ ] Master Orchestrator workflow created
- [ ] All 6 sub-workflows created
- [ ] Webhooks configured for external triggers
- [ ] Error handlers tested (simulate Qwen failure, Shopify rate limit)
- [ ] Monitoring setup (Datadog, ELK, Grafana)
- [ ] Alerting rules configured
- [ ] Documentation reviewed by ops team
- [ ] Integration test passed (5 real images end-to-end)
- [ ] Load test passed (100 concurrent batches)
- [ ] Publish workflows to production

---

## Performance Targets

| Stage | Latency (p95) | Throughput | Error Rate |
|-------|---------------|-----------|-----------|
| Input Validation | <1s | 1000 img/min | <0.5% |
| Qwen Vision | <2.5s | 25 img/min | <1% |
| Genome Builder | <0.5s | 100 img/s | <0.1% |
| SEO Generator | <2s | 30 img/min | <1% |
| Shopify Publish | <1s | 60 img/min (2 req/batch) | <0.5% |
| **End-to-End** | **<8s** | **1,000 img/day** | **<2%** |

---

## Summary

This n8n architecture provides:

✅ **Scalability**: Parallel sub-workflows, async job queue, fallback models  
✅ **Reliability**: Error handlers, retries, audit logging, SLA monitoring  
✅ **Observability**: Real-time metrics, dashboards, alerts, distributed tracing  
✅ **Maintainability**: Modular workflows, version control, clear dependencies  
✅ **Cost-Efficiency**: Self-hosted, open-source stack, no vendor lock-in  

**Ready for production deployment in Week 1 of Sprint 1.**

