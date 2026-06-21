# gen_dim_date_TEMPLATE.py - generate the conformed Gold dim_date (Fabric notebook body / PySpark).
# dim_date is GENERATED, not ingested (no source). Conformed + shared across all domains/facts.
# Idempotent overwrite - safe to re-run; re-run yearly to EXTEND end_date. No PHI, no SCD2, no RLS.
# See docs/architecture/gold-dim-date-and-conformed-dimensions.md. AU: financial year = Jul 1 -> Jun 30.
#
# Parameters cell (toggle as "Parameters" in Fabric; overridden at call time):
start_date = "2015-01-01"
end_date   = "2035-12-31"
gold_root  = "abfss://<ws>@onelake.dfs.fabric.microsoft.com/<lh_gold>.Lakehouse/Tables"  # resolved by the framework
target_schema = "shared"          # conformed schema (ADR-49), NOT a business-domain schema
target_table  = "dim_date"

from pyspark.sql import functions as F

days = F.datediff(F.to_date(F.lit(end_date)), F.to_date(F.lit(start_date)))
df = (spark.range(0, spark.sql(f"SELECT datediff('{end_date}','{start_date}') + 1 AS n").first()["n"])
      .withColumn("date", F.expr(f"date_add(to_date('{start_date}'), cast(id as int))"))
      .drop("id"))

df = (df
    .withColumn("year",        F.year("date"))
    .withColumn("quarter",     F.quarter("date"))
    .withColumn("month",       F.month("date"))
    .withColumn("month_name",  F.date_format("date", "MMMM"))
    .withColumn("month_short", F.date_format("date", "MMM"))
    .withColumn("day",         F.dayofmonth("date"))
    .withColumn("day_of_week", F.expr("((dayofweek(date) + 5) % 7) + 1"))   # Mon=1..Sun=7 (ISO)
    .withColumn("day_name",    F.date_format("date", "EEEE"))
    .withColumn("day_short",   F.date_format("date", "EEE"))
    .withColumn("week_of_year", F.weekofyear("date"))
    .withColumn("day_of_year",  F.dayofyear("date"))
    .withColumn("is_weekend",   F.expr("dayofweek(date) in (1,7)"))         # Sun=1, Sat=7 in Spark
    .withColumn("is_last_day_of_month", F.expr("date = last_day(date)"))
    .withColumn("date_key",     F.expr("year(date)*10000 + month(date)*100 + dayofmonth(date)"))
    # Australian financial year: Jul 1 -> Jun 30
    .withColumn("fin_year",     F.expr("year(date) + cast(month(date) >= 7 as int)"))
    .withColumn("fin_month_no", F.expr("((month(date) + 5) % 12) + 1"))     # Jul=1 .. Jun=12
    .withColumn("fin_quarter",  F.expr("cast(floor((((month(date)+5)%12))/3) as int) + 1")))

# Public holidays = a left join to the seeded shared.public_holiday table (national + relevant states).
# Keep holidays as data, not code, so the generator stays pure. If the table is absent, default to non-holiday.
try:
    hol = spark.read.format("delta").load(f"{gold_root}/{target_schema}/public_holiday").select(
        F.col("date").alias("hdate"), F.col("holiday_name"))
    df = (df.join(hol, df["date"] == hol["hdate"], "left").drop("hdate")
            .withColumn("is_public_holiday", F.col("holiday_name").isNotNull()))
except Exception:
    df = df.withColumn("holiday_name", F.lit(None).cast("string")).withColumn("is_public_holiday", F.lit(False))

df = df.withColumn("is_business_day", F.expr("not is_weekend and not is_public_holiday")) \
       .orderBy("date_key")

# Idempotent overwrite (re-run to extend the range; a day never "changes" -> no SCD2/MERGE needed).
(df.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
   .save(f"{gold_root}/{target_schema}/{target_table}"))

print(f"dim_date written: {df.count()} rows, {start_date}..{end_date} -> {target_schema}.{target_table}")
