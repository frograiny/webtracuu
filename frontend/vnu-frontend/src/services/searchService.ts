import axiosInstance from './httpClient';
import type { Project, SearchFilters } from '../types';

interface SearchParams {
    q: string;
    field?: string;
    target?: string;
    year?: number | string;
    type?: string;
    limit?: number;
    offset?: number;
}

export async function searchProjects(
    query: string,
    filters?: SearchFilters,
    pagination?: { limit?: number; offset?: number }
): Promise<Project[]> {
    try {
        const params: SearchParams = {
            q: query,
            limit: pagination?.limit || 20,
            offset: pagination?.offset || 0,
        };

        // Ánh xạ lại tên tham số filter cho đúng với FastAPI
        if (filters?.field && filters.field !== "Tất cả") params.field = filters.field;
        if (filters?.targetAudience && filters.targetAudience !== "Tất cả") params.target = filters.targetAudience;
        if (filters?.year && filters.year !== "Tất cả") params.year = filters.year;
        
        // Thêm mapping cho các trường mới
        if (filters?.documentType && filters.documentType !== "Tất cả") params.type = filters.documentType;

        const response = await axiosInstance.get(
            `/projects/search`,
            { params }
        );

        // FastAPI trả về mảng ở định dạng tiếng Việt (tenDeTai, chuNhiem...), ta map lại
        if (response.data.status === 'success') {
            const rawItems = response.data.data.items;
            return rawItems.map((item: any) => ({
                id: item.id,
                title: item.tenDeTai,
                author: item.chuNhiem,
                targetAudience: item.doiTuong,
                field: item.linhVuc,
                year: item.namThucHien,
                status: item.trangThai,
                abstract: item.tomTat,
                keywords: item.tuKhoa,
            }));
        }

        return [];
    } catch (error) {
        console.error('Search error:', error);
        throw new Error('Failed to fetch search results');
    }
}

export async function getFiltersData(): Promise<any> {
    try {
        const response = await axiosInstance.get(`/filters`);
        if (response.data.status === 'success') {
            return response.data.data;
        }
        return { fields: [], years: [], audiences: [] };
    } catch (error) {
        console.error('Lỗi khi lấy bộ lọc', error);
        return { fields: [], years: [], audiences: [] };
    }
}
