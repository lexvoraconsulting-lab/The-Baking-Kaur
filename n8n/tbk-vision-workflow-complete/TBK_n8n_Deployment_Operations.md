# n8n Deployment & Operations Guide
## TBK Vision Workflow Pipeline
### Production Setup & Monitoring

---

## Part 1: Pre-Deployment Checklist

### Prerequisites
- [ ] Docker / Docker Compose installed
- [ ] PostgreSQL 15+ available
- [ ] Redis 7+ available
- [ ] Shopify Admin API access token
- [ ] OpenAI / LLaMA API keys
- [ ] Datadog account + API key
- [ ] Slack workspace + webhook URL
- [ ] Qwen GPU endpoint (or API key)
- [ ] S3/Blob storage configured
- [ ] SSL/TLS certificates (for production)

### Environment Setup
```bash
# 1. Create .env file
cat > .env << 'EOF'
# n8n Database
N8N_DB_TYPE=postgresdb
N8N_DB_POSTGRESDB_HOST=postgres
N8N_DB_POSTGRESDB_PORT=5432
N8N_DB_POSTGRESDB_DATABASE=n8n
N8N_DB_POSTGRESDB_USER=n8n_user
N8N_DB_POSTGRESDB_PASSWORD=$(openssl rand -base64 32)

# n8n Settings
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=$(openssl rand -base64 24)
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
N8N_DOMAIN=n8n.tbk.com
NODE_ENV=production

# Redis (for job queue)
REDIS_URL=redis://redis:6379

# External APIs
SHOPIFY_ADMIN_TOKEN=shpat_xxxxxxxxxx
SHOPIFY_STORE=thebakingkaur
OPENAI_API_KEY=sk-xxxxxxxxxx
DATADOG_API_KEY=xxxxxxxxxxx
DATADOG_APP_KEY=xxxxxxxxxxx
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
QWEN_API_ENDPOINT=http://qwen-gpu-1:8000
QWEN_API_KEY=xxxxxxxxxxxx

# PostgreSQL (TBK pipeline data)
TBK_DB_HOST=postgres
TBK_DB_PORT=5432
TBK_DB_DATABASE=tbk_pipeline
TBK_DB_USER=vision_user
TBK_DB_PASSWORD=$(openssl rand -base64 32)

# Elasticsearch
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASSWORD=$(openssl rand -base64 32)

# Workflow IDs (populated after creation)
TBK_INPUT_VALIDATION_WF_ID=
TBK_QWEN_VISION_WF_ID=
TBK_GENOME_BUILDER_WF_ID=
TBK_SEO_GENERATOR_WF_ID=
TBK_SHOPIFY_PUBLISHER_WF_ID=
TBK_AUDIT_LOGGER_WF_ID=
EOF

# 2. Generate secure passwords
openssl rand -base64 32 > .secrets/db_password
openssl rand -base64 24 > .secrets/admin_password
```

---

## Part 2: Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.9'

services:
  # PostgreSQL (n8n database + TBK pipeline data)
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: n8n_user
      POSTGRES_PASSWORD: ${N8N_DB_POSTGRESDB_PASSWORD}
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d  # Initialize TBK schema
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis (n8n job queue)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # n8n Application
  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    environment:
      DB_TYPE: ${N8N_DB_TYPE}
      DB_POSTGRESDB_HOST: ${N8N_DB_POSTGRESDB_HOST}
      DB_POSTGRESDB_PORT: ${N8N_DB_POSTGRESDB_PORT}
      DB_POSTGRESDB_DATABASE: ${N8N_DB_POSTGRESDB_DATABASE}
      DB_POSTGRESDB_USER: ${N8N_DB_POSTGRESDB_USER}
      DB_POSTGRESDB_PASSWORD: ${N8N_DB_POSTGRESDB_PASSWORD}
      N8N_BASIC_AUTH_ACTIVE: ${N8N_BASIC_AUTH_ACTIVE}
      N8N_BASIC_AUTH_USER: ${N8N_BASIC_AUTH_USER}
      N8N_BASIC_AUTH_PASSWORD: ${N8N_BASIC_AUTH_PASSWORD}
      N8N_HOST: ${N8N_HOST}
      N8N_PORT: ${N8N_PORT}
      N8N_PROTOCOL: ${N8N_PROTOCOL}
      N8N_DOMAIN: ${N8N_DOMAIN}
      NODE_ENV: ${NODE_ENV}
      REDIS_URL: ${REDIS_URL}
      WEBHOOK_URL: https://${N8N_DOMAIN}/webhook/
      GENERIC_TIMEZONE: UTC
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/workflows  # Mount workflows
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - tbk_network
    labels:
      - "com.example.description=n8n workflow engine"

  # Elasticsearch (for logs)
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=${ELASTICSEARCH_PASSWORD}
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -s https://elastic:${ELASTICSEARCH_PASSWORD}@localhost:9200/_cluster/health | grep -q green"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Kibana (for ELK visualization)
  kibana:
    image: docker.elastic.co/kibana/kibana:8.6.0
    environment:
      - ELASTICSEARCH_HOSTS=https://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=${ELASTICSEARCH_PASSWORD}
      - xpack.security.enabled=true
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  # nginx (reverse proxy)
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs  # SSL certificates
    depends_on:
      - n8n
    networks:
      - tbk_network

