const AUDIENCE_LABEL_MAP: Record<string, string> = {
    'Giáo viên': 'Giảng viên',
    'Học sinh': 'Sinh viên',
};

export function normalizeAudienceLabel(value?: string): string {
    if (!value) return '';
    return AUDIENCE_LABEL_MAP[value] ?? value;
}
