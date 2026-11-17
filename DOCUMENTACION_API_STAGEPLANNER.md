# Documentación de la API REST y Seguridad Anti-IDOR: STAGE PLAN (v3.1)
**Proyecto de Título: Analista Programador — INACAP**  
**Subsistema:** `@stageplan/backend` (Node.js + Express + TypeScript + Prisma ORM)

---

## 1. Arquitectura de Seguridad Implementada

### 1.1 Mitigación de Control de Acceso Roto (OWASP Top 10 A01: Broken Access Control / IDOR)
Cada consulta de base de datos que involucra datos sensibles de un usuario (`Venue`, `RiderCalculation`) **obliga** a que el `ownerId` coincida con el identificador inyectado en el JWT:

```typescript
// Patrón de acceso seguro anti-IDOR implementado:
const venue = await prisma.venue.findFirst({
  where: { 
    id: venueId, 
    ownerId: req.user.id // Inyectado desde el token Bearer autenticado
  }
});
if (!venue) {
  return res.status(404).json({ error: 'Recinto no encontrado o no tiene permisos sobre él.' });
}
```

### 1.2 Endpoints Oficiales de la API

| Método | Endpoint | Autenticación | Descripción |
|---|---|:---:|---|
| `POST` | `/api/auth/register` | Pública | Registro de usuario con hash de contraseña `bcrypt` (10 rounds). |
| `POST` | `/api/auth/login` | Pública | Login que emite JWT firmado (12h de validez). |
| `GET` | `/api/auth/me` | Bearer JWT | Obtiene perfil del usuario logueado en sesión. |
| `GET` | `/api/venues` | Bearer JWT | Lista únicamente los recintos creados por el usuario (`where: { ownerId }`). |
| `POST` | `/api/venues` | Bearer JWT | Registra un nuevo recinto validando esquema Zod (`VenueSchema`). |
| `GET` | `/api/venues/:id` | Bearer JWT | Obtiene un recinto por ID validando pertenencia (Anti-IDOR). |
| `PUT` | `/api/venues/:id` | Bearer JWT | Modifica un recinto validando pertenencia (Anti-IDOR). |
| `DELETE` | `/api/venues/:id` | Bearer JWT | Elimina un recinto en cascada validando pertenencia (Anti-IDOR). |
| `POST` | `/api/venues/:venueId/calculate` | Bearer JWT | **Motor oficial:** Valida Rider (`RiderSchema`), ejecuta `calc-engine` (@stageplan/shared) y persiste el cálculo versionado (`3.1.0`) en PostgreSQL. |
| `GET` | `/api/calculations/history` | Bearer JWT | Consulta el historial cronológico de cálculos versionados por usuario. |
| `GET` | `/api/calculations/:id` | Bearer JWT | Obtiene el detalle completo de un cálculo para re-generar el reporte en cliente o Layout. |