volumes:
  postgres_data:
  redis_data:
  n8n_data:
  elasticsearch_data:

networks:
  tbk_network:
    driver: bridge
```

---

## Part 3: Database Initialization

```sql
-- init-scripts/01-tbk-schema.sql
-- Run this on first deployment

-- Create TBK Pipeline Databases
CREATE DATABASE tbk_pipeline;

-- Connect to tbk_pipeline
\c tbk_pipeline;

-- Batches Table
CREATE TABLE batches (
  batch_id VARCHAR(255) PRIMARY KEY,
  execution_id UUID NOT NULL,
  source VARCHAR(50),  -- 'upload_folder', 'shopify_api', 'webhook'
  file_count INT,
  status VARCHAR(50),  -- 'processing', 'success', 'failed', 'partial'
  processed_count INT DEFAULT 0,
  error_count INT DEFAULT 0,
  execution_metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Images Table
CREATE TABLE images (
  image_id UUID PRIMARY KEY,
  batch_id VARCHAR(255) REFERENCES batches(batch_id),
  file_hash VARCHAR(64) UNIQUE,  -- SHA256
  s3_path VARCHAR(500),
  file_name VARCHAR(255),
  file_size INT,
  mime_type VARCHAR(50),
  width INT,
  height INT,
  status VARCHAR(50),  -- 'queued', 'processing', 'success', 'failed'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Vision Results Table
CREATE TABLE vision_results (
  vision_id UUID PRIMARY KEY,
  image_id UUID REFERENCES images(image_id),
  vision_data JSONB,  -- Qwen output
  confidence_scores JSONB,
  model_version VARCHAR(50),
  latency_ms INT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Cake Genomes Table
CREATE TABLE cake_genomes (
  genome_id UUID PRIMARY KEY,
  image_id UUID REFERENCES images(image_id),
  genome_data JSONB,  -- 300+ fields
  schema_version VARCHAR(10),
  field_coverage FLOAT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- SEO Content Table
CREATE TABLE seo_content (
  seo_id UUID PRIMARY KEY,
  image_id UUID REFERENCES images(image_id),
  title VARCHAR(255),
  meta_description VARCHAR(500),
  tags TEXT[],
  alt_text TEXT,
  faq JSONB,
  seo_scores JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Shopify Publishing Table
CREATE TABLE shopify_publishes (
  publish_id UUID PRIMARY KEY,
  image_id UUID REFERENCES images(image_id),
  shopify_product_id VARCHAR(255),
  publish_status VARCHAR(50),  -- 'queued', 'success', 'failed'
  published_fields TEXT[],
  error_message TEXT,
  attempts INT DEFAULT 0,
  last_attempt TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Pipeline Audit Logs
CREATE TABLE pipeline_audits (
  audit_id UUID PRIMARY KEY,
  image_id UUID REFERENCES images(image_id),
  batch_id VARCHAR(255),
  stage VARCHAR(50),
  status VARCHAR(50),
  latency_ms INT,
  input_data JSONB,
  output_data JSONB,
  error_message TEXT,
  model_version VARCHAR(50),
  confidence_score FLOAT,
  created_at TIMESTAMP DEFAULT NOW(),
  created_by VARCHAR(255)
);

-- Image Hashes (for deduplication)
CREATE TABLE image_hashes (
  hash_id UUID PRIMARY KEY,
  file_hash VARCHAR(64) UNIQUE,
  image_id UUID REFERENCES images(image_id),
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_images_batch_id ON images(batch_id);
CREATE INDEX idx_images_status ON images(status);
CREATE INDEX idx_vision_results_image_id ON vision_results(image_id);
CREATE INDEX idx_genomes_image_id ON cake_genomes(image_id);
CREATE INDEX idx_seo_image_id ON seo_content(image_id);
CREATE INDEX idx_publishes_image_id ON shopify_publishes(image_id);
CREATE INDEX idx_audits_image_id ON pipeline_audits(image_id);
CREATE INDEX idx_audits_batch_id ON pipeline_audits(batch_id);
CREATE INDEX idx_audits_stage ON pipeline_audits(stage);
CREATE INDEX idx_audits_created_at ON pipeline_audits(created_at);
```

---

## Part 4: Deployment Steps

### Step 1: Start Infrastructure
```bash
# Create directory structure
mkdir -p n8n-deployment/{certs,init-scripts,workflows,nginx}
cd n8n-deployment

# Start services
docker-compose up -d

# Wait for services to be healthy
docker-compose ps
# All should show "healthy" in STATUS column

# Verify PostgreSQL is ready
docker-compose exec postgres pg_isready -U n8n_user
# Output: accepting connections
```

### Step 2: Access n8n UI
```bash
# Open browser
https://n8n.tbk.com/

# Login
Username: admin (from .env)
Password: (from .env N8N_BASIC_AUTH_PASSWORD)

# Accept license (first time only)
```

### Step 3: Add Credentials in n8n

Navigate to **Settings → Credentials** and add:

```javascript
// 1. PostgreSQL (TBK Pipeline)
Type: PostgreSQL
Host: postgres
Port: 5432
Database: tbk_pipeline
User: vision_user
Password: (from .env)
Name: postgres_tbk_credentials
Save

// 2. Shopify
Type: Shopify
Shop: thebakingkaur.myshopify.com
Access Token: (from Shopify Admin)
Name: shopify_admin_credentials
Save

// 3. OpenAI
Type: OpenAI
API Key: (from OpenAI)
Name: openai_gpt4_credentials
Save

// 4. Slack Webhook
Type: Slack Webhook
Webhook URL: (from Slack)
Name: slack_webhook_credentials
Save

// 5. HTTP Header (Datadog)
Type: HTTP Header Authorization
Credential type: Bearer Token
Token: (from Datadog API)
Name: datadog_api_credentials
Save
```

### Step 4: Create Sub-Workflows (via UI)

1. **Input Validation Workflow**
   - Create from template or import from file
   - Save as "Input_Validation_Workflow"
   - Note the workflow ID

2. **Qwen Vision Workflow**
   - HTTP POST to Qwen GPU endpoint
   - Handle success/fallback to CLIP
   - Save as "Qwen_Vision_Workflow"

3. **Genome Builder Workflow**
   - Function node to transform vision → genome
   - Store in PostgreSQL
   - Save as "Genome_Builder_Workflow"

4. **SEO Generator Workflow**
   - OpenAI call for title/description
   - Save as "SEO_Generator_Workflow"

5. **Shopify Publisher Workflow**
   - Shopify GraphQL mutation
   - Handle rate limits + retries
   - Save as "Shopify_Publisher_Workflow"

6. **Audit Logger Workflow**
   - PostgreSQL insert
   - Elasticsearch indexing
   - Save as "Audit_Logger_Workflow"

### Step 5: Create Master Orchestrator

```bash
# Copy workflow code
cp TBK_n8n_Master_Orchestrator_Code.ts /path/to/workflows/

# Or import via n8n UI:
# 1. Click "+" in workflow list
# 2. Select "Import from File"
# 3. Upload TBK_n8n_Master_Orchestrator_Code.ts

# Update workflow IDs in Master Orchestrator
# Settings → Workflow → Parameters
# Set each sub-workflow ID:
# TBK_INPUT_VALIDATION_WF_ID=...
# TBK_QWEN_VISION_WF_ID=...
# (etc.)
```

### Step 6: Test Workflow

```bash
# 1. Go to Master Orchestrator
# 2. Click "Execute Workflow"
# 3. Provide test input:
{
  "batch_id": "test_integration_001",
  "source": "api",
  "file_urls": [
    "s3://tbk-images-test/cake_001.jpg"
  ]
}

# 4. Monitor execution in logs
# Expected duration: 30-45 seconds

# 5. Verify results
# - Slack notification received ✓
# - PostgreSQL batch record created ✓
# - Audit logs in Elasticsearch ✓
# - Datadog metrics recorded ✓
```

---

## Part 5: Monitoring & Observability

### Datadog Dashboard Setup

```bash
# Create dashboard via API
curl -X POST https://api.datadoghq.com/api/v1/dashboard \
  -H "DD-API-KEY: ${DATADOG_API_KEY}" \
  -d '{
    "title": "TBK Vision Pipeline",
    "widgets": [
      {
        "definition": {
          "type": "timeseries",
          "requests": [
            {
              "q": "avg:tbk.vision.batch.duration{*}"
            }
          ],
          "title": "Batch Duration (ms)"
        }
      },
      {
        "definition": {
          "type": "gauge",
          "requests": [
            {
              "q": "avg:tbk.vision.batch.success_rate{*}"
            }
          ],
          "title": "Success Rate (%)"
        }
      },
      {
        "definition": {
          "type": "timeseries",
          "requests": [
            {
              "q": "sum:tbk.vision.errors{*}"
            }
          ],
          "title": "Error Count"
        }
      }
    ]
  }'
```

### ELK Stack (Kibana)

1. Open Kibana: `http://localhost:5601`
2. Create Index Pattern: `pipeline-logs-*`
3. Create Dashboard:
   - Top-level metrics (errors, latency)
   - Logs by stage
   - Trace visualization

### Alerting Rules

```yaml
# Datadog Monitors

# Monitor 1: High Error Rate
name: "TBK Vision - High Error Rate"
type: metric alert
query: "avg:tbk.vision.errors{*} > 5"
threshold: 5
time_window: 5m
notify:
  - slack: "#tbk-pipeline-alerts"
  - pagerduty: "tbk-on-call"

# Monitor 2: Latency SLA
name: "TBK Vision - Latency SLA Breach"
type: metric alert
query: "percentile:tbk.vision.batch.duration{*}:0.99 > 8000"
threshold: 8000
notify:
  - slack: "#tbk-pipeline-alerts"

# Monitor 3: Qwen API Down
name: "TBK Vision - Qwen Unavailable"
type: service check
service: "qwen-gpu-api"
threshold: 2  # 2 failed checks
notify:
  - slack: "#tbk-pipeline-critical"
  - pagerduty: "tbk-on-call"
```

---

## Part 6: Operations Runbook

### Daily Operations

**Morning Checklist** (9 AM):
```bash
# 1. Verify all services healthy
docker-compose ps
# All green ✓

# 2. Check error rate
curl -X GET "https://api.datadoghq.com/api/v1/query?query=avg:tbk.vision.errors{*}" \
  -H "DD-API-KEY: ${DATADOG_API_KEY}" | jq '.results[0].values[]'
# Should be near 0 ✓

# 3. Review logs
# Kibana → Search: "status:failed" 
# Expected: <5 errors in last 24h ✓

# 4. Check queue depth
docker-compose exec postgres psql -U vision_user -d tbk_pipeline -c \
  "SELECT COUNT(*) FROM images WHERE status='queued';"
# Should be <100 ✓
```

### Incident Response

**Scenario 1: Qwen GPU Down**
```bash
# 1. Alert fires (ELK shows qwen errors)
# 2. Acknowledge in Slack: "Working on it"
# 3. Check GPU status
ssh qwen-gpu-1 nvidia-smi
# If GPU not responsive, restart

# 4. Fallback to CLIP enabled automatically (see code)
# Monitor metrics while using fallback
# Notify team in #tbk-pipeline-alerts

# 5. Once GPU restored, rerun failed images
curl -X POST http://n8n:5678/webhook/tbk-rerun-batch \
  -d '{"batch_id": "failed_batch_id"}'

# 6. Verify recovery in Datadog
# Success rate should return to >98%
```

**Scenario 2: Database Connection Error**
```bash
# 1. Check PostgreSQL
docker-compose logs postgres | tail -50

# 2. Restart if needed
docker-compose restart postgres

# 3. Verify reconnection
docker-compose exec postgres pg_isready -U n8n_user

# 4. Check for data consistency
docker-compose exec postgres psql -U vision_user -d tbk_pipeline \
  -c "SELECT COUNT(*) FROM images WHERE status='processing';"
# Should be 0 (nothing stuck in processing)

# 5. Resume batch queue
# Batches with status='processing' → resume
```

**Scenario 3: Shopify API Rate Limited**
```bash
# 1. Alert: "Shopify 429 Too Many Requests"
# 2. n8n automatically retries with exponential backoff
# 3. Check queue
docker-compose exec postgres psql -U vision_user -d tbk_pipeline \
  -c "SELECT COUNT(*) FROM shopify_publishes WHERE status='queued';"

# 4. If queue >100, pause new batches
# POST /admin/pause-ingestion (custom endpoint)

# 5. Monitor Shopify rate limit status
# Shopify API responds with X-Request-Id and backoff time
# Once recovered, resume

# 6. Notify team of delay
curl -X POST ${SLACK_WEBHOOK_URL} \
  -d '{"text": "Shopify rate limited. Backoff 60s. Queue depth: 150"}'
```

---

## Part 7: Scaling & Optimization

### Horizontal Scaling (n8n Workers)

```yaml
# Add worker nodes in docker-compose
services:
  n8n-worker-1:
    image: n8nio/n8n:latest
    command: worker --concurrency 10
    environment:
      N8N_REDIS_HOST: redis
      # ... other env vars
    depends_on:
      - redis
      - postgres

  n8n-worker-2:
    image: n8nio/n8n:latest
    command: worker --concurrency 10
    environment:
      N8N_REDIS_HOST: redis
      # ... other env vars
    depends_on:
      - redis
      - postgres

# Main n8n instance becomes coordinator
n8n:
  # ... config ...
  command: start
```

### Database Query Optimization

```sql
-- Monitor slow queries
SELECT query, calls, mean_time FROM pg_stat_statements 
WHERE mean_time > 100  -- >100ms
ORDER BY mean_time DESC;

-- Add missing indexes
CREATE INDEX idx_pipeline_audits_batch_created 
  ON pipeline_audits(batch_id, created_at DESC);

-- Analyze query plans
EXPLAIN ANALYZE 
SELECT * FROM images WHERE batch_id='xyz' AND status='success';
```

### Caching Strategy (Redis)

```python
# Cache frequently accessed data
# Vision model responses (identical images)
# SEO title suggestions (similar cakes)

# In n8n Function node:
import redis

redis_client = redis.Redis(host='redis', port=6379)
cache_key = f"vision:{image_hash}"
cached = redis_client.get(cache_key)

if cached:
    return json.loads(cached)  # Cache hit (100x faster)
else:
    result = qwen_analyze(image)  # Cache miss
    redis_client.setex(cache_key, 86400*7, json.dumps(result))  # 7-day TTL
    return result
```

---

## Part 8: Backup & Disaster Recovery

### Automated Backups

```bash
# PostgreSQL backup (daily)
#!/bin/bash
BACKUP_DIR="/mnt/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

docker-compose exec -T postgres pg_dump \
  -U n8n_user n8n > ${BACKUP_DIR}/n8n_${DATE}.sql

docker-compose exec -T postgres pg_dump \
  -U vision_user tbk_pipeline > ${BACKUP_DIR}/tbk_pipeline_${DATE}.sql

# Retain 30 days
find ${BACKUP_DIR} -type f -mtime +30 -delete

# Upload to S3
aws s3 cp ${BACKUP_DIR} s3://tbk-backups/postgres/ --recursive
```

### Recovery Procedure

```bash
# Restore PostgreSQL
docker-compose down
docker volume rm n8n-deployment_postgres_data
docker-compose up -d postgres

# Wait for database ready
docker-compose exec postgres pg_isready -U n8n_user

# Restore data
docker-compose exec -T postgres psql -U n8n_user < /mnt/backups/postgres/tbk_pipeline_YYYYMMDD_HHMMSS.sql

# Restart n8n
docker-compose up -d n8n
```

---

## Conclusion

This n8n deployment provides:

✅ **Production-ready** infrastructure (containerized, monitored, backed up)  
✅ **Scalable** architecture (workers, caching, optimization)  
✅ **Observable** (Datadog, ELK, Slack alerts)  
✅ **Resilient** (error handlers, fallbacks, retries)  
✅ **Documented** (runbook, checklists, playbooks)  

**Ready to deploy in Week 1 of Sprint 1.**

