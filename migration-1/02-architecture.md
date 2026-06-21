# 02 - Architecture

Target platform, the medallion + serving design, the default ingestion path and its only exceptions, the source
families, and the naming standard. Every rule here is closed (one right way).

## 1. Platform stack
- **Compute:** Fabric Lakehouse (PySpark notebooks) for all transformation; Fabric Data Pipelines for orchestration.
- **Store:** OneLake (Delta). Bronze raw may be Parquet/CSV; Silver/Gold are Delta.
- **Serving:** the lakehouse's built-in **SQL analytics endpoint** (views) + **Direct Lake** for Power BI.
- **Control plane:** Azure SQL Database (meta.*/log.*).
- **Runtime:** Fabric Runtime 1.3 (Spark 3.5 / Py 3.11 / Delta 3.2). Libraries via Fabric Environments, never inline pip.
- **Governance:** Microsoft Purview. **IaC:** Terraform (microsoft/fabric + azurerm/azapi; capacity via azapi).

## 2. Medallion + serving (ADR: serving)
- **Lakehouse per layer** (lh_bronze / lh_silver / lh_gold / lh_archive). Schema carries meaning, not the domain:
  bronze schema = source system; silver schema = subject area; gold schema = business domain.
- **Tables live in the lakehouse** (managed Delta, created by the Spark writer). **Serving VIEWS live in the
  lakehouse's SQL analytics endpoint** (same DB, zero copy) - **no separate Warehouse item**. A Warehouse is the
  *exception only*, for writable T-SQL over OneLake shortcuts (rare).
- **Two views per served table**, exact table name (no `v_` prefix), in separate schemas (enables clean
  schema-level grants; the base table schema is never granted to consumers):
  - `[domain]_TECH_VIEW.[table]` - full columns; engineers/analysts + pipeline SP (PIM/JIT for prod PHI).
  - `[domain]_VIEW.[table]` - consumption; **PHI columns OMITTED (CLS by omission)** - the read-only lakehouse
    SQL endpoint has no DDM, and omission is the strongest CLS anyway.
- **Two BI paths over one Gold copy:** (a) certified dashboards = **Direct Lake over the Gold tables** + RLS/OLS
  in the semantic model (fastest, no refresh); (b) ad-hoc SQL/extracts = the views above. Security is always at
  the data/model layer, never the dashboard.
- **Conformed dimensions (dim_date, public_holiday) are GENERATED/seeded**, not ingested: `date_key = yyyymmdd`,
  no SCD2, AU financial year (Jul-Jun) + holidays as a seed table, idempotent overwrite, one shared copy.

## 3. The default ingestion path + the ONLY exceptions (closed rule)
**Default (use unless a row below applies):**
```
ORIGINAL/external source -> Bronze -> Silver -> Gold -> semantic model -> dashboard
        (framework: watermark · drift · reconciliation · SCD2 · DQ · lineage · RLS/CLS)
```
Source = the **origin system** (not Synapse). Onboarding = a manifest (config). Every layer earns its place via
the framework's guarantees. This scales with data volume, not source count (pipeline count stays flat).

**Exceptions (each per-object, documented, recon-gated, never the default):**
| # | Use case | Instead |
|---|---|---|
| 1 | One-time historical/archival backfill from Synapse | read Synapse bronze from STORAGE -> Delta -> recon -> archive (ADR-39; 07) |
| 2 | Cold archival (retain-only) | straight to `lh_archive` after recon, no Silver/Gold |
| 3 | Cross-domain sharing (no copy) | OneLake shortcut into a shared lakehouse |
| 4 | External non-Delta served without owning it | Warehouse `OPENROWSET` views over a shortcut |
| 5 | Real-time / IoT | Eventstream -> Eventhouse + Bronze (not batch) |
| 6 | Dataverse zero-copy (if chosen over Copy) | Link to Fabric |
| 7 | Reference/generated data (no source) | generate/seed (dim_date, public_holiday) |

## 4. Source families (one generic runner each)
| Family | Mechanism | Auth | Watermark | Load types | Key caveats |
|---|---|---|---|---|---|
| SQL table (incl. Synapse) | notebook (Spark JDBC); Copy only if forced/bulk | SP/MI via KV | typed col (datetime2(3)/bigint) | append · incremental_watermark · snapshot_archive | half-open (lower,upper]; epoch 1900-01-01 |
| Dataverse / D365 | Copy (Dataverse connector) or Link-to-Fabric | SP secret in KV | modifiedon | incremental_watermark | 100K rows/req ($skiptoken); rate cap |
| F&O OData | Copy (OData connector) | SP secret | entity field | incremental_watermark | OData paging |
| File landing | notebook (Spark read -> Delta) | storage key/SAS/SP | manifest/EOT control file | append · snapshot_archive | manifest/EOT gate + quarantine; CSV/Parquet -> Delta on write |
| REST/API | notebook (paged) | token/OAuth via KV | API cursor | incremental_watermark | pagination + rate limits |
| Object store (S3/GCS) | shortcut or Copy -> notebook | connection | manifest | full · append | egress cost; shortcut = read-through |
| Streaming/IoT | Eventstream -> Eventhouse + Bronze | event auth | n/a | streaming | AU-region Event Hubs |

## 5. Naming standard (closed)
| Asset | Pattern | Example |
|---|---|---|
| Workspace | healthent-{domain}-{env} | healthent-clinical-prod |
| Lakehouse | lh_{layer} | lh_gold |
| Control SQL DB | sqldb-healthent-control-{env} | sqldb-healthent-control-prod |
| Pipeline | pl_{source}_{target}_{pattern} | pl_d365_bronze_full |
| Notebook | nb_{layer}_{subject}_{pattern} | nb_silver_patient_incremental |
| Gold table | [domain]_[fact|dim|bridge]_[entity] | hr_dim_employee |
| Gold view schemas | [domain]_VIEW / [domain]_TECH_VIEW | clinical_view / clinical_tech_view |
| Entra group | sg-healthent-{domain}-{role} | sg-healthent-clinical-eng |
| Service principal | sp-healthent-{purpose}-{env} | sp-healthent-fabric-prod |
| Key Vault | kv-healthent-{domain}-{env} | kv-healthent-clinical-prod |
| Dataflow project | HEARING_P{n} or a delivery-system id (stable external key) | HEARING_P1 |
| dag_uid | df_{domain}_{entity} | df_audiology_appointments |
| ADR | ADR-{nn}-{short-title} | ADR-22-control-plane-azure-sql |

House style: no em dashes, no smart quotes, no ambiguity; conventions are closed rules, IDs are issued by a
mechanism (never picked by hand).
