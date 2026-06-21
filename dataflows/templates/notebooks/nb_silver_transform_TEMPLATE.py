# Fabric notebook (source) - SILVER TRANSFORM TEMPLATE  (invert-control contract, 2026-06-17)
# =============================================================================
#  HOW TO USE (Data Engineer):
#    1. Copy to  silver/Notebook/{PROJECT_CODE}/{notebook_name}.py  (the scaffolder does this).
#    2. Write ONE function: build(spark, sources) -> DataFrame. That is the ONLY code you write.
#    3. Delete the <TODO>s. Add your flow's proc_param rows in the metadata PR (manifest.yml).
#
#  WHAT YOU CAN DO INSIDE build() - NO LIMIT ON LOGIC:
#    - Full PySpark: DataFrame API, joins, window functions, pandas/vectorised UDFs, ML, etc.
#    - Full Spark SQL: register the framework-resolved `sources` as temp views and run any
#      spark.sql(...) you like (CTEs, multi-step) - you can MIX PySpark and Spark SQL freely
#      (see the two cells below). This is the same heavy pyspark+SQL style as the UDP example.
#    - If you prefer SQL-ONLY (no notebook), use a `transform_spark_sql` proc instead and put
#      your SQL in a proc_param `sql_inline` or a .sql file - the framework runs it for you
#      (see templates/notebooks/silver_transform_sql_TEMPLATE.sql). Same guardrails either way.
#
#  WHAT THE FRAMEWORK OWNS (you cannot bypass a guardrail) - the `healthent_framework` wheel,
#  attached via env-healthent-framework, does EVERY side effect:
#    - source resolution from your proc_param `source_map` (logical refs, ADR-36 - never an abfss)
#    - source-readiness + freshness gate (won't run on a failed/stale source - ADR-48)
#    - the standard AUDIT/lineage columns (_run_id, _source_code, _written/_updated)
#    - Gold PHI masking (unconditional when target_layer='gold')
#    - the empty-source guardrail (an empty read never wipes a target)
#    - the sanctioned Delta write chosen by `write_mode` (append|overwrite|merge|scd2), with the
#      metadata-driven layout (partition_by / cluster_by) and the SCD2 invariant
#    - run logging. There is intentionally NO df.write, no path building, no masking call here.
#
#  LIBRARIES (read this):
#    - Runtime-bundled libs (pyspark, delta, pandas, numpy, pyarrow) - just import them.
#    - ANYTHING ELSE (e.g. fhir-resources, hl7apy, scikit-learn, a parser) must be added to the
#      Fabric Environment (infra/fabric-environments/env-healthent-{scope}.yml), pinned exact
#      version, via PR (§33). DO NOT %pip install in a cell - it breaks reproducibility and the
#      env pin, and the dataflows-ci gate fails the PR.
#
#  CI/CD RULES (the dataflows-ci gate enforces these - a PR fails otherwise):
#    - Parameters cell stays the FIRST code cell; typed literals only (no None) - W7.
#    - Wheel imports + Environment libs ONLY. Never %run. Never %pip install (§33).
#    - Explicit output columns - never SELECT * (§5/§6).
#    - The entrypoint line `run_transform(build, globals())` must be present and unchanged.
# =============================================================================
#  Dataflow   : <TODO dag_uid e.g. df_audiology_appointments>   Layer: silver
#  Author     : <TODO name>     Date: <TODO>
# =============================================================================

# ===== PARAMETERS CELL =======================================================
# Supplied by the framework at run time (the runner passes them). Leave as typed literals.
proc_id       = 0
proc_run_id   = 0
ctrl_server   = ""
ctrl_database = ""
env           = "pilot"
dag_uid       = ""        # for run-event logging only

# ===== CELL: dependencies ====================================================
# The built-in framework wheel is the only REQUIRED import. Add Environment-provided libraries
# here too (e.g. `import hl7apy`) - never %pip install (they come from env-healthent-{scope}, §33).
from healthent_framework.transform import run_transform      # noqa: F401
from pyspark.sql import functions as F, types as T           # noqa: F401
from pyspark.sql.window import Window                         # noqa: F401


# ===== CELL: transform - THE ONLY CODE YOU WRITE =============================
def build(spark, sources):
    """<TODO one-sentence description of the conformed Silver output>.

    `sources` = {view_name: DataFrame} resolved by the framework from your proc_param
    `source_map` (a silver build may read SEVERAL bronze tables - fan-in). Return the
    conformed DataFrame. Do NOT write it - the framework writes it using the `write_mode`
    you set in proc_param (merge is the silver default).

    HEAVY/PARAMETRIC transform? Use the 3-arg form `def build(spark, sources, params):` - the
    framework passes your proc_param dict as `params` (the UDP self.metadata equivalent), so you
    can read run_date, thresholds, source_code, etc. The 2-arg form below is the common case.

    MULTIPLE TARGETS from one build (UDP split-flow: IDEN / UNIDEN / EXCEPTION)? Return a dict
    `{"target_table_a": df_a, "target_table_b": df_b, ...}` instead of one DataFrame - the framework
    computes your shared upstream ONCE and writes each target with its own write_mode/keys/layout
    from the proc_param `targets` map (falls back to the proc default). One read/compute, N writes.

    You may use PySpark, Spark SQL, or BOTH. Two equivalent styles:
    """
    # ---- style A: PySpark (delete if you use SQL) --------------------------
    src = sources["<TODO view_name e.g. appointment_bronze>"]
    keys = ["<TODO business key column>"]
    w = Window.partitionBy(*keys).orderBy(F.col("_ingested_at_utc").desc())
    latest = src.withColumn("_rn", F.row_number().over(w)).filter(F.col("_rn") == 1).drop("_rn")
    out = latest.select(
        # <TODO: F.col("...").cast(T....Type()).alias("..."), ... - explicit, no SELECT *>
    )

    # ---- style B: Spark SQL over the same sources (delete if you use PySpark) ----
    # Register each framework-resolved source as a temp view, then write any Spark SQL.
    # for name, df in sources.items():
    #     df.createOrReplaceTempView(name)
    # out = spark.sql(\"\"\"
    #     SELECT a.<col1>, a.<col2>, b.<col3>          -- explicit columns, never SELECT *
    #     FROM   <appointment_bronze> a
    #     LEFT   JOIN <clinic_bronze> b ON a.clinic_id = b.clinic_id
    #     QUALIFY ROW_NUMBER() OVER (PARTITION BY a.<key> ORDER BY a._ingested_at_utc DESC) = 1
    # \"\"\")

    return out


# ===== CELL: entrypoint (framework owns I/O - DO NOT CHANGE) ================
if notebookutils is not None:  # noqa: F821  (runtime-injected; conftest injects None offline)
    run_transform(build, globals())
else:
    print("silver transform template loaded offline - build() defined, not executed.")
