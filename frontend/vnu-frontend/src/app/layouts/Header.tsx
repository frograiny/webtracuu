import React from 'react';
import husLogo from '../../assets/logohuss.png';

export const Header = () => {
    return (
        <header className="bg-white border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-24">
                    <div className="flex items-center gap-4">
                        <div className="w-16 h-16 flex items-center justify-center">
                            <img src={husLogo} alt="HUS Logo" className="w-full h-full object-contain" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-[#0a3875] leading-tight drop-shadow-sm">
                                TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN<br/>
                                <span className="text-[1.1rem]">ĐẠI HỌC QUỐC GIA HÀ NỘI</span>
                            </h1>
                            <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mt-0.5">
                                VNU University of Science
                            </p>
                        </div>
                    </div>
                    <nav className="hidden lg:flex gap-7 font-bold text-[#0a3875] text-[0.9rem] tracking-wide">
                        <a href="#" className="hover:text-blue-600 transition-colors py-3 border-b-2 border-transparent hover:border-blue-600">TRANG CHỦ</a>
                        <a href="#" className="hover:text-blue-600 transition-colors py-3 border-b-2 border-[#0a3875] text-[#0a3875]">NGHIÊN CỨU</a>
                        <a href="#" className="hover:text-blue-600 transition-colors py-3 border-b-2 border-transparent hover:border-blue-600">ĐÀO TẠO</a>
                        <a href="#" className="hover:text-blue-600 transition-colors py-3 border-b-2 border-transparent hover:border-blue-600">TUYỂN DỤNG</a>
                        <a href="#" className="hover:text-blue-600 transition-colors py-3 border-b-2 border-transparent hover:border-blue-600">GIỚI THIỆU</a>
                    </nav>
                </div>
            </div>
        </header>
    );
};
