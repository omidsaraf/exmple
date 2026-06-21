# Fabric notebook (source) - GOLD BUILD TEMPLATE (facts / aggregates)  (invert-control, 2026-06-17)
# =============================================================================
#  WHEN TO USE THIS:
#    SCD2 DIMENSIONS are metadata-only - the framework's nb_scd2_processor builds them from
#    meta.* (§29). You do NOT write a notebook for a dim. This template is for GOLD
#    FACTS / AGGREGATES that genuinely need transform code.
#
#  HOW TO USE (Data Engineer): same contract as the silver template - you write ONE
#    build(spark, sources) and nothing else. The framework owns all I/O: source resolution,
#    source-readiness gate, audit columns, **Gold PHI masking (applied automatically - raw PHI
#    can never reach Gold, §7/§28 = P1)**, the empty-source guardrail, the sanctioned write
#    (write_mode + partition/cluster from proc_param), and logging. There is no df.write here.
#
#  NO LIMIT ON LOGIC: full PySpark AND/OR Spark SQL inside build() (register `sources` as temp
#    views and spark.sql(...) - mix freely), exactly like the silver template. SQL-only builds
#    use a transform_spark_sql proc (see silver_transform_sql_TEMPLATE.sql).
#
#  LIBRARIES: runtime-bundled libs just import; anything else is added to the Fabric Environment
#    (infra/fabric-environments/), pinned, via PR - never %pip install (§33).
#
#  CI/CD RULES (dataflows-ci gate): parameters cell FIRST; wheel + Environment imports only (no
#    %run / no %pip); explicit columns (no SELECT *); the entrypoint line stays unchanged.
# =============================================================================
#  Dataflow : <TODO dag_uid e.g. df_audiology_appointments>   Layer: gold
#  Author   : <TODO name>     Date: <TODO>
# =============================================================================

# ===== PARAMETERS CELL =======================================================
proc_id       = 0
proc_run_id   = 0
ctrl_server   = ""
ctrl_database = ""
env           = "pilot"
dag_uid       = ""

# ===== CELL: dependencies (built-in framework wheel) ========================
from healthent_framework.transform import run_transform      # noqa: F401
from pyspark.sql import functions as F, types as T           # noqa: F401


# ===== CELL: build - THE ONLY CODE YOU WRITE ================================
def build(spark, sources):
    """<TODO one-sentence description of the fact/aggregate>.

    `sources` = {view: DataFrame} from your proc_param source_map (read the SILVER tech
    views). Return the Gold DataFrame. Columns flagged mask_at_gold in meta.ingestion_column
    are masked by the framework after this returns - but you should also AGGREGATE PHI out
    where the grain allows (age-banding, clinic-level rollups), since masking is the floor,
    not the goal. Never write here - the framework writes (write_mode from proc_param)."""
    fact = sources["<TODO silver tech view>"]
    return fact.select(
        # <TODO explicit columns - aggregated/dimension keys; PHI masked or aggregated out>
    )


# ===== CELL: entrypoint (framework owns I/O - DO NOT CHANGE) ================
if notebookutils is not None:  # noqa: F821
    run_transform(build, globals())
else:
    print("gold build template loaded offline - build() defined, not executed.")
