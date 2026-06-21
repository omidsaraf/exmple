# Fabric notebook (source) - df_dynamics_contact / silver  (HEARING_P2, invert-control contract)
# =============================================================================
#  WORKED EXAMPLE 2 of 3 (CRM 365 / Dataverse table source) - same shape as
#  templates/notebooks/nb_silver_transform_TEMPLATE.py.
#  The DE writes build() ONLY. The framework (healthent_framework wheel, run_transform) owns ALL I/O:
#  source resolution, audit columns, Gold masking, the sanctioned Delta write (write_mode from
#  proc_param), the SCD2 invariant, and logging. There is no df.write / path / writer here, by design.
#  Transform: Bronze Dataverse `contact` -> Silver conformed contact
#    1. latest version per contactid (bronze is append-only, §15.6)
#    2. conform + rename Dataverse columns to the business model
#       (firstname+lastname -> full_name, emailaddress1 -> email, telephone1|mobilephone -> phone,
#        birthdate -> birth_date, address1_postalcode -> postcode, gendercode -> gender_code)
#    3. typed, explicit column list; null-guard on the business key.
#  Every identifiable column flows through to the Gold dim where it is masked (two-view split).
# =============================================================================

# ===== PARAMETERS CELL =======================================================
proc_id       = 0
proc_run_id   = 0
ctrl_server   = ""
ctrl_database = ""
env           = "pilot"
dag_uid       = "df_dynamics_contact"

# ===== CELL: dependencies (built-in framework wheel - the only import) =======
from healthent_framework.transform import run_transform      # noqa: F401
from pyspark.sql import functions as F, types as T           # noqa: F401
from pyspark.sql.window import Window                         # noqa: F401


# ===== CELL: transform - THE ONLY CODE THE DE WRITES ========================
def build(spark, sources):
    """Bronze Dataverse contact -> Silver conformed contact (dedupe + rename + type).

    `sources` = {view: DataFrame} resolved by the framework from proc_param source_map
    (e.g. {"contact_bronze": "dynamics/bronze/main:dynamics/contact"}).
    Return the conformed DataFrame; the framework writes it (write_mode=merge from proc_param)."""
    src = sources["contact_bronze"]

    # 1) latest version per business key (Bronze is append-only, §15.6)
    w = Window.partitionBy("contactid").orderBy(F.col("_ingested_at_utc").desc())
    latest = (src.withColumn("_rn", F.row_number().over(w))
                 .filter(F.col("_rn") == 1).drop("_rn"))

    # 2) conform + rename; prefer assembled name, fall back to Dataverse fullname
    assembled = F.trim(F.concat_ws(" ", F.col("firstname"), F.col("lastname")))
    full_name = F.coalesce(F.when(assembled != "", assembled), F.col("fullname"))

    # 3) explicit, typed output columns - never SELECT * (§5)
    return (latest
        .filter(F.col("contactid").isNotNull())
        .select(
            F.col("contactid").cast(T.StringType()).alias("contactid"),
            full_name.cast(T.StringType()).alias("full_name"),
            F.lower(F.trim(F.col("emailaddress1"))).cast(T.StringType()).alias("email"),
            F.coalesce(F.col("telephone1"), F.col("mobilephone")).cast(T.StringType()).alias("phone"),
            F.col("birthdate").cast(T.DateType()).alias("birth_date"),
            F.trim(F.col("address1_postalcode")).cast(T.StringType()).alias("postcode"),
            F.col("gendercode").cast(T.IntegerType()).alias("gender_code"),
            F.col("_ingested_at_utc"))
        .withColumn("_conformed_at_utc", F.current_timestamp()))


# ===== CELL: entrypoint (framework owns I/O - DO NOT CHANGE) ================
if notebookutils is not None:  # noqa: F821
    run_transform(build, globals())
else:
    print("SlvrDynamicsContactHearingP2 loaded offline - build() defined, not executed.")
