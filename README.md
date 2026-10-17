\# RetailMax DataOps



Repositorio del pipeline de datos y del modelo de prediccion de ventas de

RetailMax (5 paises, tiendas fisicas y e-commerce). Aqui vive todo lo

necesario para recrear cualquier resultado con comandos desde la terminal

\## Estructura



```text

retailmax-dataops/

├── src/                Codigo del pipeline (extraccion, transformacion, entrenamiento)

├── scripts/            Base sintetica para DEV y snapshots

├── notebooks/          Notebooks EXPORTADOS a .py (sin salidas)

├── sql/queries/        Consultas de negocio

├── config/             Configuracion por entorno (YAML) y reglas MDM (JSON)

├── pipelines/          DAG de Airflow y Jenkinsfile

├── infra/              Terraform: un mismo codigo para DEV, QA y PROD

├── data/               Solo punteros .dvc y PROVENANCE.md (nunca los datos)

├── models/             Vacia en Git: los modelos no se versionan

├── dvc.yaml, .dvc/     Versionamiento de datos con DVC

├── Dockerfile          Entorno reproducible

└── requirements\*.txt   Dependencias con versiones fijas

```



\## Como ejecutarlo en local (DEV)



```bash

python -m venv venv

source venv/Scripts/activate        # Windows (Git Bash). En Linux/Mac: source venv/bin/activate

pip install -r requirements-dev.txt

python -m scripts.create\_db data/ventas.db

APP\_ENV=dev python -m src.train\_ventas

```



\## 1. Que SI se versiona en Git



| Que | Donde | Por que |

|---|---|---|

| Codigo Python y SQL | `src/`, `scripts/`, `sql/` | Es la base de la reproducibilidad |

| Notebooks limpios | `notebooks/\*.py` | Diffs legibles sin datos ni salidas |

| Configuracion | `config/\*.yaml`, `config/\*.json` | Cada entorno se define en codigo, no se configura a mano |

| Dependencias | `requirements\*.txt`, `Dockerfile` | Evita el "en mi maquina si funciona" |

| Pipelines | `pipelines/`, `dvc.yaml` | Saber que flujo produjo cada resultado y poder revertirlo |

| Infraestructura | `infra/\*.tf`, `infra/envs/\*.tfvars` | Entornos identicos y auditables |

| Punteros de datos | `data/\*.dvc`, `data/PROVENANCE.md` | Se versiona la procedencia mas no los datos |



\## 2. Que NO se versiona y por que



| Que | Por que | Donde vive |

|---|---|---|

| Datos (`\*.csv`, `\*.parquet`, `\*.db`) | Pesan gigas y contienen datos personales (PII) | S3, versionados con DVC |

| Modelos (`\*.pkl`) | Binarios que se regeneran desde codigo + datos | DVC / MLflow Model Registry |

| `.env` y credenciales | Riesgo de seguridad | Gestor de secretos (AWS Secrets Manager, GitHub Secrets) |

| `terraform.tfstate` | Contiene secretos y el estado real de la nube | Backend S3 con bloqueo (`infra/versions.tf`) |

| `\*.ipynb` con salidas | Pesan, ensucian el historial y pueden tener datos | Se exportan a `.py` |

| `venv/`, `\_\_pycache\_\_/` | Se regeneran en cada maquina | Local |



Todas estas reglas estan declaradas en `.gitignore`



\## 3. Versionado de la procedencia de los datos



No guardamos los datos en Git guardamos de donde vienen



1\. \*\*Puntero DVC:\*\* `dvc add data/ventas\_2026.parquet` crea

&#x20;  `data/ventas\_2026.parquet.dvc`, un archivo pequeno con el \*\*hash\*\* del

&#x20;  dataset. Ese archivo si va a Git; el dataset va a S3 con `dvc push`

2\. \*\*Documento de procedencia:\*\* `data/PROVENANCE.md` registra la fuente,

&#x20;  la fecha de extraccion, la consulta usada, las transformaciones y la

&#x20;  version de la definicion maestra de "cliente activo"

3\. \*\*Snapshots:\*\* `scripts/create\_snapshot.py` guarda copias fechadas de la

&#x20;  base de datos para recuperarse de corrupciones o borrados

4\. \*\*Recrear un modelo antiguo:\*\* `git checkout <version>` + `dvc pull` +

&#x20;  `python -m src.train\_ventas`



\## Flujo de trabajo



1\. Crear una rama: `git checkout -b feature/<cambio>`

2\. Commits atomicos con prefijo: `feat:`, `fix:`, `test:`, `docs:`, `ci`

3\. Abrir un Pull Request hacia `main`; un revisor aprueba

4\. Con las pruebas en verde se hace merge y el cambio pasa a QA y luego a PROD

