export interface ApiResponse<T> {
    success: boolean;
    data: T;
    error?: string;
    timestamp?: string;
}

export interface PaginationMeta {
    total: number;
    page: number;
    pageSize: number;
    hasMore: boolean;
}
