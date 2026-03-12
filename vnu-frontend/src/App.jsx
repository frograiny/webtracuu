import React, { useState, useEffect, useMemo } from 'react';
import { Search, Filter, BookOpen, User, Calendar, Tag, Info, X, ChevronRight, GraduationCap, Loader2 } from 'lucide-react';

// ==========================================
// HƯỚNG DẪN SETUP BACKEND:
// ==========================================
// 1. Cài PostgreSQL và tạo database: createdb vnu_research_db
// 2. Cài Python dependencies: pip install fastapi uvicorn sqlalchemy psycopg2-binary
// 3. Chạy: uvicorn app:app --reload --port 8000
// 4. Seed dữ liệu: curl -X POST http://localhost:8000/api/v1/seed-data
// 5. Frontend tự động fetch data từ http://localhost:8000

// ==========================================
// 1. MÔ PHỎNG DỮ LIỆU TỪ DATABASE/API
// ==========================================
const mockDatabase = [
  {
    id: "NCKH-2023-001",
    tenDeTai: "Ứng dụng trí tuệ nhân tạo trong việc cá nhân hóa lộ trình học tập",
    chuNhiem: "Nguyễn Văn An",
    doiTuong: "Giáo viên",    
    linhVuc: "Công nghệ thông tin",
    namThucHien: 2023,
    trangThai: "Đã nghiệm thu",
    tuKhoa: ["AI", "Giáo dục", "Cá nhân hóa"],
    tomTat: "Nghiên cứu ứng dụng các thuật toán học máy để phân tích kết quả học tập của học sinh, từ đó tự động đề xuất bài tập và tài liệu phù hợp với năng lực từng cá nhân."
  },
  {
    id: "NCKH-2023-002",
    tenDeTai: "Giải pháp nâng cao ý thức bảo vệ môi trường cho học sinh THPT qua các hoạt động ngoại khóa",
    chuNhiem: "Trần Thị Bích",
    doiTuong: "Giáo viên",
    linhVuc: "Khoa học xã hội",
    namThucHien: 2023,
    trangThai: "Đã nghiệm thu",
    tuKhoa: ["Môi trường", "Ngoại khóa", "Ý thức"],
    tomTat: "Đề tài tập trung vào việc thiết kế và tổ chức các chuỗi sự kiện, câu lạc bộ bảo vệ môi trường, đánh giá sự thay đổi trong nhận thức và hành động của học sinh trước và sau khi tham gia."
  },
  {
    id: "NCKH-2024-001",
    tenDeTai: "Chế tạo vật liệu sinh học thay thế nhựa dùng một lần từ vỏ trấu",
    chuNhiem: "Lê Hoàng Cường",
    doiTuong: "Học sinh",
    linhVuc: "Hóa học & Vật liệu",
    namThucHien: 2024,
    trangThai: "Đang thực hiện",
    tuKhoa: ["Vật liệu sinh học", "Vỏ trấu", "Bảo vệ môi trường"],
    tomTat: "Dự án nghiên cứu quy trình xử lý vỏ trấu phế phẩm nông nghiệp thành các sản phẩm như đĩa, ly, muỗng có khả năng phân hủy sinh học trong môi trường tự nhiên."
  },
  {
    id: "NCKH-2022-005",
    tenDeTai: "Thiết kế hệ thống tưới tiêu tự động sử dụng năng lượng mặt trời cho vườn trường",
    chuNhiem: "Phạm Minh Đức",
    doiTuong: "Học sinh",
    linhVuc: "Kỹ thuật cơ điện",
    namThucHien: 2022,
    trangThai: "Đã nghiệm thu",
    tuKhoa: ["IoT", "Năng lượng mặt trời", "Tự động hóa"],
    tomTat: "Hệ thống sử dụng cảm biến độ ẩm đất và ánh sáng để điều khiển máy bơm nước tự động, nguồn điện được cung cấp hoàn toàn từ tấm pin năng lượng mặt trời mini."
  },
  {
    id: "NCKH-2024-002",
    tenDeTai: "Nghiên cứu tác động của mạng xã hội đến tâm lý lứa tuổi vị thành niên",
    chuNhiem: "Hoàng Thu Trang",
    doiTuong: "Học sinh",
    linhVuc: "Tâm lý học",
    namThucHien: 2024,
    trangThai: "Đang thực hiện",
    tuKhoa: ["Mạng xã hội", "Tâm lý", "Vị thành niên"],
    tomTat: "Khảo sát trên 500 học sinh về thời lượng sử dụng mạng xã hội và các biểu hiện tâm lý (lo âu, tự ti, trầm cảm), từ đó đề xuất các giải pháp đồng hành cùng học sinh."
  },
  {
    id: "NCKH-2023-010",
    tenDeTai: "Đổi mới phương pháp giảng dạy môn Lịch sử qua hình thức Gamification",
    chuNhiem: "Vũ Hải Yến",
    doiTuong: "Giáo viên",
    linhVuc: "Khoa học giáo dục",
    namThucHien: 2023,
    trangThai: "Đã nghiệm thu",
    tuKhoa: ["Gamification", "Lịch sử", "Phương pháp giảng dạy"],
    tomTat: "Thiết kế các bài học Lịch sử dưới dạng trò chơi nhập vai, giải đố để tăng tính tương tác và hứng thú học tập cho học sinh khối 10."
  }
];

