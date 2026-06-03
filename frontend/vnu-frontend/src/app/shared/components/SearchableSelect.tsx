import React, { FC, useEffect, useMemo, useRef, useState } from 'react';
import { Check, ChevronDown, Search } from 'lucide-react';

interface SearchableSelectProps {
    label: string;
    value?: string;
    options: Array<string | number>;
    onChange: (value: string) => void;
    placeholder?: string;
    searchPlaceholder?: string;
    emptyText?: string;
}

export const SearchableSelect: FC<SearchableSelectProps> = ({
    label,
    value,
    options,
    onChange,
    placeholder = 'Chọn',
    searchPlaceholder = 'Tìm kiếm...',
    emptyText = 'Không có kết quả phù hợp',
}) => {
    const containerRef = useRef<HTMLDivElement | null>(null);
    const [open, setOpen] = useState(false);
    const [search, setSearch] = useState('');

    const selectedValue = value || '';
    const normalizedOptions = useMemo(() => options.map((option) => String(option)), [options]);

    const filteredOptions = useMemo(() => {
        const keyword = search.trim().toLowerCase();
        if (!keyword) return normalizedOptions;

        return normalizedOptions.filter((option) => option.toLowerCase().includes(keyword));
    }, [normalizedOptions, search]);

    useEffect(() => {
        if (!open) {
            setSearch('');
            return;
        }

        const handleClickOutside = (event: MouseEvent) => {
            if (!containerRef.current?.contains(event.target as Node)) {
                setOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [open]);

    return (
        <div ref={containerRef} className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-1.5">{label}</label>

            <button
                type="button"
                onClick={() => setOpen((prev) => !prev)}
                className={`w-full bg-white border text-sm rounded-lg px-3 py-2.5 transition-colors flex items-center justify-between gap-3 focus:outline-none focus:ring-2 focus:ring-blue-800 focus:border-blue-800 ${
                    open ? 'border-blue-800 ring-2 ring-blue-800 text-gray-700' : 'border-gray-200 text-gray-700'
                }`}
                aria-haspopup="listbox"
                aria-expanded={open}
            >
                <span className={`truncate text-left ${selectedValue ? 'text-gray-700' : 'text-gray-400'}`}>
                    {selectedValue || placeholder}
                </span>
                <ChevronDown className={`w-4 h-4 shrink-0 transition-transform ${open ? 'rotate-180' : ''}`} />
            </button>

            {open && (
                <div className="absolute z-20 mt-2 w-full rounded-xl border border-gray-200 bg-white shadow-lg">
                    <div className="p-2 border-b border-gray-100">
                        <div className="flex items-center gap-2 rounded-lg border border-gray-200 px-3 py-2">
                            <Search className="w-4 h-4 text-gray-400" />
                            <input
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                placeholder={searchPlaceholder}
                                className="w-full border-none bg-transparent text-sm text-gray-700 outline-none placeholder:text-gray-400"
                            />
                        </div>
                    </div>

                    <div className="max-h-60 overflow-auto p-1.5">
                        {filteredOptions.length > 0 ? (
                            filteredOptions.map((option) => {
                                const selected = option === selectedValue;

                                return (
                                    <button
                                        key={option}
                                        type="button"
                                        className={`w-full rounded-lg px-3 py-2 text-left text-sm transition-colors flex items-center justify-between gap-3 ${
                                            selected ? 'bg-blue-50 text-blue-800' : 'text-gray-700 hover:bg-gray-50'
                                        }`}
                                        onClick={() => {
                                            onChange(option);
                                            setOpen(false);
                                        }}
                                        role="option"
                                        aria-selected={selected}
                                    >
                                        <span className="truncate">{option}</span>
                                        {selected && <Check className="w-4 h-4 shrink-0" />}
                                    </button>
                                );
                            })
                        ) : (
                            <div className="px-3 py-2 text-sm text-gray-500">{emptyText}</div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};
