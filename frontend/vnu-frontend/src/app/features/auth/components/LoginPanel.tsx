import React, { FormEvent, useEffect, useState } from 'react';
import { LogIn, LogOut, UserPlus } from 'lucide-react';
import {
    getCurrentUser,
    getStoredUser,
    loginUser,
    logoutUser,
    registerUser,
} from '../../../core/services/authService';
import type { AuthUser } from '../../../shared/types/auth';

type AuthMode = 'login' | 'register';

export function LoginPanel() {
    const [mode, setMode] = useState<AuthMode>('login');
    const [user, setUser] = useState<AuthUser | null>(() => getStoredUser());
    const [fullName, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('auth_token');
        if (!token) return;

        getCurrentUser()
            .then(setUser)
            .catch(() => {
                logoutUser();
                setUser(null);
            });
    }, []);

    const resetForm = () => {
        setFullName('');
        setEmail('');
        setPassword('');
    };

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            if (mode === 'register') {
                await registerUser({
                    full_name: fullName,
                    email,
                    password,
                });
                setMode('login');
                setMessage('Tao tai khoan thanh cong. Dang nhap de tiep tuc.');
                setPassword('');
                return;
            }

            const session = await loginUser({ email, password });
            setUser(session.user);
            resetForm();
        } catch {
            setMessage(mode === 'login' ? 'Email hoac mat khau khong dung.' : 'Khong tao duoc tai khoan.');
        } finally {
            setLoading(false);
        }
    };

    if (user) {
        return (
            <div className="bg-white p-5 border border-gray-200 shadow-sm mb-6 border-t-[3px] border-t-[#0a3875]">
                <div className="flex items-start justify-between gap-3 border-b border-gray-100 pb-3">
                    <div>
                        <h3 className="font-bold text-[1.05rem] text-[#0a3875] uppercase italic">Tai khoan</h3>
                        <p className="text-xs text-gray-500 mt-1">{user.role}</p>
                    </div>
                    <button
                        type="button"
                        className="p-2 border border-gray-200 text-gray-600 hover:text-red-700 hover:border-red-200"
                        onClick={() => {
                            logoutUser();
                            setUser(null);
                        }}
                        title="Dang xuat"
                    >
                        <LogOut className="w-4 h-4" />
                    </button>
                </div>
                <div className="pt-3">
                    <p className="text-sm font-semibold text-gray-800">{user.full_name}</p>
                    <p className="text-xs text-gray-500 break-all mt-1">{user.email}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white p-5 border border-gray-200 shadow-sm mb-6 border-t-[3px] border-t-[#0a3875]">
            <div className="flex items-center justify-between gap-2 border-b border-gray-100 pb-3">
                <h3 className="font-bold text-[1.05rem] text-[#0a3875] uppercase italic">
                    {mode === 'login' ? 'Dang nhap' : 'Tao tai khoan'}
                </h3>
                <button
                    type="button"
                    className="p-2 border border-gray-200 text-gray-600 hover:text-[#0a3875] hover:border-blue-200"
                    onClick={() => {
                        setMode(mode === 'login' ? 'register' : 'login');
                        setMessage('');
                    }}
                    title={mode === 'login' ? 'Tao tai khoan' : 'Dang nhap'}
                >
                    {mode === 'login' ? <UserPlus className="w-4 h-4" /> : <LogIn className="w-4 h-4" />}
                </button>
            </div>

            <form className="pt-4 space-y-3" onSubmit={handleSubmit}>
                {mode === 'register' && (
                    <input
                        className="w-full border border-gray-300 px-3 py-2 text-sm outline-none focus:border-[#0a3875]"
                        placeholder="Ho ten"
                        value={fullName}
                        onChange={(event) => setFullName(event.target.value)}
                        required
                    />
                )}
                <input
                    className="w-full border border-gray-300 px-3 py-2 text-sm outline-none focus:border-[#0a3875]"
                    placeholder="Email"
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required
                />
                <input
                    className="w-full border border-gray-300 px-3 py-2 text-sm outline-none focus:border-[#0a3875]"
                    placeholder="Mat khau"
                    type="password"
                    minLength={8}
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                />
                {message && <p className="text-xs text-red-600 leading-relaxed">{message}</p>}
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex items-center justify-center gap-2 bg-[#0a3875] text-white px-4 py-2 text-sm font-semibold hover:bg-blue-900 disabled:opacity-60"
                >
                    <LogIn className="w-4 h-4" />
                    {loading ? 'Dang xu ly...' : mode === 'login' ? 'Dang nhap' : 'Dang ky'}
                </button>
            </form>
        </div>
    );
}
