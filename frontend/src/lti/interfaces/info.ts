export interface UserInfo {
    userId: string;
    roles: string[];
    name?: string;
}

export interface CourseInfo {
    id: string;
    label: string;
    title: string;
}

export interface PlatformInfo {
    guid: string;
    name: string;
    version: string;
    product_family_code: string;
}