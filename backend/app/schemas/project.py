"""Pydantic schemas cho Research Project API responses."""

from pydantic import BaseModel, Field


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

    class Config:
        from_attributes = True


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
