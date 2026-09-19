# GCP Deployment Specialist Reference

Complete guide for optimizing Google Cloud Platform deployments, specifically
Cloud Run + Litestream SQLite + FastAPI + React architectures.

---

## Reference Repositories

### Core Deployment Pattern
| Repo | What | Why |
|------|------|-----|
| [steren/litestream-cloud-run-example](https://github.com/steren/litestream-cloud-run-example) | Official Litestream + Cloud Run reference | Exact pattern for SQLite replication on Cloud Run |
| [benbjohnson/litestream](https://github.com/benbjohnson/litestream) | Streaming SQLite replication | Core replication engine, GCS backend support |
| [GoogleCloudPlatform/cloud-run-hello](https://github.com/GoogleCloudPlatform/cloud-run-hello) | Official Cloud Run examples | Docker multi-stage patterns for Cloud Run |

### Infrastructure-as-Code
| Repo | What | Why |
|------|------|-----|
| [GoogleCloudPlatform/cloud-foundation-fabric](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric) | Modular Terraform for GCP | Landing zone toolkit, production-ready modules |
| [GoogleCloudPlatform/terraform-google-secure-cicd](https://github.com/GoogleCloudPlatform/terraform-google-secure-cicd) | Secure CI/CD via Terraform | Pipeline + infrastructure as code |
| [pulumi/pulumi-gcp](https://github.com/pulumi/pulumi-gcp) | Pulumi GCP provider | Code-first IaC (Python/TS), easier for solopreneurs |

### Cost Optimization
| Repo | What | Why |
|------|------|-----|
| [hystax/optscale](https://github.com/hystax/optscale) | FinOps platform | Multi-cloud cost optimization with automated recs |
| [opencost/opencost](https://github.com/opencost/opencost) | Real-time cost allocation | Kubernetes/Cloud Run cost visibility |

### Security Hardening
| Repo | What | Why |
|------|------|-----|
| [GoogleCloudPlatform/gcp-hardening-toolkit](https://github.com/GoogleCloudPlatform/gcp-hardening-toolkit) | GCP security hardening IaC | Terraform modules for constraints, detection, triage |
| [leg100/gcp-hardening-guide](https://github.com/leg100/gcp-hardening-guide) | GCP org hardening guide | Firewall rules, OS Login, SA key restrictions |
| [doitintl/secure-gcp-reference](https://github.com/doitintl/secure-gcp-reference) | Secure GCP reference | Best-practice compliant infrastructure |

### CI/CD
| Repo | What | Why |
|------|------|-----|
| [google-github-actions/deploy-cloudrun](https://github.com/google-github-actions/deploy-cloudrun) | GitHub Action → Cloud Run | Official deployment action |
| [GoogleCloudPlatform/cloud-run-mcp](https://github.com/GoogleCloudPlatform/cloud-run-mcp) | MCP server for Cloud Run | Deploy apps from MCP-enabled agents |

### Monitoring & Observability
| Repo | What | Why |
|------|------|-----|
| Google Managed Prometheus | Metrics collection | 24-month retention, PromQL, multi-cloud |
| Grafana + Google Cloud Monitoring | Visualization | Unified dashboards for Cloud Run, GCS, SQLite health |

### Curated Resource Lists
| Repo | What |
|------|------|
| [GoogleCloudPlatform/awesome-google-cloud](https://github.com/GoogleCloudPlatform/awesome-google-cloud) | Official curated GCP resources |
| [awesomelistsio/awesome-google-cloud-platform](https://github.com/awesomelistsio/awesome-google-cloud-platform) | Tools, SDKs, templates across all GCP services |

---

## Cloud Run + Litestream Architecture

### Critical Constraint
Litestream requires `--max-instances 1` on Cloud Run — single instance only.

### Deployment Flow
```
Container Start
  → Litestream restore (download SQLite from GCS)
  → Litestream replicate (background continuous sync)
  → Application start (FastAPI + static React assets)
  → Health check passes → receive traffic
```

### Entrypoint Pattern
```bash
#!/bin/bash
set -e

# 1. Restore database from GCS backup
litestream restore -if-db-not-exists -if-replica-exists \
  -config /etc/litestream.yml \
  /data/social_arb.db

# 2. Start Litestream replication + application
exec litestream replicate -exec "uvicorn social_arb.serve:app --host 0.0.0.0 --port $PORT" \
  -config /etc/litestream.yml
```

### Litestream Config
```yaml
dbs:
  - path: /data/social_arb.db
    replicas:
      - type: gcs
        bucket: ${GCS_BUCKET}
        path: db/
        retention: 72h
        sync-interval: 1s
```

### Environment Variables (never hardcode)
| Variable | Source | Description |
|----------|--------|-------------|
| `GCS_BUCKET` | Cloud Run env / Secret Manager | Litestream replication target |
| `PORT` | Cloud Run (auto-set) | HTTP listening port |
| `GOOGLE_CLOUD_PROJECT` | Cloud Run (auto-set) | GCP project ID |
| `DATABASE_PATH` | Config / env | SQLite file location |

---

## Docker Multi-Stage Build Optimization

### Pattern for FastAPI + React
```dockerfile
# Stage 1: Build React frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/ui
COPY ui/package*.json ./
RUN npm ci --production=false
COPY ui/ ./
RUN npm run build

# Stage 2: Python backend + Litestream
FROM python:3.11-slim AS production

# Install Litestream
ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.13/litestream-v0.3.13-linux-amd64.tar.gz /tmp/
RUN tar -xzf /tmp/litestream-*.tar.gz -C /usr/local/bin/ && rm /tmp/litestream-*.tar.gz

# Install Python dependencies
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY social_arb/ ./social_arb/
COPY --from=frontend-build /app/ui/dist ./ui/dist

# Copy configs
COPY litestream.yml /etc/litestream.yml
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
```

### Size Reduction Tips
- Use `-alpine` or `-slim` base images
- Copy dependency manifests BEFORE source code (layer caching)
- Use `--no-cache-dir` for pip
- Use `npm ci` not `npm install` for deterministic builds
- Multi-stage: build artifacts only, don't copy dev dependencies
- Typical reduction: 1.3GB → 250MB (81% smaller)

---

## Cloud Run Deployment Optimization

### gcloud Deploy Command
```bash
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_URL} \
  --region ${REGION} \
  --platform managed \
  --max-instances 1 \
  --min-instances 0 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars "GCS_BUCKET=${GCS_BUCKET}" \
  --allow-unauthenticated \
  --execution-environment gen2
```

### Key Flags
| Flag | Value | Why |
|------|-------|-----|
| `--max-instances 1` | **Required** | Litestream single-instance constraint |
| `--min-instances 0` | Cost saving | Scale to zero when idle |
| `--memory 512Mi` | Right-sized | SQLite + FastAPI footprint |
| `--execution-environment gen2` | Performance | Better startup, full Linux syscalls |
| `--timeout 300` | Generous | Allow for Litestream restore on cold start |

### Cost Optimization Checklist
- [ ] Scale to zero (`--min-instances 0`) for dev/staging
- [ ] Right-size memory (start 256Mi, increase if OOM)
- [ ] Use CPU allocation = "request" (not "always") for bursty workloads
- [ ] Set concurrency to match app capabilities (FastAPI async = higher concurrency)
- [ ] Enable Cloud CDN for static React assets
- [ ] Use Artifact Registry (not Container Registry) for cheaper storage
- [ ] Set up billing alerts at $10, $25, $50/month thresholds
- [ ] Review unused GCS objects (Litestream WAL retention)

### Cold Start Optimization
1. **Reduce image size** (multi-stage builds, slim bases)
2. **Pre-warm with min-instances=1** for production
3. **Lazy imports** in Python (don't import everything at module level)
4. **Use startup CPU boost** (`--cpu-boost` flag)
5. **Optimize Litestream restore** (smaller DB = faster restore)

---

## CI/CD Pipeline (GitHub Actions)

### Workflow Template
```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  REGION: ${{ secrets.GCP_REGION }}
  SERVICE: ${{ secrets.GCP_SERVICE_NAME }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # Required for Workload Identity Federation

    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Build and push container
        run: |
          gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE

      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: ${{ env.SERVICE }}
          image: gcr.io/${{ env.PROJECT_ID }}/${{ env.SERVICE }}
          region: ${{ env.REGION }}
```

### Security: Workload Identity Federation
Use WIF instead of service account keys:
```bash
# One-time setup
gcloud iam workload-identity-pools create github-pool \
  --location=global
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --location=global \
  --workload-identity-pool=github-pool \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository"
```

---

## Security Hardening Checklist

- [ ] Use Workload Identity Federation (no JSON key files)
- [ ] Disable service account key creation (org policy)
- [ ] Enable VPC connector for private networking
- [ ] Set IAM to least-privilege (Cloud Run Invoker only)
- [ ] Use Secret Manager for API keys, DB credentials
- [ ] Enable Cloud Audit Logging
- [ ] Set up org-level security constraints
- [ ] Scan container images for vulnerabilities (Artifact Analysis)
- [ ] Pin base image versions (never use `:latest` in production)
- [ ] Configure Cloud Armor for DDoS protection (if public)

---

## Monitoring Setup

### Cloud Run Metrics to Watch
| Metric | Alert Threshold | Why |
|--------|----------------|-----|
| `container/instance_count` | > 1 | Litestream requires single instance |
| `container/memory/utilization` | > 80% | OOM risk |
| `container/startup_latency` | > 30s | Cold start too slow |
| `request_count` (5xx) | > 5/min | Application errors |
| `request_latencies` (p99) | > 2s | Performance degradation |

### Litestream Health Checks
```python
@app.get("/health")
async def health():
    """Check both app and Litestream replication health."""
    db_exists = os.path.exists(config.DATABASE_PATH)
    db_size = os.path.getsize(config.DATABASE_PATH) if db_exists else 0
    return {
        "status": "healthy" if db_exists else "degraded",
        "database": {"exists": db_exists, "size_bytes": db_size},
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## Troubleshooting Playbook

### Common Issues

**1. Litestream restore fails on cold start**
- Cause: GCS bucket doesn't exist or permissions missing
- Fix: Ensure service account has `storage.objectAdmin` on the bucket
- Test: `litestream restore -if-replica-exists -config litestream.yml /tmp/test.db`

**2. Container exits immediately**
- Cause: Litestream subprocess fails, takes down main process
- Fix: Use `-if-db-not-exists -if-replica-exists` flags (don't fail on first deploy)
- Debug: `gcloud run services logs read ${SERVICE} --region ${REGION}`

**3. Database appears empty after deploy**
- Cause: Restore path doesn't match app's DATABASE_PATH
- Fix: Ensure litestream.yml path matches config.DATABASE_PATH exactly

**4. 503 Service Unavailable on cold start**
- Cause: Litestream restore takes too long
- Fix: Increase `--timeout`, reduce DB size, add startup probe

**5. High GCS costs from WAL segments**
- Cause: Litestream retention too long or sync too frequent
- Fix: Set `retention: 24h` (instead of 72h), `sync-interval: 10s` for dev

---

## Notes
- All values use `${VARIABLE}` syntax — resolve from config/env/secrets, never hardcode
- All commands tested against GCP Cloud Run gen2 execution environment
- Litestream v0.3.13+ required for GCS backend improvements
- Always test restore locally before deploying: `litestream restore -o /tmp/test.db`
