import axiosInstance from './httpClient';
import type { AuthSession, AuthUser } from '../../shared/types/auth';

export interface RegisterPayload {
    email: string;
    full_name: string;
    password: string;
}

export interface LoginPayload {
    email: string;
    password: string;
}

export async function registerUser(payload: RegisterPayload): Promise<AuthUser> {
    const response = await axiosInstance.post('/auth/register', payload);
    return response.data;
}

export async function loginUser(payload: LoginPayload): Promise<AuthSession> {
    const response = await axiosInstance.post('/auth/login', payload);
    const session = response.data;
    localStorage.setItem('auth_token', session.access_token);
    localStorage.setItem('auth_user', JSON.stringify(session.user));
    return session;
}

export async function getCurrentUser(): Promise<AuthUser> {
    const response = await axiosInstance.get('/auth/me');
    localStorage.setItem('auth_user', JSON.stringify(response.data));
    return response.data;
}

export function getStoredUser(): AuthUser | null {
    const rawUser = localStorage.getItem('auth_user');
    if (!rawUser) return null;

    try {
        return JSON.parse(rawUser);
    } catch {
        localStorage.removeItem('auth_user');
        return null;
    }
}

export function logoutUser() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
}
