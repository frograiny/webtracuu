import React, { FC } from 'react';
import { Search, Loader2, X } from 'lucide-react';

interface SearchBarProps {
    query: string;
    setQuery: (q: string) => void;
    loading?: boolean;
    className?: string;
}

export const SearchBar: FC<SearchBarProps> = ({ query, setQuery, loading, className = '' }) => {
    return (
        <div className={`relative ${className}`}>
            <div className="flex items-center gap-2 px-4 py-3 bg-white rounded-xl border border-gray-200 focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-100 transition-all duration-300 shadow-sm">
                {loading ? (
                    <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
                ) : (
                    <Search className="w-5 h-5 text-gray-400" />
                )}

                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Tìm kiếm tên đề tài, tác giả, hoặc từ khóa..."
                    className="flex-1 bg-transparent border-none outline-none text-gray-700 placeholder:text-gray-400 text-base"
                />

                {query && (
                    <button
                        onClick={() => setQuery('')}
                        className="p-1 rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
                        title="Xóa tìm kiếm"
                    >
                        <X className="w-4 h-4" />
                    </button>
                )}
            </div>
        </div>
    );
};
