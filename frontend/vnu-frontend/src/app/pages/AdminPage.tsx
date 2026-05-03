import React from 'react';
import { MainLayout } from '../layouts/MainLayout';
import { LoginPanel } from '../features/auth/components/LoginPanel';

export function AdminPage() {
  return (
    <MainLayout showLoginPanel={true}>
      <div className="mb-6 border-b-[3px] border-[#0a3875] pb-2 flex items-center gap-3">
        <div className="w-1.5 h-6 bg-[#0a3875] shrink-0"></div>
        <h2 className="text-xl font-bold text-[#0a3875] uppercase tracking-wide">
          Trang Quản Lý Admin
        </h2>
      </div>

      <div className="bg-white p-6 border border-gray-200 shadow-sm">
        <h3 className="text-lg font-bold text-[#0a3875] mb-4">Chào mừng đến với trang quản lý</h3>
        <p className="text-gray-700 mb-4">
          Vui lòng đăng nhập để truy cập các chức năng:
        </p>
        <ul className="list-disc list-inside text-gray-700 space-y-2">
          <li>Thêm mới công trình nghiên cứu</li>
          <li>Chỉnh sửa thông tin công trình</li>
          <li>Xóa công trình</li>
          <li>Quản lý người dùng</li>
          <li>Xem thống kê tra cứu</li>
        </ul>
      </div>
    </MainLayout>
  );
}

export default AdminPage;