// Các tùy chọn cho bộ lọc
const fields = ["Tất cả", "Công nghệ thông tin", "Khoa học xã hội", "Hóa học & Vật liệu", "Kỹ thuật cơ điện", "Tâm lý học", "Khoa học giáo dục"];
const roles = ["Tất cả", "Giáo viên", "Học sinh"];
const years = ["Tất cả", "2024", "2023", "2022"];

export default function App() {
  // States cho tìm kiếm và lọc
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedField, setSelectedField] = useState('Tất cả');
  const [selectedRole, setSelectedRole] = useState('Tất cả');
  const [selectedYear, setSelectedYear] = useState('Tất cả');
  
  // States cho hiển thị dữ liệu
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [searchMode, setSearchMode] = useState('normal'); // 'normal' hoặc 'ai'

  // ==========================================
  // 2. GỌI API BACKEND THỰC TẾ (Fetch Data)
  // ==========================================
  const fetchDeTaiNCKH = async (query, field, role, year) => {
    setIsLoading(true);
    try {
      // Xây dựng URL với query parameters
      const params = new URLSearchParams({
        q: query,
        field: field,
        target: role,
        year: year,
        limit: 50
      });

      // Gọi API backend
      const response = await fetch(`http://localhost:8000/api/v1/projects/search?${params}`);
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const jsonData = await response.json();

      // Kiểm tra format response
      if (jsonData.status === "success" && jsonData.data) {
        setData(jsonData.data.items || []);
      } else {
        console.error("Unexpected API response format:", jsonData);
        setData([]);
      }
    } catch (error) {
      console.error("Lỗi khi gọi API:", error);
      // Nếu API không khả dụng, hiển thị mockDatabase (fallback)
      let result = mockDatabase;
      if (query) {
        const lowerQuery = query.toLowerCase();
        result = result.filter(item => 
          item.tenDeTai.toLowerCase().includes(lowerQuery) || 
          item.chuNhiem.toLowerCase().includes(lowerQuery) ||
          item.tuKhoa.some(kw => kw.toLowerCase().includes(lowerQuery))
        );
      }
      if (field !== 'Tất cả') {
        result = result.filter(item => item.linhVuc === field);
      }
      if (role !== 'Tất cả') {
        result = result.filter(item => item.doiTuong === role);
      }
      if (year !== 'Tất cả') {
        result = result.filter(item => item.namThucHien.toString() === year);
      }
      setData(result);
    } finally {
      setIsLoading(false);
    }
  };

  // ==========================================
  // 2B. GỌI API AI SEMANTIC SEARCH
  // ==========================================
  const fetchDeTaiAI = async (query) => {
    if (!query.trim()) {
      setData([]);
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/ai-search?q=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const jsonData = await response.json();

      if (jsonData.status === "success" && jsonData.data) {
        setData(jsonData.data || []);
      } else {
        console.error("Unexpected API response format:", jsonData);
        setData([]);
      }
    } catch (error) {
      console.error("Lỗi khi gọi AI Search API:", error);
      // Fallback nếu API không khả dụng
      setData([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Gọi API mỗi khi các tham số lọc thay đổi
  useEffect(() => {
    if (searchMode === 'ai' && searchQuery.trim()) {
      fetchDeTaiAI(searchQuery);
    } else {
      fetchDeTaiNCKH(searchQuery, selectedField, selectedRole, selectedYear);
    }
  }, [searchQuery, selectedField, selectedRole, selectedYear, searchMode]);


  // ==========================================
  // 3. GIAO DIỆN CHÍNH (UI)
  // ==========================================
  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800">
      {/* Header */}
      <header className="bg-blue-700 text-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <GraduationCap size={32} className="text-blue-200" />
            <div>
              <h1 className="text-xl font-bold tracking-tight">Cổng Tra Cứu NCKH</h1>
              <p className="text-xs text-blue-200">Học sinh & Giáo viên</p>
            </div>
          </div>
          <nav className="hidden md:flex space-x-6">
            <a href="#" className="hover:text-blue-200 transition-colors font-medium">Trang chủ</a>
            <a href="#" className="hover:text-blue-200 transition-colors font-medium">Thống kê</a>
            <a href="#" className="hover:text-blue-200 transition-colors font-medium">Hướng dẫn API</a>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8 flex flex-col md:flex-row gap-6">
        
        {/* Sidebar Bộ Lọc */}
        <aside className="w-full md:w-64 flex-shrink-0">
          <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-200 sticky top-24">
            <h2 className="text-lg font-semibold flex items-center mb-4 text-gray-700">
              <Filter size={20} className="mr-2 text-blue-600" />
              Bộ lọc tra cứu
            </h2>

            {/* Thông báo khi dùng AI Search */}
            {searchMode === 'ai' && (
              <div className="mb-4 p-3 bg-purple-50 border border-purple-200 rounded-lg">
                <p className="text-xs text-purple-700">
                  💡 <strong>Chế độ AI:</strong> Tìm kiếm bằng ý nghĩa, các bộ lọc bên dưới sẽ không được dùng.
                </p>
              </div>
            )}
            
            {/* Disable filters khi ở AI mode */}
            <div className={searchMode === 'ai' ? 'opacity-50 pointer-events-none' : ''}>
              {/* Lọc: Đối tượng */}
            <div className="mb-5">
              <label className="block text-sm font-medium text-gray-700 mb-2">Đối tượng</label>
              <div className="space-y-2">
                {roles.map(role => (
                  <label key={role} className="flex items-center">
                    <input 
                      type="radio" 
                      name="role" 
                      value={role}
                      checked={selectedRole === role}
                      onChange={(e) => setSelectedRole(e.target.value)}
                      className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                    />
                    <span className="ml-2 text-sm text-gray-600">{role}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Lọc: Lĩnh vực */}
            <div className="mb-5">
              <label className="block text-sm font-medium text-gray-700 mb-2">Lĩnh vực nghiên cứu</label>
              <select 
                value={selectedField}
                onChange={(e) => setSelectedField(e.target.value)}
                className="w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm p-2 border"
              >
                {fields.map(field => (
                  <option key={field} value={field}>{field}</option>
                ))}
              </select>
            </div>

            {/* Lọc: Năm thực hiện */}
            <div className="mb-5">
              <label className="block text-sm font-medium text-gray-700 mb-2">Năm thực hiện</label>
              <select 
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value)}
                className="w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm p-2 border"
              >
                {years.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>
            
            <button 
              onClick={() => {
                setSearchQuery('');
                setSelectedField('Tất cả');
                setSelectedRole('Tất cả');
                setSelectedYear('Tất cả');
              }}
              className="w-full py-2 px-4 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Xóa bộ lọc
            </button>
            </div>  {/* End of disabled filters div */}
          </div>
        </aside>

        {/* Khu vực nội dung chính (Tìm kiếm & Kết quả) */}
        <div className="flex-1">
          
          {/* Thanh tìm kiếm */}
          <div className="mb-6">
            <div className="flex gap-3 mb-3">
              <button 
                onClick={() => setSearchMode('normal')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  searchMode === 'normal'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                }`}
              >
                🔍 Tìm kiếm bình thường
              </button>
              <button 
                onClick={() => setSearchMode('ai')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  searchMode === 'ai'
                    ? 'bg-purple-600 text-white shadow-md'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                }`}
              >
                🤖 AI Semantic Search
              </button>
            </div>
            
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder={searchMode === 'ai' 
                  ? "Hỏi bằng câu tự nhiên. VD: 'có đề tài nào về AI và giáo dục không?'"
                  : "Nhập tên đề tài, tác giả hoặc từ khóa..."
                }
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-xl leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm shadow-sm transition-all"
              />
            </div>
          </div>

          {/* Tiêu đề kết quả */}
          <div className="mb-4 flex justify-between items-center">
            <h3 className="text-xl font-bold text-gray-800">
              Kết quả tra cứu
            </h3>
            <span className="text-sm bg-blue-100 text-blue-800 py-1 px-3 rounded-full font-medium">
              {data.length} đề tài
            </span>
          </div>

          {/* Danh sách kết quả */}
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-20 bg-white rounded-xl shadow-sm border border-gray-100">
              <Loader2 className="h-8 w-8 text-blue-500 animate-spin mb-4" />
              <p className="text-gray-500">Đang tải dữ liệu từ API...</p>
            </div>
          ) : data.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 bg-white rounded-xl shadow-sm border border-gray-100">
              <BookOpen className="h-12 w-12 text-gray-300 mb-4" />
              <p className="text-gray-500 font-medium">Không tìm thấy đề tài nào phù hợp.</p>
              <p className="text-sm text-gray-400 mt-1">Vui lòng thử thay đổi từ khóa hoặc bộ lọc.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {data.map((topic) => (
                <div 
                  key={topic.id} 
                  onClick={() => setSelectedTopic(topic)}
                  className="bg-white p-5 rounded-xl shadow-sm border border-gray-200 hover:shadow-md hover:border-blue-300 transition-all cursor-pointer group"
                >
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="text-lg font-bold text-blue-700 group-hover:text-blue-800 pr-4 leading-snug">
                      {topic.tenDeTai}
                    </h4>
                    <span className={`flex-shrink-0 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                      topic.trangThai === 'Đã nghiệm thu' 
                        ? 'bg-green-50 text-green-700 border-green-200' 
                        : 'bg-yellow-50 text-yellow-700 border-yellow-200'
                    }`}>
                      {topic.trangThai}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm text-gray-600 mb-4">
                    <div className="flex items-center">
                      <User size={16} className="mr-2 text-gray-400" />
                      <span className="font-medium text-gray-800 mr-1">{topic.chuNhiem}</span> 
                      <span className="text-xs px-2 py-0.5 bg-gray-100 rounded-md">({topic.doiTuong})</span>
                    </div>
                    <div className="flex items-center">
                      <Tag size={16} className="mr-2 text-gray-400" />
                      {topic.linhVuc}
                    </div>
                    <div className="flex items-center">
                      <Calendar size={16} className="mr-2 text-gray-400" />
                      Năm: {topic.namThucHien}
                    </div>
                  </div>

                  <p className="text-gray-600 text-sm line-clamp-2 mb-3">
                    {topic.tomTat}
                  </p>

                  <div className="flex items-center justify-between mt-4 pt-3 border-t border-gray-100">
                    <div className="flex flex-wrap gap-2">
                      {topic.tuKhoa.map((kw, idx) => (
                        <span key={idx} className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-50 text-blue-600">
                          #{kw}
                        </span>
                      ))}
                    </div>
                    <div className="text-blue-600 flex items-center text-sm font-medium group-hover:translate-x-1 transition-transform">
                      Xem chi tiết <ChevronRight size={16} className="ml-1" />
                    </div>
                  </div>

                  {/* Hiển thị AI Score nếu là AI Search Mode */}
                  {searchMode === 'ai' && topic.ai_relevance_score && (
                    <div className="mt-3 pt-3 border-t border-purple-100">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-purple-600 font-medium">🤖 Độ phù hợp AI:</span>
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-2 bg-purple-100 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-purple-500 rounded-full"
                              style={{ width: `${topic.ai_relevance_score}%` }}
                            />
                          </div>
                          <span className="text-purple-700 font-bold">{topic.ai_relevance_score}%</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Modal Hiển thị Chi tiết Đề tài */}
      {selectedTopic && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <h2 className="text-lg font-bold text-gray-800 flex items-center">
                <Info size={20} className="mr-2 text-blue-600" />
                Thông tin chi tiết đề tài
              </h2>
              <button 
                onClick={() => setSelectedTopic(null)}
                className="text-gray-400 hover:text-red-500 hover:bg-red-50 p-2 rounded-full transition-colors"
              >
                <X size={20} />
              </button>
            </div>
            
            {/* Modal Body */}
            <div className="p-6 overflow-y-auto">
              <div className="mb-6">
                <span className="text-xs font-bold tracking-wider text-gray-500 uppercase">Mã đề tài: {selectedTopic.id}</span>
                <h3 className="text-2xl font-bold text-blue-800 mt-2 mb-4 leading-snug">
                  {selectedTopic.tenDeTai}
                </h3>
                <div className="flex flex-wrap gap-2">
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${
                      selectedTopic.trangThai === 'Đã nghiệm thu' 
                        ? 'bg-green-50 text-green-700 border-green-200' 
                        : 'bg-yellow-50 text-yellow-700 border-yellow-200'
                    }`}>
                      {selectedTopic.trangThai}
                  </span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700 border border-gray-200">
                    Năm: {selectedTopic.namThucHien}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 bg-gray-50 p-4 rounded-xl border border-gray-100">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Chủ nhiệm đề tài</p>
                  <p className="font-semibold text-gray-800 flex items-center">
                    <User size={16} className="mr-2 text-gray-400" />
                    {selectedTopic.chuNhiem}
                    <span className="ml-2 text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded-md">{selectedTopic.doiTuong}</span>
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Lĩnh vực nghiên cứu</p>
                  <p className="font-semibold text-gray-800 flex items-center">
                    <BookOpen size={16} className="mr-2 text-gray-400" />
                    {selectedTopic.linhVuc}
                  </p>
                </div>
              </div>

              <div>
                <h4 className="text-lg font-bold text-gray-800 mb-3 border-b pb-2">Tóm tắt nội dung</h4>
                <p className="text-gray-700 leading-relaxed text-justify whitespace-pre-line">
                  {selectedTopic.tomTat}
                </p>
              </div>

              <div className="mt-8">
                <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">Từ khóa</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedTopic.tuKhoa.map((kw, idx) => (
                    <span key={idx} className="inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-medium bg-blue-50 text-blue-700 border border-blue-100">
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 flex justify-end">
              <button 
                onClick={() => setSelectedTopic(null)}
                className="px-5 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-colors"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}