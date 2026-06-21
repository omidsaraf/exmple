# silver/ - kind first, then ONE folder per project (`{dag_uid}/`)

```
silver/
├── DDL/
│   └── {PROJECT-ID}/          <- e.g. HEARING_P1 - ISSUED by metadata/project-register.md
│       └── NN_{object_name}.sql        <- one per object; banded NN = deploy order (see DDL/README)
└── Notebook/
    └── {dag_uid}/
        └── Slvr{Domain}{Entity}{ProjCode}.py  <- Optus shape, e.g. SlvrAudlgyApptAud001.py
```

Notebook bodies start from templates/notebooks/nb_silver_transform_TEMPLATE.py.
Anything under DDL/ or Notebook/ not inside a `{PROJECT-ID}` folder is review-blocking.
