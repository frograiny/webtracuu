import React, { FC } from 'react';
import { FileText, Users, Calendar, Target, Tag, ChevronRight } from 'lucide-react';
import type { Project } from '../../types';

interface ProjectCardProps {
    project: Project;
}

export const ProjectCard: FC<ProjectCardProps> = ({ project }) => {
    return (
        <div className="bg-white rounded-xl p-6 border border-gray-100 hover:shadow-lg transition-all duration-300 group flex flex-col h-full">
            <div className="flex justify-between items-start gap-4 mb-4">
                <h3 className="text-xl font-semibold text-gray-900 leading-tight group-hover:text-blue-600 transition-colors">
                    {project.title}
                </h3>
                <span className={`shrink-0 px-3 py-1 rounded-full text-xs font-medium border ${project.status === 'Đã nghiệm thu' ? 'bg-green-50 text-green-700 border-green-200' :
                        project.status === 'Đang thực hiện' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                            'bg-gray-50 text-gray-700 border-gray-200'
                    }`}>
                    {project.status}
                </span>
            </div>

            <p className="text-gray-600 line-clamp-3 mb-6 flex-grow text-sm leading-relaxed">
                {project.abstract}
            </p>

            <div className="grid grid-cols-2 gap-y-3 gap-x-4 mb-6 text-sm">
                <div className="flex items-center text-gray-500">
                    <Users className="w-4 h-4 mr-2" />
                    <span className="truncate" title={project.author}>{project.author}</span>
                </div>
                <div className="flex items-center text-gray-500">
                    <Calendar className="w-4 h-4 mr-2" />
                    <span>Năm {project.year}</span>
                </div>
                <div className="flex items-center text-gray-500">
                    <Target className="w-4 h-4 mr-2" />
                    <span className="truncate">{project.targetAudience}</span>
                </div>
                <div className="flex items-center text-gray-500">
                    <FileText className="w-4 h-4 mr-2" />
                    <span className="truncate">{project.field}</span>
                </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                <div className="flex gap-2 flex-wrap max-w-[80%]">
                    {project.keywords && project.keywords.slice(0, 3).map((kw, idx) => (
                        <span key={idx} className="inline-flex items-center px-2 py-1 rounded-md bg-blue-50 text-blue-700 text-xs font-medium">
                            <Tag className="w-3 h-3 mr-1" />
                            {kw}
                        </span>
                    ))}
                    {project.keywords && project.keywords.length > 3 && (
                        <span className="inline-flex items-center px-2 py-1 rounded-md bg-gray-50 text-gray-600 text-xs font-medium">
                            +{project.keywords.length - 3}
                        </span>
                    )}
                </div>
                <button className="text-blue-600 hover:text-blue-700 p-2 rounded-full hover:bg-blue-50 transition-colors">
                    <ChevronRight className="w-5 h-5" />
                </button>
            </div>
        </div>
    );
};
