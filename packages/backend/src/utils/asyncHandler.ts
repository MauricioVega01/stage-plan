import { Request, Response, NextFunction, RequestHandler } from 'express';

/**
 * Wrapper de orden superior para envolver controladores asíncronos en Express.
 * Captura automáticamente cualquier promesa rechazada o excepción y la delega a next(err).
 */
export const asyncHandler = (
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
): RequestHandler => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};
