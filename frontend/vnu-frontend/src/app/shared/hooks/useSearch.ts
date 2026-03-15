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
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Cache bằng chuỗi JSONstringify để bao gồm query + filter
    const [cache, setCache] = useState<Map<string, Project[]>>(new Map());

    const debouncedQuery = useDebounce(query, debounceDelay);
    const debouncedFilters = useDebounce(filters, debounceDelay);

    useEffect(() => {
        const performSearch = async () => {
            // Bỏ qua nếu có yêu cầu minChar mà chưa đủ ký tự
            if (minChars > 0 && debouncedQuery.length > 0 && debouncedQuery.length < minChars) {
                setResults([]);
                return;
            }

            const cacheKey = JSON.stringify({ q: debouncedQuery, filters: debouncedFilters });

            // Check cache (chống trùng lặp truy vấn)
            if (cache.has(cacheKey)) {
                setResults(cache.get(cacheKey)!);
                return;
            }

            try {
                setLoading(true);
                setError(null);

                const data = await searchProjects(debouncedQuery, debouncedFilters);
                setResults(data);

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
            } finally {
                setLoading(false);
            }
        };

        performSearch();
    }, [debouncedQuery, debouncedFilters, minChars]);

    return {
        query,
        setQuery,
        results,
        loading,
        error,
        clearSearch: () => setQuery('')
    };
}
