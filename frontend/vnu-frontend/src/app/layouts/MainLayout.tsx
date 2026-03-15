import React, { FC, ReactNode } from 'react';
import { Topbar } from './Topbar';
import { Header } from './Header';

interface LayoutProps {
    children: ReactNode;
}

export const MainLayout: FC<LayoutProps> = ({ children }) => {
    return (
        <div className="min-h-screen bg-gray-50/50 font-sans text-gray-800">
            <Topbar />
            <Header />
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col lg:flex-row gap-8">
                <main className="w-full lg:w-3/4">
                    {children}
                </main>
                <aside className="w-full lg:w-1/4">
                    <div className="bg-white p-5 border border-gray-200 shadow-sm mb-6 border-t-[3px] border-t-red-700">
                        <h3 className="font-bold text-[1.05rem] mb-4 text-[#0a3875] uppercase border-b pb-2 border-gray-100 italic">Bảng tin khoa học</h3>
                        <ul className="space-y-3.5 text-sm text-gray-700">
                            <li className="hover:text-red-700 cursor-pointer transition-colors border-b border-gray-50 pb-2">Thông báo nộp đề cương Quỹ NAFOSTED đợt 2/2026.</li>
                            <li className="hover:text-red-700 cursor-pointer transition-colors border-b border-gray-50 pb-2">Lễ trao giải Sinh viên NCKH cấp ĐHQGHN năm học 2025-2026.</li>
                            <li className="hover:text-red-700 cursor-pointer transition-colors">Hướng dẫn thể thức báo cáo nghiệm thu đề tài cấp cơ sở.</li>
                        </ul>
                    </div>
                    <div className="bg-white p-5 border border-gray-200 shadow-sm border-t-[3px] border-t-[#0a3875]">
                        <h3 className="font-bold text-[1.05rem] mb-4 text-[#0a3875] uppercase border-b pb-2 border-gray-100 italic">Liên kết nhanh</h3>
                        <ul className="space-y-3 text-sm text-gray-700">
                            <li className="hover:text-red-700 cursor-pointer transition-colors flex items-center gap-2"><span className="text-[#0a3875]">»</span> Tạp chí Khoa học ĐHQGHN</li>
                            <li className="hover:text-red-700 cursor-pointer transition-colors flex items-center gap-2"><span className="text-[#0a3875]">»</span> Cổng thông tin Cục SHTT</li>
                            <li className="hover:text-red-700 cursor-pointer transition-colors flex items-center gap-2"><span className="text-[#0a3875]">»</span> TT Thư viện và Tri thức số</li>
                            <li className="hover:text-red-700 cursor-pointer transition-colors flex items-center gap-2"><span className="text-[#0a3875]">»</span> Quản lý đề tài VNU</li>
                        </ul>
                    </div>
                </aside>
            </div>
            
            <footer className="bg-gray-800 text-gray-400 py-10 mt-8 border-t border-gray-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm">
                    <p className="font-semibold text-gray-300">TỬ SÁCH SỐ CÔNG TRÌNH NGHIÊN CỨU KHOA HỌC</p>
                    <p className="mt-1">Trường Đại học Khoa học Tự nhiên, ĐHQGHN</p>
                    <p className="mt-1 text-xs text-gray-500">334 Nguyễn Trãi, Thanh Xuân Trung, Thanh Xuân, Hà Nội</p>
                </div>
            </footer>
        </div>
    );
};
