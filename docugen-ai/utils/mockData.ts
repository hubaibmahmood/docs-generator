import { FileNode, FileType } from '../types';

export const MOCK_REPO_FILES: FileNode[] = [
  {
    id: 'root',
    name: 'src',
    type: FileType.FOLDER,
    path: 'src',
    children: [
      {
        id: 'auth-service',
        name: 'authService.ts',
        type: FileType.FILE,
        path: 'src/services/authService.ts',
        language: 'typescript',
        content: `
import jwt from 'jsonwebtoken';
import { User } from '../models/User';

export class AuthService {
  private secret: string;

  constructor(secret: string) {
    this.secret = secret;
  }

  /**
   * Authenticates a user by email and password
   */
  async login(email: string, password: string): Promise<{ token: string, user: User }> {
    // Simulated DB call
    const user = await User.findOne({ email });
    if (!user || !user.validatePassword(password)) {
      throw new Error('Invalid credentials');
    }
    
    const token = jwt.sign({ id: user.id, role: user.role }, this.secret, { expiresIn: '1h' });
    return { token, user };
  }

  async validateToken(token: string): Promise<any> {
    return jwt.verify(token, this.secret);
  }
}
        `
      },
      {
        id: 'api-routes',
        name: 'routes.ts',
        type: FileType.FILE,
        path: 'src/api/routes.ts',
        language: 'typescript',
        content: `
import { Router } from 'express';
import { UserController } from './controllers/UserController';

const router = Router();
const userController = new UserController();

// GET /users - List all users
router.get('/users', userController.listUsers);

// POST /users - Create new user
router.post('/users', userController.createUser);

// GET /users/:id - Get user details
router.get('/users/:id', userController.getUser);

export default router;
        `
      },
      {
        id: 'utils',
        name: 'helpers.ts',
        type: FileType.FILE,
        path: 'src/utils/helpers.ts',
        language: 'typescript',
        content: `
/**
 * Formats a date string to local locale
 */
export const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US').format(date);
};

/**
 * Retries a promise n times
 */
export const retry = async <T>(fn: () => Promise<T>, retries: number = 3): Promise<T> => {
  try {
    return await fn();
  } catch (err) {
    if (retries > 0) return retry(fn, retries - 1);
    throw err;
  }
};
        `
      }
    ]
  },
  {
    id: 'config',
    name: 'package.json',
    type: FileType.FILE,
    path: 'package.json',
    language: 'json',
    content: `
{
  "name": "demo-api-service",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.2",
    "jsonwebtoken": "^9.0.0",
    "mongoose": "^7.0.0",
    "react": "^18.2.0"
  }
}
    `
  }
];
