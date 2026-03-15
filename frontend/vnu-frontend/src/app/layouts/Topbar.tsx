import React from 'react';
import { Phone, Mail } from 'lucide-react';

export const Topbar = () => {
    return (
        <div className="bg-gray-800 text-gray-300 text-sm py-1.5 hidden md:block">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
                <div className="flex gap-4">
                    <span className="flex items-center gap-1.5"><Phone className="w-3.5 h-3.5 text-gray-400" /> (024) 3858 3755</span>
                    <span className="flex items-center gap-1.5"><Mail className="w-3.5 h-3.5 text-gray-400" /> pkhcn_hus@vnu.edu.vn</span>
                </div>
                <div className="flex gap-4">
                    <a href="#" className="hover:text-white transition-colors">Cán bộ</a>
                    <a href="#" className="hover:text-white transition-colors">Sinh viên</a>
                    <a href="#" className="hover:text-white transition-colors">Thư viện</a>
                </div>
            </div>
        </div>
    );
};
