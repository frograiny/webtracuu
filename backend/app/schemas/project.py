"""Pydantic schemas cho Research Project API responses."""

from pydantic import BaseModel, Field, validator


class ProjectItem(BaseModel):
    """Schema cho 1 đề tài NCKH trong kết quả trả về."""
    id: str
    tenDeTai: str
    chuNhiem: str
    doiTuong: str
    linhVuc: str | None = None
    namThucHien: int | None = None
    trangThai: str | None = None
    tomTat: str | None = None
    tuKhoa: list[str] = Field(default_factory=list)
    loaiTaiLieu: str | None = None
    namTrienKhai: int | None = None
    pdfLink: str | None = None

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    """Schema cho tạo mới một đề tài NCKH."""
    tenDeTai: str = Field(..., min_length=10, max_length=500, description="Tiêu đề đề tài")
    chuNhiem: str = Field(..., min_length=3, max_length=200, description="Chủ nhiệm đề tài")
    doiTuong: str = Field(..., description="Đối tượng (Sinh viên/Giảng viên/Doanh nghiệp)")
    linhVuc: str = Field(..., min_length=3, max_length=200, description="Lĩnh vực nghiên cứu")
    namThucHien: int = Field(..., ge=2000, le=2030, description="Năm thực hiện")
    trangThai: str = Field(default="Đang thực hiện", description="Trạng thái")
    tomTat: str = Field(default="", max_length=2000, description="Tóm tắt nội dung")
    tuKhoa: list[str] = Field(default_factory=list, description="Từ khóa")
    loaiTaiLieu: str = Field(default="", description="Loại tài liệu")
    namTrienKhai: int | None = Field(default=None, ge=2000, le=2030, description="Năm triển khai")
    pdfLink: str = Field(default="", description="Link tài liệu / PDF")

    @validator("tenDeTai", "chuNhiem", "linhVuc")
    def strip_whitespace(cls, v):
        return v.strip() if v else v


class ProjectUpdate(BaseModel):
    """Schema cho cập nhật một đề tài NCKH."""
    tenDeTai: str | None = Field(None, min_length=10, max_length=500)
    chuNhiem: str | None = Field(None, min_length=3, max_length=200)
    doiTuong: str | None = None
    linhVuc: str | None = Field(None, min_length=3, max_length=200)
    namThucHien: int | None = Field(None, ge=2000, le=2030)
    trangThai: str | None = None
    tomTat: str | None = Field(None, max_length=2000)
    tuKhoa: list[str] | None = None
    loaiTaiLieu: str | None = None
    namTrienKhai: int | None = Field(None, ge=2000, le=2030)
    pdfLink: str | None = None

    @validator("tenDeTai", "chuNhiem", "linhVuc", pre=True)
    def strip_whitespace(cls, v):
        return v.strip() if v else v


class SearchData(BaseModel):
    """Wrapper cho kết quả tìm kiếm."""
    total: int
    items: list[ProjectItem]


class SearchResponse(BaseModel):
    """Response chuẩn cho endpoint search."""
    status: str = "success"
    data: SearchData


class ProjectDetailResponse(BaseModel):
    """Response cho endpoint chi tiết 1 đề tài."""
    status: str = "success"
    data: ProjectItem


class FilterData(BaseModel):
    """Dữ liệu bộ lọc."""
    fields: list[str]
    years: list[str]
    audiences: list[str]
    documentTypes: list[str] = Field(default_factory=list)


class FilterResponse(BaseModel):
    """Response cho endpoint filters."""
    status: str = "success"
    data: FilterData
