# Fabric notebook (source) - df_audiology_appointments / silver clinic  (HEARING_P1)
# =============================================================================
#  WORKED EXAMPLE 1 of 3 - the clinic reference table's silver conform. Same invert-control
#  contract: the DE writes build() only; the framework owns all I/O (sources, audit columns,
#  Gold masking, the sanctioned write, SCD2 invariant, logging). No df.write / path here.
#  Transform: Bronze clinic -> Silver conformed clinic (dedupe by clinic_id, trim/type).
#  Pairs with SlvrAudiologyAppointmentsHearingP1 (which fans in this table's name).
# =============================================================================

# ===== PARAMETERS CELL =======================================================
proc_id       = 0
proc_run_id   = 0
ctrl_server   = ""
ctrl_database = ""
env           = "pilot"
dag_uid       = "df_audiology_appointments"

# ===== CELL: dependencies (built-in framework wheel - the only import) =======
from healthent_framework.transform import run_transform      # noqa: F401
from pyspark.sql import functions as F, types as T           # noqa: F401
from pyspark.sql.window import Window                         # noqa: F401


# ===== CELL: transform - THE ONLY CODE THE DE WRITES ========================
def build(spark, sources):
    """Bronze clinic -> Silver conformed clinic (dedupe + trim + type).

    `sources` = {"clinic_bronze": DataFrame} resolved by the framework from proc_param
    source_map. Return the conformed DataFrame; the framework writes it (write_mode=merge)."""
    src = sources["clinic_bronze"]

    # latest version per business key (Bronze is append-only, §15.6)
    w = Window.partitionBy("clinic_id").orderBy(F.col("_ingested_at_utc").desc())
    latest = (src.withColumn("_rn", F.row_number().over(w))
                 .filter(F.col("_rn") == 1).drop("_rn"))

    return (latest
        .filter(F.col("clinic_id").isNotNull())
        .select(
            F.col("clinic_id").cast(T.IntegerType()).alias("clinic_id"),
            F.trim(F.col("clinic_name")).cast(T.StringType()).alias("clinic_name"),
            F.trim(F.col("region")).cast(T.StringType()).alias("region"),
            F.col("_ingested_at_utc"))
        .withColumn("_conformed_at_utc", F.current_timestamp()))


# ===== CELL: entrypoint (framework owns I/O - DO NOT CHANGE) ================
if notebookutils is not None:  # noqa: F821
    run_transform(build, globals())
else:
    print("SlvrAudiologyClinicHearingP1 loaded offline - build() defined, not executed.")
