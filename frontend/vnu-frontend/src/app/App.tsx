import React, { useState, useEffect } from 'react';
import { SearchBar } from '../components/Search/SearchBar';
import { SearchFiltersArea } from '../components/Search/SearchFilters';
import { ProjectCard } from '../components/ProjectCard';
import { useSearch } from '../hooks/useSearch';
import { getFiltersData } from '../services/searchService';
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
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center shadow-sm">
                <span className="text-white font-bold text-xl">VNU</span>
              </div>
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-700 to-blue-500">
                Hub Nghiên Cứu
              </h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Hệ Sinh Thái Đề Tài NCKH</h2>
          <p className="text-gray-600 text-lg">Khám phá và tra cứu hàng ngàn công trình nghiên cứu khoa học chất lượng cao.</p>
        </div>

        {/* Thanh Tìm Kiếm Cốt Lõi */}
        <SearchBar
          query={query}
          setQuery={setQuery}
          loading={loading}
          className="mb-8 max-w-3xl"
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
            <h3 className="text-xl font-bold text-gray-900">
              {results.length > 0 ? `Hiển thị ${results.length} đề tài` : "Kết quả tìm kiếm"}
            </h3>
          </div>

          {error && (
            <div className="p-4 bg-red-50 text-red-600 rounded-lg mb-6 border border-red-100">
              Có lỗi xảy ra trong quá trình tìm kiếm. Vui lòng thử lại sau.
            </div>
          )}

          {!loading && results.length === 0 && !error && (
            <div className="text-center py-16 bg-white rounded-2xl border border-gray-100 border-dashed">
              <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-gray-400 text-2xl">🔍</span>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-1">Không tìm thấy kết quả</h3>
              <p className="text-gray-500 max-w-sm mx-auto">Thử điều chỉnh từ khóa hoặc thay đổi bộ lọc để tìm được nhiều đề tài hơn.</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;