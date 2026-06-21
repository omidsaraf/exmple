-- =============================================================================
--  SILVER TRANSFORM - SPARK SQL TEMPLATE  (transform_spark_sql path, ADR-48)
-- -----------------------------------------------------------------------------
--  WHEN TO USE: you want a SQL-FIRST silver build with no notebook to maintain.
--  Set the proc to proc_type='transform_spark_sql' and supply this SQL via the
--  proc_param `sql_inline` (or point proc.sql_path at this .sql file).
--
--  HOW IT RUNS: the framework registers each source in your proc_param `source_map`
--  as a TEMP VIEW (the view name = the source_map key), runs this SQL through the SAME
--  engine as the PySpark path, then owns ALL I/O - source-readiness gate, audit columns,
--  Gold masking, empty-source guardrail, the sanctioned write (write_mode + partition/
--  cluster from metadata), the SCD2 invariant, and logging. You write SQL ONLY.
--
--  RULES: explicit columns (never SELECT *, §5); reference ONLY the source_map view
--  names (never a hardcoded table path); no DDL/DML here (the framework does the write).
--  Heavy SQL is fine: CTEs, window functions, multi-join - same as the UDP example.
-- =============================================================================
WITH latest AS (
    -- dedupe to the latest version per business key (Bronze is append-only, §15.6)
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY <business_key>
                              ORDER BY _ingested_at_utc DESC) AS _rn
    FROM   <appointment_bronze>          -- a source_map key, registered as a temp view
)
SELECT  l.<key_column>,                  -- explicit, typed columns - never SELECT *
        l.<attr_column>,
        c.<lookup_column>                -- fan-in: join another bronze source by its view name
FROM    latest l
LEFT    JOIN <clinic_bronze> c ON l.clinic_id = c.clinic_id
WHERE   l._rn = 1
  AND   l.<business_key> IS NOT NULL;
