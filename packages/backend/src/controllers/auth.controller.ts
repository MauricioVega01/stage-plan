import { Request, Response } from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { z } from 'zod';
import { prisma } from '../prisma.js';

const RegisterSchema = z.object({
  email: z.string().email('Formato de correo inválido'),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'),
  name: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
});

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

export class AuthController {
  static async register(req: Request, res: Response): Promise<void> {
    const parse = RegisterSchema.safeParse(req.body);
    if (!parse.success) {
      res.status(400).json({ error: 'Datos inválidos', details: parse.error.format() });
      return;
    }

    const { email, password, name } = parse.data;

    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      res.status(409).json({ error: 'El correo electrónico ya está registrado.' });
      return;
    }

    const passwordHash = await bcrypt.hash(password, 12);
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        name,
      },
      select: { id: true, email: true, name: true, createdAt: true },
    });

    res.status(201).json({ message: 'Usuario registrado exitosamente', user });
  }

  static async login(req: Request, res: Response): Promise<void> {
    const parse = LoginSchema.safeParse(req.body);
    if (!parse.success) {
      res.status(400).json({ error: 'Credenciales inválidas' });
      return;
    }

    const { email, password } = parse.data;
    const user = await prisma.user.findUnique({ where: { email } });

    if (!user) {
      res.status(401).json({ error: 'Credenciales incorrectas.' });
      return;
    }

    const passwordMatch = await bcrypt.compare(password, user.passwordHash);
    if (!passwordMatch) {
      res.status(401).json({ error: 'Credenciales incorrectas.' });
      return;
    }

    const secret = process.env.JWT_SECRET;
    if (!secret && process.env.NODE_ENV === 'production') {
      res.status(500).json({ error: 'Configuración de seguridad incompleta en el servidor.' });
      return;
    }
    const jwtSecret = secret || 'dev_only_stageplan_secret_key';
    const token = jwt.sign(
      { id: user.id, email: user.email, name: user.name },
      jwtSecret,
      { expiresIn: '12h' }
    );

    res.json({
      message: 'Inicio de sesión exitoso',
      token,
      user: { id: user.id, email: user.email, name: user.name },
    });
  }

  static async me(req: Request, res: Response): Promise<void> {
    if (!req.user) {
      res.status(401).json({ error: 'No autenticado' });
      return;
    }
    res.json({ user: req.user });
  }
}

