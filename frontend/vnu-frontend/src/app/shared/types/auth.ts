export interface AuthUser {
    id: string;
    email: string;
    full_name: string;
    role: string;
    is_active: boolean;
}

export interface AuthSession {
    access_token: string;
    token_type: string;
    user: AuthUser;
}
