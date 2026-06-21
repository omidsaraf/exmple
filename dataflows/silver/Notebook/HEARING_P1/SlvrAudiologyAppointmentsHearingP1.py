# Fabric notebook (source) - df_audiology_appointments / silver  (HEARING_P1, invert-control contract)
# =============================================================================
#  WORKED EXAMPLE 1 of 3 (table source) - identical in shape to
#  templates/notebooks/nb_silver_transform_TEMPLATE.py.
#  The DE writes build() ONLY. The framework (healthent_framework wheel, run_transform) owns ALL I/O:
#  source resolution, audit columns, Gold masking, the sanctioned Delta write (write_mode from
#  proc_param), the SCD2 invariant, and logging. There is no df.write / path / writer here, by design.
#  Transform: Bronze appointment -> Silver conformed appointment
#    1. latest version per appointment_id (bronze is append-only, §15.6)
#    2. standardise appointment_status (trim/lower, controlled vocabulary)
#    3. typed, explicit column list; null-guard on the business key
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

VALID_STATUSES = ["booked", "completed", "cancelled", "no_show", "rescheduled"]


# ===== CELL: transform - THE ONLY CODE THE DE WRITES ========================
def build(spark, sources):
    """Bronze appointment + clinic -> Silver conformed appointment (dedupe + standardise +
    denormalise clinic_name + type). Demonstrates silver FAN-IN: this build reads TWO bronze
    tables (the appointment fact and the clinic reference) declared in the proc_param source_map.

    `sources` = {view: DataFrame} resolved by the framework from proc_param source_map, e.g.
    {"appointment_bronze": "audiology/bronze/main:audiology/appointment",
     "clinic_bronze":      "audiology/bronze/main:audiology/clinic"}.
    Return the conformed DataFrame; the framework writes it (write_mode=merge from proc_param)."""
    appt = sources["appointment_bronze"]
    clinic = sources["clinic_bronze"]

    # 1) latest version per business key on each source (Bronze is append-only, §15.6)
    w_a = Window.partitionBy("appointment_id").orderBy(F.col("_ingested_at_utc").desc())
    latest_appt = (appt.withColumn("_rn", F.row_number().over(w_a))
                       .filter(F.col("_rn") == 1).drop("_rn"))
    w_c = Window.partitionBy("clinic_id").orderBy(F.col("_ingested_at_utc").desc())
    latest_clinic = (clinic.withColumn("_rn", F.row_number().over(w_c))
                           .filter(F.col("_rn") == 1).drop("_rn")
                           .select("clinic_id", "clinic_name"))

    # 2) fan-in: denormalise the clinic name onto each appointment (left join keeps orphans)
    joined = latest_appt.join(F.broadcast(latest_clinic), on="clinic_id", how="left")

    # 3) conform: explicit, typed columns; standardise status (§5/§6)
    return (joined
        .filter(F.col("appointment_id").isNotNull())
        .select(
            F.col("appointment_id").cast(T.LongType()).alias("appointment_id"),
            F.col("patient_id").cast(T.LongType()).alias("patient_id"),
            F.col("clinic_id").cast(T.IntegerType()).alias("clinic_id"),
            F.col("clinic_name").cast(T.StringType()).alias("clinic_name"),
            F.col("appointment_ts").cast(T.TimestampType()).alias("appointment_ts"),
            F.when(F.lower(F.trim(F.col("appointment_status"))).isin(VALID_STATUSES),
                   F.lower(F.trim(F.col("appointment_status"))))
             .otherwise(F.lit("unknown")).alias("appointment_status"),
            F.col("duration_minutes").cast(T.IntegerType()).alias("duration_minutes"),
            F.col("_ingested_at_utc"))
        .withColumn("_conformed_at_utc", F.current_timestamp()))


# ===== CELL: entrypoint (framework owns I/O - DO NOT CHANGE) ================
if notebookutils is not None:  # noqa: F821
    run_transform(build, globals())
else:
    print("SlvrAudiologyAppointmentsHearingP1 loaded offline - build() defined, not executed.")
