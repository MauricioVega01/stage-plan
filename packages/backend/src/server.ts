import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';

import { authMiddleware } from './middlewares/auth.js';
import { errorHandler } from './middlewares/errorHandler.js';
import { asyncHandler } from './utils/asyncHandler.js';
import { AuthController } from './controllers/auth.controller.js';
import { VenueController } from './controllers/venue.controller.js';
import { CalculationController } from './controllers/calculation.controller.js';

dotenv.config();

// Validación de configuración crítica en producción
if (process.env.NODE_ENV === 'production' && !process.env.JWT_SECRET) {
  console.error('FATAL: La variable de entorno JWT_SECRET es estrictamente requerida en producción.');
  process.exit(1);
}

const app = express();
const port = process.env.PORT || 3000;

// 1. Cabeceras de Seguridad y Políticas CORS
app.use(helmet());
app.use(
  cors({
    origin: process.env.FRONTEND_URL || 'http://localhost:5173',
    credentials: true,
  })
);

// 2. Rate Limiting contra ataques de fuerza bruta
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 200, // Máximo 200 peticiones por ventana
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api', apiLimiter);

// Rate limiter específico para endpoints de login (máx 10 intentos por IP / 15 min)
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Demasiadas solicitudes de autenticación desde esta IP. Por favor intente más tarde.' },
});

app.use(express.json());

// 3. Healthcheck
app.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'STAGE PLAN Backend API',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
  });
});

// 4. Rutas Públicas de Autenticación
app.post('/api/auth/register', asyncHandler(AuthController.register));
app.post('/api/auth/login', loginLimiter, asyncHandler(AuthController.login));
app.get('/api/auth/me', authMiddleware, asyncHandler(AuthController.me));

// 5. Rutas Protegidas de Recintos (Venues) - 100% Anti-IDOR
app.get('/api/venues', authMiddleware, asyncHandler(VenueController.list));
app.get('/api/venues/:id', authMiddleware, asyncHandler(VenueController.getById));
app.post('/api/venues', authMiddleware, asyncHandler(VenueController.create));
app.put('/api/venues/:id', authMiddleware, asyncHandler(VenueController.update));
app.delete('/api/venues/:id', authMiddleware, asyncHandler(VenueController.delete));

// 6. Rutas Protegidas de Cálculo e Historial (Engine + Prisma)
app.post('/api/venues/:venueId/calculate', authMiddleware, asyncHandler(CalculationController.calculateAndSave));
app.get('/api/calculations/history', authMiddleware, asyncHandler(CalculationController.listHistory));
app.get('/api/calculations/:id', authMiddleware, asyncHandler(CalculationController.getById));

// 7. Middleware Centralizado de Excepciones y Normalización de Errores
app.use(errorHandler);

if (process.env.NODE_ENV !== 'test') {
  app.listen(port, () => {
    console.log(`[STAGE PLAN API] Servidor escuchando en http://localhost:${port}`);
  });
}

export default app;

