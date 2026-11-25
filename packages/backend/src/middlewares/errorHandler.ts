import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';

/**
 * Middleware centralizado de gestión de errores y excepciones para la API de StagePlan.
 * Normaliza respuestas de validación Zod, códigos de error Prisma y oculta stack traces en producción.
 */
export function errorHandler(
  err: any,
  _req: Request,
  res: Response,
  _next: NextFunction
): void {
  // 1. Manejo de errores de validación de esquemas Zod
  if (err instanceof ZodError) {
    res.status(400).json({
      error: 'Error de validación de datos de entrada',
      details: err.format(),
    });
    return;
  }

  // 2. Manejo de errores conocidos del motor ORM Prisma
  if (err && typeof err === 'object' && 'code' in err && typeof err.code === 'string' && err.code.startsWith('P')) {
    switch (err.code) {
      case 'P2002':
        res.status(409).json({
          error: 'Conflicto de integridad: ya existe un registro con esos datos únicos.',
          fields: (err as any).meta?.target,
        });
        return;
      case 'P2025':
        res.status(404).json({
          error: 'El recurso solicitado no fue encontrado en la base de datos.',
        });
        return;
      case 'P2003':
        res.status(400).json({
          error: 'Violación de clave foránea: el registro dependiente no existe o no es accesible.',
        });
        return;
      default:
        res.status(400).json({
          error: `Error de base de datos (${err.code}).`,
        });
        return;
    }
  }

  // 3. Fallo genérico / no capturado
  console.error('[Error de Servidor No Capturado]:', err);

  const statusCode = typeof err.status === 'number' ? err.status : (typeof err.statusCode === 'number' ? err.statusCode : 500);
  const isProduction = process.env.NODE_ENV === 'production';

  res.status(statusCode).json({
    error: isProduction ? 'Ha ocurrido un error interno en el servidor.' : (err.message || 'Error interno del servidor'),
    ...(isProduction ? {} : { stack: err.stack }),
  });
}
