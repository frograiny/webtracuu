import { useState, useEffect } from 'react';
import { useDebounce } from './useDebounce';
import { searchProjects } from '../../core/services/searchService';
import type { Project, SearchFilters } from '../types';

interface UseSearchOptions {
    debounceDelay?: number;
    minChars?: number;
}

export function useSearch(filters: SearchFilters, options: UseSearchOptions = {}) {
    const { debounceDelay = 300, minChars = 0 } = options;

    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Project[]>([]);
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Cache bằng chuỗi JSONstringify để bao gồm query + filter + page
    const [cache, setCache] = useState<Map<string, { results: Project[], total: number }>>(new Map());

    const debouncedQuery = useDebounce(query, debounceDelay);
    const debouncedFilters = useDebounce(filters, debounceDelay);

    // Reset về trang 1 khi thay đổi điều kiện tìm kiếm
    useEffect(() => {
        setPage(1);
    }, [debouncedQuery, debouncedFilters]);

    useEffect(() => {
        const performSearch = async () => {
            // Bỏ qua nếu có yêu cầu minChar mà chưa đủ ký tự
            if (minChars > 0 && debouncedQuery.length > 0 && debouncedQuery.length < minChars) {
                setResults([]);
                setTotal(0);
                return;
            }

            const cacheKey = JSON.stringify({ q: debouncedQuery, filters: debouncedFilters, page });

            // Check cache (chống trùng lặp truy vấn)
            if (cache.has(cacheKey)) {
                const cachedData = cache.get(cacheKey)!;
                setResults(cachedData.results);
                setTotal(cachedData.total);
                return;
            }

            try {
                setLoading(true);
                setError(null);

                const limit = 10;
                const offset = (page - 1) * limit;
                const data = await searchProjects(debouncedQuery, debouncedFilters, { limit, offset });
                setResults(data.results);
                setTotal(data.total);

                // Update cache (chỉ lưu tối đa 50 truy vấn tránh bị rò rỉ bộ nhớ)
                setCache(prev => {
                    const newCache = new Map(prev);
                    if (newCache.size > 50) {
                        const firstKey = newCache.keys().next().value;
                        if (firstKey) newCache.delete(firstKey);
                    }
                    return newCache.set(cacheKey, data);
                });

            } catch (err) {
                setError(err instanceof Error ? err.message : 'Search failed');
                setResults([]);
                setTotal(0);
            } finally {
                setLoading(false);
            }
        };

        performSearch();
    }, [debouncedQuery, debouncedFilters, page, minChars]);

    return {
        query,
        setQuery,
        results,
        total,
        page,
        setPage,
        loading,
        error,
        clearSearch: () => {
            setQuery('');
            setPage(1);
        }
    };
}
