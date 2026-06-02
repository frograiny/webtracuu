import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  Calendar, 
  Users, 
  Target, 
  FileText, 
  Tag, 
  ExternalLink, 
  Bookmark, 
  Award, 
  Loader2 
} from 'lucide-react';
import { MainLayout } from '../layouts/MainLayout';
import axiosInstance from '../core/services/httpClient';
import type { Project } from '../shared/types';

// Helper để biến đổi link Google Drive thông thường thành link /preview để nhúng iframe được
function getEmbeddableUrl(url: string): string {
  if (!url) return '';
  
  // Google Drive share link
  if (url.includes('drive.google.com')) {
    const match = url.match(/\/d\/([a-zA-Z0-9-_]+)/);
    if (match && match[1]) {
      return `https://drive.google.com/file/d/${match[1]}/preview`;
    }
  }
  
  // OneDrive share link
  if (url.includes('onedrive.live.com') && url.includes('resid=')) {
    return url.replace('/redir?', '/embed?').replace('/view.aspx?', '/embed?');
  }

  // Nếu là file PDF trực tiếp, có thể nhúng trực tiếp hoặc qua Google Docs Viewer
  if (url.toLowerCase().endsWith('.pdf')) {
    return url;
  }

  // Mặc định trả về qua Google Docs Viewer làm proxy nhúng các loại tài liệu khác
  return `https://docs.google.com/viewer?url=${encodeURIComponent(url)}&embedded=true`;
}

