import { Request, Response } from 'express';
import { VenueSchema } from '@stageplan/shared';
import { prisma } from '../prisma.js';

export class VenueController {
  // GET /api/venues (Solo lista los recintos propiedad del usuario autenticado)
  static async list(req: Request, res: Response): Promise<void> {
    const ownerId = req.user!.id;
    const venues = await prisma.venue.findMany({
      where: { ownerId },
      orderBy: { createdAt: 'desc' },
    });
    res.json(venues);
  }

  // GET /api/venues/:id (Protección anti-IDOR: verifica ownerId en la consulta)
  static async getById(req: Request, res: Response): Promise<void> {
    const ownerId = req.user!.id;
    const id = req.params.id as string;

    const venue = await prisma.venue.findFirst({
      where: { id, ownerId },
    });

    if (!venue) {
      res.status(404).json({ error: 'Recinto no encontrado o no tiene permisos para acceder.' });
      return;
    }

    res.json(venue);
  }

  // POST /api/venues (Crea un nuevo recinto asociado al usuario)
  static async create(req: Request, res: Response): Promise<void> {
    const ownerId = req.user!.id;
    const parse = VenueSchema.safeParse(req.body);

    if (!parse.success) {
      res.status(400).json({ error: 'Datos de recinto inválidos', details: parse.error.format() });
      return;
    }

    const data = parse.data;
    const venue = await prisma.venue.create({
      data: {
        ownerId,
        name: data.name,
        widthMeters: data.widthMeters,
        depthMeters: data.depthMeters,
        heightMeters: data.heightMeters,
        environmentType: data.environmentType,
        electricalDistanceMeters: data.electricalDistanceMeters,
      },
    });

    res.status(201).json(venue);
  }

  // PUT /api/venues/:id (Protección anti-IDOR en actualización)
  static async update(req: Request, res: Response): Promise<void> {
    const ownerId = req.user!.id;
    const id = req.params.id as string;

    const parse = VenueSchema.partial().safeParse(req.body);
    if (!parse.success) {
      res.status(400).json({ error: 'Datos de actualización inválidos', details: parse.error.format() });
      return;
    }

    const existing = await prisma.venue.findFirst({ where: { id, ownerId } });
    if (!existing) {
      res.status(404).json({ error: 'Recinto no encontrado o no tiene permisos para modificar.' });
      return;
    }

    const updated = await prisma.venue.update({
      where: { id },
      data: parse.data,
    });

    res.json(updated);
  }

  // DELETE /api/venues/:id (Protección anti-IDOR en eliminación)
  static async delete(req: Request, res: Response): Promise<void> {
    const ownerId = req.user!.id;
    const id = req.params.id as string;

    const existing = await prisma.venue.findFirst({ where: { id, ownerId } });
    if (!existing) {
      res.status(404).json({ error: 'Recinto no encontrado o no tiene permisos para eliminar.' });
      return;
    }

    await prisma.venue.delete({ where: { id } });
    res.json({ message: 'Recinto eliminado exitosamente.' });
  }
}

