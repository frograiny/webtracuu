import React, { FC } from 'react';
import type { SearchFilters } from '../../types';

interface SearchFiltersProps {
    filters: SearchFilters;
    setFilters: (filters: SearchFilters) => void;
    filterOptions: {
        fields: string[];
        years: (string | number)[];
        audiences: string[];
    };
}

export const SearchFiltersArea: FC<SearchFiltersProps> = ({ filters, setFilters, filterOptions }) => {
    const handleChange = (key: keyof SearchFilters, value: string) => {
        setFilters({ ...filters, [key]: value });
    };

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {/* Lĩnh Vực */}
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Lĩnh vực nghiên cứu</label>
                <select
                    className="w-full bg-white border border-gray-200 text-gray-700 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 transition-colors"
                    value={filters.field || 'Tất cả'}
                    onChange={(e) => handleChange('field', e.target.value)}
                >
                    {filterOptions.fields.map(field => (
                        <option key={field} value={field}>{field}</option>
                    ))}
                </select>
            </div>

            {/* Năm Thực Hiện */}
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Năm thực hiện</label>
                <select
                    className="w-full bg-white border border-gray-200 text-gray-700 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 transition-colors"
                    value={filters.year || 'Tất cả'}
                    onChange={(e) => handleChange('year', e.target.value)}
                >
                    {filterOptions.years.map(year => (
                        <option key={year} value={year}>{year}</option>
                    ))}
                </select>
            </div>

            {/* Đối tượng */}
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Đối tượng mục tiêu</label>
                <select
                    className="w-full bg-white border border-gray-200 text-gray-700 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 transition-colors"
                    value={filters.targetAudience || 'Tất cả'}
                    onChange={(e) => handleChange('targetAudience', e.target.value)}
                >
                    {filterOptions.audiences.map(aud => (
                        <option key={aud} value={aud}>{aud}</option>
                    ))}
                </select>
            </div>
        </div>
    );
};
