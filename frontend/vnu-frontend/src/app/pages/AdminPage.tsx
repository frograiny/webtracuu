import React, { FormEvent, useEffect, useState } from 'react';
import { Edit3, LogIn, LogOut, Plus, RefreshCw, Save, Trash2, UserPlus, X } from 'lucide-react';
import { MainLayout } from '../layouts/MainLayout';
import axiosInstance from '../core/services/httpClient';
import {
  getCurrentUser,
  getStoredUser,
  loginUser,
  logoutUser,
  registerUser,
} from '../core/services/authService';
import type { AuthUser } from '../shared/types/auth';

interface AdminProject {
  id: string;
  tenDeTai: string;
  chuNhiem: string;
  doiTuong: string;
  linhVuc: string;
  namThucHien: number;
  trangThai: string;
  tomTat: string;
  tuKhoa: string[];
  loaiTaiLieu: string;
  namTrienKhai?: number | null;
  pdfLink?: string;
}

interface ProjectFormState {
  tenDeTai: string;
  chuNhiem: string;
  doiTuong: string;
  linhVuc: string;
  namThucHien: string;
  trangThai: string;
  tomTat: string;
  tuKhoa: string;
  loaiTaiLieu: string;
  namTrienKhai: string;
  pdfLink: string;
}

const emptyForm: ProjectFormState = {
  tenDeTai: '',
  chuNhiem: '',
  doiTuong: 'Giang vien',
  linhVuc: '',
  namThucHien: String(new Date().getFullYear()),
  trangThai: 'Dang thuc hien',
  tomTat: '',
  tuKhoa: '',
  loaiTaiLieu: 'De tai NCKH',
  namTrienKhai: String(new Date().getFullYear()),
  pdfLink: '',
};

function toForm(project: AdminProject): ProjectFormState {
  return {
    tenDeTai: project.tenDeTai ?? '',
    chuNhiem: project.chuNhiem ?? '',
    doiTuong: project.doiTuong ?? 'Giang vien',
    linhVuc: project.linhVuc ?? '',
    namThucHien: String(project.namThucHien ?? new Date().getFullYear()),
    trangThai: project.trangThai ?? 'Dang thuc hien',
    tomTat: project.tomTat ?? '',
    tuKhoa: Array.isArray(project.tuKhoa) ? project.tuKhoa.join(', ') : String(project.tuKhoa ?? ''),
    loaiTaiLieu: project.loaiTaiLieu ?? 'De tai NCKH',
    namTrienKhai: project.namTrienKhai ? String(project.namTrienKhai) : '',
    pdfLink: project.pdfLink ?? '',
  };
}

function toPayload(form: ProjectFormState) {
  return {
    tenDeTai: form.tenDeTai.trim(),
    chuNhiem: form.chuNhiem.trim(),
    doiTuong: form.doiTuong.trim(),
    linhVuc: form.linhVuc.trim(),
    namThucHien: Number(form.namThucHien),
    trangThai: form.trangThai.trim(),
    tomTat: form.tomTat.trim(),
    tuKhoa: form.tuKhoa
      .split(',')
      .map((keyword) => keyword.trim())
      .filter(Boolean),
    loaiTaiLieu: form.loaiTaiLieu.trim(),
    namTrienKhai: form.namTrienKhai ? Number(form.namTrienKhai) : null,
    pdfLink: form.pdfLink.trim(),
  };
}

function normalizeItems(items: any[]): AdminProject[] {
  return items.map((item) => ({
    id: item.id,
    tenDeTai: item.tenDeTai,
    chuNhiem: item.chuNhiem,
    doiTuong: item.doiTuong,
    linhVuc: item.linhVuc,
    namThucHien: item.namThucHien,
    trangThai: item.trangThai,
    tomTat: item.tomTat,
    tuKhoa: Array.isArray(item.tuKhoa) ? item.tuKhoa : String(item.tuKhoa ?? '').split(/\s*,\s*/).filter(Boolean),
    loaiTaiLieu: item.loaiTaiLieu,
    namTrienKhai: item.namTrienKhai,
    pdfLink: item.pdfLink,
  }));
}

