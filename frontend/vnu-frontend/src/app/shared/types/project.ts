export interface Project {
    id: string;
    title: string;
    author: string;
    targetAudience: 'Giảng viên' | 'Sinh viên' | string;
    field: string;
    year: number;
    status: 'Đang thực hiện' | 'Đã nghiệm thu' | 'Hoàn thành' | string;
    abstract: string;
    keywords: string[];
    createdAt?: string;
    updatedAt?: string;
    ai_relevance_score?: number;
}

export interface SearchFilters {
    field?: string;
    targetAudience?: string;
    year?: number | string;
    status?: string;
    keywords?: string[];
    documentType?: string;
    implementationYear?: number | string;
}

export interface SearchResponse {
    data: {
        total: number;
        items: Project[];
    };
    status: string;
    message?: string;
}

export interface SearchError {
    code: string;
    message: string;
}
