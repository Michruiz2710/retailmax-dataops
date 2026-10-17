## Que cambia?
Describe el cambio en 2-3 lineas.

## Por que?
Problema o incidente de RetailMax que resuelve.

## Como se probo?
- [ ] Pruebas unitarias e integracion (pytest)
- [ ] Pruebas de calidad de datos
- [ ] Metrica del modelo comparada con la version en produccion

## Checklist del revisor
- [ ] El codigo sigue el formato (black) y no tiene alertas de seguridad (bandit)
- [ ] No se suben datos, modelos, .env ni terraform.tfstate
- [ ] Si cambia el esquema hay una migracion nueva en sql/migrations/