export function AdminPage() {
  const [user, setUser] = useState<AuthUser | null>(() => getStoredUser());
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [projects, setProjects] = useState<AdminProject[]>([]);
  const [form, setForm] = useState<ProjectFormState>(emptyForm);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const isAdmin = user?.role === 'admin';

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (!token) return;

    getCurrentUser()
      .then(setUser)
      .catch(() => {
        logoutUser();
        setUser(null);
      });
  }, []);

  const loadProjects = async () => {
    setLoading(true);
    setMessage('');
    try {
      const response = await axiosInstance.get('/projects/search', {
        params: { q: '', limit: 100, offset: 0 },
      });
      setProjects(normalizeItems(response.data.data.items ?? []));
    } catch {
      setMessage('Khong tai duoc danh sach de tai.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAdmin) {
      loadProjects();
    }
  }, [isAdmin]);

  const handleAuthSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      if (authMode === 'register') {
        await registerUser({ full_name: fullName, email, password });
        setAuthMode('login');
        setMessage('Tao tai khoan thanh cong. Dang nhap de vao trang admin.');
        setPassword('');
        return;
      }

      const session = await loginUser({ email, password });
      setUser(session.user);
      setEmail('');
      setPassword('');
      setFullName('');
    } catch {
      setMessage(authMode === 'login' ? 'Dang nhap that bai.' : 'Khong tao duoc tai khoan.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitProject = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const payload = toPayload(form);
      if (editingId) {
        await axiosInstance.put(`/projects/${editingId}`, payload);
        setMessage('Da cap nhat de tai.');
      } else {
        await axiosInstance.post('/projects', payload);
        setMessage('Da them de tai moi.');
      }

      setForm(emptyForm);
      setEditingId(null);
      await loadProjects();
    } catch (error: any) {
      const detail = error?.response?.data?.detail;
      setMessage(typeof detail === 'string' ? detail : 'Khong luu duoc du lieu.');
    } finally {
      setLoading(false);
    }
  };

  const startEdit = (project: AdminProject) => {
    setEditingId(project.id);
    setForm(toForm(project));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const deleteProject = async (project: AdminProject) => {
    if (!confirm(`Xoa de tai "${project.tenDeTai}"?`)) return;

    setLoading(true);
    setMessage('');
    try {
      await axiosInstance.delete(`/projects/${project.id}`);
      setMessage('Da xoa de tai.');
      await loadProjects();
    } catch {
      setMessage('Khong xoa duoc de tai.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout showLoginPanel={false}>
      <div className="mb-6 border-b-[3px] border-[#0a3875] pb-2 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-1.5 h-6 bg-[#0a3875] shrink-0"></div>
          <h2 className="text-xl font-bold text-[#0a3875] uppercase tracking-wide">Trang quan tri</h2>
        </div>
        {user && (
          <button
            type="button"
            className="flex items-center gap-2 border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 hover:border-red-300 hover:text-red-700"
            onClick={() => {
              logoutUser();
              setUser(null);
              setProjects([]);
            }}
          >
            <LogOut className="w-4 h-4" />
            Dang xuat
          </button>
        )}
      </div>

      {!user && (
        <div className="max-w-xl bg-white p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between border-b border-gray-100 pb-3 mb-5">
            <h3 className="text-lg font-bold text-[#0a3875]">
              {authMode === 'login' ? 'Dang nhap admin' : 'Tao tai khoan'}
            </h3>
            <button
              type="button"
              className="p-2 border border-gray-200 text-gray-600 hover:text-[#0a3875]"
              onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
              title={authMode === 'login' ? 'Tao tai khoan' : 'Dang nhap'}
            >
              {authMode === 'login' ? <UserPlus className="w-4 h-4" /> : <LogIn className="w-4 h-4" />}
            </button>
          </div>

          <form className="space-y-4" onSubmit={handleAuthSubmit}>
            {authMode === 'register' && (
              <input
                className="w-full border border-gray-300 px-3 py-2 text-sm outline-none focus:border-[#0a3875]"
                placeholder="Ho ten"
                value={fullName}
                onChange={(event) => setFullName(event.target.value)}
                required
              />
            )}
            <input
              className="w-full border border-gray-300 px-3 py-2 text-sm outline-none focus:border-[#0a3875]"
              placeholder="Email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
            <input
              className="w-full border border-gray-300 px-3 py-2 text-sm outline-none focus:border-[#0a3875]"
              placeholder="Mat khau"
              type="password"
              minLength={8}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
            {message && <p className="text-sm text-red-600">{message}</p>}
            <button
              type="submit"
              disabled={loading}
              className="flex w-full items-center justify-center gap-2 bg-[#0a3875] px-4 py-2 text-sm font-semibold text-white hover:bg-blue-900 disabled:opacity-60"
            >
              <LogIn className="w-4 h-4" />
              {loading ? 'Dang xu ly...' : authMode === 'login' ? 'Dang nhap' : 'Dang ky'}
            </button>
          </form>
        </div>
      )}

      {user && !isAdmin && (
        <div className="bg-yellow-50 border border-yellow-200 p-5 text-sm text-yellow-800">
          Tai khoan hien tai co role <strong>{user.role}</strong>. Trang nay chi danh cho admin.
        </div>
      )}

      {isAdmin && (
        <div className="grid grid-cols-1 xl:grid-cols-[420px_1fr] gap-6">
          <form className="bg-white border border-gray-200 shadow-sm p-5 h-fit" onSubmit={handleSubmitProject}>
            <div className="flex items-center justify-between border-b border-gray-100 pb-3 mb-4">
              <h3 className="font-bold text-[#0a3875]">{editingId ? 'Sua de tai' : 'Them de tai'}</h3>
              {editingId && (
                <button
                  type="button"
                  className="p-2 border border-gray-200 text-gray-600"
                  onClick={() => {
                    setEditingId(null);
                    setForm(emptyForm);
                  }}
                  title="Huy sua"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            <div className="space-y-3">
              <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Ten de tai" value={form.tenDeTai} onChange={(event) => setForm({ ...form, tenDeTai: event.target.value })} required minLength={10} />
              <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Chu nhiem" value={form.chuNhiem} onChange={(event) => setForm({ ...form, chuNhiem: event.target.value })} required />
              <div className="grid grid-cols-2 gap-3">
                <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Doi tuong" value={form.doiTuong} onChange={(event) => setForm({ ...form, doiTuong: event.target.value })} required />
                <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Linh vuc" value={form.linhVuc} onChange={(event) => setForm({ ...form, linhVuc: event.target.value })} required />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Nam thuc hien" type="number" min="2000" max="2030" value={form.namThucHien} onChange={(event) => setForm({ ...form, namThucHien: event.target.value })} required />
                <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Nam trien khai" type="number" min="2000" max="2030" value={form.namTrienKhai} onChange={(event) => setForm({ ...form, namTrienKhai: event.target.value })} />
              </div>
              <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Trang thai" value={form.trangThai} onChange={(event) => setForm({ ...form, trangThai: event.target.value })} />
              <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Loai tai lieu" value={form.loaiTaiLieu} onChange={(event) => setForm({ ...form, loaiTaiLieu: event.target.value })} />
              <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Tu khoa, cach nhau bang dau phay" value={form.tuKhoa} onChange={(event) => setForm({ ...form, tuKhoa: event.target.value })} />
              <input className="w-full border border-gray-300 px-3 py-2 text-sm" placeholder="Link tài liệu / PDF (Google Drive, OneDrive...)" value={form.pdfLink} onChange={(event) => setForm({ ...form, pdfLink: event.target.value })} />
              <textarea className="w-full min-h-28 border border-gray-300 px-3 py-2 text-sm" placeholder="Tom tat" value={form.tomTat} onChange={(event) => setForm({ ...form, tomTat: event.target.value })} />

              <button type="submit" disabled={loading} className="flex w-full items-center justify-center gap-2 bg-[#0a3875] px-4 py-2 text-sm font-semibold text-white hover:bg-blue-900 disabled:opacity-60">
                {editingId ? <Save className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                {editingId ? 'Luu thay doi' : 'Them moi'}
              </button>
            </div>
          </form>

          <div className="bg-white border border-gray-200 shadow-sm">
            <div className="flex items-center justify-between gap-3 border-b border-gray-100 p-4">
              <div>
                <h3 className="font-bold text-[#0a3875]">Danh sach de tai</h3>
                <p className="text-xs text-gray-500 mt-1">{projects.length} ban ghi</p>
              </div>
              <button type="button" className="p-2 border border-gray-200 text-gray-600 hover:text-[#0a3875]" onClick={loadProjects} title="Tai lai">
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>

            {message && <div className="mx-4 mt-4 border border-blue-100 bg-blue-50 p-3 text-sm text-blue-800">{message}</div>}

            <div className="divide-y divide-gray-100">
              {projects.map((project) => (
                <div key={project.id} className="p-4 flex flex-col md:flex-row md:items-start md:justify-between gap-3">
                  <div>
                    <p className="text-sm font-semibold text-gray-900">{project.tenDeTai}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {project.chuNhiem} | {project.linhVuc} | {project.namThucHien}
                    </p>
                  </div>
                  <div className="flex shrink-0 gap-2">
                    <button type="button" className="p-2 border border-gray-200 text-gray-600 hover:text-[#0a3875]" onClick={() => startEdit(project)} title="Sua">
                      <Edit3 className="w-4 h-4" />
                    </button>
                    <button type="button" className="p-2 border border-gray-200 text-gray-600 hover:text-red-700" onClick={() => deleteProject(project)} title="Xoa">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
              {!loading && projects.length === 0 && (
                <div className="p-8 text-center text-sm text-gray-500">Chua co du lieu.</div>
              )}
            </div>
          </div>
        </div>
      )}
    </MainLayout>
  );
}

export default AdminPage;
