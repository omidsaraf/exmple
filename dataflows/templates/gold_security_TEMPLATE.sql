/*==============================================================================
  gold_security_TEMPLATE.sql  -  REFERENCE TEMPLATE (not deployed as-is)
------------------------------------------------------------------------------
  ADR-51 + ADR-33: per-layer serving security on the VIEWS, GA Fabric.
  Default home for the views = the LAKEHOUSE'S OWN SQL analytics endpoint (the auto "warehouse on top of
  the lakehouse"; GA CREATE VIEW + RLS + CLS) - NO separate Warehouse item. (A separate Warehouse is an
  exception, only for writable T-SQL; if used, the same DDL applies + OneLake shortcuts.)
  Pattern (all GA on the Lakehouse SQL endpoint and, if ever used, a Warehouse):
    - tables live in the LAKEHOUSE (lh_gold); the SQL endpoint holds VIEWS over those tables (same DB, zero copy)
    - TWO views per table: [domain]_VIEW (consumption: PHI omitted/masked) and
      [domain]_TECH_VIEW (full, privileged)
    - RLS via CREATE SECURITY POLICY + an inline TVF predicate keyed to an Entra GROUP
    - CLS by OMITTING the column in the consumption view (strongest) and/or DDM in-place mask
    - GRANT by Entra security group, never individual users; tech/UNMASK behind PIM/JIT
  Replace {domain}/{entity}/{cols}; this file lives in templates/ (NOT */DDL/, so it is
  not parsed/deployed by CI). gen_views renders the real per-flow versions in Phase 7.

  NOTE on Direct Lake: this T-SQL security governs Warehouse/SQL-endpoint + Import/DirectQuery
  consumers. Direct Lake binds to the LAKEHOUSE TABLES and bypasses these views - enforce
  Direct Lake security in the semantic model (RLS/OLS) + OneLake data-access roles.
==============================================================================*/

-- ============================================================== schemas (per domain)
-- CREATE SCHEMA [audio];             -- tables (in the lakehouse; shown for reference)
-- CREATE SCHEMA [audio_view];        -- consumption / masked views
-- CREATE SCHEMA [audio_tech_view];   -- tech / unmasked views
GO

-- ============================================================== 1) TWO views, cross-DB over lh_gold
-- Consumption view: PHI columns OMITTED (nothing to leak) - the strongest CLS.
CREATE OR ALTER VIEW [audio_view].[audio_dim_patient] AS
    SELECT patient_sk, clinic_id, region, age_band, hearing_band   -- no name/dob/address
    FROM   [lh_gold].[audio].[audio_dim_patient];
GO
-- Tech view: full columns, restricted to privileged roles.
CREATE OR ALTER VIEW [audio_tech_view].[audio_dim_patient] AS
    SELECT *
    FROM   [lh_gold].[audio].[audio_dim_patient];
GO

-- ============================================================== 2) RLS (GA)
-- NOTE (ADR-53): the DEFAULT that gen_views auto-emits is GROUP-ONLY RLS (IS_MEMBER of the domain groups;
-- members see all rows, others none). The mapping-table predicate below is the RICHER variant - use it only
-- for a flow that needs per-row (region/clinic) scoping.
-- ----- mapping-table variant (optional, per-flow) - one policy, Entra-group keyed -----
CREATE FUNCTION [audio].[fn_rls_clinic](@clinic_id INT)
    RETURNS TABLE WITH SCHEMABINDING AS
    RETURN SELECT 1 AS ok
           WHERE IS_ROLEMEMBER('sg-healthent-audiology-read') = 1          -- broad readers: all rows
              OR EXISTS (SELECT 1 FROM [audio].[clinic_access_map] m       -- or scoped by mapping table
                         WHERE m.clinic_id = @clinic_id
                           AND m.principal = USER_NAME());
GO
CREATE SECURITY POLICY [audio].[rls_audio_dim_patient]
    ADD FILTER PREDICATE [audio].[fn_rls_clinic](clinic_id) ON [audio_view].[audio_dim_patient],
    ADD FILTER PREDICATE [audio].[fn_rls_clinic](clinic_id) ON [audio_tech_view].[audio_dim_patient]
    WITH (STATE = ON);
GO

-- ============================================================== 3) DDM (GA) - in-place mask where needed
-- (alternative to omission when the same view must show masked vs full by privilege)
-- ALTER TABLE [lh_gold].[audio].[audio_dim_patient]
--   ALTER COLUMN medicare_no ADD MASKED WITH (FUNCTION = 'partial(0,"XXX-XXX-",3)');
-- GRANT UNMASK TO [sg-healthent-audiology-admin];   -- privileged see real values

-- ============================================================== 4) GRANTs - by Entra GROUP, least privilege
GRANT SELECT ON SCHEMA::[audio_view]      TO [sg-healthent-audiology-read];    -- consumption: general readers
GRANT SELECT ON SCHEMA::[audio_tech_view] TO [sg-healthent-audiology-eng];     -- tech: engineers (PIM/JIT)
-- DENY by default: no grants on [lh_gold] tables to humans; the framework MI/SP writes them.
GO
