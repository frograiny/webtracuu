import React, { FC, useMemo } from 'react';
import { SearchableSelect } from '../../../shared/components/SearchableSelect';
import type { SearchFilters } from '../../../shared/types';
import { normalizeAudienceLabel } from '../../../shared/utils/audience';

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

    const ensureAllOption = (options: string[]) => {
        const sanitizedOptions = options.filter(Boolean);
        const withoutAll = sanitizedOptions.filter((option) => option !== 'Tất cả');
        return ['Tất cả', ...withoutAll];
    };

    const audienceOptions = useMemo(() => {
        const normalizedAudiences = filterOptions.audiences.map((audience) => normalizeAudienceLabel(audience));
        return ensureAllOption(Array.from(new Set(normalizedAudiences)));
    }, [filterOptions.audiences]);

    const yearOptions = useMemo(
        () => ensureAllOption(filterOptions.years.map((year) => String(year))),
        [filterOptions.years]
    );

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Lĩnh vực nghiên cứu</label>
                <select
                    className="w-full bg-white border border-gray-200 text-gray-700 text-sm rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-800 focus:border-blue-800 block p-2.5 transition-colors"
                    value={filters.field || 'Tất cả'}
                    onChange={(e) => handleChange('field', e.target.value)}
                >
                    {filterOptions.fields.map((field) => (
                        <option key={field} value={field}>
                            {field}
                        </option>
                    ))}
                </select>
            </div>

            <SearchableSelect
                label="Năm thực hiện"
                value={filters.year ? String(filters.year) : 'Tất cả'}
                options={yearOptions}
                onChange={(value) => handleChange('year', value)}
                searchPlaceholder="Tìm năm thực hiện..."
                emptyText="Không tìm thấy năm phù hợp"
            />

            <SearchableSelect
                label="Thành phần thực hiện"
                value={filters.targetAudience ? normalizeAudienceLabel(filters.targetAudience) : 'Tất cả'}
                options={audienceOptions}
                onChange={(value) => handleChange('targetAudience', value)}
                searchPlaceholder="Tìm thành phần thực hiện..."
                emptyText="Không tìm thấy thành phần phù hợp"
            />
        </div>
    );
};
