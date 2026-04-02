import axiosInstance from './httpClient';
import type { Project, SearchFilters } from '../../shared/types';
import { normalizeAudienceLabel } from '../../shared/utils/audience';

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
): Promise<{ results: Project[]; total: number }> {
    try {
        const params: SearchParams = {
            q: query,
            limit: pagination?.limit || 20,
            offset: pagination?.offset || 0,
        };

        if (filters?.field && filters.field !== 'Tất cả') params.field = filters.field;
        if (filters?.targetAudience && filters.targetAudience !== 'Tất cả') {
            params.target = normalizeAudienceLabel(filters.targetAudience);
        }
        if (filters?.year && filters.year !== 'Tất cả') params.year = filters.year;
        if (filters?.documentType && filters.documentType !== 'Tất cả') params.type = filters.documentType;

        const response = await axiosInstance.get('/projects/search', { params });

        if (response.data.status === 'success') {
            const rawItems = response.data.data.items;
            const total = response.data.data.total;

            return {
                results: rawItems.map((item: any) => ({
                    id: item.id,
                    title: item.tenDeTai,
                    author: item.chuNhiem,
                    targetAudience: normalizeAudienceLabel(item.doiTuong),
                    field: item.linhVuc,
                    year: item.namThucHien,
                    status: item.trangThai,
                    abstract: item.tomTat,
                    keywords: item.tuKhoa,
                })),
                total,
            };
        }

        return { results: [], total: 0 };
    } catch (error) {
        console.error('Search error:', error);
        throw new Error('Failed to fetch search results');
    }
}

export async function getFiltersData(): Promise<any> {
    try {
        const response = await axiosInstance.get('/filters');
        if (response.data.status === 'success') {
            return {
                ...response.data.data,
                audiences: (response.data.data.audiences ?? []).map((audience: string) =>
                    normalizeAudienceLabel(audience)
                ),
            };
        }
        return { fields: [], years: [], audiences: [] };
    } catch (error) {
        console.error('Lỗi khi lấy bộ lọc', error);
        return { fields: [], years: [], audiences: [] };
    }
}
