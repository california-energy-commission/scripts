# CEC Scripts

Test, lint and deploy schema files in all CEC repositories

## How to run locally

Pass the source and target as parameters:

```
.\deploy\deploy-schema-windows-amd64.exe -d ../NORESCO/2019-Prescriptive-NonResidential-Schema/deployed -s ../NORESCO/2019-Prescriptive-NonResidential-Schema/schema -v 2019.1.003
```

You can also do the other way around.

Go to the schema repo and run:

```
<path to Scripts repo>\deploy\deploy-schema-windows-amd64.exe -d ./deployed -s ./schema -v 2019.1.003
```


