# gold/ - kind first, then ONE folder per project (`{dag_uid}/`)

```
gold/
├── DDL/
│   └── {PROJECT-ID}/          <- e.g. HEARING_P1 - ISSUED by metadata/project-register.md
│       └── NN_{object_name}.sql        <- one per object; banded NN = deploy order (see DDL/README)
└── Notebook/
    └── {dag_uid}/
        └── Cnsm{Domain}{Entity}{ProjCode}.py  <- Optus shape, e.g. SlvrAudlgyApptAud001.py
```

SCD2 dims are metadata-only via the framework; DDL files are Warehouse serving views.
Anything under DDL/ or Notebook/ not inside a `{PROJECT-ID}` folder is review-blocking.
