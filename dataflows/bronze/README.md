# bronze/ - kind first, then ONE folder per project (`{dag_uid}/`)

```
bronze/
├── DDL/
│   └── {PROJECT-ID}/          <- e.g. HEARING_P1 - ISSUED by metadata/project-register.md
│       └── NN_{object_name}.sql        <- one per object; banded NN = deploy order (see DDL/README)
└── Notebook/
    └── {dag_uid}/
        └── Brnz{Domain}{Entity}{ProjCode}.py  <- Optus shape, e.g. SlvrAudlgyApptAud001.py
```

Bronze is METADATA-ONLY by default (ADR-34); a bronze project folder here is the approval-gated exception.
Anything under DDL/ or Notebook/ not inside a `{PROJECT-ID}` folder is review-blocking.
