import React, { useState, useEffect } from 'react';
import { SearchBar } from '../components/Search/SearchBar';
import { SearchFiltersArea } from '../components/Search/SearchFilters';
import { ProjectCard } from '../components/ProjectCard';
import { useSearch } from '../hooks/useSearch';
import { getFiltersData } from '../services/searchService';
import { MainLayout } from '../layout/MainLayout';
import type { SearchFilters } from '../types';
import './App.css';

function App() {
  const [filters, setFilters] = useState<SearchFilters>({});
  const [filterOptions, setFilterOptions] = useState({ fields: [], years: [], audiences: [] });

  // Custom hook xử lý toàn bộ logic gọi API, debounce, cache
  const { query, setQuery, results, loading, error } = useSearch(filters, {
    debounceDelay: 300,
  });

  // Fetch dữ liệu bộ lọc một lần khi load trang
  useEffect(() => {
    const fetchFilters = async () => {
      const data = await getFiltersData();
      setFilterOptions(data);
    };
    fetchFilters();
  }, []);

  return (
    <MainLayout>
        <div className="mb-6 border-b-[3px] border-[#0a3875] pb-2 flex items-center gap-3">
          <div className="w-1.5 h-6 bg-[#0a3875] shrink-0"></div>
          <h2 className="text-xl font-bold text-[#0a3875] uppercase tracking-wide">
            Tra cứu Công trình Nghiên cứu
          </h2>
        </div>

        {/* Thanh Tìm Kiếm Cốt Lõi */}
        <SearchBar
          query={query}
          setQuery={setQuery}
          filters={filters}
          setFilters={setFilters}
          loading={loading}
          className="mb-6 max-w-4xl"
        />

        {/* Bộ Lọc (Filters) */}
        <SearchFiltersArea
          filters={filters}
          setFilters={setFilters}
          filterOptions={filterOptions}
        />

        {/* Kết quả tìm kiếm / Lỗi */}
        <div className="mt-8">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-bold text-[#0a3875]">
              {results.length > 0 ? `Hiển thị ${results.length} tài liệu` : "Kết quả tra cứu"}
            </h3>
          </div>

          {error && (
            <div className="p-4 bg-red-50 text-red-600 rounded mb-6 border border-red-100 text-sm">
              Có lỗi xảy ra trong quá trình tìm kiếm. Vui lòng thử lại sau.
            </div>
          )}

          {!loading && results.length === 0 && !error && (
            <div className="text-center py-12 bg-white border border-gray-200 shadow-sm mt-4">
              <div className="w-12 h-12 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-gray-400 text-xl">🔍</span>
              </div>
              <p className="text-gray-500 text-sm">Không tìm thấy tài liệu nào phù hợp với điều kiện tra cứu.</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {results.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        </div>
    </MainLayout>
  );
}

export default App;