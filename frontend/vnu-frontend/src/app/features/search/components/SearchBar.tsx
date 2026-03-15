import React, { FC } from 'react';
import { Search, Loader2, X } from 'lucide-react';
import type { SearchFilters } from '../../../shared/types';

interface SearchBarProps {
    query: string;
    setQuery: (q: string) => void;
    filters?: SearchFilters;
    setFilters?: (filters: SearchFilters) => void;
    loading?: boolean;
    className?: string;
}

export const SearchBar: FC<SearchBarProps> = ({ query, setQuery, filters, setFilters, loading, className = '' }) => {
    return (
        <div className={`flex gap-2 ${className}`}>
            {setFilters && filters && (
                <select
                    className="bg-white border border-gray-300 text-gray-700 text-sm focus:border-[#0a3875] outline-none transition-all shadow-sm rounded-sm shrink-0 font-medium md:min-w-[180px] px-3"
                    value={filters.documentType || 'Tất cả'}
                    onChange={(e) => setFilters({ ...filters, documentType: e.target.value })}
                >
                    <option value="Tất cả">Tất cả tài liệu</option>
                    <option value="Đề tài NCKH">Đề tài NCKH</option>
                    <option value="Luận văn Thạc sĩ">Luận văn Thạc sĩ</option>
                    <option value="Khóa luận Tốt nghiệp">Khóa luận Tốt nghiệp</option>
                </select>
            )}
            <div className="flex flex-1 items-center gap-2 px-3 py-2 bg-white rounded-sm border border-gray-300 focus-within:border-[#0a3875] focus-within:ring-[0.5px] focus-within:ring-[#0a3875] transition-all shadow-sm">
                {loading ? (
                    <Loader2 className="w-5 h-5 text-[#0a3875] animate-spin" />
                ) : (
                    <Search className="w-5 h-5 text-gray-400" />
                )}

                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Tìm kiếm tài liệu, tên đề tài, tác giả, hoặc từ khóa..."
                    className="flex-1 bg-transparent border-none outline-none text-gray-800 placeholder:text-gray-400 text-sm"
                />

                {query && (
                    <button
                        onClick={() => setQuery('')}
                        className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                        title="Xóa tìm kiếm"
                    >
                        <X className="w-4 h-4" />
                    </button>
                )}
            </div>
        </div>
    );
};