export function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProjectDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axiosInstance.get(`/projects/${id}`);
        if (response.data && response.data.data) {
          const item = response.data.data;
          setProject({
            id: item.id,
            title: item.tenDeTai,
            author: item.chuNhiem,
            targetAudience: item.doiTuong,
            field: item.linhVuc,
            year: item.namThucHien,
            status: item.trangThai,
            abstract: item.tomTat,
            keywords: item.tuKhoa,
            pdfLink: item.pdfLink,
          });
        } else {
          setError('Không tìm thấy thông tin đề tài này.');
        }
      } catch (err: any) {
        console.error('Lỗi khi tải chi tiết đề tài:', err);
        setError('Có lỗi xảy ra trong quá trình tải dữ liệu. Vui lòng thử lại sau.');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchProjectDetails();
    }
  }, [id]);

  return (
    <MainLayout showLoginPanel={false}>
      {/* Nút Quay Lại */}
      <div className="mb-6">
        <Link 
          to="/" 
          className="inline-flex items-center gap-2 text-sm font-semibold text-[#0a3875] hover:text-blue-800 transition-colors group"
        >
          <ArrowLeft className="w-4 h-4 transform group-hover:-translate-x-1 transition-transform" />
          Quay lại danh sách tra cứu
        </Link>
      </div>

      {loading && (
        <div className="flex flex-col items-center justify-center py-20 bg-white border border-gray-100 rounded-2xl shadow-sm">
          <Loader2 className="w-10 h-10 text-[#0a3875] animate-spin mb-4" />
          <p className="text-gray-500 text-sm">Đang tải thông tin chi tiết đề tài nghiên cứu...</p>
        </div>
      )}

      {error && (
        <div className="p-8 text-center bg-red-50 border border-red-100 text-red-600 rounded-2xl">
          <p className="font-semibold text-lg mb-2">Đã xảy ra lỗi</p>
          <p className="text-sm text-red-500 mb-6">{error}</p>
          <Link 
            to="/" 
            className="px-6 py-2.5 bg-[#0a3875] text-white font-medium text-sm rounded-lg hover:bg-blue-900 transition-colors"
          >
            Quay lại trang chủ
          </Link>
        </div>
      )}

      {!loading && !error && project && (
        <div className="space-y-8 animate-fadeIn">
          {/* Header Đề Tài */}
          <div className="bg-white border border-gray-200 shadow-sm p-6 md:p-8 rounded-2xl">
            <div className="flex flex-wrap items-center gap-3 mb-4">
              <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${
                project.status === 'Đã nghiệm thu' || project.status === 'Hoàn thành'
                  ? 'bg-green-50 text-green-700 border-green-200' 
                  : project.status === 'Đang thực hiện'
                  ? 'bg-amber-50 text-amber-700 border-amber-200'
                  : 'bg-gray-50 text-gray-700 border-gray-200'
              }`}>
                {project.status}
              </span>
              {project.field && (
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                  {project.field}
                </span>
              )}
            </div>

            <h1 className="text-2xl md:text-3xl font-extrabold text-gray-900 leading-snug mb-6">
              {project.title}
            </h1>

            {/* Grid Thông Tin Cơ Bản */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
              <div className="flex items-start p-4 bg-gray-50 border border-gray-100 rounded-xl">
                <Users className="w-5 h-5 text-[#0a3875] mr-3 mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs text-gray-400 font-medium">Chủ nhiệm đề tài</p>
                  <p className="text-sm font-semibold text-gray-900 mt-0.5">{project.author}</p>
                </div>
              </div>

              <div className="flex items-start p-4 bg-gray-50 border border-gray-100 rounded-xl">
                <Calendar className="w-5 h-5 text-[#0a3875] mr-3 mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs text-gray-400 font-medium">Năm thực hiện</p>
                  <p className="text-sm font-semibold text-gray-900 mt-0.5">Năm {project.year}</p>
                </div>
              </div>

              <div className="flex items-start p-4 bg-gray-50 border border-gray-100 rounded-xl">
                <Target className="w-5 h-5 text-[#0a3875] mr-3 mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs text-gray-400 font-medium">Đối tượng áp dụng</p>
                  <p className="text-sm font-semibold text-gray-900 mt-0.5">{project.targetAudience || 'Chưa xác định'}</p>
                </div>
              </div>

              <div className="flex items-start p-4 bg-gray-50 border border-gray-100 rounded-xl">
                <Bookmark className="w-5 h-5 text-[#0a3875] mr-3 mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs text-gray-400 font-medium">Loại tài liệu</p>
                  <p className="text-sm font-semibold text-gray-900 mt-0.5">{project.field || 'Đề tài NCKH'}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Tóm tắt & Nội dung nghiên cứu */}
          <div className="bg-white border border-gray-200 shadow-sm p-6 md:p-8 rounded-2xl space-y-6">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-3">
              <Award className="w-5 h-5 text-[#0a3875]" />
              <h2 className="text-lg font-bold text-gray-900">Tóm tắt nội dung đề tài</h2>
            </div>
            
            <p className="text-gray-700 text-base leading-relaxed whitespace-pre-line p-5 bg-blue-50/30 rounded-xl border border-blue-50/50">
              {project.abstract || 'Không có tóm tắt nào cho đề tài này.'}
            </p>

            {project.keywords && project.keywords.length > 0 && (
              <div className="pt-4 flex items-center gap-2 flex-wrap">
                <span className="text-xs font-bold text-gray-400 uppercase tracking-wide mr-2">Từ khóa:</span>
                {project.keywords.map((keyword, index) => (
                  <span 
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-md bg-gray-100 text-gray-700 text-xs font-medium border border-gray-200"
                  >
                    <Tag className="w-3 h-3 mr-1 text-gray-400" />
                    {keyword}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Khung đọc tài liệu PDF */}
          <div className="bg-white border border-gray-200 shadow-sm p-6 md:p-8 rounded-2xl space-y-6">
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-[#0a3875]" />
                <h2 className="text-lg font-bold text-gray-900">Tài liệu đính kèm (PDF / Báo cáo)</h2>
              </div>
              {project.pdfLink && (
                <a 
                  href={project.pdfLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-colors border border-emerald-500 shrink-0"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  Mở tài liệu trong tab mới
                </a>
              )}
            </div>

            {project.pdfLink ? (
              <div className="space-y-4">
                <div className="aspect-[4/3] md:aspect-[16/9] w-full border border-gray-200 rounded-xl overflow-hidden shadow-inner bg-gray-50 relative">
                  <iframe
                    src={getEmbeddableUrl(project.pdfLink)}
                    className="w-full h-full"
                    title={`Embedded Document: ${project.title}`}
                    allow="autoplay"
                  />
                </div>
                <p className="text-xs text-gray-400 text-center italic">
                  * Trình xem tài liệu được đồng bộ hóa từ nguồn cấp gốc. Nếu tài liệu không tải được, bạn vui lòng ấn nút 
                  <strong className="text-[#0a3875] not-italic"> "Mở tài liệu trong tab mới" </strong> phía trên.
                </p>
              </div>
            ) : (
              <div className="py-12 flex flex-col items-center justify-center text-center bg-gray-50 border border-dashed border-gray-200 rounded-xl">
                <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 mb-3">
                  <FileText className="w-6 h-6" />
                </div>
                <p className="text-gray-500 font-medium text-sm">Chưa cập nhật tài liệu PDF trực tuyến</p>
                <p className="text-gray-400 text-xs mt-1">Đề tài nghiên cứu khoa học này chưa có liên kết bản mềm báo cáo đính kèm.</p>
              </div>
            )}
          </div>
        </div>
      )}
    </MainLayout>
  );
}

export default ProjectDetailPage;
