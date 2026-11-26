# Documentación de la API REST y Seguridad Anti-IDOR: STAGE PLAN (v4.0)
**Proyecto Integrado (TIHV43) — Analista Programador — INACAP Sede Maipú (Sección C1 · Grupo G10)**  
**Subsistema:** `@stageplan/backend` (Node.js + Express + TypeScript + Prisma ORM + SQLite `dev.db`)

---

## 1. Arquitectura de Seguridad Implementada en Backend

### 1.1 Mitigación Anti-IDOR (OWASP Top 10 A01: Broken Access Control)
Toda consulta sobre recintos (`Venue`) o cálculos (`RiderCalculation`) filtra obligatoriamente por `ownerId: req.user.id` extraído del token JWT validado en `authMiddleware`. Ante un recurso inexistente o perteneciente a otro usuario, el controlador responde **`HTTP 404`** para impedir la enumeración de UUIDs válidos.

```typescript
// Patrón implementado en VenueController y CalculationController:
const venue = await prisma.venue.findFirst({
  where: {
    id: venueId,
    ownerId: req.user!.id,
  },
});
if (!venue) {
  res.status(404).json({ error: 'Recinto no encontrado o no tiene permisos sobre él.' });
  return;
}
```

### 1.2 Bloqueo Temporal ante Fuerza Bruta, Rate Limiting y Manejo de Errores
- **Hashing de Contraseñas:** `bcrypt` con factor de costo **12 rondas** (`AuthController.register`).
- **Bloqueo por Intentos Fallidos (`HTTP 423 Locked`):** Tras **5 intentos fallidos** consecutivos de login, `AuthController.login` bloquea la cuenta durante **15 minutos** (`intentos_fallidos` y `bloqueado_hasta` en tabla `usuarios` de SQLite/Prisma).
- **Rate Limiting (`express-rate-limit`):** `200 peticiones / 15 min` en `/api` y `10 peticiones / 15 min` sobre `/api/auth/login` (`HTTP 429`).
- **Cabeceras y CORS:** `helmet()` + `cors({ origin: process.env.FRONTEND_URL || 'http://localhost:5173', credentials: true })`.
- **Excepciones Controladas:** Todas las rutas usan `asyncHandler` y delegan fallos hacia `errorHandler` centralizado sin filtrar *stack traces*.
- **Persistencia Híbrida:** En la PoC actual opera **SQLite 3 (`dev.db`)** mediante Prisma ORM (4 tablas 3FN en español + documentos JSON), con migración configurada hacia **PostgreSQL 16** para producción (`entrega_sumativa_02/sql/schema_stageplan_pg16.sql`).

---

## 2. Endpoints Oficiales de la API

| Método | Endpoint | Autenticación | Descripción |
|---|---|:---:|---|
| `GET` | `/health` | Pública | Verificación de estado del servicio Express. |
| `POST` | `/api/auth/register` | Pública | Registro validado con Zod y hash `bcrypt` (12 rondas). |
| `POST` | `/api/auth/login` | Pública (`loginLimiter 10/15m`) | Emite JWT firmado (`12h`) y aplica bloqueo `HTTP 423` tras 5 fallos. |
| `GET` | `/api/auth/me` | Bearer JWT | Retorna perfil del operador autenticado. |
| `GET` | `/api/venues` | Bearer JWT | Lista únicamente los recintos del usuario (`where: { ownerId }`). |
| `POST` | `/api/venues` | Bearer JWT | Registra un recinto validando esquema `VenueSchema` de Zod. |
| `GET` | `/api/venues/:id` | Bearer JWT | Obtiene un recinto validando propiedad (`HTTP 404` si es ajeno). |
| `PUT` | `/api/venues/:id` | Bearer JWT | Actualiza un recinto validando propiedad (`HTTP 404` si es ajeno). |
| `DELETE` | `/api/venues/:id` | Bearer JWT | Elimina un recinto en cascada validando propiedad (`HTTP 404` si es ajeno). |
| `POST` | `/api/venues/:venueId/calculate` | Bearer JWT | Valida `RiderSchema` + `EngineeringParamsSchema`, ejecuta `@stageplan/shared` y persiste `engineVersion: '4.0.0'` en `calculos_rider`. |
| `GET` | `/api/calculations/history` | Bearer JWT | Lista el historial de cálculos del propietario autenticado. |
| `GET` | `/api/calculations/:id` | Bearer JWT | Obtiene el detalle de un cálculo validando `ownerId` (`HTTP 404` si es ajeno). |
